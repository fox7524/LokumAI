from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes, parse_yaml_frontmatter


TITLE_RE = re.compile(r"^# (.+)$", re.M)
RAW_INDEX_RE = re.compile(r"^RAG_Memory_Cell_(\d{2})_")
MAX_CURATED_RAW_LINKS = 8


@dataclass(frozen=True)
class DomainSpec:
    key: str
    title: str
    raw_tag: str
    synthesis_tag: str
    synthesis_filename: str
    index_filename: str
    summary: str
    usage_guidance: tuple[str, ...]


@dataclass(frozen=True)
class NoteRef:
    stem: str
    title: str
    path: Path
    sort_key: tuple[int, str]


@dataclass(frozen=True)
class DomainCatalog:
    spec: DomainSpec
    raw_notes: tuple[NoteRef, ...]
    synthesis_note: NoteRef


DOMAIN_SPECS: tuple[DomainSpec, ...] = (
    DomainSpec(
        key="apple_silicon_mlx",
        title="Apple Silicon and MLX",
        raw_tag="#hardware/apple_mlx",
        synthesis_tag="#domain/apple_silicon_mlx",
        synthesis_filename="H3_Apple_Silicon_Memory_Execution_Synthesis.md",
        index_filename="Index_Apple_Silicon_and_MLX.md",
        summary="Apple Silicon, Metal ve MLX tarafındaki unified memory, dispatch yüzeyi ve execution darboğazlarını tek girişte toplar.",
        usage_guidance=(
            "Önce sentez kapısını açıp darboğaz ailesini ayır, sonra temsilci ham hücrelere in.",
            "Barrier, residency, queue-depth veya kernel fusion soruları bu girişten başlamalıdır.",
        ),
    ),
    DomainSpec(
        key="embedded_interrupt_dma",
        title="Embedded and ESP32",
        raw_tag="#hardware/esp32",
        synthesis_tag="#domain/embedded_interrupt_dma",
        synthesis_filename="H3_Embedded_Interrupt_DMA_Synthesis.md",
        index_filename="Index_Embedded_and_ESP32.md",
        summary="ESP32, FreeRTOS, ISR ve DMA zincirini watchdog, jitter ve buffering semptomlarına göre düzenler.",
        usage_guidance=(
            "Kesme gecikmesi, underrun veya cache-disable penceresi anlatılıyorsa bu indeksten ilerle.",
            "Önce hidden_3 sentezini, sonra temsilci ISR ve DMA hücrelerini aç.",
        ),
    ),
    DomainSpec(
        key="cryptographic_integrity_memory_safety",
        title="Cryptography and Memory Safety",
        raw_tag="#system/crypto",
        synthesis_tag="#domain/cryptographic_integrity_memory_safety",
        synthesis_filename="H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis.md",
        index_filename="Index_Cryptography_and_Memory_Safety.md",
        summary="Bellek güvenliği ile kriptografik bütünlük savunmalarını tek bir failure-surface navigasyonuna dönüştürür.",
        usage_guidance=(
            "PAC, CFI, canary, enclave, AEAD veya witness exposure soruları için bu kapıyı kullan.",
            "Sentez notu, exploit semptomunu hangi primitive ailesine indireceğini belirler.",
        ),
    ),
    DomainSpec(
        key="cognitive_graph_rag_routing",
        title="Cognitive Graph RAG",
        raw_tag="#rag/graph_rag",
        synthesis_tag="#domain/cognitive_graph_rag_routing",
        synthesis_filename="H3_Cognitive_Graph_RAG_Routing_Synthesis.md",
        index_filename="Index_Cognitive_Graph_RAG.md",
        summary="Graph RAG, multi-hop retrieval, reranking ve context packing notlarını yönlendirme ekonomisi etrafında düzenler.",
        usage_guidance=(
            "Traversal budget, reranking veya context-window sıkışması yaşayan sorgular buradan başlamalıdır.",
            "Sentez notu hangi graph stratejisine inileceğini, seçili ham hücreler ise uygulama yüzeyini gösterir.",
        ),
    ),
)


def clean_tag(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def extract_title(text: str, fallback: str) -> str:
    match = TITLE_RE.search(text)
    return match.group(1).strip() if match else fallback


def sort_key_for_path(path: Path) -> tuple[int, str]:
    match = RAW_INDEX_RE.match(path.name)
    if match:
        return (int(match.group(1)), path.stem)
    return (10_000, path.stem)


def read_note_ref(path: Path) -> NoteRef:
    text = path.read_text(encoding="utf-8")
    return NoteRef(
        stem=path.stem,
        title=extract_title(text, fallback=path.stem.replace("_", " ")),
        path=path,
        sort_key=sort_key_for_path(path),
    )


def global_index_path(knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / "Brain_Growth_Index.md"


def domain_index_path(spec: DomainSpec, knowledge_dir: Path = KNOWLEDGE_DIR) -> Path:
    return knowledge_dir / spec.index_filename


def domain_specs_by_raw_tag() -> dict[str, DomainSpec]:
    return {spec.raw_tag: spec for spec in DOMAIN_SPECS}


def domain_specs_by_synthesis_tag() -> dict[str, DomainSpec]:
    return {spec.synthesis_tag: spec for spec in DOMAIN_SPECS}


def collect_domain_catalogs(knowledge_dir: Path = KNOWLEDGE_DIR) -> dict[str, DomainCatalog]:
    raw_notes: dict[str, list[NoteRef]] = {spec.key: [] for spec in DOMAIN_SPECS}
    synthesis_notes: dict[str, NoteRef] = {}

    raw_lookup = domain_specs_by_raw_tag()
    synthesis_lookup = domain_specs_by_synthesis_tag()

    for path in sorted(knowledge_dir.glob("RAG_Memory_Cell_*.md")):
        frontmatter = parse_yaml_frontmatter(path.read_text(encoding="utf-8"))
        tags = {clean_tag(tag) for tag in frontmatter.get("tags", []) if str(tag).strip()}
        for tag, spec in raw_lookup.items():
            if tag in tags:
                raw_notes[spec.key].append(read_note_ref(path))
                break

    for path in sorted(knowledge_dir.glob("H3_*.md")):
        frontmatter = parse_yaml_frontmatter(path.read_text(encoding="utf-8"))
        tags = {clean_tag(tag) for tag in frontmatter.get("tags", []) if str(tag).strip()}
        for tag, spec in synthesis_lookup.items():
            if tag in tags:
                synthesis_notes[spec.key] = read_note_ref(path)
                break

    catalogs: dict[str, DomainCatalog] = {}
    for spec in DOMAIN_SPECS:
        if not raw_notes[spec.key]:
            raise FileNotFoundError(f"{spec.title} için raw memory cell bulunamadı")
        synthesis_note = synthesis_notes.get(spec.key)
        if synthesis_note is None:
            raise FileNotFoundError(f"{spec.title} için synthesis notu bulunamadı")
        ordered_raw = tuple(sorted(raw_notes[spec.key], key=lambda item: item.sort_key))
        catalogs[spec.key] = DomainCatalog(spec=spec, raw_notes=ordered_raw, synthesis_note=synthesis_note)
    return catalogs


def unique_notes(notes: list[NoteRef]) -> list[NoteRef]:
    seen: set[str] = set()
    ordered: list[NoteRef] = []
    for note in notes:
        if note.stem in seen:
            continue
        seen.add(note.stem)
        ordered.append(note)
    return ordered


def select_curated_raw_notes(raw_notes: tuple[NoteRef, ...], limit: int = MAX_CURATED_RAW_LINKS) -> list[NoteRef]:
    ordered = list(raw_notes)
    if len(ordered) <= limit:
        return ordered

    middle = len(ordered) // 2
    selected = unique_notes(
        [
            *ordered[:3],
            *ordered[max(3, middle - 1) : min(len(ordered), middle + 1)],
            *ordered[-3:],
        ]
    )

    if len(selected) < limit:
        for note in ordered:
            if note.stem not in {item.stem for item in selected}:
                selected.append(note)
            if len(selected) == limit:
                break

    return sorted(selected[:limit], key=lambda item: item.sort_key)


def segmented_curated_notes(raw_notes: tuple[NoteRef, ...]) -> list[tuple[str, list[NoteRef]]]:
    curated = select_curated_raw_notes(raw_notes)
    if len(curated) <= 3:
        return [("Temel girişler", curated)]

    first = curated[:3]
    middle = curated[3:-3]
    last = curated[-3:]
    sections: list[tuple[str, list[NoteRef]]] = [("Temel girişler", first)]
    if middle:
        sections.append(("Orta katman kırılma noktaları", middle))
    sections.append(("İleri hata ve optimizasyon yüzeyleri", last))
    return sections


def render_frontmatter(*tags: str) -> str:
    lines = ["---", "date: 2026-08-30", "tags:"]
    for tag in tags:
        lines.append(f'  - "{tag}"')
    lines.append("---")
    return "\n".join(lines)


def render_global_index(catalogs: dict[str, DomainCatalog]) -> str:
    area_lines = []
    phase_lines = []
    for spec in DOMAIN_SPECS:
        catalog = catalogs[spec.key]
        area_lines.append(
            "- "
            f"[[{Path(spec.index_filename).stem}]] "
            f"({len(catalog.raw_notes)} raw, 1 synthesis) — "
            f"kapı notu: [[{catalog.synthesis_note.stem}]]"
        )
        phase_lines.append(
            f"- {spec.title}: Faz 1 ham hücreler temsilci alt kümeyle açılır, "
            f"Faz 2 sentez kapısı [[{catalog.synthesis_note.stem}]] üzerinden daraltılır."
        )

    usage_lines = [
        "1. Önce ilgili alan girişini aç ve problem ailesini daralt.",
        "2. Sonra hidden_3 sentez notundan mekanizma seviyesini seç.",
        "3. Son olarak temsilci ham memory-cell bağlantılarıyla kök semptoma in.",
        "4. Bu indeks bilinçli olarak tüm ham notları tek sayfada dökmez; alan bazlı gezinti sunar.",
    ]

    text = (
        f"{render_frontmatter('#index/brain_growth', '#navigation/domain_entry')}\n\n"
        "# Brain Growth Index\n\n"
        "## Alanlar\n\n"
        f"{chr(10).join(area_lines)}\n\n"
        "## Fazlar\n\n"
        "- Faz 1: Ham research wave notları alanlara göre ayrılmıştır.\n"
        "- Faz 2: Her alan için bir hidden_3 sentez kapısı vardır.\n"
        "- Faz 3: Kalite doğrulaması quality_validator ile rapor-first çalışır.\n"
        "- Faz 4: Bu not ve dört alan indeksi, küratörlü gezinme katmanını oluşturur.\n"
        f"{chr(10).join(phase_lines)}\n\n"
        "## Kullanım\n\n"
        f"{chr(10).join(f'- {line}' if line[0].isdigit() is False else line for line in usage_lines)}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def render_domain_index(catalog: DomainCatalog) -> str:
    curated_sections = segmented_curated_notes(catalog.raw_notes)
    curated_count = sum(len(notes) for _, notes in curated_sections)
    omitted_count = max(0, len(catalog.raw_notes) - curated_count)

    phase_blocks = [
        (
            "### Faz 1 · Temsilci ham memory-cell girişleri\n\n"
            + "\n\n".join(
                f"{section}\n\n" + "\n".join(f"- [[{note.stem}]]" for note in notes)
                for section, notes in curated_sections
            )
        ),
        (
            "### Faz 2 · Hidden_3 sentez kapısı\n\n"
            f"- [[{catalog.synthesis_note.stem}]]\n"
            f"- Bu kapı, {catalog.spec.title} alanındaki ham hücreleri mekanizma ailesine göre daraltır."
        ),
        (
            "### Faz 4 · Kürasyon notu\n\n"
            f"- Toplam raw hücre: {len(catalog.raw_notes)}\n"
            f"- Bu sayfada görünen temsilci bağlantı: {curated_count}\n"
            f"- Görünmeyen {omitted_count} hücre, sentez kapısı ve etiket üzerinden açılır; bilinçli olarak tek sayfada omnidump yapılmaz."
        ),
    ]

    usage_lines = "\n".join(f"- {line}" for line in catalog.spec.usage_guidance)

    text = (
        f"{render_frontmatter('#index/brain_growth', catalog.spec.synthesis_tag)}\n\n"
        f"# {catalog.spec.title} Index\n\n"
        "## Alanlar\n\n"
        f"- Üst giriş: [[Brain_Growth_Index]]\n"
        f"- Alan sentezi: [[{catalog.synthesis_note.stem}]]\n"
        f"- Kapsam özeti: {catalog.spec.summary}\n\n"
        "## Fazlar\n\n"
        f"{chr(10).join(phase_blocks)}\n\n"
        "## Kullanım\n\n"
        f"{usage_lines}\n"
    )
    assert_no_forbidden_nodes(text)
    return text


def build_index_documents(knowledge_dir: Path = KNOWLEDGE_DIR) -> dict[str, str]:
    catalogs = collect_domain_catalogs(knowledge_dir=knowledge_dir)
    documents = {str(global_index_path(knowledge_dir)): render_global_index(catalogs)}
    for spec in DOMAIN_SPECS:
        documents[str(domain_index_path(spec, knowledge_dir))] = render_domain_index(catalogs[spec.key])
    return documents


def write_indexes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    documents = build_index_documents(knowledge_dir=knowledge_dir)
    written: list[Path] = []
    for path_str, text in documents.items():
        path = Path(path_str)
        if path.exists() and not force:
            raise FileExistsError(f"Refusing to overwrite existing index file: {path.name}")
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return sorted(written)


def print_plan(knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
    catalogs = collect_domain_catalogs(knowledge_dir=knowledge_dir)
    print("Planned index note count: 5")
    print(f"- {global_index_path(knowledge_dir).name}: 4 alan girişi")
    for spec in DOMAIN_SPECS:
        catalog = catalogs[spec.key]
        curated = select_curated_raw_notes(catalog.raw_notes)
        print(
            f"- {spec.index_filename}: raw={len(catalog.raw_notes)}, "
            f"synthesis=1, curated_links={len(curated)}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 4 brain-growth index notes.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Plan index files without writing")
    mode.add_argument("--write", action="store_true", help="Write index markdown files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing index files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print_plan()
        return 0

    written = write_indexes(force=args.force)
    print("Write completed.")
    for path in written:
        print(f"- {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
