import marimo


__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from citation_report import Report

    return Report, mo, pl


@app.cell
def _(mo):
    mo.md("""
    # Report citation explorer

    This read-only example normalizes common Philippine report citation forms.
    """)
    return


@app.cell
def _(Report, pl):
    sources = pl.DataFrame(
        {
            "citation": [
                "250 Phil. 271, Jan. 1, 2019",
                "42 SCRA 109, 117-118, October 29, 1971",
                "50 Off. Gazette 583, Jan. 1, 1949",
            ]
        }
    )
    reports = pl.DataFrame(
        [
            {
                "source": source,
                "normalized": report.volpubpage,
                "report_date": report.report_date,
            }
            for source in sources.get_column("citation")
            for report in Report.extract_reports(source)
        ],
        schema={
            "source": pl.String,
            "normalized": pl.String,
            "report_date": pl.Date,
        },
    )
    return (reports,)


@app.cell
def _(mo, reports):
    mo.ui.table(reports, selection=None)
    return


if __name__ == "__main__":
    app.run()
