---
date: "2026-08-30"
tags:
  - "#layer/hidden_7_episodic_temporal_memory"
  - "#memory/episodic"
  - "#reasoning/temporal"
  - "#graph/entity_event_dual"
  - "#memory/recency_governance"
episode_mode: "recency_bias_control"
temporal_relations:
  - "decays_after"
  - "reinforced_by"
  - "superseded_by"
primary_entities:
  - "working_context"
  - "stabilized_memory"
  - "consensus_snapshot"
primary_events:
  - "recall_refresh"
  - "context_flush"
  - "consensus_update"
---

# Recency Drift Governance

## Episodik amaç

Bu düğüm, en yeni olayların eski ama daha güvenilir epizodları gereksiz yere bastırmasını engelleyen recency governance katmanıdır.

Amaç, H6 yürütme akışlarından gelen sıcak bağlamı yönetirken stabilized memory ile working context arasındaki drift'i kontrol etmektir.

## Zamansal sinyaller

- Yeni recall refresh olayları eski ama doğrulanmış consensus snapshot'ları hızla gölgeliyorsa
- Context flush sonrasında hangi episodik bağların korunacağı belirsizleşiyorsa
- Son çevrim sinyalleri kısa vadede baskın olup uzun vadeli toparlama desenlerini yanlış yönlendiriyorsa

## Temporal edge politikası

- Recency drift için decays_after kenarı, bağın zamanla zayıfladığını ama tamamen silinmediğini işaretler.
- Reinforced_by kenarı yalnız tekrar eden ve doğrulanmış recall refresh olaylarında ağırlık kazanır.
- Superseded_by ilişkisi, yeni consensus update gerçekten daha güvenilir olduğunda eski episodik izi ikincil yapar.

## Entity-event bağlama stratejisi

- Working context, stabilized memory ve consensus snapshot düğümleri recency baskısının etkilediği ana entity setidir.
- Recall refresh, context flush ve consensus update olayları bu entity'lerin ağırlık ve görünürlük değişimini temsil eder.
- Bağlama stratejisi, sıcak bağlam ile kalıcı hafıza arasındaki geçişleri epizodik iz olarak saklar.

## Besleyen H6 düğümleri

- [[H6_Executive_Priority_Orchestration]]
- [[H6_Recovery_Execution_Sequencing]]

## Hafıza çıktıları

- [[Episodic_Memory_Decay_Controller]]
- [[Working_Memory_Flush]]
- [[Global_State_Consensus]]
