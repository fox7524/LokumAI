from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h7_builder


def test_discover_hidden_7_targets_reads_h7_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H7_Test_Episodic.md").write_text("# H7 Test\n", encoding="utf-8")

    assert common.discover_hidden_7_targets(knowledge_dir) == {"H7_Test_Episodic"}


def test_allowed_forward_targets_includes_hidden_7_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H7_Test_Episodic.md").write_text("# H7 Test\n", encoding="utf-8")

    assert "H7_Test_Episodic" in common.allowed_forward_targets(knowledge_dir)


def create_h7_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h7_builder.H7_FAMILIES:
        targets.update(family.h6_inputs)
        targets.update(family.memory_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden7_shape() -> None:
    note = h7_builder.H7_FAMILIES[0]
    text = h7_builder.render_h7_note(note)

    assert 'date: "2026-08-30"' in text
    assert '  - "#layer/hidden_7_episodic_temporal_memory"' in text
    assert '  - "#memory/episodic"' in text
    assert '  - "#reasoning/temporal"' in text
    assert '  - "#graph/entity_event_dual"' in text
    assert 'episode_mode: "' in text
    assert "temporal_relations:" in text
    assert "primary_entities:" in text
    assert "primary_events:" in text
    assert "## Episodik amaç" in text
    assert "## Zamansal sinyaller" in text
    assert "## Temporal edge politikası" in text
    assert "## Entity-event bağlama stratejisi" in text
    assert "## Besleyen H6 düğümleri" in text
    assert "## Hafıza çıktıları" in text


def test_write_h7_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h7_builder.write_h7_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h7_notes_creates_four_episodic_temporal_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h7_dependency_stubs(knowledge_dir)

    written = h7_builder.write_h7_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h7_builder.H7_FAMILIES) == 4
    assert all(path.name.startswith("H7_") for path in written)


def test_run_checks_reports_expected_graph_counts(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h7_dependency_stubs(knowledge_dir)
    written = h7_builder.write_h7_notes(force=False, knowledge_dir=knowledge_dir)

    results = h7_builder.run_checks(written)

    assert len(results) == 4
    assert results[0]["h6_inputs"] >= 2
    assert results[0]["temporal_relations"] >= 2
    assert results[0]["primary_entities"] >= 2
    assert results[0]["primary_events"] >= 2
    assert results[0]["memory_outputs"] >= 2
    assert results[0]["forbidden_refs"] is False


def test_rendered_h7_notes_keep_forbidden_dictionary_node_out() -> None:
    text = h7_builder.render_h7_note(h7_builder.H7_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
