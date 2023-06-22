from datetime import date

import pytest

from citation_report import Report


@pytest.mark.parametrize(
    "data, volume, publisher, page, report_date",
    [
        (
            "250 Phil. 271, 271-272, Jan. 1, 2019",
            "250",
            "Phil.",
            "271",
            date(year=2019, month=1, day=1),
        ),
    ],
)
def test_get_reports(data, volume, publisher, page, report_date):
    report = next(Report.extract_reports(data))
    assert isinstance(report, Report)
    assert report.volume == volume
    assert report.publisher == publisher
    assert report.page == page
    assert report.report_date == report_date
    assert report.__str__() == "250 Phil. 271"
    assert not report.scra
    assert report.phil == "250 Phil. 271"
