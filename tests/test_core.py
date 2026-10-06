import pytest
from archlens import core


@pytest.fixture(autouse=True)
def tmp_adr(tmp_path, monkeypatch):
    monkeypatch.setenv("ARCHLENS_ADR_DIR", str(tmp_path / "adr"))


def test_adr_roundtrip():
    p = core.create_adr("Use Kafka for events", "ctx", "dec", "cons", alternatives="RabbitMQ")
    assert "0001-use-kafka-for-events.md" in p
    assert core.list_adrs() == ["0001-use-kafka-for-events.md"]
    assert "RabbitMQ" in core.read_adr("0001-use-kafka-for-events.md")


def test_adr_path_traversal_blocked():
    with pytest.raises(FileNotFoundError):
        core.read_adr("../../etc/passwd")


def test_rules_domain_filter():
    ids = {r["id"] for r in core.get_rules("insurance")}
    assert "INS-01" in ids and "G-01" in ids and "BNK-01" not in ids


def test_review_flags_gaps():
    res = core.review_checklist("We use OAuth and idempotent APIs.", "insurance")
    by_id = {i["id"]: i for i in res["items"]}
    assert by_id["G-03"]["likely_gap"] is False
    assert by_id["INS-02"]["likely_gap"] is True
