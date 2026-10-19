"""Produce valid, count- and UTF-8-byte-bounded pages of local JSON evidence."""
import argparse
import json
import sys
from pathlib import Path


def encode(value):
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def preview(value, chars):
    if isinstance(value, (dict, list)):
        return {"type": type(value).__name__, "count": len(value)}
    if isinstance(value, str):
        return {"text": value[:chars], "characters": len(value),
                "truncated": len(value) > chars}
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise ValueError("unsupported value type")


def project(data, collection, fields, offset=0, limit=8, max_bytes=4096, chars=160):
    if offset < 0 or limit < 1 or max_bytes < 1 or chars < 1:
        raise ValueError("offset must be nonnegative; limits must be positive")
    if not fields or len(set(fields)) != len(fields) or any(not f for f in fields):
        raise ValueError("choose distinct nonempty fields")
    if not isinstance(data, dict) or collection not in data:
        raise ValueError("expected an object with the requested collection")
    rows = data[collection]
    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
        raise ValueError("collection must contain only object records")
    if offset > len(rows):
        raise ValueError("offset exceeds collection length")
    selected = []

    def payload(items):
        end = offset + len(items)
        return encode({"total": len(rows), "offset": offset, "returned": len(items),
                       "has_more": end < len(rows),
                       "next_offset": end if end < len(rows) else None,
                       "rows": items})

    for row in rows[offset:offset + limit]:
        item = {field: preview(row[field], chars) for field in fields if field in row}
        candidate = selected + [item]
        if len(payload(candidate)) > max_bytes:
            break
        selected = candidate
    result = payload(selected)
    if len(result) > max_bytes or (offset < len(rows) and not selected):
        raise ValueError("budget cannot fit a progressing page; choose fewer fields or more bytes")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--collection", required=True)
    parser.add_argument("--fields", required=True)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--max-bytes", type=int, default=4096)
    parser.add_argument("--chars", type=int, default=160)
    args = parser.parse_args()
    try:
        data = json.loads(args.source.read_text(encoding="utf-8"))
        result = project(data, args.collection, args.fields.split(","), args.offset,
                         args.limit, args.max_bytes, args.chars)
    except (OSError, ValueError, RecursionError) as exc:
        # Do not echo source data or unbounded exception strings into the result.
        print("projection failed (" + type(exc).__name__ +
              "); check schema, offset and byte budget", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
