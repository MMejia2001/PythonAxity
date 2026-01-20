import random
import time
from itertools import islice


def retry(
    max_attempts=3, initial_delay=0.2, backoff_factor=2.0, exceptions=(Exception,)
):
    """
    Decorador: reintenta una función si lanza error.

    - max_attempts: número máximo de intentos
    - initial_delay: tiempo inicial de espera (segundos)
    - backoff_factor: multiplicador del delay en cada intento (backoff)
    - exceptions: tupla de excepciones que activan el retry
    """

    def decorator(func):
        def wrapper(*args, **kwargs): #Cualquier cantidad de argumentos posicionales y con nombre
            delay = initial_delay
            attempt = 1

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= max_attempts:
                        # Ya no reintentamos
                        raise

                    print(
                        f"Intento {attempt} falló: {e}. "
                        f"Reintentando en {delay:.2f}s..."
                    )
                    time.sleep(delay)

                    delay *= backoff_factor
                    attempt += 1

        return wrapper

    return decorator


def batch(iterable, size):
    """
    Generador: produce lotes (listas) de tamaño 'size' desde un iterable.

    Ej:
    list(batch([1,2,3,4,5], 2)) -> [[1,2],[3,4],[5]]
    """
    if size <= 0:
        raise ValueError("size debe ser mayor que 0")

    it = iter(iterable)

    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk


class Timer:
    """
    Context manager simple para medir tiempo.

    Uso:
    with Timer("mi bloque"):
        ...
    """

    def __init__(self, label="bloque"):
        self.label = label
        self.start = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end = time.perf_counter()
        elapsed = end - self.start
        print(f"{self.label} tardó {elapsed:.4f} s")
        # False => si hubo excepción, NO la ocultamos
        return False


# -------------------------
# DEMOS (para probar el lab)
# -------------------------


@retry(max_attempts=5, initial_delay=0.2, backoff_factor=2.0, exceptions=(ValueError,))
def flaky_operation():
    """Función que falla aleatoriamente para probar retry."""
    n = random.random()
    if n < 0.7:
        raise ValueError("Fallé a propósito (simulación)")
    return "Éxito"


def main():
    print("\n--- Demo retry con backoff ---")
    try:
        result = flaky_operation()
        print("Resultado:", result)
    except ValueError:
        print("No se pudo después de varios intentos.")

    print("\n--- Demo batch generator ---")
    items = list(range(1, 11))
    for chunk in batch(items, 3):
        print("Lote:", chunk)

    print("\n--- Demo Timer context manager ---")
    with Timer("sumar muchos números"):
        total = 0
        for i in range(1_000_000):
            total += i
    print("Total:", total)


if __name__ == "__main__":
    main()
