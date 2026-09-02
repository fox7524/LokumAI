from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from tools.brain_growth import common


H9_GLOB = "H9_*.md"
OUTPUT_SECTION_HEADER = "## Paketlenen çıktı yolları"


def _clean_scalar(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def _clean_list(values: object) -> tuple[str, ...]:
    if not isinstance(values, list):
        return ()
    cleaned: list[str] = []
    for item in values:
        cleaned_item = _clean_scalar(item)
        if cleaned_item:
            cleaned.append(cleaned_item)
    return tuple(cleaned)


def _extract_section(text: str, header: str) -> str:
    lines = text.splitlines()
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == header:
            start_index = index + 1
            break
    if start_index is None:
        return ""

    collected: list[str] = []
    for line in lines[start_index:]:
        if line.startswith("## "):
            break
        collected.append(line)
    return "\n".join(collected).strip()


@dataclass(frozen=True)
class H9ExecutionPackage:
    package_id: str
    path: str
    package_mode: str
    source_policy: str
    delivery_surfaces: tuple[str, ...]
    package_contracts: tuple[str, ...]
    outputs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        # dataclasses -> tuples become lists; we want stable JSON-like objects
        return data


def load_h9_package(path: Path, *, knowledge_dir: Path = common.KNOWLEDGE_DIR) -> H9ExecutionPackage:
    text = common.read_note_text(path)
    common.assert_no_forbidden_nodes(text)

    frontmatter = common.parse_yaml_frontmatter(text)
    package_mode = _clean_scalar(frontmatter.get("package_mode", ""))
    source_policy = _clean_scalar(frontmatter.get("source_policy", ""))
    delivery_surfaces = _clean_list(frontmatter.get("delivery_surfaces", []))
    package_contracts = tuple(sorted(_clean_list(frontmatter.get("package_contracts", []))))

    # Runtime açısından "delivery surface" bir gerçek hedef; varlığını burada zorunlu kılıyoruz.
    missing_surfaces = [
        surface for surface in delivery_surfaces if not (knowledge_dir / f"{surface}.md").exists()
    ]
    if missing_surfaces:
        raise FileNotFoundError(f"Eksik delivery surface notları: {', '.join(missing_surfaces)}")

    output_section = _extract_section(text, OUTPUT_SECTION_HEADER)
    outputs = tuple(common.parse_wikilinks(output_section))

    return H9ExecutionPackage(
        package_id=path.stem,
        path=str(path),
        package_mode=package_mode,
        source_policy=source_policy,
        delivery_surfaces=delivery_surfaces,
        package_contracts=package_contracts,
        outputs=outputs,
    )


def build_execution_plan(*, knowledge_dir: Path = common.KNOWLEDGE_DIR) -> dict[str, Any]:
    packages: list[H9ExecutionPackage] = []
    for path in sorted(knowledge_dir.glob(H9_GLOB), key=lambda item: item.name):
        packages.append(load_h9_package(path, knowledge_dir=knowledge_dir))

    surface_index: dict[str, list[str]] = {}
    for package in packages:
        for surface in package.delivery_surfaces:
            surface_index.setdefault(surface, []).append(package.package_id)

    for surface in surface_index:
        surface_index[surface] = sorted(surface_index[surface])

    return {
        "kind": "execution_plan",
        "package_count": len(packages),
        "packages": [package.to_dict() for package in packages],
        "surface_index": dict(sorted(surface_index.items(), key=lambda item: item[0])),
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="H9 execution paketlerinden dry-run plan üretir.")
    parser.add_argument("--knowledge-dir", type=Path, default=common.KNOWLEDGE_DIR)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    plan = build_execution_plan(knowledge_dir=args.knowledge_dir)

    payload = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

