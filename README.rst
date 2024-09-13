.. role:: bash(code)
  :language: bash

********
Deskmaid
********

|ci-docs| |ci-lint| |ci-tests| |pypi| |versions| |discord| |license|

.. |ci-docs| image:: https://github.com/Dashstrom/deskmaid/actions/workflows/docs.yml/badge.svg
  :target: https://github.com/Dashstrom/deskmaid/actions/workflows/docs.yml
  :alt: CI : Docs

.. |ci-lint| image:: https://github.com/Dashstrom/deskmaid/actions/workflows/lint.yml/badge.svg
  :target: https://github.com/Dashstrom/deskmaid/actions/workflows/lint.yml
  :alt: CI : Lint

.. |ci-tests| image:: https://github.com/Dashstrom/deskmaid/actions/workflows/tests.yml/badge.svg
  :target: https://github.com/Dashstrom/deskmaid/actions/workflows/tests.yml
  :alt: CI : Tests

.. |pypi| image:: https://img.shields.io/pypi/v/deskmaid.svg
  :target: https://pypi.org/project/deskmaid
  :alt: PyPI : deskmaid

.. |versions| image:: https://img.shields.io/pypi/pyversions/deskmaid.svg
  :target: https://pypi.org/project/deskmaid
  :alt: Python : versions

.. |discord| image:: https://img.shields.io/badge/Discord-dashstrom-5865F2?style=flat&logo=discord&logoColor=white
  :target: https://dsc.gg/dashstrom
  :alt: Discord

.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
  :target: https://github.com/Dashstrom/deskmaid/blob/main/LICENSE
  :alt: License : MIT

Description
###########

Deskmaid is a configurable desktop cleaner.
It scans your desktop and moves selected files to a folder, organizing them by file extension.
Everything can be configured in :bash:`~/.config/deskmaid/config.yml`.

Installation
############

You can install :bash:`deskmaid` using `pipx <https://pipx.pypa.io/stable/>`_
from `PyPI <https://pypi.org/project>`_

..  code-block:: bash

  pip install pipx
  pipx ensurepath
  pipx install deskmaid
  deskmaid shortcut

This will install two shortcuts on your desktop:

.. image:: https://raw.githubusercontent.com/Dashstrom/deskmaid/main/docs/resources/shortcuts.png
   :alt: Two shortcuts, one with Thoru vacuuming and the other with Kanna opening her mouth wide, both people are from the anime Miss Kobayashi's Dragon Maid

How to cancel a run ?
#####################

Open shell then run:

..  code-block:: bash

  deskmaid undo

Development
###########

Contributing
************

Contributions are very welcome. Tests can be run with :bash:`poe check`, please
ensure the coverage at least stays the same before you submit a pull request.

Setup
*****

You need to install `Poetry <https://python-poetry.org/docs/#installation>`_
and `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
for work with this project.

..  code-block:: bash

  git clone https://github.com/Dashstrom/deskmaid
  cd deskmaid
  poetry install --all-extras
  poetry run poe setup
  poetry shell

Poe
********

Poe is available for help you to run tasks.

..  code-block:: text

  test           Run test suite.
  lint           Run linters: ruff checker and ruff formatter and mypy.
  format         Run linters in fix mode.
  check          Run all checks: lint, test and docs.
  check-tag      Check if the current tag match the version.
  cov            Run coverage for generate report and html.
  locale         Compile locale and refresh .po and .mo files.
  open-cov       Open html coverage report in webbrowser.
  docs           Build documentation.
  open-docs      Open documentation in webbrowser.
  setup          Setup pre-commit.
  pre-commit     Run pre-commit.
  commit         Test, commit and push.
  clean          Clean cache files.

Skip commit verification
************************

If the linting is not successful, you can't commit.
For forcing the commit you can use the next command :

..  code-block:: bash

  git commit --no-verify -m 'MESSAGE'

Commit with commitizen
**********************

To respect commit conventions, this repository uses
`Commitizen <https://github.com/commitizen-tools/commitizen?tab=readme-ov-file>`_.

..  code-block:: bash

  poe commit

How to add dependency
*********************

..  code-block:: bash

  poetry add 'PACKAGE'

Ignore illegitimate warnings
****************************

To ignore illegitimate warnings you can add :

- **# noqa: ERROR_CODE** on the same line for ruff.
- **# type: ignore[ERROR_CODE]** on the same line for mypy.
- **# pragma: no cover** on the same line to ignore line for coverage.
- **# doctest: +SKIP** on the same line for doctest.

Uninstall
#########

..  code-block:: bash

  pipx uninstall deskmaid

License
#######

This work is licensed under `MIT <https://github.com/Dashstrom/deskmaid/blob/main/LICENSE>`_.
