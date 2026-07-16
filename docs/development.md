---
icon: lucide/wrench
---

# Development

## Setup

Use Python 3.14 and install the package with uv:

```bash
uv sync --all-extras --dev
```

Run the repository gates with:

```bash
just check
```

This runs the test and doctest suite, validates the Marimo notebook, builds a
strict Zensical site, and produces a source and wheel distribution.

## Documentation

Preview documentation locally:

```bash
just docs
```

Build the static site without starting a server:

```bash
uv run zensical build --clean --strict
```

## Notebook Examples

`notebooks/report_explorer.py` is a Marimo example backed by a Polars frame.
Start it with:

```bash
uv run marimo edit notebooks/report_explorer.py
```

It is a review and exploration surface only; the package API remains the
regex and `Report` model exported from `citation_report`.

## Change Boundaries

Keep the public contract small and explicit:

- `REPORT_REGEX` and `REPORT_PATTERN` are composition surfaces for downstream
  citation parsers.
- The documented named capture groups are part of that contract.
- `Report` owns normalized report identities and extraction behavior.
- Publisher variants must have fixture-backed acceptance and nearby rejection
  cases before the grammar is widened.
