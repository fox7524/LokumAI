from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import layered_projection


def write_note(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_build_projection_groups_nodes_by_layer_and_derives_forward_transitions(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test.md",
        "---\n"
        "tags:\n"
        '  - "#rag/memory_cell"\n'
        '  - "#hardware/apple_mlx"\n'
        "---\n\n"
        "# Raw Test\n",
    )
    write_note(
        knowledge_dir / "H3_Test.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_3_logic_synthesis"\n'
        '  - "#domain/apple_silicon_mlx"\n'
        "---\n\n"
        "# H3 Test\n\n"
        "## Besleyen düğümler\n\n"
        "- [[RAG_Memory_Cell_13_Test]]\n",
    )
    write_note(
        knowledge_dir / "H4_Test.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_4_reasoning_convergence"\n'
        '  - "#domain/multi_domain"\n'
        "---\n\n"
        "# H4 Test\n\n"
        "## Besleyen sentez düğümleri\n\n"
        "- [[H3_Test]]\n",
    )
    write_note(
        knowledge_dir / "H5_Test_Control.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_5_metacognitive_control"\n'
        '  - "#domain/multi_domain"\n'
        "---\n\n"
        "# H5 Test Control\n\n"
        "## Besleyen H4 düğümleri\n\n"
        "- [[H4_Test]]\n",
    )
    write_note(
        knowledge_dir / "H6_Beta_Executive.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_6_executive_orchestration"\n'
        '  - "#domain/alpha"\n'
        "---\n\n"
        "# H6 Beta Executive\n\n"
        "## Besleyen H5 düğümleri\n\n"
        "- [[H5_Test_Control]]\n",
    )
    write_note(
        knowledge_dir / "H6_Alpha_Executive.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_6_executive_orchestration"\n'
        '  - "#domain/zeta"\n'
        "---\n\n"
        "# H6 Alpha Executive\n\n"
        "## Besleyen H5 düğümleri\n\n"
        "- [[H5_Test_Control]]\n",
    )
    write_note(
        knowledge_dir / "H7_Test_Episodic.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_7_episodic_temporal_memory"\n'
        '  - "#reasoning/temporal"\n'
        '  - "#graph/entity_event_dual"\n'
        '  - "#domain/temporal_reasoning"\n'
        'episode_mode: "ordered_episode_reconstruction"\n'
        "temporal_relations:\n"
        '  - "before"\n'
        '  - "after"\n'
        "primary_entities:\n"
        '  - "executive_queue"\n'
        '  - "response_plan"\n'
        "primary_events:\n"
        '  - "priority_shift"\n'
        '  - "execution_release"\n'
        "---\n\n"
        "# H7 Test Episodic\n\n"
        "## Besleyen H6 düğümleri\n\n"
        "- [[H6_Alpha_Executive]]\n"
        "- [[H6_Beta_Executive]]\n",
    )
    write_note(
        knowledge_dir / "H8_Test_Decision.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_8_decision_assembly"\n'
        '  - "#workspace/global_broadcast"\n'
        '  - "#decision/dominant_thoughtseed"\n'
        '  - "#policy/assembly"\n'
        '  - "#domain/decision_assembly"\n'
        'workspace_mode: "dominant_policy_broadcast"\n'
        'dominant_thoughtseed: "recovery_first_consensus"\n'
        "candidate_policies:\n"
        '  - "stabilize_consensus_before_execution"\n'
        '  - "minimize_regret_under_risk"\n'
        "broadcast_targets:\n"
        '  - "Executive_Action_Formatter"\n'
        '  - "Final_Execution_Gate"\n'
        "---\n\n"
        "# H8 Test Decision\n\n"
        "## Besleyen H7 düğümleri\n\n"
        "- [[H7_Test_Episodic]]\n\n"
        "## Yayınlanan çıktı yolları\n\n"
        "- [[Global_State_Consensus]]\n",
    )
    write_note(
        knowledge_dir / "H9_Test_Package.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_9_execution_packaging"\n'
        '  - "#execution/package_contract"\n'
        '  - "#execution/delivery_surface"\n'
        '  - "#policy/surface_binding"\n'
        'package_mode: "surface_bound_policy_delivery"\n'
        'source_policy: "dominant_policy_surface_binding"\n'
        "delivery_surfaces:\n"
        '  - "Executive_Action_Formatter"\n'
        '  - "Final_Execution_Gate"\n'
        "package_contracts:\n"
        '  - "surface_route_manifest"\n'
        '  - "policy_binding_envelope"\n'
        "---\n\n"
        "# H9 Test Package\n\n"
        "## Besleyen H8 düğümleri\n\n"
        "- [[H8_Test_Decision]]\n\n"
        "## Paketlenen çıktı yolları\n\n"
        "- [[Final_Execution_Gate]]\n"
        "- [[Cognitive_Response_Generator]]\n",
    )
    write_note(
        knowledge_dir / "H10_Test_Supervision.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_10_strategic_supervision"\n'
        '  - "#strategy/supervision_contract"\n'
        '  - "#strategy/oversight_surface"\n'
        '  - "#execution/governance_binding"\n'
        'supervision_mode: "global_supervision_arbitration"\n'
        'governing_signal: "surface_alignment_supervision"\n'
        "oversight_surfaces:\n"
        '  - "Global_State_Consensus"\n'
        '  - "Long_Term_Strategic_Planner"\n'
        "supervision_contracts:\n"
        '  - "supervision_route_manifest"\n'
        '  - "strategic_alignment_contract"\n'
        "---\n\n"
        "# H10 Test Supervision\n\n"
        "## Besleyen H9 düğümleri\n\n"
        "- [[H9_Test_Package]]\n\n"
        "## Denetlenen çıktı yolları\n\n"
        "- [[Global_State_Consensus]]\n"
        "- [[Long_Term_Strategic_Planner]]\n",
    )
    write_note(
        knowledge_dir / "H11_Test_Audit.md",
        "---\n"
        "tags:\n"
        '  - "#layer/hidden_11_reflection_audit"\n'
        '  - "#audit/trace_contract"\n'
        '  - "#audit/evidence_surface"\n'
        '  - "#audit/provenance_binding"\n'
        'reflection_mode: "trace_provenance_attestation"\n'
        'audit_signal: "supervision_trace_digest"\n'
        "audit_surfaces:\n"
        '  - "Metacognitive_Reflection_Core"\n'
        '  - "Global_State_Consensus"\n'
        "audit_contracts:\n"
        '  - "provenance_trace_manifest"\n'
        '  - "surface_route_attestation"\n'
        "---\n\n"
        "# H11 Test Audit\n\n"
        "## Besleyen H10 düğümleri\n\n"
        "- [[H10_Test_Supervision]]\n\n"
        "## Üretilen audit çıktıları\n\n"
        "- [[Global_Risk_Assessment]]\n",
    )
    write_note(
        knowledge_dir / "RAG_Trace_Test_Query.md",
        "---\n"
        "tags:\n"
        '  - "#layer/input_rag"\n'
        '  - "#rag/trace"\n'
        'trace_id: "test_query"\n'
        'query: "execution surface binding?"\n'
        "rag_links:\n"
        '  - "H9_Test_Package"\n'
        '  - "H11_Test_Audit"\n'
        "---\n\n"
        "# RAG Trace Test Query\n\n"
        "## RAG bağları (rag_links)\n\n"
        "- [[H9_Test_Package]]\n"
        "- [[H11_Test_Audit]]\n",
    )
    write_note(
        knowledge_dir / "Brain_Growth_Index.md",
        "---\n"
        "tags:\n"
        '  - "#index/brain_growth"\n'
        "---\n\n"
        "# Brain Growth Index\n\n"
        "## Alanlar\n\n"
        "- [[H11_Test_Audit]]\n"
        "- [[H10_Test_Supervision]]\n"
        "- [[H9_Test_Package]]\n"
        "- [[H8_Test_Decision]]\n"
        "- [[H7_Test_Episodic]]\n"
        "- [[H6_Alpha_Executive]]\n"
        "- [[H6_Beta_Executive]]\n",
    )
    write_note(knowledge_dir / "LokumAI-1.0.md", "# Forbidden\n")

    projection = layered_projection.build_projection(knowledge_dir=knowledge_dir)

    assert list(projection["layers"]) == [
        "raw",
        "hidden_3",
        "hidden_4",
        "hidden_5",
        "hidden_6",
        "hidden_7",
        "hidden_8",
        "hidden_9",
        "hidden_10",
        "hidden_11",
        "index",
    ]
    assert [node["id"] for node in projection["layers"]["raw"]] == ["RAG_Memory_Cell_13_Test"]
    assert [node["id"] for node in projection["layers"]["hidden_3"]] == ["H3_Test"]
    assert [node["id"] for node in projection["layers"]["hidden_4"]] == ["H4_Test"]
    assert [node["id"] for node in projection["layers"]["hidden_5"]] == ["H5_Test_Control"]
    assert [node["id"] for node in projection["layers"]["hidden_6"]] == [
        "H6_Beta_Executive",
        "H6_Alpha_Executive",
    ]
    assert [node["id"] for node in projection["layers"]["hidden_7"]] == ["H7_Test_Episodic"]
    assert [node["id"] for node in projection["layers"]["hidden_8"]] == ["H8_Test_Decision"]
    assert [node["id"] for node in projection["layers"]["hidden_9"]] == ["H9_Test_Package"]
    assert [node["id"] for node in projection["layers"]["hidden_10"]] == ["H10_Test_Supervision"]
    assert [node["id"] for node in projection["layers"]["hidden_11"]] == ["H11_Test_Audit"]
    assert [node["id"] for node in projection["layers"]["index"]] == ["Brain_Growth_Index"]
    assert projection["layer_counts"] == {
        "raw": 1,
        "hidden_3": 1,
        "hidden_4": 1,
        "hidden_5": 1,
        "hidden_6": 2,
        "hidden_7": 1,
        "hidden_8": 1,
        "hidden_9": 1,
        "hidden_10": 1,
        "hidden_11": 1,
        "index": 1,
    }
    assert projection["transition_counts"] == {
        "raw_to_hidden_3": 1,
        "hidden_3_to_hidden_4": 1,
        "hidden_4_to_hidden_5": 1,
        "hidden_5_to_hidden_6": 2,
        "hidden_6_to_hidden_7": 2,
        "hidden_6_to_index": 2,
        "hidden_7_to_hidden_8": 1,
        "hidden_7_to_index": 1,
        "hidden_8_to_hidden_9": 1,
        "hidden_8_to_index": 1,
        "hidden_9_to_hidden_10": 1,
        "hidden_9_to_index": 1,
        "hidden_10_to_hidden_11": 1,
        "hidden_10_to_index": 1,
        "hidden_11_to_index": 1,
    }
    assert projection["domain_clusters"]["hardware/apple_mlx"] == {
        "node_count": 1,
        "layers": {"raw": 1},
        "internal_edge_count": 0,
        "external_edge_count": 1,
        "nodes": ["RAG_Memory_Cell_13_Test"],
    }
    assert projection["domain_clusters"]["domain/multi_domain"] == {
        "node_count": 2,
        "layers": {"hidden_4": 1, "hidden_5": 1},
        "internal_edge_count": 1,
        "external_edge_count": 3,
        "nodes": ["H4_Test", "H5_Test_Control"],
    }
    assert projection["cluster_spread_by_layer"]["hidden_6"] == {
        "total_nodes": 2,
        "cluster_count": 2,
        "dominant_cluster": "domain/alpha",
        "dominant_cluster_share": 0.5,
        "clusters": {"domain/alpha": 1, "domain/zeta": 1},
    }
    assert projection["cluster_spread_by_layer"]["hidden_5"] == {
        "total_nodes": 1,
        "cluster_count": 1,
        "dominant_cluster": "domain/multi_domain",
        "dominant_cluster_share": 1.0,
        "clusters": {"domain/multi_domain": 1},
    }
    assert projection["cluster_spread_by_layer"]["hidden_7"] == {
        "total_nodes": 1,
        "cluster_count": 1,
        "dominant_cluster": "domain/temporal_reasoning",
        "dominant_cluster_share": 1.0,
        "clusters": {"domain/temporal_reasoning": 1},
    }
    assert projection["cluster_spread_by_layer"]["hidden_8"] == {
        "total_nodes": 1,
        "cluster_count": 1,
        "dominant_cluster": "domain/decision_assembly",
        "dominant_cluster_share": 1.0,
        "clusters": {"domain/decision_assembly": 1},
    }
    assert projection["cluster_spread_by_layer"]["hidden_9"] == {
        "total_nodes": 1,
        "cluster_count": 1,
        "dominant_cluster": "hidden_9",
        "dominant_cluster_share": 1.0,
        "clusters": {"hidden_9": 1},
    }
    assert projection["cluster_spread_by_layer"]["hidden_10"] == {
        "total_nodes": 1,
        "cluster_count": 1,
        "dominant_cluster": "hidden_10",
        "dominant_cluster_share": 1.0,
        "clusters": {"hidden_10": 1},
    }
    assert projection["layout_quality"] == {
        "balance": 0.5,
        "density": 0.28,
        "cross_cluster_pressure": 0.94,
        "readability": 0.43,
    }
    assert projection["layers"]["hidden_6"][0] == {
        "id": "H6_Beta_Executive",
        "title": "H6 Beta Executive",
        "path": str(knowledge_dir / "H6_Beta_Executive.md"),
        "layer": "hidden_6",
        "domain": "domain/alpha",
        "direct_links": ["H5_Test_Control"],
        "layout_sort_key": "domain/alpha::H6_Beta_Executive",
        "tracked_links": ["H5_Test_Control"],
        "incoming_edge_count": 1,
        "outgoing_edge_count": 2,
        "layer_column": 4,
        "slot_index": 0,
        "x": 960,
        "y": -80,
    }
    assert projection["layers"]["hidden_6"][1] == {
        "id": "H6_Alpha_Executive",
        "title": "H6 Alpha Executive",
        "path": str(knowledge_dir / "H6_Alpha_Executive.md"),
        "layer": "hidden_6",
        "domain": "domain/zeta",
        "direct_links": ["H5_Test_Control"],
        "layout_sort_key": "domain/zeta::H6_Alpha_Executive",
        "tracked_links": ["H5_Test_Control"],
        "incoming_edge_count": 1,
        "outgoing_edge_count": 2,
        "layer_column": 4,
        "slot_index": 1,
        "x": 960,
        "y": 80,
    }
    assert projection["layers"]["hidden_7"][0] == {
        "id": "H7_Test_Episodic",
        "title": "H7 Test Episodic",
        "path": str(knowledge_dir / "H7_Test_Episodic.md"),
        "layer": "hidden_7",
        "domain": "domain/temporal_reasoning",
        "direct_links": ["H6_Alpha_Executive", "H6_Beta_Executive"],
        "layout_sort_key": "domain/temporal_reasoning::H7_Test_Episodic",
        "tracked_links": ["H6_Alpha_Executive", "H6_Beta_Executive"],
        "incoming_edge_count": 2,
        "outgoing_edge_count": 2,
        "layer_column": 5,
        "slot_index": 0,
        "x": 1200,
        "y": 0,
    }
    assert projection["layers"]["hidden_8"][0] == {
        "id": "H8_Test_Decision",
        "title": "H8 Test Decision",
        "path": str(knowledge_dir / "H8_Test_Decision.md"),
        "layer": "hidden_8",
        "domain": "domain/decision_assembly",
        "direct_links": ["Global_State_Consensus", "H7_Test_Episodic"],
        "layout_sort_key": "domain/decision_assembly::H8_Test_Decision",
        "tracked_links": ["H7_Test_Episodic"],
        "incoming_edge_count": 1,
        "outgoing_edge_count": 2,
        "layer_column": 6,
        "slot_index": 0,
        "x": 1440,
        "y": 0,
    }
    assert projection["layers"]["hidden_9"][0] == {
        "id": "H9_Test_Package",
        "title": "H9 Test Package",
        "path": str(knowledge_dir / "H9_Test_Package.md"),
        "layer": "hidden_9",
        "domain": "hidden_9",
        "direct_links": ["Cognitive_Response_Generator", "Final_Execution_Gate", "H8_Test_Decision"],
        "layout_sort_key": "hidden_9::H9_Test_Package",
        "tracked_links": ["H8_Test_Decision"],
        "incoming_edge_count": 1,
        "outgoing_edge_count": 2,
        "layer_column": 7,
        "slot_index": 0,
        "x": 1680,
        "y": 0,
    }
    assert projection["layers"]["hidden_10"][0] == {
        "id": "H10_Test_Supervision",
        "title": "H10 Test Supervision",
        "path": str(knowledge_dir / "H10_Test_Supervision.md"),
        "layer": "hidden_10",
        "domain": "hidden_10",
        "direct_links": ["Global_State_Consensus", "H9_Test_Package", "Long_Term_Strategic_Planner"],
        "layout_sort_key": "hidden_10::H10_Test_Supervision",
        "tracked_links": ["H9_Test_Package"],
        "incoming_edge_count": 1,
        "outgoing_edge_count": 2,
        "layer_column": 8,
        "slot_index": 0,
        "x": 1920,
        "y": 0,
    }
    assert projection["temporal_dual_graph"]["entity_nodes"] == [
        {
            "id": "entity:executive_queue",
            "label": "executive_queue",
            "episodes": ["H7_Test_Episodic"],
        },
        {
            "id": "entity:response_plan",
            "label": "response_plan",
            "episodes": ["H7_Test_Episodic"],
        },
    ]
    assert projection["temporal_dual_graph"]["event_nodes"] == [
        {
            "id": "event:execution_release",
            "label": "execution_release",
            "episodes": ["H7_Test_Episodic"],
        },
        {
            "id": "event:priority_shift",
            "label": "priority_shift",
            "episodes": ["H7_Test_Episodic"],
        },
    ]
    assert projection["temporal_dual_graph"]["temporal_edges"] == [
        {
            "source": "event:priority_shift",
            "target": "event:execution_release",
            "relation": "before",
            "episode": "H7_Test_Episodic",
            "episode_mode": "ordered_episode_reconstruction",
        }
    ]
    assert projection["workspace_broadcast_graph"]["thoughtseed_nodes"] == [
        {
            "id": "thoughtseed:recovery_first_consensus",
            "label": "recovery_first_consensus",
            "episodes": ["H8_Test_Decision"],
        }
    ]
    assert projection["workspace_broadcast_graph"]["policy_nodes"] == [
        {
            "id": "policy:minimize_regret_under_risk",
            "label": "minimize_regret_under_risk",
            "episodes": ["H8_Test_Decision"],
        },
        {
            "id": "policy:stabilize_consensus_before_execution",
            "label": "stabilize_consensus_before_execution",
            "episodes": ["H8_Test_Decision"],
        },
    ]
    assert projection["workspace_broadcast_graph"]["selection_edges"] == [
        {
            "source": "thoughtseed:recovery_first_consensus",
            "target": "policy:stabilize_consensus_before_execution",
            "relation": "selects",
            "episode": "H8_Test_Decision",
            "workspace_mode": "dominant_policy_broadcast",
        },
        {
            "source": "thoughtseed:recovery_first_consensus",
            "target": "policy:minimize_regret_under_risk",
            "relation": "selects",
            "episode": "H8_Test_Decision",
            "workspace_mode": "dominant_policy_broadcast",
        },
    ]
    assert projection["workspace_broadcast_graph"]["broadcast_edges"] == [
        {
            "source": "policy:stabilize_consensus_before_execution",
            "target": "target:Executive_Action_Formatter",
            "relation": "broadcasts_to",
            "episode": "H8_Test_Decision",
        },
        {
            "source": "policy:stabilize_consensus_before_execution",
            "target": "target:Final_Execution_Gate",
            "relation": "broadcasts_to",
            "episode": "H8_Test_Decision",
        },
    ]
    assert projection["execution_package_graph"]["policy_nodes"] == [
        {
            "id": "source_policy:dominant_policy_surface_binding",
            "label": "dominant_policy_surface_binding",
            "packages": ["H9_Test_Package"],
        }
    ]
    assert projection["execution_package_graph"]["package_nodes"] == [
        {
            "id": "package:H9_Test_Package",
            "label": "H9_Test_Package",
            "package_mode": "surface_bound_policy_delivery",
            "contracts": ["policy_binding_envelope", "surface_route_manifest"],
        }
    ]
    assert projection["execution_package_graph"]["surface_nodes"] == [
        {
            "id": "surface:Executive_Action_Formatter",
            "label": "Executive_Action_Formatter",
            "packages": ["H9_Test_Package"],
        },
        {
            "id": "surface:Final_Execution_Gate",
            "label": "Final_Execution_Gate",
            "packages": ["H9_Test_Package"],
        },
    ]
    assert projection["execution_package_graph"]["binding_edges"] == [
        {
            "source": "source_policy:dominant_policy_surface_binding",
            "target": "package:H9_Test_Package",
            "relation": "binds",
            "package_mode": "surface_bound_policy_delivery",
        }
    ]
    assert projection["execution_package_graph"]["delivery_edges"] == [
        {
            "source": "package:H9_Test_Package",
            "target": "surface:Executive_Action_Formatter",
            "relation": "delivers_to",
        },
        {
            "source": "package:H9_Test_Package",
            "target": "surface:Final_Execution_Gate",
            "relation": "delivers_to",
        },
    ]
    assert projection["strategic_supervision_graph"]["signal_nodes"] == [
        {
            "id": "signal:surface_alignment_supervision",
            "label": "surface_alignment_supervision",
            "supervision_notes": ["H10_Test_Supervision"],
        }
    ]
    assert projection["strategic_supervision_graph"]["supervision_nodes"] == [
        {
            "id": "supervision:H10_Test_Supervision",
            "label": "H10_Test_Supervision",
            "supervision_mode": "global_supervision_arbitration",
            "contracts": ["strategic_alignment_contract", "supervision_route_manifest"],
        }
    ]
    assert projection["strategic_supervision_graph"]["oversight_nodes"] == [
        {
            "id": "oversight:Global_State_Consensus",
            "label": "Global_State_Consensus",
            "supervision_notes": ["H10_Test_Supervision"],
        },
        {
            "id": "oversight:Long_Term_Strategic_Planner",
            "label": "Long_Term_Strategic_Planner",
            "supervision_notes": ["H10_Test_Supervision"],
        },
    ]
    assert projection["strategic_supervision_graph"]["governance_edges"] == [
        {
            "source": "signal:surface_alignment_supervision",
            "target": "supervision:H10_Test_Supervision",
            "relation": "governs",
            "supervision_mode": "global_supervision_arbitration",
        }
    ]
    assert projection["strategic_supervision_graph"]["oversight_edges"] == [
        {
            "source": "supervision:H10_Test_Supervision",
            "target": "oversight:Global_State_Consensus",
            "relation": "oversees",
        },
        {
            "source": "supervision:H10_Test_Supervision",
            "target": "oversight:Long_Term_Strategic_Planner",
            "relation": "oversees",
        },
    ]
    assert projection["rag_binding_graph"]["trace_nodes"] == [
        {
            "id": "rag_trace:RAG_Trace_Test_Query",
            "label": "RAG Trace Test Query",
            "query": "execution surface binding?",
            "rag_links": ["H11_Test_Audit", "H9_Test_Package"],
        }
    ]
    assert projection["rag_binding_graph"]["target_nodes"] == [
        {
            "id": "target:H11_Test_Audit",
            "label": "H11_Test_Audit",
            "trace_notes": ["RAG_Trace_Test_Query"],
        },
        {
            "id": "target:H9_Test_Package",
            "label": "H9_Test_Package",
            "trace_notes": ["RAG_Trace_Test_Query"],
        },
    ]
    assert projection["rag_binding_graph"]["rag_edges"] == [
        {
            "source": "rag_trace:RAG_Trace_Test_Query",
            "target": "target:H11_Test_Audit",
            "relation": "retrieved",
        },
        {
            "source": "rag_trace:RAG_Trace_Test_Query",
            "target": "target:H9_Test_Package",
            "relation": "retrieved",
        },
    ]
    assert all(node["id"] != "LokumAI-1.0" for layer in projection["layers"].values() for node in layer)


def test_write_projection_outputs_json_and_markdown(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    output_dir = tmp_path / "projections"
    write_note(knowledge_dir / "RAG_Memory_Cell_13_Test.md", "# Raw\n")
    write_note(knowledge_dir / "H3_Test.md", "# H3\n\n[[RAG_Memory_Cell_13_Test]]\n")
    write_note(knowledge_dir / "H4_Test.md", "# H4\n\n[[H3_Test]]\n")
    write_note(knowledge_dir / "H5_Test_Control.md", "# H5\n\n[[H4_Test]]\n")
    write_note(knowledge_dir / "H6_Test_Executive.md", "# H6\n\n[[H5_Test_Control]]\n")
    write_note(
        knowledge_dir / "H7_Test_Episodic.md",
        "---\n"
        'episode_mode: "ordered_episode_reconstruction"\n'
        "temporal_relations:\n"
        '  - "before"\n'
        "primary_entities:\n"
        '  - "working_context"\n'
        "primary_events:\n"
        '  - "context_flush"\n'
        "---\n\n"
        "# H7\n\n"
        "[[H6_Test_Executive]]\n",
    )
    write_note(
        knowledge_dir / "H8_Test_Decision.md",
        "---\n"
        'workspace_mode: "dominant_policy_broadcast"\n'
        'dominant_thoughtseed: "recovery_first_consensus"\n'
        "candidate_policies:\n"
        '  - "stabilize_consensus_before_execution"\n'
        "broadcast_targets:\n"
        '  - "Final_Execution_Gate"\n'
        "---\n\n"
        "# H8\n\n"
        "[[H7_Test_Episodic]]\n",
    )
    write_note(
        knowledge_dir / "H9_Test_Package.md",
        "---\n"
        'package_mode: "surface_bound_policy_delivery"\n'
        'source_policy: "dominant_policy_surface_binding"\n'
        "delivery_surfaces:\n"
        '  - "Final_Execution_Gate"\n'
        "package_contracts:\n"
        '  - "surface_route_manifest"\n'
        "---\n\n"
        "# H9\n\n"
        "[[H8_Test_Decision]]\n",
    )
    write_note(
        knowledge_dir / "H10_Test_Supervision.md",
        "---\n"
        'supervision_mode: "global_supervision_arbitration"\n'
        'governing_signal: "surface_alignment_supervision"\n'
        "oversight_surfaces:\n"
        '  - "Global_State_Consensus"\n'
        "supervision_contracts:\n"
        '  - "supervision_route_manifest"\n'
        "---\n\n"
        "# H10\n\n"
        "[[H9_Test_Package]]\n",
    )
    write_note(knowledge_dir / "Index_Test.md", "# Index\n\n[[H10_Test_Supervision]]\n")

    written = layered_projection.write_projection_outputs(
        knowledge_dir=knowledge_dir,
        output_dir=output_dir,
    )

    assert [path.name for path in written] == [
        "brain_growth_layered_projection.json",
        "brain_growth_layered_projection.md",
    ]

    json_payload = json.loads((output_dir / "brain_growth_layered_projection.json").read_text(encoding="utf-8"))
    markdown = (output_dir / "brain_growth_layered_projection.md").read_text(encoding="utf-8")

    assert json_payload["layer_counts"] == {
        "raw": 1,
        "hidden_3": 1,
        "hidden_4": 1,
        "hidden_5": 1,
        "hidden_6": 1,
        "hidden_7": 1,
        "hidden_8": 1,
        "hidden_9": 1,
        "hidden_10": 1,
        "hidden_11": 0,
        "index": 1,
    }
    assert "domain_clusters" in json_payload
    assert "cluster_spread_by_layer" in json_payload
    assert "layout_quality" in json_payload
    assert json_payload["layers"]["hidden_6"][0]["layer_column"] == 4
    assert json_payload["layers"]["hidden_6"][0]["slot_index"] == 0
    assert json_payload["layers"]["hidden_6"][0]["x"] == 960
    assert json_payload["layers"]["hidden_6"][0]["y"] == 0
    assert json_payload["layers"]["hidden_7"][0]["layer_column"] == 5
    assert json_payload["layers"]["hidden_7"][0]["x"] == 1200
    assert json_payload["layers"]["hidden_8"][0]["layer_column"] == 6
    assert json_payload["layers"]["hidden_8"][0]["x"] == 1440
    assert json_payload["layers"]["hidden_9"][0]["layer_column"] == 7
    assert json_payload["layers"]["hidden_9"][0]["x"] == 1680
    assert json_payload["layers"]["hidden_10"][0]["layer_column"] == 8
    assert json_payload["layers"]["hidden_10"][0]["x"] == 1920
    assert "temporal_dual_graph" in json_payload
    assert json_payload["temporal_dual_graph"]["entity_nodes"][0]["id"] == "entity:working_context"
    assert "workspace_broadcast_graph" in json_payload
    assert json_payload["workspace_broadcast_graph"]["thoughtseed_nodes"][0]["id"] == "thoughtseed:recovery_first_consensus"
    assert "execution_package_graph" in json_payload
    assert json_payload["execution_package_graph"]["package_nodes"][0]["id"] == "package:H9_Test_Package"
    assert "strategic_supervision_graph" in json_payload
    assert json_payload["strategic_supervision_graph"]["supervision_nodes"][0]["id"] == "supervision:H10_Test_Supervision"
    assert "Brain Growth Layered Projection" in markdown
    assert "## Katman özeti" in markdown
    assert "- raw: 1" in markdown
    assert "- hidden_5_to_hidden_6: 1" in markdown
    assert "- hidden_6_to_hidden_7: 1" in markdown
    assert "- hidden_7_to_hidden_8: 1" in markdown
    assert "- hidden_8_to_hidden_9: 1" in markdown
    assert "- hidden_9_to_hidden_10: 1" in markdown
    assert "## Domain kümeleri" in markdown
    assert "## Temporal dual graph" in markdown
    assert "## Workspace broadcast graph" in markdown
    assert "## Execution package graph" in markdown
    assert "## Strategic supervision graph" in markdown
    assert "## Yerleşim kalite skorları" in markdown
    assert "layer_column=4, slot_index=0, x=960, y=0" in markdown
