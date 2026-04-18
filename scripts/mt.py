"""Batch-translate .po files with deep-translator (Google backend).

Usage:
    python scripts/mt.py bugs.po
    python scripts/mt.py tutorial/*.po
    python scripts/mt.py library/functions.po

- Protects reST markup (:func:`x`, ``code``, *emph*, **strong**, |subst|, links,
  URLs, Python identifiers) with placeholder tokens before translation.
- Only touches entries whose msgstr is empty — idempotent, safe to resume.
- Marks every generated entry `fuzzy` so a human reviewer must confirm it.
- Rewrites `bugs.po`-specific issue-tracker links to this repo's tracker.

The output is machine translation of uneven quality; downstream review is
required before removing the `fuzzy` flag.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import polib
from deep_translator import GoogleTranslator

TRACKER_FROM = "https://github.com/python/cpython/issues"
TRACKER_TO = "https://github.com/tamnd/python-docs-vi/issues"
TRACKER_HINT_FROM = "The documentation"
# Keep as-is — bugs.po has one msgid that references the CPython tracker.

# Order matters — longer / more specific patterns first.
PATTERNS = [
    re.compile(r":[a-zA-Z:]+:`[^`]+`"),           # :func:`foo`, :mod:`x.y`
    re.compile(r"``[^`]+``"),                     # ``inline code``
    re.compile(r"`[^`]+`_"),                      # `link`_
    re.compile(r"`[^`]+`"),                       # `ref`
    re.compile(r"\*\*[^*\n]+\*\*"),               # **strong**
    re.compile(r"\*[^*\s][^*\n]*\*"),             # *emphasis*
    re.compile(r"\|[^|\n]+\|"),                   # |substitutions|
    re.compile(r"https?://\S+"),                  # bare URLs
    re.compile(r"#\s*[A-Za-z0-9_-]+"),            # anchors
    re.compile(r"\b[A-Z_][A-Z0-9_]{2,}\b"),       # SHOUTING_IDENTIFIERS
]

TOKEN_FMT = "zz{:03d}zz"
TOKEN_RE = re.compile(r"zz\d{3}zz")


def protect(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        key = TOKEN_FMT.format(len(tokens))
        tokens[key] = match.group(0)
        return key

    for pat in PATTERNS:
        text = pat.sub(replace, text)
    return text, tokens


def restore(text: str, tokens: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        return tokens.get(match.group(0), match.group(0))

    return TOKEN_RE.sub(replace, text)


def translate_one(translator: GoogleTranslator, msgid: str) -> str | None:
    protected, tokens = protect(msgid)
    if not protected.strip():
        return None
    try:
        result = translator.translate(protected)
    except Exception as exc:  # rate limit / network / empty input
        print(f"  ! translate failed: {exc!r}", file=sys.stderr)
        return None
    if not result:
        return None
    return restore(result, tokens)


def maybe_rewrite_tracker(text: str) -> str:
    return text.replace(TRACKER_FROM, TRACKER_TO)


def process_file(path: Path, translator: GoogleTranslator, delay: float) -> tuple[int, int]:
    po = polib.pofile(str(path))
    done = skipped = 0
    for entry in po:
        if entry.obsolete or not entry.msgid.strip():
            continue
        if entry.msgstr.strip():
            skipped += 1
            continue
        translated = translate_one(translator, entry.msgid)
        if translated is None:
            skipped += 1
            continue
        translated = maybe_rewrite_tracker(translated)
        entry.msgstr = translated
        if "fuzzy" not in entry.flags:
            entry.flags.append("fuzzy")
        done += 1
        if delay:
            time.sleep(delay)
    po.save(str(path))
    return done, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help=".po files to translate")
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--source", default="en")
    parser.add_argument("--target", default="vi")
    args = parser.parse_args()

    translator = GoogleTranslator(source=args.source, target=args.target)
    total_done = total_skipped = 0
    for raw in args.files:
        path = Path(raw)
        if not path.exists():
            print(f"skip missing: {path}", file=sys.stderr)
            continue
        print(f"== {path}", flush=True)
        done, skipped = process_file(path, translator, args.delay)
        print(f"   translated={done} skipped={skipped}", flush=True)
        total_done += done
        total_skipped += skipped
    print(f"\nTotal: translated={total_done} skipped={total_skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
