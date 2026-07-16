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
| `volpubpage` | Legacy normalized `volume publisher page` form |
| `qualified_volpubpage` | Identity that retains Official Gazette supplement or issue detail |

The three normalized convenience properties (`phil`, `scra`, and `offg`) are
either the matching normalized citation or `None`. `str(report)` returns
`volpubpage` when present.

Official Gazette qualifiers remain available as `supplement` and
`issue_number`. `qualified_volpubpage` distinguishes, for example,
`47 O.G. 43` from `47 O.G. Supp. 43`, while `volpubpage` remains compatible
with the earlier three-part representation.

## Deduplicate Citations

Use `Report.get_unique` when source text can repeat a citation and the caller
only needs normalized identities. It preserves first-seen source order and
uses qualified Gazette identities.

```python
from citation_report import Report

citations = Report.get_unique("22 Phil. 303; 22 Phil. 303; 176 SCRA 240")
assert set(citations) == {"22 Phil. 303", "176 SCRA 240"}
```

## Error Boundaries

`extract_reports` yields only complete report citations. It uses
`citation-date` to decode full dates; calendar-invalid or year-only report
dates leave `report_date` as `None` and do not alter citation identity.

`normalize_report_text` applies NFC only. This preserves superscript and
circled footnote markers as delimiters instead of converting them into page
digits.

Use `get_publisher_label(match)` only when working directly with a prior
`REPORT_PATTERN` match. Most callers should use `Report.extract_reports`,
which applies that step automatically.
