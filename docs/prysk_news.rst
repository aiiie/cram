Version 0.12.0 (May. 29, 2022)
-----------------------------------------------------
* Remove whitespace
* Add basic support for color(s) to cli
* Remove doctest configuration from prysk setup code
* Add additional commit hooks
* Update noxfile
* Add pre-commit to dev tools
* Fix code style
* Fix integration test execution
* Add doctest(s) to unit test execution
* Refactor xunit module
* Update dev dependencies
* Fix key name for isort configuration in pyproject
* Port optparse based cli to argparse based cli
* Update pypi shield to always point to the latest published version
* Update dependencies
* Bump JamesIves/github-pages-deploy-action from 4.2.5 to 4.3.0
* Bump pylint from 2.12.2 to 2.13.4
* Move dev-dependencies to dev-dependencies section
* Bump furo from 2022.2.23 to 2022.3.4
* Bump actions/checkout from 2.4.0 to 3
* Bump coverage from 6.3.1 to 6.3.2
* Bump JamesIves/github-pages-deploy-action from 4.2.3 to 4.2.5
* Bump actions/setup-python from 2 to 3
* Bump furo from 2022.1.2 to 2022.2.23
* Fix path of output folder for documentation
* Remove makefile dependency, just call sphinx directly
* Add copy button extension to sphinx
* Add nox target for fixing formatting and import order
* Add basic information for developers
* Update and add index, gettings started and contributors
* Wrap snippets in code blocks for improved syntax highlighting
* Fix broken link in README.rst
* Fix nox warnings
* Fix syntax error in gh-pages action
* Add support for tags as trigger of gh-pages workflow

Version 0.11.0 (February. 11, 2022)
-----------------------------------------------------
* Reorder publishing steps
* Fix release notes of 0.10.0 release

Version 0.10.0 (February. 11, 2022)
-----------------------------------------------------
* Add version sanity check
* Add support for automated releases
* Add support for retrieving project version from pyproject.toml

Version 0.9.0 (February. 11, 2022)
-----------------------------------------------------
* Add support for automated releases
* Add support for retrieving project version from pyproject.toml

Version 0.9 (Jan. 29, 2022)
---------------------------
* Add basic documentation
* Release new version to account and cope with accidentally
  deleted (untagged prysk version 0.8)

    .. note::
        once a version is published on pipy it can't be
        reused even if it has been deleted
        (see `file name reuse <https://pypi.org/help/#file-name-reuse>`_).

Version 0.8 (Jan. 25, 2022)
---------------------------
* Rename cram to prysk

    .. warning::
        Also semantically relevant names have been renamed,
        e.g. env var CRAMTMP is now PRYSK_TEMP
