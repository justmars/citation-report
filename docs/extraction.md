---
icon: lucide/book-open-check
---

# Extracting Reports

`Report.extract_reports` turns report-pattern matches into `Report` models.
The model normalizes the publisher label and preserves the captured volume,
first page, and optional parsed date.

```python
from citation_report import Report

report = next(Report.extract_reports("50 Off. Gazette 583, Jan. 1, 1949"))
assert report.publisher == "O.G."
assert report.volpubpage == "50 O.G. 583"
assert str(report.report_date) == "1949-01-01"
```

## Model Fields

| Field | Meaning |
| --- | --- |
| `publisher` | Normalized `Phil.`, `SCRA`, or `O.G.` label |
| `volume` | Captured report volume |
| `page` | Captured first report page |
| `report_date` | Optional `datetime.date` parsed from the report citation |
| `volpubpage` | Normalized `volume publisher page` identity |

The three normalized convenience properties (`phil`, `scra`, and `offg`) are
either the matching normalized citation or `None`. `str(report)` returns
`volpubpage` when present.

## Deduplicate Citations

Use `Report.get_unique` when source text can repeat a citation and the caller
only needs normalized identities.

```python
from citation_report import Report

citations = Report.get_unique("22 Phil. 303; 22 Phil. 303; 176 SCRA 240")
assert set(citations) == {"22 Phil. 303", "176 SCRA 240"}
```

## Error Boundaries

`extract_reports` yields only complete report citations. It silently skips
date strings that `dateutil` cannot turn into a calendar date, leaving
`report_date` as `None`; it does not alter the matched citation identity.

Use `get_publisher_label(match)` only when working directly with a prior
`REPORT_PATTERN` match. Most callers should use `Report.extract_reports`,
which applies that step automatically.
