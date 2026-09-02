# Hidden 10 Strategic Supervision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-class `hidden_10_strategic_supervision` layer that supervises H9 execution packages, extends validator coverage, and exports a derived `strategic_supervision_graph`.

**Architecture:** Keep H9 focused on execution packaging and add H10 as a distinct strategic-oversight layer. Extend the existing `brain_growth` pattern consistently: discovery in `common.py`, deterministic note generation in `h10_builder.py`, H10-specific validation in `quality_validator.py`, and derived supervision graph export in `layered_projection.py`.

**Tech Stack:** Python 3, Obsidian Markdown, `pytest`, existing `brain_growth` builder/validator/projection modules.

---

## File map

### Create

- `tools/brain_growth/h10_builder.py`
- `tests/test_brain_growth_h10_builder.py`
- `Lokum1.0/Knowledge/H10_Global_Supervision_Arbitration.md`
- `Lokum1.0/Knowledge/H10_Rollback_Escalation_Governance.md`
- `Lokum1.0/Knowledge/H10_Strategic_Resource_Oversight.md`
- `Lokum1.0/Knowledge/H10_Long_Horizon_Outcome_Review.md`

### Modify

- `tools/brain_growth/common.py`
- `tools/brain_growth/quality_validator.py`
- `tools/brain_growth/layered_projection.py`
- `tests/test_brain_growth_validator.py`
- `tests/test_brain_growth_layered_projection.py`

### Refresh

- `docs/brain_growth/reports/brain_growth_validation.json`
- `docs/brain_growth/reports/brain_growth_validation.txt`
- `docs/brain_growth/projections/brain_growth_layered_projection.json`
- `docs/brain_growth/projections/brain_growth_layered_projection.md`

---

### Task 1: Add H10 discovery and builder tests

**Files:**
- Modify: `tools/brain_growth/common.py`
- Create: `tests/test_brain_growth_h10_builder.py`

- [ ] **Step 1: Write the failing H10 builder tests**

Create `tests/test_brain_growth_h10_builder.py` with:

```python
def test_discover_hidden_10_targets_reads_h10_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H10_Test_Supervision.md").write_text("# H10 Test\n", encoding="utf-8")

    assert common.discover_hidden_10_targets(knowledge_dir) == {"H10_Test_Supervision"}


def test_allowed_forward_targets_includes_hidden_10_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H10_Test_Supervision.md").write_text("# H10 Test\n", encoding="utf-8")

    targets = common.allowed_forward_targets(knowledge_dir)
    assert "H10_Test_Supervision" in targets
```

- [ ] **Step 2: Run the test to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h10_builder.py -q`

Expected: FAIL because `discover_hidden_10_targets` and `h10_builder` do not exist yet.

- [ ] **Step 3: Add H10 discovery to `common.py`**

Add:

```python
def discover_hidden_10_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H10_*.md")}
```

and update:

```python
| discover_hidden_10_targets(knowledge_dir)
```

- [ ] **Step 4: Re-run the test to keep only builder failures**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h10_builder.py -q`

Expected: Still FAIL, but now only because `h10_builder` behavior is missing.

---

### Task 2: Implement the H10 builder and generate H10 notes

**Files:**
- Create: `tools/brain_growth/h10_builder.py`
- Test: `tests/test_brain_growth_h10_builder.py`

- [ ] **Step 1: Extend the failing tests with H10 semantic shape**

Add:

```python
def test_render_note_contains_required_hidden10_shape() -> None:
    text = h10_builder.render_h10_note(h10_builder.H10_FAMILIES[0])

    assert '#layer/hidden_10_strategic_supervision' in text
    assert 'supervision_mode: "' in text
    assert 'governing_signal:' in text
    assert 'oversight_surfaces:' in text
    assert 'supervision_contracts:' in text
    assert '## Stratejik denetim amacı' in text
    assert '## Besleyen H9 düğümleri' in text
```

and:

```python
def test_write_h10_notes_creates_four_strategic_supervision_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "H9_Execution_Surface_Binding.md",
        "H9_Response_Payload_Composition.md",
        "H9_Commit_Ready_Delivery_Check.md",
        "H9_Failsafe_Action_Packaging.md",
        "Long_Term_Strategic_Planner.md",
        "Strategic_Resource_Allocator.md",
        "Global_State_Consensus.md",
        "Final_Execution_Gate.md",
    ):
        (knowledge_dir / name).write_text(f"# {Path(name).stem}\n", encoding="utf-8")

    written = h10_builder.write_h10_notes(knowledge_dir=knowledge_dir)
    assert [path.name for path in written] == [
        "H10_Global_Supervision_Arbitration.md",
        "H10_Long_Horizon_Outcome_Review.md",
        "H10_Rollback_Escalation_Governance.md",
        "H10_Strategic_Resource_Oversight.md",
    ]
```

- [ ] **Step 2: Run the tests to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h10_builder.py -q`

Expected: FAIL because `h10_builder.py` does not exist yet.

- [ ] **Step 3: Write minimal `h10_builder.py`**

Implement:

```python
@dataclass(frozen=True)
class H10Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    supervision_mode: str
    governing_signal: str
    oversight_surfaces: tuple[str, ...]
    supervision_contracts: tuple[str, ...]
    supervision_purpose: tuple[str, ...]
    h9_inputs: tuple[str, ...]
    governing_signal_mapping: tuple[str, ...]
    oversight_contract_strategy: tuple[str, ...]
    escalation_rules: tuple[str, ...]
    downstream_outputs: tuple[str, ...]
```

Required tags:

```python
REQUIRED_TAGS = (
    "#layer/hidden_10_strategic_supervision",
    "#strategy/supervision_contract",
    "#strategy/oversight_surface",
    "#execution/governance_binding",
)
```

Required sections:

```python
SECTION_HEADERS = (
    "## Stratejik denetim amacı",
    "## Governing signal eşlemesi",
    "## Oversight surface sözleşmeleri",
    "## Escalation ve rollback kuralları",
    "## Besleyen H9 düğümleri",
    "## Denetlenen çıktı yolları",
)
```

- [ ] **Step 4: Implement deterministic H10 families**

Create:

```python
H10_Global_Supervision_Arbitration
H10_Rollback_Escalation_Governance
H10_Strategic_Resource_Oversight
H10_Long_Horizon_Outcome_Review
```

Each family must reference real H9 notes and existing strategic surfaces only.

- [ ] **Step 5: Implement render, verify, write, and CLI**

Add:

```python
def render_h10_note(family: H10Family) -> str: ...
def verify_h10_note(path: Path, family: H10Family) -> dict[str, object]: ...
def write_h10_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]: ...
def run_checks(paths: list[Path]) -> list[dict[str, object]]: ...
```

- [ ] **Step 6: Run the tests to verify GREEN**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h10_builder.py -q`

Expected: PASS.

- [ ] **Step 7: Generate the real H10 notes**

Run: `python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/h10_builder.py`

Expected: Four `H10_*.md` files are written into `Lokum1.0/Knowledge`.

---

### Task 3: Extend validator coverage for H10

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write failing H10 validator tests**

Add:

```python
def test_validate_h10_note_accepts_hidden10_shape(tmp_path: Path) -> None:
    note_path = tmp_path / "H10_Test_Supervision.md"
    note_path.write_text(h10_note_text(title="Strategic Supervision"), encoding="utf-8")

    report = quality_validator.validate_h10_note(note_path, tmp_path)

    assert report.ok is True
    assert report.metrics["h9_inputs"] == 1
    assert report.metrics["oversight_surface_count"] == 2
    assert report.metrics["supervision_contract_count"] == 2
    assert report.metrics["supervised_output_count"] == 2
```

and:

```python
def test_build_report_contains_h10_counts_and_supervision_remediation_map(tmp_path: Path) -> None:
    ...
    assert report["kinds"]["h10"]["file_count"] == 1
```

- [ ] **Step 2: Run validator tests to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_validator.py -q`

Expected: FAIL because `validate_h10_note` and `h10` report integration are missing.

- [ ] **Step 3: Implement H10 validator support**

Add:

```python
H10_FILENAME_RE = re.compile(r"^H10_([A-Za-z0-9_]+)\.md$")
REPORT_KIND_ORDER = ("raw", "synthesis", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "index")
```

Create:

```python
def h10_note_paths(knowledge_dir: Path) -> list[Path]: ...
def h10_family_lookup() -> dict[str, Any]: ...
def supported_supervision_modes() -> set[str]: ...
def validate_h10_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport: ...
```

Metrics:

```python
{
    "h9_inputs": ...,
    "oversight_surface_count": ...,
    "supervision_contract_count": ...,
    "supervised_output_count": ...,
    "wikilink_count": ...,
}
```

- [ ] **Step 4: Register H10 issue codes and safe fix boundaries**

Add:

```python
invalid_supervision_mode
missing_governing_signal
missing_oversight_surface
missing_supervision_contract
missing_h9_input
missing_governing_signal_mapping
missing_oversight_contract
missing_escalation_rule
h10_spec_violation
```

and ensure `--fix` does not invent H10 semantic values.

- [ ] **Step 5: Re-run validator tests to verify GREEN**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_validator.py -q`

Expected: PASS.

---

### Task 4: Extend projection with hidden_10 and `strategic_supervision_graph`

**Files:**
- Modify: `tools/brain_growth/layered_projection.py`
- Modify: `tests/test_brain_growth_layered_projection.py`

- [ ] **Step 1: Write failing projection tests for H10**

Add:

```python
assert list(projection["layers"]) == [
    "raw", "hidden_3", "hidden_4", "hidden_5",
    "hidden_6", "hidden_7", "hidden_8", "hidden_9", "hidden_10", "index"
]
assert projection["transition_counts"]["hidden_9_to_hidden_10"] == 1
assert "strategic_supervision_graph" in projection
assert projection["strategic_supervision_graph"]["supervision_nodes"]
assert projection["strategic_supervision_graph"]["oversight_nodes"]
```

- [ ] **Step 2: Run projection tests to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_layered_projection.py -q`

Expected: FAIL because `hidden_10` and `strategic_supervision_graph` do not exist.

- [ ] **Step 3: Extend layer discovery and ordering**

Update:

```python
LAYER_ORDER = (
    "raw", "hidden_3", "hidden_4", "hidden_5",
    "hidden_6", "hidden_7", "hidden_8", "hidden_9", "hidden_10", "index"
)
```

and:

```python
"hidden_10": sorted(path for path in knowledge_dir.glob("H10_*.md") if path.stem not in FORBIDDEN_NODES),
```

- [ ] **Step 4: Implement derived H10 supervision graph**

Add:

```python
def build_strategic_supervision_graph(hidden_10_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    ...
```

Output:

```python
{
    "signal_nodes": ...,
    "supervision_nodes": ...,
    "oversight_nodes": ...,
    "governance_edges": ...,
    "oversight_edges": ...,
}
```

- [ ] **Step 5: Add projection payload and markdown export**

Extend:

```python
"strategic_supervision_graph": build_strategic_supervision_graph(layers["hidden_10"])
```

and markdown:

```python
lines.extend(["", "## Strategic supervision graph", ""])
lines.append(f"- supervision_nodes: {len(...)}")
```

- [ ] **Step 6: Re-run projection tests to verify GREEN**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_layered_projection.py -q`

Expected: PASS.

---

### Task 5: Refresh reports and verify the full chain

**Files:**
- Refresh: `docs/brain_growth/reports/brain_growth_validation.json`
- Refresh: `docs/brain_growth/reports/brain_growth_validation.txt`
- Refresh: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Refresh: `docs/brain_growth/projections/brain_growth_layered_projection.md`

- [ ] **Step 1: Run the full `brain_growth` test suite**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth*.py`

Expected: All tests pass.

- [ ] **Step 2: Refresh projection outputs**

Run: `python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/layered_projection.py`

- [ ] **Step 3: Refresh validator outputs**

Run:

```bash
python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/quality_validator.py --format json --output /Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/reports/brain_growth_validation.json
python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/quality_validator.py --format text --output /Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/reports/brain_growth_validation.txt
```

Expected:

- `Status: pass`
- `h10: files=4, ok=4, issues=0`
- `forbidden_reference_count: 0`

- [ ] **Step 4: Verify H10 shows up in the artifacts**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path("/Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/projections/brain_growth_layered_projection.md").read_text(encoding="utf-8")
print("hidden_10" in text, "Strategic supervision graph" in text)
PY
```

Expected: `True True`

---

## Self-review

### Spec coverage

- H10 semantic layer: covered by Task 2
- validator H10 support: covered by Task 3
- projection `hidden_10` and `strategic_supervision_graph`: covered by Task 4
- artifact refresh and integrity pass: covered by Task 5

### Placeholder scan

- No placeholders remain.

### Type consistency

- H10 discovery uses `H10_*.md`
- validator registers `h10` as a first-class kind
- projection uses `hidden_10`
- derived graph name is consistently `strategic_supervision_graph`
