# ArchLens

**An MCP server for AI-assisted architecture governance.** Let any MCP client write Architecture Decision Records and review designs against pluggable, domain-specific rule packs.

## Features
- `create_adr`, `list_adrs`, `read_adr`: numbered Markdown ADRs
- `get_review_rules`, `list_domains`: rule packs for **general, insurance, banking, healthcare, agentic-ai**
- `review_design`: pairs your design with the rule checklist; the LLM returns PASS/FAIL/UNKNOWN with evidence
- Custom packs: set `ARCHLENS_RULES_DIR` to a folder of your own YAML files

## Install
```bash
git clone https://github.com/ptrivedi74/archlens && cd archlens
python -m venv .venv && .venv\Scripts\activate    # Windows
pip install -e ".[dev]"
pytest -q
mcp dev src/archlens/server.py                    # MCP inspector
```



> Review `examples/sample_design.md` against the insurance and agentic-ai rules, then record the key decision as an ADR.

## Roadmap
- [ ] PDF/Markdown ingestion tool
- [ ] Mermaid/C4 diagram generation from ADRs
- [ ] GitHub Action: review design docs on pull requests
- [ ] Packs: EU AI Act, NIST AI RMF, TOGAF, Well-Architected

## License
MIT
