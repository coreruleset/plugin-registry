#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Self-check for scripts/generate_registry.py: semantic validation and rendering safety.

check-jsonschema only catches structural errors; duplicate names and
overlapping rule ID ranges are cross-item constraints it cannot express,
so they are asserted here instead. This also covers rendering-safety
regressions (HTML/markdown escaping, regex-replacement backreferences)
that a schema alone can't guarantee against.
"""

import importlib.util
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("generate_registry", ROOT / "scripts" / "generate_registry.py")
generate_registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_registry)

import yaml


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def check_semantic_validation() -> None:
    registry = load(ROOT / "registry.yaml")
    assert generate_registry.validate(registry) == [], "registry.yaml must be semantically valid"

    duplicate = load(ROOT / "tests/registry/invalid-semantic/duplicate-name.yaml")
    errors = generate_registry.validate(duplicate)
    assert any("duplicate plugin name" in e for e in errors), errors

    overlapping = load(ROOT / "tests/registry/invalid-semantic/overlapping-ranges.yaml")
    errors = generate_registry.validate(overlapping)
    assert any("overlapping rule ID ranges" in e for e in errors), errors


def check_ci_badge_escaping() -> None:
    # registry-schema.json's pattern rules this repository value out today, but
    # the escaping is defense in depth, independent of the schema.
    malicious = {"ci": True, "repository": 'https://github.com/foo/bar" onerror="alert(1)'}
    badge = generate_registry.format_ci(malicious)
    # The tag has exactly three literal attributes (alt=".." src=".." height="..") -> 6 quotes.
    # A leaked, unescaped quote from the malicious value would add 2 more.
    assert badge.count('"') == 6, badge
    assert "&quot;" in badge, badge


def check_repository_link_escaping() -> None:
    malicious = "https://github.com/foo/bar<script>alert(1)</script>"
    rendered = generate_registry.format_repository(malicious)
    assert "<script>" not in rendered, rendered
    assert "&lt;script&gt;" in rendered, rendered


def check_readme_substitution_ignores_backreferences() -> None:
    # A naive `pattern.sub(table, readme)` treats the generated table as a
    # regex replacement string, so a literal "\1" in a rendered row would
    # crash generation (re.error: invalid group reference). Exercise the
    # real render_readme() end to end (not a reimplementation of its
    # substitution) against a temp file, with render_row monkeypatched to
    # return backreference-looking text.
    original_readme_path = generate_registry.README
    original_render_row = generate_registry.render_row
    tmp_path = None
    try:
        fd, name = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        tmp_path = Path(name)
        tmp_path.write_text(f"before\n{generate_registry.BEGIN_MARKER}\nold\n{generate_registry.END_MARKER}\nafter\n")
        generate_registry.README = tmp_path
        generate_registry.render_row = lambda _plugin: r"some \1 backreference-looking text"

        generate_registry.render_readme({"plugins": [{}]})

        result = tmp_path.read_text()
    finally:
        generate_registry.README = original_readme_path
        generate_registry.render_row = original_render_row
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)

    expected_table = (
        f"{generate_registry.BEGIN_MARKER}\n"
        f"{generate_registry.TABLE_HEADER}\n"
        r"some \1 backreference-looking text"
        f"\n{generate_registry.END_MARKER}"
    )
    assert result == f"before\n{expected_table}\nafter\n", result


def main() -> None:
    check_semantic_validation()
    check_ci_badge_escaping()
    check_repository_link_escaping()
    check_readme_substitution_ignores_backreferences()

    print("all checks passed")


if __name__ == "__main__":
    main()
