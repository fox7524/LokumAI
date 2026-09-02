from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h6_builder


def test_discover_hidden_6_targets_reads_h6_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H6_Test_Executive.md").write_text("# H6 Test\n", encoding="utf-8")

    assert common.discover_hidden_6_targets(knowledge_dir) == {"H6_Test_Executive"}


def test_allowed_forward_targets_includes_hidden_6_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H6_Test_Executive.md").write_text("# H6 Test\n", encoding="utf-8")

    assert "H6_Test_Executive" in common.allowed_forward_targets(knowledge_dir)


def create_h6_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h6_builder.H6_FAMILIES:
        targets.update(family.h5_inputs)
        targets.update(family.orchestration_anchors)
        targets.update(family.coordinated_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden6_sections() -> None:
    note = h6_builder.H6_FAMILIES[0]
    text = h6_builder.render_h6_note(note)

    assert '  - "#layer/hidden_6_executive_orchestration"' in text
    assert "## Orkestrasyon amacı" in text
    assert "## Yürütücü sinyaller" in text
    assert "## Orkestrasyon politikası" in text
    assert "## Besleyen H5 düğümleri" in text
    assert "## Koordine ettiği çıktı yolları" in text


def test_write_h6_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h6_builder.write_h6_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h6_notes_creates_four_executive_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h6_dependency_stubs(knowledge_dir)

    written = h6_builder.write_h6_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h6_builder.H6_FAMILIES) == 4
    assert all(path.name.startswith("H6_") for path in written)


def test_run_checks_reports_expected_link_counts(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h6_dependency_stubs(knowledge_dir)
    written = h6_builder.write_h6_notes(force=False, knowledge_dir=knowledge_dir)

    results = h6_builder.run_checks(written)

    assert len(results) == 4
    assert results[0]["h5_inputs"] >= 2
    assert results[0]["anchors"] >= 1
    assert results[0]["coordinated_outputs"] >= 2
    assert results[0]["forbidden_refs"] is False


def test_rendered_h6_notes_keep_forbidden_dictionary_node_out() -> None:
    text = h6_builder.render_h6_note(h6_builder.H6_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
