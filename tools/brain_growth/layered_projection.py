from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import (
    FORBIDDEN_NODES,
    KNOWLEDGE_DIR,
    PROJECT_ROOT,
    parse_wikilinks,
    parse_yaml_frontmatter,
    read_note_text,
)


TITLE_RE = re.compile(r"^# (.+)$", re.M)
LAYER_ORDER = (
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
)
LAYER_RANK = {name: index for index, name in enumerate(LAYER_ORDER)}
DOMAIN_PREFIXES = ("#domain/", "#hardware/", "#system/", "#reasoning/", "#navigation/", "#index/")
LAYER_X_STEP = 240
LAYER_Y_STEP = 160


def collect_layer_paths(knowledge_dir: Path) -> dict[str, list[Path]]:
    index_paths = [
        path
        for path in [knowledge_dir / "Brain_Growth_Index.md", *sorted(knowledge_dir.glob("Index_*.md"))]
        if path.exists()
    ]
    return {
        "raw": sorted(
            path for path in knowledge_dir.glob("RAG_Memory_Cell_*.md") if path.stem not in FORBIDDEN_NODES
        ),
        "hidden_3": sorted(path for path in knowledge_dir.glob("H3_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_4": sorted(path for path in knowledge_dir.glob("H4_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_5": sorted(path for path in knowledge_dir.glob("H5_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_6": sorted(path for path in knowledge_dir.glob("H6_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_7": sorted(path for path in knowledge_dir.glob("H7_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_8": sorted(path for path in knowledge_dir.glob("H8_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_9": sorted(path for path in knowledge_dir.glob("H9_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_10": sorted(path for path in knowledge_dir.glob("H10_*.md") if path.stem not in FORBIDDEN_NODES),
        "hidden_11": sorted(path for path in knowledge_dir.glob("H11_*.md") if path.stem not in FORBIDDEN_NODES),
        "index": sorted(path for path in index_paths if path.stem not in FORBIDDEN_NODES),
    }


def extract_title(text: str, fallback: str) -> str:
    match = TITLE_RE.search(text)
    return match.group(1).strip() if match else fallback.replace("_", " ")


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def clean_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [clean_tag(value) for value in values if clean_tag(value)]


def extract_domain(frontmatter: dict[str, object], layer: str) -> str:
    tags = [clean_tag(tag) for tag in frontmatter.get("tags", []) if str(tag).strip()]
    for prefix in DOMAIN_PREFIXES:
        for tag in tags:
            if tag.startswith(prefix):
                return tag.removeprefix("#")
    return layer


def note_record(path: Path, layer: str) -> dict[str, Any]:
    text = read_note_text(path)
    frontmatter = parse_yaml_frontmatter(text)
    return {
        "id": path.stem,
        "title": extract_title(text, fallback=path.stem),
        "path": str(path),
        "layer": layer,
        "domain": extract_domain(frontmatter, layer),
        "direct_links": sorted(set(parse_wikilinks(text))),
        "layout_sort_key": "",
    }


def apply_layout_metadata(layers: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    for layer in LAYER_ORDER:
        ordered_nodes = sorted(layers[layer], key=lambda node: (node["domain"], node["id"]))
        midpoint = (len(ordered_nodes) - 1) / 2
        for slot_index, node in enumerate(ordered_nodes):
            node["layout_sort_key"] = f"{node['domain']}::{node['id']}"
            node["layer_column"] = LAYER_RANK[layer]
            node["slot_index"] = slot_index
            node["x"] = LAYER_RANK[layer] * LAYER_X_STEP
            node["y"] = int((slot_index - midpoint) * LAYER_Y_STEP)
        layers[layer] = ordered_nodes
    return layers


def build_temporal_dual_graph(hidden_7_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    entity_index: dict[str, dict[str, Any]] = {}
    event_index: dict[str, dict[str, Any]] = {}
    temporal_edges: list[dict[str, Any]] = []

    for node in hidden_7_nodes:
        frontmatter = parse_yaml_frontmatter(read_note_text(Path(node["path"])))
        episode_id = node["id"]
        episode_mode = clean_tag(frontmatter.get("episode_mode", ""))
        primary_entities = clean_list(frontmatter.get("primary_entities", []))
        primary_events = clean_list(frontmatter.get("primary_events", []))
        temporal_relations = clean_list(frontmatter.get("temporal_relations", []))

        for entity in primary_entities:
            entity_record = entity_index.setdefault(
                entity,
                {"id": f"entity:{entity}", "label": entity, "episodes": []},
            )
            if episode_id not in entity_record["episodes"]:
                entity_record["episodes"].append(episode_id)

        for event in primary_events:
            event_record = event_index.setdefault(
                event,
                {"id": f"event:{event}", "label": event, "episodes": []},
            )
            if episode_id not in event_record["episodes"]:
                event_record["episodes"].append(episode_id)

        for index, relation in enumerate(temporal_relations):
            if index + 1 >= len(primary_events):
                break
            temporal_edges.append(
                {
                    "source": f"event:{primary_events[index]}",
                    "target": f"event:{primary_events[index + 1]}",
                    "relation": relation,
                    "episode": episode_id,
                    "episode_mode": episode_mode,
                }
            )

    entity_nodes = [entity_index[key] for key in sorted(entity_index)]
    event_nodes = [event_index[key] for key in sorted(event_index)]
    return {
        "entity_nodes": entity_nodes,
        "event_nodes": event_nodes,
        "temporal_edges": temporal_edges,
    }


def build_workspace_broadcast_graph(hidden_8_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    thoughtseed_index: dict[str, dict[str, Any]] = {}
    policy_index: dict[str, dict[str, Any]] = {}
    selection_edges: list[dict[str, Any]] = []
    broadcast_edges: list[dict[str, Any]] = []

    for node in hidden_8_nodes:
        frontmatter = parse_yaml_frontmatter(read_note_text(Path(node["path"])))
        episode_id = node["id"]
        workspace_mode = clean_tag(frontmatter.get("workspace_mode", ""))
        dominant_thoughtseed = clean_tag(frontmatter.get("dominant_thoughtseed", ""))
        candidate_policies = clean_list(frontmatter.get("candidate_policies", []))
        broadcast_targets = clean_list(frontmatter.get("broadcast_targets", []))

        if dominant_thoughtseed:
            thoughtseed_record = thoughtseed_index.setdefault(
                dominant_thoughtseed,
                {"id": f"thoughtseed:{dominant_thoughtseed}", "label": dominant_thoughtseed, "episodes": []},
            )
            if episode_id not in thoughtseed_record["episodes"]:
                thoughtseed_record["episodes"].append(episode_id)

        for policy in candidate_policies:
            policy_record = policy_index.setdefault(
                policy,
                {"id": f"policy:{policy}", "label": policy, "episodes": []},
            )
            if episode_id not in policy_record["episodes"]:
                policy_record["episodes"].append(episode_id)
            if dominant_thoughtseed:
                selection_edges.append(
                    {
                        "source": f"thoughtseed:{dominant_thoughtseed}",
                        "target": f"policy:{policy}",
                        "relation": "selects",
                        "episode": episode_id,
                        "workspace_mode": workspace_mode,
                    }
                )

        if candidate_policies:
            selected_policy = candidate_policies[0]
            for target in broadcast_targets:
                broadcast_edges.append(
                    {
                        "source": f"policy:{selected_policy}",
                        "target": f"target:{target}",
                        "relation": "broadcasts_to",
                        "episode": episode_id,
                    }
                )

    thoughtseed_nodes = [thoughtseed_index[key] for key in sorted(thoughtseed_index)]
    policy_nodes = [policy_index[key] for key in sorted(policy_index)]
    return {
        "thoughtseed_nodes": thoughtseed_nodes,
        "policy_nodes": policy_nodes,
        "selection_edges": selection_edges,
        "broadcast_edges": broadcast_edges,
    }


def build_execution_package_graph(hidden_9_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    policy_index: dict[str, dict[str, Any]] = {}
    package_nodes: list[dict[str, Any]] = []
    surface_index: dict[str, dict[str, Any]] = {}
    binding_edges: list[dict[str, Any]] = []
    delivery_edges: list[dict[str, Any]] = []

    for node in hidden_9_nodes:
        frontmatter = parse_yaml_frontmatter(read_note_text(Path(node["path"])))
        package_id = node["id"]
        package_mode = clean_tag(frontmatter.get("package_mode", ""))
        source_policy = clean_tag(frontmatter.get("source_policy", ""))
        delivery_surfaces = clean_list(frontmatter.get("delivery_surfaces", []))
        package_contracts = sorted(clean_list(frontmatter.get("package_contracts", [])))

        package_nodes.append(
            {
                "id": f"package:{package_id}",
                "label": package_id,
                "package_mode": package_mode,
                "contracts": package_contracts,
            }
        )

        if source_policy:
            policy_record = policy_index.setdefault(
                source_policy,
                {"id": f"source_policy:{source_policy}", "label": source_policy, "packages": []},
            )
            if package_id not in policy_record["packages"]:
                policy_record["packages"].append(package_id)
            binding_edges.append(
                {
                    "source": f"source_policy:{source_policy}",
                    "target": f"package:{package_id}",
                    "relation": "binds",
                    "package_mode": package_mode,
                }
            )

        for surface in delivery_surfaces:
            surface_record = surface_index.setdefault(
                surface,
                {"id": f"surface:{surface}", "label": surface, "packages": []},
            )
            if package_id not in surface_record["packages"]:
                surface_record["packages"].append(package_id)
            delivery_edges.append(
                {
                    "source": f"package:{package_id}",
                    "target": f"surface:{surface}",
                    "relation": "delivers_to",
                }
            )

    policy_nodes = [policy_index[key] for key in sorted(policy_index)]
    surface_nodes = [surface_index[key] for key in sorted(surface_index)]
    package_nodes = sorted(package_nodes, key=lambda item: item["id"])
    return {
        "policy_nodes": policy_nodes,
        "package_nodes": package_nodes,
        "surface_nodes": surface_nodes,
        "binding_edges": binding_edges,
        "delivery_edges": delivery_edges,
    }


def build_strategic_supervision_graph(hidden_10_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    signal_index: dict[str, dict[str, Any]] = {}
    supervision_nodes: list[dict[str, Any]] = []
    oversight_index: dict[str, dict[str, Any]] = {}
    governance_edges: list[dict[str, Any]] = []
    oversight_edges: list[dict[str, Any]] = []

    for node in hidden_10_nodes:
        frontmatter = parse_yaml_frontmatter(read_note_text(Path(node["path"])))
        supervision_id = node["id"]
        supervision_mode = clean_tag(frontmatter.get("supervision_mode", ""))
        governing_signal = clean_tag(frontmatter.get("governing_signal", ""))
        oversight_surfaces = clean_list(frontmatter.get("oversight_surfaces", []))
        supervision_contracts = sorted(clean_list(frontmatter.get("supervision_contracts", [])))

        supervision_nodes.append(
            {
                "id": f"supervision:{supervision_id}",
                "label": supervision_id,
                "supervision_mode": supervision_mode,
                "contracts": supervision_contracts,
            }
        )

        if governing_signal:
            signal_record = signal_index.setdefault(
                governing_signal,
                {"id": f"signal:{governing_signal}", "label": governing_signal, "supervision_notes": []},
            )
            if supervision_id not in signal_record["supervision_notes"]:
                signal_record["supervision_notes"].append(supervision_id)
            governance_edges.append(
                {
                    "source": f"signal:{governing_signal}",
                    "target": f"supervision:{supervision_id}",
                    "relation": "governs",
                    "supervision_mode": supervision_mode,
                }
            )

        for surface in oversight_surfaces:
            oversight_record = oversight_index.setdefault(
                surface,
                {"id": f"oversight:{surface}", "label": surface, "supervision_notes": []},
            )
            if supervision_id not in oversight_record["supervision_notes"]:
                oversight_record["supervision_notes"].append(supervision_id)
            oversight_edges.append(
                {
                    "source": f"supervision:{supervision_id}",
                    "target": f"oversight:{surface}",
                    "relation": "oversees",
                }
            )

    signal_nodes = [signal_index[key] for key in sorted(signal_index)]
    oversight_nodes = [oversight_index[key] for key in sorted(oversight_index)]
    supervision_nodes = sorted(supervision_nodes, key=lambda item: item["id"])
    return {
        "signal_nodes": signal_nodes,
        "supervision_nodes": supervision_nodes,
        "oversight_nodes": oversight_nodes,
        "governance_edges": governance_edges,
        "oversight_edges": oversight_edges,
    }


def build_reflection_audit_graph(hidden_11_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    signal_index: dict[str, dict[str, Any]] = {}
    audit_nodes: list[dict[str, Any]] = []
    surface_index: dict[str, dict[str, Any]] = {}
    signal_edges: list[dict[str, Any]] = []
    surface_edges: list[dict[str, Any]] = []

    for node in hidden_11_nodes:
        frontmatter = parse_yaml_frontmatter(read_note_text(Path(node["path"])))
        audit_id = node["id"]
        reflection_mode = clean_tag(frontmatter.get("reflection_mode", ""))
        audit_signal = clean_tag(frontmatter.get("audit_signal", ""))
        audit_surfaces = clean_list(frontmatter.get("audit_surfaces", []))
        audit_contracts = sorted(clean_list(frontmatter.get("audit_contracts", [])))

        audit_nodes.append(
            {
                "id": f"audit:{audit_id}",
                "label": audit_id,
                "reflection_mode": reflection_mode,
                "contracts": audit_contracts,
            }
        )

        if audit_signal:
            signal_record = signal_index.setdefault(
                audit_signal,
                {"id": f"signal:{audit_signal}", "label": audit_signal, "audit_notes": []},
            )
            if audit_id not in signal_record["audit_notes"]:
                signal_record["audit_notes"].append(audit_id)
            signal_edges.append(
                {
                    "source": f"signal:{audit_signal}",
                    "target": f"audit:{audit_id}",
                    "relation": "attests",
                    "reflection_mode": reflection_mode,
                }
            )

        for surface in audit_surfaces:
            surface_record = surface_index.setdefault(
                surface,
                {"id": f"surface:{surface}", "label": surface, "audit_notes": []},
            )
            if audit_id not in surface_record["audit_notes"]:
                surface_record["audit_notes"].append(audit_id)
            surface_edges.append(
                {
                    "source": f"audit:{audit_id}",
                    "target": f"surface:{surface}",
                    "relation": "audits",
                }
            )

    signal_nodes = [signal_index[key] for key in sorted(signal_index)]
    surface_nodes = [surface_index[key] for key in sorted(surface_index)]
    audit_nodes = sorted(audit_nodes, key=lambda item: item["id"])
    return {
        "signal_nodes": signal_nodes,
        "audit_nodes": audit_nodes,
        "surface_nodes": surface_nodes,
        "signal_edges": signal_edges,
        "surface_edges": surface_edges,
    }


def build_rag_binding_graph(knowledge_dir: Path, nodes_by_id: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    trace_nodes: list[dict[str, Any]] = []
    target_index: dict[str, dict[str, Any]] = {}
    rag_edges: list[dict[str, Any]] = []

    for path in sorted(knowledge_dir.glob("RAG_Trace_*.md"), key=lambda item: item.name):
        text = read_note_text(path)
        frontmatter = parse_yaml_frontmatter(text)
        query = clean_tag(frontmatter.get("query", ""))
        rag_links = sorted({target for target in clean_list(frontmatter.get("rag_links", [])) if target in nodes_by_id})
        if not rag_links:
            continue

        trace_nodes.append(
            {
                "id": f"rag_trace:{path.stem}",
                "label": extract_title(text, fallback=path.stem),
                "query": query,
                "rag_links": rag_links,
            }
        )

        for target in rag_links:
            target_record = target_index.setdefault(
                target,
                {"id": f"target:{target}", "label": target, "trace_notes": []},
            )
            if path.stem not in target_record["trace_notes"]:
                target_record["trace_notes"].append(path.stem)
            rag_edges.append(
                {
                    "source": f"rag_trace:{path.stem}",
                    "target": f"target:{target}",
                    "relation": "retrieved",
                }
            )

    trace_nodes = sorted(trace_nodes, key=lambda item: item["id"])
    target_nodes = [target_index[key] for key in sorted(target_index)]
    return {
        "trace_nodes": trace_nodes,
        "target_nodes": target_nodes,
        "rag_edges": rag_edges,
    }


def build_domain_clusters(
    nodes_by_id: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    clusters: dict[str, dict[str, Any]] = {}

    for node in nodes_by_id.values():
        cluster = clusters.setdefault(
            node["domain"],
            {
                "node_count": 0,
                "layers": Counter(),
                "internal_edge_count": 0,
                "external_edge_count": 0,
                "nodes": [],
            },
        )
        cluster["node_count"] += 1
        cluster["layers"][node["layer"]] += 1
        cluster["nodes"].append(node["id"])

    for edge in edges:
        source_domain = nodes_by_id[edge["source"]]["domain"]
        target_domain = nodes_by_id[edge["target"]]["domain"]
        if source_domain == target_domain:
            clusters[source_domain]["internal_edge_count"] += 1
            continue
        clusters[source_domain]["external_edge_count"] += 1
        clusters[target_domain]["external_edge_count"] += 1

    return {
        domain: {
            "node_count": cluster["node_count"],
            "layers": {
                layer: count
                for layer, count in sorted(
                    dict(cluster["layers"]).items(),
                    key=lambda item: (LAYER_RANK[item[0]], item[0]),
                )
            },
            "internal_edge_count": cluster["internal_edge_count"],
            "external_edge_count": cluster["external_edge_count"],
            "nodes": sorted(cluster["nodes"]),
        }
        for domain, cluster in sorted(clusters.items())
    }


def build_cluster_spread_by_layer(layers: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    spread: dict[str, dict[str, Any]] = {}
    for layer in LAYER_ORDER:
        nodes = layers[layer]
        clusters = Counter(node["domain"] for node in nodes)
        total_nodes = len(nodes)
        dominant_cluster = min(
            (domain for domain, count in clusters.items() if count == max(clusters.values(), default=0)),
            default=None,
        )
        dominant_cluster_share = round(clusters[dominant_cluster] / total_nodes, 2) if dominant_cluster else 0.0
        spread[layer] = {
            "total_nodes": total_nodes,
            "cluster_count": len(clusters),
            "dominant_cluster": dominant_cluster,
            "dominant_cluster_share": dominant_cluster_share,
            "clusters": dict(sorted(clusters.items())),
        }
    return spread


def calculate_layout_quality(
    layer_counts: dict[str, int],
    edges: list[dict[str, Any]],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, float]:
    counts = [layer_counts[layer] for layer in LAYER_ORDER]
    max_count = max(counts, default=0)
    min_count = min(counts, default=0)
    balance = 1.0 if max_count == 0 else round(min_count / max_count, 2)

    max_possible_forward_edges = 0
    running_suffix_total = 0
    for layer in reversed(LAYER_ORDER):
        max_possible_forward_edges += layer_counts[layer] * running_suffix_total
        running_suffix_total += layer_counts[layer]
    density = round(len(edges) / max_possible_forward_edges, 2) if max_possible_forward_edges else 0.0

    cross_cluster_edges = sum(
        1
        for edge in edges
        if nodes_by_id[edge["source"]]["domain"] != nodes_by_id[edge["target"]]["domain"]
    )
    cross_cluster_pressure = round(cross_cluster_edges / len(edges), 2) if edges else 0.0

    readability = round((balance + (1 - density) + (1 - cross_cluster_pressure)) / 3, 2)
    return {
        "balance": balance,
        "density": density,
        "cross_cluster_pressure": cross_cluster_pressure,
        "readability": max(0.0, min(1.0, readability)),
    }


def build_projection(knowledge_dir: Path = KNOWLEDGE_DIR) -> dict[str, Any]:
    layer_paths = collect_layer_paths(knowledge_dir)
    layers: dict[str, list[dict[str, Any]]] = {
        layer: [note_record(path, layer) for path in paths]
        for layer, paths in layer_paths.items()
    }
    layers = apply_layout_metadata(layers)

    nodes_by_id = {
        node["id"]: node
        for layer_nodes in layers.values()
        for node in layer_nodes
    }

    edges_seen: set[tuple[str, str]] = set()
    outgoing_counts = Counter()
    incoming_counts = Counter()
    transition_counts = Counter()

    for layer_nodes in layers.values():
        for node in layer_nodes:
            for target_id in node["direct_links"]:
                if target_id not in nodes_by_id or target_id in FORBIDDEN_NODES or target_id == node["id"]:
                    continue
                source_node = node
                target_node = nodes_by_id[target_id]
                source_rank = LAYER_RANK[source_node["layer"]]
                target_rank = LAYER_RANK[target_node["layer"]]
                if source_rank <= target_rank:
                    edge = (source_node["id"], target_node["id"])
                else:
                    edge = (target_node["id"], source_node["id"])
                if edge in edges_seen:
                    continue
                edges_seen.add(edge)
                outgoing_counts[edge[0]] += 1
                incoming_counts[edge[1]] += 1
                transition_counts[
                    f"{nodes_by_id[edge[0]]['layer']}_to_{nodes_by_id[edge[1]]['layer']}"
                ] += 1

    for layer_nodes in layers.values():
        for node in layer_nodes:
            node["tracked_links"] = sorted(
                {target_id for target_id in node["direct_links"] if target_id in nodes_by_id and target_id not in FORBIDDEN_NODES}
            )
            node["incoming_edge_count"] = incoming_counts[node["id"]]
            node["outgoing_edge_count"] = outgoing_counts[node["id"]]

    edges = [
        {
            "source": source,
            "target": target,
            "source_layer": nodes_by_id[source]["layer"],
            "target_layer": nodes_by_id[target]["layer"],
        }
        for source, target in sorted(
            edges_seen,
            key=lambda edge: (
                LAYER_RANK[nodes_by_id[edge[0]]["layer"]],
                LAYER_RANK[nodes_by_id[edge[1]]["layer"]],
                edge[0],
                edge[1],
            ),
        )
    ]

    layer_counts = {layer: len(layers[layer]) for layer in LAYER_ORDER}
    domain_clusters = build_domain_clusters(nodes_by_id, edges)
    cluster_spread_by_layer = build_cluster_spread_by_layer(layers)
    layout_quality = calculate_layout_quality(layer_counts, edges, nodes_by_id)
    ordered_transitions = {
        name: count
        for name, count in sorted(
            transition_counts.items(),
            key=lambda item: (
                LAYER_RANK[item[0].split("_to_")[0]],
                LAYER_RANK[item[0].split("_to_")[1]],
                item[0],
            ),
        )
    }
    temporal_dual_graph = build_temporal_dual_graph(layers["hidden_7"])
    workspace_broadcast_graph = build_workspace_broadcast_graph(layers["hidden_8"])
    execution_package_graph = build_execution_package_graph(layers["hidden_9"])
    strategic_supervision_graph = build_strategic_supervision_graph(layers["hidden_10"])
    reflection_audit_graph = build_reflection_audit_graph(layers["hidden_11"])
    rag_binding_graph = build_rag_binding_graph(knowledge_dir, nodes_by_id)

    return {
        "knowledge_dir": str(knowledge_dir),
        "layer_order": list(LAYER_ORDER),
        "layer_counts": layer_counts,
        "layers": {layer: layers[layer] for layer in LAYER_ORDER},
        "domain_clusters": domain_clusters,
        "cluster_spread_by_layer": cluster_spread_by_layer,
        "layout_quality": layout_quality,
        "transition_counts": ordered_transitions,
        "temporal_dual_graph": temporal_dual_graph,
        "workspace_broadcast_graph": workspace_broadcast_graph,
        "execution_package_graph": execution_package_graph,
        "strategic_supervision_graph": strategic_supervision_graph,
        "reflection_audit_graph": reflection_audit_graph,
        "rag_binding_graph": rag_binding_graph,
        "edges": edges,
        "summary": {
            "total_nodes": sum(layer_counts.values()),
            "total_edges": len(edges),
            "rag_trace_count": len(rag_binding_graph["trace_nodes"]),
            "rag_edge_count": len(rag_binding_graph["rag_edges"]),
        },
    }


def render_projection_markdown(projection: dict[str, Any]) -> str:
    lines = [
        "# Brain Growth Layered Projection",
        "",
        "## Kaynak",
        "",
        f"- knowledge_dir: `{projection['knowledge_dir']}`",
        f"- total_nodes: {projection['summary']['total_nodes']}",
        f"- total_edges: {projection['summary']['total_edges']}",
        "",
        "## Katman özeti",
        "",
    ]

    for layer in projection["layer_order"]:
        lines.append(f"- {layer}: {projection['layer_counts'][layer]}")

    lines.extend(["", "## Katman geçişleri", ""])
    if projection["transition_counts"]:
        for transition_name, count in projection["transition_counts"].items():
            lines.append(f"- {transition_name}: {count}")
    else:
        lines.append("- none: 0")

    lines.extend(["", "## Domain kümeleri", ""])
    if projection["domain_clusters"]:
        for domain, summary in projection["domain_clusters"].items():
            layer_mix = ", ".join(f"{layer}={count}" for layer, count in summary["layers"].items()) or "none"
            lines.append(
                "- "
                f"{domain}: "
                f"node_count={summary['node_count']}, "
                f"internal_edges={summary['internal_edge_count']}, "
                f"external_edges={summary['external_edge_count']}, "
                f"layers={layer_mix}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Katman bazlı cluster yayılımı", ""])
    for layer in projection["layer_order"]:
        spread = projection["cluster_spread_by_layer"][layer]
        lines.append(
            "- "
            f"{layer}: "
            f"cluster_count={spread['cluster_count']}, "
            f"dominant_cluster={spread['dominant_cluster']}, "
            f"dominant_cluster_share={spread['dominant_cluster_share']}"
        )

    lines.extend(["", "## Yerleşim kalite skorları", ""])
    for score_name, value in projection["layout_quality"].items():
        lines.append(f"- {score_name}: {value}")

    lines.extend(["", "## Temporal dual graph", ""])
    lines.append(f"- entity_nodes: {len(projection['temporal_dual_graph']['entity_nodes'])}")
    lines.append(f"- event_nodes: {len(projection['temporal_dual_graph']['event_nodes'])}")
    lines.append(f"- temporal_edges: {len(projection['temporal_dual_graph']['temporal_edges'])}")

    lines.extend(["", "## Workspace broadcast graph", ""])
    lines.append(f"- thoughtseed_nodes: {len(projection['workspace_broadcast_graph']['thoughtseed_nodes'])}")
    lines.append(f"- policy_nodes: {len(projection['workspace_broadcast_graph']['policy_nodes'])}")
    lines.append(f"- selection_edges: {len(projection['workspace_broadcast_graph']['selection_edges'])}")
    lines.append(f"- broadcast_edges: {len(projection['workspace_broadcast_graph']['broadcast_edges'])}")

    lines.extend(["", "## Execution package graph", ""])
    lines.append(f"- policy_nodes: {len(projection['execution_package_graph']['policy_nodes'])}")
    lines.append(f"- package_nodes: {len(projection['execution_package_graph']['package_nodes'])}")
    lines.append(f"- surface_nodes: {len(projection['execution_package_graph']['surface_nodes'])}")
    lines.append(f"- binding_edges: {len(projection['execution_package_graph']['binding_edges'])}")
    lines.append(f"- delivery_edges: {len(projection['execution_package_graph']['delivery_edges'])}")

    lines.extend(["", "## Strategic supervision graph", ""])
    lines.append(f"- signal_nodes: {len(projection['strategic_supervision_graph']['signal_nodes'])}")
    lines.append(f"- supervision_nodes: {len(projection['strategic_supervision_graph']['supervision_nodes'])}")
    lines.append(f"- oversight_nodes: {len(projection['strategic_supervision_graph']['oversight_nodes'])}")
    lines.append(f"- governance_edges: {len(projection['strategic_supervision_graph']['governance_edges'])}")
    lines.append(f"- oversight_edges: {len(projection['strategic_supervision_graph']['oversight_edges'])}")

    lines.extend(["", "## Düğümler", ""])
    for layer in projection["layer_order"]:
        nodes = projection["layers"][layer]
        lines.extend([f"### {layer}", ""])
        if not nodes:
            lines.append("- none")
            lines.append("")
            continue
        for node in nodes:
            lines.append(
                "- "
                f"[[{node['id']}]] "
                f"("
                f"domain={node['domain']}, "
                f"incoming={node['incoming_edge_count']}, "
                f"outgoing={node['outgoing_edge_count']}, "
                f"layer_column={node['layer_column']}, "
                f"slot_index={node['slot_index']}, "
                f"x={node['x']}, "
                f"y={node['y']}"
                f")"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_projection_outputs(
    knowledge_dir: Path = KNOWLEDGE_DIR,
    output_dir: Path | None = None,
) -> list[Path]:
    output_root = output_dir or (PROJECT_ROOT / "docs" / "brain_growth" / "projections")
    output_root.mkdir(parents=True, exist_ok=True)

    projection = build_projection(knowledge_dir=knowledge_dir)
    json_path = output_root / "brain_growth_layered_projection.json"
    md_path = output_root / "brain_growth_layered_projection.md"

    json_path.write_text(json.dumps(projection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_projection_markdown(projection), encoding="utf-8")
    return [json_path, md_path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a layered projection export for the brain-growth vault.")
    parser.add_argument("--knowledge-dir", type=Path, default=KNOWLEDGE_DIR)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    written = write_projection_outputs(knowledge_dir=args.knowledge_dir, output_dir=args.output_dir)
    projection = build_projection(knowledge_dir=args.knowledge_dir)
    print("Write completed.")
    print(f"- total_nodes={projection['summary']['total_nodes']}")
    print(f"- total_edges={projection['summary']['total_edges']}")
    for path in written:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
