"""Policy document loading utilities.

These policy files are plain Markdown in Phase 1. Later phases can chunk,
embed, and index them for RAG without changing their source location.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from itara.utils import policies_dir


@dataclass(frozen=True)
class PolicyDocument:
    """A loaded policy document."""

    policy_id: str
    title: str
    path: Path
    content: str
    word_count: int


def _title_from_content(content: str, path: Path) -> str:
    """Extract the first Markdown H1 title from policy content."""
    for line in content.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()

    msg = f"Policy document must contain an H1 title: {path}"
    raise ValueError(msg)


def _policy_id_from_path(path: Path) -> str:
    """Create a stable policy ID from the filename."""
    return path.stem


def load_policy_documents(path: Path | None = None) -> tuple[PolicyDocument, ...]:
    """Load all Markdown policy documents from the policy directory."""
    target_dir = path or policies_dir()

    if not target_dir.exists():
        msg = f"Policy directory does not exist: {target_dir}"
        raise FileNotFoundError(msg)

    policy_paths = sorted(target_dir.glob("*.md"))
    if not policy_paths:
        msg = f"No Markdown policy documents found in: {target_dir}"
        raise ValueError(msg)

    documents: list[PolicyDocument] = []

    for policy_path in policy_paths:
        content = policy_path.read_text(encoding="utf-8-sig").strip()
        if not content:
            msg = f"Policy document is empty: {policy_path}"
            raise ValueError(msg)

        documents.append(
            PolicyDocument(
                policy_id=_policy_id_from_path(policy_path),
                title=_title_from_content(content, policy_path),
                path=policy_path,
                content=content,
                word_count=len(content.split()),
            )
        )

    return tuple(documents)


def get_policy_document_by_id(policy_id: str, path: Path | None = None) -> PolicyDocument:
    """Return a policy document by ID."""
    documents = load_policy_documents(path)

    for document in documents:
        if document.policy_id == policy_id:
            return document

    available_policy_ids = ", ".join(document.policy_id for document in documents)
    msg = f"Unknown policy_id '{policy_id}'. Available policy IDs: {available_policy_ids}"
    raise KeyError(msg)
