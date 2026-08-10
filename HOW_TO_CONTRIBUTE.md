# Contributing

When contributing to this repository, please first discuss the change you wish to make via an [issue](../../issues/new). Feature additions, bug fixes, etc. should all be addressed with a pull request (PR).

Please note we have a [code of conduct](/CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request process

Pull requests should be made by forking the repository, making the changes, and requesting to merge back.
All pull requests should branch off of the `dev` branch with a descriptive prefix, e.g. `feat/new_feature` or `fix/fix_issue_number`.
Additionally, all pull requests should target back into the `dev` branch.

Once you have a new branch with the appropriate name, originating from `dev`, on a fork of the repository, complete the following steps.

1. Download the dependencies in the developer [requirements file](/requirements/developer.txt).
2. Add unit tests for features being added or bugs being fixed.
3. Include any new method/function in the corresponding docs file.
4. Run `pytest` to verify all unit tests pass. (To see what lines are covered, read the [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/reporting.html) documentation.)
5. [OPTIONAL] Format codebase according to the steps below.
6. Submit pull request with a list of changes, links to issues that it addresses (if applicable)
7. You may merge the Pull Request in once you have the sign-off of at least one other developer, or if you do not have permission to do that, you may request the reviewer to merge it for you.

## Format codebase
1. Identify the unnecessary imports in the
   1. source code by running `pylint xgi/ --disable=all --enable W0611`
   2. notebooks by running `nbqa pylint . --disable=all --enable W0611`
2. Remove these unnecessary imports.
3. Sort the import statements in the
   1. source code by running `isort .`
   2. notebooks by running `nbqa isort .` to sort any new import statements in the source code and tutorials.
4. Format the source code and notebooks by running `black .` for consistent styling.

## Profile importing XGI

Install the `test` dependencies and visualize the import times using [tuna](https://github.com/nschloe/tuna):
```python
python3 -X importtime -c "import xgi" 2> test.log
tuna test.log
```

## New Version process

New releases should be drawn from the development branch `dev` when appropriate and only after the CI workflow runs without errors and all documentation for new/updated features is updated.
Once you have a content on `dev` that you wish to include into a release, do the following steps to create a new release:

1. Open a new PR from the `dev` branch to the `main` branch. Title the PR `vMAJOR.MINOR.PATCH-rc` where the MAJOR, MINOR, and PATCH version identifiers conform to [SemVer](http://semver.org/) (the 'rc' stands for 'release candidate').
2. **While on the `dev` branch**, ensure release candidate is stable and ready for production. If needed, iterate development further while this PR is open. You must ensure:
   - CI workflow runs without errors
   - All new/updated features have updated docstrings
   - Style is maintained (see 'Format codebase' above)
   - The changelog is updated. Paste the output of `python tools/generate_changelog.py -m xgi-org xgi [last release tag]` into a new heading for the proposed release (`vMAJOR.MINOR.PATCH` without the 'rc').
3. Await approval for the PR.
4. Once the PR is approved, the approving/merging maintainer must bump the version number. Increase the version number in [\_\_init\_\_.py](xgi/__init__.py.py) to the new version. Commit these changes with the commit message "bump: v[last release] -> v[proposed release]". No new approval is needed for this tiny change.
5. Merge the PR.
6. Create a new release on GitHub by selecting "Releases", then clicking "Draft a new release". Click "Choose a tag" and type "v" followed by the version number and then click "Create new tag". The release title will be this same string. Paste the contents of the CHANGELOG into the "Describe this release" field. Click "Publish release". This will trigger a GitHub action that will publish the new version on PyPI.

The new version is now on PyPI! Make sure to update wherever you use xgi :)
