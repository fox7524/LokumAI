from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common


def test_parse_wikilinks_normalizes_alias_anchor_and_extension() -> None:
    text = (
        "[[Temporal_Pattern_Recognition|temporal]] "
        "[[Pointer_Authentication_Check#runtime]] "
        "[[Topology_Analysis.md]]"
    )

    assert common.parse_wikilinks(text) == [
        "Temporal_Pattern_Recognition",
        "Pointer_Authentication_Check",
        "Topology_Analysis",
    ]


def test_parse_yaml_frontmatter_reads_simple_lists() -> None:
    text = """---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
status: draft
---

body
"""

    frontmatter = common.parse_yaml_frontmatter(text)

    assert frontmatter["date"] == "2026-08-30"
    assert frontmatter["tags"] == ['"#rag/memory_cell"', '"#rag/training"']
    assert frontmatter["status"] == "draft"


def test_forbidden_node_detection_rejects_dictionary_node() -> None:
    with pytest.raises(ValueError, match="LokumAI-1.0"):
        common.assert_no_forbidden_nodes("Bad link [[LokumAI-1.0]]")


def test_link_target_layer_membership_accepts_allowed_targets() -> None:
    allowed = {"Temporal_Pattern_Recognition", "Topology_Analysis"}

    common.assert_link_target_layer_membership(
        ["[[Temporal_Pattern_Recognition]]", "Topology_Analysis"],
        allowed_targets=allowed,
    )


def test_link_target_layer_membership_rejects_unknown_targets() -> None:
    with pytest.raises(ValueError, match="Unknown_Node"):
        common.assert_link_target_layer_membership(
            ["Unknown_Node"],
            allowed_targets={"Temporal_Pattern_Recognition"},
        )


def test_filename_normalization_for_raw_and_h3_notes() -> None:
    raw_name = common.build_note_filename(
        "RAG_Memory_Cell",
        "MLX zero-copy dispatch / buffer reuse",
        index=13,
    )
    h3_name = common.build_note_filename("H3", "Apple silicon memory execution synthesis")

    assert raw_name == "RAG_Memory_Cell_13_MLX_Zero_Copy_Dispatch_Buffer_Reuse.md"
    assert h3_name == "H3_Apple_Silicon_Memory_Execution_Synthesis.md"


def test_hidden_target_discovery_reads_real_knowledge_nodes() -> None:
    hidden_1 = common.discover_hidden_1_targets()
    hidden_2 = common.discover_hidden_2_targets()

    assert "Zero_Copy_Buffer_Analysis" in hidden_1
    assert "Temporal_Pattern_Recognition" in hidden_2


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
