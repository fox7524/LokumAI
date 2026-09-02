---
title: "LokumAI Cognitive Brain Growth — phased architecture design"
date: "2026-08-30"
status: draft
---

# Goal

Grow `Lokum1.0/Knowledge` in a controlled, research-backed way without collapsing the current feed-forward graph into a spaghetti mesh.

This design expands the vault through four ordered sub-projects:

1. `50+` new research-grade memory-cell nodes with `200+` controlled forward synapses
2. topic-based `hidden_3` synthesis nodes
3. an automatic node quality validator
4. an index and navigation layer

The chosen direction is explicitly `A + C`:
- `A` controlled growth
- `C` phased growth

# Why phased growth

The user wants aggressive scale, but also wants real data, deep research, and topology discipline. Doing `50+ nodes + hidden_8 + validator + index` in one uncontrolled wave would create three risks:

- link explosion that damages retrieval quality
- inconsistent node quality across domains
- no reliable checkpoint to tell whether the graph is improving or merely getting bigger

The architecture therefore grows in layers:

- first raw research memory
- then synthesis
- then validation
- then navigation

This preserves signal quality while still allowing large expansion.

# Non-goals (for this growth cycle)

- Editing or linking `LokumAI-1.0.md`
- Rewriting the existing old node population en masse
- Building `hidden_4` through `hidden_8` immediately in the first execution cycle
- Replacing current graph semantics with free-form backlinks
- Creating speculative nodes without research grounding

`hidden_4` to `hidden_8` stay as future architecture targets, but this cycle only establishes the foundation needed to reach them safely.

# Current constraints

## Immutable center rule

`LokumAI-1.0.md` remains an orphan dictionary node:

- it is not modified
- it is not linked to
- it is not used as a synthesis or index hub

## Node format rule

All new raw research nodes are Obsidian Markdown files following:

- filename format: `RAG_Memory_Cell_[Specific_Topic].md`
- quoted YAML tags
- deep technical sections
- source-backed content
- exactly controlled forward links

## Topology rule

The current graph must remain feed-forward by policy:

- raw research nodes link upward into allowed downstream layers
- synthesis nodes aggregate lower-layer nodes
- validator reads graph state but does not create arbitrary semantic links
- index nodes navigate, but do not become an uncontrolled “supernode”

# Chosen architecture

## Phase 1 — Research node wave

Create at least `50` new memory-cell nodes in the user’s target domains, using deep research and bilingual dense writing where helpful.

Primary domains:

- Apple Silicon / MLX / Metal / UMA / zero-copy / dispatch
- embedded systems / ESP32 / FreeRTOS / interrupts / DMA
- security / cryptography / PAC / memory safety / P2P / ZKP
- AI / GNN / Graph RAG / Cognitive RAG / retrieval routing

### Phase 1 structure

Every new node includes:

- quoted YAML frontmatter
- technical core
- verified findings
- LokumAI inference
- query hints
- source section
- controlled forward wikilinks

### Phase 1 link policy

Each raw node must add only intentional upward links.

Minimum target:
- total new forward synapses across the wave: `200+`

Policy:
- no link to `LokumAI-1.0.md`
- no arbitrary cross-link storm
- no body-level wikilink sprawl if it weakens graph discipline
- links should favor meaningful ascent into feature extraction, pattern recognition, and later approved synthesis nodes

## Phase 2 — Topic-based hidden_3 synthesis

After enough raw memory exists, introduce synthesis nodes that sit conceptually above raw extraction/pattern notes.

These are not generic summaries. They are higher-order convergence nodes that:

- compress recurring patterns across multiple memory cells
- define topic-specific abstractions
- act as retrieval bridges into reasoning-oriented layers

Candidate synthesis families:

- `H3_Apple_Silicon_Memory_Execution_Synthesis`
- `H3_Embedded_Interrupt_DMA_Synthesis`
- `H3_Cryptographic_Integrity_and_Memory_Safety_Synthesis`
- `H3_Cognitive_Graph_RAG_Routing_Synthesis`

### Phase 2 rules

- each synthesis node must ingest multiple lower-layer notes
- each synthesis node must describe abstraction, invariants, and routing meaning
- synthesis nodes must not become encyclopedic dump files
- synthesis nodes should remain topic-bounded and composable

## Phase 3 — Automatic node quality validator

Introduce a validator that audits the growing vault for structural and content quality.

The validator’s job is to detect:

- missing or malformed frontmatter
- forbidden `LokumAI-1.0` references
- invalid link counts or invalid target layers
- missing required sections
- placeholder or shallow content
- poor source density
- layer-policy violations

### Validator outputs

The first version should report, not silently mutate.

Expected outputs:

- machine-readable report
- human-readable summary
- per-file quality findings
- pass/fail indicators for topology and content completeness

This creates a feedback loop before larger upper-layer expansion.

## Phase 4 — Index and navigation layer

Once raw nodes, synthesis nodes, and validation exist, add navigational structure.

This phase creates:

- one or more topic entry nodes
- a brain-growth index node
- navigation maps into the major research domains
- stable entrypoints for future `hidden_4+` growth

### Index rules

- index nodes organize, they do not absorb everything
- avoid one giant omnilinking file
- keep navigation domain-based
- preserve feed-forward semantics as much as practical

# Subagent execution model

The user explicitly wants this run with subagents in sequence.

Execution model:

1. subagent for Phase 1
2. subagent for Phase 2
3. subagent for Phase 3
4. subagent for Phase 4

Each phase should have:

- its own plan section
- its own verification gate
- its own completion report

This keeps the work autonomous while still reviewable.

# File strategy

## Phase 1 expected file classes

- create many files under `Lokum1.0/Knowledge/`
  - `RAG_Memory_Cell_*.md`

## Phase 2 expected file classes

- create synthesis files under `Lokum1.0/Knowledge/`
  - likely `H3_*.md` or a similarly explicit naming convention

## Phase 3 expected file classes

- create validator code in repository code area, not inside the user-facing vault as random scratch files
- create validator outputs in a predictable report location

## Phase 4 expected file classes

- create index and navigation nodes under `Lokum1.0/Knowledge/`

# Naming and layer policy

## Raw memory cells

Required:

- `RAG_Memory_Cell_[Specific_Topic].md`

## Synthesis nodes

Recommended:

- `H3_[Topic]_Synthesis.md`

This makes layer identity obvious at the filename level and simplifies validation.

# Research policy

All large node waves must be grounded in real sources.

Preferred source order:

1. official documentation
2. standards / specifications / vendor security docs
3. strong academic papers
4. technical engineering references

Disallowed quality pattern:

- filler nodes built from generic AI prose

Required quality pattern:

- concrete mechanisms
- technical terminology
- accurate architectural relations
- retrieval-relevant abstractions

# Success criteria

The design is successful if:

- Phase 1 adds `50+` new research-grade nodes
- the new wave introduces `200+` intentional forward synapses
- Phase 2 creates topic-bounded `hidden_3` synthesis nodes
- Phase 3 provides repeatable quality auditing
- Phase 4 adds usable index/navigation entrypoints
- `LokumAI-1.0.md` remains untouched and unlinked
- the graph becomes more navigable and more semantically useful, not merely larger

# Open decisions already resolved

- Growth style: controlled, not explosive
- Delivery model: phased, not one-shot
- Execution style: sequential subagents
- Architecture target: prepare for future `hidden_4+`, but do not fabricate it prematurely
- Priority order: `1 -> 2 -> 3 -> 4`
