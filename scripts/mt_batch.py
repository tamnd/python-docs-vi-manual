"""Batch MT using translate.googleapis.com/translate_a/single.

Packs multiple msgids per request with QQZSEP markers, splits on return.
Falls back to single-string translation when the batch response doesn't
preserve the expected number of segments.

Usage:
    python scripts/mt_batch.py MACHINE/ [--delay 0.3] [--batch-chars 3500]
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
import requests

TRACKER_FROM = "https://github.com/python/cpython/issues"
TRACKER_TO = "https://github.com/tamnd/python-docs-vi/issues"

ENDPOINT = "https://translate.googleapis.com/translate_a/single"
COMMON_PARAMS = {"client": "gtx", "sl": "en", "tl": "vi", "dt": "t"}

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

SEP_FMT = "\n\nQQZSEP{:04d}QQZEND\n\n"
SEP_RE = re.compile(r"\s*QQZSEP\d{4}QQZEND\s*")

COMMENT_LINE_RE = re.compile(r"^((?:>>>|\.\.\.)[^\S\n]*)(#[^\S\n]*)(.+)$", re.MULTILINE)


def is_code_block(msgid: str) -> bool:
    for line in msgid.splitlines():
        if line.strip():
            return line.startswith(">>>")
    return False


def translate_code_block(msgid: str, delay: float) -> str:
    """Keep all code lines verbatim; translate only inline # comment text."""
    result = []
    for line in msgid.splitlines():
        m = COMMENT_LINE_RE.match(line)
        if m:
            prefix, hash_part, comment_text = m.group(1), m.group(2), m.group(3)
            translated = http_translate(comment_text)
            time.sleep(delay)
            if translated and translated.strip():
                result.append(f"{prefix}{hash_part}{translated.strip()}")
                continue
        result.append(line)
    return "\n".join(result)


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


def http_translate(text: str) -> str | None:
    if not text.strip():
        return ""
    params = dict(COMMON_PARAMS, q=text)
    delay = 1.0
    for attempt in range(6):
        try:
            r = requests.get(ENDPOINT, params=params, timeout=30)
        except Exception:
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
            continue
        if r.status_code == 200:
            try:
                data = r.json()
            except Exception:
                return None
            if not data or not data[0]:
                return None
            return "".join(seg[0] for seg in data[0] if seg and seg[0])
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
            continue
        return None
    return None


def batch_translate(msgids: list[str], max_chars: int, delay: float) -> list[str | None]:
    results: list[str | None] = [None] * len(msgids)
    protected_all = [protect(m) for m in msgids]

    i = 0
    while i < len(msgids):
        batch_items: list[int] = []
        total = 0
        while i < len(msgids):
            piece = protected_all[i][0]
            if not piece.strip():
                results[i] = ""
                i += 1
                continue
            sep_len = len(SEP_FMT.format(0))
            if len(piece) > max_chars - 50:
                if batch_items:
                    break
                batch_items.append(i)
                total = len(piece)
                i += 1
                break
            added = len(piece) + sep_len
            if batch_items and total + added > max_chars:
                break
            batch_items.append(i)
            total += added
            i += 1

        if not batch_items:
            continue

        if len(batch_items) == 1:
            idx = batch_items[0]
            result = http_translate(protected_all[idx][0])
            if result is not None:
                results[idx] = restore(result, protected_all[idx][1])
            time.sleep(delay)
            continue

        joined = ""
        for n, idx in enumerate(batch_items):
            joined += protected_all[idx][0] + SEP_FMT.format(n)

        translated = http_translate(joined)
        time.sleep(delay)

        def fallback_individual() -> None:
            for idx in batch_items:
                r = http_translate(protected_all[idx][0])
                if r is not None:
                    results[idx] = restore(r, protected_all[idx][1])
                time.sleep(delay)

        if translated is None:
            fallback_individual()
            continue

        parts = SEP_RE.split(translated)
        parts = [p for p in parts if p.strip() != ""]
        if len(parts) < len(batch_items):
            fallback_individual()
            continue

        for n, idx in enumerate(batch_items):
            piece = parts[n] if n < len(parts) else ""
            piece = piece.strip("\n")
            if piece.strip():
                results[idx] = restore(piece, protected_all[idx][1])

    return results


def chunk_list(items: list, n: int) -> list[list]:
    if n <= 1:
        return [items]
    size = (len(items) + n - 1) // n
    return [items[i : i + size] for i in range(0, len(items), size)]


def process_file(
    path: Path,
    max_chars: int,
    delay: float,
    only_empty: bool,
    workers: int,
) -> tuple[int, int]:
    po = polib.pofile(str(path))
    targets = [e for e in po if not e.obsolete and e.msgid.strip()]
    if only_empty:
        targets = [e for e in targets if not e.msgstr.strip()]
    if not targets:
        return 0, 0

    code_entries = [e for e in targets if is_code_block(e.msgid)]
    normal_entries = [e for e in targets if not is_code_block(e.msgid)]

    done = skipped = 0

    # Code blocks: translate only inline # comments, keep code verbatim
    for entry in code_entries:
        entry.msgstr = translate_code_block(entry.msgid, delay)
        if "fuzzy" not in entry.flags:
            entry.flags.append("fuzzy")
        done += 1

    # Normal entries: batch translate as before
    if normal_entries:
        msgids = [e.msgid for e in normal_entries]
        if workers > 1 and len(msgids) > workers * 4:
            shards = chunk_list(msgids, workers)
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
                shard_results = list(
                    pool.map(lambda s: batch_translate(s, max_chars, delay), shards)
                )
            translations: list[str | None] = []
            for r in shard_results:
                translations.extend(r)
        else:
            translations = batch_translate(msgids, max_chars, delay)

        for entry, translated in zip(normal_entries, translations):
            if translated is None or not translated.strip():
                skipped += 1
                continue
            entry.msgstr = translated.replace(TRACKER_FROM, TRACKER_TO)
            if "fuzzy" not in entry.flags:
                entry.flags.append("fuzzy")
            done += 1

    po.save(str(path))
    return done, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    parser.add_argument("--delay", type=float, default=0.3)
    parser.add_argument("--batch-chars", type=int, default=3500)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--only-empty", action="store_true")
    args = parser.parse_args()

    root = Path(args.root)
    files = [root] if root.is_file() else sorted(root.rglob("*.po"))
    start = time.time()
    total_done = total_skip = 0
    for idx, path in enumerate(files, 1):
        try:
            d, s = process_file(path, args.batch_chars, args.delay, args.only_empty, args.workers)
        except Exception as exc:
            print(f"! {path}: {exc}", file=sys.stderr, flush=True)
            d, s = 0, 0
        total_done += d
        total_skip += s
        elapsed = time.time() - start
        print(
            f"[{idx}/{len(files)}] +{d} -{s} total_done={total_done} "
            f"total_skip={total_skip} t={elapsed:.0f}s — {path}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
