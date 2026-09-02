from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from tools.brain_growth import layered_projection, quality_validator
from tools.execution import runtime_executor


ValidatorScope = Literal["h11", "h10", "h9", "h8", "h7", "h6", "h5", "h4", "synthesis", "raw", "index", "all"]


SUPPORTED_VALIDATOR_SCOPES: tuple[str, ...] = (
    "h11",
    "h10",
    "h9",
    "h8",
    "h7",
    "h6",
    "h5",
    "h4",
    "synthesis",
    "raw",
    "index",
    "all",
)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def execute_live(
    *,
    knowledge_dir: Path,
    reports_dir: Path,
    projections_dir: Path,
    write_execution_plan_path: Path,
    validator_scope: ValidatorScope = "h11",
    validator_format: Literal["json", "text"] = "json",
) -> dict[str, Any]:
    """
    "Gerçek executor" ilk sürüm: allowlisted, deterministik işlemler çalıştırır.

    - H9 paketlerinden execution_plan.json üretir
    - brain_growth quality report üretir (scope seçilebilir)
    - layered projection üretir

    Not: Bu sürüm shell/ESP32/dış ağ gibi aksiyonlara dokunmaz.
    """

    if validator_scope not in SUPPORTED_VALIDATOR_SCOPES:
        raise ValueError(f"validator_scope desteklenmiyor: {validator_scope}")

    # 1) Execution plan
    plan = runtime_executor.build_execution_plan(knowledge_dir=knowledge_dir)
    _ensure_parent(write_execution_plan_path)
    write_execution_plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2) Validator report
    report = quality_validator.build_report(scope=str(validator_scope), knowledge_dir=knowledge_dir)
    report_json_path = reports_dir / "brain_growth_validation.json"
    report_txt_path = reports_dir / "brain_growth_validation.txt"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_txt_path.write_text(quality_validator.render_text_report(report) + "\n", encoding="utf-8")

    # 3) Projection outputs
    layered_projection.write_projection_outputs(knowledge_dir=knowledge_dir, output_dir=projections_dir)

    status = "ok" if report["summary"]["issue_count"] == 0 else "fail"
    return {
        "status": status,
        "execution_plan_path": str(write_execution_plan_path),
        "report_paths": [str(report_json_path), str(report_txt_path)],
        "projections_dir": str(projections_dir),
        "validator_scope": validator_scope,
        "issue_count": report["summary"]["issue_count"],
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="LokumAI live executor (allowlisted deterministic actions).")
    parser.add_argument("--knowledge-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--validator-scope", choices=SUPPORTED_VALIDATOR_SCOPES, default="h11")
    args = parser.parse_args(argv)

    out_dir: Path = args.out_dir
    result = execute_live(
        knowledge_dir=args.knowledge_dir,
        reports_dir=out_dir / "reports",
        projections_dir=out_dir / "projections",
        write_execution_plan_path=out_dir / "execution_plan.json",
        validator_scope=args.validator_scope,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())

