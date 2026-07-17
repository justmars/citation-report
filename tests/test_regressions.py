from datetime import date

import pytest
from pydantic import ValidationError

from citation_report import REPORT_PATTERN, Report, normalize_report_text


@pytest.mark.parametrize("marker", ["²", "①", "⑵"])
def test_footnote_markers_do_not_change_page_identity(marker):
    raw = f"250 SCRA 271{marker}"

    assert (match := REPORT_PATTERN.fullmatch(raw))
    assert match.group("page") == "271"

    report = next(Report.extract_reports(raw))
    assert report.page == "271"
    assert report.volpubpage == "250 SCRA 271"


def test_normalization_is_idempotent_and_keeps_compatibility_numbers_distinct():
    raw = "250 SCRA 271²"

    assert normalize_report_text(raw) == raw
    assert normalize_report_text(normalize_report_text(raw)) == raw


def test_extract_reports_with_spans_matches_normalized_input():
    raw = "prefix 50\xa0 Off. Gaz.,\xa0 583"
    normalized = normalize_report_text(raw)

    assert list(Report.extract_reports_with_spans(raw)) == list(
        Report.extract_reports_with_spans(normalized, text_is_normalized=True)
    )


def test_extract_reports_with_spans_skips_incomplete_matches(monkeypatch):
    monkeypatch.setattr("citation_report.main.get_publisher_label", lambda match: None)

    assert list(Report.extract_reports_with_spans("42 SCRA 109")) == []
    assert list(Report.extract_reports("42 SCRA 109")) == []


@pytest.mark.parametrize(
    "raw, filler, expected_date",
    [
        ("42 SCRA 109, 29 October 1971", None, date(1971, 10, 29)),
        ("42 SCRA 109, 117-118", "117-118", None),
        (
            "42 SCRA 109, 117-118, October 29, 1971",
            "117-118",
            date(1971, 10, 29),
        ),
        ("42 SCRA 109 (October 29, 1971)", None, date(1971, 10, 29)),
        ("42 SCRA 109 [29 October 1971]", None, date(1971, 10, 29)),
        ("49 O.G. 2740 (1953)", None, None),
        ("42 SCRA 109 February 30, 2000", None, None),
    ],
)
def test_independent_pinpoint_and_date_parsing(raw, filler, expected_date):
    assert (match := REPORT_PATTERN.fullmatch(raw))
    assert match.group("filler") == filler

    report = next(Report.extract_reports(raw))
    assert report.report_date == expected_date


def test_malformed_pinpoint_does_not_fullmatch():
    assert REPORT_PATTERN.fullmatch("42 SCRA 109, ---") is None


def test_malformed_date_never_invents_a_current_year_date():
    report = next(Report.extract_reports("42 SCRA 109 October,,29,1971"))

    assert report.volpubpage == "42 SCRA 109"
    assert report.report_date is None


@pytest.mark.parametrize(
    "raw, expected_page",
    [
        ("1 Phil. Reports 100", "100"),
        ("100 S.C.R.A. 105", "105"),
        ("1 SCRA 241a", "241a"),
        ("122 SCRA 100-A", "100-A"),
    ],
)
def test_documented_publisher_and_page_variants(raw, expected_page):
    assert (match := REPORT_PATTERN.fullmatch(raw))
    assert match.group("page") == expected_page

    report = next(Report.extract_reports(raw))
    assert report.page == expected_page


def test_official_gazette_qualifiers_keep_a_distinct_identity():
    supplement = next(Report.extract_reports("47 O.G. Supp. 43"))
    issue = next(Report.extract_reports("49 O.G. No. 7, 2740"))
    plain = next(Report.extract_reports("47 O.G. 43"))

    assert supplement.supplement is True
    assert supplement.issue_number is None
    assert supplement.volpubpage == "47 O.G. 43"
    assert supplement.qualified_volpubpage == "47 O.G. Supp. 43"
    assert issue.issue_number == "7"
    assert issue.qualified_volpubpage == "49 O.G. No. 7, 2740"
    assert supplement != plain
    assert Report.get_unique("47 O.G. 43; 47 O.G. Supp. 43") == [
        "47 O.G. 43",
        "47 O.G. Supp. 43",
    ]


def test_partial_reports_do_not_render_placeholder_citations():
    partial = Report(publisher="SCRA")

    assert partial.scra is None
    assert partial.volpubpage is None
    assert partial == Report(publisher="SCRA")
    assert partial != None  # noqa: E711


def test_official_gazette_qualifiers_require_official_gazette():
    with pytest.raises(ValidationError):
        Report(publisher="SCRA", volume="1", page="2", supplement=True)


def test_extract_from_dict_is_case_insensitive_and_scans_all_candidates():
    data = {"ScRa": "1 Phil. 2; 14 SCRA 314"}

    assert Report.extract_from_dict(data, "SCRA") == "14 SCRA 314"
    assert Report.extract_from_dict({"scra": 314}, "scra") is None


def test_get_unique_preserves_first_seen_order():
    assert Report.get_unique("22 Phil. 303; 176 SCRA 240; 22 Phil. 303") == [
        "22 Phil. 303",
        "176 SCRA 240",
    ]
