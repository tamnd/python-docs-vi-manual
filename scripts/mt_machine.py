"""Concurrent MT for MACHINE/ tree — translates every msgid regardless of
existing msgstr. Intended to produce a pure-MT snapshot of the full
documentation for side-by-side comparison.

Usage:
    python scripts/mt_machine.py MACHINE/
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
import threading
import time
from pathlib import Path

import polib
from deep_translator import GoogleTranslator

TRACKER_FROM = "https://github.com/python/cpython/issues"
TRACKER_TO = "https://github.com/tamnd/python-docs-vi/issues"

PATTERNS = [
    re.compile(r":[a-zA-Z:]+:`[^`]+`"),
    re.compile(r"``[^`]+``"),
    re.compile(r"`[^`]+`_"),
    re.compile(r"`[^`]+`"),
    re.compile(r"\*\*[^*\n]+\*\*"),
    re.compile(r"\*[^*\s][^*\n]*\*"),
    re.compile(r"\|[^|\n]+\|"),
    re.compile(r"https?://\S+"),
    re.compile(r"#\s*[A-Za-z0-9_-]+"),
    re.compile(r"\b[A-Z_][A-Z0-9_]{2,}\b"),
]

TOKEN_FMT = "zz{:03d}zz"
TOKEN_RE = re.compile(r"zz\d{3}zz")

_LOCAL = threading.local()
_LOCK = threading.Lock()


def get_translator() -> GoogleTranslator:
    tr = getattr(_LOCAL, "tr", None)
    if tr is None:
        tr = GoogleTranslator(source="en", target="vi")
        _LOCAL.tr = tr
    return tr


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


def translate_one(msgid: str) -> str | None:
    protected, tokens = protect(msgid)
    if not protected.strip():
        return None
    if len(protected) > 4500:
        return None
    delay = 1.0
    for _ in range(6):
        try:
            result = get_translator().translate(protected)
        except Exception as exc:
            msg = str(exc).lower()
            if any(k in msg for k in ("too many", "429", "rate", "timeout", "503", "502")):
                time.sleep(delay)
                delay = min(delay * 2, 30.0)
                continue
            return None
        if result:
            return restore(result, tokens).replace(TRACKER_FROM, TRACKER_TO)
        time.sleep(delay)
        delay = min(delay * 2, 30.0)
    return None


PROGRESS = {"done": 0, "skip": 0, "total": 0, "files": 0}


def process_file(path: Path, workers: int, only_empty: bool) -> None:
    po = polib.pofile(str(path))
    targets = [e for e in po if not e.obsolete and e.msgid.strip()]
    if only_empty:
        targets = [e for e in targets if not e.msgstr.strip()]
    if not targets:
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda e: (e, translate_one(e.msgid)), targets))

    for entry, translated in results:
        if translated is None:
            with _LOCK:
                PROGRESS["skip"] += 1
            continue
        entry.msgstr = translated
        if "fuzzy" not in entry.flags:
            entry.flags.append("fuzzy")
        with _LOCK:
            PROGRESS["done"] += 1

    po.save(str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--only-empty", action="store_true",
                        help="skip entries that already have a msgstr")
    args = parser.parse_args()

    root = Path(args.root)
    if root.is_file():
        files = [root]
    else:
        files = sorted(root.rglob("*.po"))
    PROGRESS["total"] = len(files)
    start = time.time()
    for idx, path in enumerate(files, 1):
        try:
            process_file(path, args.workers, args.only_empty)
        except Exception as exc:
            print(f"! {path}: {exc}", file=sys.stderr, flush=True)
        PROGRESS["files"] += 1
        if idx % 5 == 0 or idx == len(files):
            elapsed = time.time() - start
            print(
                f"[{idx}/{len(files)}] done={PROGRESS['done']} "
                f"skip={PROGRESS['skip']} t={elapsed:.0f}s — {path}",
                flush=True,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
