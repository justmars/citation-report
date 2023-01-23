---
hide:
  - navigation
---
# Citation Report

## Concepts

### Definition

There are three popular repositories of Philippine Supreme Court decisions. Reference to such decisions are (traditionally) based on the name of the repository. Two of which - `Phil.` and `SCRA` - are talked about in the case of _China Airlines v. Chiok_, G.R. No. 152122, July 30, 2003:

> x x x This Court hereby exhorts members of the bar and the bench to refer to and quote from the _official repository of our decisions_, the **Philippine Reports**, whenever practicable [footnote: In the present case, Philippine Reports are cited whenever possible.]. In the absence of this primary source, which is still being updated, they may resort to _unofficial sources_ like the SCRA [footnote: **Supreme Court Reports Annotated**]. We remind them that the Court’s ponencia, when used to support a judgment or ruling, should be quoted accurately. (emphasis and footnotes supplied)

### Kinds

Style | Nature | Publisher | Description  | Basis
:--:|:--:|:--:|:--:|:--
`Phil.`  | Public | Philippine Reports | Though "official", often delayed in publication | _The [Supreme Court] Reporter shall prepare and publish with each reported decision a concise synopsis of the facts necessary to a clear understanding of the case x x x_
`Offg.` | Public | Official Gazette | Though "official", decisions are only published here occasionally | _There shall be published in the Official Gazette all x x x decisions or abstracts of decisions of the Supreme Court and the Court of Appeals, or other courts of similar rank, as may be deemed by the said courts of sufficient importance to be so published; x x x_
`SCRA` | Private | Supreme Court Reports Annotated | An unofficial source but more frequently printed by private entity | See disquisition in _China Airlines v. Chiok_ (2003)

### Formats

Each of the Report citations above have the same format... differing only in the `publisher` involved. Because of inconsistent styling over the years -- e.g. instead of _Phil._, what will be written is _Phil Rep._ -- it's necessary to create a uniform format using a `volume` `publisher` `page` format:

&nbsp;| Volume | Publisher | Page/s | Date
:--|:--:|:--:|:--:|:--:
_Sample Inconsistencies_ | Volume no. | Name / style of the publisher / reporter | Page number/s of the volume | Optional date
_1 Phil. Reports 100_ is equivalent to _1 Phil. 100_ | 1 | `Phil.` | 100 | -
_100 S.C.R.A. 105, 101-103_ (1994) is equivalent to _100 SCRA 105_ | 1 | `SCRA` | 105 | -
_41 Off. Gazette 1001, Jan. 1, 1949_ is equivalent to _41 O.G. 1001_ | 41 | `O.G.` | 1001 | Jan. 1, 1949

## API

### Report Model

::: citation_report.Report

### Report Pattern

::: citation_report.REPORT_PATTERN

### get_publisher_label()

::: citation_report.get_publisher_label
