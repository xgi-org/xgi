from testbook import testbook
from pathlib import Path

TUTO = Path(__file__).parent.parent / "tutorials"


def test_tutorial_notebooks():
    for notebook in TUTO.iterdir():
        if notebook.suffix == ".ipynb":
            with testbook(notebook, execute=True) as tb:
                # possibly add here more specific tests
                pass
