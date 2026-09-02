---
title: "LokumAI hidden_5 + projection metrics/layout design"
date: "2026-08-30"
status: approved
---

# Goal

Extend the current LokumAI cognitive graph beyond `hidden_4` by adding:

1. a real `hidden_5` metacognitive control / arbitration layer
2. validator-side before/after delta reporting for graph-health changes
3. projection-side spatial layout scoring and domain clustering

# Current state

The project already has:

- `raw` memory cells
- `H3` synthesis nodes
- `H4` reasoning / convergence nodes
- validator v2 with `H4` validation, metrics, and safe `--fix`
- layered projection export with layer counts and transition counts

This means the graph is already structured, but one more level of explicit control is still missing.

# Problem

Three gaps remain:

## 1. Missing control layer

`H4` can converge evidence, but it does not yet model:

- policy arbitration
- reflection gating
- conflict resolution between reasoning branches
- escalation vs compression decisions

That belongs in `hidden_5`.

## 2. Missing metric deltas

The validator reports current health, but not change over time.
Without deltas, it is harder to tell whether a regeneration improved or degraded the graph.

## 3. Missing visual quality signals

The projection exports layer counts and edges, but not whether the layout is:

- clustered cleanly by domain
- balanced by layer
- visually dense or noisy

# Architecture decision

Use the same dual-model strategy as before:

## Semantic graph

The Obsidian vault remains the source of truth.
New `H5_*` notes become real semantic nodes in the vault.

## Derived projection

Projection remains computed from the vault.
New layout metrics and domain clusters are derived views, not authoritative structure.

# hidden_5 design

## Purpose

`hidden_5` is the metacognitive arbitration layer.
It does not summarize facts and does not merely combine topics.
Instead, it decides which reasoning route should dominate when multiple `H4` nodes compete.

## hidden_5 responsibilities

- choose between competing reasoning policies
- detect when the system should escalate vs compress
- arbitrate risk vs performance vs recall trade-offs
- stabilize downstream control decisions

## First hidden_5 families

The first iteration should stay compact:

- `H5_Metacognitive_Policy_Arbitration.md`
- `H5_Risk_Performance_Tradeoff_Control.md`
- `H5_Retrieval_Depth_Governance.md`
- `H5_Global_Escalation_Gate.md`

## hidden_5 note shape

Each `H5_*` note must include:

- quoted YAML frontmatter
- `#layer/hidden_5_metacognitive_control`
- `## Kontrol amacı`
- `## Arbitration sinyalleri`
- `## Karar politikası`
- `## Besleyen H4 düğümleri`
- `## Yönettiği çıktı yolları`

Each note must consume multiple `H4_*` nodes.

# Validator extension

## New support

Validator must learn:

- `H5` note discovery
- `H5` section validation
- `H5` input/output link checks
- new graph metrics for `h5`

## Delta reporting

Validator should compare:

- current report
- previous saved report

And emit:

- count deltas by node kind
- edge/link deltas where available
- issue delta
- compliance delta

The output should be informative but safe: read-only comparison, no hidden mutation.

# Projection extension

## Domain clustering

Projection should group nodes into domain clusters based on existing tag-derived domain labels.

Expected outputs:

- cluster membership by node
- node counts by cluster
- per-layer cluster distribution

## Spatial layout scoring

Projection should compute heuristic scores such as:

- layer balance score
- cluster coherence score
- cross-cluster edge pressure
- visual density score
- left-to-right readability score

These are descriptive metrics, not exact geometry.

# File strategy

Likely implementation files:

- `tools/brain_growth/h5_builder.py`
- `tests/test_brain_growth_h5_builder.py`
- `tools/brain_growth/quality_validator.py`
- `tests/test_brain_growth_validator.py`
- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_layered_projection.py`
- new `Lokum1.0/Knowledge/H5_*.md`

# Order

The next execution wave should run in this order:

1. build `H5`
2. extend validator with `H5` and delta reporting
3. extend projection with clustering and layout scores
4. refresh reports and projection artifacts

# Success criteria

This wave is successful if:

- `H5` exists as a real metacognitive layer
- validator reports `h5` counts and change deltas
- projection reports clusters and layout-quality metrics
- no forbidden node references are introduced
- `LokumAI-1.0.md` remains untouched
