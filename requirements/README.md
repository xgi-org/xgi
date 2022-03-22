# pip requirements files

## Index

- [`default.txt`](default.txt)
  Default requirements
- [`tutorial.txt`](example.txt)
  Requirements for running the Jupyter Notebooks with the examples
- [`test.txt`](test.txt)
  Requirements for running test suite
- [`documentation.txt`](doc.txt)
  Requirements for building the documentation (see `../docs/`)
- [`developer.txt`](developer.txt)
  Requirements for developers
- [`release.txt`](release.txt)
  Requirements for making releases

## Examples

### Installing requirements

```bash
$ pip install -U -r requirements/default.txt
```

### Running the tests

```bash
$ pip install -U -r requirements/default.txt
$ pip install -U -r requirements/test.txt
```