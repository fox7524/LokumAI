# Bilişsel RAG Bellek Hücresi Entegrasyon Planı

> **Ajanik yürütücüler için:** `writing-plans` disipliniyle dosya düzeyinde kararları uygula, `executing-plans` disipliniyle blokaj çıkarsa dur ve kullanıcıya dön. Bu plan onaylanmadan uygulamaya geçme.

## Özet

`Lokum1.0/Knowledge` içinde, mevcut topolojiyi bozmadan en az 10 değil, doğrudan 12 adet yüksek yoğunluklu `RAG_Memory_Cell_*.md` notu üret. Her not Obsidian Flavored Markdown kullanacak, quoted YAML frontmatter taşıyacak, derin teknik içerik içerecek, dosya sonunda yalnızca ve tam 3 adet uygun `hidden_1` veya `hidden_2` düğümüne wikilink verecek, `LokumAI-1.0.md` dosyasına hiçbir şekilde bağlanmayacak.

Bu plan doğrudan not üretimini seçer; ayrı bir kalıcı script veya yardımcı dosya oluşturmaz. Gerekirse uygulama sırasında geçici doğrulama mantığı geçici çalışma alanında kullanılabilir, ancak kullanıcı klasörüne yalnızca final `.md` düğümleri yazılır.

## Mevcut Durum Analizi

### Vault topolojisi

`Lokum1.0/Knowledge/LokumAI-1.0.md` dosyası ağ sözlüğü olarak açıkça `orphan` tanımlanmış; burada `#layer/input`, `#layer/hidden_1_feature_extraction`, `#layer/hidden_2_pattern_recognition`, `#layer/hidden_3_logic_synthesis`, `#layer/hidden_4_decision_making`, `#layer/output`, ayrıca `#rag/memory_cell`, `#rag/training`, `#hardware/apple_mlx`, `#hardware/esp32`, `#system/crypto` etiket sözlüğü bulunuyor. Bu dosya mevcut tasarım gereği ne linklenecek ne değiştirilecek.

`Knowledge` klasöründe `hidden_1` ve `hidden_2` havuzu fiilen mevcut. İnceleme sonucunda:

- `hidden_1` tarafında örnek düğümler: `Zero_Copy_Buffer_Analysis.md`, `DRAM_Bandwidth_Utilization.md`, `Data_Prefetch_Evaluation.md`, `Instruction_Fetch_Analysis.md`, `Pointer_Authentication_Check.md`, `Memory_Leak_Fingerprinting.md`, `Packet_Header_Parsing.md`.
- `hidden_2` tarafında örnek düğümler: `Graph_Neural_Network_Embeddings.md`, `Topology_Analysis.md`, `Node2Vec_Mapping.md`, `Cross_Correlation_Matrix.md`, `Temporal_Pattern_Recognition.md`, `Probabilistic_Graphical_Models.md`, `Causal_Inference_Engine.md`.

### Mevcut not kalitesi

Okunan örnekler `Zero_Copy_Buffer_Analysis.md`, `Pointer_Authentication_Check.md`, `Graph_Neural_Network_Embeddings.md`, `Attention_Head_1.md`, `Topology_Analysis.md` biçimsel olarak basit ve içerik olarak sığ. Genellikle:

- tek katman etiketi var
- `#rag/memory_cell` ve `#rag/training` yok
- gerçek kaynak atfı yok
- çok sayıda genel bağlantı kullanılıyor
- teknik ayrıntı yerine şablon cümleler bulunuyor

Yeni üretilecek notlar bu kalite açığını kapatmalı; mevcut düğümleri düzenlemek yerine, yeni yüksek yoğunluklu bellek hücreleri eklenmeli.

## Araştırma Temeli

Plan şu doğrulanmış dış kaynaklara dayanır:

1. MLX unified memory dokümantasyonu, Apple silicon üzerinde dizilerin shared memory’de yaşadığını; işlemlerin veri kopyalamadan CPU veya GPU stream’lerinde çalıştırılabildiğini; scheduler’ın akış bağımlılıklarını yönettiğini söylüyor. [$TRAE_REF](https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html)
2. MLX dönüşüm dokümantasyonu, Metal tabanlı DLPack alışverişinde zero-copy’nin yalnızca private olmayan Metal buffer durumunda mümkün olduğunu; private buffer’ların kopyaya düştüğünü belirtiyor. [$TRAE_REF](https://ml-explore.github.io/mlx/build/html/usage/numpy.html)
3. Metal buffer dokümantasyonu, `MTLBuffer` kaynaklarının `storageMode` ile yönetildiğini ve `storageModeShared` ile `storageModePrivate` ayrımının gerçek performans/topoloji etkisi taşıdığını gösteriyor. [$TRAE_REF](https://developer.apple.com/documentation/metal/buffers?changes=_6)
4. ESP-IDF FreeRTOS dokümantasyonu, ESP hedeflerinde dual-core SMP, core affinity, `xTaskCreatePinnedToCore()`, tick sorumluluklarının core bazlı ayrımı ve scheduler davranış farklarını açıkça tanımlıyor. [$TRAE_REF](https://docs.espressif.com/projects/esp-idf/en/v5.3.5/esp32p4/api-reference/system/freertos_idf.html)
5. ESP-IDF interrupt allocation dokümantasyonu, shared interrupt’ların yalnızca level-triggered kullanılabileceğini, interrupt tahsisinin tahsis eden core’a bağlı olduğunu ve IRAM-safe ISR gereksinimlerini net biçimde açıklıyor. [$TRAE_REF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/intr_alloc.html)
6. ESP-IDF heap/dma dokümantasyonu, DMA için `MALLOC_CAP_DMA` gerektiğini, ISR içinde heap çağrılarının teorik olarak mümkün ama kuvvetle önerilmediğini ve pre-allocation yaklaşımının tercih edilmesi gerektiğini söylüyor. [$TRAE_REF](https://docs.espressif.com/projects/esp-idf/en/v5.2.7/esp32s3/api-reference/system/mem_alloc.html)
7. Apple platform security dokümantasyonu, Pointer Authentication Codes’un bellek bozulması kaynaklı code-pointer saldırılarını zorlaştırmak için kullanıldığını ve M5 nesline kadar Apple SoC çizgisinde koruma ailesinin sürdüğünü gösteriyor. [$TRAE_REF](https://support.apple.com/en-ca/guide/security/sec8b776536b/web)
8. GLM-RAG makalesi, vanilla RAG’ın single-hop senaryolarda yeterli olabildiğini; graph-based retrieval’ın multi-hop görevlerde güçlendiğini; GLM retriever’ın semantik + graph yapıyı birlikte işlediğini; GNN retriever’ın ise graph coverage’da avantajlı olabildiğini ortaya koyuyor. [$TRAE_REF](https://arxiv.org/html/2607.28397v1)

## Skill Uyum Notları

Yürütme şu yüklenmiş skill kurallarıyla uyumlu olmalı:

- `brainstorming`
  - tasarımı uygulamadan önce netleştir
  - ağ topolojisine zarar verecek serbest linkleme yapma
- `writing-plans`
  - dosya bazlı kararları önceden sabitle
  - belirsiz “uygun node seç” gibi boşluk bırakma
  - doğrulamayı planın içine göm
- `obsidian-markdown`
  - quoted frontmatter kullan
  - vault içi bağlantılarda yalnızca wikilink kullan
  - external kaynaklarda standart URL kullan
- `obsidian-cli`
  - uygulama sonrası backlink ve tag doğrulaması için kullanılabilir
- `executing-plans`
  - uygulama sırasında doğrulama bozulursa dur
  - `LokumAI-1.0.md` blacklist kuralı kırılırsa devam etme

## Önerilen Değişiklikler

### Ortak not şeması

#### Dosyalar

- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_01_MLX_Unified_Memory_Model.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_02_MLX_Zero_Copy_DLPack_and_Buffer_Reusage.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_03_Metal_Shared_vs_Private_StorageMode.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_07_P2P_Encryption_and_ZKP_Constraint_Surface.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_08_Apple_PAC_Runtime_Integrity.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_09_Memory_Safety_Primitives_and_Failure_Signatures.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_10_GNN_Message_Passing_for_Graph_Retrieval.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_11_GLM_RAG_Semantic_Graph_Fusion.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_12_Cognitive_RAG_SingleHop_vs_MultiHop_Routing.md`

#### Ne

Tüm yeni notlar aynı OMF-benzeri iskeleti izleyecek:

1. quoted YAML frontmatter
2. H1 başlık
3. `## Teknik çekirdek`
4. `## Doğrulanmış bulgular`
5. `## LokumAI için çıkarım`
6. `## Sorgu ipuçları`
7. sonda yalnızca 3 adet wikilink

#### Neden

Bu, retrieval kalitesini artırır; notlar hem insan tarafından okunabilir hem de daha sonra graph traversal mantığı için düzenli anchor görevi görür.

#### Nasıl

Her not için şu frontmatter zorunludur:

```yaml
---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "<konuya_uygun_tag>"
---
```

Ek kararlar:

- `#` içeren YAML değerleri daima quoted olacak.
- Gövde içinde ek wikilink kullanılmayacak.
- Kaynak URL’leri gövdede düz markdown link veya çıplak URL olarak verilebilir.
- Dosya sonunda tam 3 non-empty line wikilink olacak.
- `[[LokumAI-1.0]]` veya `[[LokumAI-1.0.md]]` hiçbir yerde bulunmayacak.

### 1. Apple Silicon ve MLX notları

#### Dosyalar

- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_01_MLX_Unified_Memory_Model.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_02_MLX_Zero_Copy_DLPack_and_Buffer_Reusage.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_03_Metal_Shared_vs_Private_StorageMode.md`

#### Ne

Apple Silicon M5 Pro UMA, MLX shared memory, zero-copy sınırlamaları ve Metal storage mode ayrımı için üç ayrı bellek hücresi oluştur.

#### Neden

Bu alanlar kullanıcı isteğinin çekirdeğinde ve mevcut notlar bunları yalnızca isim düzeyinde geçiyor; gerçek buffer reuse, stream bağımlılığı ve storage mode farkları henüz temsil edilmiyor.

#### Nasıl

`RAG_Memory_Cell_01_MLX_Unified_Memory_Model.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#hardware/apple_mlx"`
- içerik:
  - MLX array’lerinin unified memory’de yaşaması
  - CPU/GPU stream’inde kopyasız çalıştırma modeli
  - scheduler dependency insertion mantığı
- final wikilinks:
  - `[[Zero_Copy_Buffer_Analysis]]`
  - `[[DRAM_Bandwidth_Utilization]]`
  - `[[Data_Prefetch_Evaluation]]`

`RAG_Memory_Cell_02_MLX_Zero_Copy_DLPack_and_Buffer_Reusage.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#hardware/apple_mlx"`
- içerik:
  - DLPack ile framework geçişi
  - private olmayan Metal buffer’da zero-copy
  - private buffer geldiğinde kopya zorunluluğu
  - gradient görünürlüğü ve external memory mutation riski
- final wikilinks:
  - `[[Zero_Copy_Buffer_Analysis]]`
  - `[[Token_Embedding_Generator]]`
  - `[[Cross_Correlation_Matrix]]`

`RAG_Memory_Cell_03_Metal_Shared_vs_Private_StorageMode.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#hardware/apple_mlx"`
- içerik:
  - `MTLBuffer`
  - `storageModeShared` ve `storageModePrivate`
  - resource locality ve dispatch etkisi
- final wikilinks:
  - `[[L1_Cache_Hit_Ratio]]`
  - `[[L2_Cache_Hit_Ratio]]`
  - `[[Zero_Copy_Buffer_Analysis]]`

### 2. ESP32 ve gömülü sistem notları

#### Dosyalar

- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md`

#### Ne

ESP32/ESP-IDF alanını üç ayrı hücreye böl: SMP/affinity, interrupt allocation, DMA+ISR memory disiplini.

#### Neden

Bu ayırım yapılmazsa FreeRTOS, hardware interrupts ve DMA tek bir kaba notta karışır; retrieval tarafında sinyal ayrımı kaybolur.

#### Nasıl

`RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#hardware/esp32"`
- içerik:
  - dual-core SMP farkları
  - `xTaskCreatePinnedToCore()`
  - `tskNO_AFFINITY`
  - scheduler ve tick sorumluluğu
- final wikilinks:
  - `[[Behavioral_Feature_Mapping]]`
  - `[[Temporal_Pattern_Recognition]]`
  - `[[Cross_Correlation_Matrix]]`

`RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#hardware/esp32"`
- içerik:
  - `esp_intr_alloc()`
  - shared vs non-shared interrupt
  - shared interrupt’ta yalnızca level-triggered kullanım
  - core on allocation / free symmetry
  - IRAM-safe ISR koşulları
- final wikilinks:
  - `[[Instruction_Fetch_Analysis]]`
  - `[[Branch_Prediction_Modeling]]`
  - `[[Temporal_Pattern_Recognition]]`

`RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#hardware/esp32"`
- içerik:
  - `MALLOC_CAP_DMA`
  - external PSRAM hariç DMA-capable memory
  - ISR’de heap çağrılarının neden önerilmediği
  - pre-allocation ve fixed buffer stratejisi
- final wikilinks:
  - `[[Packet_Header_Parsing]]`
  - `[[DRAM_Bandwidth_Utilization]]`
  - `[[Memory_Leak_Fingerprinting]]`

### 3. Kriptografi ve bellek güvenliği notları

#### Dosyalar

- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_07_P2P_Encryption_and_ZKP_Constraint_Surface.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_08_Apple_PAC_Runtime_Integrity.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_09_Memory_Safety_Primitives_and_Failure_Signatures.md`

#### Ne

Kriptografi ve memory safety tarafını üç hücreye böl: P2P+ZKP bağlamı, Apple PAC, düşük seviye failure signatures.

#### Neden

Kullanıcı yalnızca PAC değil, daha geniş güvenlik/kriptografi temalarını da istedi. PAC bypass ifadesini spekülatif exploit dili yerine doğrulanabilir primitive ve failure-mode diliyle ele almak daha doğru.

#### Nasıl

`RAG_Memory_Cell_07_P2P_Encryption_and_ZKP_Constraint_Surface.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#system/crypto"`
- içerik:
  - P2P encryption pipeline yüzeyleri
  - ZKP’nin state disclosure azaltma rolü
  - donanım/veri yolu düzeyinde hangi sinyallerin exposure yarattığı
  - bu başlığın “constraint surface” olarak konumlanması
- final wikilinks:
  - `[[Cryptographic_Entropy_Analysis]]`
  - `[[Probabilistic_Graphical_Models]]`
  - `[[Causal_Inference_Engine]]`

`RAG_Memory_Cell_08_Apple_PAC_Runtime_Integrity.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#system/crypto"`
- içerik:
  - PAC’ın code pointer koruması
  - memory corruption mitigasyonu
  - Apple silicon runtime integrity bağlamı
  - exploit-by-pass dili yerine primitive odaklı anlatım
- final wikilinks:
  - `[[Pointer_Authentication_Check]]`
  - `[[Stack_Smash_Detection]]`
  - `[[Heap_Overflow_Heuristics]]`

`RAG_Memory_Cell_09_Memory_Safety_Primitives_and_Failure_Signatures.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#system/crypto"`
- içerik:
  - bellek güvenliği primitive’leri
  - invalid pointer / crash signature düşüncesi
  - PAC ile stack smash / heap overflow arasında ayrım
  - hangi telemetry pattern’lerinin retrieval’de güvenlik sinyali sayılacağı
- final wikilinks:
  - `[[Pointer_Authentication_Check]]`
  - `[[Instruction_Fetch_Analysis]]`
  - `[[Heap_Overflow_Heuristics]]`

### 4. GNN ve Cognitive RAG notları

#### Dosyalar

- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_10_GNN_Message_Passing_for_Graph_Retrieval.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_11_GLM_RAG_Semantic_Graph_Fusion.md`
- Create `Lokum1.0/Knowledge/RAG_Memory_Cell_12_Cognitive_RAG_SingleHop_vs_MultiHop_Routing.md`

#### Ne

AI tarafında üç hücre oluştur: message passing retriever mantığı, GLM-RAG semantik+graph fusion, single-hop vs multi-hop routing kararı.

#### Neden

Kullanıcının hedefi sıradan RAG değil, Cognitive Graph RAG. Bu yüzden sadece “GNN vardır” notu yetmez; retrieval politikasını belirleyen farklar belleğe ayrı hücreler olarak yazılmalı.

#### Nasıl

`RAG_Memory_Cell_10_GNN_Message_Passing_for_Graph_Retrieval.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#rag/graph_rag"`
- içerik:
  - query-conditioned message passing
  - graph coverage avantajı
  - semantics açısından sınırlılık
- final wikilinks:
  - `[[Graph_Neural_Network_Embeddings]]`
  - `[[Node2Vec_Mapping]]`
  - `[[Topology_Analysis]]`

`RAG_Memory_Cell_11_GLM_RAG_Semantic_Graph_Fusion.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#rag/graph_rag"`
- içerik:
  - GLM’in graph transformer + LM birleşimi
  - token düzeyinde text-attributed graph işleme
  - GNN retriever’a göre semantik avantaj
- final wikilinks:
  - `[[Graph_Neural_Network_Embeddings]]`
  - `[[Probabilistic_Graphical_Models]]`
  - `[[Topology_Analysis]]`

`RAG_Memory_Cell_12_Cognitive_RAG_SingleHop_vs_MultiHop_Routing.md`
- tags:
  - `"#rag/memory_cell"`
  - `"#rag/training"`
  - `"#rag/graph_rag"`
- içerik:
  - vanilla RAG single-hop yeterliliği
  - graph-based retrieval’ın multi-hop üstünlüğü
  - Cognitive RAG’da ne zaman graph traversal tetikleneceği
- final wikilinks:
  - `[[Causal_Inference_Engine]]`
  - `[[Sequence_Alignment]]`
  - `[[Temporal_Pattern_Recognition]]`

## Varsayımlar ve Kararlar

- Uygulama aşamasında mevcut notlar değiştirilmeyecek; yalnızca yeni `RAG_Memory_Cell_*.md` dosyaları oluşturulacak.
- `date` alanı uygulama gününde güncellenebilir; plan örneğinde bugün için `2026-08-30` kullanıldı.
- `#rag/graph_rag` etiketi sözlük dosyasında sayılmıyor, ancak hiyerarşik tag mantığıyla geçerli ve içerik için uygundur. İstenirse uygulama sırasında bu alan `#rag/embedding` ile değiştirilmeyecek; `#rag/graph_rag` korunacak çünkü ayrım semantik olarak önemlidir.
- “PAC bypass” başlığı doğrudan exploit tarifi üretmeyecek; doğrulanabilir runtime integrity, primitive ve failure-mode çerçevesinde yazılacak.
- P2P encryption ve ZKP için not, dış araştırma ile desteklenecek; bu başlıkta resmi vendor doc bulunamazsa akademik/teknik kaynak kullanılabilir fakat içerik yine savunmacı ve mimari düzeyde kalacaktır.
- Gövde içinde wikilink kullanılmaması bilinçli karardır; böylece “tam 3 link” kuralı deterministik kalır.
- Uygulama yöntemi doğrudan dosya yazımıdır; kullanıcı klasörüne script bırakılmayacak.

## Doğrulama Adımları

Uygulama bittiğinde şu kontroller yapılmalı:

1. `Knowledge` içinde `RAG_Memory_Cell_*.md` ile başlayan tam 12 yeni dosya bulunduğunu doğrula.
2. Her yeni dosyada frontmatter’ın `---` ile başlayıp bittiğini doğrula.
3. Her yeni dosyada şu tag’lerin bulunduğunu doğrula:
   - `"#rag/memory_cell"`
   - `"#rag/training"`
   - konuya uygun üçüncü tag
4. Her yeni dosyada `[[LokumAI-1.0]]` ve `[[LokumAI-1.0.md]]` geçmediğini doğrula.
5. Her yeni dosyada toplam wikilink sayısının tam 3 olduğunu doğrula.
6. Her yeni dosyada son 3 non-empty line’ın wikilink olduğunu doğrula.
7. Bu 3 linkin gerçekten mevcut `hidden_1` veya `hidden_2` dosyalarına gittiğini doğrula.
8. Her yeni dosyada yüzeysel placeholder cümle olmadığını, en az şu bölümlerin bulunduğunu doğrula:
   - `## Teknik çekirdek`
   - `## Doğrulanmış bulgular`
   - `## LokumAI için çıkarım`
   - `## Sorgu ipuçları`
9. En az bir Apple/MLX, bir ESP-IDF, bir PAC/security, bir Graph RAG kaynağının içerik içinde anıldığını doğrula.
10. İsteğe bağlı olarak Obsidian/backlink tarafında yeni notların link ağına katıldığını, fakat `LokumAI-1.0.md` dosyasının orphan kaldığını kontrol et.
