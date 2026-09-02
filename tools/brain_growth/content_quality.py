from __future__ import annotations

import re
from pathlib import Path

RAW_REQUIRED_SECTIONS = (
    "## Teknik çekirdek",
    "## Mimari davranış",
    "## Kritik sınırlamalar",
    "## Failure modes",
    "## Debug / telemetry / profiling sinyalleri",
    "## LokumAI için çıkarım",
    "## Sorgu ipuçları",
    "## Kaynaklar",
)

SYNTHESIS_REQUIRED_SECTIONS = (
    "## Soyutlama",
    "## İnvariantlar",
    "## Retrieval yönlendirme anlamı",
    "## Besleyen düğümler",
    "## İleri besleme",
)

INDEX_REQUIRED_SECTIONS = (
    "## Alanlar",
    "## Fazlar",
    "## Kullanım",
)


def detect_note_kind(path: Path) -> str:
    stem = path.stem
    if stem.startswith("RAG_Memory_Cell_"):
        return "raw"
    if stem.startswith("H3_"):
        return "synthesis"
    if stem.startswith("Index_"):
        return "index"
    if stem.startswith(("H4_", "H5_", "H6_", "H7_", "H8_", "H9_", "H10_", "H11_")):
        return "governance"
    return "other"


def required_sections_for_kind(kind: str) -> tuple[str, ...]:
    mapping = {
        "raw": RAW_REQUIRED_SECTIONS,
        "synthesis": SYNTHESIS_REQUIRED_SECTIONS,
        "index": INDEX_REQUIRED_SECTIONS,
    }
    return mapping.get(kind, ())


def classify_note_depth(text: str, required_section_count: int) -> str:
    body_words = len(re.findall(r"\w+", text))
    section_count = text.count("\n## ")
    minimum_structured_sections = min(max(required_section_count, 1), 2)
    if body_words < 20 and section_count < minimum_structured_sections:
        return "thin"
    if body_words >= 320 and section_count >= 3:
        return "strong"
    return "medium"


def compute_quality_score(
    *,
    text: str,
    required_sections: tuple[str, ...],
    inbound_links: int,
    outbound_links: int,
) -> dict[str, float]:
    present_sections = sum(1 for section in required_sections if section in text)
    structure_score = present_sections / max(len(required_sections), 1)
    technical_depth_score = min(len(re.findall(r"\w+", text)) / 450, 1.0)
    retrieval_utility_score = (
        1.0 if "## Sorgu ipuçları" in text or "## Retrieval yönlendirme anlamı" in text else 0.0
    )
    source_grounding_score = 1.0 if "## Kaynaklar" in text and "http" in text else 0.0
    graph_integration_score = min((inbound_links + outbound_links) / 6, 1.0)
    return {
        "structure_score": round(structure_score, 3),
        "technical_depth_score": round(technical_depth_score, 3),
        "retrieval_utility_score": round(retrieval_utility_score, 3),
        "source_grounding_score": round(source_grounding_score, 3),
        "graph_integration_score": round(graph_integration_score, 3),
    }
