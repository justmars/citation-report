# citation-report

![Github CI](https://github.com/justmars/citation-report/actions/workflows/main.yml/badge.svg)

Regex formula of Philippine Supreme Court citations in report format, i.e. SCRA, PHIL, OFFG; utilized in the [LawSQL dataset](https://lawsql.com).

## Documentation

See [documentation](https://justmars.github.io/citation-report), building on top of [citation-date](https://justmars.github.io/citation-date).

## Development

Checkout code, create a new virtual environment:

```sh
poetry add citation-report # python -m pip install citation-report
poetry update # install dependencies
poetry shell
```

Run tests:

```sh
pytest
```
