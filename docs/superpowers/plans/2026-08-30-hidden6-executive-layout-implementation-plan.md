# Hidden 6 Executive Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a real `hidden_6` executive orchestration layer, extend validator reporting with `h6` support and remediation mapping, and enrich layered projection exports with deterministic positional layout metadata.

**Architecture:** Reuse the existing brain-growth toolchain. `H6_*` notes become real vault nodes, `quality_validator.py` learns how to validate them and attach remediation guidance, and `layered_projection.py` derives stable positional metadata from the semantic graph without redefining semantic truth.

**Tech Stack:** Python 3, Markdown/Obsidian notes, `pytest`, existing `tools/brain_growth/*` modules

---

## File map

- Create: `tools/brain_growth/h6_builder.py`
- Create: `tests/test_brain_growth_h6_builder.py`
- Modify: `tools/brain_growth/common.py`
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`
- Modify: `tools/brain_growth/layered_projection.py`
- Modify: `tests/test_brain_growth_layered_projection.py`
- Create: `Lokum1.0/Knowledge/H6_Executive_Priority_Orchestration.md`
- Create: `Lokum1.0/Knowledge/H6_Retrieval_Action_Coordination.md`
- Create: `Lokum1.0/Knowledge/H6_Global_Response_Orchestration.md`
- Create: `Lokum1.0/Knowledge/H6_Recovery_Execution_Sequencing.md`
- Modify: `docs/brain_growth/reports/brain_growth_validation.json`
- Modify: `docs/brain_growth/reports/brain_growth_validation.txt`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.md`

### Task 1: Extend shared layer helpers and add H6 builder

**Files:**
- Modify: `tools/brain_growth/common.py`
- Create: `tools/brain_growth/h6_builder.py`
- Create: `tests/test_brain_growth_h6_builder.py`
- Create: `Lokum1.0/Knowledge/H6_Executive_Priority_Orchestration.md`
- Create: `Lokum1.0/Knowledge/H6_Retrieval_Action_Coordination.md`
- Create: `Lokum1.0/Knowledge/H6_Global_Response_Orchestration.md`
- Create: `Lokum1.0/Knowledge/H6_Recovery_Execution_Sequencing.md`

- [ ] **Step 1: Write failing tests for hidden_6 discovery and note generation**
- [ ] **Step 2: Run the focused pytest commands and verify failure**
- [ ] **Step 3: Add `discover_hidden_6_targets()` to `tools/brain_growth/common.py` and include it in `allowed_forward_targets()`**
- [ ] **Step 4: Create `tools/brain_growth/h6_builder.py` with fixed section headers, target verification, CLI, and four real H6 families**
- [ ] **Step 5: Generate the four real `H6_*.md` notes**
- [ ] **Step 6: Re-run `tests/test_brain_growth_h6_builder.py` and verify pass**

### Task 2: Extend validator with H6 support and remediation mapping

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write failing tests for `validate_h6_note()` and remediation mapping**
- [ ] **Step 2: Run the focused pytest commands and verify failure**
- [ ] **Step 3: Add `H6_REQUIRED_SECTIONS`, `h6_note_paths()`, `validate_h6_note()`, and `h6` counts to report building**
- [ ] **Step 4: Add remediation-map generation from validator issue codes**
- [ ] **Step 5: Render remediation hints in JSON and text reports**
- [ ] **Step 6: Re-run `tests/test_brain_growth_validator.py` and verify pass**

### Task 3: Extend projection with positional layout export

**Files:**
- Modify: `tools/brain_growth/layered_projection.py`
- Modify: `tests/test_brain_growth_layered_projection.py`

- [ ] **Step 1: Write failing tests for `hidden_6` layer support and positional metadata**
- [ ] **Step 2: Run the focused pytest commands and verify failure**
- [ ] **Step 3: Extend projection collection to include `H6_*.md` and update `LAYER_ORDER`**
- [ ] **Step 4: Compute deterministic slot indices and stable `x/y` export coordinates**
- [ ] **Step 5: Re-run `tests/test_brain_growth_layered_projection.py` and verify pass**

### Task 4: Refresh artifacts and run full integrity checks

**Files:**
- Modify: `docs/brain_growth/reports/brain_growth_validation.json`
- Modify: `docs/brain_growth/reports/brain_growth_validation.txt`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.md`

- [ ] **Step 1: Run the full brain-growth pytest suite**
- [ ] **Step 2: Regenerate `H6` notes, validator reports, and projection outputs**
- [ ] **Step 3: Sanity-check generated JSON outputs**
- [ ] **Step 4: Confirm `LokumAI-1.0.md` remained untouched**

## Self-review

- Spec coverage:
  - `hidden_6` is covered by Task 1.
  - validator `h6` support and remediation mapping are covered by Task 2.
  - positional layout export is covered by Task 3.
  - artifact refresh and integrity verification are covered by Task 4.
- Placeholder scan:
  - no placeholder tokens remain in the plan body.
- Type consistency:
  - `discover_hidden_6_targets()`, `validate_h6_note()`, remediation mapping, and positional export fields are named consistently across tasks.
