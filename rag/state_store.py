from __future__ import annotations

import hashlib
from typing import Any

from .chunker import chunk_text
from .normalize import normalize_text


def file_signature(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def build_file_state(source_path: str, raw_text: str, chunk_size: int, overlap: int) -> dict[str, Any]:
    chunks = chunk_text(raw_text, chunk_size=chunk_size, overlap=overlap)
    return {
        "source_path": source_path,
        "file_signature": file_signature(raw_text),
        "chunk_count": len(chunks),
        "chunk_signatures": [chunk.signature for chunk in chunks],
    }
