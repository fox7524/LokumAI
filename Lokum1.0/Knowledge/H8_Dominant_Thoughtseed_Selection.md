---
date: "2026-08-30"
tags:
  - "#layer/hidden_8_decision_assembly"
  - "#workspace/global_broadcast"
  - "#decision/dominant_thoughtseed"
  - "#policy/assembly"
  - "#workspace/thoughtseed_selection"
workspace_mode: "dominant_policy_broadcast"
dominant_thoughtseed: "recovery_first_consensus"
candidate_policies:
  - "stabilize_consensus_before_execution"
  - "minimize_regret_under_risk"
broadcast_targets:
  - "Executive_Action_Formatter"
  - "Final_Execution_Gate"
---

# Dominant Thoughtseed Selection

## Karar montaj amacı

Bu düğüm, H7 episodik örüntüler içinden o anki baskın karar çekirdeğini seçer.

Amaç, temporal recall ve recency governance çıktılarından tek bir dominant thoughtseed üretmektir.

## Dominant thoughtseed sinyalleri

- Aynı epizod ailesi birden çok çevrimde aynı karar önceliğini tekrar ediyorsa
- Recency drift kontrolü kısa vadeli gürültüyü baskılayıp kalıcı örüntüyü öne çıkarıyorsa
- Execution öncesi hangi policy'nin baskın olması gerektiği açık biçimde ayrışıyorsa

## Policy broadcast stratejisi

- Dominant thoughtseed önce aday policy setini sıralar, sonra en yüksek uyumlu policy'yi yayınlar.
- Broadcast yalnız doğrulanmış episodik örüntülerden beslenir; tekil gürültü sinyalleri seçimi belirlemez.

## Commitment kuralları

- Dominant thoughtseed en az iki episodik sinyal tarafından desteklenmeden sabitlenmez.
- Recency baskısı tek başına policy seçimi yapamaz; temporal tutarlılık da aranır.

## Besleyen H7 düğümleri

- [[H7_Episodic_Timeline_Alignment]]
- [[H7_Recency_Drift_Governance]]
## Yayınlanan çıktı yolları


- [[Global_State_Consensus]]
- [[Episodic_Memory_Consolidation]]
