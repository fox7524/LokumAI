---
date: "2026-08-31"
tags:
  - "#layer/input_rag"
  - "#rag/trace"
  - "#rag/link_binding"
trace_id: "sample_ui_export_001"
query: "Execution surface binding nasıl çalışıyor?"
rag_links:
  - "H9_Execution_Surface_Binding"
  - "H8_Global_Policy_Broadcast"
  - "H11_Trace_Provenance_Attestation"
---

# RAG Trace sample_ui_export_001

## Sorgu

Execution surface binding nasıl çalışıyor?

## RAG bağları (rag_links)

- [[H9_Execution_Surface_Binding]]
- [[H8_Global_Policy_Broadcast]]
- [[H11_Trace_Provenance_Attestation]]

## Skorlar (distance)

- H9_Execution_Surface_Binding: 0.920000
- H8_Global_Policy_Broadcast: 0.880000
- H11_Trace_Provenance_Attestation: 0.830000

## Ham trace (kısaltılmış)

```json
{
  "trace_id": "sample_ui_export_001",
  "query": "Execution surface binding nasıl çalışıyor?",
  "sources": [
    {
      "source_path": "Lokum1.0/Knowledge/H9_Execution_Surface_Binding.md",
      "file_id": "demo"
    },
    {
      "source_path": "Lokum1.0/Knowledge/H8_Global_Policy_Broadcast.md",
      "file_id": "demo"
    },
    {
      "source_path": "Lokum1.0/Knowledge/H11_Trace_Provenance_Attestation.md",
      "file_id": "demo"
    }
  ],
  "distances": [
    0.92,
    0.88,
    0.83
  ],
  "count": 3
}
```
