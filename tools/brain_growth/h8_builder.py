from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


SECTION_HEADERS = (
    "## Karar montaj amacı",
    "## Dominant thoughtseed sinyalleri",
    "## Policy broadcast stratejisi",
    "## Commitment kuralları",
    "## Besleyen H7 düğümleri",
    "## Yayınlanan çıktı yolları",
)

REQUIRED_TAGS = (
    "#layer/hidden_8_decision_assembly",
    "#workspace/global_broadcast",
    "#decision/dominant_thoughtseed",
    "#policy/assembly",
)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class H8Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    workspace_mode: str
    dominant_thoughtseed: str
    candidate_policies: tuple[str, ...]
    broadcast_targets: tuple[str, ...]
    decision_purpose: tuple[str, ...]
    h7_inputs: tuple[str, ...]
    assembly_signals: tuple[str, ...]
    broadcast_strategy: tuple[str, ...]
    commitment_rules: tuple[str, ...]
    downstream_outputs: tuple[str, ...]


H8_FAMILIES: tuple[H8Family, ...] = (
    H8Family(
        filename="H8_Dominant_Thoughtseed_Selection.md",
        title="Dominant Thoughtseed Selection",
        tags=(*REQUIRED_TAGS, "#workspace/thoughtseed_selection"),
        workspace_mode="dominant_policy_broadcast",
        dominant_thoughtseed="recovery_first_consensus",
        candidate_policies=("stabilize_consensus_before_execution", "minimize_regret_under_risk"),
        broadcast_targets=("Executive_Action_Formatter", "Final_Execution_Gate"),
        decision_purpose=(
            "Bu düğüm, H7 episodik örüntüler içinden o anki baskın karar çekirdeğini seçer.",
            "Amaç, temporal recall ve recency governance çıktılarından tek bir dominant thoughtseed üretmektir.",
        ),
        h7_inputs=("H7_Episodic_Timeline_Alignment", "H7_Recency_Drift_Governance"),
        assembly_signals=(
            "Aynı epizod ailesi birden çok çevrimde aynı karar önceliğini tekrar ediyorsa",
            "Recency drift kontrolü kısa vadeli gürültüyü baskılayıp kalıcı örüntüyü öne çıkarıyorsa",
            "Execution öncesi hangi policy'nin baskın olması gerektiği açık biçimde ayrışıyorsa",
        ),
        broadcast_strategy=(
            "Dominant thoughtseed önce aday policy setini sıralar, sonra en yüksek uyumlu policy'yi yayınlar.",
            "Broadcast yalnız doğrulanmış episodik örüntülerden beslenir; tekil gürültü sinyalleri seçimi belirlemez.",
        ),
        commitment_rules=(
            "Dominant thoughtseed en az iki episodik sinyal tarafından desteklenmeden sabitlenmez.",
            "Recency baskısı tek başına policy seçimi yapamaz; temporal tutarlılık da aranır.",
        ),
        downstream_outputs=("Global_State_Consensus", "Episodic_Memory_Consolidation"),
    ),
    H8Family(
        filename="H8_Global_Policy_Broadcast.md",
        title="Global Policy Broadcast",
        tags=(*REQUIRED_TAGS, "#workspace/policy_broadcast"),
        workspace_mode="dominant_policy_broadcast",
        dominant_thoughtseed="global_execution_alignment",
        candidate_policies=("align_execution_with_temporal_recall", "defer_action_until_consensus_stable"),
        broadcast_targets=("Executive_Action_Formatter", "Global_State_Consensus"),
        decision_purpose=(
            "Bu düğüm, seçilmiş policy'nin hangi yüzeylere hangi sırayla yayınlanacağını tanımlar.",
            "Amaç, global workspace düzeyinde kararın aynı anda birden çok downstream yüzeye tutarlı aktarılmasıdır.",
        ),
        h7_inputs=("H7_Event_Entity_Binding", "H7_Episodic_Timeline_Alignment"),
        assembly_signals=(
            "Entity-event bağları ile timeline hizası aynı policy yönünde yakınsıyorsa",
            "Broadcast edilecek policy birden çok downstream yüzeye ortak koordinasyon gerektiriyorsa",
            "Kararın sistem geneline yayılması execution öncesi önkoşul haline geldiyse",
        ),
        broadcast_strategy=(
            "Policy önce consensus yüzeyine, sonra execution formatter katmanına iletilir.",
            "Broadcast hedefleri sabit sırada değerlendirilir ve her hedef aynı policy kaynağına bağlanır.",
        ),
        commitment_rules=(
            "Broadcast başlamadan önce aday policy listesi boş olmamalıdır.",
            "Aynı çevrim içinde çelişen policy'ler varsa dominant thoughtseed yeniden hesaplanır.",
        ),
        downstream_outputs=("Executive_Action_Formatter", "Final_Execution_Gate"),
    ),
    H8Family(
        filename="H8_Decision_Commitment_Gate.md",
        title="Decision Commitment Gate",
        tags=(*REQUIRED_TAGS, "#workspace/commitment_gate"),
        workspace_mode="commitment_gate_selection",
        dominant_thoughtseed="causal_commitment_lock",
        candidate_policies=("commit_when_causal_chain_closed", "block_execution_on_partial_recall"),
        broadcast_targets=("Final_Execution_Gate", "Cognitive_Response_Generator"),
        decision_purpose=(
            "Bu düğüm, kararın gerçekten sabitlenip execution tarafına geçmeye hazır olup olmadığını belirler.",
            "Amaç, causal recall zinciri tamamlanmadan erken policy commit edilmesini engellemektir.",
        ),
        h7_inputs=("H7_Temporal_Causal_Recall", "H7_Episodic_Timeline_Alignment"),
        assembly_signals=(
            "Causal zincir kapanmadan karar commit edilirse downstream risk artıyorsa",
            "Timeline sırası ile policy commit eşiği birlikte okunması gereken bir bağ oluşturuyorsa",
            "Execution açılmadan önce tek bir karar kapısı gereksinimi netleşmişse",
        ),
        broadcast_strategy=(
            "Commit kararı yalnız causal recall tamamlandığında execution yüzeylerine yayınlanır.",
            "Eksik zincirlerde broadcast yerine bekleme sinyali korunur.",
        ),
        commitment_rules=(
            "En az bir H7 causal input ve bir timeline input aynı kararı desteklemelidir.",
            "Partial recall durumunda policy önerilebilir ama commit edilemez.",
        ),
        downstream_outputs=("Final_Execution_Gate", "Cognitive_Response_Generator"),
    ),
    H8Family(
        filename="H8_Exception_Override_Arbitration.md",
        title="Exception Override Arbitration",
        tags=(*REQUIRED_TAGS, "#workspace/override_arbitration"),
        workspace_mode="override_exception_arbitration",
        dominant_thoughtseed="failsafe_priority_override",
        candidate_policies=("override_on_high_risk_regression", "preserve_stable_memory_over_hot_context"),
        broadcast_targets=("Working_Memory_Flush", "Final_Execution_Gate"),
        decision_purpose=(
            "Bu düğüm, istisna durumlarında hangi override veya failsafe policy'nin baskın olacağını çözer.",
            "Amaç, sıcak bağlamın güvenilir hafızayı ezdiği anlarda güvenli arbitration katmanı sağlamaktır.",
        ),
        h7_inputs=("H7_Recency_Drift_Governance", "H7_Temporal_Causal_Recall"),
        assembly_signals=(
            "Sıcak bağlam ile doğrulanmış episodik izler çatışmaya düştüğünde",
            "Riskli override kararı geçmiş causal zincir ile destekleniyorsa",
            "Execution kapısına gitmeden önce exception arbitration gereksinimi belirginleşiyorsa",
        ),
        broadcast_strategy=(
            "Override policy önce bellek temizleme veya stabilizasyon yüzeyine, sonra execution kapısına iletilir.",
            "Failsafe ağırlığı yüksek olduğunda sıcak bağlam yerine stabilize edilmiş episodik örüntü öncelik kazanır.",
        ),
        commitment_rules=(
            "Override yalnız risk sinyali ile episodik kanıt birlikte görünüyorsa sabitlenir.",
            "Tek çevrimlik sapmalar kalıcı arbitration kararı üretmez.",
        ),
        downstream_outputs=("Working_Memory_Flush", "Long_Term_Strategic_Planner"),
    ),
)


def clean_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def clean_list(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(clean_value(value) for value in values if clean_value(value))


def family_output_path(family: H8Family, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / family.filename


def verify_existing_targets(targets: tuple[str, ...], knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    missing = [target for target in targets if not (knowledge_dir / f"{target}.md").exists()]
    if missing:
        raise FileNotFoundError(f"Eksik hedef notlar: {', '.join(missing)}")


def render_h8_note(family: H8Family) -> str:
    purpose_text = "\n\n".join(family.decision_purpose)
    signal_lines = "\n".join(f"- {item}" for item in family.assembly_signals)
    strategy_lines = "\n".join(f"- {item}" for item in family.broadcast_strategy)
    commitment_lines = "\n".join(f"- {item}" for item in family.commitment_rules)
    h7_lines = "\n".join(f"- [[{item}]]" for item in family.h7_inputs)
    output_lines = "\n".join(f"- [[{item}]]" for item in family.downstream_outputs)

    text = (
        "---\n"
        'date: "2026-08-30"\n'
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + f'workspace_mode: "{family.workspace_mode}"\n'
        + f'dominant_thoughtseed: "{family.dominant_thoughtseed}"\n'
        + "candidate_policies:\n"
        + "".join(f'  - "{item}"\n' for item in family.candidate_policies)
        + "broadcast_targets:\n"
        + "".join(f'  - "{item}"\n' for item in family.broadcast_targets)
        + "---\n\n"
        f"# {family.title}\n\n"
        "## Karar montaj amacı\n\n"
        f"{purpose_text}\n\n"
        "## Dominant thoughtseed sinyalleri\n\n"
        f"{signal_lines}\n\n"
        "## Policy broadcast stratejisi\n\n"
        f"{strategy_lines}\n\n"
        "## Commitment kuralları\n\n"
        f"{commitment_lines}\n\n"
        "## Besleyen H7 düğümleri\n\n"
        f"{h7_lines}\n\n"
        "## Yayınlanan çıktı yolları\n\n"
        f"{output_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def parse_section(text: str, header: str) -> str:
    pattern = re.compile(rf"{re.escape(header)}\n\n(.*?)(?=\n## |\Z)", re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def verify_h8_note(path: Path, family: H8Family) -> dict[str, object]:
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

    if clean_value(frontmatter.get("workspace_mode", "")) != family.workspace_mode:
        raise ValueError(f"{path.name}: workspace_mode beklenen değerle uyuşmuyor")

    if clean_value(frontmatter.get("dominant_thoughtseed", "")) != family.dominant_thoughtseed:
        raise ValueError(f"{path.name}: dominant_thoughtseed beklenen değerle uyuşmuyor")

    if clean_list(frontmatter.get("candidate_policies", [])) != family.candidate_policies:
        raise ValueError(f"{path.name}: candidate_policies beklenen sırayla uyuşmuyor")

    if clean_list(frontmatter.get("broadcast_targets", [])) != family.broadcast_targets:
        raise ValueError(f"{path.name}: broadcast_targets beklenen sırayla uyuşmuyor")

    source_section = parse_section(text, "## Besleyen H7 düğümleri")
    source_links = WIKILINK_RE.findall(source_section)
    if tuple(source_links) != family.h7_inputs:
        raise ValueError(f"{path.name}: H7 girdileri beklenen hedeflerle uyuşmuyor")

    output_section = parse_section(text, "## Yayınlanan çıktı yolları")
    output_links = WIKILINK_RE.findall(output_section)
    if tuple(output_links) != family.downstream_outputs:
        raise ValueError(f"{path.name}: çıktı yolları beklenen hedeflerle uyuşmuyor")

    return {
        "path": str(path),
        "h7_inputs": len(family.h7_inputs),
        "candidate_policies": len(family.candidate_policies),
        "broadcast_targets": len(family.broadcast_targets),
        "downstream_outputs": len(family.downstream_outputs),
        "forbidden_refs": False,
    }


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    print(f"Planned hidden_8 note count: {len(H8_FAMILIES)}")
    for family in H8_FAMILIES:
        output = family_output_path(family, knowledge_dir)
        print(
            f"- {output.name}: "
            f"h7_inputs={len(family.h7_inputs)}, "
            f"candidate_policies={len(family.candidate_policies)}, "
            f"broadcast_targets={len(family.broadcast_targets)}, "
            f"downstream_outputs={len(family.downstream_outputs)}"
        )


def write_h8_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H8_FAMILIES:
        verify_existing_targets(family.h7_inputs, knowledge_dir)
        verify_existing_targets(family.broadcast_targets, knowledge_dir)
        verify_existing_targets(family.downstream_outputs, knowledge_dir)
        path = family_output_path(family, knowledge_dir)
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h8_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)


def run_checks(paths: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    family_by_filename = {family.filename: family for family in H8_FAMILIES}
    for path in paths:
        family = family_by_filename[path.name]
        results.append(verify_h8_note(path, family))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate hidden_8 decision assembly notes.")
    parser.add_argument("--dry-run", action="store_true", help="Plan H8 files without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H8 files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_h8_notes(force=args.force)
    results = run_checks(written)

    print("Write completed.")
    for result in results:
        print(
            f"CHECK PASS | {Path(str(result['path'])).name} | "
            f"h7_inputs={result['h7_inputs']} | "
            f"candidate_policies={result['candidate_policies']} | "
            f"broadcast_targets={result['broadcast_targets']} | "
            f"downstream_outputs={result['downstream_outputs']} | "
            f"forbidden_refs={result['forbidden_refs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
