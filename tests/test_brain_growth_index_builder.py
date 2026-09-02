from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import common, index_builder, quality_validator


def write_note(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def raw_note_text(*, title: str, raw_tag: str) -> str:
    return (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        '  - "#rag/memory_cell"\n'
        '  - "#rag/training"\n'
        f'  - "{raw_tag}"\n'
        "---\n\n"
        f"# {title}\n\n"
        "## Teknik çekirdek\n\n"
        "Ham not.\n\n"
        "## Doğrulanmış bulgular\n\n"
        "- Bulgu\n\n"
        "## LokumAI için çıkarım\n\n"
        "Çıkarım.\n\n"
        "## Sorgu ipuçları\n\n"
        "- ipucu\n\n"
        "## Kaynaklar\n\n"
        "- https://example.com\n"
    )


def synthesis_note_text(*, title: str, domain_tag: str) -> str:
    return (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        '  - "#layer/hidden_3_logic_synthesis"\n'
        f'  - "{domain_tag}"\n'
        "---\n\n"
        f"# {title}\n\n"
        "## Soyutlama\n\n"
        "Sentez.\n\n"
        "## İnvariantlar\n\n"
        "- Kural\n\n"
        "## Retrieval yönlendirme anlamı\n\n"
        "- Yönlendirme\n\n"
        "## Besleyen düğümler\n\n"
        "- [[RAG_Memory_Cell_13_Test]]\n\n"
        "## İleri besleme\n\n"
        "- [[Semantic_Graph_Weaver]]\n"
    )


def populate_minimal_knowledge(knowledge_dir: Path, raw_per_domain: int = 3) -> None:
    for spec_index, spec in enumerate(index_builder.DOMAIN_SPECS, start=1):
        for offset in range(raw_per_domain):
            raw_index = spec_index * 10 + offset
            write_note(
                knowledge_dir / f"RAG_Memory_Cell_{raw_index:02d}_{spec.key}_{offset}.md",
                raw_note_text(title=f"{spec.title} Raw {offset}", raw_tag=spec.raw_tag),
            )
        write_note(
            knowledge_dir / spec.synthesis_filename,
            synthesis_note_text(
                title=Path(spec.synthesis_filename).stem.replace("H3_", "").replace("_", " "),
                domain_tag=spec.synthesis_tag,
            ),
        )


def test_index_output_filenames_are_stable(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"

    assert index_builder.global_index_path(knowledge_dir).name == "Brain_Growth_Index.md"
    assert [spec.index_filename for spec in index_builder.DOMAIN_SPECS] == [
        "Index_Apple_Silicon_and_MLX.md",
        "Index_Embedded_and_ESP32.md",
        "Index_Cryptography_and_Memory_Safety.md",
        "Index_Cognitive_Graph_RAG.md",
    ]


def test_collect_domain_catalogs_groups_raw_and_synthesis_by_domain_tag(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    populate_minimal_knowledge(knowledge_dir, raw_per_domain=2)

    catalogs = index_builder.collect_domain_catalogs(knowledge_dir=knowledge_dir)

    assert set(catalogs) == {spec.key for spec in index_builder.DOMAIN_SPECS}
    for spec in index_builder.DOMAIN_SPECS:
        catalog = catalogs[spec.key]
        assert len(catalog.raw_notes) == 2
        assert catalog.synthesis_note.path.name == spec.synthesis_filename


def test_rendered_indexes_include_required_sections_and_pass_validator(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    populate_minimal_knowledge(knowledge_dir, raw_per_domain=3)

    catalogs = index_builder.collect_domain_catalogs(knowledge_dir=knowledge_dir)
    global_text = index_builder.render_global_index(catalogs)
    domain_text = index_builder.render_domain_index(catalogs[index_builder.DOMAIN_SPECS[0].key])

    for section in quality_validator.INDEX_REQUIRED_SECTIONS:
        assert section in global_text
        assert section in domain_text

    common.assert_no_forbidden_nodes(global_text)
    common.assert_no_forbidden_nodes(domain_text)
    assert "LokumAI-1.0" not in global_text
    assert "LokumAI-1.0" not in domain_text


def test_domain_index_curates_raw_links_instead_of_dumping_everything(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    populate_minimal_knowledge(knowledge_dir, raw_per_domain=12)

    catalog = index_builder.collect_domain_catalogs(knowledge_dir=knowledge_dir)[index_builder.DOMAIN_SPECS[0].key]
    curated = index_builder.select_curated_raw_notes(catalog.raw_notes)
    text = index_builder.render_domain_index(catalog)

    raw_links = [link for link in common.parse_wikilinks(text) if link.startswith("RAG_Memory_Cell_")]
    assert len(curated) == index_builder.MAX_CURATED_RAW_LINKS
    assert len(raw_links) == index_builder.MAX_CURATED_RAW_LINKS
    assert len({note.stem for note in catalog.raw_notes}) > len(set(raw_links))
    assert "omnidump yapılmaz" in text


def test_write_indexes_persists_global_and_domain_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    populate_minimal_knowledge(knowledge_dir, raw_per_domain=2)

    written = index_builder.write_indexes(force=False, knowledge_dir=knowledge_dir)

    assert [path.name for path in written] == sorted(
        [
            "Brain_Growth_Index.md",
            "Index_Apple_Silicon_and_MLX.md",
            "Index_Embedded_and_ESP32.md",
            "Index_Cryptography_and_Memory_Safety.md",
            "Index_Cognitive_Graph_RAG.md",
        ]
    )
    for path in written:
        assert path.exists()
