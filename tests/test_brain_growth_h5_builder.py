from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, h5_builder


def test_discover_hidden_5_targets_reads_h5_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H5_Test_Control.md").write_text("# H5 Test\n", encoding="utf-8")

    assert common.discover_hidden_5_targets(knowledge_dir) == {"H5_Test_Control"}


def test_allowed_forward_targets_includes_hidden_5_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H5_Test_Control.md").write_text("# H5 Test\n", encoding="utf-8")

    assert "H5_Test_Control" in common.allowed_forward_targets(knowledge_dir)


def create_h5_dependency_stubs(knowledge_dir: Path) -> None:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h5_builder.H5_FAMILIES:
        targets.update(family.h4_inputs)
        targets.update(family.control_anchors)
        targets.update(family.managed_outputs)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden5_sections() -> None:
    note = h5_builder.H5_FAMILIES[0]
    text = h5_builder.render_h5_note(note)

    assert '  - "#layer/hidden_5_metacognitive_control"' in text
    assert "## Kontrol amacı" in text
    assert "## Arbitration sinyalleri" in text
    assert "## Karar politikası" in text
    assert "## Besleyen H4 düğümleri" in text
    assert "## Yönettiği çıktı yolları" in text


def test_write_h5_notes_requires_existing_targets(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(FileNotFoundError):
        h5_builder.write_h5_notes(force=False, knowledge_dir=knowledge_dir)


def test_write_h5_notes_creates_four_control_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h5_dependency_stubs(knowledge_dir)

    written = h5_builder.write_h5_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h5_builder.H5_FAMILIES) == 4
    assert all(path.name.startswith("H5_") for path in written)


def test_run_checks_reports_expected_link_counts(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_h5_dependency_stubs(knowledge_dir)
    written = h5_builder.write_h5_notes(force=False, knowledge_dir=knowledge_dir)

    results = h5_builder.run_checks(written)

    assert len(results) == 4
    assert results[0]["h4_inputs"] >= 2
    assert results[0]["control_anchors"] >= 1
    assert results[0]["managed_outputs"] >= 2
    assert results[0]["forbidden_refs"] is False


def test_rendered_h5_notes_keep_forbidden_dictionary_node_out() -> None:
    text = h5_builder.render_h5_note(h5_builder.H5_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
