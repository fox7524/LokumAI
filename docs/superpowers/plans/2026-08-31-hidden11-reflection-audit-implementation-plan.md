# Hidden 11 Reflection & Audit Implementation Plan

**Goal:** `hidden_11_reflection_audit` katmanını toolchain’e first-class eklemek: builder + validator + projection + H11 notları.

## File map

### Create

- `tools/brain_growth/h11_builder.py`
- `tests/test_brain_growth_h11_builder.py`
- `tests/test_brain_growth_h11_validator.py`
- `Lokum1.0/Knowledge/H11_Trace_Provenance_Attestation.md`
- `Lokum1.0/Knowledge/H11_Outcome_Regression_Postmortem.md`
- `Lokum1.0/Knowledge/H11_Rollback_Decision_Audit.md`
- `Lokum1.0/Knowledge/H11_Failsafe_Cost_Accounting.md`

### Modify

- `tools/brain_growth/common.py`
- `tools/brain_growth/quality_validator.py`
- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_layered_projection.py`

## Uygulama adımları

- [x] **Step 1: Builder + discovery RED/GREEN**
  - `discover_hidden_11_targets()` eklendi
  - `h11_builder.py` ile 4 H11 ailesi üretildi
- [x] **Step 2: Validator RED/GREEN**
  - `validate_h11_note()` eklendi
  - `REPORT_KIND_ORDER` içine `h11` eklendi
- [x] **Step 3: Projection RED/GREEN**
  - `LAYER_ORDER` içine `hidden_11` eklendi
  - `reflection_audit_graph` türetilmiş graph eklendi
- [ ] **Step 4: Repo-wide doğrulama**
  - `python3 -m pytest -q`
  - `python3 -m tools.brain_growth.quality_validator --scope all`

