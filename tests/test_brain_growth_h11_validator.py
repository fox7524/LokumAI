from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.brain_growth import h11_builder, quality_validator


def test_validate_h11_note_accepts_family_shape(tmp_path: Path) -> None:
    knowledge_dir = tmp_path / "Knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    # Create minimal dependency stubs
    targets = set()
    family = h11_builder.H11_FAMILIES[0]
    targets.update(family.h10_inputs)
    targets.update(family.audit_surfaces)
    targets.update(family.downstream_outputs)
    for target in sorted(targets):
        (knowledge_dir / f"{target}.md").write_text(f"# {target}\n", encoding="utf-8")

    path = knowledge_dir / family.filename
    path.write_text(h11_builder.render_h11_note(family), encoding="utf-8")

    report = quality_validator.validate_h11_note(path, knowledge_dir=knowledge_dir)

    assert report.ok is True
    assert report.kind == "h11"
    assert report.metrics["audit_surfaces"] >= 2
    assert report.metrics["audit_contracts"] >= 2

