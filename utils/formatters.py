"""Utilidades de formateo de datos."""

import numpy as np


def format_array_summary(arr: np.ndarray, name: str = "array") -> str:
    """Retorna un resumen formateado de un array.

    Args:
        arr: Array numpy.
        name: Nombre del array para el mensaje.

    Returns:
        String con resumen del array.
    """
    if len(arr) == 0:
        return f"{name}: array vacío"

    return (
        f"{name}: min={np.min(arr):.3f}, "
        f"max={np.max(arr):.3f}, "
        f"mean={np.mean(arr):.3f}, "
        f"std={np.std(arr):.3f}"
    )


def format_complex(z: complex) -> str:
    """Formatea un número complejo de forma legible.

    Args:
        z: Número complejo.

    Returns:
        String formateado.
    """
    real = z.real
    imag = z.imag
    sign = "+" if imag >= 0 else "-"
    return f"{real:.3f} {sign} {abs(imag):.3f}i"


def format_simulation_time(seconds: float) -> str:
    """Formatea un tiempo en segundos a una unidad legible.

    Args:
        seconds: Tiempo en segundos.

    Returns:
        String formateado.
    """
    if seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        minutes = seconds / 60
        return f"{minutes:.1f} min"
