# Hidden 5 Metrics Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a real `hidden_5` metacognitive control layer, extend validator reporting with `h5` and before/after deltas, and enrich layered projection exports with domain clustering and layout-quality scores.

**Architecture:** Reuse the existing brain-growth toolchain instead of branching it. `H5_*` notes become real vault nodes, `quality_validator.py` learns how to validate and compare graph-health snapshots, and `layered_projection.py` keeps deriving presentation metrics from the semantic graph without redefining truth.

**Tech Stack:** Python 3, Markdown/Obsidian notes, `pytest`, existing `tools/brain_growth/*` modules

---

## File map

- Create: `tools/brain_growth/h5_builder.py`
- Create: `tests/test_brain_growth_h5_builder.py`
- Modify: `tools/brain_growth/common.py`
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`
- Modify: `tools/brain_growth/layered_projection.py`
- Modify: `tests/test_brain_growth_layered_projection.py`
- Create: `Lokum1.0/Knowledge/H5_Metacognitive_Policy_Arbitration.md`
- Create: `Lokum1.0/Knowledge/H5_Risk_Performance_Tradeoff_Control.md`
- Create: `Lokum1.0/Knowledge/H5_Retrieval_Depth_Governance.md`
- Create: `Lokum1.0/Knowledge/H5_Global_Escalation_Gate.md`
- Modify: `docs/brain_growth/reports/brain_growth_validation.json`
- Modify: `docs/brain_growth/reports/brain_growth_validation.txt`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.md`

### Task 1: Extend shared layer helpers and add H5 builder

**Files:**
- Modify: `tools/brain_growth/common.py`
- Create: `tools/brain_growth/h5_builder.py`
- Create: `tests/test_brain_growth_h5_builder.py`
- Create: `Lokum1.0/Knowledge/H5_Metacognitive_Policy_Arbitration.md`
- Create: `Lokum1.0/Knowledge/H5_Risk_Performance_Tradeoff_Control.md`
- Create: `Lokum1.0/Knowledge/H5_Retrieval_Depth_Governance.md`
- Create: `Lokum1.0/Knowledge/H5_Global_Escalation_Gate.md`

- [ ] **Step 1: Write failing tests for hidden_5 discovery and note generation**
- [ ] **Step 2: Run the focused pytest commands and verify failure**
- [ ] **Step 3: Add `discover_hidden_5_targets()` to `tools/brain_growth/common.py` and include it in `allowed_forward_targets()`**
- [ ] **Step 4: Create `tools/brain_growth/h5_builder.py` with `H5Family`, fixed section headers, target verification, CLI, and four real H5 families**
- [ ] **Step 5: Generate the four real `H5_*.md` notes**
- [ ] **Step 6: Re-run `tests/test_brain_growth_h5_builder.py` and verify pass**

### Task 2: Extend validator with H5 support and delta reporting

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write failing tests for `validate_h5_note()` and delta reporting**
- [ ] **Step 2: Run the focused pytest commands and verify failure**
- [ ] **Step 3: Add `H5_REQUIRED_SECTIONS`, `h5_note_paths()`, `validate_h5_note()`, and `h5` counts to report building**
- [ ] **Step 4: Add previous-report loading and delta calculation for file counts, issues, compliance, and wikilink totals**
- [ ] **Step 5: Render delta blocks in both JSON and text reports**
- [ ] **Step 6: Re-run `tests/test_brain_growth_validator.py` and verify pass**

### Task 3: Extend projection with domain clustering and layout-quality scores

**Files:**
- Modify: `tools/brain_growth/layered_projection.py`
- Modify: `tests/test_brain_growth_layered_projection.py`

- [ ] **Step 1: Write failing tests for `hidden_5` layer support, domain clusters, and layout scores**
- [ ] **Step 2: Run the focused pytest commands and verify failure**
- [ ] **Step 3: Extend projection collection to include `H5_*.md` and update `LAYER_ORDER`**
- [ ] **Step 4: Compute domain cluster summaries and per-layer cluster spread**
- [ ] **Step 5: Compute heuristic layout scores for balance, density, cross-cluster pressure, and readability**
- [ ] **Step 6: Re-run `tests/test_brain_growth_layered_projection.py` and verify pass**

### Task 4: Refresh artifacts and run full integrity checks

**Files:**
- Modify: `docs/brain_growth/reports/brain_growth_validation.json`
- Modify: `docs/brain_growth/reports/brain_growth_validation.txt`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.md`

- [ ] **Step 1: Run the full brain-growth pytest suite**
- [ ] **Step 2: Regenerate `H5` notes, validator reports, and projection outputs**
- [ ] **Step 3: Sanity-check generated JSON outputs**
- [ ] **Step 4: Confirm `LokumAI-1.0.md` remained untouched**

## Self-review

- Spec coverage:
  - `hidden_5` is covered by Task 1.
  - validator `h5` support and delta reporting are covered by Task 2.
  - projection clustering and layout scores are covered by Task 3.
  - artifact refresh and integrity verification are covered by Task 4.
- Placeholder scan:
  - no placeholder tokens remain in the plan body.
- Type consistency:
  - `discover_hidden_5_targets()`, `validate_h5_note()`, delta reporting, and projection cluster/score outputs are named consistently across tasks.
