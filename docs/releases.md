---
icon: lucide/tags
---

# Release Notes

## 1.0.0 — 2026-07-19

This release compares `1.0.0` with `0.2.0` at commit `02af311`, the last
pushed `main` revision before the current development line. It consolidates
the six subsequent parser, documentation, build, and CI commits into one
public release boundary. The intermediate `0.3.0` and `0.4.0` metadata were
never pushed to `main` as separate release boundaries.

### At a Glance

| Area | 0.2.0 | 1.0.0 |
| --- | --- | --- |
| Python | 3.13 or newer | 3.14 or newer |
| Date parsing | Direct `python-dateutil` parsing | Deterministic `citation-date >=1.0.0` decoding |
| Text normalization | NFKD compatibility decomposition | NFC through `normalize_report_text` |
| Extraction result | Normalized `Report` models | Models, plus source-ordered occurrence spans |
| Official Gazette identity | Supplement and issue details collapsed | Qualified supplement and issue identities retained |
| Deduplication | Unordered, three-part identities | First-seen order and qualified identities |
| Documentation | MkDocs and a Jupyter notebook | Strict Zensical site and a checked Marimo explorer |
| Package checks | Tests and linting | Tests, doctests, notebook, docs, distributions, and wheel import |

### Breaking Changes and Migration

- Python 3.13 support is removed. Use Python 3.14 or newer.
- The minimum dependencies are now `citation-date >=1.0.0` and
  `pydantic >=2.13.0`. The direct `python-dateutil` dependency is removed.
- `Report.get_unique()` now preserves first-seen order and uses qualified
  Official Gazette identities. Callers must not expect arbitrary set order or
  expect plain and supplement citations to collapse together.
- Complete Official Gazette identity is exposed through
  `qualified_volpubpage`. The legacy three-part `volpubpage` remains available
  when a caller intentionally wants qualifier-free compatibility.
- Partial models no longer render placeholder strings such as
  `"None SCRA None"`. Their reporter properties and `volpubpage` are `None`.
- Report equality now distinguishes qualified Gazette citations and safely
  returns `False` for unrelated values instead of raising an attribute error.
- `REPORT_REGEX` and `REPORT_PATTERN` retain their documented named capture
  groups, but the citation tail is stricter: a pinpoint and a date are
  independent optional suffixes, and malformed tails are not accepted as full
  matches. Downstream compositions should use named groups rather than numeric
  group positions.

### Features

- `normalize_report_text(text)` is exported as the shared NFC normalization
  boundary for report extraction.
- `Report.extract_reports_with_spans(text, *, text_is_normalized=False)` yields
  `((start, end), Report)` occurrences in source order. Callers that normalize
  once can pass `text_is_normalized=True` to keep offsets aligned.
- `Report` adds `supplement` and `issue_number` fields plus `qualified_offg`
  and `qualified_volpubpage` properties.
- Publisher grammar now recognizes documented variants such as
  `Phil. Reports` and `S.C.R.A.`.
- Page grammar accepts observed lettered forms such as `241a` and `100-A`, and
  treats superscript or circled footnote markers as boundaries rather than
  digits.
- A checked Marimo and Polars report explorer replaces the obsolete Jupyter
  notebook.

### Corrections and Bug Fixes

- NFC normalization prevents superscript and circled footnotes from becoming
  page digits before parsing.
- Dates are decoded through `citation-date`; invalid or malformed dates remain
  `None` instead of being interpreted heuristically.
- A report may now have a pinpoint without a date, a date without a pinpoint,
  or both.
- Plain, supplement, and numbered-issue Official Gazette citations remain
  distinct during equality and deduplication.
- `extract_from_dict()` matches keys and requested report types without case
  sensitivity, rejects non-string candidates safely, and scans the candidate
  until it finds the requested reporter.
- `get_unique()` returns stable first-seen order.
- Publisher regex patterns are cached and automatically recompiled if their
  source expression changes.

### Before and After

#### Footnote markers no longer change page identity

```python
from citation_report import Report

# 0.2.0
next(Report.extract_reports("250 SCRA 271²")).page
# '2712'

# 1.0.0
next(Report.extract_reports("250 SCRA 271²")).page
# '271'
```

#### Official Gazette qualifiers remain distinct

```python
from citation_report import Report

source = "47 O.G. 43; 47 O.G. Supp. 43"

# 0.2.0
Report.get_unique(source)
# ['47 O.G. 43']

# 1.0.0
Report.get_unique(source)
# ['47 O.G. 43', '47 O.G. Supp. 43']
```

Use the qualified property when a complete identity is required:

```python
report = next(Report.extract_reports("49 O.G. No. 7, 2740"))
assert report.volpubpage == "49 O.G. 2740"
assert report.qualified_volpubpage == "49 O.G. No. 7, 2740"
```

#### Dictionary extraction is case-insensitive and reporter-aware

```python
from citation_report import Report

data = {"ScRa": "1 Phil. 2; 14 SCRA 314"}

# 0.2.0
Report.extract_from_dict(data, "SCRA")
# None

# 1.0.0
Report.extract_from_dict(data, "SCRA")
# '14 SCRA 314'
```

#### Partial models and unrelated comparisons are safe

```python
from citation_report import Report

partial = Report(publisher="SCRA")

# 0.2.0
partial.volpubpage
# 'None SCRA None'
# partial == None raised AttributeError

# 1.0.0
assert partial.volpubpage is None
assert (partial == None) is False  # noqa: E711
```

#### Documented variants and pinpoint-only citations are complete matches

```python
from citation_report import REPORT_PATTERN

# Both were False in 0.2.0 and are True in 1.0.0.
assert REPORT_PATTERN.fullmatch("1 Phil. Reports 100") is not None
assert REPORT_PATTERN.fullmatch("42 SCRA 109, 117-118") is not None
```

#### Occurrences now preserve source offsets

```python
from citation_report import Report

source = "See 50 Off. Gazette 583 and 22 Phil. 303."
span, report = next(Report.extract_reports_with_spans(source))

assert span == (4, 23)
assert source[slice(*span)] == "50 Off. Gazette 583"
assert report.qualified_volpubpage == "50 O.G. 583"
```

`extract_reports_with_spans()` did not exist in `0.2.0`; callers previously
had to search the text a second time to recover occurrence offsets.

### Engineering and Documentation Improvements

- The package now builds through `uv_build`, and CI verifies both source and
  wheel distributions plus an import from the built wheel.
- The repository gate covers tests and doctests, the Marimo notebook, a strict
  Zensical build, and package construction.
- Documentation is split into overview, regex composition, structured
  extraction, release, and development paths, with tests requiring every page
  to appear exactly once in navigation.
- Maintained documentation is prevented from depending on temporary plan
  files.
