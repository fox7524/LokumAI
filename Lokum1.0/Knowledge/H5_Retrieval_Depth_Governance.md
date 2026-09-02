---
date: 2026-08-30
tags:
  - "#layer/hidden_5_metacognitive_control"
  - "#control/retrieval_depth_governance"
  - "#domain/cognitive_graph_rag"
---

# Retrieval Depth Governance

## Kontrol amacı

Bu düğüm, graph retrieval'ın ne kadar derine, ne kadar genişe ve hangi noktada durdurularak downstream bağlama teslim edileceğini yönetir.

Amaç, recall artışı ile semantic drift, latency ve context packing maliyeti arasındaki çizgiyi operasyonel biçimde sabitlemektir.

## Arbitration sinyalleri

- Derin graph traversal daha çok düğüm getiriyor ama cevap güveni belirgin şekilde artmıyorsa
- Bağlam paketleme baskısı yüzünden güçlü aday kanıtlar kırpılmaya başlıyorsa
- Retrieval genişlemesi farklı domain kümelerini karıştırıp semantik drift sinyali üretiyorsa

## Karar politikası

- Depth artışı önce kanıt çeşitliliği sonra cevap tutarlılığı üretmiyorsa arama erken kapatılır.
- Hallucination riski yükselirse daha sığ ama daha doğrulanabilir altgraf tercih edilir.
- Çapraz domain açıklama gerekiyorsa derinlik yalnız cluster geçişleri gerekçelendirilebildiğinde artırılır.

## Besleyen H4 düğümleri

### Hidden_4 arbitration girdileri

- [[H4_Cognitive_Retrieval_Policy_Selection]]
- [[H4_Cross_Domain_Causal_Alignment]]
- [[H4_Performance_Bottleneck_Disambiguation]]

### Metacognitive control anchor düğümleri

- [[Semantic_Drift_Detector]]
- [[Hallucination_Detection_Filter]]

## Yönettiği çıktı yolları

- [[Semantic_Graph_Weaver]]
- [[Cognitive_RAG_Finalizer]]
- [[Attention_Routing_Metacontroller]]
