---
icon: lucide/regex
---

# Patterns

`REPORT_REGEX` is the public format string for a report citation. Compile it
with `re.I | re.X`; `REPORT_PATTERN` is the package's already-compiled version
for ordinary matching.

```python
import re

from citation_report import REPORT_REGEX

pattern = re.compile(REPORT_REGEX, re.I | re.X)
```

## Citation Shape

Every report citation has a required volume, publisher, and first page.

| Component | Capture group | Accepted form |
| --- | --- | --- |
| Volume | `volume` | A numeric volume, with the documented `-A` or `a` suffix where observed |
| Publisher | `publisher` | A recognized `Phil.`, `SCRA`, or Official Gazette variant |
| Page | `page` | The report's first page |
| Citation | `volpubpage` | The complete required three-part citation |
| Date | `report_date` | An optional report date supplied by `citation-date` |

For example, `42 SCRA 109, 117-118, October 29, 1971` captures `42 SCRA 109`
as `volpubpage`. The pinpoint material is accepted before the date, but is not
part of the normalized report identity.

## Publisher Variants

The public normalized labels are `Phil.`, `SCRA`, and `O.G.`. The grammar
accepts common source spellings including `Phil. Reports`, `S.C.R.A.`,
`Off. Gaz.`, and `Off. Gazette` where their punctuation follows the observed
forms.

Use the documented named groups when embedding this pattern in a larger regex.
The internal publisher-specific groups (`PHIL_PUB`, `SCRA_PUB`, and `OG_PUB`)
support label normalization and should not be used as a downstream API.

## Compose Safely

`REPORT_REGEX` contains named groups and should appear only once in a composed
regular expression. Use `REPORT_PATTERN` directly when no additional grammar
is needed.

```python
from citation_report import REPORT_PATTERN

match = REPORT_PATTERN.search("1 Phil. Reports 100")
assert match is not None
assert match.group("volpubpage") == "1 Phil. Reports 100"
assert match.group("publisher") == "Phil. Reports"
```
