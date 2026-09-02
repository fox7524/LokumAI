from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import quality_validator


RAW_STUB_TARGETS = (
    "Zero_Copy_Buffer_Analysis",
    "DRAM_Bandwidth_Utilization",
    "Data_Prefetch_Evaluation",
    "L1_Cache_Hit_Ratio",
)


def write_note(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def create_stub_targets(knowledge_dir: Path, names: tuple[str, ...] | list[str]) -> None:
    for name in names:
        write_note(knowledge_dir / f"{name}.md", f"# {name.replace('_', ' ')}\n")


def raw_note_text(*, title: str, links: list[str], include_frontmatter: bool = True, body_suffix: str = "") -> str:
    frontmatter = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        '  - "#rag/memory_cell"\n'
        '  - "#rag/training"\n'
        '  - "#hardware/apple_mlx"\n'
        "---\n\n"
        if include_frontmatter
        else ""
    )
    link_block = "\n".join(f"[[{link}]]" for link in links)
    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Teknik çekirdek\n\n"
        "Teknik açıklama.\n\n"
        "## Doğrulanmış bulgular\n\n"
        "- Bulgu 1\n"
        "- Bulgu 2\n\n"
        "## LokumAI için çıkarım\n\n"
        "Çıkarım.\n\n"
        "## Sorgu ipuçları\n\n"
        "- `ipucu`\n\n"
        "## Kaynaklar\n\n"
        "- https://example.com\n\n"
        f"{body_suffix}"
        f"{link_block}\n"
    )


def synthesis_note_text(
    *,
    title: str,
    raw_inputs: list[str],
    anchors: list[str],
    forward_links: list[str],
    include_sections: bool = True,
    body_suffix: str = "",
) -> str:
    frontmatter = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        '  - "#layer/hidden_3_logic_synthesis"\n'
        '  - "#domain/apple_silicon_mlx"\n'
        "---\n\n"
    )
    source_raw = "\n".join(f"- [[{item}]]" for item in raw_inputs)
    source_anchor = "\n".join(f"- [[{item}]]" for item in anchors)
    forward = "\n".join(f"- [[{item}]]" for item in forward_links)

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Soyutlama\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Soyutlama\n\n"
        "Soyutlama.\n\n"
        "## İnvariantlar\n\n"
        "- Kural\n\n"
        "## Retrieval yönlendirme anlamı\n\n"
        "- Yönlendirme\n\n"
        "## Besleyen düğümler\n\n"
        "### RAG_Memory_Cell_13+ girdileri\n\n"
        f"{source_raw}\n\n"
        "### Mevcut anchor düğümler\n\n"
        f"{source_anchor}\n\n"
        "## İleri besleme\n\n"
        f"{body_suffix}"
        f"{forward}\n"
    )


def h4_note_text(
    *,
    title: str,
    synthesis_inputs: list[str],
    anchors: list[str] | None = None,
    downstream_links: list[str] | None = None,
    include_sections: bool = True,
    include_hidden4_tag: bool = True,
) -> str:
    tags = ['  - "#reasoning/test"\n']
    if include_hidden4_tag:
        tags.insert(0, '  - "#layer/hidden_4_reasoning_convergence"\n')
    frontmatter = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(tags)
        + "---\n\n"
    )
    synthesis_lines = "\n".join(f"- [[{item}]]" for item in synthesis_inputs)
    anchor_lines = "\n".join(f"- [[{item}]]" for item in (anchors or [])) or "- [[Topology_Analysis]]"
    downstream_lines = "\n".join(f"- [[{item}]]" for item in (downstream_links or [])) or "- [[Strategic_Resource_Allocator]]"

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Yakınsama amacı\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Yakınsama amacı\n\n"
        "Amaç.\n\n"
        "## Tetikleyiciler\n\n"
        "- Tetikleyici\n\n"
        "## Karar sınırları\n\n"
        "- Sınır\n\n"
        "## Besleyen sentez düğümleri\n\n"
        "### Hidden_3 sentez girdileri\n\n"
        f"{synthesis_lines}\n\n"
        "### Stratejik anchor düğümler\n\n"
        f"{anchor_lines}\n\n"
        "## İleri yönlü etkiler\n\n"
        f"{downstream_lines}\n"
    )


def h5_note_text(
    *,
    title: str,
    h4_inputs: list[str],
    anchors: list[str] | None = None,
    managed_outputs: list[str] | None = None,
    include_sections: bool = True,
    include_hidden5_tag: bool = True,
) -> str:
    tags = ['  - "#control/test"\n']
    if include_hidden5_tag:
        tags.insert(0, '  - "#layer/hidden_5_metacognitive_control"\n')
    frontmatter = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(tags)
        + "---\n\n"
    )
    h4_lines = "\n".join(f"- [[{item}]]" for item in h4_inputs)
    anchor_lines = "\n".join(f"- [[{item}]]" for item in (anchors or [])) or "- [[Metacognitive_Reflection_Core]]"
    output_lines = "\n".join(f"- [[{item}]]" for item in (managed_outputs or [])) or "- [[Strategic_Resource_Allocator]]"

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Kontrol amacı\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Kontrol amacı\n\n"
        "Amaç.\n\n"
        "## Arbitration sinyalleri\n\n"
        "- Sinyal\n\n"
        "## Karar politikası\n\n"
        "- Politika\n\n"
        "## Besleyen H4 düğümleri\n\n"
        "### Hidden_4 arbitration girdileri\n\n"
        f"{h4_lines}\n\n"
        "### Metacognitive control anchor düğümleri\n\n"
        f"{anchor_lines}\n\n"
        "## Yönettiği çıktı yolları\n\n"
        f"{output_lines}\n"
    )


def h6_note_text(
    *,
    title: str,
    h5_inputs: list[str],
    anchors: list[str] | None = None,
    coordinated_outputs: list[str] | None = None,
    include_sections: bool = True,
    include_hidden6_tag: bool = True,
) -> str:
    tags = ['  - "#executive/test"\n']
    if include_hidden6_tag:
        tags.insert(0, '  - "#layer/hidden_6_executive_orchestration"\n')
    frontmatter = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(tags)
        + "---\n\n"
    )
    h5_lines = "\n".join(f"- [[{item}]]" for item in h5_inputs)
    anchor_lines = "\n".join(f"- [[{item}]]" for item in (anchors or [])) or "- [[Executive_Action_Formatter]]"
    output_lines = (
        "\n".join(f"- [[{item}]]" for item in (coordinated_outputs or [])) or "- [[Final_Execution_Gate]]"
    )

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Orkestrasyon amacı\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Orkestrasyon amacı\n\n"
        "Amaç.\n\n"
        "## Yürütücü sinyaller\n\n"
        "- Sinyal\n\n"
        "## Orkestrasyon politikası\n\n"
        "- Politika\n\n"
        "## Besleyen H5 düğümleri\n\n"
        "### Hidden_5 executive girdileri\n\n"
        f"{h5_lines}\n\n"
        "### Executive orchestration anchor düğümleri\n\n"
        f"{anchor_lines}\n\n"
        "## Koordine ettiği çıktı yolları\n\n"
        f"{output_lines}\n"
    )


def h7_note_text(
    *,
    title: str,
    episode_mode: str = "ordered_episode_reconstruction",
    temporal_relations: list[str] | None = None,
    primary_entities: list[str] | None = None,
    primary_events: list[str] | None = None,
    h6_inputs: list[str] | None = None,
    memory_outputs: list[str] | None = None,
    include_sections: bool = True,
    include_hidden7_tag: bool = True,
    entity_binding_text: str = "- Entity ve event bağları korunur.",
) -> str:
    tags = ['  - "#memory/test"\n']
    if include_hidden7_tag:
        tags.insert(0, '  - "#layer/hidden_7_episodic_temporal_memory"\n')
    frontmatter = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(tags)
        + f'episode_mode: "{episode_mode}"\n'
        + "temporal_relations:\n"
        + "".join(f'  - "{item}"\n' for item in (temporal_relations or []))
        + "primary_entities:\n"
        + "".join(f'  - "{item}"\n' for item in (primary_entities or []))
        + "primary_events:\n"
        + "".join(f'  - "{item}"\n' for item in (primary_events or []))
        + "---\n\n"
    )
    h6_lines = "\n".join(f"- [[{item}]]" for item in (h6_inputs or []))
    output_lines = "\n".join(f"- [[{item}]]" for item in (memory_outputs or []))

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Episodik amaç\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Episodik amaç\n\n"
        "Amaç.\n\n"
        "## Zamansal sinyaller\n\n"
        "- Sinyal.\n\n"
        "## Temporal edge politikası\n\n"
        "- before ilişkisi korunur.\n\n"
        "## Entity-event bağlama stratejisi\n\n"
        f"{entity_binding_text}\n\n"
        "## Besleyen H6 düğümleri\n\n"
        f"{h6_lines}\n\n"
        "## Hafıza çıktıları\n\n"
        f"{output_lines}\n"
    )


def h8_note_text(
    *,
    title: str,
    workspace_mode: str = "dominant_policy_broadcast",
    dominant_thoughtseed: str = "recovery_first_consensus",
    candidate_policies: list[str] | None = None,
    broadcast_targets: list[str] | None = None,
    h7_inputs: list[str] | None = None,
    downstream_outputs: list[str] | None = None,
    include_sections: bool = True,
    include_hidden8_tag: bool = True,
    broadcast_strategy_text: str = "- Policy önce consensus yüzeyine yayınlanır.",
    commitment_rules_text: str = "- Commit yalnız güçlü episodik destekle yapılır.",
) -> str:
    tags = ['  - "#workspace/test"\n']
    if include_hidden8_tag:
        tags.insert(0, '  - "#layer/hidden_8_decision_assembly"\n')
    frontmatter = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(tags)
        + f'workspace_mode: "{workspace_mode}"\n'
        + f'dominant_thoughtseed: "{dominant_thoughtseed}"\n'
        + "candidate_policies:\n"
        + "".join(f'  - "{item}"\n' for item in (candidate_policies or []))
        + "broadcast_targets:\n"
        + "".join(f'  - "{item}"\n' for item in (broadcast_targets or []))
        + "---\n\n"
    )
    h7_lines = "\n".join(f"- [[{item}]]" for item in (h7_inputs or []))
    output_lines = "\n".join(f"- [[{item}]]" for item in (downstream_outputs or []))

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Karar montaj amacı\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Karar montaj amacı\n\n"
        "Amaç.\n\n"
        "## Dominant thoughtseed sinyalleri\n\n"
        "- Sinyal.\n\n"
        "## Policy broadcast stratejisi\n\n"
        f"{broadcast_strategy_text}\n\n"
        "## Commitment kuralları\n\n"
        f"{commitment_rules_text}\n\n"
        "## Besleyen H7 düğümleri\n\n"
        f"{h7_lines}\n\n"
        "## Yayınlanan çıktı yolları\n\n"
        f"{output_lines}\n"
    )


def h9_note_text(
    *,
    title: str,
    package_mode: str = "surface_bound_policy_delivery",
    source_policy: str = "dominant_policy_surface_binding",
    delivery_surfaces: list[str] | None = None,
    package_contracts: list[str] | None = None,
    h8_inputs: list[str] | None = None,
    packaged_outputs: list[str] | None = None,
    include_sections: bool = True,
    include_hidden9_tag: bool = True,
    source_policy_mapping_text: str = "- Policy kaynak eşlemesi korunur.",
    delivery_contract_text: str = "- Delivery surface sözleşmesi korunur.",
    readiness_rules_text: str = "- Paket yalnız readiness koşulları doğrulanınca yayınlanır.",
) -> str:
    tags = ['  - "#execution/test"\n']
    if include_hidden9_tag:
        tags.insert(0, '  - "#layer/hidden_9_execution_packaging"\n')
    frontmatter = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(tags)
        + f'package_mode: "{package_mode}"\n'
        + f'source_policy: "{source_policy}"\n'
        + "delivery_surfaces:\n"
        + "".join(f'  - "{item}"\n' for item in (delivery_surfaces or []))
        + "package_contracts:\n"
        + "".join(f'  - "{item}"\n' for item in (package_contracts or []))
        + "---\n\n"
    )
    h8_lines = "\n".join(f"- [[{item}]]" for item in (h8_inputs or []))
    output_lines = "\n".join(f"- [[{item}]]" for item in (packaged_outputs or []))

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Paketleme amacı\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Paketleme amacı\n\n"
        "Amaç.\n\n"
        "## Source policy eşlemesi\n\n"
        f"{source_policy_mapping_text}\n\n"
        "## Delivery surface sözleşmeleri\n\n"
        f"{delivery_contract_text}\n\n"
        "## Readiness ve commit koşulları\n\n"
        f"{readiness_rules_text}\n\n"
        "## Besleyen H8 düğümleri\n\n"
        f"{h8_lines}\n\n"
        "## Paketlenen çıktı yolları\n\n"
        f"{output_lines}\n"
    )


def h10_note_text(
    *,
    title: str,
    supervision_mode: str = "global_supervision_arbitration",
    governing_signal: str = "surface_alignment_supervision",
    oversight_surfaces: list[str] | None = None,
    supervision_contracts: list[str] | None = None,
    h9_inputs: list[str] | None = None,
    supervised_outputs: list[str] | None = None,
    include_sections: bool = True,
    include_hidden10_tag: bool = True,
    governing_signal_mapping_text: str = "- Governing signal stratejik yüzeylere eşlenir.",
    oversight_contract_text: str = "- Oversight surface sözleşmesi korunur.",
    escalation_rules_text: str = "- Paket yalnız escalation kuralları sağlanınca açılır.",
) -> str:
    tags = ['  - "#strategy/test"\n']
    if include_hidden10_tag:
        tags.insert(0, '  - "#layer/hidden_10_strategic_supervision"\n')
    frontmatter = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(tags)
        + f'supervision_mode: "{supervision_mode}"\n'
        + f'governing_signal: "{governing_signal}"\n'
        + "oversight_surfaces:\n"
        + "".join(f'  - "{item}"\n' for item in (oversight_surfaces or []))
        + "supervision_contracts:\n"
        + "".join(f'  - "{item}"\n' for item in (supervision_contracts or []))
        + "---\n\n"
    )
    h9_lines = "\n".join(f"- [[{item}]]" for item in (h9_inputs or []))
    output_lines = "\n".join(f"- [[{item}]]" for item in (supervised_outputs or []))

    if not include_sections:
        return frontmatter + f"# {title}\n\n## Stratejik denetim amacı\n\nEksik yapı.\n"

    return (
        f"{frontmatter}"
        f"# {title}\n\n"
        "## Stratejik denetim amacı\n\n"
        "Amaç.\n\n"
        "## Governing signal eşlemesi\n\n"
        f"{governing_signal_mapping_text}\n\n"
        "## Oversight surface sözleşmeleri\n\n"
        f"{oversight_contract_text}\n\n"
        "## Escalation ve rollback kuralları\n\n"
        f"{escalation_rules_text}\n\n"
        "## Besleyen H9 düğümleri\n\n"
        f"{h9_lines}\n\n"
        "## Denetlenen çıktı yolları\n\n"
        f"{output_lines}\n"
    )


def issue_codes(report: quality_validator.FileReport) -> set[str]:
    return {issue.code for issue in report.issues}


def test_validate_raw_note_flags_missing_frontmatter_and_sections(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(knowledge_dir, RAW_STUB_TARGETS)
    path = write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test_Note.md",
        "# Test Note\n\n## Teknik çekirdek\n\nEksik frontmatter ve eksik bölümler.\n",
    )

    report = quality_validator.validate_raw_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {"missing_frontmatter", "missing_section"} <= issue_codes(report)


def test_validate_raw_note_rejects_forbidden_dictionary_link(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(knowledge_dir, RAW_STUB_TARGETS)
    path = write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test_Note.md",
        raw_note_text(
            title="Test Note",
            links=[*RAW_STUB_TARGETS[:3], "LokumAI-1.0"],
        ),
    )

    report = quality_validator.validate_raw_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert "forbidden_node_reference" in issue_codes(report)


def test_validate_raw_note_rejects_invalid_target_layer_and_low_link_count(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(knowledge_dir, RAW_STUB_TARGETS[:2])
    path = write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test_Note.md",
        raw_note_text(
            title="Test Note",
            links=["Zero_Copy_Buffer_Analysis", "DRAM_Bandwidth_Utilization", "Unknown_Node"],
        ),
    )

    report = quality_validator.validate_raw_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {"invalid_target_layer", "insufficient_forward_links"} <= issue_codes(report)


def test_validate_raw_note_reports_thin_content_and_missing_sources(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(knowledge_dir, RAW_STUB_TARGETS)
    path = write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test_Note.md",
        (
            "---\n"
            "date: 2026-08-30\n"
            "tags:\n"
            '  - "#rag/memory_cell"\n'
            '  - "#rag/training"\n'
            "---\n\n"
            "# Test Note\n\n"
            "## Teknik çekirdek\n\n"
            "Kısa not.\n\n"
            "## Kaynaklar\n\n"
            "- Kaynak eklenecek.\n\n"
            "[[Zero_Copy_Buffer_Analysis]]\n"
            "[[DRAM_Bandwidth_Utilization]]\n"
            "[[Data_Prefetch_Evaluation]]\n"
            "[[L1_Cache_Hit_Ratio]]\n"
        ),
    )

    report = quality_validator.validate_raw_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {"thin_note", "missing_sources"} <= issue_codes(report)
    assert report.metrics["note_depth"] == "thin"
    assert report.metrics["content_quality"]["source_grounding_score"] == 0.0


def test_embedded_cluster_notes_reach_medium_or_better() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    for name in (
        "RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md",
        "RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md",
        "RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md",
    ):
        path = knowledge_dir / name
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("raw") if section not in text
        ]
        assert missing_sections == []
        report = quality_validator.validate_raw_note(path, knowledge_dir=knowledge_dir)
        depth = report.metrics.get("depth_class", report.metrics.get("note_depth"))
        assert depth in {"medium", "strong"}
        assert "thin_note" not in {issue.code for issue in report.issues}


def test_new_embedded_corpus_files_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    for name in (
        "RAG_Memory_Cell_65_ESP32_S3_Vector_Unit_Alignment_And_DMA_Tension.md",
        "RAG_Memory_Cell_66_ESP8266_Nodemcu_Wifi_Timing_And_Watchdog_Pressure.md",
        "RAG_Memory_Cell_67_STM32_DMA_Cache_Coherency_And_ISR_Boundaries.md",
        "RAG_Memory_Cell_68_RP2040_PIO_State_Machine_Timing_Debug.md",
        "RAG_Memory_Cell_69_nRF52_Softdevice_Interrupt_Priority_Constraints.md",
        "RAG_Memory_Cell_70_Zephyr_Devicetree_Driver_Bringup_Failure_Modes.md",
        "RAG_Memory_Cell_71_Platformio_Build_Graph_Drift_And_Flag_Parity.md",
    ):
        path = knowledge_dir / name
        assert path.exists(), f"Eksik embedded corpus dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("raw") if section not in text
        ]
        assert missing_sections == []
        report = quality_validator.validate_raw_note(path, knowledge_dir=knowledge_dir)
        depth = report.metrics.get("depth_class", report.metrics.get("note_depth"))
        assert depth in {"medium", "strong"}
        issue_set = {issue.code for issue in report.issues}
        # Mevcut slug normalizer mixed-case gövdeleri (NodeMCU, SoftDevice, DeviceTree,
        # PlatformIO) birebir korumuyor. Kullanıcı tarafından talep edilen legacy dosya
        # adlarını sabit tutup, içerik ve graph bütünlüğünü temiz doğruluyoruz.
        assert issue_set <= {"filename_mismatch"}, report


def test_embedded_synthesis_and_index_have_no_thin_content() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        (
            knowledge_dir / "H3_Embedded_Interrupt_DMA_Synthesis.md",
            "synthesis",
            lambda path: quality_validator.validate_synthesis_note(path, knowledge_dir=knowledge_dir),
        ),
        (
            knowledge_dir / "Index_Embedded_and_ESP32.md",
            "index",
            lambda path: quality_validator.validate_index_note(path),
        ),
    )

    for path, kind, validate in targets:
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind(kind) if section not in text
        ]
        assert missing_sections == []

        quality_metrics = quality_validator.content_quality_metrics(
            kind,
            text,
            outbound_links=len(quality_validator.parse_wikilinks(text)),
        )
        depth = quality_metrics["note_depth"]
        assert depth in {"medium", "strong"}

        report = validate(path)
        assert report.ok is True, report
        assert "thin_note" not in issue_codes(report)


def test_remaining_h3_synthesis_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        (
            "H3_Apple_Silicon_Memory_Execution_Synthesis.md",
            8,
            2,
            3,
        ),
        (
            "H3_Cognitive_Graph_RAG_Routing_Synthesis.md",
            8,
            2,
            3,
        ),
        (
            "H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis.md",
            8,
            2,
            3,
        ),
    )

    for name, expected_raw_inputs, expected_anchor_inputs, expected_forward_links in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H3 synthesis dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("synthesis") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_synthesis_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["raw_inputs"] == expected_raw_inputs
        assert report.metrics["anchor_inputs"] == expected_anchor_inputs
        assert report.metrics["forward_links"] == expected_forward_links
        assert "synthesis_spec_violation" not in issue_codes(report)


def test_validate_filename_mismatch_for_raw_and_synthesis_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            *RAW_STUB_TARGETS,
            "Semantic_Graph_Weaver",
            "RAG_Memory_Cell_13_Test_Note",
            "RAG_Memory_Cell_14_Test_Note",
            "RAG_Memory_Cell_15_Test_Note",
            "RAG_Memory_Cell_16_Test_Note",
            "RAG_Memory_Cell_17_Test_Note",
            "RAG_Memory_Cell_18_Test_Note",
            "RAG_Memory_Cell_19_Test_Note",
            "RAG_Memory_Cell_20_Test_Note",
        ],
    )

    raw_path = write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test_Note.md",
        raw_note_text(title="Different Raw Title", links=list(RAW_STUB_TARGETS)),
    )
    synthesis_path = write_note(
        knowledge_dir / "H3_Expected_Synthesis_Title.md",
        synthesis_note_text(
            title="Different Synthesis Title",
            raw_inputs=[f"RAG_Memory_Cell_{index:02d}_Test_Note" for index in range(13, 21)],
            anchors=list(RAW_STUB_TARGETS[:2]),
            forward_links=["Semantic_Graph_Weaver"],
        ),
    )

    raw_report = quality_validator.validate_raw_note(raw_path, knowledge_dir=knowledge_dir)
    synthesis_report = quality_validator.validate_synthesis_note(synthesis_path, knowledge_dir=knowledge_dir)

    assert "filename_mismatch" in issue_codes(raw_report)
    assert "filename_mismatch" in issue_codes(synthesis_report)


def test_validate_synthesis_note_flags_missing_sections_and_forward_links(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(knowledge_dir, RAW_STUB_TARGETS)
    path = write_note(
        knowledge_dir / "H3_Bad_Synthesis.md",
        synthesis_note_text(
            title="Bad Synthesis",
            raw_inputs=[],
            anchors=[],
            forward_links=[],
            include_sections=False,
        ),
    )

    report = quality_validator.validate_synthesis_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {"missing_section", "insufficient_forward_links"} <= issue_codes(report)


def test_write_report_output_persists_json_and_text(tmp_path: Path) -> None:
    report = {
        "generated_at": "2026-08-30T00:00:00+00:00",
        "scope": "all",
        "knowledge_dir": "/tmp/Knowledge",
        "summary": {
            "files_scanned": 2,
            "files_with_issues": 1,
            "issue_count": 1,
            "status": "fail",
        },
        "kinds": {
            "raw": {"kind": "raw", "file_count": 1, "ok_count": 0, "issue_count": 1},
            "synthesis": {"kind": "synthesis", "file_count": 1, "ok_count": 1, "issue_count": 0},
            "index": {"kind": "index", "file_count": 0, "ok_count": 0, "issue_count": 0},
        },
        "files": [
            {
                "path": "/tmp/Knowledge/RAG_Memory_Cell_13_Test.md",
                "kind": "raw",
                "title": "Test",
                "ok": False,
                "issues": [{"code": "missing_frontmatter", "message": "frontmatter eksik"}],
                "metrics": {"index": 13, "wikilink_count": 3},
            }
        ],
    }

    json_path = tmp_path / "reports" / "validator.json"
    text_path = tmp_path / "reports" / "validator.txt"

    quality_validator.write_report_output(report, "json", json_path)
    quality_validator.write_report_output(report, "text", text_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["summary"]["status"] == "fail"
    text_content = text_path.read_text(encoding="utf-8")
    assert "Brain Growth Quality Report" in text_content
    assert "[missing_frontmatter]" in text_content


def test_validate_h4_note_accepts_hidden4_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H3_Test",
            "Topology_Analysis",
            "Strategic_Resource_Allocator",
        ],
    )
    path = write_note(
        knowledge_dir / "H4_Test_Reasoning.md",
        h4_note_text(
            title="Test Reasoning",
            synthesis_inputs=["H3_Test"],
            anchors=["Topology_Analysis"],
            downstream_links=["Strategic_Resource_Allocator"],
        ),
    )

    report = quality_validator.validate_h4_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h4"
    assert report.metrics["h3_inputs"] == 1


def test_h4_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H4_Cognitive_Retrieval_Policy_Selection.md",
        "H4_Cross_Domain_Causal_Alignment.md",
        "H4_Edge_Device_Response_Strategy.md",
        "H4_Performance_Bottleneck_Disambiguation.md",
        "H4_Resource_Execution_Prioritization.md",
        "H4_Security_Failure_Mode_Arbitration.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H4 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h4") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h4_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h3_inputs"] >= 1
        assert report.metrics["forward_links"] >= 1
        assert "missing_h3_input" not in issue_codes(report)


def test_h5_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H5_Global_Escalation_Gate.md",
        "H5_Metacognitive_Policy_Arbitration.md",
        "H5_Retrieval_Depth_Governance.md",
        "H5_Risk_Performance_Tradeoff_Control.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H5 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h5") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h5_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h4_inputs"] >= 1
        assert report.metrics["managed_outputs"] >= 1
        assert "missing_h4_input" not in issue_codes(report)
        assert "h5_spec_violation" not in issue_codes(report)


def test_validate_h5_note_accepts_hidden5_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H4_Test_Reasoning",
            "Metacognitive_Reflection_Core",
            "Strategic_Resource_Allocator",
        ],
    )
    path = write_note(
        knowledge_dir / "H5_Test_Control.md",
        h5_note_text(
            title="Test Control",
            h4_inputs=["H4_Test_Reasoning"],
            anchors=["Metacognitive_Reflection_Core"],
            managed_outputs=["Strategic_Resource_Allocator"],
        ),
    )

    report = quality_validator.validate_h5_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h5"
    assert report.metrics["h4_inputs"] == 1
    assert report.metrics["managed_outputs"] == 1


def test_validate_h6_note_accepts_hidden6_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H5_Metacognitive_Policy_Arbitration",
            "H5_Risk_Performance_Tradeoff_Control",
            "Executive_Action_Formatter",
            "Final_Execution_Gate",
        ],
    )
    path = write_note(
        knowledge_dir / "H6_Test_Executive.md",
        h6_note_text(
            title="Test Executive",
            h5_inputs=[
                "H5_Metacognitive_Policy_Arbitration",
                "H5_Risk_Performance_Tradeoff_Control",
            ],
            anchors=["Executive_Action_Formatter"],
            coordinated_outputs=["Final_Execution_Gate"],
        ),
    )

    report = quality_validator.validate_h6_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h6"
    assert report.metrics["h5_inputs"] == 2
    assert report.metrics["coordinated_outputs"] == 1


def test_h6_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H6_Executive_Priority_Orchestration.md",
        "H6_Global_Response_Orchestration.md",
        "H6_Recovery_Execution_Sequencing.md",
        "H6_Retrieval_Action_Coordination.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H6 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h6") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h6_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h5_inputs"] >= 2
        assert report.metrics["coordinated_outputs"] >= 1
        assert "missing_h5_input" not in issue_codes(report)
        assert "h6_spec_violation" not in issue_codes(report)


def test_validate_h7_note_accepts_hidden7_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H6_Executive_Priority_Orchestration",
            "H6_Retrieval_Action_Coordination",
            "Episodic_Memory_Consolidation",
            "Semantic_Graph_Weaver",
        ],
    )
    path = write_note(
        knowledge_dir / "H7_Test_Episodic.md",
        h7_note_text(
            title="Test Episodic",
            temporal_relations=["before", "after"],
            primary_entities=["executive_queue", "retrieval_budget"],
            primary_events=["priority_shift", "execution_release"],
            h6_inputs=[
                "H6_Executive_Priority_Orchestration",
                "H6_Retrieval_Action_Coordination",
            ],
            memory_outputs=[
                "Episodic_Memory_Consolidation",
                "Semantic_Graph_Weaver",
            ],
        ),
    )

    report = quality_validator.validate_h7_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h7"
    assert report.metrics["h6_inputs"] == 2
    assert report.metrics["temporal_relation_count"] == 2
    assert report.metrics["entity_count"] == 2
    assert report.metrics["event_count"] == 2


def test_validate_h7_note_flags_temporal_binding_and_frontmatter_issues(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Episodic_Memory_Consolidation",
        ],
    )
    path = write_note(
        knowledge_dir / "H7_Broken_Episodic.md",
        h7_note_text(
            title="Broken Episodic",
            episode_mode="invalid_mode",
            temporal_relations=[],
            primary_entities=[],
            primary_events=[],
            h6_inputs=[],
            memory_outputs=["Episodic_Memory_Consolidation"],
            entity_binding_text="",
            include_hidden7_tag=False,
        ),
    )

    report = quality_validator.validate_h7_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {
        "missing_tag",
        "invalid_episode_mode",
        "missing_temporal_relation",
        "missing_entity_event_binding",
        "missing_h6_input",
        "missing_primary_entities",
        "missing_primary_events",
    } <= issue_codes(report)


def test_h7_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H7_Episodic_Timeline_Alignment.md",
        "H7_Event_Entity_Binding.md",
        "H7_Recency_Drift_Governance.md",
        "H7_Temporal_Causal_Recall.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H7 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h7") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h7_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h6_inputs"] >= 1
        assert report.metrics["memory_outputs"] >= 1
        assert "missing_h6_input" not in issue_codes(report)
        assert "h7_spec_violation" not in issue_codes(report)


def test_validate_h8_note_accepts_hidden8_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H7_Episodic_Timeline_Alignment",
            "H7_Recency_Drift_Governance",
            "Executive_Action_Formatter",
            "Final_Execution_Gate",
            "Global_State_Consensus",
            "Episodic_Memory_Consolidation",
        ],
    )
    path = write_note(
        knowledge_dir / "H8_Test_Decision.md",
        h8_note_text(
            title="Test Decision",
            candidate_policies=["stabilize_consensus_before_execution", "minimize_regret_under_risk"],
            broadcast_targets=["Executive_Action_Formatter", "Final_Execution_Gate"],
            h7_inputs=["H7_Episodic_Timeline_Alignment", "H7_Recency_Drift_Governance"],
            downstream_outputs=["Global_State_Consensus", "Episodic_Memory_Consolidation"],
        ),
    )

    report = quality_validator.validate_h8_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h8"
    assert report.metrics["h7_inputs"] == 2
    assert report.metrics["candidate_policy_count"] == 2
    assert report.metrics["broadcast_target_count"] == 2
    assert report.metrics["downstream_output_count"] == 2


def test_validate_h8_note_flags_workspace_binding_and_frontmatter_issues(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Global_State_Consensus",
        ],
    )
    path = write_note(
        knowledge_dir / "H8_Broken_Decision.md",
        h8_note_text(
            title="Broken Decision",
            workspace_mode="invalid_mode",
            dominant_thoughtseed="",
            candidate_policies=[],
            broadcast_targets=[],
            h7_inputs=[],
            downstream_outputs=["Global_State_Consensus"],
            broadcast_strategy_text="",
            commitment_rules_text="",
            include_hidden8_tag=False,
        ),
    )

    report = quality_validator.validate_h8_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {
        "missing_tag",
        "invalid_workspace_mode",
        "missing_dominant_thoughtseed",
        "missing_candidate_policy",
        "missing_broadcast_target",
        "missing_h7_input",
        "missing_policy_broadcast_strategy",
        "missing_commitment_rule",
    } <= issue_codes(report)


def test_h8_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H8_Decision_Commitment_Gate.md",
        "H8_Dominant_Thoughtseed_Selection.md",
        "H8_Exception_Override_Arbitration.md",
        "H8_Global_Policy_Broadcast.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H8 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h8") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h8_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h7_inputs"] >= 1
        assert report.metrics["broadcast_target_count"] >= 1
        assert report.metrics["downstream_output_count"] >= 1
        assert "missing_h7_input" not in issue_codes(report)
        assert "h8_spec_violation" not in issue_codes(report)


def test_validate_h9_note_accepts_hidden9_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H8_Dominant_Thoughtseed_Selection",
            "Executive_Action_Formatter",
            "Final_Execution_Gate",
        ],
    )
    path = write_note(
        knowledge_dir / "H9_Test_Package.md",
        h9_note_text(
            title="Test Package",
            delivery_surfaces=["Executive_Action_Formatter", "Final_Execution_Gate"],
            package_contracts=["surface_route_manifest", "policy_binding_envelope"],
            h8_inputs=["H8_Dominant_Thoughtseed_Selection"],
            packaged_outputs=["Executive_Action_Formatter", "Final_Execution_Gate"],
        ),
    )

    report = quality_validator.validate_h9_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h9"
    assert report.metrics["h8_inputs"] == 1
    assert report.metrics["delivery_surface_count"] == 2
    assert report.metrics["package_contract_count"] == 2
    assert report.metrics["packaged_output_count"] == 2


def test_validate_h9_note_flags_package_contract_and_frontmatter_issues(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Executive_Action_Formatter",
        ],
    )
    path = write_note(
        knowledge_dir / "H9_Broken_Package.md",
        h9_note_text(
            title="Broken Package",
            package_mode="invalid_mode",
            source_policy="",
            delivery_surfaces=[],
            package_contracts=[],
            h8_inputs=[],
            packaged_outputs=["Executive_Action_Formatter"],
            source_policy_mapping_text="",
            delivery_contract_text="",
            readiness_rules_text="",
            include_hidden9_tag=False,
        ),
    )

    report = quality_validator.validate_h9_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {
        "missing_tag",
        "invalid_package_mode",
        "missing_source_policy",
        "missing_delivery_surface",
        "missing_package_contract",
        "missing_h8_input",
        "missing_source_policy_mapping",
        "missing_delivery_surface_contract",
        "missing_readiness_rule",
    } <= issue_codes(report)


def test_h9_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H9_Commit_Ready_Delivery_Check.md",
        "H9_Execution_Surface_Binding.md",
        "H9_Failsafe_Action_Packaging.md",
        "H9_Response_Payload_Composition.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H9 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h9") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h9_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h8_inputs"] >= 1
        assert report.metrics["delivery_surface_count"] >= 1
        assert report.metrics["package_contract_count"] >= 1
        assert report.metrics["packaged_output_count"] >= 1
        assert "missing_h8_input" not in issue_codes(report)
        assert "h9_spec_violation" not in issue_codes(report)


def test_validate_h10_note_accepts_hidden10_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H9_Execution_Surface_Binding",
            "Global_State_Consensus",
            "Long_Term_Strategic_Planner",
        ],
    )
    path = write_note(
        knowledge_dir / "H10_Test_Supervision.md",
        h10_note_text(
            title="Test Supervision",
            oversight_surfaces=["Global_State_Consensus", "Long_Term_Strategic_Planner"],
            supervision_contracts=["supervision_route_manifest", "strategic_alignment_contract"],
            h9_inputs=["H9_Execution_Surface_Binding"],
            supervised_outputs=["Global_State_Consensus", "Long_Term_Strategic_Planner"],
        ),
    )

    report = quality_validator.validate_h10_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h10"
    assert report.metrics["h9_inputs"] == 1
    assert report.metrics["oversight_surface_count"] == 2
    assert report.metrics["supervision_contract_count"] == 2
    assert report.metrics["supervised_output_count"] == 2


def test_validate_h10_note_flags_supervision_contract_and_frontmatter_issues(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Global_State_Consensus",
        ],
    )
    path = write_note(
        knowledge_dir / "H10_Broken_Supervision.md",
        h10_note_text(
            title="Broken Supervision",
            supervision_mode="invalid_mode",
            governing_signal="",
            oversight_surfaces=[],
            supervision_contracts=[],
            h9_inputs=[],
            supervised_outputs=["Global_State_Consensus"],
            governing_signal_mapping_text="",
            oversight_contract_text="",
            escalation_rules_text="",
            include_hidden10_tag=False,
        ),
    )

    report = quality_validator.validate_h10_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is False
    assert {
        "missing_tag",
        "invalid_supervision_mode",
        "missing_governing_signal",
        "missing_oversight_surface",
        "missing_supervision_contract",
        "missing_h9_input",
        "missing_governing_signal_mapping",
        "missing_oversight_surface_contract",
        "missing_escalation_rule",
    } <= issue_codes(report)


def test_h10_layer_notes_validate_cleanly() -> None:
    knowledge_dir = Path("/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge")
    targets = (
        "H10_Global_Supervision_Arbitration.md",
        "H10_Long_Horizon_Outcome_Review.md",
        "H10_Rollback_Escalation_Governance.md",
        "H10_Strategic_Resource_Oversight.md",
    )

    for name in targets:
        path = knowledge_dir / name
        assert path.exists(), f"Eksik H10 note dosyası: {path.name}"
        text = path.read_text(encoding="utf-8")
        missing_sections = [
            section for section in quality_validator.required_sections_for_kind("h10") if section not in text
        ]
        assert missing_sections == []

        report = quality_validator.validate_h10_note(path, knowledge_dir=knowledge_dir)
        assert report.ok is True, report
        assert report.metrics["h9_inputs"] >= 1
        assert report.metrics["oversight_surface_count"] >= 1
        assert report.metrics["supervision_contract_count"] >= 1
        assert report.metrics["supervised_output_count"] >= 1
        assert "missing_h9_input" not in issue_codes(report)
        assert "h10_spec_violation" not in issue_codes(report)


def test_build_report_contains_h6_counts_and_remediation_map(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H5_Metacognitive_Policy_Arbitration",
            "Executive_Action_Formatter",
            "Final_Execution_Gate",
        ],
    )
    write_note(
        knowledge_dir / "H6_Broken_Executive.md",
        h6_note_text(
            title="Broken Executive",
            h5_inputs=["H5_Metacognitive_Policy_Arbitration"],
            anchors=["Executive_Action_Formatter"],
            coordinated_outputs=["Final_Execution_Gate"],
            include_sections=False,
            include_hidden6_tag=False,
        ),
    )

    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert report["kinds"]["h6"]["file_count"] == 1
    assert report["graph_metrics"]["node_count_by_kind"]["h6"] == 1
    assert report["summary"]["status"] == "fail"
    remediation_map = report["remediation_map"]
    assert remediation_map["issue_code_count"] >= 2
    remediation_entries = {entry["issue_code"]: entry for entry in remediation_map["entries"]}
    assert remediation_entries["missing_section"]["repair_class"] == "section_structure_repair"
    assert remediation_entries["missing_tag"]["repair_class"] == "frontmatter_taxonomy_repair"
    text_report = quality_validator.render_text_report(report)
    assert "Remediation hints:" in text_report
    assert "missing_section" in text_report


def test_build_report_contains_h7_counts_and_temporal_remediation_map(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Episodic_Memory_Consolidation",
        ],
    )
    write_note(
        knowledge_dir / "H7_Broken_Episodic.md",
        h7_note_text(
            title="Broken Episodic",
            episode_mode="invalid_mode",
            temporal_relations=[],
            primary_entities=[],
            primary_events=[],
            h6_inputs=[],
            memory_outputs=["Episodic_Memory_Consolidation"],
            entity_binding_text="",
            include_hidden7_tag=False,
        ),
    )

    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert report["kinds"]["h7"]["file_count"] == 1
    assert report["graph_metrics"]["node_count_by_kind"]["h7"] == 1
    remediation_entries = {entry["issue_code"]: entry for entry in report["remediation_map"]["entries"]}
    assert remediation_entries["missing_temporal_relation"]["repair_class"] == "temporal_edge_schema_repair"
    assert remediation_entries["missing_entity_event_binding"]["repair_class"] == "entity_event_binding_repair"
    assert remediation_entries["invalid_episode_mode"]["repair_class"] == "episodic_frontmatter_repair"
    assert remediation_entries["missing_primary_entities"]["repair_class"] == "episodic_frontmatter_repair"
    assert remediation_entries["missing_primary_events"]["repair_class"] == "episodic_frontmatter_repair"
    assert remediation_entries["missing_h6_input"]["repair_class"] == "graph_input_coverage_repair"
    text_report = quality_validator.render_text_report(report)
    assert "- h7: files=1" in text_report
    assert "missing_temporal_relation" in text_report


def test_build_report_contains_h8_counts_and_workspace_remediation_map(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Global_State_Consensus",
        ],
    )
    write_note(
        knowledge_dir / "H8_Broken_Decision.md",
        h8_note_text(
            title="Broken Decision",
            workspace_mode="invalid_mode",
            dominant_thoughtseed="",
            candidate_policies=[],
            broadcast_targets=[],
            h7_inputs=[],
            downstream_outputs=["Global_State_Consensus"],
            broadcast_strategy_text="",
            commitment_rules_text="",
            include_hidden8_tag=False,
        ),
    )

    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert report["kinds"]["h8"]["file_count"] == 1
    assert report["graph_metrics"]["node_count_by_kind"]["h8"] == 1
    remediation_entries = {entry["issue_code"]: entry for entry in report["remediation_map"]["entries"]}
    assert remediation_entries["invalid_workspace_mode"]["repair_class"] == "workspace_frontmatter_repair"
    assert remediation_entries["missing_dominant_thoughtseed"]["repair_class"] == "workspace_frontmatter_repair"
    assert remediation_entries["missing_candidate_policy"]["repair_class"] == "policy_broadcast_repair"
    assert remediation_entries["missing_broadcast_target"]["repair_class"] == "policy_broadcast_repair"
    assert remediation_entries["missing_h7_input"]["repair_class"] == "graph_input_coverage_repair"
    assert remediation_entries["missing_policy_broadcast_strategy"]["repair_class"] == "policy_broadcast_repair"
    assert remediation_entries["missing_commitment_rule"]["repair_class"] == "decision_commitment_repair"
    text_report = quality_validator.render_text_report(report)
    assert "- h8: files=1" in text_report
    assert "missing_dominant_thoughtseed" in text_report


def test_build_report_contains_h9_counts_and_packaging_remediation_map(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Executive_Action_Formatter",
        ],
    )
    write_note(
        knowledge_dir / "H9_Broken_Package.md",
        h9_note_text(
            title="Broken Package",
            package_mode="invalid_mode",
            source_policy="",
            delivery_surfaces=[],
            package_contracts=[],
            h8_inputs=[],
            packaged_outputs=["Executive_Action_Formatter"],
            source_policy_mapping_text="",
            delivery_contract_text="",
            readiness_rules_text="",
            include_hidden9_tag=False,
        ),
    )

    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert report["kinds"]["h9"]["file_count"] == 1
    assert report["graph_metrics"]["node_count_by_kind"]["h9"] == 1
    remediation_entries = {entry["issue_code"]: entry for entry in report["remediation_map"]["entries"]}
    assert remediation_entries["invalid_package_mode"]["repair_class"] == "package_frontmatter_repair"
    assert remediation_entries["missing_source_policy"]["repair_class"] == "package_frontmatter_repair"
    assert remediation_entries["missing_delivery_surface"]["repair_class"] == "delivery_surface_contract_repair"
    assert remediation_entries["missing_package_contract"]["repair_class"] == "package_contract_repair"
    assert remediation_entries["missing_h8_input"]["repair_class"] == "graph_input_coverage_repair"
    assert remediation_entries["missing_source_policy_mapping"]["repair_class"] == "source_policy_mapping_repair"
    assert remediation_entries["missing_delivery_surface_contract"]["repair_class"] == "delivery_surface_contract_repair"
    assert remediation_entries["missing_readiness_rule"]["repair_class"] == "packaging_readiness_repair"
    text_report = quality_validator.render_text_report(report)
    assert "- h9: files=1" in text_report
    assert "missing_source_policy" in text_report


def test_build_report_contains_h10_counts_and_supervision_remediation_map(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "Global_State_Consensus",
        ],
    )
    write_note(
        knowledge_dir / "H10_Broken_Supervision.md",
        h10_note_text(
            title="Broken Supervision",
            supervision_mode="invalid_mode",
            governing_signal="",
            oversight_surfaces=[],
            supervision_contracts=[],
            h9_inputs=[],
            supervised_outputs=["Global_State_Consensus"],
            governing_signal_mapping_text="",
            oversight_contract_text="",
            escalation_rules_text="",
            include_hidden10_tag=False,
        ),
    )

    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert report["kinds"]["h10"]["file_count"] == 1
    assert report["graph_metrics"]["node_count_by_kind"]["h10"] == 1
    remediation_entries = {entry["issue_code"]: entry for entry in report["remediation_map"]["entries"]}
    assert remediation_entries["invalid_supervision_mode"]["repair_class"] == "supervision_frontmatter_repair"
    assert remediation_entries["missing_governing_signal"]["repair_class"] == "supervision_frontmatter_repair"
    assert remediation_entries["missing_oversight_surface"]["repair_class"] == "oversight_surface_contract_repair"
    assert remediation_entries["missing_supervision_contract"]["repair_class"] == "supervision_contract_repair"
    assert remediation_entries["missing_h9_input"]["repair_class"] == "graph_input_coverage_repair"
    assert remediation_entries["missing_governing_signal_mapping"]["repair_class"] == "governing_signal_mapping_repair"
    assert remediation_entries["missing_oversight_surface_contract"]["repair_class"] == "oversight_surface_contract_repair"
    assert remediation_entries["missing_escalation_rule"]["repair_class"] == "strategic_escalation_repair"
    text_report = quality_validator.render_text_report(report)
    assert "- h10: files=1" in text_report
    assert "missing_governing_signal" in text_report


def test_build_report_contains_graph_metrics_section(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            *RAW_STUB_TARGETS,
            "H3_Test",
            "Topology_Analysis",
            "Strategic_Resource_Allocator",
        ],
    )
    write_note(
        knowledge_dir / "RAG_Memory_Cell_13_Test_Note.md",
        raw_note_text(title="Test Note", links=list(RAW_STUB_TARGETS)),
    )
    write_note(
        knowledge_dir / "H4_Test_Reasoning.md",
        h4_note_text(
            title="Test Reasoning",
            synthesis_inputs=["H3_Test"],
            anchors=["Topology_Analysis"],
            downstream_links=["Strategic_Resource_Allocator"],
        ),
    )

    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert "graph_metrics" in report
    assert report["graph_metrics"]["node_count_by_kind"]["h4"] == 1
    assert "forward_link_compliance_ratio" in report["graph_metrics"]


def test_build_report_contains_h5_and_delta_metrics(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    create_stub_targets(
        knowledge_dir,
        [
            "H4_Test_Reasoning",
            "Metacognitive_Reflection_Core",
            "Strategic_Resource_Allocator",
        ],
    )
    write_note(
        knowledge_dir / "H5_Test_Control.md",
        h5_note_text(
            title="Test Control",
            h4_inputs=["H4_Test_Reasoning"],
            anchors=["Metacognitive_Reflection_Core"],
            managed_outputs=["Strategic_Resource_Allocator"],
        ),
    )
    previous_report = {
        "generated_at": "2026-08-29T23:59:59+00:00",
        "summary": {
            "files_scanned": 0,
            "files_with_issues": 0,
            "issue_count": 0,
        },
        "kinds": {
            "raw": {"file_count": 0, "ok_count": 0, "issue_count": 0},
            "synthesis": {"file_count": 0, "ok_count": 0, "issue_count": 0},
            "h4": {"file_count": 0, "ok_count": 0, "issue_count": 0},
            "h5": {"file_count": 0, "ok_count": 0, "issue_count": 0},
            "index": {"file_count": 0, "ok_count": 0, "issue_count": 0},
        },
        "graph_metrics": {
            "node_count_by_kind": {
                "raw": 0,
                "synthesis": 0,
                "h4": 0,
                "h5": 0,
                "index": 0,
            },
            "forward_link_compliance_ratio": 0.0,
            "forbidden_reference_count": 0,
            "total_wikilinks": 0,
        },
    }

    report = quality_validator.build_report(
        scope="all",
        knowledge_dir=knowledge_dir,
        previous_report=previous_report,
    )

    assert report["kinds"]["h5"]["file_count"] == 1
    assert report["graph_metrics"]["node_count_by_kind"]["h5"] == 1
    assert report["delta"]["summary"]["files_scanned"]["delta"] == report["summary"]["files_scanned"]
    assert report["delta"]["kinds"]["h5"]["file_count"]["delta"] == 1
    assert report["delta"]["graph_metrics"]["forward_link_compliance_ratio"]["before"] == 0.0
    assert report["delta"]["graph_metrics"]["total_wikilinks"]["delta"] == report["graph_metrics"]["total_wikilinks"]
    assert "Delta vs previous report" in quality_validator.render_text_report(report)


def test_apply_safe_fixes_quotes_tags_and_adds_missing_section() -> None:
    original_text = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        "  - #rag/memory_cell\n"
        "  - #rag/training\n"
        "---\n\n"
        "# Test\n\n"
        "## Teknik çekirdek\n\n"
        "Metin.\n"
    )

    fixed_text, changes = quality_validator.apply_safe_fixes(original_text, kind="raw")

    assert '  - "#rag/memory_cell"' in fixed_text
    assert '  - "#rag/training"' in fixed_text
    assert "## Doğrulanmış bulgular" in fixed_text
    assert "quote_tags" in changes
    assert "add_missing_sections" in changes
