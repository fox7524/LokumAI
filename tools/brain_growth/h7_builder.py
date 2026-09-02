from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Episodik amaç",
    "## Zamansal sinyaller",
    "## Temporal edge politikası",
    "## Entity-event bağlama stratejisi",
    "## Besleyen H6 düğümleri",
    "## Hafıza çıktıları",
)

REQUIRED_TAGS = (
    "#layer/hidden_7_episodic_temporal_memory",
    "#memory/episodic",
    "#reasoning/temporal",
    "#graph/entity_event_dual",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H7Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    episode_mode: str
    temporal_relations: tuple[str, ...]
    primary_entities: tuple[str, ...]
    primary_events: tuple[str, ...]
    episodic_purpose: tuple[str, ...]
    h6_inputs: tuple[str, ...]
    temporal_signals: tuple[str, ...]
    temporal_edge_policy: tuple[str, ...]
    entity_event_binding_strategy: tuple[str, ...]
    memory_outputs: tuple[str, ...]


H7_FAMILIES: tuple[H7Family, ...] = (
    H7Family(
        filename="H7_Episodic_Timeline_Alignment.md",
        title="Episodic Timeline Alignment",
        tags=(
            *REQUIRED_TAGS,
            "#memory/timeline_alignment",
        ),
        episode_mode="ordered_episode_reconstruction",
        temporal_relations=("before", "after", "overlaps_with"),
        primary_entities=("executive_queue", "retrieval_budget", "response_plan"),
        primary_events=("priority_shift", "evidence_lock", "execution_release"),
        episodic_purpose=(
            "Bu episodik düğüm, H6 seviyesinde ayrı yürütülen kararların hangi sırayla yaşandığını tek bir zaman çizgisinde hizalar.",
            "Amaç, executive öncelik değişimleri ile retrieval-to-action geçişlerinin aynı epizod içinde yeniden kurulabilmesini sağlamaktır.",
        ),
        h6_inputs=(
            "H6_Executive_Priority_Orchestration",
            "H6_Retrieval_Action_Coordination",
        ),
        temporal_signals=(
            "Aynı olay ailesi içinde önce kanıt toplama sonra eylem montajı sonra execution açılışı gözleniyorsa",
            "H6 karar sırası farklı çevrimlerde kayıyor ve post-hoc analiz zaman çizgisini tutarlı kuramıyorsa",
            "Bir epizodun kritik anları response planı ile queue önceliği arasında dağılmış görünüyorsa",
        ),
        temporal_edge_policy=(
            "Timeline rekonstrüksiyonu için before/after ilişkileri varsayılan kenar ailesi olarak tutulur.",
            "Eşzamanlı ama bağımlı adımlar overlaps_with kenarı ile bağlanır; salt aynı çevrimde görünmeleri yeterli sayılmaz.",
            "Execution release ancak upstream evidence_lock olayı açıkça bağlanabiliyorsa aynı epizoda dahil edilir.",
        ),
        entity_event_binding_strategy=(
            "Entity bağları, queue, budget ve response planı gibi durum taşıyan öğeleri epizodun sabit aktörleri olarak işler.",
            "Event bağları, bu aktörlerin durum değiştirdiği priority_shift, evidence_lock ve execution_release anlarına sabitlenir.",
            "Bağlama stratejisi, aynı entity'nin birden çok event içindeki rolünü zaman çizgisi sıra bilgisiyle korur.",
        ),
        memory_outputs=(
            "Episodic_Memory_Consolidation",
            "Semantic_Graph_Weaver",
            "Time_Series_Smoothing",
        ),
    ),
    H7Family(
        filename="H7_Event_Entity_Binding.md",
        title="Event Entity Binding",
        tags=(
            *REQUIRED_TAGS,
            "#memory/entity_binding",
        ),
        episode_mode="entity_event_binding",
        temporal_relations=("triggers", "participates_in", "co_occurs_with"),
        primary_entities=("retrieval_path", "threat_surface", "consensus_state"),
        primary_events=("graph_expansion", "mitigation_decision", "consensus_commit"),
        episodic_purpose=(
            "Bu düğüm, aynı epizod içinde hangi entity'nin hangi event ile hangi bağlamda ilişkili olduğunu belirginleştirir.",
            "Amaç, H6 response ve retrieval akışlarından gelen olayları dual-graph temsiline çevrilmeye hazır hale getirmektir.",
        ),
        h6_inputs=(
            "H6_Retrieval_Action_Coordination",
            "H6_Global_Response_Orchestration",
        ),
        temporal_signals=(
            "Graph expansion ile mitigation kararı aynı olay penceresinde birbirini etkiliyorsa",
            "Consensus commit, hangi retrieval path veya threat surface değişiminin sonucu olduğu belirsizleşiyorsa",
            "Entity'ler sabit kalıyor ama event bağları her çevrimde yeniden çözülüyorsa",
        ),
        temporal_edge_policy=(
            "Event-to-entity kenarları, yalnız nedensel ya da katılımsal bağ gerekçelendirilebildiğinde açılır.",
            "Sadece aynı anda görülme durumu, co_occurs_with kenarı dışında daha güçlü bağ üretmez.",
            "Consensus commit gibi kapanış event'leri upstream graph_expansion veya mitigation_decision olaylarına geriye dönük bağlanır.",
        ),
        entity_event_binding_strategy=(
            "Retrieval path, threat surface ve consensus state düğümleri episode boyunca taşınan ana entity setidir.",
            "Graph expansion, mitigation decision ve consensus commit olayları bu entity'lerin zaman içindeki rol değişimlerini işaretler.",
            "Aynı event birden çok entity'ye bağlanıyorsa bağ türü ayrı tutulur ve dual-graph çakışması önlenir.",
        ),
        memory_outputs=(
            "Ontological_Graph_Mapper",
            "Semantic_Graph_Weaver",
            "Episodic_Memory_Consolidation",
        ),
    ),
    H7Family(
        filename="H7_Temporal_Causal_Recall.md",
        title="Temporal Causal Recall",
        tags=(
            *REQUIRED_TAGS,
            "#memory/causal_recall",
        ),
        episode_mode="causal_episode_recall",
        temporal_relations=("causes", "preceded_by", "resolved_by"),
        primary_entities=("response_branch", "recovery_window", "strategic_plan"),
        primary_events=("incident_escalation", "recovery_gate_open", "plan_revision"),
        episodic_purpose=(
            "Bu düğüm, geçmiş epizodlardan neden-sonuç zinciri çıkararak hangi olay dizisinin stratejik planı değiştirdiğini hatırlatır.",
            "Amaç, response branch ve recovery sequencing ilişkisini sırf anlık state olarak değil zamansal causal recall olarak depolamaktır.",
        ),
        h6_inputs=(
            "H6_Global_Response_Orchestration",
            "H6_Recovery_Execution_Sequencing",
        ),
        temporal_signals=(
            "Incident escalation sonrası recovery gate açılışı ile plan revision arasındaki sıra anlamlı fark yaratıyorsa",
            "Benzer olaylar farklı sonuçlar üretiyor ve kritik farkın temporal order olduğu düşünülüyorsa",
            "Geçmiş response zinciri geri çağrılmadan yeni stratejik plan güvenle sabitlenemiyorsa",
        ),
        temporal_edge_policy=(
            "Causal recall içinde causes ve resolved_by kenarları, salt korelasyondan daha güçlü kanıt istediği için ayrı tutulur.",
            "Plan revision bir closure event olarak yalnız ilgili recovery window tamamlandıktan sonra resolved_by kenarı alır.",
            "Preceded_by ilişkisi, incident escalation ile recovery gate open arasındaki minimal zaman düzenini korur.",
        ),
        entity_event_binding_strategy=(
            "Response branch ve strategic plan gibi entity'ler, epizod boyunca etkilenip yeniden yapılandırılan sürekli öğelerdir.",
            "Incident escalation, recovery gate open ve plan revision olayları bu entity'ler üstündeki dönüşümü zamanlı işaretler.",
            "Bağlama stratejisi, recall sırasında hangi event'in hangi entity durumunu değiştirdiğini nedensel sırayla geri çağırır.",
        ),
        memory_outputs=(
            "Episodic_Memory_Consolidation",
            "Cognitive_Response_Generator",
            "Long_Term_Strategic_Planner",
        ),
    ),
    H7Family(
        filename="H7_Recency_Drift_Governance.md",
        title="Recency Drift Governance",
        tags=(
            *REQUIRED_TAGS,
            "#memory/recency_governance",
        ),
        episode_mode="recency_bias_control",
        temporal_relations=("decays_after", "reinforced_by", "superseded_by"),
        primary_entities=("working_context", "stabilized_memory", "consensus_snapshot"),
        primary_events=("recall_refresh", "context_flush", "consensus_update"),
        episodic_purpose=(
            "Bu düğüm, en yeni olayların eski ama daha güvenilir epizodları gereksiz yere bastırmasını engelleyen recency governance katmanıdır.",
            "Amaç, H6 yürütme akışlarından gelen sıcak bağlamı yönetirken stabilized memory ile working context arasındaki drift'i kontrol etmektir.",
        ),
        h6_inputs=(
            "H6_Executive_Priority_Orchestration",
            "H6_Recovery_Execution_Sequencing",
        ),
        temporal_signals=(
            "Yeni recall refresh olayları eski ama doğrulanmış consensus snapshot'ları hızla gölgeliyorsa",
            "Context flush sonrasında hangi episodik bağların korunacağı belirsizleşiyorsa",
            "Son çevrim sinyalleri kısa vadede baskın olup uzun vadeli toparlama desenlerini yanlış yönlendiriyorsa",
        ),
        temporal_edge_policy=(
            "Recency drift için decays_after kenarı, bağın zamanla zayıfladığını ama tamamen silinmediğini işaretler.",
            "Reinforced_by kenarı yalnız tekrar eden ve doğrulanmış recall refresh olaylarında ağırlık kazanır.",
            "Superseded_by ilişkisi, yeni consensus update gerçekten daha güvenilir olduğunda eski episodik izi ikincil yapar.",
        ),
        entity_event_binding_strategy=(
            "Working context, stabilized memory ve consensus snapshot düğümleri recency baskısının etkilediği ana entity setidir.",
            "Recall refresh, context flush ve consensus update olayları bu entity'lerin ağırlık ve görünürlük değişimini temsil eder.",
            "Bağlama stratejisi, sıcak bağlam ile kalıcı hafıza arasındaki geçişleri epizodik iz olarak saklar.",
        ),
        memory_outputs=(
            "Episodic_Memory_Decay_Controller",
            "Working_Memory_Flush",
            "Global_State_Consensus",
        ),
    ),
)


def clean_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def clean_list(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(clean_value(value) for value in values if clean_value(value))


def family_output_path(family: H7Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h7_note(family: H7Family) -> str:
    purpose_text = "\n\n".join(family.episodic_purpose)
    signal_lines = "\n".join(f"- {item}" for item in family.temporal_signals)
    edge_lines = "\n".join(f"- {item}" for item in family.temporal_edge_policy)
    binding_lines = "\n".join(f"- {item}" for item in family.entity_event_binding_strategy)
    h6_lines = "\n".join(f"- [[{item}]]" for item in family.h6_inputs)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.memory_outputs)

    text = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + f'episode_mode: "{family.episode_mode}"\n'
        + "temporal_relations:\n"
        + "".join(f'  - "{item}"\n' for item in family.temporal_relations)
        + "primary_entities:\n"
        + "".join(f'  - "{item}"\n' for item in family.primary_entities)
        + "primary_events:\n"
        + "".join(f'  - "{item}"\n' for item in family.primary_events)
        + "---\n\n"
        f"# {family.title}\n\n"
        "## Episodik amaç\n\n"
        f"{purpose_text}\n\n"
        "## Zamansal sinyaller\n\n"
        f"{signal_lines}\n\n"
        "## Temporal edge politikası\n\n"
        f"{edge_lines}\n\n"
        "## Entity-event bağlama stratejisi\n\n"
        f"{binding_lines}\n\n"
        "## Besleyen H6 düğümleri\n\n"
        f"{h6_lines}\n\n"
        "## Hafıza çıktıları\n\n"
        f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h7_note(path: Path, family: H7Family) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_yaml_frontmatter(text)
    tags = clean_list(frontmatter.get("tags", []))
    assert_no_forbidden_nodes(text)

    missing_sections = [header for header in SECTION_HEADERS if header not in text]
    if missing_sections:
        raise ValueError(f"{path.name}: eksik bölümler: {', '.join(missing_sections)}")

    title_line = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "")
    if title_line != family.title:
        raise ValueError(f"{path.name}: başlık beklenen değerle uyuşmuyor")

    for tag in family.tags:
        if tag not in tags:
            raise ValueError(f"{path.name}: etiket eksik: {tag}")

    if clean_value(frontmatter.get("episode_mode", "")) != family.episode_mode:
        raise ValueError(f"{path.name}: episode_mode beklenen değerle uyuşmuyor")

    if clean_list(frontmatter.get("temporal_relations", [])) != family.temporal_relations:
        raise ValueError(f"{path.name}: temporal_relations beklenen sırayla uyuşmuyor")

    if clean_list(frontmatter.get("primary_entities", [])) != family.primary_entities:
        raise ValueError(f"{path.name}: primary_entities beklenen sırayla uyuşmuyor")

    if clean_list(frontmatter.get("primary_events", [])) != family.primary_events:
        raise ValueError(f"{path.name}: primary_events beklenen sırayla uyuşmuyor")

    source_section = parse_section(text, "## Besleyen H6 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    if tuple(source_links) != family.h6_inputs:
        raise ValueError(f"{path.name}: H6 girdileri beklenen hedeflerle uyuşmuyor")

    output_section = parse_section(text, "## Hafıza çıktıları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.memory_outputs:
        raise ValueError(f"{path.name}: hafıza çıktıları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h6_inputs": len(family.h6_inputs),
        "temporal_relations": len(family.temporal_relations),
        "primary_entities": len(family.primary_entities),
        "primary_events": len(family.primary_events),
        "memory_outputs": len(family.memory_outputs),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_7 note count: {len(H7_FAMILIES)}")
    for family in H7_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"h6_inputs={len(family.h6_inputs)}, "
            f"temporal_relations={len(family.temporal_relations)}, "
            f"primary_entities={len(family.primary_entities)}, "
            f"primary_events={len(family.primary_events)}, "
            f"memory_outputs={len(family.memory_outputs)}"
        )


def write_h7_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H7_FAMILIES:
        verify_existing_targets(family.h6_inputs, knowledge_dir)
        verify_existing_targets(family.memory_outputs, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h7_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H7_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h7_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_7 episodic temporal memory notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H7 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H7 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h7_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"h6_inputs={result['h6_inputs']} | "
            f"temporal_relations={result['temporal_relations']} | "
            f"primary_entities={result['primary_entities']} | "
            f"primary_events={result['primary_events']} | "
            f"memory_outputs={result['memory_outputs']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
