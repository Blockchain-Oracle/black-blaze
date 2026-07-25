#!/usr/bin/env python3
"""Check external HTTP links found in committed Markdown files."""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".research-clones", ".research-venv"}
URL_RE = re.compile(r"https?://[^\s)>\]`]+")
REACHABLE_AUTH_STATUSES = {401, 403, 405, 408, 409, 425, 429}
EXPECTED_PRIVATE_URLS = {"https://github.com/Blockchain-Oracle/black-blaze"}


def collect_urls() -> list[str]:
    urls: set[str] = set()
    for path in ROOT.rglob("*.md"):
        if EXCLUDED.intersection(path.relative_to(ROOT).parts):
            continue
        for url in URL_RE.findall(path.read_text(encoding="utf-8")):
            urls.add(url.rstrip(".,;:'\""))
    return sorted(urls)


def fetch(url: str, timeout: float) -> dict[str, object]:
    headers = {"User-Agent": "black-blaze-context-link-check/1.0"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "status": response.status, "final_url": response.url, "ok": True}
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and url in EXPECTED_PRIVATE_URLS:
            return {"url": url, "status": 404, "final_url": exc.url, "ok": True, "note": "expected unauthenticated response for private repository"}
        if exc.code in REACHABLE_AUTH_STATUSES:
            return {"url": url, "status": exc.code, "final_url": exc.url, "ok": True, "note": "reachable but access/method/rate restricted"}
        if exc.code in {400, 404, 410, 500, 501}:
            get_request = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-0"}, method="GET")
            try:
                with urllib.request.urlopen(get_request, timeout=timeout) as response:
                    return {"url": url, "status": response.status, "final_url": response.url, "ok": True}
            except urllib.error.HTTPError as get_exc:
                return {"url": url, "status": get_exc.code, "final_url": get_exc.url, "ok": get_exc.code in REACHABLE_AUTH_STATUSES, "error": str(get_exc)}
            except Exception as get_exc:  # noqa: BLE001
                return {"url": url, "status": None, "ok": False, "error": str(get_exc)}
        return {"url": url, "status": exc.code, "final_url": exc.url, "ok": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"url": url, "status": None, "ok": False, "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    urls = collect_urls()
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch, url, args.timeout): url for url in urls}
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: str(item["url"]))

    failures = [item for item in results if not item["ok"]]
    payload = {"checked": len(results), "reachable": len(results) - len(failures), "failed": len(failures), "results": results}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Checked {len(results)} URLs: {len(results) - len(failures)} reachable, {len(failures)} failed")
    for item in failures:
        print(f"FAIL {item.get('status')} {item['url']} — {item.get('error', 'unknown error')}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
