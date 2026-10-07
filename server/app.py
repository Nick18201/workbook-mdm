"""
FastAPI Server for Marge de Manœuvre Workbook Generator.
"""

import io
import os
import sys
import logging
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
    TemplateInfo,
)
from server.gemini_service import (
    parse_notes_with_gemini,
    refine_spec_with_gemini,
    customize_spec_with_gemini,
)
from server.pdf_compiler import compile_workbook_from_spec
from server.predefined_workbooks import (
    get_predefined_info_list,
    get_predefined_spec,
)

app = FastAPI(

    title="MDM Workbook Generator API",
    description="Générateur de livrets pédagogiques PDF piloté par IA pour Marge de Manœuvre",
    version="1.0.0",
)

# Pas de CORS : l'interface est servie par cette même application (même origine).

_FIELD_LABELS = {
    "raw_notes": "Notes de séance",
    "feedback": "Consigne d'ajustement",
    "chapter_title": "Titre du chapitre",
    "beneficiary_name": "Nom du bénéficiaire",
    "beneficiary_context": "Contexte du bénéficiaire",
    "custom_instructions": "Consignes spécifiques",
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


@app.post("/api/parse", response_model=WorkbookSpec)
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


@app.post("/api/iterate", response_model=IterateResponse)
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


@app.get("/api/templates", response_model=list[TemplateInfo])
def api_list_templates():
    """
    Retourne la liste des livrets de référence pré-intégrés (MDM Bilan de Compétences & Business Plan).
    """
    return get_predefined_info_list()


@app.get("/api/templates/{template_id}", response_model=WorkbookSpec)
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


@app.post("/api/customize", response_model=CustomizeResponse)
def api_customize_workbook(request: CustomizeRequest, response: Response):
    """
    Personnalise un livret existant pour un bénéficiaire selon son profil et les consignes du coach.
    """
    if request.base_spec is None and not get_predefined_spec(request.template_id):
        raise HTTPException(
            status_code=404,
            detail=f"Modèle de livret '{request.template_id}' introuvable.",
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
        filename = (
            f"Workbook_Chapitre_{spec.chapter_num}.pdf"
            if spec.chapter_num
            else "Workbook.pdf"
        )
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error("Erreur lors de la compilation du PDF : %s", e, exc_info=True)
        raise _internal_error("La compilation du PDF")


@app.post("/api/quick-generate")
def api_quick_generate(request: ParseRequest):
    """
    One-shot: Parses raw notes with Gemini and compiles the PDF directly in a single call.
    """
    try:
        spec, fallback_reason = parse_notes_with_gemini(request)
        pdf_bytes = compile_workbook_from_spec(spec)
        filename = f"Workbook_Chapitre_{spec.chapter_num}.pdf"
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
