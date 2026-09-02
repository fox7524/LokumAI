# Wave 7 Episodic Temporal Reasoning Plan

## Summary

Bir sonraki dalga için en doğru kapsam, LokumAI bilişsel grafını `hidden_6` sonrasına taşıyan tek bir `Wave 7` açmaktır. Bu dalga, yeni bir `hidden_7` katmanı altında episodic memory ve temporal reasoning iskeleti kurmalı; bunu yaparken mevcut `brain_growth` desenini bozmadan yeni `H7_*.md` notları, validator genişletmesi ve projection tarafında türetilmiş bir `temporal_dual_graph` export’u eklemelidir.

Planın temel amacı üç parçayı birlikte tasarlamaktır:

1. semantic vault içinde gerçek `H7_*` episodic-temporal düğümler
2. validator içinde H7 doğrulama ve temporal/entity-event remediation kuralları
3. projection içinde `hidden_7` görünürlüğü ve entity-event + temporal edge temsili

Bu dalga runtime retrieval motoru kurmayacak. Amaç, önce semantic modelin, validasyonun ve görsel/export yüzeyinin bu yeni bilişsel yeteneği taşıyabilmesini sağlamaktır.

## Current State Analysis

Mevcut durumda proje aşağıdaki katmanlara sahip:

- `raw` memory cell düğümleri
- `H3` synthesis düğümleri
- `H4` reasoning / convergence düğümleri
- `H5` metacognitive control düğümleri
- `H6` executive orchestration düğümleri

Güncel validator raporuna göre sistem temiz durumdadır:

- `raw: 52`
- `synthesis: 4`
- `h4: 6`
- `h5: 4`
- `h6: 4`
- `index: 5`
- `files_scanned: 75`
- `issue_count: 0`

Güncel projection çıktısına göre katmanlı görünüş artık sabit positional metadata üretiyor:

- `raw: 64`
- `hidden_3: 4`
- `hidden_4: 6`
- `hidden_5: 4`
- `hidden_6: 4`
- `index: 5`
- `total_nodes: 87`
- `total_edges: 119`

Bu yapı şunu gösteriyor: reasoning, metacognitive arbitration ve executive orchestration oturmuş durumda; fakat sistem hâlâ olayların zaman içindeki sıralı belleğini ve entity-event ayrımını first-class şekilde temsil etmiyor. Mevcut projection dosyasında `RAG_Memory_Cell_56_Temporal_Edges_In_Episodic_Memory_Graphs` gibi temporal fikirler ham bilgi olarak var, fakat bunlar henüz katman düzeyinde bilişsel yeteneğe dönüşmemiş.

Araştırma zemini bunu destekliyor:

- DYNA, episodic memory için olay düğümleri ile `before/after/co-occurs` gibi directed timestamped temporal edges kullanımını öneriyor ve temporal KG tabanlı external memory’nin continual learning için uygun olduğunu gösteriyor.
- E2RAG, entity ve event subgraph’larını ayrı tutup bunları bipartite mapping ile bağlamanın temporal-causal consistency için daha iyi olduğunu savunuyor.

Bu nedenle Wave 7’nin doğru hedefi, bu iki fikri mevcut LokumAI desenine uyarlamak olmalıdır.

## Proposed Changes

### 1. Yeni semantic katman: `hidden_7_episodic_temporal_memory`

#### Dosyalar

- `tools/brain_growth/common.py`
- `tools/brain_growth/h7_builder.py`
- `tests/test_brain_growth_h7_builder.py`
- `Lokum1.0/Knowledge/H7_Episodic_Timeline_Alignment.md`
- `Lokum1.0/Knowledge/H7_Event_Entity_Binding.md`
- `Lokum1.0/Knowledge/H7_Temporal_Causal_Recall.md`
- `Lokum1.0/Knowledge/H7_Recency_Drift_Governance.md`

#### Ne değişecek

`common.py` içine `discover_hidden_7_targets()` eklenecek ve `allowed_forward_targets()` H7 setini tanıyacak. Yeni `h7_builder.py`, H4/H5/H6 builder desenini koruyarak dört gerçek `H7_*.md` notu üretecek.

Her `H7_*` notu şu zorunlu shape’e sahip olacak:

- quoted YAML frontmatter
- `#layer/hidden_7_episodic_temporal_memory`
- `#memory/episodic`
- `#reasoning/temporal`
- `#graph/entity_event_dual`
- `episode_mode`
- `temporal_relations`
- `primary_entities`
- `primary_events`

Önerilen zorunlu section başlıkları:

- `## Episodik amaç`
- `## Zamansal sinyaller`
- `## Temporal edge politikası`
- `## Entity-event bağlama stratejisi`
- `## Besleyen H6 düğümleri`
- `## Hafıza çıktıları`

#### Neden

H6 yürütücü kararları orkestre ediyor, ama olay-zaman bağımlı belleği modellemiyor. H7, H6’dan gelen kontrol çıktılarını “hangi olay hangi sırada yaşandı, hangi entity hangi event ile hangi bağlamda ilişkili” düzeyine taşıyarak temporal cognition açacak.

#### Nasıl

TDD ile ilerlenmeli:

1. `tests/test_brain_growth_h7_builder.py` içinde önce fail eden testler yazılmalı
2. `discover_hidden_7_targets()` ve `allowed_forward_targets()` genişletilmeli
3. `H7Family` veri yapısı tanımlanmalı
4. builder içinde deterministic render ve target verification eklenmeli
5. dört gerçek `H7_*` notu üretilmeli

Bu dalgada üretilmesi önerilen H7 aileleri:

- `H7_Episodic_Timeline_Alignment.md`
- `H7_Event_Entity_Binding.md`
- `H7_Temporal_Causal_Recall.md`
- `H7_Recency_Drift_Governance.md`

### 2. Validator genişletmesi: H7 validation + remediation classes

#### Dosyalar

- `tools/brain_growth/quality_validator.py`
- `tests/test_brain_growth_validator.py`
- `docs/brain_growth/reports/brain_growth_validation.json`
- `docs/brain_growth/reports/brain_growth_validation.txt`

#### Ne değişecek

Validator artık `H7_*.md` notlarını da resmi katman olarak tarayacak. `REPORT_KIND_ORDER` içine `h7` eklenecek. `H7_REQUIRED_SECTIONS`, `h7_note_paths()` ve `validate_h7_note()` tanımlanacak.

Yeni issue code aileleri:

- `missing_temporal_relation`
- `missing_entity_event_binding`
- `missing_h6_input`
- `invalid_episode_mode`
- `missing_primary_entities`
- `missing_primary_events`

Yeni remediation class aileleri:

- `temporal_edge_schema_repair`
- `entity_event_binding_repair`
- `episodic_frontmatter_repair`

#### Neden

Mevcut validator yapısal kaliteyi kontrol ediyor ama episodic-temporal katmanın asıl riskleri için özel sinyal üretmiyor. H7 geldikten sonra kalite sorunu artık sadece “section eksik” değil; temporal edge modelinin, entity-event bağının ve episode mode’un bozulması da kritik olacak.

#### Nasıl

Validator, H7 frontmatter ve body içeriğini parse ederek en az şu metrikleri üretmeli:

- `h6_inputs`
- `temporal_relation_count`
- `entity_count`
- `event_count`
- `wikilink_count`

Text ve JSON raporlarında `h7` kind sayıları ve gerekiyorsa remediation hints açık görünmeli. Safe-fix bu dalgada H7 semantics’ini otomatik doldurmamalı; sadece raporlamalı.

### 3. Projection genişletmesi: `hidden_7` ve `temporal_dual_graph`

#### Dosyalar

- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_layered_projection.py`
- `docs/brain_growth/projections/brain_growth_layered_projection.json`
- `docs/brain_growth/projections/brain_growth_layered_projection.md`

#### Ne değişecek

`LAYER_ORDER` içine `hidden_7` eklenecek. H7 düğümleri positional layout modeline dahil edilecek. Ayrıca projection payload’ına derived bir `temporal_dual_graph` bölümü eklenecek.

Bu bölüm en az şu alanları taşımalı:

- `entity_nodes`
- `event_nodes`
- `bipartite_edges`
- `temporal_edges`

Her temporal edge içinde relation alanı açıkça bulunmalı:

- `before`
- `after`
- `co_occurs`

#### Neden

E2RAG’in ana fikri entity ve event’i ayırmaktır. DYNA’nın ana fikri olayları temporal edge’lerle bağlamaktır. Bunları ayrı ayrı runtime motoruna çevirmeden önce projection/export seviyesinde görünür hale getirmek, hem sistemin okunabilirliğini hem sonraki dalgaların güvenliğini artırır.

#### Nasıl

İlk sürümde entity ve event ayrı Obsidian notları olmayacak. Bunun yerine H7 frontmatter alanlarından projection sırasında derived dual-graph üretilecek. Bu sayede dosya patlaması olmadan temporal-episodic model sistemin içine alınır.

Projection testleri en az şunları doğrulamalı:

- `hidden_7` katmanı `LAYER_ORDER` içinde görünmeli
- `hidden_6_to_hidden_7` transition üretilebilmeli
- `temporal_dual_graph.entity_nodes` boş olmamalı
- `temporal_dual_graph.event_nodes` boş olmamalı
- `temporal_dual_graph.temporal_edges` relation taşımalı

### 4. Artifact refresh ve integrity pass

#### Dosyalar

- `docs/brain_growth/reports/brain_growth_validation.json`
- `docs/brain_growth/reports/brain_growth_validation.txt`
- `docs/brain_growth/projections/brain_growth_layered_projection.json`
- `docs/brain_growth/projections/brain_growth_layered_projection.md`

#### Ne değişecek

Full brain-growth suite çalıştırılacak, sonra H7 builder, validator ve projection artefact’ları yenilenecek.

#### Neden

H7, mevcut H4/H5/H6 zincirinin üstüne bindiği için regresyon riski yüksek. Bu nedenle artifact refresh yalnız çıktı üretmek için değil, yeni temporal layer’ın eski reasoning/control/orchestration katmanlarını bozmadığını göstermek için de gereklidir.

#### Nasıl

Son integrity pass şu noktaları açıkça doğrulamalı:

- `h7` validator kind sayımları görünmeli
- projection’da `hidden_7` görünmeli
- `temporal_dual_graph` export dolu gelmeli
- remediation map gereksiz gürültü üretmemeli
- `LokumAI-1.0.md` untouched kalmalı

## Assumptions & Decisions

### Ana karar

Wave 7, tam bir episodic retrieval engine kurmayacak. Bu dalga yalnızca semantic layer + validator + projection iskeletini açacak.

### Kapsam dışı kararlar

Bu dalgada yapılmayacaklar:

- gerçek runtime graph traversal retriever
- automatic entity extraction pipeline
- yeni raw research wave üretimi
- legacy `layer/hidden_7_strategic_planning` notlarını migrate etme

### Legacy hidden_7 kararı

Mevcut repoda eski `hidden_7` adlandırmaları bulunabilse bile, bu dalga resmi layer olarak sadece `H7_*.md` pattern’i ile çalışmalı. Aksi halde semantic çakışma ve validator scope patlaması olur.

### Skill kaynaklı kararlar

Yüklü workflow’lardan alınan bağlayıcı desenler:

- `brainstorming`: tek wave kapsamı, design-first, gereksiz subsystem genişlemesinden kaçın
- `writing-plans`: file map açık olsun, görevler TDD-friendly ve küçük parçalara bölünsün
- `obsidian-markdown`: frontmatter geçerli kalsın, wikilink yapısı net olsun, vault içi bağlantılar Obsidian uyumlu yazılsın

### Araştırma kaynaklı kararlar

Web araştırmasının planı etkileyen iki ana sonucu:

- episodic memory için olay düğümleri + temporal ilişkiler ilk sınıf olmalı
- entity ve event’in aynı düğümde ezilmesi yerine ayrı yüzeyler olarak korunması daha güvenli

Bu nedenle H7 frontmatter’ında `primary_entities`, `primary_events` ve `temporal_relations` zorunlu tutulmalı; projection bu yapıdan dual-graph türetmeli.

## Verification Steps

### Kod ve test düzeyi

1. `tests/test_brain_growth_h7_builder.py` fail etmeli, sonra geçmeli
2. `tests/test_brain_growth_validator.py` içine H7 kapsamı eklendiğinde fail etmeli, sonra geçmeli
3. `tests/test_brain_growth_layered_projection.py` içine `hidden_7` ve `temporal_dual_graph` assertion’ları eklenmeli, önce fail sonra pass doğrulanmalı

### Çalıştırma düzeyi

1. H7 builder gerçek notları üretmeli
2. validator raporu `h7` kind’ını göstermeli
3. remediation map yeni temporal/entity-event repair class’larını desteklemeli
4. projection JSON ve Markdown `hidden_7` ile `temporal_dual_graph` alanlarını göstermeli

### Integrity düzeyi

1. full brain-growth pytest suite temiz geçmeli
2. validator `status: pass` üretmeli
3. forbidden reference count artmamalı
4. `LokumAI-1.0.md` hash’i değişmemeli

### Başarı ölçütü

Wave 7 başarıyla tamamlanmış sayılırsa:

- 4 adet `H7_*` note üretilmiştir
- validator `h7` sayımlarını ve temporal remediation mantığını gösterir
- projection `hidden_7` ve `temporal_dual_graph` export eder
- H6 davranışı regress etmez
- vault merkezi kuralı bozulmaz

## Source Notes

- Current project state: `docs/superpowers/specs/2026-08-30-hidden6-executive-layout-design.md`
- Current validator state: `docs/brain_growth/reports/brain_growth_validation.txt`
- Current projection state: `docs/brain_growth/projections/brain_growth_layered_projection.md`
- Research references:
  - `https://arxiv.org/pdf/2606.15778`
  - `https://arxiv.org/html/2506.05939v1`
