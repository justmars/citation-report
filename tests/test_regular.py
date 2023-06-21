import pytest

from citation_report import REPORT_PATTERN


@pytest.mark.parametrize(
    "raw_text, volume, publisher, page",
    [
        ("250 SCRA 271", "250", "SCRA", "271"),
        ("1 SCRA 2", "1", "SCRA", "2"),
        ("1-A SCRA 1", "1-A", "SCRA", "1"),
        ("1a Phil. 3", "1a", "Phil.", "3"),
        ("2 Phil. 3", "2", "Phil.", "3"),
        ("2 o.g. 630", "2", "o.g.", "630"),
        ("47 O.G. 2020", "47", "O.G.", "2020"),
        ("47 O.G. Supp. 43", "47", "O.G. Supp.", "43"),
        ("1 Off. Gaz. Suppl. 12", "1", "Off. Gaz. Suppl.", "12"),
        ("46 O.G. No. 11, 90", "46", "O.G. No. 11,", "90"),
        ("49 O.G. No. 7, 2740 (1953)", "49", "O.G. No. 7,", "2740"),
        ("56 OG (No. 4) 1068", "56", "OG (No. 4)", "1068"),
        ("49 Off. Gazette 4857", "49", "Off. Gazette", "4857"),
    ],
)
def test_reports(raw_text, volume, publisher, page):
    assert (match := REPORT_PATTERN.fullmatch(raw_text))
    assert match.group("volume") == volume
    assert match.group("publisher") == publisher
    assert match.group("page") == page


@pytest.mark.parametrize(
    "data, volume, publisher, page, filler, date",
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
def test_pass_extended_with_full_dates(data, volume, publisher, page, filler, date):
    assert (match := REPORT_PATTERN.search(data))
    assert match.group("volume") == volume
    assert match.group("publisher") == publisher
    assert match.group("page") == page
    assert match.group("filler") == filler
    assert match.group("report_date") == date
    assert match.group("post_report_full_date") == date
    assert match.group("naked_date") == date
