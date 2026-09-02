from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = PROJECT_ROOT / "Lokum1.0" / "Knowledge"
FORBIDDEN_NODES = {"LokumAI-1.0", "LokumAI-1.0.md"}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER_BOUNDARY = "---"

HIDDEN_1_CANDIDATES = {
    "Anomaly_Feature_Extraction",
    "Behavioral_Feature_Mapping",
    "Cache_Miss_Detector",
    "Context_Switch_Monitor",
    "DRAM_Bandwidth_Utilization",
    "Data_Prefetch_Evaluation",
    "GPU_Performance_Counters",
    "Instruction_Fetch_Analysis",
    "L1_Cache_Hit_Ratio",
    "L2_Cache_Hit_Ratio",
    "Memory_Leak_Fingerprinting",
    "Packet_Header_Parsing",
    "Zero_Copy_Buffer_Analysis",
}

HIDDEN_2_CANDIDATES = {
    "Causal_Inference_Engine",
    "Cross_Correlation_Matrix",
    "Cryptographic_Entropy_Analysis",
    "Graph_Neural_Network_Embeddings",
    "Heap_Overflow_Heuristics",
    "Node2Vec_Mapping",
    "Pointer_Authentication_Check",
    "Probabilistic_Graphical_Models",
    "Sequence_Alignment",
    "Stack_Smash_Detection",
    "Temporal_Pattern_Recognition",
    "Topology_Analysis",
}


def read_note_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("[[") and target.endswith("]]"):
        target = target[2:-2]
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if target.endswith(".md"):
        target = Path(target).stem
    return target


def parse_wikilinks(text: str) -> list[str]:
    return [normalize_link_target(match.group(1)) for match in WIKILINK_RE.finditer(text)]


def parse_yaml_frontmatter(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        return {}

    data: dict[str, object] = {}
    current_key: str | None = None

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == FRONTMATTER_BOUNDARY:
            break
        if not stripped:
            continue
        if line.startswith("  - ") and current_key:
            current = data.setdefault(current_key, [])
            if isinstance(current, list):
                current.append(stripped[2:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        raw_value = value.strip()
        if not raw_value:
            data[current_key] = []
            continue
        data[current_key] = raw_value
    return data


def find_forbidden_node_mentions(text: str) -> set[str]:
    mentions = set()
    for forbidden in FORBIDDEN_NODES:
        if forbidden in text:
            mentions.add(forbidden)
    for target in parse_wikilinks(text):
        if target in {"LokumAI-1.0", "LokumAI-1"}:
            mentions.add("LokumAI-1.0")
    return mentions


def assert_no_forbidden_nodes(text: str) -> None:
    mentions = find_forbidden_node_mentions(text)
    if mentions:
        joined = ", ".join(sorted(mentions))
        raise ValueError(f"Forbidden node reference detected: {joined}")


def _existing_stems(candidates: set[str], knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {stem for stem in candidates if (knowledge_dir / f"{stem}.md").exists()}


def discover_hidden_1_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return _existing_stems(HIDDEN_1_CANDIDATES, knowledge_dir)


def discover_hidden_2_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return _existing_stems(HIDDEN_2_CANDIDATES, knowledge_dir)


def discover_hidden_3_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H3_*.md")}


def discover_hidden_4_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H4_*.md")}


def discover_hidden_5_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H5_*.md")}


def discover_hidden_6_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H6_*.md")}


def discover_hidden_7_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H7_*.md")}


def discover_hidden_8_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H8_*.md")}


def discover_hidden_9_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H9_*.md")}


def discover_hidden_10_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H10_*.md")}


def discover_hidden_11_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H11_*.md")}


def allowed_forward_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return (
        discover_hidden_1_targets(knowledge_dir)
        | discover_hidden_2_targets(knowledge_dir)
        | discover_hidden_3_targets(knowledge_dir)
        | discover_hidden_4_targets(knowledge_dir)
        | discover_hidden_5_targets(knowledge_dir)
        | discover_hidden_6_targets(knowledge_dir)
        | discover_hidden_7_targets(knowledge_dir)
        | discover_hidden_8_targets(knowledge_dir)
        | discover_hidden_9_targets(knowledge_dir)
        | discover_hidden_10_targets(knowledge_dir)
        | discover_hidden_11_targets(knowledge_dir)
    )


def assert_link_target_layer_membership(
    link_targets: list[str] | set[str],
    allowed_targets: set[str] | None = None,
) -> None:
    allowed = allowed_targets or allowed_forward_targets()
    invalid = sorted({normalize_link_target(target) for target in link_targets} - allowed)
    if invalid:
        raise ValueError(f"Invalid forward-link targets: {', '.join(invalid)}")


def normalize_topic_slug(topic: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", topic)
    normalized: list[str] = []
    for part in parts:
        if part.isupper() or any(char.isdigit() for char in part):
            normalized.append(part)
        else:
            normalized.append(part.capitalize())
    return "_".join(normalized)


def build_note_filename(prefix: str, topic: str, index: int | None = None) -> str:
    slug = normalize_topic_slug(topic)
    if prefix == "RAG_Memory_Cell":
        if index is None:
            raise ValueError("RAG_Memory_Cell files require an index")
        return f"{prefix}_{index:02d}_{slug}.md"
    if prefix == "H3":
        return f"{prefix}_{slug}.md"
    raise ValueError(f"Unsupported prefix: {prefix}")
