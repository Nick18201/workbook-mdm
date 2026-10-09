"""
Essais du vrai Gemini sur les modes de l'app (lot 3, feuille de route section 8).

Chaque fichier de cas/ est une requête de l'API, passée comme l'interface la passe, puis
mesurée : les règles des carnets (/api/check, avec le profil, les notes et la durée demandée),
les pages du PDF, ce qui devait rester tel quel et ce que le cas attend (son « but »). Deux
tirages d'un même cas mesurent la stabilité des réponses.

    python essais-gemini/essais.py                  le plan : appels et jetons estimés, aucun appel
    python essais-gemini/essais.py --secours        tout en mode de secours : ni clé ni dépense
    python essais-gemini/essais.py --vrai --serie 1 --tirages 2 --plafond 220000

Avec --vrai, la clé GEMINI_API_KEY vient de l'environnement ou d'un .env (le dossier courant,
server/, puis la copie principale du dépôt) et n'est jamais affichée. Le script s'arrête au
premier échec de Gemini, et avant un cas qui dépasserait le plafond de jetons. Les maquettes et
les PDF vont dans sorties/ (hors de git), le rapport dans rapports/ (avec --vrai seulement).
À lancer depuis la racine du dépôt.
"""

import argparse
import difflib
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for _path in (ROOT, ROOT / "Scripts"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

CHARS_PER_TOKEN = 3.5  # du français et du JSON mêlés, pour les estimations
# Recalés sur la série 1 du 9 octobre 2026 (14 appels) : les réponses dépassent de 15 % la taille
# de la maquette envoyée, et la réflexion du modèle ajoute environ un quart des jetons reçus
RECEIVED_FACTOR = 1.15
THINKING_SHARE = 0.25
GUESSED_SPEC_CHARS = 15_000  # un document créé, pour estimer une retouche avant de l'avoir
FEEDBACK_MAX = 4800  # comme « Corriger ces points » dans l'interface
REF = "_ref"
FIX = "à corriger"


class Stop(Exception):
    """Gemini a échoué, ou le plafond de jetons serait dépassé : on n'appelle plus."""


# --- La clé -------------------------------------------------------------------------------

def _env_files():
    yield Path(".env")
    yield Path("server") / ".env"
    try:
        common = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True,
                                check=True, cwd=ROOT).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return
    main = (ROOT / common).resolve().parent  # la copie principale du dépôt, depuis un worktree
    yield main / ".env"
    yield main / "server" / ".env"


def load_key() -> bool:
    """Met GEMINI_API_KEY (et GEMINI_MODELS) dans l'environnement, sans jamais les afficher."""
    for path in _env_files():
        if os.environ.get("GEMINI_API_KEY"):
            break
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                key, sep, value = line.strip().partition("=")
                if sep and key.strip() in ("GEMINI_API_KEY", "GEMINI_MODELS"):
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return bool(os.environ.get("GEMINI_API_KEY"))


# --- Les cas ------------------------------------------------------------------------------

def load_cases(serie=None, ids=None) -> list:
    """Les cas de cas/, dans l'ordre de leurs fichiers (« 03-creation.json » : le cas « creation »)."""
    cases = []
    for path in sorted((HERE / "cas").glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        case["id"] = path.stem.split("-", 1)[1]
        if (serie is None or case["serie"] == serie) and (not ids or case["id"] in ids):
            cases.append(case)
    return cases


def _source_size(case) -> int:
    """La taille de la maquette dont part une retouche : celle d'un lancement réel, sinon une estimation."""
    name = f"{case['depuis']}-t{case.get('depuis_tirage', 1)}.json"
    for run in sorted((HERE / "sorties").glob("*"), reverse=True):
        if not run.name.endswith("secours") and (run / name).is_file():
            spec = json.loads((run / name).read_text(encoding="utf-8"))["spec"]
            return len(json.dumps(spec, ensure_ascii=False))
    return GUESSED_SPEC_CHARS


def estimate(case) -> tuple:
    """Les appels d'un tirage, et les jetons envoyés, reçus et de réflexion estimés, sans appeler Gemini."""
    from server import gemini_service as gs
    from server.models import CustomizeRequest, ParseRequest

    prompts, received = [], []
    request = case.get("requete") or {}
    real, key = gs._generate_json, os.environ.get("GEMINI_API_KEY")
    gs._generate_json = lambda api_key, system, user, build, label: prompts.append((len(system), len(user)))
    os.environ["GEMINI_API_KEY"] = "factice"  # aucun client n'est créé : _generate_json est remplacé
    try:
        if case["mode"] == "parse":
            gs.parse_notes_with_gemini(ParseRequest(**request))
            received.append(GUESSED_SPEC_CHARS)
        elif case["mode"] == "customize":
            for part in case.get("parties") or [None]:
                gs.customize_spec_with_gemini(CustomizeRequest(**dict(request, part=part)))
                received.append(prompts[-1][1])  # la maquette revient, à peu près de la même taille
        else:
            size = _source_size(case)
            prompts.append((len(gs.ITERATE_SYSTEM_PROMPT), size + FEEDBACK_MAX // 2))
            received.append(size + 1500)
    finally:
        gs._generate_json = real
        if key is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = key
    sent = sum(system + user for system, user in prompts) / CHARS_PER_TOKEN
    answers = sum(received) / CHARS_PER_TOKEN * RECEIVED_FACTOR
    return len(prompts), round(sent), round(answers), round(answers * THINKING_SHARE)


# --- Ce que l'on observe pendant un appel -------------------------------------------------

class UsageLog(logging.Handler):
    """Les jetons de chaque appel, que gemini_service inscrit au journal d'uvicorn."""

    def __init__(self):
        super().__init__(logging.INFO)
        self.calls = []

    def emit(self, record):
        usage = getattr(record, "gemini_usage", None)
        if usage:
            self.calls.append(usage)


def _strip(value):
    if isinstance(value, dict):
        return {k: _strip(v) for k, v in value.items() if k != REF}
    if isinstance(value, list):
        return [_strip(v) for v in value]
    return value


def _pairs(base_items, out_items, kind):
    """Chaque élément de base et sa réponse, appariés comme keep_fixed le fait (par '_ref', ou par position)."""
    outs = [o for o in out_items or [] if isinstance(o, dict)]
    by_ref = {o[REF]: o for o in outs if o.get(REF)}
    if len(outs) == len(base_items):
        for b, o in zip(base_items, outs):
            if not o.get(REF) and o.get(kind) == b.get(kind):
                by_ref.setdefault(b[REF], o)
    return [(b, by_ref.get(b[REF])) for b in base_items]


def fixed_changes(base: dict, out: dict) -> dict:
    """Ce que Gemini a changé ou perdu de ce qui est fixe, avant que keep_fixed ne le rétablisse."""
    from workbook_generator.spec import FIXED_BLOCK_TYPES

    changed, lost = [], []

    def note(b, o):
        if o is None:
            lost.append(b[REF])
        elif _strip(o) != _strip(b):
            changed.append(b[REF])

    for page, out_page in _pairs(base.get("pages") or [], out.get("pages") or [], "template"):
        if page.get("fixed"):
            note(page, out_page)
            continue
        for block, out_block in _pairs(page.get("blocks") or [], (out_page or {}).get("blocks") or [], "type"):
            if block.get("fixed") or block.get("type") in FIXED_BLOCK_TYPES:
                note(block, out_block)
    return {"modifies": changed, "perdus": lost}


FIXED_LOG = []


def _watching(keep_fixed):
    def watched(base, out):
        FIXED_LOG.append(fixed_changes(base, out if isinstance(out, dict) else {}))
        return keep_fixed(base, out)
    return watched


# --- Les mesures --------------------------------------------------------------------------

def _texts(value) -> list:
    """Les textes d'une maquette : les chaînes qui ont une espace (pas les identifiants)."""
    if isinstance(value, dict):
        return [t for v in value.values() for t in _texts(v)]
    if isinstance(value, list):
        return [t for v in value for t in _texts(v)]
    return [value] if isinstance(value, str) and " " in value.strip() else []


def adaptable_texts(spec: dict) -> list:
    """Les textes qu'une personnalisation peut changer : hors des pages et des blocs fixes."""
    from workbook_generator.spec import FIXED_BLOCK_TYPES

    texts = []
    for page in spec.get("pages") or []:
        if page.get("fixed"):
            continue
        texts += _texts({k: v for k, v in page.items() if k != "blocks"})
        for block in page.get("blocks") or []:
            if not (block.get("fixed") or block.get("type") in FIXED_BLOCK_TYPES):
                texts += _texts(block)
    return texts


def _blocks(spec: dict, *types) -> list:
    return [b for p in spec.get("pages") or [] for b in p.get("blocks") or [] if b.get("type") in types]


def _examples(value) -> list:
    """Les exemples contrastés (métier : en surface → exploitable) et les « example » des questions."""
    found = []
    if isinstance(value, dict):
        if value.get("type") == "contrast_example":
            found.append(f"{value.get('title', '')} : « {value.get('surface', '')} » → « {value.get('exploitable', '')} »")
        elif isinstance(value.get("example"), str) and value["example"].strip():
            found.append(value["example"])
        for v in value.values():
            found += _examples(v)
    elif isinstance(value, list):
        for v in value:
            found += _examples(v)
    return found


def _shape(spec: dict) -> list:
    """La suite des gabarits et des blocs, pour comparer deux tirages."""
    shape = []
    for page in spec.get("pages") or []:
        shape.append(page.get("template", "?"))
        shape += ["· " + str(block.get("type")) for block in page.get("blocks") or []]
    return shape


def _page_key(page) -> str:
    return json.dumps(_strip(page), sort_keys=True, ensure_ascii=False)


def measure_created(spec: dict) -> dict:
    pages = spec.get("pages") or []
    summary = next((p.get("params") or {} for p in pages if p.get("template") == "summary"), {})
    eyebrows = []
    for page in pages:
        eyebrow = page.get("part_title") or ""
        if eyebrow.startswith("Exercice") and eyebrow not in eyebrows:
            eyebrows.append(eyebrow)
    return {
        "gabarit": " → ".join(p.get("template", "?") for p in pages),
        "sourcils": eyebrows,
        "ouverture": summary.get("points"),
        "duree": summary.get("duration"),
        "meteo": len(_blocks(spec, "energy")),
        "annonces": len(_blocks(spec, "protocol")),
        "ancrages": len(_blocks(spec, "anchor")),
        "exemples": _examples(spec),
        "prenom": spec.get("beneficiary_name"),
    }


def measure_customized(base: dict, spec: dict, fixed_log: list) -> dict:
    gaps = []
    base_pages, pages = base.get("pages") or [], spec.get("pages") or []
    if len(base_pages) != len(pages):
        gaps.append(f"{len(base_pages)} pages → {len(pages)}")
    for i, (b, o) in enumerate(zip(base_pages, pages), start=1):
        if b.get("template") != o.get("template"):
            gaps.append(f"p. {i} : {b.get('template')} → {o.get('template')}")
            continue
        before = [x.get("type") for x in b.get("blocks") or []]
        after = [x.get("type") for x in o.get("blocks") or []]
        if before != after:
            gaps.append(f"p. {i} : blocs {', '.join(before)} → {', '.join(after)}")
    before, after = adaptable_texts(base), set(adaptable_texts(spec))
    rewritten = sum(text not in after for text in before) / max(len(before), 1)
    return {
        "structure": gaps,
        "fixes_modifies": [ref for log in fixed_log for ref in log["modifies"]],
        "fixes_perdus": [ref for log in fixed_log for ref in log["perdus"]],
        "part_reecrite": round(rewritten, 2),
        "exemples": _examples(spec),
        "prenom": spec.get("beneficiary_name"),
    }


def fixed_altered(before: dict, spec: dict) -> list:
    """Les pages et les blocs fixes de `before` qui ont changé dans `spec` (appariés par position)."""
    from workbook_generator.spec import FIXED_BLOCK_TYPES

    altered = []
    for i, (page, out) in enumerate(zip(before.get("pages") or [], spec.get("pages") or []), start=1):
        if page.get("fixed"):
            if _page_key(page) != _page_key(out):
                altered.append(f"p{i}")
            continue
        blocks, out_blocks = page.get("blocks") or [], out.get("blocks") or []
        if [b.get("type") for b in blocks] != [b.get("type") for b in out_blocks]:
            continue  # des blocs ajoutés ou retirés : la position ne dit plus rien
        for k, (block, out_block) in enumerate(zip(blocks, out_blocks), start=1):
            if (block.get("fixed") or block.get("type") in FIXED_BLOCK_TYPES) and _page_key(block) != _page_key(out_block):
                altered.append(f"p{i}.b{k}")
    return altered


def measure_retouch(before: dict, spec: dict) -> dict:
    old_pages = {_page_key(p) for p in before.get("pages") or []}
    kept = sum(_page_key(p) in old_pages for p in spec.get("pages") or [])
    old_tables = {_page_key(t) for t in _blocks(before, "table")}
    tables = []
    for table in _blocks(spec, "table"):
        if _page_key(table) in old_tables:
            continue
        rows = table.get("rows") or []
        cells = [cell for row in rows for cell in row[1:]]
        text = json.dumps(table, ensure_ascii=False)
        tables.append({
            "en_tetes": table.get("headers"),
            "lignes": len(rows),
            "paliers_30_60_90": all(n in text for n in ("30", "60", "90")),
            "toutes_les_cases": bool(cells) and all(isinstance(c, dict) and c.get("field_id") for c in cells),
        })
    return {
        "pages_identiques": f"{kept}/{len(before.get('pages') or [])}",
        "nouveaux_tableaux": tables,
        "gabarit_roadmap": sum(p.get("template") == "roadmap" for p in spec.get("pages") or []),
        "fixes_changes": fixed_altered(before, spec),
    }


def fixes_text(findings: list) -> str:
    """La consigne que « Corriger ces points » range dans « Ajuster »."""
    text = "Corrige ces points relevés par le contrôle des règles des carnets, sans rien changer d'autre :"
    for f in findings:
        line = f"\n- {f'Page {f['page']} : ' if f.get('page') else ''}{f['message']}"
        if len(text) + len(line) > FEEDBACK_MAX:
            break
        text += line
    return text


def measure_fixes(source_findings: list, findings: list, before: dict, spec: dict) -> dict:
    after = {f["message"] for f in findings}
    old_pages = {_page_key(p) for p in before.get("pages") or []}
    return {
        "avant": len(source_findings),
        "apres": len(findings),
        "restees": [f["message"] for f in source_findings if f["message"] in after],
        "nouvelles": [f["message"] for f in findings if f["message"] not in {s["message"] for s in source_findings}],
        "pages_identiques": f"{sum(_page_key(p) in old_pages for p in spec.get('pages') or [])}/{len(before.get('pages') or [])}",
        "fixes_changes": fixed_altered(before, spec),
    }


def verdict(result: dict) -> str:
    """Ce que le cas attend, en quelques mots, pour le tableau du rapport."""
    m, mode = result["mesures"], result["mode"]
    if mode == "customize":
        structure = "structure gardée" if not m["structure"] else f"{len(m['structure'])} écart(s) de structure"
        return (f"{structure} ; fixe : {len(m['fixes_modifies'])} modifié(s), {len(m['fixes_perdus'])} perdu(s), "
                f"rétablis ; {round(m['part_reecrite'] * 100)} % des textes réécrits")
    if mode == "parse":
        return (f"{len(m['sourcils'])} exercices, {m['duree']} ; météo {m['meteo']}, annonces {m['annonces']}, "
                f"ancrages {m['ancrages']}")
    if mode == "iterate":
        tables = m["nouveaux_tableaux"]
        if not tables:
            return "aucun tableau ajouté" + (" (gabarit roadmap)" if m["gabarit_roadmap"] else "")
        t = tables[0]
        return (f"tableau de {t['lignes']} lignes, paliers 30-60-90 {'oui' if t['paliers_30_60_90'] else 'non'}, "
                f"toutes les cases {'oui' if t['toutes_les_cases'] else 'non'} ; pages identiques {m['pages_identiques']}"
                f" ; fixe changé : {len(m['fixes_changes'])}")
    return (f"remarques {m['avant']} → {m['apres']} ; pages identiques {m['pages_identiques']} ; "
            f"fixe changé : {len(m['fixes_changes'])}")


# --- Un cas, un tirage --------------------------------------------------------------------

def _post(client, url, body):
    response = client.post(url, json=body)
    if response.status_code != 200:
        raise RuntimeError(f"{url} : {response.status_code} {response.text[:300]}")
    return response


def _generation(responses) -> tuple:
    for response in responses:
        if response.headers.get("X-MDM-Generation") == "fallback":
            return "fallback", response.headers.get("X-MDM-Fallback-Reason")
    return "ai", None


def run_one(client, usage, case, tirage, source=None) -> dict:
    """Passe le cas comme l'interface, puis le mesure. `source` : le résultat d'un cas « depuis »."""
    from workbook_generator.spec import load_workbook

    mode, request = case["mode"], dict(case.get("requete") or {})
    first_call = len(usage.calls)
    FIXED_LOG.clear()
    responses, summaries, base = [], [], None
    started = time.monotonic()
    if mode == "parse":
        responses.append(_post(client, "/api/parse", request))
        spec = responses[-1].json()
        control = {"sources": request["raw_notes"], "duration_min": request.get("duration_min")}
    elif mode == "customize":
        spec = None
        for part in case.get("parties") or [None]:  # comme l'interface : chaque partie part du résultat précédent
            body = dict(request, part=part)
            if spec is not None:
                body.update(template_id=None, base_spec=spec)
            responses.append(_post(client, "/api/customize", body))
            spec = responses[-1].json()["spec"]
            summaries.append(responses[-1].json().get("customizations_summary"))
        control = {"context": request["beneficiary_context"]}
        base = load_workbook(request["template_id"]).model_dump(exclude_unset=True, exclude_none=True)
    else:
        base = source["spec"]
        request["feedback"] = request.get("feedback") or fixes_text(source["remarques"])
        request["raw_notes"] = (source.get("requete") or {}).get("raw_notes")
        responses.append(_post(client, "/api/iterate", dict(request, current_spec=base)))
        spec = responses[-1].json()["spec"]
        summaries.append(responses[-1].json().get("changes_summary"))
        control = source["controle"]
    seconds = time.monotonic() - started
    generation, reason = _generation(responses)

    findings = _post(client, "/api/check", dict(control, spec=spec, structure=True, layout=True)).json()
    page_count = _post(client, "/api/page-count", spec).json()["page_count"]
    if mode == "parse":
        measures = measure_created(spec)
    elif mode == "customize":
        measures = measure_customized(base, spec, list(FIXED_LOG))
    elif mode == "iterate":
        measures = measure_retouch(base, spec)
    else:
        measures = measure_fixes(source["remarques"], findings, base, spec)
    calls = usage.calls[first_call:]
    result = {
        "cas": case["id"], "titre": case["titre"], "but": case.get("but"), "mode": mode, "tirage": tirage,
        "generation": generation, "raison": reason, "secondes": round(seconds, 1),
        "appels": calls, "jetons": {kind: sum(c[kind] for c in calls) for kind in ("prompt", "candidates", "thoughts")},
        "pages_pdf": page_count, "remarques": findings, "resume": summaries, "mesures": measures,
        "requete": request, "controle": control, "spec": spec,
    }
    result["verdict"] = verdict(result)
    return result


# --- Un lancement -------------------------------------------------------------------------

def _spent(result) -> int:
    return sum(result["jetons"].values())


def _find_source(case_id, results, outdir, vrai, tirage=1):
    """
    Un tirage (le 1er par défaut) d'un cas « depuis » : de ce lancement, sinon (avec le vrai
    Gemini) du plus récent lancement réel de sorties/. En secours, tout tirage de ce lancement fait l'affaire.
    """
    same = [result for result in results if result["cas"] == case_id]
    for result in same:
        if result["tirage"] == tirage:
            return result
    if not vrai:
        if same:
            return same[0]
        raise Stop(f"le cas « {case_id} » n'a pas encore tourné : lancez-le avant celui qui en part")
    runs = sorted((p for p in (HERE / "sorties").glob("*") if p.is_dir() and p != outdir), reverse=True)
    for run in runs:
        if run.name.endswith("secours"):
            continue
        path = run / f"{case_id}-t{tirage}.json"
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    raise Stop(f"le cas « {case_id} » n'a pas encore tourné : lancez-le avant celui qui en part")


def run(cases, outdir, tirages=1, vrai=False, plafond=None, pdf=True) -> list:
    """
    Chaque cas, `tirages` fois ; ses maquettes (et ses PDF) dans `outdir`. Avec vrai=False, la
    clé est retirée de l'environnement : tout passe en secours.
    """
    from fastapi.testclient import TestClient

    from server import gemini_service as gs
    from server.app import app
    from workbook_generator.compiler import compile_workbook_from_spec
    from workbook_generator.spec import WorkbookSpec

    if not vrai:
        os.environ.pop("GEMINI_API_KEY", None)  # server.app charge un .env : pas d'appel en secours
    usage = UsageLog()
    log = logging.getLogger("uvicorn.error")
    log.setLevel(logging.INFO)
    log.addHandler(usage)
    real_keep_fixed = gs.keep_fixed
    gs.keep_fixed = _watching(real_keep_fixed)
    client = TestClient(app)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    results, spent = [], 0
    try:
        for case in cases:
            calls, sent, received, thinking = estimate(case)
            for tirage in range(1, tirages + 1):
                if plafond and spent + sent + received + thinking > plafond:
                    raise Stop(f"plafond : {spent} jetons dépensés, le cas « {case['id']} » en demanderait "
                               f"~{sent + received + thinking} de plus (plafond {plafond})")
                source = (_find_source(case["depuis"], results, outdir, vrai, case.get("depuis_tirage", 1))
                          if case.get("depuis") else None)
                result = run_one(client, usage, case, tirage, source)
                results.append(result)
                spent += _spent(result)
                (outdir / f"{case['id']}-t{tirage}.json").write_text(
                    json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
                if pdf:
                    compile_workbook_from_spec(WorkbookSpec(**result["spec"]), str(outdir / f"{case['id']}-t{tirage}.pdf"))
                fixes = sum(f["level"] == FIX for f in result["remarques"])
                print(f"{case['id']}, tirage {tirage} : {result['generation']}, {result['secondes']} s, "
                      f"{_spent(result)} jetons, {result['pages_pdf']} pages, {fixes} à corriger, "
                      f"{len(result['remarques']) - fixes} à vérifier ; {result['verdict']}", flush=True)
                if vrai and result["generation"] != "ai":
                    raise Stop(f"Gemini a échoué sur « {case['id']} » ({result['raison']})")
    except Stop as stop:
        print(f"Arrêt : {stop}", flush=True)
    finally:
        gs.keep_fixed = real_keep_fixed
        log.removeHandler(usage)
    return results


# --- Le rapport ---------------------------------------------------------------------------

def _n(value) -> str:
    return f"{value:,}".replace(",", " ")


def _s(seconds) -> str:
    return f"{seconds} s".replace(".", ",")


def _d(value) -> str:
    return str(value).replace(".", ",")


def stability(results) -> list:
    """Pour chaque cas tiré deux fois : ce qui change d'un tirage à l'autre."""
    rows = []
    by_case = {}
    for result in results:
        by_case.setdefault(result["cas"], []).append(result)
    for case_id, draws in by_case.items():
        if len(draws) < 2:
            continue
        a, b = draws[0], draws[1]
        shape = difflib.SequenceMatcher(None, _shape(a["spec"]), _shape(b["spec"])).ratio()
        texts_a, texts_b = set(adaptable_texts(a["spec"])), set(adaptable_texts(b["spec"]))
        common = len(texts_a & texts_b) / max(len(texts_a | texts_b), 1)
        counts = [(sum(f["level"] == FIX for f in d["remarques"]), sum(f["level"] != FIX for f in d["remarques"]))
                  for d in (a, b)]
        rows.append({
            "cas": case_id,
            "pages": f"{a['pages_pdf']} / {b['pages_pdf']}",
            "remarques": " / ".join(f"{fix} + {check}" for fix, check in counts),
            "forme": round(shape, 2),
            "textes_communs": round(common, 2),
            "verdicts": [a["verdict"], b["verdict"]],
        })
    return rows


def report(results, tirages, plafond, vrai) -> str:
    from server.gemini_service import GEMINI_MODELS

    now = datetime.now()
    calls = [c for r in results for c in r["appels"]]
    totals = {kind: sum(c[kind] for c in calls) for kind in ("prompt", "candidates", "thoughts")}
    total = sum(totals.values())
    lines = [
        "# Essais du vrai Gemini" if vrai else "# Essais en mode de secours",
        "",
        f"{now:%d/%m/%Y, %H h %M} · modèle {', '.join(GEMINI_MODELS)} · {tirages} tirage(s) par cas · "
        f"script `essais-gemini/essais.py`",
        "",
        "## Dépense",
        "",
        f"{len(calls)} appels : {_n(totals['prompt'])} jetons envoyés, {_n(totals['candidates'])} reçus, "
        f"{_n(totals['thoughts'])} de réflexion, soit {_n(total)}"
        + (f" (plafond {_n(plafond)})." if plafond else "."),
        "",
        "## Résultats",
        "",
        "| Cas | Tirage | Durée | Jetons | Pages | À corriger | À vérifier | Ce que le cas attend |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        fixes = sum(f["level"] == FIX for f in r["remarques"])
        lines.append(f"| {r['cas']} | {r['tirage']} | {_s(r['secondes'])} | {_n(_spent(r))} | {r['pages_pdf']} | {fixes} "
                     f"| {len(r['remarques']) - fixes} | {r['verdict']} |")
    rows = stability(results)
    if rows:
        lines += ["", "## Stabilité (tirage 1 / tirage 2)", "",
                  "Forme : la ressemblance des suites de gabarits et de blocs (1 : identiques). Textes communs : "
                  "la part des textes adaptables écrits à l'identique dans les deux tirages.", "",
                  "| Cas | Pages | Remarques (à corriger + à vérifier) | Forme | Textes communs |",
                  "|---|---|---|---|---|"]
        for row in rows:
            lines.append(f"| {row['cas']} | {row['pages']} | {row['remarques']} | {_d(row['forme'])} "
                         f"| {_d(row['textes_communs'])} |")
    lines += ["", "## Détail", ""]
    seen = set()
    for r in results:
        if r["cas"] not in seen:
            seen.add(r["cas"])
            lines += [f"### {r['titre']}", "", f"But : {r['but']}", ""]
        lines += [f"**Tirage {r['tirage']}** : {r['generation']}, {_s(r['secondes'])}, {r['pages_pdf']} pages du PDF.", ""]
        for summary in r["resume"]:
            if summary:
                lines.append(f"- Résumé de la réponse : {summary}")
        m = r["mesures"]
        if r["mode"] == "parse":
            lines += [f"- Gabarit : {m['gabarit']}", f"- Sourcils : {' ; '.join(m['sourcils']) or 'aucun'}",
                      f"- Ouverture : {' ; '.join(m['ouverture'] or []) or 'aucune ligne'} (total {m['duree']})",
                      f"- Météo {m['meteo']}, annonces {m['annonces']}, ancrages {m['ancrages']}, prénom {m['prenom'] or 'aucun'}"]
        elif r["mode"] == "customize":
            lines += [f"- Structure : {' ; '.join(m['structure']) or 'gardée'}",
                      f"- Fixe changé par Gemini puis rétabli : {', '.join(m['fixes_modifies']) or 'rien'} ; "
                      f"perdu puis rétabli : {', '.join(m['fixes_perdus']) or 'rien'}",
                      f"- Textes réécrits : {round(m['part_reecrite'] * 100)} % ; prénom : {m['prenom'] or 'aucun'}"]
        elif r["mode"] == "iterate":
            lines += [f"- Pages identiques : {m['pages_identiques']} ; fixe changé : "
                      f"{', '.join(m['fixes_changes']) or 'rien'}",
                      f"- Nouveaux tableaux : {json.dumps(m['nouveaux_tableaux'], ensure_ascii=False) or 'aucun'}"]
        else:
            lines += [f"- Remarques : {m['avant']} → {m['apres']} ; pages identiques : {m['pages_identiques']} ; "
                      f"fixe changé : {', '.join(m['fixes_changes']) or 'rien'}"]
            lines += [f"- Restée : {message}" for message in m["restees"]]
            lines += [f"- Nouvelle : {message}" for message in m["nouvelles"]]
        if r["remarques"]:
            lines.append("- Remarques du contrôle :")
            lines += [f"  - {f'p. {f['page']} · ' if f.get('page') else ''}{f['level']} · {f['rule']} : {f['message']}"
                      for f in r["remarques"]]
        if m.get("exemples"):
            lines.append("- Exemples :")
            lines += [f"  - {example}" for example in m["exemples"]]
        lines.append("")
    return "\n".join(lines)


def print_plan(cases, tirages):
    totals = [0, 0, 0, 0]
    print(f"Plan : {len(cases)} cas × {tirages} tirage(s), sans appel (estimation à {CHARS_PER_TOKEN} caractères par jeton)")
    for case in cases:
        estimated = estimate(case)
        totals = [total + value * tirages for total, value in zip(totals, estimated)]
        calls, sent, received, thinking = estimated
        print(f"- {case['id']} ({case['mode']}) : {calls} appel(s) par tirage, ~{_n(sent)} jetons envoyés, "
              f"~{_n(received)} reçus, ~{_n(thinking)} de réflexion")
    calls, sent, received, thinking = totals
    print(f"Total : {calls} appels, ~{_n(sent)} jetons envoyés, ~{_n(received)} reçus, ~{_n(thinking)} de réflexion, "
          f"soit ~{_n(sent + received + thinking)}.")


def main():
    parser = argparse.ArgumentParser(description="Essais du vrai Gemini sur les modes de l'app (lot 3).")
    parser.add_argument("--vrai", action="store_true", help="appeler le vrai Gemini : une dépense, à annoncer avant")
    parser.add_argument("--secours", action="store_true", help="tout en mode de secours, sans clé ni dépense")
    parser.add_argument("--serie", type=int, help="la série de cas (1 ou 2)")
    parser.add_argument("--cas", nargs="*", help="les cas à passer (ex : reconversion creation)")
    parser.add_argument("--tirages", type=int, default=1, help="tirages par cas (2 pour la stabilité)")
    parser.add_argument("--plafond", type=int, help="jetons au plus, réflexion comprise")
    parser.add_argument("--nom", help="le nom du rapport, après sa date (ex : verification)")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    cases = load_cases(args.serie, args.cas)
    if not cases:
        sys.exit("Aucun cas ne correspond.")
    if not (args.vrai or args.secours):
        print_plan(cases, args.tirages)
        return
    if args.vrai and not load_key():
        sys.exit("Pas de GEMINI_API_KEY (environnement ou .env) : rien n'est appelé.")
    outdir = HERE / "sorties" / (f"{datetime.now():%Y%m%d-%H%M%S}" + ("" if args.vrai else "-secours"))
    results = run(cases, outdir, args.tirages, vrai=args.vrai, plafond=args.plafond)
    if not results:
        return
    text = report(results, args.tirages, args.plafond, args.vrai)
    (outdir / "rapport.md").write_text(text, encoding="utf-8")
    if args.vrai:
        name = f"{datetime.now():%Y-%m-%d}-" + (args.nom or (f"serie-{args.serie}" if args.serie else "cas"))
        path = HERE / "rapports" / f"{name}.md"
        if path.exists():
            path = path.with_name(f"{name}-{datetime.now():%H%M}.md")
        path.parent.mkdir(exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"Rapport : {path.relative_to(ROOT)}")
    print(f"Sorties : {outdir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
