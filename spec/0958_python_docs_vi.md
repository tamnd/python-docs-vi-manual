# 0958 - Vietnamese Translation of the Python Documentation

## Summary

Bootstrap a repository that hosts the Vietnamese (`vi`) translation of the
official Python documentation, following the process defined in
[PEP 545](https://peps.python.org/pep-0545/).

The repository exposes one `.po` file per page of the CPython documentation.
All translatable strings are generated from CPython's reStructuredText
sources through `make gettext`, then materialized as per-language message
catalogs with `sphinx-intl`. The first commit pins a specific CPython
commit on the `3.14` branch and contains every generated `.po` file with
empty `msgstr` entries (i.e. the English source only).

## Goals

- Create `tamnd/python-docs-vi` as a private GitHub repository.
- Produce an initial commit that carries the full set of English source
  strings extracted from CPython's docs, ready to receive Vietnamese
  translations.
- Track the exact CPython commit the catalogs were generated from, so that
  test builds use the matching `.rst` sources.
- Ship a `Makefile`, `README`, `TRANSLATORS`, and tooling configuration
  mirroring the layout established by other PEP 545 translation teams
  (e.g. `python/python-docs-tr`, `python/python-docs-fr`).
- Satisfy the PEP 545 repository requirements so the repo can later be
  transferred to the `python/` GitHub organization.

## Non-Goals

- Translate any strings in this first commit.
- Register the translation with `docsbuild-scripts` or request inclusion in
  the language switcher on docs.python.org (those happen after reaching
  the milestones listed in PEP 545).
- Set up Transifex, Weblate, or other external translation platforms.
- Define Vietnamese terminology conventions or a glossary.
- Automate merges with upstream CPython changes.

## Background

PEP 545 standardizes how Python documentation translations are organized:

- One repository per language, named `python-docs-{LANGUAGE_TAG}` where the
  tag follows IETF BCP 47 (lowercased, no redundant region subtag).
- The repository exposes only `.po` files, so different translation tools
  can all sync through git.
- A coordinator signs the Documentation Contribution Agreement and manages
  contributors. The agreement (contribution under CC0 in exchange for
  public credit) must be shown in the `README`.
- Multiple Python versions live on different branches, not separate
  repositories.
- A language only appears in docs.python.org's language switcher after
  reaching 100% translation of `bugs`, `tutorial/`, and `library/functions`.

For Vietnamese, the language tag is `vi`. No region subtag is needed.

## Repository Layout

The repository mirrors CPython's `Doc/` tree but carries only `.po` files:

```
python-docs-vi/
├── .github/                      # issue templates, CI
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── LICENSE                       # CC0 1.0
├── Makefile                      # local build / verify targets
├── README.md                     # with Documentation Contribution Agreement
├── TRANSLATORS                   # one translator per line
├── about.po
├── bugs.po
├── c-api/*.po
├── contents.po
├── copyright.po
├── deprecations/*.po
├── distributing/*.po
├── extending/*.po
├── faq/*.po
├── glossary.po
├── howto/*.po
├── installing/*.po
├── library/*.po
├── license.po
├── reference/*.po
├── requirements-dev.txt
├── sphinx.po
├── tutorial/*.po
├── using/*.po
├── whatsnew/*.po
└── spec/0958_python_docs_vi.md   # this document
```

The `Makefile` clones CPython into `venv/cpython/`, checks out the pinned
commit, copies the `.po` files into `locales/vi/LC_MESSAGES/`, and runs
CPython's `Doc/` Sphinx build with `language=vi`. This matches the
convention used by other translation repos and keeps the build
reproducible.

## Bootstrap Procedure

These steps produced the first commit.

### 1. Target version

- Branch: `3.14`
- CPython commit:
  `67100b3e926c2c7cdd9d0825add677b19664f377`
  (the HEAD of `python/cpython@3.14` on 2026-04-18).

### 2. Build the POT catalogs

```sh
git clone --depth 1 --branch 3.14 https://github.com/python/cpython
cd cpython
git fetch --depth 1 origin 67100b3e926c2c7cdd9d0825add677b19664f377
git checkout 67100b3e926c2c7cdd9d0825add677b19664f377
cd Doc
make venv
make gettext        # produces build/gettext/*.pot
```

### 3. Generate the Vietnamese `.po` files

```sh
python3 -m pip install sphinx-intl
cd cpython/Doc
sphinx-intl update -p build/gettext -l vi
```

This creates `cpython/Doc/locales/vi/LC_MESSAGES/**/*.po` with all
`msgid` strings populated and every `msgstr` empty.

### 4. Flatten into the repo

Copy the generated catalogs into the repo root, preserving the subtree
layout (`c-api/`, `library/`, `tutorial/`, ...):

```sh
rsync -av cpython/Doc/locales/vi/LC_MESSAGES/ python-docs-vi/
```

### 5. Scaffold

Add `README.md`, `Makefile`, `TRANSLATORS`, `CONTRIBUTING.md`,
`requirements-dev.txt`, `.gitignore`, `.gitattributes`, and
`.pre-commit-config.yaml`. The `Makefile` pins
`CPYTHON_CURRENT_COMMIT := 67100b3e926c2c7cdd9d0825add677b19664f377`.

### 6. First commit

```sh
git add -A
git commit -m "Initial import of Python 3.14 docs (English source)"
git push -u origin main
```

## Documentation Contribution Agreement

The `README.md` must include, verbatim, the agreement from PEP 545:

> NOTE REGARDING THE LICENSE FOR TRANSLATIONS: Python's documentation is
> maintained using a global network of volunteers. By posting this project
> on Transifex, GitHub, and other public places, and inviting you to
> participate, we are proposing an agreement that you will provide your
> improvements to Python's documentation or the translation of Python's
> documentation for the PSF's use under the CC0 license (available at
> https://creativecommons.org/publicdomain/zero/1.0/legalcode). In return,
> you may publicly claim credit for the portion of the translation you
> contributed and, if your translation is accepted by the PSF, you may
> (but are not required to) submit a patch including an appropriate
> annotation in the TRANSLATORS file. Although nothing in this
> Documentation Contribution Agreement obligates the PSF to incorporate
> your textual contribution, your participation in the Python community
> is welcomed and appreciated.
>
> You signify acceptance of this agreement by submitting your work to the
> PSF for inclusion in the documentation.

## Coordinator

Initial coordinator: **tamnd** (`tamnd87@gmail.com`).

The coordinator's responsibilities per PEP 545:

- Manage the team and contributors.
- Ensure contributors understand and accept the Documentation Contribution
  Agreement.
- Choose and manage tooling (issue tracker, chat, translation memory).
- Route issues to the right upstream tracker (CPython for source bugs,
  this repo for translation bugs).
- Maintain quality of the translated strings.

## Path to the `python/` Organization

This repository is created private under `tamnd/` to give the team room to
bootstrap tooling before PEP 545 requirements are fully met. Transfer to
`python/python-docs-vi` is conditioned on:

1. A coordinator who has signed the Python CLA.
2. The README containing the Documentation Contribution Agreement.
3. At least one contributor beyond the coordinator.
4. Evidence of active translation work (non-empty `msgstr` entries in one
   or more files).

Inclusion in the docs.python.org language switcher additionally requires
100% translation of `bugs.po`, `tutorial/*.po`, and `library/functions.po`,
as specified in PEP 545.

## Maintenance Model

- One branch per supported Python version. `main` tracks the most recent
  CPython release branch (currently `3.14`).
- Periodically re-run `make gettext` + `sphinx-intl update` against a newer
  CPython commit and commit the `msgmerge` result. Bump
  `CPYTHON_CURRENT_COMMIT` in the `Makefile` in the same commit.
- Fuzzy entries introduced by `msgmerge` are resolved by translators
  before the updated catalog is merged.

## Acceptance Criteria

- `tamnd/python-docs-vi` exists as a private GitHub repository.
- The first commit on `main` contains the full set of `.po` files
  generated from CPython commit `67100b3e926c2c7cdd9d0825add677b19664f377`
  with empty `msgstr` entries.
- `Makefile`, `README.md` (with the Documentation Contribution Agreement),
  `TRANSLATORS`, `CONTRIBUTING.md`, and `requirements-dev.txt` are present
  at the repository root.
- `spec/0958_python_docs_vi.md` documents the bootstrap.
- `git log` shows a single commit authored by the coordinator.

## References

- [PEP 545 -- Python Documentation Translations](https://peps.python.org/pep-0545/)
- [python/python-docs-fr](https://github.com/python/python-docs-fr)
- [python/python-docs-tr](https://github.com/python/python-docs-tr)
- [sphinx-intl](https://pypi.org/project/sphinx-intl/)
