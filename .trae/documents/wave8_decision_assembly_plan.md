# Wave 8 Decision Assembly Plan

## Summary

Wave 8 için en doğru kapsam, LokumAI `brain_growth` zincirine resmi bir `hidden_8_decision_assembly` katmanı eklemektir. Bu katman, `hidden_7` episodic-temporal belleğin ürettiği olay ve ilişki örüntülerini doğrudan execution'a çevirmeye çalışmayacak; bunun yerine sistemin o anki baskın karar çekirdeğini seçen, aday policy setini assemble eden ve seçilmiş policy’yi aşağı akış yüzeylerine broadcast eden üst seviye karar montaj katmanı olacaktır.

Bu dalga yine mevcut proje desenini korumalıdır:

1. semantic vault içinde gerçek `H8_*.md` düğümleri
2. validator içinde H8 doğrulama ve remediation mantığı
3. projection içinde `hidden_8` görünürlüğü ve türetilmiş `workspace_broadcast_graph`

Amaç runtime executor kurmak değil, semantic model + validation + export yüzeyini güvenli şekilde büyütmektir.

## Current State Analysis

Mevcut `brain_growth` mimarisi şu resmi katmanları first-class olarak destekliyor:

- `raw`
- `hidden_3`
- `hidden_4`
- `hidden_5`
- `hidden_6`
- `hidden_7`
- `index`

Projedeki builder/validator/projection üçlüsü artık katman bazlı sabit bir desene oturmuş durumda:

- `tools/brain_growth/common.py` yeni resmi layer discovery noktasıdır
- `tools/brain_growth/h7_builder.py` en güncel builder kalıbıdır
- `tools/brain_growth/quality_validator.py` katman bazlı kalite, remediation ve delta mantığını taşır
- `tools/brain_growth/layered_projection.py` resmi katman görünürlüğü, transition sayımı ve türetilmiş graph exportlarını üretir

Güncel durumdan çıkarılan ana sonuçlar:

- H6 orchestration düzeyini temsil ediyor
- H7 episodic-temporal reasoning düzeyini temsil ediyor
- H7 projection tarafında `temporal_dual_graph` ile entity/event/temporal edge ayrımını görünür hale getiriyor
- Sistem henüz “hangi episodik örüntü şu an baskın policy’ye dönüşmeli” sorusunu resmi bir katman olarak modellemiyor

Repo içinde eski `layer/hidden_8_decision_assembly` etiketli legacy notlar var, ancak bunlar yeni `brain_growth` standardına uymuyor:

- dosya adları `H8_*.md` resmi kalıbında değil
- quoted frontmatter ve builder family disiplini taşımıyor
- validator ve projection kapsamına resmi olarak dahil edilmeleri semantic çakışma yaratır

Bu yüzden Wave 8’in tasarımında legacy hidden_8 içerikleri “ilham veya downstream hedef” olarak görülebilir; fakat resmi H8 discovery kapsamına dahil edilmemelidir.

Araştırma yönü de bu katmanı destekliyor:

- episodic memory, belirsiz ve feature-rich ortamlarda esnek karar vermeyi destekleyen ayrıntılı olay geri çağırımı sağlar
- global workspace benzeri yaklaşımlar, yarışan bilişsel adaylar arasından baskın içeriğin seçilip sistem geneline broadcast edilmesini vurgular

Bu iki fikir birlikte okunduğunda, H7’den sonra doğru üst soyutlama “decision assembly + dominant policy broadcast” katmanıdır.

## Proposed Changes

### 1. Yeni semantic katman: `hidden_8_decision_assembly`

#### Dosyalar

- `tools/brain_growth/common.py`
- `tools/brain_growth/h8_builder.py`
- `tests/test_brain_growth_h8_builder.py`
- `Lokum1.0/Knowledge/H8_Dominant_Thoughtseed_Selection.md`
- `Lokum1.0/Knowledge/H8_Global_Policy_Broadcast.md`
- `Lokum1.0/Knowledge/H8_Decision_Commitment_Gate.md`
- `Lokum1.0/Knowledge/H8_Exception_Override_Arbitration.md`

#### Ne değişecek

`common.py` içine `discover_hidden_8_targets()` eklenecek ve `allowed_forward_targets()` resmi H8 setini tanıyacak. Yeni `h8_builder.py`, H7 builder desenini koruyarak dört adet gerçek `H8_*.md` karar montaj düğümü üretecek.

Her `H8_*` notu aşağıdaki zorunlu shape’i taşıyacak:

- quoted YAML frontmatter
- `#layer/hidden_8_decision_assembly`
- `#workspace/global_broadcast`
- `#decision/dominant_thoughtseed`
- `#policy/assembly`
- `workspace_mode`
- `dominant_thoughtseed`
- `candidate_policies`
- `broadcast_targets`

Önerilen zorunlu section başlıkları:

- `## Karar montaj amacı`
- `## Dominant thoughtseed sinyalleri`
- `## Policy broadcast stratejisi`
- `## Commitment kuralları`
- `## Besleyen H7 düğümleri`
- `## Yayınlanan çıktı yolları`

#### Neden

H7 olayların sırasını ve entity-event bağlarını temsil ediyor, fakat karar seçim/broadcast katmanını henüz oluşturmuyor. Wave 8, H7’den gelen temporal-episodic örüntüyü “hangi policy şu an baskın olmalı ve nereye yayınlanmalı” biçimine taşıyarak bilişsel grafı bir seviye daha soyutlayacak.

#### Nasıl

TDD ile ilerlenmeli:

1. `tests/test_brain_growth_h8_builder.py` içinde fail eden H8 discovery/render/write testleri yazılmalı
2. `discover_hidden_8_targets()` ve `allowed_forward_targets()` genişletilmeli
3. `H8Family` veri yapısı tanımlanmalı
4. deterministic render, target verification ve `run_checks()` mantığı eklenmeli
5. dört gerçek `H8_*` notu üretilmeli

Bu dalgada önerilen H8 aileleri:

- `H8_Dominant_Thoughtseed_Selection.md`
- `H8_Global_Policy_Broadcast.md`
- `H8_Decision_Commitment_Gate.md`
- `H8_Exception_Override_Arbitration.md`

### 2. Validator genişletmesi: H8 validation + workspace remediation

#### Dosyalar

- `tools/brain_growth/quality_validator.py`
- `tests/test_brain_growth_validator.py`
- `docs/brain_growth/reports/brain_growth_validation.json`
- `docs/brain_growth/reports/brain_growth_validation.txt`

#### Ne değişecek

Validator artık `H8_*.md` notlarını da resmi katman olarak tarayacak. `REPORT_KIND_ORDER` içine `h8` eklenecek. `H8_REQUIRED_SECTIONS`, `h8_note_paths()`, `supported_workspace_modes()` ve `validate_h8_note()` tanımlanacak.

Yeni issue code aileleri:

- `invalid_workspace_mode`
- `missing_dominant_thoughtseed`
- `missing_candidate_policy`
- `missing_broadcast_target`
- `missing_h7_input`
- `missing_policy_broadcast_strategy`
- `missing_commitment_rule`

Yeni remediation class aileleri:

- `workspace_frontmatter_repair`
- `policy_broadcast_repair`
- `decision_commitment_repair`
- `family_spec_alignment_repair`

#### Neden

H8 ile birlikte kalite riski artık yalnız section eksikliği değil; dominant thoughtseed, policy adayları, broadcast hedefleri ve commitment mantığının bozulması da kritik hale gelecek. Validator bunu özel hata kodlarıyla görünür hale getirmelidir.

#### Nasıl

Validator, H8 frontmatter ve body içeriğini parse ederek en az şu metrikleri üretmeli:

- `h7_inputs`
- `candidate_policy_count`
- `broadcast_target_count`
- `downstream_output_count`
- `wikilink_count`

`--fix` bu dalgada H8 semantics’ini uydurmamalı; yalnızca yapısal, güvenli düzeltmelerle sınırlı kalmalı. Eksik semantic alanlar raporlanmalı, otomatik doldurulmamalıdır.

### 3. Projection genişletmesi: `hidden_8` ve `workspace_broadcast_graph`

#### Dosyalar

- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_layered_projection.py`
- `docs/brain_growth/projections/brain_growth_layered_projection.json`
- `docs/brain_growth/projections/brain_growth_layered_projection.md`

#### Ne değişecek

`LAYER_ORDER` içine `hidden_8` eklenecek. H8 düğümleri mevcut positional layout modeline dahil edilecek. Ayrıca projection payload’ına türetilmiş bir `workspace_broadcast_graph` bölümü eklenecek.

Bu bölüm en az şu alanları taşımalı:

- `thoughtseed_nodes`
- `policy_nodes`
- `selection_edges`
- `broadcast_edges`

Her selection edge içinde decision ilişki tipi açıkça bulunmalı; her broadcast edge içinde hedef ve kaynak policy net görünmelidir.

#### Neden

H7’de `temporal_dual_graph` ile episodik yapı dışa vuruldu. Wave 8 için de karar montajının projection seviyesinde görünür hale gelmesi gerekir. Bu, hem görsel okunabilirliği artırır hem de ileride policy/runtime motoruna geçiş için güvenli bir ara yüz sağlar.

#### Nasıl

İlk sürümde thoughtseed veya policy ayrı Obsidian notları olmayacak. Bunun yerine H8 frontmatter alanlarından projection sırasında türetilmiş `workspace_broadcast_graph` üretilecek. Böylece dosya patlaması olmadan karar montajı modeli sisteme alınır.

Projection testleri en az şunları doğrulamalı:

- `hidden_8` katmanı `LAYER_ORDER` içinde görünmeli
- `hidden_7_to_hidden_8` transition üretilebilmeli
- `workspace_broadcast_graph.thoughtseed_nodes` boş olmamalı
- `workspace_broadcast_graph.policy_nodes` boş olmamalı
- `selection_edges` relation alanı taşımalı
- `broadcast_edges` hedef yayınları içermeli

### 4. Artifact refresh ve integrity pass

#### Dosyalar

- `docs/brain_growth/reports/brain_growth_validation.json`
- `docs/brain_growth/reports/brain_growth_validation.txt`
- `docs/brain_growth/projections/brain_growth_layered_projection.json`
- `docs/brain_growth/projections/brain_growth_layered_projection.md`

#### Ne değişecek

Full `brain_growth` test paketi çalıştırılacak, sonra H8 builder, validator ve projection artefact’ları yenilenecek.

#### Neden

H8, mevcut H7-H6 zincirinin üstüne bindiği için regresyon riski yüksektir. Artifact refresh yalnız çıktı üretmek için değil, yeni karar montaj katmanının önceki reasoning/orchestration/episodic katmanları bozmadığını göstermek için de gereklidir.

#### Nasıl

Son integrity pass şu noktaları açıkça doğrulamalı:

- validator `h8` kind sayımlarını göstermeli
- projection’da `hidden_8` görünmeli
- `workspace_broadcast_graph` dolu gelmeli
- remediation map gereksiz semantic uydurma yapmamalı
- `LokumAI-1.0.md` untouched kalmalı

## Assumptions & Decisions

### Ana karar

Wave 8, runtime decision executor veya gerçek policy engine kurmayacak. Bu dalga yalnız semantic layer + validator + projection iskeletini açacaktır.

### Legacy hidden_8 kararı

Mevcut repoda eski `layer/hidden_8_decision_assembly` notları bulunuyor. Bu dalgada resmi layer discovery yalnız `H8_*.md` pattern’i ile çalışmalıdır. Legacy notlar validator/projection’ın resmi H8 kapsamına dahil edilmeyecek.

### Girdi seviyesi kararı

H8 düğümleri H6’dan değil H7’den beslenmelidir. Çünkü bu katmanın amacı orchestration’ı tekrarlamak değil, episodik-temporal örüntülerden karar montajı yapmaktır.

### Export kararı

Wave 8’in projection çıktısında yeni derived graph adı `workspace_broadcast_graph` olacaktır. Bu graph thoughtseed ve policy seviyesini dışa vuracak, ama ayrı vault notları üretmeyecektir.

### Skill kaynaklı kararlar

Bu plan aşağıdaki skill desenleriyle hizalanmıştır:

- `brainstorming`: tek wave kapsamı, design-first, gereksiz subsystem genişlemesini reddet
- `writing-plans`: file map açık olsun, görevler küçük ve TDD-friendly parçalara ayrılsın
- `obsidian-markdown`: frontmatter geçerli kalsın, wikilink yapısı vault uyumlu olsun

### Kullanılmayan skill kararı

Bu aşamada `agent-browser`, `data-analysis`, `consulting-analysis`, `obsidian-bases`, `obsidian-cli` ve ismi eşleşmeyen `report-generator-skill` Wave 8 planı için gerekli değildir. Gerekirse sonraki alt görevlerde devreye alınabilirler; fakat bu dalganın çekirdeği builder/validator/projection + Obsidian note disiplinidir.

## Verification Steps

### Kod ve test düzeyi

1. `tests/test_brain_growth_h8_builder.py` fail etmeli, sonra geçmeli
2. `tests/test_brain_growth_validator.py` içine H8 kapsamı eklendiğinde önce fail etmeli, sonra geçmeli
3. `tests/test_brain_growth_layered_projection.py` içine `hidden_8` ve `workspace_broadcast_graph` assertion’ları eklenmeli, önce fail sonra pass doğrulanmalı

### Çalıştırma düzeyi

1. H8 builder gerçek notları üretmeli
2. validator raporu `h8` kind’ını göstermeli
3. remediation map yeni workspace/policy repair class’larını desteklemeli
4. projection JSON ve Markdown `hidden_8` ile `workspace_broadcast_graph` alanlarını göstermeli

### Integrity düzeyi

1. full `brain_growth` pytest paketi temiz geçmeli
2. validator `status: pass` üretmeli
3. forbidden reference count artmamalı
4. `LokumAI-1.0.md` değişmemeli

### Başarı ölçütü

Wave 8 başarıyla tamamlanmış sayılırsa:

- 4 adet `H8_*` note üretilmiştir
- validator `h8` sayımlarını ve workspace remediation mantığını gösterir
- projection `hidden_8` ve `workspace_broadcast_graph` export eder
- H7 davranışı regress etmez
- legacy hidden_8 içerikleri resmi katman kapsamını bozmaz
- vault merkezi kuralı korunur
