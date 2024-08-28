# Installation instructions

## pip installing with options

You may wish to selectively install dependencies required for testing, developing, or building certain parts of the project.
These options are the following:

- `benchmark`: Requirements needed to run the benchmarking notebooks
- `tutorial`: Requirements needed to run the Jupyter Notebooks with the examples
- `test`: Requirements needed to run the test suite
- `docs`: Requirements needed to build the documentation (see the [docs](https://github.com/xgi-org/xgi/tree/main/docs))
- `developer`: Requirements needed to format the codebase
- `release`: Requirements needed to release new versions of XGI

```sh
pip install xgi[option]
pip install xgi[option1,option2]
```

## pip installing dependencies (without installing XGI)

You may wish to install the dependencies without actually installing XGI itself. The following are the requirements files to do that:

- `benchmark.txt`: Requirements to run the benchmarking notebooks
- `default.txt`: Default requirements
- `tutorial.txt`: Requirements for running the Jupyter Notebooks with the examples
- `test.txt`: Requirements for running test suite
- `docs.txt`: Requirements for building the documentation (see `../docs/`)
- `developer.txt`: Requirements for developers
- `release.txt`: Requirements for making releases

To install these dependencies, simply run
```bash
$ pip install -U -r requirements/{filename}
```
where the filename is one of the ones listed above. For example, to install the requirements necessary to run the test suite, run
```bash
$ pip install -U -r requirements/default.txt
$ pip install -U -r requirements/test.txt
```