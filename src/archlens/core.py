"""Pure logic (no MCP dependency) so it is easy to test."""
from __future__ import annotations
import os
import re
from datetime import date
from pathlib import Path

import yaml

RULES_DIR = Path(__file__).parent / "rules"


def adr_dir() -> Path:
    d = Path(os.environ.get("ARCHLENS_ADR_DIR", "docs/adr"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_rules(extra_dir: str | None = None) -> list[dict]:
    """Load built-in packs plus optional custom packs from ARCHLENS_RULES_DIR."""
    dirs = [RULES_DIR]
    extra = extra_dir or os.environ.get("ARCHLENS_RULES_DIR")
    if extra:
        dirs.append(Path(extra))
    rules: list[dict] = []
    for d in dirs:
        for f in sorted(d.glob("*.yaml")):
            rules += yaml.safe_load(f.read_text(encoding="utf-8")).get("rules", [])
    return rules


def list_domains() -> list[str]:
    return sorted({r["domain"] for r in load_rules()})


def get_rules(domain: str = "general") -> list[dict]:
    wanted = {"general", domain.lower()}
    return [r for r in load_rules() if r["domain"] in wanted]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "untitled"


def create_adr(title: str, context: str, decision: str, consequences: str,
               alternatives: str = "", status: str = "Proposed") -> str:
    d = adr_dir()
    n = len(list(d.glob("[0-9][0-9][0-9][0-9]-*.md"))) + 1
    path = d / f"{n:04d}-{slugify(title)}.md"
    body = (
        f"# {n}. {title}\n\nDate: {date.today()}\nStatus: {status}\n\n"
        f"## Context\n{context}\n\n## Decision\n{decision}\n\n"
        + (f"## Alternatives considered\n{alternatives}\n\n" if alternatives else "")
        + f"## Consequences\n{consequences}\n"
    )
    path.write_text(body, encoding="utf-8")
    return str(path)


def list_adrs() -> list[str]:
    return [p.name for p in sorted(adr_dir().glob("[0-9][0-9][0-9][0-9]-*.md"))]


def read_adr(name: str) -> str:
    p = adr_dir() / Path(name).name  # basename only: blocks path traversal
    if not p.exists():
        raise FileNotFoundError(name)
    return p.read_text(encoding="utf-8")


def review_checklist(design: str, domain: str = "general") -> dict:
    """Pair the design text with applicable rules. Keyword hits are a cheap hint;
    the LLM makes the actual pass/fail judgement."""
    text = design.lower()
    items = []
    for r in get_rules(domain):
        kws = [k.lower() for k in r.get("keywords", [])]
        hits = [k for k in kws if k in text]
        items.append({
            "id": r["id"], "severity": r.get("severity", "medium"),
            "check": r["check"], "keyword_hits": hits,
            "likely_gap": bool(kws) and not hits,
        })
    return {
        "domain": domain,
        "instructions": ("For each item decide PASS / FAIL / UNKNOWN using the design text. "
                         "Cite evidence. 'likely_gap' is only a keyword hint."),
        "items": items,
        "design": design,
    }
