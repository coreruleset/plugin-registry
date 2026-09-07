# CRS Plugin Registry Schema

## Overview

`registry.yaml`, at the root of this repository, is the authoritative index of registered CRS
plugins. It is defined by [JSON Schema (2020-12)](https://json-schema.org/draft/2020-12/json-schema-core)
in [`registry-schema.json`](../registry-schema.json). [`README.md`](../README.md)'s table and
[`registry.json`](../registry.json) are both generated from it by
[`scripts/generate_registry.py`](../scripts/generate_registry.py); do not edit either by hand.

This is a separate file with a separate owner from the per-plugin
[`plugin.yaml`](plugin-descriptor-schema.md) descriptor:

- **`registry.yaml`, in this repo** — authoritative for rule ID range allocation and for the
  vetting signal (`type`, `status`). Changed only through reviewed PRs.
- **`plugin.yaml`, in each plugin repository** — authoritative for the plugin's description and
  its configuration variables.

The index stays in this repo rather than being assembled by fetching every plugin repository's
`plugin.yaml`, for three reasons: rule ID ranges have to be allocated centrally to prevent
collisions between plugins that don't know about each other; some registered plugin repositories
are private and cannot be fetched at all; and a plugin repository declaring itself
`status: tested` in its own descriptor attests nothing, while the same field here, set through
review, does.

## What the registry attests, and what it does not

Registering a plugin here means a rule ID range is allocated to it and that CRS maintainers
reviewed the registration (the `type` and `status` fields). That is the extent of it.

**The registry is not a code audit and not a supply-chain guarantee.** Registration does not mean
the plugin's code was reviewed line by line, that its releases are signed, or that its dependencies
were checked. `status: tested` means integration tests exist and pass, not that the plugin is free
of bugs or safe against a malicious release. Installers should resolve to a release tag and record
what they installed; signing or checksums may attach to release tags in a later iteration, but are
out of scope today.

## Fields

Each entry under `plugins` has:

| Field           | Required | Description |
|-----------------|----------|-------------|
| `name`          | yes      | Plugin name as shown in the registry. |
| `rule_id_range` | yes      | `{start, end}` object; both within 9,500,000 - 9,999,999, and not overlapping any other plugin's range or a `reserved` range. |
| `repository`    | yes      | GitHub repository URL. The CI badge and the repository link are both derived from this field, so a swapped or mistyped badge is no longer possible. |
| `type`          | yes      | `official` (coreruleset-maintained) or `3rd-party`. |
| `status`        | yes      | `tested`, `being-tested`, `untested`, or `draft` — the same maturity scale as `plugin.yaml`, but attested here through review rather than self-declared. |
| `ci`            | no       | Whether the repository has a `.github/workflows/integration.yml` workflow. Defaults to `false`; drives whether the generated CI badge is shown. |
| `private`       | no       | Whether the repository is private. Defaults to `false`; shown as `(Private)` next to the status. |
| `license`       | yes      | SPDX license identifier (e.g., `Apache-2.0`, `GPL-2.0`). |

Top-level `reserved` documents rule ID ranges that are intentionally not allocated, each with a
`rule_id_range` and a `note` explaining why (for example, a range vacated by a retired plugin) so
the hole isn't mistaken for a bug and silently reallocated.

## Validation

`registry-schema.json` covers structure: required fields, enums, the rule ID bounds, and the
GitHub repository URL shape. Two constraints it cannot express — unique plugin names, and no
overlapping rule ID ranges across plugins and reserved ranges — are checked separately by
[`scripts/generate_registry.py`](../scripts/generate_registry.py), which fails the same way schema
validation does when it finds a violation. CI runs both, then regenerates `README.md` and
`registry.json` and fails on any drift (`git diff --exit-code`), so the generated files can never
go stale relative to `registry.yaml`.
