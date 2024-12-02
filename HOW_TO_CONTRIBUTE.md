# Contributing

When contributing to this repository, please first discuss the change you wish to make via an [issue](../../issues/new). Feature additions, bug fixes, etc. should all be addressed with a pull request (PR).

Please note we have a [code of conduct](/CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request process

1. Download the dependencies in the developer [requirements file](/requirements/developer.txt).
2. Add unit tests for features being added or bugs being fixed.
3. Include any new method/function in the corresponding docs file.
4. Run `pytest` to verify all unit tests pass. (To see what lines are covered, read the [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/reporting.html) documentation.)
5. [OPTIONAL] Format codebase according to the steps below.
5. Submit Pull Request with a list of changes, links to issues that it addresses (if applicable)
6. You may merge the Pull Request in once you have the sign-off of at least one other developer, or if you do not have permission to do that, you may request the reviewer to merge it for you.

## Format codebase
1. Identify the unnecessary imports in the
   1. source code by running `pylint xgi/ --disable=all --enable W0611`
   2. notebooks by running `nbqa pylint . --disable=all --enable W0611`
2. Remove these unnecessary imports.
3. Sort the import statements in the
   1. source code by running `isort .`
   2. notebooks by running `nbqa isort .` to sort any new import statements in the source code and tutorials.
4. Format the source code and notebooks by running `black .` for consistent styling.

## New Version process

1. Make sure that the Github Actions workflow runs without any errors.
2. Run `python tools/generate_changelog.py -m xgi-org xgi [last release tag]` to get the merged pull requests with their links. Paste this into the changelog file under a new heading and edit to make more legible. Associate a GitHub username with each pull request.
3. Increase the version number in [\_\_init\_\_.py](xgi/__init__.py.py) to the new version agreed upon by the core developers. The versioning scheme we use is [SemVer](http://semver.org/).
4. Commit these changes.
5. Create a new release on GitHub by selecting "Releases", then clicking "Draft a new release". Click "Choose a tag" and type "v" followed by the version number and then click "Create new tag". The release title will be this same string. Paste the contents of the CHANGELOG into the "Describe this release" field. Click "Publish release". This will trigger a GitHub action that will publish the new version on PyPI.
6. The new version is now on PyPI.