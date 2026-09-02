from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.brain_growth.content_quality import (
    classify_note_depth,
    compute_quality_score,
    detect_note_kind,
    required_sections_for_kind,
)


def audit_knowledge_dir(knowledge_dir: Path) -> dict[str, object]:
    notes: list[dict[str, object]] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        kind = detect_note_kind(path)
        required_sections = required_sections_for_kind(kind)
        missing_sections = [section for section in required_sections if section not in text]
        depth_class = classify_note_depth(text, len(required_sections))
        if kind == "raw" and required_sections and len(missing_sections) >= len(required_sections) - 2:
            depth_class = "thin"
        scores = compute_quality_score(
            text=text,
            required_sections=required_sections,
            inbound_links=0,
            outbound_links=text.count("[["),
        )
        notes.append(
            {
                "path": str(path),
                "kind": kind,
                "depth_class": depth_class,
                "missing_sections": missing_sections,
                "scores": scores,
            }
        )

    summary = {
        "total_notes": len(notes),
        "thin_count": sum(1 for note in notes if note["depth_class"] == "thin"),
        "medium_count": sum(1 for note in notes if note["depth_class"] == "medium"),
        "strong_count": sum(1 for note in notes if note["depth_class"] == "strong"),
    }
    return {"summary": summary, "notes": notes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit vault content depth and section coverage.")
    parser.add_argument("--knowledge-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    report = audit_knowledge_dir(args.knowledge_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
