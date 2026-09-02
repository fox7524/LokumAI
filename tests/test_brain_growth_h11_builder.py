from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h11_builder


def test_discover_hidden_11_targets_reads_h11_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H11_Test_Audit.md").write_text("# H11 Test\n", encoding="utf-8")

    assert common.discover_hidden_11_targets(knowledge_dir) == {"H11_Test_Audit"}


def test_allowed_forward_targets_includes_hidden_11_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H11_Test_Audit.md").write_text("# H11 Test\n", encoding="utf-8")

    targets = common.allowed_forward_targets(knowledge_dir)
    assert "H11_Test_Audit" in targets


def create_h11_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h11_builder.H11_FAMILIES:
        targets.update(family.h10_inputs)
        targets.update(family.audit_surfaces)
        targets.update(family.downstream_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden11_shape() -> None:
    note = h11_builder.H11_FAMILIES[0]
    text = h11_builder.render_h11_note(note)

    assert '  - "#layer/hidden_11_reflection_audit"' in text
    assert '  - "#audit/trace_contract"' in text
    assert '  - "#audit/evidence_surface"' in text
    assert '  - "#audit/provenance_binding"' in text
    assert 'reflection_mode: "' in text
    assert 'audit_signal: "' in text
    assert "audit_surfaces:" in text
    assert "audit_contracts:" in text
    assert "## Yansıma amacı" in text
    assert "## Audit signal eşlemesi" in text
    assert "## Evidence surface sözleşmeleri" in text
    assert "## İspat ve tutarlılık kuralları" in text
    assert "## Besleyen H10 düğümleri" in text
    assert "## Üretilen audit çıktıları" in text


def test_write_h11_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h11_builder.write_h11_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h11_notes_creates_four_reflection_audit_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h11_dependency_stubs(knowledge_dir)

    written = h11_builder.write_h11_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h11_builder.H11_FAMILIES) == 4
    assert [path.name for path in written] == [
        "H11_Failsafe_Cost_Accounting.md",
        "H11_Outcome_Regression_Postmortem.md",
        "H11_Rollback_Decision_Audit.md",
        "H11_Trace_Provenance_Attestation.md",
    ]
