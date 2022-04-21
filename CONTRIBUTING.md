# Contributing

When contributing to this repository, please first discuss the change you wish to make via an [issue](../../issues/new). Feature additions, bug fixes, etc. should all be addressed with a pull request (PR).

Please note we have a [code of conduct](/CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request process

1. Download the dependencies in the developer [requirements file](/requirements/developer.txt).
2. [Optional, but STRONGLY preferred] Label commits according to [Conventional Commits](https://www.conventionalcommits.org) style.
3. [Optional, but STRONGLY preferred] Add unit tests for features being added or bugs being fixed.
4. [Optional, but STRONGLY preferred] Include any new method/function in the corresponding docs file.
5. Run `pytest` to verify all unit tests pass.
6. [Optional, but STRONGLY preferred] Run `pylint xgi/ --disable all --enable W0611` and remove any unnecessary dependencies.
7. [Optional, but STRONGLY preferred] Run `isort .` to sort any new import statements.
8. [Optional, but STRONGLY preferred] Run `black .` for consistent styling.
9. Update the "Current Version" section of CHANGELOG.md with overview of changes to the interface and add the usernames of all contributors.
10. Submit Pull Request with a list of changes, links to issues that it addresses (if applicable)
11. You may merge the Pull Request in once you have the sign-off of at least one other developer, or if you do not have permission to do that, you may request the reviewer to merge it for you.

## New Version process
1. Make sure that the Github Actions workflow runs without any errors.
2. Increase the version number in [setup.py](setup.py), [conf.py](docs/source/conf.py), and [CITATION.cff](CITATION.cff) to the new version agreed upon by the core developers. The versioning scheme we use is [SemVer](http://semver.org/).
3. Change the "Current Version" heading to the version number and put a new blank "Current Version" heading above this.
4. Upload to PyPI.

## Attribution

This Contributing Statement is adapted from [this template by @PurpleBooth](https://gist.github.com/PurpleBooth/b24679402957c63ec426).