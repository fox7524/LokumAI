---
date: "2026-08-30"
tags:
  - "#layer/hidden_7_episodic_temporal_memory"
  - "#memory/episodic"
  - "#reasoning/temporal"
  - "#graph/entity_event_dual"
  - "#memory/causal_recall"
episode_mode: "causal_episode_recall"
temporal_relations:
  - "causes"
  - "preceded_by"
  - "resolved_by"
primary_entities:
  - "response_branch"
  - "recovery_window"
  - "strategic_plan"
primary_events:
  - "incident_escalation"
  - "recovery_gate_open"
  - "plan_revision"
---

# Temporal Causal Recall

## Episodik amaç

Bu düğüm, geçmiş epizodlardan neden-sonuç zinciri çıkararak hangi olay dizisinin stratejik planı değiştirdiğini hatırlatır.

Amaç, response branch ve recovery sequencing ilişkisini sırf anlık state olarak değil zamansal causal recall olarak depolamaktır.

## Zamansal sinyaller

- Incident escalation sonrası recovery gate açılışı ile plan revision arasındaki sıra anlamlı fark yaratıyorsa
- Benzer olaylar farklı sonuçlar üretiyor ve kritik farkın temporal order olduğu düşünülüyorsa
- Geçmiş response zinciri geri çağrılmadan yeni stratejik plan güvenle sabitlenemiyorsa

## Temporal edge politikası

- Causal recall içinde causes ve resolved_by kenarları, salt korelasyondan daha güçlü kanıt istediği için ayrı tutulur.
- Plan revision bir closure event olarak yalnız ilgili recovery window tamamlandıktan sonra resolved_by kenarı alır.
- Preceded_by ilişkisi, incident escalation ile recovery gate open arasındaki minimal zaman düzenini korur.

## Entity-event bağlama stratejisi

- Response branch ve strategic plan gibi entity'ler, epizod boyunca etkilenip yeniden yapılandırılan sürekli öğelerdir.
- Incident escalation, recovery gate open ve plan revision olayları bu entity'ler üstündeki dönüşümü zamanlı işaretler.
- Bağlama stratejisi, recall sırasında hangi event'in hangi entity durumunu değiştirdiğini nedensel sırayla geri çağırır.

## Besleyen H6 düğümleri

- [[H6_Global_Response_Orchestration]]
- [[H6_Recovery_Execution_Sequencing]]

## Hafıza çıktıları

- [[Episodic_Memory_Consolidation]]
- [[Cognitive_Response_Generator]]
- [[Long_Term_Strategic_Planner]]
