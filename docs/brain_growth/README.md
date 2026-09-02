# Brain Growth Toolchain

Bu klasör, `Lokum1.0/Knowledge` içindeki kontrollü büyüme akışını dokümante eder.

## Faz sırası

1. Phase 1: araştırma dalgası (`RAG_Memory_Cell_*.md`)
2. Phase 2: konu bazlı `hidden_3` sentez notları
3. Phase 3: kalite doğrulayıcı
4. Phase 4: indeks ve gezinme katmanı

## Değişmez merkez kuralı

- `LokumAI-1.0.md` salt-okunur sözlük düğümüdür.
- Bu dosya değiştirilmez.
- Yeni notlar bu dosyaya bağlanmaz.

## Adlandırma kuralları

- Ham araştırma notları: `RAG_Memory_Cell_<seri>_<Konu>.md`
- Seri numarası mevcut dizinin devamından başlar.
- Sentez notları: `H3_<Konu>.md`
- Başlık slug'ları dosya adı için normalize edilir.

## Phase 1 çıktı biçimi

Her yeni `RAG_Memory_Cell_*` notu şunları içerir:

- quoted YAML frontmatter
- `"#rag/memory_cell"`
- `"#rag/training"`
- alan etiketi
- `## Teknik çekirdek`
- `## Doğrulanmış bulgular`
- `## LokumAI için çıkarım`
- `## Sorgu ipuçları`
- `## Kaynaklar`
- en az 4 kontrollü ileri wikilink

## Rapor ve doğrulama

- pytest doğrulaması: `/Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_common.py`
- gelecekteki rapor çıktıları: `/Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/reports/`
- doğrudan sayı kontrolleri Phase 1 sonunda dosya ve wikilink toplamlarını ölçer
