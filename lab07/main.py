import asyncio
import sys
from pathlib import Path

import aiohttp


async def download_streaming(
    session: aiohttp.ClientSession,
    url: str,
    out_path: Path,
) -> int:
    """
    Descarga por streaming a disco (no usa mucha memoria).
    Regresa bytes escritos.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_written = 0
    async with session.get(url) as resp:
        # Manejo de errores HTTP
        if resp.status >= 400:
            text = await resp.text()
            raise RuntimeError(f"HTTP {resp.status}: {text[:200]}")

        with out_path.open("wb") as f:
            async for chunk in resp.content.iter_chunked(64 * 1024):  # 64 KB
                f.write(chunk)
                total_written += len(chunk)

    return total_written


async def download_with_retries(
    url: str,
    out_path: Path,
    timeout_seconds: float,
    max_attempts: int = 5,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
) -> None:
    """
    Reintenta ante fallas de red/timeout con backoff.
    """
    delay = initial_delay

    timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    for attempt in range(1, max_attempts + 1):
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                bytes_written = await download_streaming(session, url, out_path)
                print(f"Descarga completa: {out_path} ({bytes_written} bytes)")
                return

        except (aiohttp.ClientError, asyncio.TimeoutError, RuntimeError) as e:
            # RuntimeError lo usamos para HTTP >= 400 también
            if attempt == max_attempts:
                raise

            print(
                f"Intento {attempt} falló ({type(e).__name__}): {e}\n"
                f"Reintentando en {delay:.1f}s..."
            )
            await asyncio.sleep(delay)
            delay *= backoff_factor


def main() -> int:
    # Uso:
    # python main.py <url> <output_file> [timeout_seconds]
    if len(sys.argv) < 3:
        print("Uso: python main.py <url> <output_file> [timeout_seconds]")
        print("Ej:  python main.py http://localhost:8080/file out/file.bin 5")
        return 1

    url = sys.argv[1]
    out_path = Path(sys.argv[2])
    timeout_seconds = float(sys.argv[3]) if len(sys.argv) >= 4 else 5.0

    try:
        asyncio.run(
            download_with_retries(
                url=url,
                out_path=out_path,
                timeout_seconds=timeout_seconds,
            )
        )
        return 0

    except asyncio.TimeoutError as e:
        print(f"Timeout: {e}", file=sys.stderr)
        return 3

    except aiohttp.ClientError as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 4

    except RuntimeError as e:
        # aquí caen errores HTTP 4xx/5xx
        print(f"HTTP error: {e}", file=sys.stderr)
        return 2

    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return 99


if __name__ == "__main__":
    raise SystemExit(main())
