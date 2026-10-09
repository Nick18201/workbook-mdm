"""
FastAPI Server for Marge de Manœuvre Workbook Generator.
"""

import io
import os
import re
import sys
import logging
import unicodedata
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response

logger = logging.getLogger("uvicorn.error")

# Ensure path resolution
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SERVER_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Auto-load .env from project root or server dir if present
for _env_candidate in [os.path.join(PROJECT_ROOT, ".env"), os.path.join(SERVER_DIR, ".env")]:
    if os.path.exists(_env_candidate):
        with open(_env_candidate, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from server.models import (
    WorkbookSpec,
    ParseRequest,
    IterateRequest,
    IterateResponse,
    CustomizeRequest,
    CustomizeResponse,
    CheckRequest,
    CoverageRequest,
    CoverageResponse,
    FindingInfo,
    LayoutRequest,
    LayoutResponse,
    MissingElement,
    PageCountResponse,
    TemplateInfo,
)
from workbook_generator.conformity import check_spec
from workbook_generator.coverage import check_coverage
from workbook_generator.primitives import plain_title
from server.gemini_service import (
    parse_notes_with_gemini,
    refine_spec_with_gemini,
    customize_spec_with_gemini,
    layout_support_with_gemini,
)
from workbook_generator.compiler import compile_workbook_from_spec, workbook_page_count
from server.predefined_workbooks import (
    count_pages_in_background,
    get_predefined_info_list,
    get_predefined_spec,
)


@asynccontextmanager
async def lifespan(app):
    # Le nombre de pages des modèles (/api/templates) se compte en compilant chacun d'eux
    count_pages_in_background()
    yield


app = FastAPI(

    title="MDM Workbook Generator API",
    description="Générateur de livrets pédagogiques PDF piloté par IA pour Marge de Manœuvre",
    version="1.0.0",
    lifespan=lifespan,
)

# Pas de CORS : l'interface est servie par cette même application (même origine).

_FIELD_LABELS = {
    "raw_notes": "Notes de séance",
    "feedback": "Consigne d'ajustement",
    "chapter_title": "Titre du carnet",
    "beneficiary_name": "Nom du bénéficiaire",
    "beneficiary_context": "Contexte du bénéficiaire",
    "custom_instructions": "Consignes spécifiques",
    "source_text": "Texte du support",
}


_ERROR_MESSAGES = {
    "string_too_long": "texte trop long (maximum {max_length} caractères)",
    "too_long": "trop d'éléments (maximum {max_length})",
    "missing": "champ obligatoire",
    "less_than_equal": "doit être inférieur ou égal à {le}",
    "greater_than_equal": "doit être supérieur ou égal à {ge}",
    "greater_than": "doit être supérieur à {gt}",
    "literal_error": "valeur non reconnue (attendu : {expected})",
    "value_error": "{error}",
}


def _describe_validation_error(err):
    """Traduit une erreur Pydantic en une phrase lisible pour l'alerte de l'interface."""
    path = ".".join(str(p) for p in err.get("loc", ()) if p != "body")
    try:
        message = _ERROR_MESSAGES[err["type"]].format(**(err.get("ctx") or {}))
    except (KeyError, IndexError):
        message = err.get("msg", "valeur invalide")
    label = _FIELD_LABELS.get(path, path)
    return f"{label} : {message}" if label else message


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """422 avec un 'detail' textuel (l'interface l'affiche tel quel), sans renvoyer la saisie."""
    messages = [_describe_validation_error(err) for err in exc.errors()[:3]]
    return JSONResponse(
        status_code=422,
        content={"detail": "Requête invalide. " + " ; ".join(messages)},
    )


def _internal_error(action):
    """500 sans détail technique : l'exception est journalisée par l'appelant, pas renvoyée au client."""
    return HTTPException(
        status_code=500,
        detail=f"{action} a échoué (erreur interne, détails dans les journaux du serveur).",
    )


def _slug(text):
    """« Mes enquêtes métiers. » -> « Mes_enquetes_metiers » (an HTTP header takes no accent)."""
    text = unicodedata.normalize("NFKD", plain_title(text or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def _pdf_filename(spec: WorkbookSpec) -> str:
    """The PDF's name: « Carnet_7_… » for a carnet of the bilan, its title otherwise, then the beneficiary."""
    parts = [f"Carnet_{spec.carnet}" if isinstance(spec.carnet, int) else "",
             _slug(spec.chapter_title), _slug(spec.beneficiary_name)]
    return "_".join(part for part in parts if part)[:120] + ".pdf" if any(parts) else "Carnet.pdf"


def _generation_headers(fallback_reason):
    """Signals to the UI whether Gemini answered or the heuristic fallback was used."""
    if not fallback_reason:
        return {"X-MDM-Generation": "ai"}
    return {"X-MDM-Generation": "fallback", "X-MDM-Fallback-Reason": fallback_reason}


@app.get("/health")
def health_check():
    """Cloud Run health check."""
    return {"status": "ok", "service": "mdm-workbook-generator"}


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="8" fill="#2F2EFA"/>
  <text x="16" y="22" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif" font-weight="900" font-size="16" fill="#FFFFFF" text-anchor="middle">M</text>
</svg>"""


@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
    """Serves the MDM brand favicon to prevent 404 logs."""
    return Response(content=FAVICON_SVG, media_type="image/svg+xml")


@app.get("/", response_class=HTMLResponse)
def get_index():
    """Serves the single-page application UI."""
    template_path = os.path.join(SERVER_DIR, "templates", "index.html")
    if not os.path.exists(template_path):
        return HTMLResponse("<h1>Interface non trouvée.</h1>", status_code=404)
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.post("/api/parse", response_model=WorkbookSpec, response_model_exclude_unset=True)
def api_parse_notes(request: ParseRequest, response: Response):
    """
    Transforms raw notes into a structured WorkbookSpec using Gemini Flash.
    """
    try:
        spec, fallback_reason = parse_notes_with_gemini(request)
        response.headers.update(_generation_headers(fallback_reason))
        return spec
    except Exception as e:
        logger.error("Erreur lors de l'analyse IA : %s", e, exc_info=True)
        raise _internal_error("L'analyse des notes")


@app.post("/api/iterate", response_model=IterateResponse, response_model_exclude_unset=True)
def api_iterate_spec(request: IterateRequest, response: Response):
    """
    Refines an existing WorkbookSpec iteratively based on user feedback.
    """
    try:
        result, fallback_reason = refine_spec_with_gemini(request)
        response.headers.update(_generation_headers(fallback_reason))
        return result
    except Exception as e:
        logger.error("Erreur lors de l'itération IA : %s", e, exc_info=True)
        raise _internal_error("L'ajustement du livret")


@app.post("/api/layout", response_model=LayoutResponse, response_model_exclude_unset=True)
def api_layout_support(request: LayoutRequest, response: Response):
    """
    Met en page un support déjà écrit, tel quel : chaque question, consigne et case
    gardée, dans l'ordre ; seules changent la typographie, les mots proscrits et la taille
    des cases. Les ajouts possibles reviennent à part, dans 'suggestions'.
    """
    try:
        result, fallback_reason = layout_support_with_gemini(request)
        response.headers.update(_generation_headers(fallback_reason))
        return result
    except Exception as e:
        logger.error("Erreur lors de la mise en page du support : %s", e, exc_info=True)
        raise _internal_error("La mise en page du support")


@app.get("/api/templates", response_model=list[TemplateInfo])
def api_list_templates():
    """
    Retourne la liste des livrets de référence pré-intégrés (MDM Bilan de Compétences & Business Plan).
    """
    return get_predefined_info_list()


@app.get("/api/templates/{template_id}", response_model=WorkbookSpec, response_model_exclude_unset=True)
def api_get_template_spec(template_id: str):
    """
    Retourne la spécification canonique complète d'un livret modèle.
    """
    spec = get_predefined_spec(template_id)
    if not spec:
        raise HTTPException(
            status_code=404,
            detail=f"Modèle de livret '{template_id}' introuvable.",
        )
    return spec


@app.post("/api/customize", response_model=CustomizeResponse, response_model_exclude_unset=True)
def api_customize_workbook(request: CustomizeRequest, response: Response):
    """
    Personnalise un livret existant pour un bénéficiaire selon son profil et les consignes du consultant :
    tout le livret, ou une seule de ses parties (un long livret se personnalise partie par partie).
    """
    base_spec = request.base_spec if request.base_spec is not None else get_predefined_spec(request.template_id)
    if base_spec is None:
        raise HTTPException(
            status_code=404,
            detail=f"Modèle de livret '{request.template_id}' introuvable.",
        )
    if request.part is not None and not any(page.part == request.part for page in base_spec.pages):
        raise HTTPException(
            status_code=422,
            detail=f"Requête invalide. Partie {request.part} : ce livret n'a aucune page dans cette partie.",
        )
    try:
        result, fallback_reason = customize_spec_with_gemini(request)
        response.headers.update(_generation_headers(fallback_reason))
        return result
    except Exception as e:
        logger.error("Erreur lors de la personnalisation IA : %s", e, exc_info=True)
        raise _internal_error("La personnalisation")


@app.post("/api/compile")
def api_compile_pdf(spec: WorkbookSpec):
    """
    Compiles a WorkbookSpec JSON into a PDF file stream.
    """
    try:
        pdf_bytes = compile_workbook_from_spec(spec)
        filename = _pdf_filename(spec)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error("Erreur lors de la compilation du PDF : %s", e, exc_info=True)
        raise _internal_error("La compilation du PDF")


@app.post("/api/page-count", response_model=PageCountResponse)
def api_page_count(spec: WorkbookSpec):
    """
    Nombre de pages du PDF d'une spécification, pages « (suite) » comprises : le badge de
    l'aperçu, après une génération, une personnalisation, un ajustement ou un import.
    Il faut compiler la spécification (quelques dixièmes de seconde).
    """
    try:
        return PageCountResponse(page_count=workbook_page_count(spec))
    except Exception as e:
        logger.error("Erreur lors du comptage des pages : %s", e, exc_info=True)
        raise _internal_error("Le comptage des pages")


@app.post("/api/check", response_model=list[FindingInfo])
def api_check_spec(request: CheckRequest):
    """
    Contrôle de conformité d'une spécification aux règles de nos carnets (vocabulaire,
    gabarit commun, cases, exemples, protocole) : la liste de l'aperçu, après chaque
    génération, personnalisation, ajustement ou import. Une liste vide : rien à signaler.
    """
    try:
        findings = check_spec(request.spec, structure=request.structure, context=request.context,
                              layout=request.layout)
        return [FindingInfo(**finding._asdict()) for finding in findings]
    except Exception as e:
        logger.error("Erreur lors du contrôle de conformité : %s", e, exc_info=True)
        raise _internal_error("Le contrôle de conformité")


@app.post("/api/coverage", response_model=CoverageResponse)
def api_coverage(request: CoverageRequest):
    """
    Couverture d'un support par sa maquette : chaque question et chaque libellé du support
    retrouvé, dans l'ordre, puis leurs options (« Couverture : 40/40 » sous l'aperçu).
    """
    try:
        coverage = check_coverage(request.spec, request.source_text)
        return CoverageResponse(
            **coverage._asdict() | {"missing": [MissingElement(**m._asdict()) for m in coverage.missing]}
        )
    except Exception as e:
        logger.error("Erreur lors du contrôle de couverture : %s", e, exc_info=True)
        raise _internal_error("Le contrôle de couverture")


@app.post("/api/quick-generate")
def api_quick_generate(request: ParseRequest):
    """
    One-shot: Parses raw notes with Gemini and compiles the PDF directly in a single call.
    """
    try:
        spec, fallback_reason = parse_notes_with_gemini(request)
        pdf_bytes = compile_workbook_from_spec(spec)
        filename = _pdf_filename(spec)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                **_generation_headers(fallback_reason),
            },
        )
    except Exception as e:
        logger.error("Erreur lors de la génération rapide : %s", e, exc_info=True)
        raise _internal_error("La génération")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=True)
