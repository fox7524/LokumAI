---
date: 2026-08-30
tags:
  - "#layer/hidden_6_executive_orchestration"
  - "#executive/retrieval_action_coordination"
  - "#domain/cognitive_graph_rag"
---

# Retrieval Action Coordination

## Orkestrasyon amacı

Bu düğüm, retrieval derinliği ve politika seçimi ile üretilen kararların hangi eylem çıktısına ne zaman dönüştürüleceğini orkestre eder.

Amaç, semantic graph toplama maliyetini gerçek yanıt montajı ile dengeleyip gereksiz veri genişlemesini nihai execution yoluna taşımamaktır.

## Yürütücü sinyaller

- Retrieval tarafı daha fazla kanıt isterken yanıt montajı karar eşiğine ulaşmış görünüyorsa
- Yeni kanıtlar planı anlamlı biçimde değiştirmiyor ama execution paketleme maliyeti artıyorsa
- Graph tabanlı bağlam ile kullanıcıya verilecek yanıt formatı arasında gecikme ve tutarlılık baskısı oluşuyorsa

## Orkestrasyon politikası

- Cevap kararlılığı korunuyorsa yeni retrieval dalı açmak yerine mevcut kanıtların execution paketlemesi tercih edilir.
- Semantic drift sinyali yükselirse finalizer yalnız doğrulanmış altgrafı downstream aksiyona taşır.
- Nihai eylem kapısı yalnız retrieval genişlemesinin marjinal katkısı düştüğünde açılır.

## Besleyen H5 düğümleri

### Hidden_5 executive girdileri

- [[H5_Retrieval_Depth_Governance]]
- [[H5_Metacognitive_Policy_Arbitration]]

### Executive orchestration anchor düğümleri

- [[Semantic_Graph_Weaver]]
- [[Cognitive_RAG_Finalizer]]

## Koordine ettiği çıktı yolları

- [[Executive_Action_Formatter]]
- [[Cognitive_Response_Generator]]
- [[Final_Execution_Gate]]
