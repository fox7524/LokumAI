---
date: "2026-08-30"
tags:
  - "#layer/hidden_7_episodic_temporal_memory"
  - "#memory/episodic"
  - "#reasoning/temporal"
  - "#graph/entity_event_dual"
  - "#memory/entity_binding"
episode_mode: "entity_event_binding"
temporal_relations:
  - "triggers"
  - "participates_in"
  - "co_occurs_with"
primary_entities:
  - "retrieval_path"
  - "threat_surface"
  - "consensus_state"
primary_events:
  - "graph_expansion"
  - "mitigation_decision"
  - "consensus_commit"
---

# Event Entity Binding

## Episodik amaç

Bu düğüm, aynı epizod içinde hangi entity'nin hangi event ile hangi bağlamda ilişkili olduğunu belirginleştirir.

Amaç, H6 response ve retrieval akışlarından gelen olayları dual-graph temsiline çevrilmeye hazır hale getirmektir.

## Zamansal sinyaller

- Graph expansion ile mitigation kararı aynı olay penceresinde birbirini etkiliyorsa
- Consensus commit, hangi retrieval path veya threat surface değişiminin sonucu olduğu belirsizleşiyorsa
- Entity'ler sabit kalıyor ama event bağları her çevrimde yeniden çözülüyorsa

## Temporal edge politikası

- Event-to-entity kenarları, yalnız nedensel ya da katılımsal bağ gerekçelendirilebildiğinde açılır.
- Sadece aynı anda görülme durumu, co_occurs_with kenarı dışında daha güçlü bağ üretmez.
- Consensus commit gibi kapanış event'leri upstream graph_expansion veya mitigation_decision olaylarına geriye dönük bağlanır.

## Entity-event bağlama stratejisi

- Retrieval path, threat surface ve consensus state düğümleri episode boyunca taşınan ana entity setidir.
- Graph expansion, mitigation decision ve consensus commit olayları bu entity'lerin zaman içindeki rol değişimlerini işaretler.
- Aynı event birden çok entity'ye bağlanıyorsa bağ türü ayrı tutulur ve dual-graph çakışması önlenir.

## Besleyen H6 düğümleri

- [[H6_Retrieval_Action_Coordination]]
- [[H6_Global_Response_Orchestration]]

## Hafıza çıktıları

- [[Ontological_Graph_Mapper]]
- [[Semantic_Graph_Weaver]]
- [[Episodic_Memory_Consolidation]]
