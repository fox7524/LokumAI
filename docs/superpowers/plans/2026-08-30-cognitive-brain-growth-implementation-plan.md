# Cognitive Brain Growth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `Lokum1.0/Knowledge` with a controlled four-phase growth cycle: `50+` new research-grade memory cells, `hidden_3` synthesis nodes, an automatic quality validator, and a domain-based index/navigation layer.

**Architecture:** Keep the existing vault stable by introducing a new, explicit growth toolchain instead of extending the older `upscale_ann.py` / `massive_upscale_ann.py` scripts. Phase 1 writes only new `RAG_Memory_Cell_*.md` nodes, Phase 2 adds explicit `H3_*.md` synthesis nodes, Phase 3 validates graph quality without silent mutation, and Phase 4 adds navigation/index notes that organize the graph without turning into an omnidirectional supernode.

**Tech Stack:** Python 3, existing repository scripts, Obsidian Markdown, `pytest`, file-system based validation, Web research, sequential subagents.

---

## File map

### Create
- `tools/brain_growth/common.py`
- `tools/brain_growth/research_wave.py`
- `tools/brain_growth/h3_synthesis.py`
- `tools/brain_growth/quality_validator.py`
- `tools/brain_growth/index_builder.py`
- `tests/test_brain_growth_common.py`
- `tests/test_brain_growth_validator.py`
- `tests/test_brain_growth_index_builder.py`
- `docs/brain_growth/README.md`
- `docs/brain_growth/reports/.gitkeep`
- `Lokum1.0/Knowledge/RAG_Memory_Cell_*.md` (`50+` files created by Phase 1)
- `Lokum1.0/Knowledge/H3_*.md` (topic synthesis nodes created by Phase 2)
- `Lokum1.0/Knowledge/Brain_Growth_Index.md`
- `Lokum1.0/Knowledge/Index_Apple_Silicon_and_MLX.md`
- `Lokum1.0/Knowledge/Index_Embedded_and_ESP32.md`
- `Lokum1.0/Knowledge/Index_Cryptography_and_Memory_Safety.md`
- `Lokum1.0/Knowledge/Index_Cognitive_Graph_RAG.md`

### Read/Reuse
- `Lokum1.0/Knowledge/LokumAI-1.0.md` as read-only topology dictionary
- `massive_upscale_ann.py` only as prior-art reference, not as the implementation base
- `upscale_ann.py` only as prior-art reference, not as the implementation base
- `rag_ingestor_obsidian.py` for similarity/linking ideas, not as-is

### Do not modify
- `Lokum1.0/Knowledge/LokumAI-1.0.md`

---

### Task 1: Build the controlled growth toolchain

**Files:**
- Create: `tools/brain_growth/common.py`
- Create: `docs/brain_growth/README.md`
- Test: `tests/test_brain_growth_common.py`

- [ ] **Step 1: Create the shared graph-constraint module**

Implement `tools/brain_growth/common.py` with:
- `KNOWLEDGE_DIR`
- `FORBIDDEN_NODES = {"LokumAI-1.0", "LokumAI-1.0.md"}`
- layer discovery helpers for `hidden_1`, `hidden_2`, existing `hidden_3`
- functions to:
  - read note text
  - parse wikilinks
  - parse YAML frontmatter shallowly
  - assert forbidden node absence
  - assert link target layer membership
  - normalize filename-safe topic slugs

- [ ] **Step 2: Write failing tests for graph constraints**

Create `tests/test_brain_growth_common.py` with tests for:
- forbidden node detection
- wikilink extraction
- hidden-layer target validation
- filename normalization for `RAG_Memory_Cell_*` and `H3_*`

- [ ] **Step 3: Run the tests and verify failure**

Run:
```bash
pytest tests/test_brain_growth_common.py -q
```

Expected:
- failure for missing module/functions

- [ ] **Step 4: Implement the shared helpers**

Write the minimal implementation needed for those tests to pass.

- [ ] **Step 5: Re-run tests**

Run:
```bash
pytest tests/test_brain_growth_common.py -q
```

Expected:
- all tests pass

- [ ] **Step 6: Document the toolchain boundary**

Create `docs/brain_growth/README.md` describing:
- phase order `1 -> 2 -> 3 -> 4`
- immutable `LokumAI-1.0.md` rule
- naming rules
- report output location

---

### Task 2: Implement Phase 1 research wave generator

**Files:**
- Create: `tools/brain_growth/research_wave.py`
- Modify: `tools/brain_growth/common.py`
- Test: `tests/test_brain_growth_common.py`

- [ ] **Step 1: Define the Phase 1 domain matrix**

Inside `research_wave.py`, define explicit topic buckets with at least:
- Apple Silicon / MLX / Metal / UMA / zero-copy / dispatch
- ESP32 / FreeRTOS / interrupts / DMA
- PAC / memory safety / P2P / ZKP
- GNN / Graph RAG / Cognitive RAG / routing

Target count:
- minimum `50` generated note specs before file write

- [ ] **Step 2: Define the raw memory-cell template**

Template must include:
- quoted YAML frontmatter
- `#rag/memory_cell`
- `#rag/training`
- domain tag
- sections:
  - `## Teknik çekirdek`
  - `## Doğrulanmış bulgular`
  - `## LokumAI için çıkarım`
  - `## Sorgu ipuçları`
  - `## Kaynaklar`

- [ ] **Step 3: Define the linking policy**

Implement deterministic link assignment:
- per raw node: `4` forward wikilinks minimum
- only upward targets into approved downstream nodes
- allowed targets:
  - existing `hidden_1`
  - existing `hidden_2`
  - later, approved Phase 2 synthesis nodes when rerun
- never link to `LokumAI-1.0.md`

With `50+` nodes and `4+` links each, the plan guarantees `200+` new forward synapses.

- [ ] **Step 4: Add a dry-run mode before writing**

`research_wave.py` must support:
- `--dry-run`
- `--write`
- `--count <n>`

Dry-run should print:
- planned file count
- topic bucket distribution
- projected synapse count

- [ ] **Step 5: Verify dry-run first**

Run:
```bash
python3 tools/brain_growth/research_wave.py --dry-run --count 50
```

Expected:
- planned count `>= 50`
- projected synapses `>= 200`
- no write performed

- [ ] **Step 6: Write the raw research wave**

Run:
```bash
python3 tools/brain_growth/research_wave.py --write --count 50
```

Expected:
- `50+` new `RAG_Memory_Cell_*.md` files in `Lokum1.0/Knowledge`

- [ ] **Step 7: Verify Phase 1 output**

Run:
```bash
python3 tools/brain_growth/quality_validator.py --scope raw --format text
```

Expected:
- no forbidden-node references
- each raw node has required sections
- each raw node satisfies minimum forward-link count

---

### Task 3: Implement Phase 2 hidden_3 synthesis builder

**Files:**
- Create: `tools/brain_growth/h3_synthesis.py`
- Modify: `tools/brain_growth/common.py`
- Test: `tests/test_brain_growth_common.py`

- [ ] **Step 1: Define synthesis families**

Create explicit families:
- `H3_Apple_Silicon_Memory_Execution_Synthesis.md`
- `H3_Embedded_Interrupt_DMA_Synthesis.md`
- `H3_Cryptographic_Integrity_and_Memory_Safety_Synthesis.md`
- `H3_Cognitive_Graph_RAG_Routing_Synthesis.md`

- [ ] **Step 2: Define synthesis source selection**

Each synthesis node must aggregate:
- at least `8` lower-layer notes
- only from its domain family
- only from raw nodes or existing `hidden_1/hidden_2` anchors

- [ ] **Step 3: Define synthesis note structure**

Each `H3_*.md` must include:
- quoted frontmatter with `#layer/hidden_3_logic_synthesis`
- domain tag
- `## Soyutlama`
- `## İnvariantlar`
- `## Retrieval yönlendirme anlamı`
- `## Besleyen düğümler`
- `## İleri besleme`

- [ ] **Step 4: Add deterministic upward links**

Each synthesis node must:
- link downward to its source set in a bounded list
- link upward only to allowed future-facing nodes or approved decision-layer anchors already present
- avoid omnidirectional fan-out

- [ ] **Step 5: Generate synthesis notes**

Run:
```bash
python3 tools/brain_growth/h3_synthesis.py --write
```

Expected:
- `H3_*.md` files written under `Lokum1.0/Knowledge`

- [ ] **Step 6: Verify synthesis structure**

Run:
```bash
python3 tools/brain_growth/quality_validator.py --scope synthesis --format text
```

Expected:
- all `H3_*` nodes tagged as `hidden_3`
- each synthesis node has bounded, domain-coherent inputs
- no forbidden references

---

### Task 4: Implement Phase 3 automatic quality validator

**Files:**
- Create: `tools/brain_growth/quality_validator.py`
- Create: `tests/test_brain_growth_validator.py`
- Create: `docs/brain_growth/reports/.gitkeep`

- [ ] **Step 1: Write failing tests for validator rules**

Cover:
- missing frontmatter
- missing required sections
- forbidden `LokumAI-1.0` link
- invalid target layer
- insufficient forward-link count
- filename mismatch for raw and synthesis notes

- [ ] **Step 2: Run validator tests and verify failure**

Run:
```bash
pytest tests/test_brain_growth_validator.py -q
```

Expected:
- failure because validator module is not implemented yet

- [ ] **Step 3: Implement report-first validation**

`quality_validator.py` should support:
- `--scope raw|synthesis|index|all`
- `--format text|json`
- `--output docs/brain_growth/reports/<name>.json`

Checks:
- frontmatter presence
- quoted tag presence
- required section presence
- forbidden-node references
- link target validity
- minimum link count for raw wave
- synthesis filename / layer alignment
- placeholder phrase scan

- [ ] **Step 4: Re-run validator tests**

Run:
```bash
pytest tests/test_brain_growth_validator.py -q
```

Expected:
- all tests pass

- [ ] **Step 5: Produce a full quality report**

Run:
```bash
python3 tools/brain_growth/quality_validator.py --scope all --format json --output docs/brain_growth/reports/brain_growth_validation.json
python3 tools/brain_growth/quality_validator.py --scope all --format text
```

Expected:
- JSON report created
- text summary printed

---

### Task 5: Implement Phase 4 index and navigation layer

**Files:**
- Create: `tools/brain_growth/index_builder.py`
- Create: `tests/test_brain_growth_index_builder.py`
- Create: `Lokum1.0/Knowledge/Brain_Growth_Index.md`
- Create: `Lokum1.0/Knowledge/Index_Apple_Silicon_and_MLX.md`
- Create: `Lokum1.0/Knowledge/Index_Embedded_and_ESP32.md`
- Create: `Lokum1.0/Knowledge/Index_Cryptography_and_Memory_Safety.md`
- Create: `Lokum1.0/Knowledge/Index_Cognitive_Graph_RAG.md`

- [ ] **Step 1: Write failing tests for index generation**

Cover:
- stable index filenames
- section presence
- bounded domain links
- no forbidden node link
- no giant all-links dump

- [ ] **Step 2: Run the index tests and verify failure**

Run:
```bash
pytest tests/test_brain_growth_index_builder.py -q
```

Expected:
- failure because builder is not implemented yet

- [ ] **Step 3: Implement domain-based index generation**

`index_builder.py` should:
- scan raw and synthesis nodes
- group them by domain
- write one global brain growth index
- write four domain entry nodes
- keep link lists curated and sectioned, not exhaustive dumps

- [ ] **Step 4: Generate the navigation layer**

Run:
```bash
python3 tools/brain_growth/index_builder.py --write
```

Expected:
- `Brain_Growth_Index.md`
- four domain index notes

- [ ] **Step 5: Validate navigation output**

Run:
```bash
pytest tests/test_brain_growth_index_builder.py -q
python3 tools/brain_growth/quality_validator.py --scope index --format text
```

Expected:
- index tests pass
- no forbidden references
- navigation stays domain-bounded

---

### Task 6: Final verification and subagent handoff

**Files:**
- Read: `docs/brain_growth/reports/brain_growth_validation.json`
- Read: `Lokum1.0/Knowledge/Brain_Growth_Index.md`

- [ ] **Step 1: Count new raw nodes**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
files = list(Path("Lokum1.0/Knowledge").glob("RAG_Memory_Cell_*.md"))
print(len(files))
PY
```

Expected:
- output `>= 50`

- [ ] **Step 2: Count new synapses**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
import re
count = 0
for path in Path("Lokum1.0/Knowledge").glob("RAG_Memory_Cell_*.md"):
    count += len(re.findall(r"\[\[[^\]]+\]\]", path.read_text(encoding="utf-8")))
print(count)
PY
```

Expected:
- output `>= 200`

- [ ] **Step 3: Confirm immutable center rule**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
bad = []
for path in Path("Lokum1.0/Knowledge").glob("*.md"):
    if path.name == "LokumAI-1.0.md":
        continue
    text = path.read_text(encoding="utf-8")
    if "LokumAI-1.0" in text:
        bad.append(path.name)
print(bad)
PY
```

Expected:
- output `[]`

- [ ] **Step 4: Confirm phase deliverables**

Check that all exist:
- `50+` raw memory cells
- `H3_*` synthesis notes
- validator report
- index layer notes

- [ ] **Step 5: Stop and report**

Report:
- total new raw nodes
- total new synthesis nodes
- total new forward synapses
- validator summary
- created index files

Do not expand into `hidden_4+` in this execution cycle.

---

## Self-review

### Spec coverage
- Phase 1 research wave: covered by Task 2
- Phase 2 hidden_3 synthesis: covered by Task 3
- Phase 3 automatic validator: covered by Task 4
- Phase 4 index/navigation: covered by Task 5
- sequential subagent model: enabled by the task-by-task phase layout

### Placeholder scan
- No `TBD`, `TODO`, or “implement later” placeholders remain.

### Type consistency
- Raw nodes use `RAG_Memory_Cell_*`
- Synthesis nodes use `H3_*`
- validator is report-first
- `LokumAI-1.0.md` remains immutable throughout
