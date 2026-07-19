import re
from re import Match, Pattern

from pydantic import BaseModel, Field, PrivateAttr

separator = r"[\.,\s]*"


class PublisherStyle(BaseModel):
    """Each publisher is represented by a regex expression `regex`.
    The `group_name` should be present in the `regex`.
    """

    label: str = Field(..., title="Report style", description="Use for uniformity")
    group_name: str = Field(
        ...,
        title="Regex group name",
        description="Custom regex group that identifies the publisher",
    )
    regex: str = Field(
        ...,
        title="Regular expression",
        description=(  # noqa: E501
            "Extract various publisher styles, e.g. 'Phil.' or 'Phil. Report', 'SCRA'"
            " or 'S.C.R.A. All expressions eventually combined in `REPORT_PATTERN`."
        ),
    )
    _pattern_cache: tuple[str, Pattern] | None = PrivateAttr(default=None)

    @property
    def pattern(self) -> Pattern:
        if self._pattern_cache is None or self._pattern_cache[0] != self.regex:
            self._pattern_cache = (self.regex, re.compile(self.regex, re.I | re.X))
        return self._pattern_cache[1]


ReportPhil = PublisherStyle(
    label="Phil.",
    group_name="PHIL_PUB",
    regex=rf"(?P<PHIL_PUB>phil{separator}(?:rep(?:ort(?:s)?)?)?{separator})",
)  # e.g .4 Phil. Rep., 545

ReportSCRA = PublisherStyle(
    label="SCRA",
    group_name="SCRA_PUB",
    regex=r"(?P<SCRA_PUB>(?:SCRA|S\.C\.R\.A\.))",
)

ReportOffg = PublisherStyle(
    label="O.G.",
    group_name="OG_PUB",
    regex=rf"""(?P<OG_PUB>
                (
                    (
                        o
                        {separator}
                        g
                        {separator}
                    )|
                    (
                        off
                        {separator}
                        gaz(ette)?
                        {separator}
                    )
                )
                (
                    (
                        (?P<OG_SUPPLEMENT>suppl?)
                        # Supp. vs. Suppl.; 47 Off. Gaz. Suppl. 12
                        {separator}
                    )|
                    (
                        \(? # 56 OG (No. 4) 1068
                        no # 49 O.G. No. 7, 2740 (1953),
                        {separator} # 46 O.G. No. 11, 90
                        (?P<OG_ISSUE_NUMBER>[0-9]{{1,4}})  # note enclosing brackets
                        \)?
                        {separator}
                    )
                )?
            )
        """,
)

REPORT_STYLES = (ReportPhil, ReportSCRA, ReportOffg)
PUBLISHER_LABELS = tuple(style.label for style in REPORT_STYLES)
PUBLISHER_GROUP_LABELS = tuple(
    (style.group_name, style.label) for style in REPORT_STYLES
)


def get_publisher_label(match: Match) -> str | None:
    """Given a regex match object from `REPORT_PATTERN`,
    determine if it contains a group name representing a Report publisher.

    Examples:
        >>> from citation_report import REPORT_PATTERN, get_publisher_label
        >>> assert REPORT_PATTERN.search("124Phil.1241 statement") is None
        >>> sample = "This is an example 124 Phil. 1241 statement"
        >>> m = REPORT_PATTERN.search(sample)
        >>> m
        <re.Match object; span=(19, 33), match='124 Phil. 1241'>
        >>> label = get_publisher_label(m)
        >>> label
        'Phil.'

    Args:
        match (Match): Based on a prior `re.search` or `re.finditer`
            result on text

    Returns:
        str | None: The first matching publisher found
    """
    for group_name, label in PUBLISHER_GROUP_LABELS:
        if match.group(group_name):
            return label
