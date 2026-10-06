# Contributing

The easiest way to contribute is a **rule pack**.

1. Add `src/archlens/rules/<domain>.yaml` (or copy an existing one).
2. Each rule: `id`, `domain`, `severity` (high/medium/low), `check` (one testable sentence), optional `keywords` (hint only).
3. Run `pytest -q` and open a PR.

Wanted packs: telecom, retail, public sector, TOGAF principles, AWS/Azure Well-Architected, EU AI Act.
