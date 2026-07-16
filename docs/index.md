# Citation Report

`citation-report` recognizes report citations from Philippine Supreme Court
decision repositories and returns their normalized report form. It composes
the report-date grammar from
[citation-date](https://github.com/justmars/citation-date), while keeping the
publisher grammar and report extraction local to this package.

## Reader Paths

=== "Compose a report regex"

    1. Read [Patterns](patterns.md) for the public regex constants and capture groups.
    2. Compile `REPORT_REGEX` with `re.I | re.X` when composing it into a larger expression.
    3. Use named captures; numeric group positions are internal.

=== "Extract structured reports"

    1. Read [Extracting reports](extraction.md) for `Report` and its normalized properties.
    2. Pass source text to `Report.extract_reports`.
    3. Preserve the original text when it is needed as evidence.

## Supported Repositories

| Normalized label | Repository | Status |
| --- | --- | --- |
| `Phil.` | Philippine Reports | Official reporter |
| `SCRA` | Supreme Court Reports Annotated | Private reporter |
| `O.G.` | Official Gazette | Official publication |

The grammar recognizes observed publisher variants, such as `Phil. Reports`
and `Off. Gazette`, then normalizes them to these labels. A matched citation is
always anchored by a volume, publisher, and page; a date and pinpoint material
may follow it.

## Quick Example

```python
from citation_report import Report

reports = list(Report.extract_reports("42 SCRA 109, 117-118, October 29, 1971"))
assert reports[0].volpubpage == "42 SCRA 109"
assert str(reports[0].report_date) == "1971-10-29"
```

The parser returns the citation's first page, not subsequent pinpoint pages.
`Report.get_unique` is available when a caller only needs deduplicated
normalized citation strings.
