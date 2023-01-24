import toml

import citation_report


def test_version():
    assert (
        toml.load("pyproject.toml")["tool"]["poetry"]["version"]
        == citation_report.__version__
    )
