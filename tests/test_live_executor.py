from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.execution import live_executor


def test_execute_live_writes_execution_plan_and_brain_growth_reports(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    output_dir = tmp_path / "out"
    reports_dir = output_dir / "reports"
    projections_dir = output_dir / "projections"

    knowledge_dir.mkdir(parents=True, exist_ok=True)

    # Minimal surface notes
    for name in (
        "Final_Execution_Gate.md",
        "Cognitive_Response_Generator.md",
        "Executive_Action_Formatter.md",
        "Global_State_Consensus.md",
        "Long_Term_Strategic_Planner.md",
        "Global_Risk_Assessment.md",
        "Kernel_Panic_Trigger.md",
        "Metacognitive_Reflection_Core.md",
        "Strategic_Resource_Allocator.md",
        "Resource_Lifecycle_Manager.md",
        "Memory_Deallocation_Force.md",
        "Cooling_Fan_Override.md",
        "System_Halt_Interrupt.md",
    ):
        (knowledge_dir / name).write_text(f"# {Path(name).stem}\n", encoding="utf-8")

    # Minimal upstream notes (so validator doesn't choke when scope=all isn't used).
    (knowledge_dir / "H8_Decision.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_8_decision_assembly"
  - "#workspace/global_broadcast"
  - "#decision/dominant_thoughtseed"
  - "#policy/assembly"
workspace_mode: "dominant_policy_broadcast"
dominant_thoughtseed: "x"
candidate_policies:
  - "p"
broadcast_targets:
  - "Final_Execution_Gate"
---

# H8 Decision

## Besleyen H7 düğümleri

- [[H7_Episode]]

## Yayınlanan çıktı yolları

- [[Global_State_Consensus]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "H7_Episode.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_7_episodic_temporal_memory"
  - "#graph/entity_event_dual"
episode_mode: "ordered_episode_reconstruction"
temporal_relations:
  - "before"
primary_entities:
  - "e"
primary_events:
  - "v"
---

# H7 Episode

## Besleyen H6 düğümleri

- [[H6_Exec]]

## Hafıza çıktıları

- [[H8_Decision]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "H6_Exec.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_6_executive_orchestration"
---

# H6 Exec

## Besleyen H5 düğümleri

- [[H5_Control]]

## Koordine ettiği çıktı yolları

- [[H7_Episode]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "H5_Control.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_5_metacognitive_control"
---

# H5 Control

## Besleyen H4 düğümleri

- [[H4_Reason]]

## Yönettiği çıktı yolları

- [[H6_Exec]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "H4_Reason.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_4_reasoning_convergence"
---

# H4 Reason

## Besleyen sentez düğümleri

- [[H3_Synth]]

## İleri yönlü etkiler

- [[H5_Control]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "H3_Synth.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_3_logic_synthesis"
---

# H3 Synth

## Besleyen düğümler

- [[RAG_Memory_Cell_13_Test]]

## İleri besleme

- [[H4_Reason]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "RAG_Memory_Cell_13_Test.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#rag/memory_cell"
  - "#rag/training"
  - "#hardware/apple_mlx"
---

# Raw

## Teknik çekirdek

X

## Doğrulanmış bulgular

- x

## LokumAI için çıkarım

x

## Sorgu ipuçları

- x

## Kaynaklar

- https://example.com
""",
        encoding="utf-8",
    )

    # H9 package
    (knowledge_dir / "H9_Commit_Ready_Delivery_Check.md").write_text(
        """---
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

## Besleyen H8 düğümleri

- [[H8_Decision]]

## Paketlenen çıktı yolları

- [[Final_Execution_Gate]]
- [[Cognitive_Response_Generator]]
- [[Executive_Action_Formatter]]
""",
        encoding="utf-8",
    )

    # H10 + H11 minimal for chain
    (knowledge_dir / "H10_Rollback_Escalation_Governance.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_10_strategic_supervision"
  - "#strategy/supervision_contract"
  - "#strategy/oversight_surface"
  - "#execution/governance_binding"
supervision_mode: "rollback_escalation_governance"
governing_signal: "commit_readiness_escalation"
oversight_surfaces:
  - "Final_Execution_Gate"
  - "Global_Risk_Assessment"
supervision_contracts:
  - "rollback_readiness_contract"
  - "escalation_decision_manifest"
---

# Rollback Escalation Governance

## Stratejik denetim amacı

x

## Governing signal eşlemesi

- x

## Oversight surface sözleşmeleri

- x

## Escalation ve rollback kuralları

- x

## Besleyen H9 düğümleri

- [[H9_Commit_Ready_Delivery_Check]]

## Denetlenen çıktı yolları

- [[Global_Risk_Assessment]]
""",
        encoding="utf-8",
    )

    (knowledge_dir / "H11_Custom_Audit.md").write_text(
        """---
date: "2026-08-31"
tags:
  - "#layer/hidden_11_reflection_audit"
  - "#audit/trace_contract"
  - "#audit/evidence_surface"
  - "#audit/provenance_binding"
reflection_mode: "rollback_decision_audit"
audit_signal: "rollback_escalation_attestation"
audit_surfaces:
  - "Final_Execution_Gate"
  - "Global_Risk_Assessment"
audit_contracts:
  - "rollback_decision_log"
  - "escalation_provenance_bundle"
---

# Custom Audit

## Yansıma amacı

x

## Audit signal eşlemesi

- x

## Evidence surface sözleşmeleri

- x

## İspat ve tutarlılık kuralları

- x

## Besleyen H10 düğümleri

- [[H10_Rollback_Escalation_Governance]]

## Üretilen audit çıktıları

- [[Kernel_Panic_Trigger]]
""",
        encoding="utf-8",
    )

    result = live_executor.execute_live(
        knowledge_dir=knowledge_dir,
        reports_dir=reports_dir,
        projections_dir=projections_dir,
        write_execution_plan_path=output_dir / "execution_plan.json",
        validator_scope="h11",
    )

    assert result["status"] == "ok"
    assert (output_dir / "execution_plan.json").exists()
    assert (reports_dir / "brain_growth_validation.json").exists()
    assert (projections_dir / "brain_growth_layered_projection.json").exists()

    payload = json.loads((output_dir / "execution_plan.json").read_text(encoding="utf-8"))
    assert payload["kind"] == "execution_plan"


def test_execute_live_rejects_unknown_validator_scope(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError, match="validator_scope"):
        live_executor.execute_live(
            knowledge_dir=knowledge_dir,
            reports_dir=tmp_path / "reports",
            projections_dir=tmp_path / "projections",
            write_execution_plan_path=tmp_path / "execution_plan.json",
            validator_scope="nope",
        )
