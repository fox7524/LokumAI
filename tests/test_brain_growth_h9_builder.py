from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h9_builder


def test_discover_hidden_9_targets_reads_h9_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H9_Test_Package.md").write_text("# H9 Test\n", encoding="utf-8")

    assert common.discover_hidden_9_targets(knowledge_dir) == {"H9_Test_Package"}


def test_allowed_forward_targets_includes_hidden_9_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H9_Test_Package.md").write_text("# H9 Test\n", encoding="utf-8")

    assert "H9_Test_Package" in common.allowed_forward_targets(knowledge_dir)


def create_h9_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h9_builder.H9_FAMILIES:
        targets.update(family.h8_inputs)
        targets.update(family.delivery_surfaces)
        targets.update(family.downstream_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden9_shape() -> None:
    note = h9_builder.H9_FAMILIES[0]
    text = h9_builder.render_h9_note(note)

    assert 'date: "2026-08-30"' in text
    assert '  - "#layer/hidden_9_execution_packaging"' in text
    assert '  - "#execution/package_contract"' in text
    assert '  - "#execution/delivery_surface"' in text
    assert '  - "#policy/surface_binding"' in text
    assert 'package_mode: "' in text
    assert 'source_policy: "' in text
    assert "delivery_surfaces:" in text
    assert "package_contracts:" in text
    assert "## Paketleme amacı" in text
    assert "## Source policy eşlemesi" in text
    assert "## Delivery surface sözleşmeleri" in text
    assert "## Readiness ve commit koşulları" in text
    assert "## Besleyen H8 düğümleri" in text
    assert "## Paketlenen çıktı yolları" in text


def test_write_h9_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h9_builder.write_h9_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h9_notes_creates_four_execution_packaging_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h9_dependency_stubs(knowledge_dir)

    written = h9_builder.write_h9_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h9_builder.H9_FAMILIES) == 4
    assert [path.name for path in written] == [
        "H9_Commit_Ready_Delivery_Check.md",
        "H9_Execution_Surface_Binding.md",
        "H9_Failsafe_Action_Packaging.md",
        "H9_Response_Payload_Composition.md",
    ]


def test_run_checks_reports_expected_execution_packaging_counts(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h9_dependency_stubs(knowledge_dir)
    written = h9_builder.write_h9_notes(force=False, knowledge_dir=knowledge_dir)

    results = h9_builder.run_checks(written)

    assert len(results) == 4
    assert results[0]["h8_inputs"] >= 1
    assert results[0]["delivery_surfaces"] >= 2
    assert results[0]["package_contracts"] >= 2
    assert results[0]["downstream_outputs"] >= 2
    assert results[0]["forbidden_refs"] is False


def test_rendered_h9_notes_keep_forbidden_dictionary_node_out() -> None:
    text = h9_builder.render_h9_note(h9_builder.H9_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
