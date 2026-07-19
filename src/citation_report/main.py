import datetime
import unicodedata
from collections.abc import Iterator, Mapping

from citation_date import decode_date
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .published_report import REPORT_PATTERN
from .publisher import (
    PUBLISHER_LABELS,
    ReportOffg,
    ReportPhil,
    ReportSCRA,
    get_publisher_label,
)


def is_eq(a: str | None, b: str | None) -> bool:
    """Checks if string `a` is not None, string `b` is not None and both
    `a` and `b` are equal."""
    if a and b:
        if a.lower() == b.lower():
            return True
    return False


def normalize_report_text(text: str) -> str:
    """Normalize report text without promoting compatibility-number footnotes.

    NFC keeps superscript and circled footnote markers distinct from citation
    digits while retaining ordinary Unicode text unchanged.
    """
    return unicodedata.normalize("NFC", text)


class Report(BaseModel):
    """The `REPORT_PATTERN` is a `re.Pattern` object that
    contains pre-defined regex group names. These group names can be mapped
    to the `Report` model's fields:

    Field | Type | Description
    --:|:--:|:--
    `publisher` | optional (str) | Type of the publisher.
    `volume` | optional (str) | Publisher volume number.
    `page` | optional (str) | Publisher volume page.
    `volpubpage` | optional (str) | Combined fields: <volume> <publisher> <page>
    `report_date` | optional (date) | Optional date associated with the report citation

    It's important that each field be **optional**. The `Report` will be joined
    to another `BaseModel` object, i.e. the `Docket`, in a third-party library.
    It must be stressed that the `Report` object is only one part of
    the eventual `DockerReportCitation` object. It can:

    1. have both a `Docket` and a `Report`,
    2. have just a `Docket`;
    3. have just a `Report`.

    If the value of the property exists, it represents whole `@volpubpage` value.

    1. `@phil`
    2. `@scra`
    3. `@offg`
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    publisher: str | None = Field(default=None, max_length=5)
    volume: str | None = Field(
        default=None,
        description="Can exceptionally include letters e.g. vol 1a",
        max_length=10,
    )
    page: str | None = Field(
        default=None,
        description="Page number can have letters, e.g. 241a",
        max_length=6,
    )
    supplement: bool | None = Field(
        default=None,
        description="Whether an Official Gazette citation is from a supplement.",
    )
    issue_number: str | None = Field(
        default=None,
        max_length=4,
        description="Optional Official Gazette issue number.",
    )
    report_date: datetime.date | None = Field(
        default=None,
        description="Exceptionally, report citations reference dates.",
    )

    @field_validator("publisher")
    def publisher_limited_to_phil_scra_offg(cls, v):
        if v and v not in PUBLISHER_LABELS:
            raise ValueError(f"not allowed in options={PUBLISHER_LABELS}")
        return v

    @field_validator("issue_number")
    def issue_number_is_ascii_digits(cls, v):
        if v is not None and (not v.isascii() or not v.isdigit()):
            raise ValueError("issue_number must contain ASCII digits only")
        return v

    @model_validator(mode="after")
    def official_gazette_qualifiers_are_consistent(self):
        if self.supplement and self.issue_number:
            raise ValueError("a report cannot be both a supplement and an issue")
        if (
            self.supplement or self.issue_number
        ) and self.publisher != ReportOffg.label:
            raise ValueError("Official Gazette qualifiers require publisher='O.G.'")
        return self

    def __repr__(self) -> str:
        return f"<Report {self.volpubpage}>"

    def __str__(self) -> str:
        return self.volpubpage or ""

    def __eq__(self, other: object) -> bool:
        """Naive equality checks will only compare direct values,
        exceptionally, when volume, publisher and page are provided,
        must compare all three values with each other.

        Examples:
            >>> a = Report(volume='10', publisher='Phil.', page='25')
            >>> b = Report(volume='10', publisher='Phil.')
            >>> a == b
            False
            >>> c = Report(volume='10', publisher='SCRA', page='25')
            >>> a == c
            False
            >>> d = Report(volume='10', publisher='Phil.', page='25')
            >>> a == d
            True

        Args:
            other (Self): The other Report instance to compare.

        Returns:
            bool: Whether values are equal
        """
        if not isinstance(other, Report):
            return NotImplemented
        if self is other:
            return True

        self_identity = self.qualified_volpubpage
        other_identity = other.qualified_volpubpage
        if self_identity and other_identity:
            return self_identity.casefold() == other_identity.casefold()

        return all(
            getattr(self, field) == getattr(other, field)
            for field in Report.model_fields
        )

    @property
    def has_complete_identity(self) -> bool:
        return all((self.publisher, self.volume, self.page))

    @property
    def phil(self):
        return (
            f"{self.volume} {ReportPhil.label} {self.page}"
            if self.has_complete_identity and self.publisher == ReportPhil.label
            else None
        )

    @property
    def scra(self):
        return (
            f"{self.volume} {ReportSCRA.label} {self.page}"
            if self.has_complete_identity and self.publisher == ReportSCRA.label
            else None
        )

    @property
    def offg(self):
        return (
            f"{self.volume} {ReportOffg.label} {self.page}"
            if self.has_complete_identity and self.publisher == ReportOffg.label
            else None
        )

    @property
    def volpubpage(self):
        return self.phil or self.scra or self.offg

    @property
    def qualified_offg(self) -> str | None:
        if not self.offg:
            return None
        if self.supplement:
            return f"{self.volume} {ReportOffg.label} Supp. {self.page}"
        if self.issue_number:
            return (
                f"{self.volume} {ReportOffg.label} No. "
                f"{self.issue_number}, {self.page}"
            )
        return self.offg

    @property
    def qualified_volpubpage(self) -> str | None:
        return self.phil or self.scra or self.qualified_offg

    @classmethod
    def extract_reports_with_spans(
        cls, text: str, *, text_is_normalized: bool = False
    ) -> Iterator[tuple[tuple[int, int], "Report"]]:
        """Extract complete reports together with their spans in ``text``.

        ``text_is_normalized`` lets callers that already use
        :func:`normalize_report_text` retain offsets into their source string.
        As with :meth:`extract_reports`, incomplete matches are not yielded.
        """
        normalized_text = text if text_is_normalized else normalize_report_text(text)
        for match in REPORT_PATTERN.finditer(normalized_text):
            raw_report_date = match.group("report_date")
            decoded_date = (
                decode_date(raw_report_date, is_output_date_object=True)
                if raw_report_date
                else None
            )
            report_date = (
                decoded_date if isinstance(decoded_date, datetime.date) else None
            )

            publisher = get_publisher_label(match)
            volume = match.group("volume")
            page = match.group("page")
            supplement = True if match.group("OG_SUPPLEMENT") else None
            issue_number = match.group("OG_ISSUE_NUMBER")

            if publisher and volume and page:
                yield match.span(), Report(
                    publisher=publisher,
                    volume=volume,
                    page=page,
                    report_date=report_date,
                    supplement=supplement,
                    issue_number=issue_number,
                )

    @classmethod
    def extract_reports(cls, text: str) -> Iterator["Report"]:
        """Given sample legalese `text`, extract all Supreme Court `Report` patterns.

        Examples:
            >>> sample = "250 Phil. 271, 271-272, Jan. 1, 2019"
            >>> report = next(Report.extract_reports(sample))
            >>> type(report)
            <class 'citation_report.main.Report'>
            >>> report.volpubpage
            '250 Phil. 271'
            >>> unnormalized = "50\xa0 Off. Gaz.,\xa0 583"
            >>> report1 = next(Report.extract_reports(unnormalized))
            >>> report1.volpubpage
            '50 O.G. 583'

        Args:
            text (str): Text containing report citations.

        Yields:
            Iterator["Report"]: Iterator of `Report` instances
        """
        for _, report in cls.extract_reports_with_spans(text):
            yield report

    @classmethod
    def extract_from_dict(
        cls, data: Mapping[object, object], report_type: str
    ) -> str | None:
        """Assuming a dictionary with any of the following report_type keys
        `scra`, `phil` or `offg`, get the value of the Report property.

        Examples:
            >>> sample_data = {"scra": "14 SCRA 314"} # dict
            >>> Report.extract_from_dict(sample_data, "scra")
            '14 SCRA 314'

        Args:
            data (dict): A `dict` containing a possible report `{key: value}`
            report_type (str): Must be either "scra", "phil", or "offg"

        Returns:
            str | None: The value of the key `report_type` in the `data` dict.
        """
        normalized_type = report_type.casefold()
        if normalized_type not in {"scra", "phil", "offg"}:
            return None

        candidate = next(
            (
                value
                for key, value in data.items()
                if isinstance(key, str) and key.casefold() == normalized_type
            ),
            None,
        )
        if not isinstance(candidate, str):
            return None

        for obj in cls.extract_reports(candidate):
            result = getattr(obj, normalized_type)
            if result:
                return result
        return None

    @classmethod
    def get_unique(cls, text: str) -> list[str]:
        """Will only get `Report` volpubpages (string) from the text. This
        is used later in `citation_utils` to prevent duplicate citations.

        Examples:
            >>> text = "(22 Phil. 303; 22 Phil. 303; 176 SCRA 240; Peñalosa v. Tuason, 22 Phil. 303, 313 (1912); Heirs of Roxas v. Galido, 108 Phil. 582 (1960)); Valmonte v. PCSO, supra; Bugnay Const. and Dev. Corp. v. Laron, 176 SCRA 240 (1989)"
            >>> len(Report.get_unique(text))
            3
            >>> set(Report.get_unique(text)) == {'22 Phil. 303', '176 SCRA 240', '108 Phil. 582'}
            True

        Args:
            text (str): Text to search for report patterns

        Returns:
            list[str]: Unique report `volpubpage` strings found in the text
        """  # noqa: E501
        unique: dict[str, str] = {}
        for report in cls.extract_reports(text):
            identity = report.qualified_volpubpage
            if identity:
                unique.setdefault(identity.casefold(), identity)
        return list(unique.values())
