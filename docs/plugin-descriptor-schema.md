# CRS Plugin Descriptor Schema

## Overview

The plugin descriptor schema defines a `plugin.yaml` file that lives in the root of each CRS plugin repository. It provides machine-readable metadata about the plugin, its configuration variables, and compatibility requirements.

The plugin registry aggregates these descriptors to generate the registry table, and downstream tooling (such as a CRS configurator) can parse them to build preconfigured CRS deployments based on plugin selection.

## Goals

- Allow each plugin repository to be the single source of truth for its own metadata.
- Enable automated tooling to discover, validate, and configure plugins.
- Replace manual registry table maintenance with generated output.
- Provide enough information for a configurator to present a UI for plugin selection and variable tuning.

## Schema Structure

The schema is defined as [JSON Schema (2020-12)](https://json-schema.org/draft/2020-12/json-schema-core) in [`plugin-schema.json`](../plugin-schema.json). A `plugin.yaml` file has the following top-level sections:

### `schema_version`

**Required.** Integer, currently fixed at `1`.

Allows future evolution of the schema without breaking existing parsers. Tooling should check this field and handle unknown versions gracefully.

### `plugin`

**Required.** Plugin identity and metadata.

| Field              | Required | Description |
|--------------------|----------|-------------|
| `name`             | yes      | Plugin name following the CRS convention: `<name>-plugin`. Validated by regex. |
| `description`      | yes      | One-line summary of the plugin's purpose. |
| `long_description` | no       | Multi-line extended description for documentation and UI display. |
| `type`             | yes      | `official` (coreruleset-maintained) or `3rd-party`. |
| `category`         | no       | Functional category: `rule-exclusion`, `detection`, `protection`, `utility`, `logging`, or `performance`. |
| `status`           | yes      | Maturity level: `tested`, `being-tested`, `untested`, or `draft`. |
| `license`          | yes      | SPDX license identifier (e.g., `Apache-2.0`, `GPL-2.0-only`). |
| `authors`          | yes      | List of author objects with `name` (required), `email` and `url` (optional). |
| `repository`       | yes      | URL of the plugin source repository. |
| `homepage`         | no       | URL to documentation or project site. |
| `keywords`         | no       | Tags for discovery and categorization. |

### `rule_id_range`

**Required.** The registered rule ID block from the plugin registry.

| Field   | Description |
|---------|-------------|
| `start` | First rule ID in the allocated range (integer, 9500000-9999999). |
| `end`   | Last rule ID in the allocated range (integer, 9500000-9999999). |

Plugins typically receive a 1,000-ID range. The schema validates that values fall within the CRS plugin namespace (9,500,000 - 9,999,999).

### `compatibility`

**Optional.** WAF engine and CRS version requirements.

| Field         | Description |
|---------------|-------------|
| `crs_version` | Version constraint string (e.g., `>=4.0.0`). |
| `engines`     | List of compatible WAF engines, each one of: `modsecurity2`, `modsecurity3`, or `coraza`. |

When omitted, no compatibility constraints are assumed. Tooling should treat missing engines as "compatible with all".

### `dependencies`

**Optional.** List of other CRS plugins this plugin depends on.

Each entry has:
| Field     | Required | Description |
|-----------|----------|-------------|
| `name`    | yes      | Name of the required plugin. |
| `version` | no       | Version constraint for the dependency. |

Most plugins have no dependencies. This field exists for plugins that build on top of other plugins.

### `configuration`

**Required.** The key section for automated tooling. Describes the config file and all user-tunable variables.

| Field       | Description |
|-------------|-------------|
| `file`      | Path to the `-config.conf` file relative to the plugin root. |
| `variables` | List of transaction variable definitions (see below). |

#### Variable Definition

Each entry in `variables` describes a single `tx.*` variable from the config file:

| Field            | Required | Description |
|------------------|----------|-------------|
| `name`           | yes      | Full ModSecurity variable name (e.g., `tx.myplugin_enabled`). |
| `type`           | yes      | Data type: `boolean`, `integer`, `string`, `list`, or `enum`. |
| `default`        | no       | Default value if not set by the user. |
| `description`    | yes      | Human-readable explanation of the variable. |
| `required`       | no       | Whether the user must explicitly set this variable (default: `false`). |
| `allowed_values` | no       | List of valid values when type is `enum`. |
| `separator`           | no       | String used to separate multiple entries when type is `list`. |
| `prefix`                 | no       | String marking the beginning of a list entry when type is `list`. |
| `suffix`                 | no       | String marking the end of a list entry when type is `list`. |
| `example`        | no       | Example value for documentation. |
| `min`            | no       | Minimum value when type is `integer`. |
| `max`            | no       | Maximum value when type is `integer`. |

#### Variable Types

The four types cover all patterns found across existing CRS plugins:

- **`boolean`** — Enable/disable flags. Every plugin has at least `tx.<name>_enabled`. Values are integers: `0` (disabled) or `1` (enabled), following the ModSecurity convention for boolean flags.
- **`integer`** — Numeric thresholds and limits (e.g., `tx.body-decompress-plugin_max_data_size_bytes`). Supports `min`/`max` constraints.
- **`string`** — Freeform text values. The `example` field helps users understand the expected format.
- **`list`** — Structured list of strings (e.g., `tx.google-oauth2-plugin_whitelisted_parameters`). The fields `separator`, `prefix`, `suffix` define the format. For example, the list `|a/ |b/ |c/` would be defined as follows:
  - `separator`: `" "` (space character)
  - `prefix`: `"|"`
  - `suffix`: `"/"`
- **`enum`** — Constrained choices (e.g., `tx.phpmyadmin-rule-exclusions-plugin_url_format` with values `v51`, `v52`). Must include `allowed_values`.

## Design Decisions

### Why YAML over JSON or TOML?

YAML supports comments, multi-line strings, and is widely used in the CRS ecosystem (test files use FTW YAML format). Plugin authors already work with YAML for regression tests, so it is familiar.

### Why `schema_version` as a top-level field?

Embedding versioning in the schema itself allows parsers to detect incompatible changes before attempting to parse. This is simpler than relying on file naming or external version tracking.

### Why typed variables with constraints?

A configurator project needs to know more than just variable names and defaults. By declaring types, allowed values, and numeric bounds, tooling can:

1. Render appropriate input widgets (toggle for boolean, slider for bounded integer, dropdown for enum).
2. Validate user input before generating configuration.
3. Generate documentation automatically.

### Why is `configuration` required?

Every CRS plugin has at least one configuration variable (`tx.<name>_enabled`). Making this section required ensures consistency and guarantees that tooling always has something to work with, even for minimal rule-exclusion plugins.

### Why no `version` field?

The plugin version is derived from GitHub release tags at query time. Embedding a version in `plugin.yaml` would inevitably drift because developers forget to bump it. Tooling should fetch the latest release tag from the repository URL instead. This keeps `plugin.yaml` as a static descriptor that rarely needs updating.

### Why separate `rule_id_range` from `plugin`?

The rule ID range is a registry-level concern (namespace coordination), not a plugin identity attribute. Keeping it separate makes it clear that this range is allocated by the registry and should not be changed unilaterally.

### Category taxonomy

The six categories cover the existing plugin landscape:

| Category         | Examples |
|------------------|----------|
| `rule-exclusion` | wordpress, drupal, nextcloud, phpbb, cpanel |
| `detection`      | fake-bot |
| `protection`     | dos-protection |
| `utility`        | template, body-decompress, auto-decoding |
| `logging`        | database-logging, false-positive-report |
| `performance`    | performance-plugin |

New categories can be added to the schema's enum as the ecosystem grows.

## Configurator Integration

The primary consumer of `plugin.yaml` files is a configurator tool that:

1. **Fetches** `plugin.yaml` from each registered plugin repository.
2. **Presents** available plugins grouped by category, with descriptions and compatibility info.
3. **Collects** user choices: which plugins to enable and how to tune their variables.
4. **Validates** input against variable constraints (type, min/max, allowed_values).
5. **Resolves** dependencies between plugins.
6. **Generates** a complete CRS configuration with all selected plugins and their tuned `tx.*` variables.

## Rollout Plan

1. Add `plugin.yaml` to `coreruleset/template-plugin` as the reference implementation.
2. Get feedback from the CRS team and iterate on the schema.
3. Once the schema is accepted, create PRs adding `plugin.yaml` to all registered plugins.
4. Update the registry to validate incoming plugin registrations against the schema.
5. Build the configurator project.
