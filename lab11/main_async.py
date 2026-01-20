from __future__ import annotations

import asyncio
import sys

import httpx

from lab_concurrency.bench import timer


async def fetch_one(
    client: httpx.AsyncClient, sem: asyncio.Semaphore, url: str
) -> bool:
    async with sem:  # limita cuántas requests simultáneas hay
        r = await client.get(url)
        return r.status_code == 200


async def fetch_async(url: str, n: int, concurrency: int) -> int:
    sem = asyncio.Semaphore(concurrency)
    ok = 0

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_one(client, sem, url) for _ in range(n)]
        results = await asyncio.gather(*tasks)

    ok = sum(1 for r in results if r)
    return ok


def main() -> None:
    # Uso: python main_async.py <url> <n> <concurrency>
    url = sys.argv[1] if len(sys.argv) > 1 else "https://httpbin.org/delay/1"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    concurrency = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    with timer(f"async fetch x{n} (concurrency={concurrency})"):
        ok = asyncio.run(fetch_async(url, n, concurrency))

    print("OK:", ok)


if __name__ == "__main__":
    main()
