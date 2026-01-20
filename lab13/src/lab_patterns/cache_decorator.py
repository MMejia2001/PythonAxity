from __future__ import annotations

from functools import wraps


def simple_cache(func):
    """
    Decorator: cachea resultados por argumentos.
    Sirve para no recalcular si piden lo mismo.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper
