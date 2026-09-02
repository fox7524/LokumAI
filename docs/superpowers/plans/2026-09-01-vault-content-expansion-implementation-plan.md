# Vault Content Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** LokumAI vault içindeki ince `.md` düğümlerini reasoning-grade teknik notlara dönüştürmek, yeni embedded platform corpus’u eklemek ve içerik kalitesini validator ile ölçülebilir hale getirmek.

**Architecture:** Uygulama iki paralel eksende ilerler: önce içerik kalitesini ölçen ve section/derinlik skoru üreten küçük bir audit katmanı eklenir, ardından bu audit çıktısına dayanarak mevcut zayıf notlar ve yeni embedded corpus dalga dalga yazılır. Son adımda index/synthesis düğümleri güncellenir ve validator raporu ile graph kurallarının korunup korunmadığı doğrulanır.

**Tech Stack:** Python 3.13, `pytest`, mevcut `tools/brain_growth` validator/projection araçları, Obsidian Markdown vault, YAML frontmatter, mevcut `quality_validator.py` raporlama modeli.

---

## File map

### Create

- `tools/brain_growth/content_quality.py`
- `tools/brain_growth/vault_content_audit.py`
- `tests/test_brain_growth_content_quality.py`
- `tests/test_brain_growth_vault_content_audit.py`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity.md`

### Modify

- `tools/brain_growth/quality_validator.py`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md`
- `Lokum1.0/Knowledge/H3_Embedded_Interrupt_DMA_Synthesis.md`
- `Lokum1.0/Knowledge/Index_Embedded_and_ESP32.md`
- `tests/test_brain_growth_validator.py`

## Task 1: Content quality primitives

**Files:**
- Create: `tools/brain_growth/content_quality.py`
- Test: `tests/test_brain_growth_content_quality.py`

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_brain_growth_content_quality.py -q`

Expected: `ModuleNotFoundError` or `ImportError` because `content_quality.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

from pathlib import Path
import re

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
        "index": ("## Alanlar", "## Fazlar", "## Kullanım"),
    }
    return mapping.get(kind, ())


def classify_note_depth(text: str, required_section_count: int) -> str:
    body_words = len(re.findall(r"\w+", text))
    section_count = text.count("\n## ")
    coverage = section_count / max(required_section_count, 1)
    if body_words < 120 or coverage < 0.35:
        return "thin"
    if body_words < 320 or coverage < 0.7:
        return "medium"
    return "strong"


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
    retrieval_utility_score = 1.0 if "## Sorgu ipuçları" in text or "## Retrieval yönlendirme anlamı" in text else 0.0
    source_grounding_score = 1.0 if "## Kaynaklar" in text and "http" in text else 0.0
    graph_integration_score = min((inbound_links + outbound_links) / 6, 1.0)
    return {
        "structure_score": round(structure_score, 3),
        "technical_depth_score": round(technical_depth_score, 3),
        "retrieval_utility_score": round(retrieval_utility_score, 3),
        "source_grounding_score": round(source_grounding_score, 3),
        "graph_integration_score": round(graph_integration_score, 3),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_brain_growth_content_quality.py -q`

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add tests/test_brain_growth_content_quality.py tools/brain_growth/content_quality.py
git commit -m "feat: add vault content quality primitives"
```

## Task 2: Vault content audit CLI

**Files:**
- Create: `tools/brain_growth/vault_content_audit.py`
- Test: `tests/test_brain_growth_vault_content_audit.py`

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path

from tools.brain_growth.vault_content_audit import audit_knowledge_dir


def write_note(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_audit_knowledge_dir_groups_notes_by_depth(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    write_note(knowledge_dir / "RAG_Memory_Cell_65_Test.md", "# Thin\\n\\nKısa.")
    write_note(
        knowledge_dir / "H3_Test.md",
        "# H3\\n\\n## Soyutlama\\n\\n" + ("Detay " * 90) + "\\n\\n## İnvariantlar\\n\\n" + ("Detay " * 60),
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
        "# Test\\n\\n## Teknik çekirdek\\n\\n" + ("Detay " * 80),
    )

    report = audit_knowledge_dir(knowledge_dir)

    assert "## Mimari davranış" in report["notes"][0]["missing_sections"]
    assert report["notes"][0]["depth_class"] == "thin"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_brain_growth_vault_content_audit.py -q`

Expected: FAIL because `vault_content_audit.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

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
    import argparse

    parser = argparse.ArgumentParser(description="Audit vault content depth and section coverage.")
    parser.add_argument("--knowledge-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    report = audit_knowledge_dir(args.knowledge_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_brain_growth_vault_content_audit.py -q`

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add tests/test_brain_growth_vault_content_audit.py tools/brain_growth/vault_content_audit.py
git commit -m "feat: add vault content audit report"
```

## Task 3: Integrate quality scoring into validator

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`
- Create/Reuse: `tools/brain_growth/content_quality.py`

- [ ] **Step 1: Write the failing validator tests**

```python
from pathlib import Path

from tools.brain_growth.quality_validator import validate_raw_note


def write_note(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_validate_raw_note_reports_thin_content_and_missing_sources(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    note = knowledge_dir / "RAG_Memory_Cell_65_Test.md"
    write_note(
        note,
        "---\\ntags:\\n  - \\\"#rag/memory_cell\\\"\\n---\\n\\n"
        "# Test\\n\\n## Teknik çekirdek\\n\\nKısa gövde.",
    )

    report = validate_raw_note(note, knowledge_dir=knowledge_dir)
    codes = {issue.code for issue in report.issues}

    assert "thin_note" in codes
    assert "missing_sources" in codes
    assert report.metrics["depth_class"] == "thin"
    assert "technical_depth_score" in report.metrics
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_validate_raw_note_reports_thin_content_and_missing_sources -q`

Expected: FAIL because `thin_note` and `missing_sources` are not emitted yet.

- [ ] **Step 3: Write minimal validator integration**

```python
from tools.brain_growth.content_quality import (
    classify_note_depth,
    compute_quality_score,
)

ISSUE_CATALOG["thin_note"] = {
    "severity": "warning",
    "repair_class": "content_depth_repair",
}
ISSUE_CATALOG["missing_sources"] = {
    "severity": "warning",
    "repair_class": "source_grounding_repair",
}


def append_content_quality_issues(
    *,
    path: Path,
    text: str,
    required_sections: tuple[str, ...],
    issues: list[Issue],
    metrics: dict[str, object],
) -> None:
    depth_class = classify_note_depth(text, len(required_sections))
    quality_scores = compute_quality_score(
        text=text,
        required_sections=required_sections,
        inbound_links=0,
        outbound_links=len(parse_wikilinks(text)),
    )
    metrics["depth_class"] = depth_class
    metrics.update(quality_scores)
    if depth_class == "thin":
        issues.append(build_issue("thin_note", f"{path.name}: içerik gövdesi çok ince"))
    if "## Kaynaklar" not in text or "http" not in text:
        issues.append(build_issue("missing_sources", f"{path.name}: kaynak bölümü veya URL izi eksik"))
```

Call `append_content_quality_issues(...)` from `validate_raw_note`, `validate_synthesis_note`, and `validate_index_note` immediately after `validate_common_shape(...)`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_brain_growth_content_quality.py tests/test_brain_growth_validator.py::test_validate_raw_note_reports_thin_content_and_missing_sources -q`

Expected: PASS with no new warnings from pytest.

- [ ] **Step 5: Commit**

```bash
git add tools/brain_growth/content_quality.py tools/brain_growth/quality_validator.py tests/test_brain_growth_validator.py
git commit -m "feat: score vault content depth in validator"
```

## Task 4: Deepen the first embedded note cluster

**Files:**
- Modify: `Lokum1.0/Knowledge/RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md`
- Modify: `Lokum1.0/Knowledge/RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md`
- Modify: `Lokum1.0/Knowledge/RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md`

- [ ] **Step 1: Write the failing content regression test**

```python
from pathlib import Path

from tools.brain_growth.quality_validator import validate_raw_note


def test_embedded_cluster_notes_reach_medium_or_better(tmp_path: Path) -> None:
    knowledge_dir = Path("Lokum1.0/Knowledge")
    for name in (
        "RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md",
        "RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md",
        "RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md",
    ):
        report = validate_raw_note(knowledge_dir / name, knowledge_dir=knowledge_dir)
        assert report.metrics["depth_class"] in {"medium", "strong"}
        assert "thin_note" not in {issue.code for issue in report.issues}
```

Add this test to `tests/test_brain_growth_validator.py`.

- [ ] **Step 2: Run test to verify current failure**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_embedded_cluster_notes_reach_medium_or_better -q`

Expected: FAIL on at least one note currently classified as `thin`.

- [ ] **Step 3: Rewrite the three notes to the new raw-note standard**

Use this section skeleton in all three files:

```markdown
## Teknik çekirdek

## Mimari davranış

## Kritik sınırlamalar

## Failure modes

## Debug / telemetry / profiling sinyalleri

## LokumAI için çıkarım

## Sorgu ipuçları

## Kaynaklar
```

Minimum content expectations:

- `RAG_Memory_Cell_04...`
  - Core 0 tick responsibility
  - `tskNO_AFFINITY` trade-offs
  - starvation / drift signals
  - scheduler debug heuristics
- `RAG_Memory_Cell_05...`
  - shared interrupt allocation limits
  - ISR handler cohabitation failure modes
  - IRAM-safe constraints
  - interrupt latency signatures under load
- `RAG_Memory_Cell_06...`
  - DMA-capable memory regions
  - preallocation vs runtime allocation trade-off
  - cache/PSRAM implications
  - underrun / descriptor starvation signatures

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_embedded_cluster_notes_reach_medium_or_better -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add Lokum1.0/Knowledge/RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md \
        tests/test_brain_growth_validator.py
git commit -m "docs: deepen core esp32 embedded memory cells"
```

## Task 5: Add the first new embedded corpus wave

**Files:**
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension.md`
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure.md`
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries.md`
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug.md`
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints.md`
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes.md`
- Create: `Lokum1.0/Knowledge/RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity.md`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write the failing test for the new corpus files**

```python
from pathlib import Path

from tools.brain_growth.quality_validator import validate_raw_note


def test_new_embedded_corpus_files_validate_cleanly() -> None:
    knowledge_dir = Path("Lokum1.0/Knowledge")
    for name in (
        "RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension.md",
        "RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure.md",
        "RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries.md",
        "RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug.md",
        "RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints.md",
        "RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes.md",
        "RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity.md",
    ):
        report = validate_raw_note(knowledge_dir / name, knowledge_dir=knowledge_dir)
        assert report.metrics["depth_class"] in {"medium", "strong"}
        assert "missing_section" not in {issue.code for issue in report.issues}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_new_embedded_corpus_files_validate_cleanly -q`

Expected: FAIL with missing-file error.

- [ ] **Step 3: Create the seven new raw notes**

Use this exact frontmatter shape in each file:

```yaml
---
date: 2026-09-01
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/<platform_or_stack>"
---
```

And this exact section layout:

```markdown
# <Title>

## Teknik çekirdek

## Mimari davranış

## Kritik sınırlamalar

## Failure modes

## Debug / telemetry / profiling sinyalleri

## LokumAI için çıkarım

## Sorgu ipuçları

## Kaynaklar
```

Required topic focus by file:

- `65`: ESP32-S3 SIMD/vector instruction alignment, DMA buffer alignment, PSRAM/throughput tension
- `66`: ESP8266/NodeMCU Wi-Fi stack latency, watchdog pressure, event-loop blocking signatures
- `67`: STM32 DMA vs D-cache coherency, ISR boundaries, invalidate/clean discipline
- `68`: RP2040 PIO state machine timing drift, FIFO underrun, IRQ pacing
- `69`: nRF52 SoftDevice interrupt priority ceilings, BLE concurrency, radio timing conflicts
- `70`: Zephyr devicetree binding mistakes, driver bringup failures, Kconfig parity drift
- `71`: PlatformIO env divergence, compile flag parity drift, framework mismatch symptoms

Each note must include:

- at least 350-500 words
- at least 2 outbound wikilinks into existing vault nodes
- at least 1 official documentation URL in `## Kaynaklar`

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_new_embedded_corpus_files_validate_cleanly -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add Lokum1.0/Knowledge/RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity.md \
        tests/test_brain_growth_validator.py
git commit -m "docs: add first embedded corpus expansion wave"
```

## Task 6: Upgrade synthesis and index nodes

**Files:**
- Modify: `Lokum1.0/Knowledge/H3_Embedded_Interrupt_DMA_Synthesis.md`
- Modify: `Lokum1.0/Knowledge/Index_Embedded_and_ESP32.md`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path

from tools.brain_growth.quality_validator import validate_index_note, validate_synthesis_note


def test_embedded_synthesis_and_index_have_no_thin_content() -> None:
    knowledge_dir = Path("Lokum1.0/Knowledge")
    synthesis = validate_synthesis_note(
        knowledge_dir / "H3_Embedded_Interrupt_DMA_Synthesis.md",
        knowledge_dir=knowledge_dir,
    )
    index_report = validate_index_note(knowledge_dir / "Index_Embedded_and_ESP32.md")

    assert synthesis.metrics["depth_class"] in {"medium", "strong"}
    assert index_report.metrics["depth_class"] in {"medium", "strong"}
    assert "thin_note" not in {issue.code for issue in synthesis.issues}
    assert "thin_note" not in {issue.code for issue in index_report.issues}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_embedded_synthesis_and_index_have_no_thin_content -q`

Expected: FAIL because one or both notes are still too thin.

- [ ] **Step 3: Rewrite the synthesis and index notes**

For `H3_Embedded_Interrupt_DMA_Synthesis.md`, add explicit content to:

- `## Soyutlama`
- `## İnvariantlar`
- `## Retrieval yönlendirme anlamı`
- `## Besleyen düğümler`
- `## İleri besleme`

For `Index_Embedded_and_ESP32.md`, ensure it includes:

- alan özeti
- kapsama sınırı
- temsilci yeni corpus notları (`65-71`)
- hangi semptomta hangi cluster’a gidileceği
- bilinen boşluklar

Include these new links in the index:

```markdown
- [[RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension]]
- [[RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure]]
- [[RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries]]
- [[RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug]]
- [[RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints]]
- [[RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes]]
- [[RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity]]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_embedded_synthesis_and_index_have_no_thin_content -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add Lokum1.0/Knowledge/H3_Embedded_Interrupt_DMA_Synthesis.md \
        Lokum1.0/Knowledge/Index_Embedded_and_ESP32.md \
        tests/test_brain_growth_validator.py
git commit -m "docs: upgrade embedded synthesis and index routing notes"
```

## Task 7: Produce audit report and full verification

**Files:**
- Create/Write output: `docs/brain_growth/reports/vault_content_audit.json`
- Modify if needed: `tools/brain_growth/vault_content_audit.py`

- [ ] **Step 1: Add a smoke test for the CLI**

```python
from pathlib import Path
import json
import subprocess


def test_vault_content_audit_cli_writes_json(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "RAG_Memory_Cell_99_Test.md").write_text("# Test\\n\\nKısa", encoding="utf-8")
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
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert "Wrote" in completed.stdout
    assert data["summary"]["total_notes"] == 1
```

Add this test to `tests/test_brain_growth_vault_content_audit.py`.

- [ ] **Step 2: Run the test to verify it fails if CLI wiring is incomplete**

Run: `python3 -m pytest tests/test_brain_growth_vault_content_audit.py::test_vault_content_audit_cli_writes_json -q`

Expected: PASS if Task 2 already wired CLI correctly; if not, fix the CLI until it passes before moving on.

- [ ] **Step 3: Generate the real report and run the full verification suite**

Run:

```bash
python3 -m tools.brain_growth.vault_content_audit \
  --knowledge-dir "/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge" \
  --output "/Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/reports/vault_content_audit.json"

python3 -m pytest \
  tests/test_brain_growth_content_quality.py \
  tests/test_brain_growth_vault_content_audit.py \
  tests/test_brain_growth_validator.py -q

python3 -m tools.brain_growth.quality_validator --scope all
```

Expected:

- audit JSON written successfully
- target tests all green
- validator exits `0` or emits only accepted non-blocking warnings

- [ ] **Step 4: Commit**

```bash
git add docs/brain_growth/reports/vault_content_audit.json \
        tools/brain_growth/vault_content_audit.py \
        tests/test_brain_growth_content_quality.py \
        tests/test_brain_growth_vault_content_audit.py \
        tests/test_brain_growth_validator.py \
        tools/brain_growth/content_quality.py \
        tools/brain_growth/quality_validator.py \
        Lokum1.0/Knowledge/RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes.md \
        Lokum1.0/Knowledge/RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity.md \
        Lokum1.0/Knowledge/H3_Embedded_Interrupt_DMA_Synthesis.md \
        Lokum1.0/Knowledge/Index_Embedded_and_ESP32.md
git commit -m "feat: expand vault content and add quality audit pipeline"
```

## Spec coverage check

- Hibrit büyüme modeli: Task 4, Task 5, Task 6
- Not tipine göre section standardı: Task 1, Task 3, Task 4, Task 5, Task 6
- Embedded corpus genişletme: Task 5
- Validator kalite genişlemesi: Task 1, Task 2, Task 3, Task 7
- Index/synthesis retrieval yönlendirme güçlendirmesi: Task 6
- Ölçülebilir kalite skoru: Task 1, Task 2, Task 3, Task 7

## Placeholder scan

- `TBD`, `TODO`, `later`, `similar to` yok.
- Her test ve komut tam yol/veriyle yazıldı.
- Her içerik dalgası için somut dosya listesi verildi.

## Type consistency check

- `detect_note_kind`, `required_sections_for_kind`, `classify_note_depth`, `compute_quality_score` Task 1’de tanımlanıp Task 2-3’te aynı adlarla kullanılıyor.
- `audit_knowledge_dir` Task 2’de tanımlanıp Task 7’de aynı imzayla CLI üzerinden kullanılıyor.
- `append_content_quality_issues` Task 3’te tanımlanıp validator entegrasyonunda aynı amaçla çağrılıyor.
