from __future__ import annotations

import sys

import httpx

from lab_concurrency.bench import timer


def fetch_sync(url: str, n: int) -> int:
    ok = 0
    with httpx.Client(timeout=10.0) as client:
        for _ in range(n):
            r = client.get(url)
            if r.status_code == 200:
                ok += 1
    return ok


def main() -> None:
    # Uso: python main_sync.py <url> <n>
    url = sys.argv[1] if len(sys.argv) > 1 else "https://httpbin.org/delay/1"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    with timer(f"sync fetch x{n}"):
        ok = fetch_sync(url, n)

    print("OK:", ok)


if __name__ == "__main__":
    main()
