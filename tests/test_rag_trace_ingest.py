from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.learning import rag_trace_ingest


def test_ingest_creates_rag_trace_note_and_filters_to_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    (knowledge_dir / "H10_Test.md").write_text("# H10 Test\n", encoding="utf-8")
    (knowledge_dir / "H9_Test.md").write_text("# H9 Test\n", encoding="utf-8")
    (knowledge_dir / "LokumAI-1.0.md").write_text("# Dictionary\n", encoding="utf-8")

    trace = {
        "trace_id": "ui-001",
        "query": "foo",
        "sources": [
            {"source_path": str(knowledge_dir / "H10_Test.md"), "file_id": "x"},
            {"note_id": "H9_Test"},
            {"note_id": "LokumAI-1.0"},
            {"note_id": "Missing_Note"},
        ],
        "distances": [0.9, 0.8, 0.7, 0.1],
    }
    trace_path = tmp_path / "trace.json"
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")

    result = rag_trace_ingest.ingest_trace_json(
        trace_json_path=trace_path,
        knowledge_dir=knowledge_dir,
        overwrite=False,
    )

    assert result.trace_note_path.exists()
    text = result.trace_note_path.read_text(encoding="utf-8")
    assert '  - "#layer/input_rag"' in text
    assert 'trace_id: "ui_001"' in text or 'trace_id: "ui-001"' in text
    assert 'query: "foo"' in text
    assert '  - "H10_Test"' in text
    assert '  - "H9_Test"' in text
    # Dictionary node must not be added as a rag_link nor be wikilinked.
    assert '  - "LokumAI-1.0"' not in text
    assert "- [[LokumAI-1.0]]" not in text


def test_ingest_refuses_overwrite_by_default(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H10_Test.md").write_text("# H10 Test\n", encoding="utf-8")

    trace = {"trace_id": "dup", "query": "x", "targets": ["H10_Test"]}
    trace_path = tmp_path / "trace.json"
    trace_path.write_text(json.dumps(trace), encoding="utf-8")

    rag_trace_ingest.ingest_trace_json(trace_json_path=trace_path, knowledge_dir=knowledge_dir, overwrite=False)
    with pytest.raises(FileExistsError):
        rag_trace_ingest.ingest_trace_json(trace_json_path=trace_path, knowledge_dir=knowledge_dir, overwrite=False)
