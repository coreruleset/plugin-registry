#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Self-check for the semantic validation in scripts/generate_registry.py.

check-jsonschema only catches structural errors; duplicate names and
overlapping rule ID ranges are cross-item constraints it cannot express,
so they are asserted here instead.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("generate_registry", ROOT / "scripts" / "generate_registry.py")
generate_registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_registry)

import yaml


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def main() -> None:
    registry = load(ROOT / "registry.yaml")
    assert generate_registry.validate(registry) == [], "registry.yaml must be semantically valid"

    duplicate = load(ROOT / "tests/registry/invalid-semantic/duplicate-name.yaml")
    errors = generate_registry.validate(duplicate)
    assert any("duplicate plugin name" in e for e in errors), errors

    overlapping = load(ROOT / "tests/registry/invalid-semantic/overlapping-ranges.yaml")
    errors = generate_registry.validate(overlapping)
    assert any("overlapping rule ID ranges" in e for e in errors), errors

    print("all checks passed")


if __name__ == "__main__":
    main()
