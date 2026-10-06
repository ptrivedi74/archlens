from mcp.server.fastmcp import FastMCP
from . import core

mcp = FastMCP("archlens")


@mcp.tool()
def create_adr(title: str, context: str, decision: str, consequences: str,
               alternatives: str = "", status: str = "Proposed") -> str:
    """Create a numbered Architecture Decision Record (Markdown) and return its path."""
    return core.create_adr(title, context, decision, consequences, alternatives, status)


@mcp.tool()
def list_adrs() -> list[str]:
    """List existing ADR files."""
    return core.list_adrs()


@mcp.tool()
def read_adr(name: str) -> str:
    """Read an ADR by file name."""
    return core.read_adr(name)


@mcp.tool()
def list_domains() -> list[str]:
    """List available rule-pack domains."""
    return core.list_domains()


@mcp.tool()
def get_review_rules(domain: str = "general") -> list[dict]:
    """Return general + domain rules (e.g. insurance, banking, healthcare, agentic-ai)."""
    return core.get_rules(domain)


@mcp.tool()
def review_design(design: str, domain: str = "general") -> dict:
    """Return a rule checklist paired with the design text for the LLM to evaluate."""
    return core.review_checklist(design, domain)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
