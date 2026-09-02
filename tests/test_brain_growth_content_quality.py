from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth.content_quality import (
    classify_note_depth,
    compute_quality_score,
    detect_note_kind,
    required_sections_for_kind,
)


def test_detect_note_kind_and_required_sections() -> None:
    assert detect_note_kind(Path("RAG_Memory_Cell_65_Test.md")) == "raw"
    assert detect_note_kind(Path("H3_Test.md")) == "synthesis"
    assert "## Teknik çekirdek" in required_sections_for_kind("raw")
    assert "## Soyutlama" in required_sections_for_kind("synthesis")


def test_classify_note_depth_uses_body_size_and_section_count() -> None:
    thin_text = "# Test\n\nKısa."
    medium_text = (
        "# Test\n\n"
        "## Teknik çekirdek\n\nBir miktar teknik açıklama.\n\n"
        "## Mimari davranış\n\nİki section var ama hâlâ kısa."
    )
    strong_text = (
        "# Test\n\n"
        "## Teknik çekirdek\n\n" + ("Yoğun teknik detay. " * 80) + "\n\n"
        "## Mimari davranış\n\n" + ("Daha fazla mekanizma. " * 50) + "\n\n"
        "## Failure modes\n\n" + ("Hata imzası. " * 25)
    )

    assert classify_note_depth(thin_text, required_section_count=8) == "thin"
    assert classify_note_depth(medium_text, required_section_count=8) == "medium"
    assert classify_note_depth(strong_text, required_section_count=8) == "strong"


def test_compute_quality_score_penalizes_missing_sections_and_missing_sources() -> None:
    text = (
        "# Test\n\n"
        "## Teknik çekirdek\n\n" + ("Detay " * 70) + "\n\n"
        "## Mimari davranış\n\n" + ("Davranış " * 40) + "\n\n"
        "## Sorgu ipuçları\n\n- foo\n- bar\n"
    )

    score = compute_quality_score(
        text=text,
        required_sections=(
            "## Teknik çekirdek",
            "## Mimari davranış",
            "## Failure modes",
            "## Sorgu ipuçları",
            "## Kaynaklar",
        ),
        inbound_links=2,
        outbound_links=3,
    )

    assert score["structure_score"] < 1.0
    assert score["source_grounding_score"] == 0.0
    assert score["retrieval_utility_score"] > 0.0
