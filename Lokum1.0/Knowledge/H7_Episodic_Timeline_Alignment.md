---
date: "2026-08-30"
tags:
  - "#layer/hidden_7_episodic_temporal_memory"
  - "#memory/episodic"
  - "#reasoning/temporal"
  - "#graph/entity_event_dual"
  - "#memory/timeline_alignment"
episode_mode: "ordered_episode_reconstruction"
temporal_relations:
  - "before"
  - "after"
  - "overlaps_with"
primary_entities:
  - "executive_queue"
  - "retrieval_budget"
  - "response_plan"
primary_events:
  - "priority_shift"
  - "evidence_lock"
  - "execution_release"
---

# Episodic Timeline Alignment

## Episodik amaç

Bu episodik düğüm, H6 seviyesinde ayrı yürütülen kararların hangi sırayla yaşandığını tek bir zaman çizgisinde hizalar.

Amaç, executive öncelik değişimleri ile retrieval-to-action geçişlerinin aynı epizod içinde yeniden kurulabilmesini sağlamaktır.

## Zamansal sinyaller

- Aynı olay ailesi içinde önce kanıt toplama sonra eylem montajı sonra execution açılışı gözleniyorsa
- H6 karar sırası farklı çevrimlerde kayıyor ve post-hoc analiz zaman çizgisini tutarlı kuramıyorsa
- Bir epizodun kritik anları response planı ile queue önceliği arasında dağılmış görünüyorsa

## Temporal edge politikası

- Timeline rekonstrüksiyonu için before/after ilişkileri varsayılan kenar ailesi olarak tutulur.
- Eşzamanlı ama bağımlı adımlar overlaps_with kenarı ile bağlanır; salt aynı çevrimde görünmeleri yeterli sayılmaz.
- Execution release ancak upstream evidence_lock olayı açıkça bağlanabiliyorsa aynı epizoda dahil edilir.

## Entity-event bağlama stratejisi

- Entity bağları, queue, budget ve response planı gibi durum taşıyan öğeleri epizodun sabit aktörleri olarak işler.
- Event bağları, bu aktörlerin durum değiştirdiği priority_shift, evidence_lock ve execution_release anlarına sabitlenir.
- Bağlama stratejisi, aynı entity'nin birden çok event içindeki rolünü zaman çizgisi sıra bilgisiyle korur.

## Besleyen H6 düğümleri

- [[H6_Executive_Priority_Orchestration]]
- [[H6_Retrieval_Action_Coordination]]

## Hafıza çıktıları

- [[Episodic_Memory_Consolidation]]
- [[Semantic_Graph_Weaver]]
- [[Time_Series_Smoothing]]
