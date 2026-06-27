"""Detección de convergencia de la simulación."""

import numpy as np


def check_convergence(
    r_history: np.ndarray,
    window: int = 50,
    threshold: float = 1e-4,
) -> bool:
    """Verifica si la simulación ha convergido.

    La simulación se considera convergida si la variación de r
    en los últimos 'window' pasos es menor que 'threshold'.

    Args:
        r_history: Historial del grado de consenso r(t).
        window: Número de pasos recientes a examinar.
        threshold: Umbral de variación para considerar convergencia.

    Returns:
        True si la simulación ha convergido, False en caso contrario.
    """
    if len(r_history) < window:
        return False

    recent = r_history[-window:]
    variation = np.max(recent) - np.min(recent)
    return bool(variation < threshold)


def get_convergence_info(r_history: np.ndarray) -> dict:
    """Obtiene información detallada sobre la convergencia.

    Args:
        r_history: Historial del grado de consenso r(t).

    Returns:
        Diccionario con información de convergencia.
    """
    if len(r_history) == 0:
        return {
            "converged": False,
            "r_final": 0.0,
            "r_min": 0.0,
            "r_max": 0.0,
            "variation": 0.0,
            "steps": 0,
        }

    r_final = float(r_history[-1])
    r_min = float(np.min(r_history))
    r_max = float(np.max(r_history))
    variation = r_max - r_min

    return {
        "converged": check_convergence(r_history),
        "r_final": r_final,
        "r_min": r_min,
        "r_max": r_max,
        "variation": variation,
        "steps": len(r_history),
    }
