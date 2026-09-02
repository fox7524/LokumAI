# Hidden 9 Execution Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-class `hidden_9_execution_packaging` layer that turns H8 policy assemblies into validated execution packages, extends validator coverage, and exports a derived `execution_package_graph`.

**Architecture:** Keep H8 focused on decision assembly and add H9 as a distinct execution-readiness layer. Extend the existing `brain_growth` pattern consistently: discovery in `common.py`, deterministic note generation in `h9_builder.py`, H9-specific validation in `quality_validator.py`, and derived package graph export in `layered_projection.py`.

**Tech Stack:** Python 3, Obsidian Markdown, `pytest`, existing `brain_growth` builder/validator/projection modules.

---

## File map

### Create

- `tools/brain_growth/h9_builder.py`
- `tests/test_brain_growth_h9_builder.py`
- `Lokum1.0/Knowledge/H9_Execution_Surface_Binding.md`
- `Lokum1.0/Knowledge/H9_Response_Payload_Composition.md`
- `Lokum1.0/Knowledge/H9_Commit_Ready_Delivery_Check.md`
- `Lokum1.0/Knowledge/H9_Failsafe_Action_Packaging.md`

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

### Task 1: Add H9 discovery and builder tests

**Files:**
- Modify: `tools/brain_growth/common.py`
- Create: `tests/test_brain_growth_h9_builder.py`

- [ ] **Step 1: Write the failing H9 builder tests**

Create `tests/test_brain_growth_h9_builder.py` with tests that lock the H9 contract:

```python
def test_discover_hidden_9_targets_reads_h9_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H9_Test_Package.md").write_text("# H9 Test\n", encoding="utf-8")

    assert common.discover_hidden_9_targets(knowledge_dir) == {"H9_Test_Package"}


def test_allowed_forward_targets_includes_hidden_9_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H9_Test_Package.md").write_text("# H9 Test\n", encoding="utf-8")

    targets = common.allowed_forward_targets(knowledge_dir)
    assert "H9_Test_Package" in targets
```

- [ ] **Step 2: Run the test to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h9_builder.py -q`

Expected: FAIL because `discover_hidden_9_targets` and `h9_builder` do not exist yet.

- [ ] **Step 3: Add H9 discovery to `common.py`**

Extend layer discovery with:

```python
def discover_hidden_9_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H9_*.md")}
```

and in `allowed_forward_targets()`:

```python
| discover_hidden_9_targets(knowledge_dir)
```

- [ ] **Step 4: Re-run the test to keep only builder failures**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h9_builder.py -q`

Expected: Still FAIL, but now only because `h9_builder` behavior is missing.

- [ ] **Step 5: Commit**

```bash
git add tools/brain_growth/common.py tests/test_brain_growth_h9_builder.py
git commit -m "test: add hidden9 discovery coverage"
```

---

### Task 2: Implement the H9 builder and generate H9 notes

**Files:**
- Create: `tools/brain_growth/h9_builder.py`
- Test: `tests/test_brain_growth_h9_builder.py`

- [ ] **Step 1: Extend the failing tests with H9 semantic shape**

Add tests like:

```python
def test_render_note_contains_required_hidden9_shape() -> None:
    text = h9_builder.render_h9_note(h9_builder.H9_FAMILIES[0])

    assert '#layer/hidden_9_execution_packaging' in text
    assert 'package_mode: "' in text
    assert 'source_policy:' in text
    assert 'delivery_surfaces:' in text
    assert 'package_contracts:' in text
    assert '## Paketleme amacı' in text
    assert '## Besleyen H8 düğümleri' in text


def test_write_h9_notes_creates_four_execution_packaging_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "H8_Dominant_Thoughtseed_Selection.md",
        "H8_Global_Policy_Broadcast.md",
        "H8_Decision_Commitment_Gate.md",
        "H8_Exception_Override_Arbitration.md",
        "Executive_Action_Formatter.md",
        "Final_Execution_Gate.md",
        "Cognitive_Response_Generator.md",
        "Working_Memory_Flush.md",
        "Global_State_Consensus.md",
        "Long_Term_Strategic_Planner.md",
    ):
        (knowledge_dir / name).write_text(f"# {Path(name).stem}\n", encoding="utf-8")

    written = h9_builder.write_h9_notes(knowledge_dir=knowledge_dir)
    assert [path.name for path in written] == [
        "H9_Commit_Ready_Delivery_Check.md",
        "H9_Execution_Surface_Binding.md",
        "H9_Failsafe_Action_Packaging.md",
        "H9_Response_Payload_Composition.md",
    ]
```

- [ ] **Step 2: Run the tests to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h9_builder.py -q`

Expected: FAIL because `h9_builder.py` does not exist yet.

- [ ] **Step 3: Write minimal `h9_builder.py`**

Implement the H9 family schema:

```python
@dataclass(frozen=True)
class H9Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    package_mode: str
    source_policy: str
    delivery_surfaces: tuple[str, ...]
    package_contracts: tuple[str, ...]
    packaging_purpose: tuple[str, ...]
    h8_inputs: tuple[str, ...]
    delivery_strategy: tuple[str, ...]
    readiness_rules: tuple[str, ...]
    downstream_outputs: tuple[str, ...]
```

Define required tags:

```python
REQUIRED_TAGS = (
    "#layer/hidden_9_execution_packaging",
    "#execution/package_contract",
    "#execution/delivery_surface",
    "#policy/surface_binding",
)
```

and required sections:

```python
SECTION_HEADERS = (
    "## Paketleme amacı",
    "## Source policy eşlemesi",
    "## Delivery surface sözleşmeleri",
    "## Readiness ve commit koşulları",
    "## Besleyen H8 düğümleri",
    "## Paketlenen çıktı yolları",
)
```

- [ ] **Step 4: Implement deterministic H9 families**

Create four families:

```python
H9_Execution_Surface_Binding
H9_Response_Payload_Composition
H9_Commit_Ready_Delivery_Check
H9_Failsafe_Action_Packaging
```

Each family must reference real existing H8 notes and existing downstream surfaces only.

- [ ] **Step 5: Implement render, verify, write, and CLI**

Add:

```python
def render_h9_note(family: H9Family) -> str: ...
def verify_h9_note(path: Path, family: H9Family) -> dict[str, object]: ...
def write_h9_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]: ...
def run_checks(paths: list[Path]) -> list[dict[str, object]]: ...
```

- [ ] **Step 6: Run the tests to verify GREEN**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_h9_builder.py -q`

Expected: PASS.

- [ ] **Step 7: Generate the real H9 notes**

Run: `python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/h9_builder.py`

Expected: Four `H9_*.md` files are written into `Lokum1.0/Knowledge`.

- [ ] **Step 8: Commit**

```bash
git add tools/brain_growth/h9_builder.py tests/test_brain_growth_h9_builder.py Lokum1.0/Knowledge/H9_*.md
git commit -m "feat: add hidden9 execution packaging layer"
```

---

### Task 3: Extend validator coverage for H9

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write failing H9 validator tests**

Add:

```python
def test_validate_h9_note_accepts_hidden9_shape(tmp_path: Path) -> None:
    note_path = tmp_path / "H9_Test_Package.md"
    note_path.write_text(h9_note_text(title="Execution Surface Binding"), encoding="utf-8")

    report = quality_validator.validate_h9_note(note_path, tmp_path)

    assert report.ok is True
    assert report.metrics["h8_inputs"] == 2
    assert report.metrics["delivery_surface_count"] == 2
    assert report.metrics["package_contract_count"] == 2
    assert report.metrics["downstream_output_count"] == 2
```

and:

```python
def test_build_report_contains_h9_counts_and_delivery_remediation_map(tmp_path: Path) -> None:
    ...
    assert report["kinds"]["h9"]["file_count"] == 1
```

- [ ] **Step 2: Run validator tests to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_validator.py -q`

Expected: FAIL because `validate_h9_note` and `h9` report integration are missing.

- [ ] **Step 3: Implement H9 validator support**

Add imports from `h9_builder.py` and extend:

```python
H9_FILENAME_RE = re.compile(r"^H9_([A-Za-z0-9_]+)\.md$")
REPORT_KIND_ORDER = ("raw", "synthesis", "h4", "h5", "h6", "h7", "h8", "h9", "index")
```

Create:

```python
def h9_note_paths(knowledge_dir: Path) -> list[Path]: ...
def h9_family_lookup() -> dict[str, Any]: ...
def supported_package_modes() -> set[str]: ...
def validate_h9_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport: ...
```

Metrics must include:

```python
{
    "h8_inputs": ...,
    "delivery_surface_count": ...,
    "package_contract_count": ...,
    "downstream_output_count": ...,
    "wikilink_count": ...,
}
```

- [ ] **Step 4: Register H9 issue codes and safe fix boundaries**

Add issue codes:

```python
invalid_package_mode
missing_source_policy
missing_delivery_surface
missing_package_contract
missing_h8_input
missing_delivery_strategy
missing_commit_readiness_rule
h9_spec_violation
```

and ensure `--fix` does not invent missing semantic values for H9.

- [ ] **Step 5: Re-run validator tests to verify GREEN**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_validator.py -q`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/brain_growth/quality_validator.py tests/test_brain_growth_validator.py
git commit -m "feat: validate hidden9 execution packaging notes"
```

---

### Task 4: Extend projection with hidden_9 and `execution_package_graph`

**Files:**
- Modify: `tools/brain_growth/layered_projection.py`
- Modify: `tests/test_brain_growth_layered_projection.py`

- [ ] **Step 1: Write failing projection tests for H9**

Add expectations like:

```python
assert list(projection["layers"]) == [
    "raw", "hidden_3", "hidden_4", "hidden_5",
    "hidden_6", "hidden_7", "hidden_8", "hidden_9", "index"
]
assert projection["transition_counts"]["hidden_8_to_hidden_9"] == 1
assert "execution_package_graph" in projection
assert projection["execution_package_graph"]["package_nodes"]
assert projection["execution_package_graph"]["surface_nodes"]
```

- [ ] **Step 2: Run projection tests to verify RED**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_layered_projection.py -q`

Expected: FAIL because `hidden_9` and `execution_package_graph` do not exist.

- [ ] **Step 3: Extend layer discovery and ordering**

Update:

```python
LAYER_ORDER = (
    "raw", "hidden_3", "hidden_4", "hidden_5",
    "hidden_6", "hidden_7", "hidden_8", "hidden_9", "index"
)
```

and `collect_layer_paths()`:

```python
"hidden_9": sorted(path for path in knowledge_dir.glob("H9_*.md") if path.stem not in FORBIDDEN_NODES),
```

- [ ] **Step 4: Implement derived H9 package graph**

Add:

```python
def build_execution_package_graph(hidden_9_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    ...
```

The output must include:

```python
{
    "policy_nodes": ...,
    "package_nodes": ...,
    "surface_nodes": ...,
    "binding_edges": ...,
    "delivery_edges": ...,
}
```

- [ ] **Step 5: Add projection payload and markdown export**

Extend:

```python
"execution_package_graph": build_execution_package_graph(layers["hidden_9"])
```

and markdown:

```python
lines.extend(["", "## Execution package graph", ""])
lines.append(f"- package_nodes: {len(...)}")
lines.append(f"- surface_nodes: {len(...)}")
```

- [ ] **Step 6: Re-run projection tests to verify GREEN**

Run: `python3 -m pytest /Users/fox/Documents/PROJECTS/LokumAI/tests/test_brain_growth_layered_projection.py -q`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/brain_growth/layered_projection.py tests/test_brain_growth_layered_projection.py
git commit -m "feat: export hidden9 execution package graph"
```

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

Expected:

```text
Write completed.
- total_nodes=...
- total_edges=...
```

- [ ] **Step 3: Refresh validator outputs**

Run:

```bash
python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/quality_validator.py --format json --output /Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/reports/brain_growth_validation.json
python3 /Users/fox/Documents/PROJECTS/LokumAI/tools/brain_growth/quality_validator.py --format text --output /Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/reports/brain_growth_validation.txt
```

Expected:

- `Status: pass`
- `h9: files=4, ok=4, issues=0`
- `forbidden_reference_count: 0`

- [ ] **Step 4: Verify H9 shows up in the artifacts**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path("/Users/fox/Documents/PROJECTS/LokumAI/docs/brain_growth/projections/brain_growth_layered_projection.md").read_text(encoding="utf-8")
print("hidden_9" in text, "Execution package graph" in text)
PY
```

Expected: `True True`

- [ ] **Step 5: Commit**

```bash
git add docs/brain_growth/reports/brain_growth_validation.json docs/brain_growth/reports/brain_growth_validation.txt docs/brain_growth/projections/brain_growth_layered_projection.json docs/brain_growth/projections/brain_growth_layered_projection.md Lokum1.0/Knowledge/H9_*.md
git commit -m "feat: refresh hidden9 brain growth artifacts"
```

---

## Self-review

### Spec coverage

- H9 semantic layer: covered by Task 2
- validator H9 support: covered by Task 3
- projection `hidden_9` and `execution_package_graph`: covered by Task 4
- artifact refresh and integrity pass: covered by Task 5

### Placeholder scan

- No `TBD`, `TODO`, or “implement later” placeholders remain.

### Type consistency

- H9 note discovery uses `H9_*.md`
- validator registers `h9` as a first-class kind
- projection uses `hidden_9`
- derived graph name is consistently `execution_package_graph`
