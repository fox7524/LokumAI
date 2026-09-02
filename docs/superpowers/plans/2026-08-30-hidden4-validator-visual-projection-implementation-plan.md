# Hidden 4 Validator Visual Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a real `hidden_4` reasoning/convergence layer, upgrade `quality_validator` with auto-fix and graph metrics, and generate a clean layered projection that makes the LokumAI vault look like a structured feed-forward neural network.

**Architecture:** Keep the Obsidian vault as the semantic source of truth and add three focused tools around it: an `H4` note builder, a validator v2 that can measure and safely repair structure, and a projection renderer that derives a layered visual/export from the real notes. Reuse the existing `common.py`, `quality_validator.py`, and `index_builder.py` patterns instead of inventing a parallel framework.

**Tech Stack:** Python 3, Markdown/Obsidian notes, `pytest`, existing `tools/brain_growth/*` modules

---

## File map

- Create: `tools/brain_growth/h4_builder.py`
- Create: `tools/brain_growth/layered_projection.py`
- Create: `tests/test_brain_growth_h4_builder.py`
- Create: `tests/test_brain_growth_layered_projection.py`
- Modify: `tools/brain_growth/common.py`
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`
- Create: `docs/brain_growth/projections/.gitkeep`
- Create: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Create: `docs/brain_growth/projections/brain_growth_layered_projection.md`
- Create: `Lokum1.0/Knowledge/H4_Cross_Domain_Causal_Alignment.md`
- Create: `Lokum1.0/Knowledge/H4_Performance_Bottleneck_Disambiguation.md`
- Create: `Lokum1.0/Knowledge/H4_Security_Failure_Mode_Arbitration.md`
- Create: `Lokum1.0/Knowledge/H4_Cognitive_Retrieval_Policy_Selection.md`
- Create: `Lokum1.0/Knowledge/H4_Resource_Execution_Prioritization.md`
- Create: `Lokum1.0/Knowledge/H4_Edge_Device_Response_Strategy.md`

## Task 1: Extend the shared layer model

**Files:**
- Modify: `tools/brain_growth/common.py`
- Test: `tests/test_brain_growth_h4_builder.py`

- [ ] **Step 1: Write the failing tests for hidden_4 target discovery and allowed forward targets**

```python
from pathlib import Path

from tools.brain_growth import common


def test_discover_hidden_4_targets_reads_h4_notes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H4_Test_Reasoning.md").write_text("# H4 Test\n", encoding="utf-8")

    assert common.discover_hidden_4_targets(knowledge_dir) == {"H4_Test_Reasoning"}


def test_allowed_forward_targets_includes_hidden_4_nodes(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "H4_Test_Reasoning.md").write_text("# H4 Test\n", encoding="utf-8")

    assert "H4_Test_Reasoning" in common.allowed_forward_targets(knowledge_dir)
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python3 -m pytest tests/test_brain_growth_h4_builder.py::test_discover_hidden_4_targets_reads_h4_notes tests/test_brain_growth_h4_builder.py::test_allowed_forward_targets_includes_hidden_4_nodes -v`

Expected: `FAIL` with `AttributeError` because `discover_hidden_4_targets()` does not exist yet.

- [ ] **Step 3: Add hidden_4 discovery support to the shared module**

```python
def discover_hidden_4_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return {path.stem for path in knowledge_dir.glob("H4_*.md")}


def allowed_forward_targets(knowledge_dir: Path = KNOWLEDGE_DIR) -> set[str]:
    return (
        discover_hidden_1_targets(knowledge_dir)
        | discover_hidden_2_targets(knowledge_dir)
        | discover_hidden_3_targets(knowledge_dir)
        | discover_hidden_4_targets(knowledge_dir)
    )
```

- [ ] **Step 4: Run the tests to verify pass**

Run: `python3 -m pytest tests/test_brain_growth_h4_builder.py::test_discover_hidden_4_targets_reads_h4_notes tests/test_brain_growth_h4_builder.py::test_allowed_forward_targets_includes_hidden_4_nodes -v`

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add tools/brain_growth/common.py tests/test_brain_growth_h4_builder.py
git commit -m "feat: add hidden4 discovery to shared graph helpers"
```

## Task 2: Build hidden_4 reasoning/convergence notes

**Files:**
- Create: `tools/brain_growth/h4_builder.py`
- Create: `tests/test_brain_growth_h4_builder.py`
- Create: `Lokum1.0/Knowledge/H4_Cross_Domain_Causal_Alignment.md`
- Create: `Lokum1.0/Knowledge/H4_Performance_Bottleneck_Disambiguation.md`
- Create: `Lokum1.0/Knowledge/H4_Security_Failure_Mode_Arbitration.md`
- Create: `Lokum1.0/Knowledge/H4_Cognitive_Retrieval_Policy_Selection.md`
- Create: `Lokum1.0/Knowledge/H4_Resource_Execution_Prioritization.md`
- Create: `Lokum1.0/Knowledge/H4_Edge_Device_Response_Strategy.md`

- [ ] **Step 1: Write the failing tests for H4 note rendering and file writing**

```python
from pathlib import Path

from tools.brain_growth import h4_builder


def test_render_note_contains_required_hidden4_sections() -> None:
    note = h4_builder.H4_FAMILIES[0]
    text = h4_builder.render_h4_note(note)

    assert '  - "#layer/hidden_4_reasoning_convergence"' in text
    assert "## Yakınsama amacı" in text
    assert "## Tetikleyiciler" in text
    assert "## Karar sınırları" in text
    assert "## Besleyen sentez düğümleri" in text
    assert "## İleri yönlü etkiler" in text


def test_write_h4_notes_creates_six_reasoning_files(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    written = h4_builder.write_h4_notes(force=False, knowledge_dir=knowledge_dir)

    assert len(written) == 6
    assert all(path.name.startswith("H4_") for path in written)
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python3 -m pytest tests/test_brain_growth_h4_builder.py::test_render_note_contains_required_hidden4_sections tests/test_brain_growth_h4_builder.py::test_write_h4_notes_creates_six_reasoning_files -v`

Expected: `FAIL` because `h4_builder.py` does not exist yet.

- [ ] **Step 3: Implement a focused H4 builder with explicit family specs**

```python
from dataclasses import dataclass
from pathlib import Path

from tools.brain_growth.common import KNOWLEDGE_DIR, assert_no_forbidden_nodes


@dataclass(frozen=True)
class H4Family:
    filename: str
    title: str
    tags: tuple[str, ...]
    synthesis_inputs: tuple[str, ...]
    strategic_anchors: tuple[str, ...]
    triggers: tuple[str, ...]
    decision_boundaries: tuple[str, ...]
    downstream_effects: tuple[str, ...]


H4_FAMILIES: tuple[H4Family, ...] = (
    H4Family(
        filename="H4_Cross_Domain_Causal_Alignment.md",
        title="Cross Domain Causal Alignment",
        tags=("#layer/hidden_4_reasoning_convergence", "#reasoning/causal_alignment"),
        synthesis_inputs=(
            "H3_Apple_Silicon_Memory_Execution_Synthesis",
            "H3_Embedded_Interrupt_DMA_Synthesis",
            "H3_Cognitive_Graph_RAG_Routing_Synthesis",
        ),
        strategic_anchors=("Causal_Inference_Engine", "Topology_Analysis"),
        triggers=("Cross-stack bottleneck ambiguity", "Latency cascade with multiple suspects"),
        decision_boundaries=("Prefer shared cause over coincidental correlation",),
        downstream_effects=("Escalate to policy routing", "Promote retrieval path narrowing"),
    ),
)


def render_h4_note(family: H4Family) -> str:
    text = (
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        + "".join(f'  - "{tag}"\n' for tag in family.tags)
        + "---\n\n"
        f"# {family.title}\n\n"
        "## Yakınsama amacı\n\n"
        f"{family.title} reasoning node.\n\n"
        "## Tetikleyiciler\n\n"
        + "".join(f"- {item}\n" for item in family.triggers)
        + "\n## Karar sınırları\n\n"
        + "".join(f"- {item}\n" for item in family.decision_boundaries)
        + "\n## Besleyen sentez düğümleri\n\n"
        + "".join(f"- [[{item}]]\n" for item in family.synthesis_inputs)
        + "".join(f"- [[{item}]]\n" for item in family.strategic_anchors)
        + "\n## İleri yönlü etkiler\n\n"
        + "".join(f"- {item}\n" for item in family.downstream_effects)
    )
    assert_no_forbidden_nodes(text)
    return text
```

- [ ] **Step 4: Expand `H4_FAMILIES` to the six agreed reasoning nodes and write them**

```python
def write_h4_notes(force: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR) -> list[Path]:
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for family in H4_FAMILIES:
        path = knowledge_dir / family.filename
        if path.exists() and not force:
            raise FileExistsError(f"{path.name} already exists; pass force=True to overwrite")
        path.write_text(render_h4_note(family), encoding="utf-8")
        written.append(path)
    return sorted(written)
```

- [ ] **Step 5: Run the tests to verify pass**

Run: `python3 -m pytest tests/test_brain_growth_h4_builder.py -v`

Expected: `passed` for rendering, file creation, and forbidden-node safety tests.

- [ ] **Step 6: Generate the real H4 notes**

Run: `python3 tools/brain_growth/h4_builder.py --force`

Expected: six `H4_*.md` files appear under `Lokum1.0/Knowledge`.

- [ ] **Step 7: Commit**

```bash
git add tools/brain_growth/h4_builder.py tests/test_brain_growth_h4_builder.py Lokum1.0/Knowledge/H4_*.md
git commit -m "feat: add hidden4 reasoning convergence layer"
```

## Task 3: Upgrade validator v2 with graph metrics

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write the failing tests for hidden_4 validation and graph metrics**

```python
from pathlib import Path

from tools.brain_growth import quality_validator


def test_validate_h4_note_accepts_hidden4_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    path = knowledge_dir / "H4_Test_Reasoning.md"
    path.write_text(
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        '  - "#layer/hidden_4_reasoning_convergence"\n'
        '  - "#reasoning/test"\n'
        "---\n\n"
        "# Test Reasoning\n\n"
        "## Yakınsama amacı\n\nAmaç.\n\n"
        "## Tetikleyiciler\n\n- Tetikleyici\n\n"
        "## Karar sınırları\n\n- Sınır\n\n"
        "## Besleyen sentez düğümleri\n\n- [[H3_Test]]\n\n"
        "## İleri yönlü etkiler\n\n- Etki\n",
        encoding="utf-8",
    )

    report = quality_validator.validate_h4_note(path, knowledge_dir=knowledge_dir)
    assert report.ok is True


def test_build_report_contains_graph_metrics_section(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    report = quality_validator.build_report(scope="all", knowledge_dir=knowledge_dir)

    assert "graph_metrics" in report
    assert "node_count_by_kind" in report["graph_metrics"]
    assert "forward_link_compliance_ratio" in report["graph_metrics"]
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_validate_h4_note_accepts_hidden4_shape tests/test_brain_growth_validator.py::test_build_report_contains_graph_metrics_section -v`

Expected: `FAIL` because `validate_h4_note()` and graph metrics do not exist yet.

- [ ] **Step 3: Add hidden_4 validation constants and report collection**

```python
H4_FILENAME_RE = re.compile(r"^H4_([A-Za-z0-9_]+)\.md$")
H4_REQUIRED_SECTIONS = (
    "## Yakınsama amacı",
    "## Tetikleyiciler",
    "## Karar sınırları",
    "## Besleyen sentez düğümleri",
    "## İleri yönlü etkiler",
)


def h4_note_paths(knowledge_dir: Path) -> list[Path]:
    return sorted(knowledge_dir.glob("H4_*.md"))


def validate_h4_note(path: Path, knowledge_dir: Path = KNOWLEDGE_DIR) -> FileReport:
    text = read_text(path)
    issues = validate_common_shape(
        path=path,
        text=text,
        required_sections=H4_REQUIRED_SECTIONS,
        required_tags=("#layer/hidden_4_reasoning_convergence",),
    )
    links = parse_wikilinks(text)
    if not any(link.startswith("H3_") for link in links):
        issues.append(build_issue("missing_h3_input", f"{path.name}: en az bir H3 girdi linki gerekli"))
    return FileReport(path=str(path), kind="h4", title=extract_title(text), ok=not issues, issues=issues)
```

- [ ] **Step 4: Add graph metrics to `build_report()`**

```python
def build_graph_metrics(file_reports: list[FileReport]) -> dict[str, Any]:
    total = len(file_reports)
    ok_count = sum(1 for report in file_reports if report.ok)
    return {
        "node_count_by_kind": {
            "raw": sum(1 for report in file_reports if report.kind == "raw"),
            "synthesis": sum(1 for report in file_reports if report.kind == "synthesis"),
            "h4": sum(1 for report in file_reports if report.kind == "h4"),
            "index": sum(1 for report in file_reports if report.kind == "index"),
        },
        "forward_link_compliance_ratio": 0.0 if total == 0 else round(ok_count / total, 4),
        "forbidden_reference_count": sum(
            1
            for report in file_reports
            for issue in report.issues
            if issue.code == "forbidden_node_reference"
        ),
    }
```

- [ ] **Step 5: Render graph metrics in text output**

```python
def render_text_report(report: dict[str, Any]) -> str:
    graph_metrics = report.get("graph_metrics", {})
    lines = [
        f"Scope: {report['scope']}",
        f"Status: {report['status']}",
        "",
        "Graph metrics:",
        f"- node_count_by_kind: {graph_metrics.get('node_count_by_kind', {})}",
        f"- forward_link_compliance_ratio: {graph_metrics.get('forward_link_compliance_ratio', 0.0)}",
        f"- forbidden_reference_count: {graph_metrics.get('forbidden_reference_count', 0)}",
    ]
    return "\n".join(lines)
```

- [ ] **Step 6: Run the validator test suite**

Run: `python3 -m pytest tests/test_brain_growth_validator.py -q`

Expected: all validator tests pass, including the new hidden_4 and metrics coverage.

- [ ] **Step 7: Commit**

```bash
git add tools/brain_growth/quality_validator.py tests/test_brain_growth_validator.py
git commit -m "feat: add hidden4 validation and graph metrics"
```

## Task 4: Add safe auto-fix mode to validator v2

**Files:**
- Modify: `tools/brain_growth/quality_validator.py`
- Modify: `tests/test_brain_growth_validator.py`

- [ ] **Step 1: Write the failing tests for safe fixes**

```python
from pathlib import Path

from tools.brain_growth import quality_validator


def test_apply_safe_fixes_quotes_tags_and_adds_missing_section(tmp_path: Path) -> None:
    path = tmp_path / "RAG_Memory_Cell_13_Test.md"
    path.write_text(
        "---\n"
        "date: 2026-08-30\n"
        "tags:\n"
        "  - #rag/memory_cell\n"
        "  - #rag/training\n"
        "---\n\n"
        "# Test\n\n"
        "## Teknik çekirdek\n\nMetin.\n",
        encoding="utf-8",
    )

    fixed_text, changes = quality_validator.apply_safe_fixes(path.read_text(encoding="utf-8"), kind="raw")

    assert '  - "#rag/memory_cell"' in fixed_text
    assert "## Doğrulanmış bulgular" in fixed_text
    assert "quote_tags" in changes
    assert "add_missing_sections" in changes
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_apply_safe_fixes_quotes_tags_and_adds_missing_section -v`

Expected: `FAIL` because `apply_safe_fixes()` does not exist yet.

- [ ] **Step 3: Implement safe fix primitives only**

```python
def apply_safe_fixes(text: str, kind: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    updated = text

    if "  - #rag/memory_cell" in updated:
        updated = updated.replace("  - #rag/memory_cell", '  - "#rag/memory_cell"')
        changes.append("quote_tags")

    required_sections = {
        "raw": RAW_REQUIRED_SECTIONS,
        "synthesis": SYNTHESIS_REQUIRED_SECTIONS,
        "h4": H4_REQUIRED_SECTIONS,
        "index": INDEX_REQUIRED_SECTIONS,
    }[kind]

    missing = [section for section in required_sections if section not in updated]
    if missing:
        updated = updated.rstrip() + "\n\n" + "\n\n".join(f"{section}\n\n- auto-added structural placeholder" for section in missing) + "\n"
        changes.append("add_missing_sections")

    return updated, changes
```

- [ ] **Step 4: Wire `--fix` into the CLI and persist a fix report**

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="all", choices=("all", "raw", "synthesis", "h4", "index"))
    parser.add_argument("--format", default="text", choices=("text", "json"))
    parser.add_argument("--fix", action="store_true")
    return parser.parse_args()
```

```python
if args.fix:
    fixed_text, changes = apply_safe_fixes(original_text, kind=kind)
    if changes:
        path.write_text(fixed_text, encoding="utf-8")
```

- [ ] **Step 5: Run the focused and full validator tests**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_apply_safe_fixes_quotes_tags_and_adds_missing_section tests/test_brain_growth_validator.py -q`

Expected: all validator tests pass.

- [ ] **Step 6: Generate a real validator report with fixes disabled first, then enabled**

Run: `python3 tools/brain_growth/quality_validator.py --scope all --format text`

Expected: baseline report prints metrics with no mutation.

Run: `python3 tools/brain_growth/quality_validator.py --scope all --format json --fix`

Expected: safe structural fixes apply only where allowed, and the JSON report includes fix metadata.

- [ ] **Step 7: Commit**

```bash
git add tools/brain_growth/quality_validator.py tests/test_brain_growth_validator.py docs/brain_growth/reports/
git commit -m "feat: add safe autofix mode to graph validator"
```

## Task 5: Build the layered visual projection/export

**Files:**
- Create: `tools/brain_growth/layered_projection.py`
- Create: `tests/test_brain_growth_layered_projection.py`
- Create: `docs/brain_growth/projections/.gitkeep`
- Create: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Create: `docs/brain_growth/projections/brain_growth_layered_projection.md`

- [ ] **Step 1: Write the failing tests for projection shape**

```python
from pathlib import Path

from tools.brain_growth import layered_projection


def test_build_projection_groups_nodes_by_layer(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "RAG_Memory_Cell_13_Test.md").write_text("# Raw\n", encoding="utf-8")
    (knowledge_dir / "H3_Test.md").write_text("# H3\n", encoding="utf-8")
    (knowledge_dir / "H4_Test.md").write_text("# H4\n", encoding="utf-8")

    projection = layered_projection.build_projection(knowledge_dir=knowledge_dir)

    assert "layers" in projection
    assert "raw" in projection["layers"]
    assert "hidden_3" in projection["layers"]
    assert "hidden_4" in projection["layers"]


def test_write_projection_outputs_json_and_markdown(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    output_dir = tmp_path / "projections"
    output_dir.mkdir(parents=True, exist_ok=True)

    written = layered_projection.write_projection_outputs(knowledge_dir=knowledge_dir, output_dir=output_dir)
    assert {path.suffix for path in written} == {".json", ".md"}
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python3 -m pytest tests/test_brain_growth_layered_projection.py -v`

Expected: `FAIL` because `layered_projection.py` does not exist yet.

- [ ] **Step 3: Implement a derived layer projection model**

```python
from pathlib import Path

from tools.brain_growth.common import KNOWLEDGE_DIR


def build_projection(knowledge_dir: Path = KNOWLEDGE_DIR) -> dict[str, object]:
    return {
        "layers": {
            "raw": sorted(path.stem for path in knowledge_dir.glob("RAG_Memory_Cell_*.md")),
            "hidden_3": sorted(path.stem for path in knowledge_dir.glob("H3_*.md")),
            "hidden_4": sorted(path.stem for path in knowledge_dir.glob("H4_*.md")),
            "index": sorted(path.stem for path in knowledge_dir.glob("Index_*.md")),
        }
    }
```

- [ ] **Step 4: Render the projection as both machine and human output**

```python
def render_projection_markdown(projection: dict[str, object]) -> str:
    layers = projection["layers"]
    return (
        "# Brain Growth Layered Projection\n\n"
        "## Layers\n\n"
        f"- raw: {len(layers['raw'])}\n"
        f"- hidden_3: {len(layers['hidden_3'])}\n"
        f"- hidden_4: {len(layers['hidden_4'])}\n"
        f"- index: {len(layers['index'])}\n"
    )
```

```python
def write_projection_outputs(knowledge_dir: Path = KNOWLEDGE_DIR, output_dir: Path | None = None) -> list[Path]:
    output_root = output_dir or (Path(__file__).resolve().parents[2] / "docs" / "brain_growth" / "projections")
    output_root.mkdir(parents=True, exist_ok=True)
    projection = build_projection(knowledge_dir=knowledge_dir)
    json_path = output_root / "brain_growth_layered_projection.json"
    md_path = output_root / "brain_growth_layered_projection.md"
    json_path.write_text(json.dumps(projection, indent=2), encoding="utf-8")
    md_path.write_text(render_projection_markdown(projection), encoding="utf-8")
    return [json_path, md_path]
```

- [ ] **Step 5: Run the projection test suite**

Run: `python3 -m pytest tests/test_brain_growth_layered_projection.py -q`

Expected: projection tests pass and both output files are written.

- [ ] **Step 6: Generate the real projection artifacts**

Run: `python3 tools/brain_growth/layered_projection.py`

Expected: `docs/brain_growth/projections/brain_growth_layered_projection.json` and `docs/brain_growth/projections/brain_growth_layered_projection.md` are created.

- [ ] **Step 7: Commit**

```bash
git add tools/brain_growth/layered_projection.py tests/test_brain_growth_layered_projection.py docs/brain_growth/projections/
git commit -m "feat: add layered graph projection exports"
```

## Task 6: End-to-end verification and refresh

**Files:**
- Modify: `docs/brain_growth/reports/brain_growth_validation.json`
- Modify: `docs/brain_growth/reports/brain_growth_validation.txt`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.json`
- Modify: `docs/brain_growth/projections/brain_growth_layered_projection.md`

- [ ] **Step 1: Run the complete test suite for the brain growth toolchain**

Run: `python3 -m pytest tests/test_brain_growth_common.py tests/test_brain_growth_h4_builder.py tests/test_brain_growth_validator.py tests/test_brain_growth_index_builder.py tests/test_brain_growth_layered_projection.py -q`

Expected: all tests pass.

- [ ] **Step 2: Regenerate H4 notes, validator reports, and projection outputs**

Run: `python3 tools/brain_growth/h4_builder.py --force && python3 tools/brain_growth/quality_validator.py --scope all --format json && python3 tools/brain_growth/quality_validator.py --scope all --format text && python3 tools/brain_growth/layered_projection.py`

Expected: updated `H4_*.md`, validator outputs, and projection files.

- [ ] **Step 3: Verify no forbidden node regressions**

Run: `python3 -m pytest tests/test_brain_growth_validator.py::test_validate_h4_note_accepts_hidden4_shape -q`

Expected: `1 passed`

- [ ] **Step 4: Sanity-check the generated outputs**

Run: `python3 -m json.tool docs/brain_growth/reports/brain_growth_validation.json > /tmp/brain_growth_validation.pretty.json && python3 -m json.tool docs/brain_growth/projections/brain_growth_layered_projection.json > /tmp/brain_growth_projection.pretty.json`

Expected: both commands succeed with no JSON parse errors.

- [ ] **Step 5: Commit**

```bash
git add Lokum1.0/Knowledge/H4_*.md docs/brain_growth/reports/ docs/brain_growth/projections/
git commit -m "chore: refresh hidden4 reports and projection artifacts"
```

## Self-review

- Spec coverage:
  - `hidden_4` real convergence layer is covered by Task 1 and Task 2.
  - validator v2 metrics and `--fix` flow are covered by Task 3 and Task 4.
  - layered visual projection/export is covered by Task 5.
  - end-to-end regeneration and safety checks are covered by Task 6.
- Placeholder scan:
  - no placeholder tokens remain in the plan body.
- Type consistency:
  - `discover_hidden_4_targets()`, `write_h4_notes()`, `validate_h4_note()`, `apply_safe_fixes()`, `build_projection()`, and `write_projection_outputs()` are used consistently across tasks.
