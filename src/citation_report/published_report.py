import re
from re import Pattern

from citation_date import REPORT_DATE_REGEX, uk_pattern

from .publisher import REPORT_STYLES

PUBLISHERS_REGEX = rf"""
    (?P<publisher>
        {"|".join(style.regex for style in REPORT_STYLES)}
    )
"""
"""A partial regex string containing the Publisher options available."""


volume = r"""
    \b
    (?P<volume>
        [12]? # makes possible from 1000 to 2999
        [0-9]{1,3}
        (
            \-A| # See Central Bank v. CA, 159-A Phil. 21, 34 (1975);
            a
        )?
    )
    \b
"""

footnote_marker = r"[⁰¹²³⁴⁵⁶⁷⁸⁹①-⑳⑴-⒇]"

page = rf"""
    (?P<page>
        [12345]? # makes possible from 1000 to 5999
        [0-9]{{1,3}}  # 49 Off. Gazette 4857
        (?:-?A)?
    )
    (?!-[A-Za-z0-9])
    (?![A-Za-z0-9_])
    (?:\b|(?={footnote_marker}))
"""

volpubpage = rf"""
    (?P<volpubpage>
        {volume}
        \s+
        {PUBLISHERS_REGEX}
        \s+
        {page}
    )
"""

footnote_suffix = rf"(?:{footnote_marker})?"

filler = (
    r"""
    (?P<filler>
        (?!"""
    + uk_pattern.pattern
    + r""")
        [0-9]{1,4}
        (?:-[0-9]{1,4})?
    )
"""
)

separator = r"(?:\s*,\s*|\s+)"

extra = rf"""
    (?:{separator}{filler})?
    (?:{separator}{REPORT_DATE_REGEX})?
"""

REPORT_REGEX = rf"{volpubpage}{footnote_suffix}{extra}"

REPORT_PATTERN: Pattern = re.compile(REPORT_REGEX, re.X | re.I)
"""A compiled regex expression that enables capturing the
parts of a report.

Examples:
    >>> from citation_report import REPORT_PATTERN
    >>> text = "42 SCRA 109, 117-118, October 29, 1971;"
    >>> sample_match = REPORT_PATTERN.search(text)
    >>> sample_match.group("volpubpage")
    '42 SCRA 109'
    >>> sample_match.group("volume")
    '42'
    >>> sample_match.group("publisher")
    'SCRA'
    >>> sample_match.group("page")
    '109'
    >>> sample_match.group("report_date")
    'October 29, 1971'
"""
