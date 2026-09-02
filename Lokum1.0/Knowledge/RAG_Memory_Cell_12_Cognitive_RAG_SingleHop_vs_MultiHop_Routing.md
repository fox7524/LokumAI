---
date: 2026-08-30
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#rag/graph_rag"
---

# Cognitive RAG SingleHop vs MultiHop Routing

## Teknik çekirdek

Her sorguya graph traversal uygulamak optimal değildir. Empirik olarak single-hop bilgi erişimi isteyen görevlerde klasik RAG veya vector retrieval çoğu zaman yeterli olur; graph tabanlı retrieval'in maliyeti burada gereksiz olabilir.

Multi-hop reasoning, ilişki zinciri, komşuluk semantiği veya belgeler arası bağ gerektiren görevlerde ise graph-based retrieval öne çıkar. Buradaki kazanç yalnızca daha fazla belge getirmek değil, hangi düğümün hangi ilişki üzerinden bağlandığını retrieval kararına sokmaktır.

Cognitive RAG routing bu yüzden soru tipini sınıflandırmalıdır: düz olgusal erişim, zincirleme nedensellik, entity-link traversal veya topolojik açıklama. Routing katmanı, graph yürütmeyi yalnızca çok-adımlı veya yapı bağımlı sorgularda tetiklemelidir.

## Doğrulanmış bulgular

- Vanilla RAG single-hop görevlerde yeterli olabilir.
- Graph-based retrieval multi-hop ve yapı bağımlı görevlerde öne çıkar.
- Asıl karar sorunun biçimidir; her güçlü retriever her görev için ekonomik değildir.
- Cognitive RAG, query complexity'yi routing sinyaline çevirmelidir.

## LokumAI için çıkarım

Bu hücre, LokumAI'nin ileri beslemeli bilişsel graph'ında hangi sorgunun hangi katmana yönlendirileceğini belirleyen politika notudur. Basit lookup ile zincirleme reasoning aynı retrieval yolunu izlememelidir.

## Sorgu ipuçları

- `single hop vs multi hop`
- `graph retrieval routing`
- `query complexity`
- `cognitive rag policy`

## Kaynaklar

- https://arxiv.org/html/2607.28397v1

[[Causal_Inference_Engine]]
[[Sequence_Alignment]]
[[Temporal_Pattern_Recognition]]
