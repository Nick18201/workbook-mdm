"""
FastAPI Server for Marge de Manœuvre Workbook Generator.
"""

import io
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

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

from server.models import WorkbookSpec, ParseRequest
from server.gemini_service import parse_notes_with_gemini
from server.pdf_compiler import compile_workbook_from_spec

app = FastAPI(
    title="MDM Workbook Generator API",
    description="Générateur de livrets pédagogiques PDF piloté par IA pour Marge de Manœuvre",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Cloud Run health check."""
    return {"status": "ok", "service": "mdm-workbook-generator"}


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
def api_parse_notes(request: ParseRequest):
    """
    Transforms raw notes into a structured WorkbookSpec using Gemini Flash.
    """
    try:
        spec = parse_notes_with_gemini(request)
        return spec
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse IA : {str(e)}"
        )


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
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la compilation du PDF : {str(e)}",
        )


@app.post("/api/quick-generate")
def api_quick_generate(request: ParseRequest):
    """
    One-shot: Parses raw notes with Gemini and compiles the PDF directly in a single call.
    """
    try:
        spec = parse_notes_with_gemini(request)
        pdf_bytes = compile_workbook_from_spec(spec)
        filename = f"Workbook_Chapitre_{spec.chapter_num}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la génération : {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=True)
