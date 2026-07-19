![Github CI](https://github.com/justmars/citation-report/actions/workflows/ci.yml/badge.svg)

# Citation Report Parser

`citation-report` provides regex patterns and structured extraction for
Philippine Supreme Court report citations: Philippine Reports (`Phil.`),
Supreme Court Reports Annotated (`SCRA`), and the Official Gazette (`O.G.`).
It is used with [citation-date](https://github.com/justmars/citation-date) in
the [LawSQL dataset](https://lawsql.com).

The package isolates report-citation grammar so downstream parsers can compose
the pattern without duplicating publisher variants or date handling.

## Quick Example

```python
from citation_report import Report

report = next(Report.extract_reports("250 Phil. 271, Jan. 1, 2019"))
assert report.volpubpage == "250 Phil. 271"
assert str(report.report_date) == "2019-01-01"
```

## Documentation

See the [documentation](https://justmars.github.io/citation-report) for
pattern composition, extraction behavior, and development commands. The
[1.0 release notes](https://justmars.github.io/citation-report/releases/)
compare the current public contract with the last pushed `0.2.0` release.

## Testing

```sh
uv sync --all-extras --dev
just check
```
