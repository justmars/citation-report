import pytest

from citation_report import REPORT_PATTERN


@pytest.mark.parametrize(
    "data, volume, publisher, page, filler, report_date",
    [
        (
            "250 Phil. 271, 271-272, Jan. 1, 2019",
            "250",
            "Phil.",
            "271",
            "271-272",
            "Jan. 1, 2019",
        ),
        (
            "47 O.G. 2020, 2025, Jan. 1, 2019",
            "47",
            "O.G.",
            "2020",
            "2025",
            "Jan. 1, 2019",
        ),
        (
            "220 SCRA 347, 354, March 23, 1993.",
            "220",
            "SCRA",
            "347",
            "354",
            "March 23, 1993",
        ),
        (
            "224 SCRA 62, 69, June 30, 1993",
            "224",
            "SCRA",
            "62",
            "69",
            "June 30, 1993",
        ),
        (
            "227 SCRA 526, 531, November 8, 1993",
            "227",
            "SCRA",
            "526",
            "531",
            "November 8, 1993",
        ),
        (
            "220 SCRA 347, 356-357, March 23, 1993.",
            "220",
            "SCRA",
            "347",
            "356-357",
            "March 23, 1993",
        ),
        (
            "17 SCRA 914, 919, August 12, 1966",
            "17",
            "SCRA",
            "914",
            "919",
            "August 12, 1966",
        ),
        (
            "42 SCRA 109, 117-118, October 29, 1971;",
            "42",
            "SCRA",
            "109",
            "117-118",
            "October 29, 1971",
        ),
        (
            "60 SCRA 89, 95-96, September 30, 1974.",
            "60",
            "SCRA",
            "89",
            "95-96",
            "September 30, 1974",
        ),
    ],
)
def test_pass_extended_with_full_dates(
    data, volume, publisher, page, filler, report_date
):
    assert (match := REPORT_PATTERN.search(data))
    assert match.group("volume") == volume
    assert match.group("publisher") == publisher
    assert match.group("page") == page
    assert match.group("filler") == filler
    assert match.group("report_date") == report_date
    assert match.group("post_report_full_date") == report_date
    assert match.group("naked_date") == report_date
