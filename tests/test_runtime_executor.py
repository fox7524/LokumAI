from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.execution import runtime_executor


def test_load_h9_package_parses_frontmatter_and_outputs(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    # Delivery surface target notes must exist to be valid.
    (knowledge_dir / "Executive_Action_Formatter.md").write_text("# EAF\n", encoding="utf-8")
    (knowledge_dir / "Final_Execution_Gate.md").write_text("# FEG\n", encoding="utf-8")
    (knowledge_dir / "Cognitive_Response_Generator.md").write_text("# CRG\n", encoding="utf-8")

    note = """---
date: "2026-08-31"
tags:
  - "#layer/hidden_9_execution_packaging"
  - "#execution/package_contract"
  - "#execution/delivery_surface"
  - "#policy/surface_binding"
  - "#execution/commit_readiness"
package_mode: "commit_ready_gate_delivery"
source_policy: "causal_commitment_delivery_gate"
delivery_surfaces:
  - "Final_Execution_Gate"
  - "Cognitive_Response_Generator"
package_contracts:
  - "commit_readiness_manifest"
  - "causal_release_contract"
---

# Commit Ready Delivery Check

## Paketlenen çıktı yolları

- [[Final_Execution_Gate]]
- [[Cognitive_Response_Generator]]
- [[Executive_Action_Formatter]]
"""

    path = knowledge_dir / "H9_Commit_Ready_Delivery_Check.md"
    path.write_text(note, encoding="utf-8")

    package = runtime_executor.load_h9_package(path, knowledge_dir=knowledge_dir)

    assert package.package_id == "H9_Commit_Ready_Delivery_Check"
    assert package.package_mode == "commit_ready_gate_delivery"
    assert package.source_policy == "causal_commitment_delivery_gate"
    assert package.delivery_surfaces == ("Final_Execution_Gate", "Cognitive_Response_Generator")
    assert package.package_contracts == ("causal_release_contract", "commit_readiness_manifest")
    assert package.outputs == (
        "Final_Execution_Gate",
        "Cognitive_Response_Generator",
        "Executive_Action_Formatter",
    )


def test_build_execution_plan_groups_by_surface(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "Executive_Action_Formatter.md",
        "Final_Execution_Gate.md",
        "Cognitive_Response_Generator.md",
        "Global_State_Consensus.md",
        "Working_Memory_Flush.md",
    ):
        (knowledge_dir / name).write_text(f"# {Path(name).stem}\n", encoding="utf-8")

    (knowledge_dir / "H9_A.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_9_execution_packaging"
  - "#execution/package_contract"
  - "#execution/delivery_surface"
  - "#policy/surface_binding"
package_mode: "surface_bound_policy_delivery"
source_policy: "dominant_policy_surface_binding"
delivery_surfaces:
  - "Executive_Action_Formatter"
  - "Final_Execution_Gate"
package_contracts:
  - "surface_route_manifest"
  - "policy_binding_envelope"
---

# A

## Paketlenen çıktı yolları

- [[Executive_Action_Formatter]]
- [[Final_Execution_Gate]]
- [[Cognitive_Response_Generator]]
""",
        encoding="utf-8",
    )

    plan = runtime_executor.build_execution_plan(knowledge_dir=knowledge_dir)

    assert plan["package_count"] == 1
    assert plan["surface_index"]["Final_Execution_Gate"] == ["H9_A"]
    assert plan["surface_index"]["Executive_Action_Formatter"] == ["H9_A"]


def test_build_execution_plan_rejects_forbidden_dictionary_links(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    (knowledge_dir / "Final_Execution_Gate.md").write_text("# FEG\n", encoding="utf-8")
    (knowledge_dir / "Cognitive_Response_Generator.md").write_text("# CRG\n", encoding="utf-8")

    (knowledge_dir / "H9_Bad.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_9_execution_packaging"
  - "#execution/package_contract"
  - "#execution/delivery_surface"
  - "#policy/surface_binding"
package_mode: "commit_ready_gate_delivery"
source_policy: "causal_commitment_delivery_gate"
delivery_surfaces:
  - "Final_Execution_Gate"
  - "Cognitive_Response_Generator"
package_contracts:
  - "commit_readiness_manifest"
  - "causal_release_contract"
---

# Bad

this must not reference [[LokumAI-1.0]]

## Paketlenen çıktı yolları

- [[Final_Execution_Gate]]
- [[Cognitive_Response_Generator]]
- [[Executive_Action_Formatter]]
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Forbidden node reference"):
        runtime_executor.build_execution_plan(knowledge_dir=knowledge_dir)

