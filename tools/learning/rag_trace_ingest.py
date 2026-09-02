from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_KNOWLEDGE_DIR = Path("Lokum1.0/Knowledge")

SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_]+")


def _utc_compact_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _safe_id(raw: str) -> str:
    cleaned = SAFE_ID_RE.sub("_", raw.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or _utc_compact_timestamp()


def _as_list(value: object) -> list[object]:
    if isinstance(value, list):
        return value
    return []


def _stem_from_path_like(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    try:
        path = Path(raw)
        if path.suffix.lower() == ".md":
            return path.stem
    except Exception:
        pass
    # Bazı UI exportları "H9_..." gibi stem döndürebilir.
    if raw.endswith(".md"):
        return Path(raw).stem
    if re.match(r"^[A-Za-z0-9_]+$", raw):
        return raw
    return None


def extract_rag_targets(trace: dict[str, Any]) -> list[str]:
    """
    UI export JSON → hedef not id listesi (stem).

    Desteklenen input şekilleri:
    - core/rag_engine.py `query_with_sources()` çıktısı:
      {
        "query": "...",
        "sources": [{"source_path": ".../Knowledge/H10_X.md", ...}, ...],
        "distances": [...],
        ...
      }
    - custom:
      { "matched_nodes": ["H10_X", "H9_Y"] }
      { "targets": ["H10_X"] }
      { "results": [{"note_id": "H10_X"}] }
    """
    targets: list[str] = []

    # 1) sources[*].source_path or note_id
    for src in _as_list(trace.get("sources")):
        if isinstance(src, dict):
            for key in ("note_id", "node_id", "id", "stem"):
                stem = _stem_from_path_like(src.get(key))
                if stem:
                    targets.append(stem)
                    break
            stem = _stem_from_path_like(src.get("source_path"))
            if stem:
                targets.append(stem)

    # 2) results[*].note_id
    for row in _as_list(trace.get("results")):
        if isinstance(row, dict):
            stem = _stem_from_path_like(row.get("note_id") or row.get("node_id") or row.get("id"))
            if stem:
                targets.append(stem)
            stem2 = _stem_from_path_like(row.get("source_path"))
            if stem2:
                targets.append(stem2)

    # 3) matched_nodes / targets (string list)
    for key in ("matched_nodes", "targets", "top_nodes"):
        for item in _as_list(trace.get(key)):
            stem = _stem_from_path_like(item)
            if stem:
                targets.append(stem)

    # uniq preserve order
    seen: set[str] = set()
    ordered: list[str] = []
    for t in targets:
        if t in seen:
            continue
        seen.add(t)
        ordered.append(t)
    return ordered


def render_rag_trace_note(*, trace_id: str, query: str, targets: list[str], raw_trace: dict[str, Any]) -> str:
    safe_trace_id = _safe_id(trace_id)
    query_line = query.strip().replace("\n", " ").strip()
    if not query_line:
        query_line = "<empty>"

    # Distances (optional)
    distances = _as_list(raw_trace.get("distances"))
    dist_lines: list[str] = []
    for i, dist in enumerate(distances[: min(len(distances), len(targets))]):
        try:
            dist_lines.append(f"- {targets[i]}: {float(dist):.6f}")
        except Exception:
            continue

    fm = [
        "---",
        f'date: "{datetime.now(timezone.utc).strftime("%Y-%m-%d")}"',
        "tags:",
        '  - "#layer/input_rag"',
        '  - "#rag/trace"',
        '  - "#rag/link_binding"',
        f'trace_id: "{safe_trace_id}"',
        f'query: "{query_line}"',
        "rag_links:",
    ]
    for t in targets:
        fm.append(f'  - "{t}"')
    fm.append("---")

    body = [
        f"# RAG Trace {safe_trace_id}",
        "",
        "## Sorgu",
        "",
        query.strip() or "<empty>",
        "",
        "## RAG bağları (rag_links)",
        "",
        *[f"- [[{t}]]" for t in targets],
        "",
    ]
    if dist_lines:
        body.extend(["## Skorlar (distance)", "", *dist_lines, ""])

    body.extend(
        [
            "## Ham trace (kısaltılmış)",
            "",
            "```json",
            json.dumps(raw_trace, ensure_ascii=False, indent=2)[:8000],
            "```",
            "",
        ]
    )

    return "\n".join([*fm, "", *body])


@dataclass(frozen=True)
class IngestResult:
    trace_note_path: Path
    target_count: int


def ingest_trace_json(
    *,
    trace_json_path: Path,
    knowledge_dir: Path,
    overwrite: bool = False,
) -> IngestResult:
    trace = json.loads(trace_json_path.read_text(encoding="utf-8"))
    if not isinstance(trace, dict):
        raise ValueError("RAG trace JSON bir object/dict olmalı")

    trace_id = str(trace.get("trace_id") or trace.get("id") or trace_json_path.stem)
    query = str(trace.get("query") or trace.get("query_text") or trace.get("prompt") or "")
    targets = extract_rag_targets(trace)

    # Valid targets = vault içinde var olan notlar (stem eşleşmesi)
    existing = {p.stem for p in knowledge_dir.glob("*.md")}
    filtered = [t for t in targets if t in existing and t != "LokumAI-1.0"]

    note_name = f"RAG_Trace_{_safe_id(trace_id)}.md"
    out_path = knowledge_dir / note_name
    if out_path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing trace note: {out_path.name}")

    note_text = render_rag_trace_note(trace_id=trace_id, query=query, targets=filtered, raw_trace=trace)
    out_path.write_text(note_text, encoding="utf-8")

    return IngestResult(trace_note_path=out_path, target_count=len(filtered))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UI RAG JSON export → vault içinde RAG trace notu üret.")
    parser.add_argument("--in", dest="in_path", type=Path, required=True, help="RAG trace JSON dosyası")
    parser.add_argument("--knowledge-dir", type=Path, default=DEFAULT_KNOWLEDGE_DIR)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    result = ingest_trace_json(trace_json_path=args.in_path, knowledge_dir=args.knowledge_dir, overwrite=args.overwrite)
    print(json.dumps({"trace_note": str(result.trace_note_path), "target_count": result.target_count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

