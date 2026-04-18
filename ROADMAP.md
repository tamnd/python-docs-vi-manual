# Roadmap

Where the Vietnamese translation stands and what is left to do. This
page breaks the remaining work into phases small enough that volunteers
can pick one up without reading the whole project.

## Where we are

PR #1 landed machine-translated `.po` files for the three catalogs
PEP 545 requires for the language-switcher milestone: `bugs.po`,
`tutorial/*.po`, `library/functions.po`. That is 1,860 entries and
about 50,240 words. Every string is marked `fuzzy`, which means Sphinx
still renders the English source at build time. None of that output is
visible on `docs.python.org/vi/` yet because no one has unfuzzied it.

So: corpus planted, zero words formally translated, zero words reviewed.

## What is left

About 1.76 million English words across 516 `.po` files. By section:

| Section       | Files | Words remaining |
|---------------|------:|----------------:|
| library/      |   325 |         791,751 |
| whatsnew/     |    25 |         566,964 |
| c-api/        |    77 |         120,511 |
| howto/        |    29 |         102,918 |
| reference/    |    11 |          67,740 |
| using/        |     9 |          30,792 |
| faq/          |     9 |          27,262 |
| extending/    |     7 |          21,920 |
| (root pages)  |     8 |          20,017 |
| deprecations/ |    14 |           7,116 |
| installing/   |     1 |           1,003 |
| distributing/ |     1 |              30 |
| **Total**     | **516** |  **1,758,024** |

## Phase 0: human review of PR #1 output

Before anyone translates new files, someone needs to read the machine
output from PR #1 and unfuzzy strings that are genuinely correct.
Otherwise the MT rots, and Sphinx keeps serving English even though
the `.po` files look finished on GitHub.

The review pass is also where we decide the things that will shape
every later phase:

- `GLOSSARY.md` with terminology decisions (list, dict, tuple, module,
  package, iterable, comprehension, decorator, callable, iterator,
  context manager, and so on).
- Second-person pronoun policy. Google picked `bạn` everywhere. A lot
  of formal Vietnamese tech writing drops the pronoun or uses `người
  dùng` / `ta`. Decide once, sweep back.
- Headings style. Imperative vs. noun form, sentence case vs. title
  case.
- Inline code and cross-reference wrapping. When Google reordered words,
  `:func:` sometimes ended up in an awkward position.

Concrete exit criteria:
- `GLOSSARY.md` exists and is linked from the README.
- `bugs.po` fully unfuzzied.
- At least one tutorial chapter (suggest `tutorial/introduction.po`)
  fully unfuzzied as the reference for style.

## Phase 1: standalone top-level pages (~20k words)

Short and highly visible. These are the pages a reader sees around
the edges of the site.

- `about.po`, `contents.po`, `copyright.po`, `license.po`, `sphinx.po`
- `improve-page.po`, `improve-page-nojs.po`
- `glossary.po` (one big file, ~18k words on its own)

Order suggestion: do everything except `glossary.po` first, because
those are short. Leave `glossary.po` for last in this phase and treat
it as a chance to lock in terminology choices. Feed anything new it
reveals back into `GLOSSARY.md`.

## Phase 2: language reference (~68k words, 11 files)

`reference/` is what people read to understand Python the language,
not the library. Heavier reading, so expect slower pace.

Big files: `datamodel.po`, `compound_stmts.po`, `expressions.po`,
`import.po`. Everything else is short.

## Phase 3: how-tos and FAQ (~130k words, 38 files)

Good volunteer work because each file is self-contained, practical,
and terminology is narrower than the library reference.

- `howto/` (29 files): notable large ones are `logging.po`,
  `argparse.po`, `urllib2.po`, `functional.po`.
- `faq/` (9 files): `programming.po` is the big one.

## Phase 4: using/ and extending/ (~53k words)

- `using/` covers command line flags, environment variables, and
  platform install notes (Windows, macOS, Unix). Useful for new
  users so it has real traffic.
- `extending/` is only for people writing C extensions. Low
  traffic but short.
- `installing/` is one file, 1k words. Easy win.
- `distributing/` is one file with 30 words. Finish it in one sitting.

## Phase 5: C API (~120k words, 77 files)

Terminology-heavy and audience-limited to C extension authors. Tackle
only after `GLOSSARY.md` is stable, because mistakes here are painful
to sweep later. Big files: `typeobj.po`, `arg.po`, `unicode.po`,
`structures.po`.

## Phase 6: library reference, minus functions.po (~792k words, 325 files)

The mountain. Work it by traffic, not alphabetically.

Tier A, top-20 most-read modules. Do these first inside Phase 6:

`os`, `sys`, `pathlib`, `re`, `json`, `typing`, `collections`,
`datetime`, `itertools`, `functools`, `asyncio`, `subprocess`, `io`,
`pickle`, `logging`, `argparse`, `http`, `urllib`, `sqlite3`, `math`.

Tier B, the rest of the stdlib that is still actively used.

Tier C, niche or historical modules (`telnetlib`, parts of `email`,
`cgi`, `xdrlib`, some `xml` pieces). Fine to leave fuzzy for now.
These have low reader volume and Sphinx will keep serving English.

Heads up on size: `asyncio`, `typing`, `unittest`, and `collections`
are each 5,000+ words and terminology-sensitive. Schedule them after
the glossary has been tested on smaller files.

## Phase 7: whatsnew/ (policy, not scope)

`whatsnew/` is 567,000 words across 25 files. No PEP 545 translation
has ever tried to translate all of it. The changelog alone is about
500,000 words.

Policy we follow:

- Translate `whatsnew/3.14.po` only (the current release).
- Everything older stays English via the `Makefile`'s `EXCLUDED`
  pattern. Sphinx falls back to the source when a `.po` file is
  excluded.
- When CPython branches 3.15, translate `whatsnew/3.15.po` too and
  keep the prior year updated as long as we have bandwidth.

## Phase 8: carry-forward maintenance

Upstream CPython keeps moving. Every few months, or when 3.15 branches:

1. Bump `CPYTHON_CURRENT_COMMIT` in the `Makefile`.
2. Re-run `make gettext` in the pinned CPython checkout.
3. Run `sphinx-intl update -l vi` against the new `.pot` files.
4. `msgmerge` will surface changed strings as `fuzzy`. Resolve them.
5. Update `GLOSSARY.md` if new terms appear.

## How to claim a file

1. Open an issue titled `Translate {path}` (e.g. `Translate library/os.po`).
   Assign yourself.
2. Create a branch named after the file, with slashes as dashes:
   `library-os`, `reference-datamodel`, etc.
3. Open a PR early, even as a draft. Early PRs prevent duplicate work
   and let someone else review terminology before you finish the file.
4. Only remove the `fuzzy` flag from strings you have actually read and
   are confident are correct.

## How to pick a file

- New contributor: start in Phase 0 (review what PR #1 produced) or
  pick a short file from Phase 1 or Phase 4. `installing/index.po`,
  `distributing/index.po`, `sphinx.po`, `improve-page.po` are all
  finishable in a single sitting.
- Experienced Python writer with opinions on terminology: help define
  `GLOSSARY.md` and the first pass on `glossary.po`.
- Someone who wants a concrete target: pick a Tier A module from
  Phase 6 and own it end to end.

## Milestones

- [x] PR #1: MT seed of PEP 545 switcher files.
- [x] `GLOSSARY.md` landed.
- [x] Pronoun and heading-style policies written down in `GLOSSARY.md`.
- [x] `bugs.po` fully unfuzzied (language-switcher dependency).
- [ ] `tutorial/*.po` fully unfuzzied (language-switcher dependency).
- [ ] `library/functions.po` fully unfuzzied (language-switcher dependency).
- [ ] Language-switcher milestone: request inclusion in `docsbuild-scripts`.

### `tutorial/*.po` file-level progress

Tracked per file so reviewers can see what's still fuzzy. Sizes are
`wc -l` on the `.po`.

- [x] `tutorial/appetite.po` (218 lines)
- [x] `tutorial/index.po` (115 lines)
- [x] `tutorial/interactive.po` (109 lines)
- [x] `tutorial/interpreter.po` (333 lines)
- [x] `tutorial/introduction.po` (1309 lines)
- [ ] `tutorial/appendix.po` (325 lines)
- [ ] `tutorial/classes.po` (2141 lines)
- [ ] `tutorial/controlflow.po` (2751 lines)
- [ ] `tutorial/datastructures.po` (1654 lines)
- [ ] `tutorial/errors.po` (1592 lines)
- [ ] `tutorial/floatingpoint.po` (852 lines)
- [ ] `tutorial/inputoutput.po` (1316 lines)
- [ ] `tutorial/modules.po` (1436 lines)
- [ ] `tutorial/stdlib.po` (799 lines)
- [ ] `tutorial/stdlib2.po` (941 lines)
- [ ] `tutorial/venv.po` (487 lines)
- [x] `tutorial/whatnow.po` (201 lines)
- [ ] Phase 1 complete.
- [ ] Phase 2 complete.
- [ ] Phase 3 complete.
- [ ] Phase 4 complete.
- [ ] Phase 5 complete.
- [ ] Phase 6 Tier A complete.
- [ ] Phase 6 Tier B complete.
- [ ] Phase 7 ongoing: current `whatsnew/` up to date; older excluded.
- [ ] Coordinator has signed the PSF CLA.
- [ ] Transfer request opened to move the repo under the `python/`
      GitHub org (requires PEP 545 criteria met).

## Scope we are deliberately not taking on

- Translating the CPython source comments or docstrings directly. We
  work from the `.pot` output only. The Sphinx build is the boundary.
- Building our own translation memory server. `sphinx-intl` plus
  `msgmerge` is enough until we outgrow it.
- Automating review. Every `fuzzy` removal has to be a human decision.
