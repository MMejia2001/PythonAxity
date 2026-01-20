from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor


def count_primes(limit: int) -> int:
    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        i = 3
        while i * i <= x:
            if x % i == 0:
                return False
            i += 2
        return True

    return sum(1 for n in range(limit) if is_prime(n))


def main() -> None:
    # Uso: python main_cpu.py <limit> <tasks>
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    tasks = int(sys.argv[2]) if len(sys.argv) > 2 else max(os.cpu_count() or 2, 2)

    t0 = time.perf_counter()
    # baseline secuencial
    seq = [count_primes(limit) for _ in range(tasks)]
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    # paralelo por procesos
    with ProcessPoolExecutor() as ex:
        par = list(ex.map(count_primes, [limit] * tasks))
    t3 = time.perf_counter()

    print(f"Sequential: {t1 - t0:.3f} s")
    print(f"ProcessPool: {t3 - t2:.3f} s")
    print("Results equal:", seq == par)


if __name__ == "__main__":
    main()
