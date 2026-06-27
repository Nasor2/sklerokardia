"""Utilidades de validación y formateo."""

import numpy as np


def validate_simulation_params(params: dict) -> list[str]:
    """Valida un diccionario de parámetros de simulación.

    Args:
        params: Diccionario con los parámetros.

    Returns:
        Lista de mensajes de error. Vacía si es válido.
    """
    errors = []

    if "alpha" in params:
        alpha = params["alpha"]
        if not isinstance(alpha, (int, float)):
            errors.append("Alpha debe ser un número")
        elif not 0.1 <= alpha <= 10.0:
            errors.append(f"Alpha debe estar entre 0.1 y 10.0, got {alpha}")

    if "K" in params:
        K = params["K"]
        if not isinstance(K, (int, float)):
            errors.append("K debe ser un número")
        elif not 0.0 <= K <= 5.0:
            errors.append(f"K debe estar entre 0.0 y 5.0, got {K}")

    if "stubborn_pct" in params:
        stubborn_pct = params["stubborn_pct"]
        if not isinstance(stubborn_pct, (int, float)):
            errors.append("Stubborn_pct debe ser un número")
        elif not 0 <= stubborn_pct <= 30:
            errors.append(f"Stubborn_pct debe estar entre 0 y 30, got {stubborn_pct}")

    if "mu" in params:
        mu = params["mu"]
        if not isinstance(mu, (int, float)):
            errors.append("Mu debe ser un número")
        elif not 0.0 <= mu <= 1.0:
            errors.append(f"Mu debe estar entre 0.0 y 1.0, got {mu}")

    return errors


def format_number(value: float, decimals: int = 3) -> str:
    """Formatea un número con decimales específicos.

    Args:
        value: Valor a formatear.
        decimals: Número de decimales.

    Returns:
        String formateado.
    """
    return f"{value:.{decimals}f}"


def format_percentage(value: float) -> str:
    """Formatea un valor como porcentaje.

    Args:
        value: Valor entre 0 y 1.

    Returns:
        String con porcentaje.
    """
    return f"{value * 100:.1f}%"


def get_state_color(r: float) -> str:
    """Retorna el color según el estado del sistema.

    Args:
        r: Grado de consenso.

    Returns:
        Color en formato hex.
    """
    if r < 0.1:
        return "#EF4444"  # Rojo - Polarizado
    elif r < 0.5:
        return "#F59E0B"  # Amarillo - Transición
    else:
        return "#10B981"  # Verde - Consenso
