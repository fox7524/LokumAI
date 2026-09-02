---
date: 2026-08-30
tags:
  - "#index/brain_growth"
  - "#domain/apple_silicon_mlx"
---

# Apple Silicon and MLX Index

## Alanlar

- Üst giriş: [[Brain_Growth_Index]]
- Alan sentezi: [[H3_Apple_Silicon_Memory_Execution_Synthesis]]
- Kapsam özeti: Apple Silicon, Metal ve MLX tarafındaki unified memory, dispatch yüzeyi ve execution darboğazlarını tek girişte toplar.

## Fazlar

### Faz 1 · Temsilci ham memory-cell girişleri

Temel girişler

- [[RAG_Memory_Cell_01_MLX_Unified_Memory_Model]]
- [[RAG_Memory_Cell_02_MLX_Zero_Copy_DLPack_and_Buffer_Reusage]]
- [[RAG_Memory_Cell_03_Metal_Shared_vs_Private_StorageMode]]

Orta katman kırılma noktaları

- [[RAG_Memory_Cell_17_Metal_Argument_Buffers_For_Batched_Dispatch_Coordination]]
- [[RAG_Memory_Cell_18_MPS_Versus_MLX_Execution_Surface_Selection]]

İleri hata ve optimizasyon yüzeyleri

- [[RAG_Memory_Cell_23_Sparse_Attention_On_Apple_Silicon_Memory_Budget]]
- [[RAG_Memory_Cell_24_Quantized_KV_Cache_Placement_On_UMA]]
- [[RAG_Memory_Cell_25_Metal_Resource_Hazard_Tracking_And_Explicit_Fencing]]
### Faz 2 · Hidden_3 sentez kapısı

- [[H3_Apple_Silicon_Memory_Execution_Synthesis]]
- Bu kapı, Apple Silicon and MLX alanındaki ham hücreleri mekanizma ailesine göre daraltır.
### Faz 4 · Kürasyon notu

- Toplam raw hücre: 16
- Bu sayfada görünen temsilci bağlantı: 8
- Görünmeyen 8 hücre, sentez kapısı ve etiket üzerinden açılır; bilinçli olarak tek sayfada omnidump yapılmaz.

## Kullanım

- Önce sentez kapısını açıp darboğaz ailesini ayır, sonra temsilci ham hücrelere in.
- Barrier, residency, queue-depth veya kernel fusion soruları bu girişten başlamalıdır.
