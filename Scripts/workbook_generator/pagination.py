"""
The page breaks of a generated document, set as our carnets set theirs (feuille de route,
section 5): a page whose blocks fit on one PDF page loses its breaks, and an exercise
whose « (suite) » page holds almost nothing is cut again, between two blocks, into pages
about as full as each other. Each try compiles the page alone (about 10 ms).

The reference workbooks are cut by hand: only documents Gemini writes, or the fallbacks
of the app, go through here, never a customized carnet.
"""

from itertools import combinations
from math import comb

from .compiler import workbook_page_fills
from .conformity import CONTINUATION_MIN_SHARE
from .spec import BlockSpec, PageSpec, WorkbookSpec

# Blocks that announce what follows them: a page never ends on one
LEADING_BLOCKS = {"heading", "paragraphs", "text", "protocol"}
# Beyond this many ways to cut a page, it keeps its own breaks
MAX_TRIES = 200


def _fills(page: PageSpec) -> list:
    """How full each PDF page of this spec page is, the page compiled alone."""
    return [fill["used"] for fill in workbook_page_fills(WorkbookSpec(pages=[page]))]


def _cut(page: PageSpec, blocks: list, positions: set) -> PageSpec:
    """The page with a page break before each block of `positions`."""
    cut = []
    for k, block in enumerate(blocks):
        if k in positions:
            cut.append(BlockSpec(type="page_break"))
        cut.append(block)
    return page.model_copy(update={"blocks": cut})


def balance_page(page: PageSpec) -> PageSpec:
    """
    A composite page cut into as few PDF pages as its blocks need, each as full as the
    others: without its breaks when it fits on one page, else with the breaks (between two
    blocks, never after an instruction) that leave its emptiest page the fullest. A page
    whose pages are all filled beyond CONTINUATION_MIN_SHARE keeps its own breaks.
    """
    blocks = [b for b in page.blocks or [] if b.type != "page_break"]
    if page.template != "composite" or page.fixed or not blocks:
        return page
    whole = page.model_copy(update={"blocks": blocks})
    whole_fills = _fills(whole)
    if len(whole_fills) == 1:
        return whole
    fills = _fills(page) if len(blocks) < len(page.blocks) else whole_fills
    if min(fills) >= CONTINUATION_MIN_SHARE:
        return page

    best, best_score = (whole, min(whole_fills)) if min(whole_fills) > min(fills) else (page, min(fills))
    breaks = len(whole_fills) - 1
    positions = [k for k in range(1, len(blocks)) if blocks[k - 1].type not in LEADING_BLOCKS]
    if len(positions) < breaks or comb(len(positions), breaks) > MAX_TRIES:
        return best
    for cut in combinations(positions, breaks):
        candidate = _cut(page, blocks, set(cut))
        tried = _fills(candidate)
        if len(tried) == len(whole_fills) and min(tried) > best_score:
            best, best_score = candidate, min(tried)
    return best


def balance_breaks(spec: WorkbookSpec) -> WorkbookSpec:
    """Every composite page of a generated document, cut by balance_page."""
    return spec.model_copy(update={"pages": [balance_page(page) for page in spec.pages]})
