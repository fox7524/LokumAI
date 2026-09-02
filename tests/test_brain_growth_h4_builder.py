from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common


def test_discover_hidden_4_targets_reads_h4_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H4_Test_Reasoning.md").write_text("# H4 Test\n", encoding="utf-8")

    assert common.discover_hidden_4_targets(knowledge_dir) == {"H4_Test_Reasoning"}


def test_allowed_forward_targets_includes_hidden_4_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H4_Test_Reasoning.md").write_text("# H4 Test\n", encoding="utf-8")

    assert "H4_Test_Reasoning" in common.allowed_forward_targets(knowledge_dir)


def create_h4_dependency_stubs(knowledge_dir: Path) -> None:
    from tools.brain_growth import h4_builder

    knowledge_dir.mkdir(parents=True, exist_ok=True)
    targets = set()
    for family in h4_builder.H4_FAMILIES:
        targets.update(family.synthesis_inputs)
        targets.update(family.strategic_anchors)
        targets.update(family.downstream_links)

    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target.replace('_', ' ')}\n", encoding="utf-8")


def test_render_note_contains_required_hidden4_sections() -> None:
    from tools.brain_growth import h4_builder

    note = h4_builder.H4_FAMILIES[0]
    text = h4_builder.render_h4_note(note)

    assert '  - "#layer/hidden_4_reasoning_convergence"' in text
    assert "## Yakınsama amacı" in text
    assert "## Tetikleyiciler" in text
    assert "## Karar sınırları" in text
    assert "## Besleyen sentez düğümleri" in text
    assert "## İleri yönlü etkiler" in text


def test_write_h4_notes_creates_six_reasoning_files(tmp_path: Path) -> None:
    from tools.brain_growth import h4_builder

    knowledge_dir = tmp_path / "Knowledge"
    create_h4_dependency_stubs(knowledge_dir)
    written = h4_builder.write_h4_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == len(h4_builder.H4_FAMILIES) == 6
    assert all(path.name.startswith("H4_") for path in written)


def test_rendered_h4_notes_keep_forbidden_dictionary_node_out() -> None:
    from tools.brain_growth import h4_builder

    text = h4_builder.render_h4_note(h4_builder.H4_FAMILIES[0])

    common.assert_no_forbidden_nodes(text)
    assert "LokumAI-1.0" not in text
