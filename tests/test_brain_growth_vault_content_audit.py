from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth.vault_content_audit import audit_knowledge_dir


def write_note(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_audit_knowledge_dir_groups_notes_by_depth(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    write_note(knowledge_dir / "RAG_Memory_Cell_65_Test.md", "# Thin\n\nKısa.")
    write_note(
        knowledge_dir / "H3_Test.md",
        "# H3\n\n## Soyutlama\n\n"
        + ("Detay " * 90)
        + "\n\n## İnvariantlar\n\n"
        + ("Detay " * 60),
    )

    report = audit_knowledge_dir(knowledge_dir)

    assert report["summary"]["total_notes"] == 2
    assert report["summary"]["thin_count"] == 1
    assert report["summary"]["medium_count"] + report["summary"]["strong_count"] == 1
    assert report["notes"][0]["path"].endswith(".md")


def test_audit_knowledge_dir_tracks_missing_sections(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    write_note(
        knowledge_dir / "RAG_Memory_Cell_66_Test.md",
        "# Test\n\n## Teknik çekirdek\n\n" + ("Detay " * 80),
    )

    report = audit_knowledge_dir(knowledge_dir)

    assert "## Mimari davranış" in report["notes"][0]["missing_sections"]
    assert report["notes"][0]["depth_class"] == "thin"


def test_vault_content_audit_cli_writes_json(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "RAG_Memory_Cell_99_Test.md").write_text("# Test\n\nKısa", encoding="utf-8")
    output = tmp_path / "audit.json"

    completed = subprocess.run(
        [
            "python3",
            "-m",
            "tools.brain_growth.vault_content_audit",
            "--knowledge-dir",
            str(knowledge_dir),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd="/Users/fox/Documents/PROJECTS/LokumAI",
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert "Wrote" in completed.stdout
    assert data["summary"]["total_notes"] == 1
