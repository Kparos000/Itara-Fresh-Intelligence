from pathlib import Path

import pytest

from itara.rag import get_policy_document_by_id, load_policy_documents
from itara.utils import policies_dir


def test_policy_directory_exists() -> None:
    assert policies_dir().exists()


def test_load_policy_documents_returns_expected_documents() -> None:
    documents = load_policy_documents()

    policy_ids = {document.policy_id for document in documents}

    assert policy_ids == {
        "human_escalation_policy",
        "markdown_policy",
        "replenishment_policy",
        "supplier_procurement_policy",
        "transfer_exception_policy",
    }


def test_policy_documents_have_titles_and_content() -> None:
    documents = load_policy_documents()

    for document in documents:
        assert document.title
        assert document.content.startswith("# ")
        assert document.word_count > 30


def test_get_policy_document_by_id_returns_expected_document() -> None:
    document = get_policy_document_by_id("transfer_exception_policy")

    assert document.title == "Store Transfer Exception Policy"
    assert "Warehouse allocation must be checked" in document.content


def test_get_policy_document_by_id_rejects_unknown_policy_id() -> None:
    with pytest.raises(KeyError, match="Unknown policy_id"):
        get_policy_document_by_id("missing_policy")


def test_load_policy_documents_rejects_missing_policy_directory(tmp_path: Path) -> None:
    missing_dir = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        load_policy_documents(missing_dir)


def test_load_policy_documents_rejects_empty_policy_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No Markdown policy documents"):
        load_policy_documents(tmp_path)
