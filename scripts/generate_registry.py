#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Generate README.md's registry table and registry.json from registry.yaml.

Fails with a non-zero exit code if registry.yaml contains duplicate plugin
names or overlapping rule ID ranges (checks that JSON Schema cannot express).
"""

import json
import re
import sys
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_YAML = ROOT / "registry.yaml"
README = ROOT / "README.md"
REGISTRY_JSON = ROOT / "registry.json"

BEGIN_MARKER = "<!-- BEGIN GENERATED:REGISTRY_TABLE -->"
END_MARKER = "<!-- END GENERATED:REGISTRY_TABLE -->"

TABLE_HEADER = (
    "| *Plugin Name* | *Rule ID Range* | *Repository* | *Type* | *Status* | *CI* | *License* |\n"
    "|---|---|---|---|---|---|---|"
)


def format_range(rule_id_range: dict) -> str:
    return f"{rule_id_range['start']:,} - {rule_id_range['end']:,}"


def format_repository(repository: str) -> str:
    slug = repository.removeprefix("https://github.com/").rstrip("/")
    return f"[{slug}]({repository})"


def format_status(plugin: dict) -> str:
    status = plugin["status"]
    text = "&#9989;&nbsp;tested" if status == "tested" else status.replace("-", " ")
    if plugin.get("private"):
        text += " (Private)"
    return text


def format_ci(plugin: dict) -> str:
    if not plugin.get("ci"):
        return ""
    url = f"{plugin['repository'].rstrip('/')}/actions/workflows/integration.yml/badge.svg"
    return f'<img alt="Integration tests" src="{escape(url, quote=True)}" height="28">'


def render_row(plugin: dict) -> str:
    cells = [
        plugin["name"],
        format_range(plugin["rule_id_range"]),
        format_repository(plugin["repository"]),
        plugin["type"],
        format_status(plugin),
        format_ci(plugin),
        plugin["license"],
    ]
    return "| " + " | ".join(cells) + " |"


def check_no_overlaps(ranges: list[tuple[str, int, int]]) -> list[str]:
    errors = []
    for label, start, end in ranges:
        if start > end:
            errors.append(f"{label}: start ({start}) is after end ({end})")
    by_start = sorted(ranges, key=lambda r: r[1])
    for (label_a, _, end_a), (label_b, start_b, _) in zip(by_start, by_start[1:]):
        if start_b <= end_a:
            errors.append(f"{label_a} and {label_b} have overlapping rule ID ranges")
    return errors


def validate(registry: dict) -> list[str]:
    errors = []

    names = [p["name"] for p in registry["plugins"]]
    seen = set()
    for name in names:
        if name in seen:
            errors.append(f"duplicate plugin name: {name}")
        seen.add(name)

    ranges = [(p["name"], p["rule_id_range"]["start"], p["rule_id_range"]["end"]) for p in registry["plugins"]]
    ranges += [
        (f"reserved({r['rule_id_range']['start']}-{r['rule_id_range']['end']})", r["rule_id_range"]["start"], r["rule_id_range"]["end"])
        for r in registry.get("reserved", [])
    ]
    errors += check_no_overlaps(ranges)

    return errors


def render_readme(registry: dict) -> None:
    readme = README.read_text()
    rows = "\n".join(render_row(p) for p in registry["plugins"])
    table = f"{BEGIN_MARKER}\n{TABLE_HEADER}\n{rows}\n{END_MARKER}"
    pattern = re.compile(re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL)
    if not pattern.search(readme):
        raise SystemExit(f"README.md is missing {BEGIN_MARKER} / {END_MARKER} markers")
    README.write_text(pattern.sub(table, readme))


def render_json(registry: dict) -> None:
    REGISTRY_JSON.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n")


def main() -> None:
    registry = yaml.safe_load(REGISTRY_YAML.read_text())
    errors = validate(registry)
    if errors:
        for error in errors:
            print(f"::error file=registry.yaml::{error}", file=sys.stderr)
        raise SystemExit(1)
    render_readme(registry)
    render_json(registry)


if __name__ == "__main__":
    main()
