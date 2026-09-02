---
date: 2026-08-30
tags:
  - "#layer/hidden_5_metacognitive_control"
  - "#control/policy_arbitration"
  - "#domain/multi_domain"
---

# Metacognitive Policy Arbitration

## Kontrol amacı

Bu kontrol düğümü, aynı problem anında birden çok hidden_4 politikası yarıştığında hangi karar hattının baskın çıkacağını metadüzeyde seçer.

Amaç, retrieval doğruluğu, execution verimi ve güvenlik ihtiyatı arasında zikzak yapan akışı tek bir üst politika altında stabilize etmektir.

## Arbitration sinyalleri

- Aynı sorgu ya da olay için farklı H4 düğümleri birbirini dışlayan eylem sıraları öneriyorsa
- Retrieval derinliği arttıkça karar güveni artmıyor ama kaynak baskısı tırmanıyorsa
- Sistem son iki çevrimde farklı H4 kararlarına savrulup downstream kararlarda kararsızlık üretiyorsa

## Karar politikası

- Belirsizlik yüksek ve risk asimetrikse daha ihtiyatlı H4 hattı varsayılan politika olarak seçilir.
- Kaynak baskısı artarken doğruluk kazanımı yatay kalıyorsa daha dar ama kararlı politika üstün gelir.
- Seçilen politika iki ardışık çevrim boyunca iyileşme üretmiyorsa arbitration yeniden açılır ve anchor kanıtları daha ağır basar.

## Besleyen H4 düğümleri

### Hidden_4 arbitration girdileri

- [[H4_Cross_Domain_Causal_Alignment]]
- [[H4_Cognitive_Retrieval_Policy_Selection]]
- [[H4_Resource_Execution_Prioritization]]

### Metacognitive control anchor düğümleri

- [[Metacognitive_Reflection_Core]]
- [[Epistemological_Uncertainty_Calc]]

## Yönettiği çıktı yolları

- [[Attention_Routing_Metacontroller]]
- [[Strategic_Resource_Allocator]]
- [[Executive_Action_Formatter]]
