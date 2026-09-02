from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h8_builder


def test_discover_hidden_8_targets_reads_h8_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H8_Test_Decision.md").write_text("# H8 Test\n", encoding="utf-8")

    assert common.discover_hidden_8_targets(knowledge_dir) == {"H8_Test_Decision"}


def test_allowed_forward_targets_includes_hidden_8_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H8_Test_Decision.md").write_text("# H8 Test\n", encoding="utf-8")

    assert "H8_Test_Decision" in common.allowed_forward_targets(knowledge_dir)


def create_h8_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h8_builder.H8_FAMILIES:
        targets.update(family.h7_inputs)
        targets.update(family.broadcast_targets)
        targets.update(family.downstream_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden8_shape() -> None:
    note = h8_builder.H8_FAMILIES[0]
    text = h8_builder.render_h8_note(note)

    assert 'date: "2026-08-30"' in text
    assert '  - "#layer/hidden_8_decision_assembly"' in text
    assert '  - "#workspace/global_broadcast"' in text
    assert '  - "#decision/dominant_thoughtseed"' in text
    assert '  - "#policy/assembly"' in text
    assert 'workspace_mode: "' in text
    assert 'dominant_thoughtseed: "' in text
    assert "candidate_policies:" in text
    assert "broadcast_targets:" in text
    assert "## Karar montaj amacı" in text
    assert "## Dominant thoughtseed sinyalleri" in text
    assert "## Policy broadcast stratejisi" in text
    assert "## Commitment kuralları" in text
    assert "## Besleyen H7 düğümleri" in text
    assert "## Yayınlanan çıktı yolları" in text


def test_write_h8_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h8_builder.write_h8_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h8_notes_creates_four_decision_assembly_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h8_dependency_stubs(knowledge_dir)

    written = h8_builder.write_h8_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h8_builder.H8_FAMILIES) == 4
    assert all(path.name.startswith("H8_") for path in written)


def test_run_checks_reports_expected_workspace_counts(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h8_dependency_stubs(knowledge_dir)
    written = h8_builder.write_h8_notes(force=False, knowledge_dir=knowledge_dir)

    results = h8_builder.run_checks(written)

    assert len(results) == 4
    assert results[0]["h7_inputs"] >= 2
    assert results[0]["candidate_policies"] >= 2
    assert results[0]["broadcast_targets"] >= 2
    assert results[0]["downstream_outputs"] >= 2
    assert results[0]["forbidden_refs"] is False


def test_rendered_h8_notes_keep_forbidden_dictionary_node_out() -> None:
    text = h8_builder.render_h8_note(h8_builder.H8_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
