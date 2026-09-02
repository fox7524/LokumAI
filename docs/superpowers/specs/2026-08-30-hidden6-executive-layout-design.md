---
title: "LokumAI hidden_6 + executive layout design"
date: "2026-08-30"
status: approved
---

# Goal

Extend the current LokumAI cognitive graph beyond `hidden_5` by adding:

1. a real `hidden_6` executive orchestration / long-horizon planning layer
2. validator-side remediation mapping and `hidden_6` graph-health support
3. projection-side positional layout export with deterministic layer slots

# Current state

The project already has:

- `raw` memory cells
- `H3` synthesis nodes
- `H4` reasoning / convergence nodes
- `H5` metacognitive control nodes
- validator reporting with deltas
- layered projection with domain clustering and layout-quality scores

This means the graph can now arbitrate reasoning, but it still lacks a true execution-orchestration tier.

# Problem

Three gaps remain:

## 1. Missing executive layer

`H5` can choose policies, but it does not yet model:

- long-horizon sequencing
- global execution ordering
- orchestration of retrieval, recovery, and response branches
- executive coordination across multiple metacognitive decisions

That belongs in `hidden_6`.

## 2. Missing remediation map

The validator can report issues and deltas, but it does not yet map issue classes to recommended remediation families.

## 3. Missing positional layout export

The projection can score visual quality, but it still lacks deterministic node slotting:

- stable layer columns
- stable within-layer ordering
- exportable positional coordinates

# Architecture decision

Use the same dual-model strategy:

## Semantic graph

The Obsidian vault remains the source of truth.
New `H6_*` notes become real semantic nodes in the vault.

## Derived projection

Projection remains computed from the vault.
Positional layout metadata is a derived presentation layer, not semantic truth.

# hidden_6 design

## Purpose

`hidden_6` is the executive orchestration layer.
It turns `H5` policy/control outputs into orchestrated multi-step execution priorities.

## hidden_6 responsibilities

- sequence long-horizon responses
- coordinate retrieval and action pathways
- choose escalation ordering
- manage recovery flow priorities

## First hidden_6 families

- `H6_Executive_Priority_Orchestration.md`
- `H6_Retrieval_Action_Coordination.md`
- `H6_Global_Response_Orchestration.md`
- `H6_Recovery_Execution_Sequencing.md`

## hidden_6 note shape

Each `H6_*` note must include:

- quoted YAML frontmatter
- `#layer/hidden_6_executive_orchestration`
- `## Orkestrasyon amacı`
- `## Yürütücü sinyaller`
- `## Orkestrasyon politikası`
- `## Besleyen H5 düğümleri`
- `## Koordine ettiği çıktı yolları`

Each note must consume multiple `H5_*` nodes.

# Validator extension

Validator must learn:

- `H6` note discovery
- `H6` section validation
- `H6` input/output link checks
- graph metrics for `h6`
- remediation-map generation for issue families

The remediation map should translate validator issue codes into recommended repair classes without mutating notes automatically.

# Projection extension

Projection should add deterministic positional metadata:

- layer column index
- slot index within layer
- cluster-aware ordering key
- stable `x/y` coordinates for exported nodes

This should make the exported graph closer to the reference neural-network visuals instead of a drifting blob.

# File strategy

Likely implementation files:

- `tools/brain_growth/h6_builder.py`
- `tests/test_brain_growth_h6_builder.py`
- `tools/brain_growth/quality_validator.py`
- `tests/test_brain_growth_validator.py`
- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_layered_projection.py`
- new `Lokum1.0/Knowledge/H6_*.md`

# Order

The next execution wave should run in this order:

1. build `H6`
2. extend validator with `H6` and remediation mapping
3. extend projection with positional layout export
4. refresh reports and projection artifacts

# Success criteria

This wave is successful if:

- `H6` exists as a real executive orchestration layer
- validator reports `h6` counts and remediation hints
- projection exports deterministic layout positions
- no forbidden node references are introduced
- `LokumAI-1.0.md` remains untouched
