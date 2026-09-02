from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h10_builder


def test_discover_hidden_10_targets_reads_h10_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H10_Test_Supervision.md").write_text("# H10 Test\n", encoding="utf-8")

    assert common.discover_hidden_10_targets(knowledge_dir) == {"H10_Test_Supervision"}


def test_allowed_forward_targets_includes_hidden_10_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H10_Test_Supervision.md").write_text("# H10 Test\n", encoding="utf-8")

    targets = common.allowed_forward_targets(knowledge_dir)
    assert "H10_Test_Supervision" in targets


def create_h10_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h10_builder.H10_FAMILIES:
        targets.update(family.h9_inputs)
        targets.update(family.oversight_surfaces)
        targets.update(family.downstream_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden10_shape() -> None:
    note = h10_builder.H10_FAMILIES[0]
    text = h10_builder.render_h10_note(note)

    assert 'date: "2026-08-30"' in text
    assert '  - "#layer/hidden_10_strategic_supervision"' in text
    assert '  - "#strategy/supervision_contract"' in text
    assert '  - "#strategy/oversight_surface"' in text
    assert '  - "#execution/governance_binding"' in text
    assert 'supervision_mode: "' in text
    assert 'governing_signal: "' in text
    assert "oversight_surfaces:" in text
    assert "supervision_contracts:" in text
    assert "## Stratejik denetim amacı" in text
    assert "## Governing signal eşlemesi" in text
    assert "## Oversight surface sözleşmeleri" in text
    assert "## Escalation ve rollback kuralları" in text
    assert "## Besleyen H9 düğümleri" in text
    assert "## Denetlenen çıktı yolları" in text


def test_write_h10_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h10_builder.write_h10_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h10_notes_creates_four_strategic_supervision_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h10_dependency_stubs(knowledge_dir)

    written = h10_builder.write_h10_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h10_builder.H10_FAMILIES) == 4
    assert [path.name for path in written] == [
        "H10_Global_Supervision_Arbitration.md",
        "H10_Long_Horizon_Outcome_Review.md",
        "H10_Rollback_Escalation_Governance.md",
        "H10_Strategic_Resource_Oversight.md",
    ]


def test_run_checks_reports_expected_supervision_counts(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h10_dependency_stubs(knowledge_dir)
    written = h10_builder.write_h10_notes(force=False, knowledge_dir=knowledge_dir)

    results = h10_builder.run_checks(written)

    assert len(results) == 4
    assert results[0]["h9_inputs"] >= 1
    assert results[0]["oversight_surfaces"] >= 2
    assert results[0]["supervision_contracts"] >= 2
    assert results[0]["downstream_outputs"] >= 2
    assert results[0]["forbidden_refs"] is False


def test_rendered_h10_notes_keep_forbidden_dictionary_node_out() -> None:
    text = h10_builder.render_h10_note(h10_builder.H10_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
