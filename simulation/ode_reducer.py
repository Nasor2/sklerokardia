"""Simulación con método de Euler vectorizado (modo rápido).

Implementa la Ecuación 1 del modelo usando operaciones vectorizadas
para mayor rendimiento. NO implementa el Ansatz de Ott-Antonsen
(Ecuaciones 7-8), que requiere resolver ODEs para los coeficientes α.

Este modo produce los mismos resultados que agent_based.py pero
es significativamente más rápido得益于 la vectorización con NumPy.
"""

import numpy as np
from scipy.integrate import solve_ivp


def run_ode(
    K: float,
    N: int,
    T: float,
    dt: float,
    phi: np.ndarray,
    rho: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Resuelve el sistema de ODEs usando Euler para agentes discretos.

    Para M agentes:
    - M ODEs para θ (ángulos)
    - Acoplamiento via z = (1/M) Σ e^{iθⱼ}

    Args:
        K: Acoplamiento.
        N: Número de agentes (para normalización).
        T: Tiempo final.
        dt: Paso temporal.
        phi: Orientaciones iniciales de los agentes.
        rho: Convicciones de los agentes.

    Returns:
        Tupla (t_history, r_history, z_history, theta_final).
    """
    M = len(phi)
    n_steps = int(T / dt)

    # Estado inicial: θ = φ
    theta = phi.copy()

    # Historiales
    t_history = np.zeros(n_steps)
    r_history = np.zeros(n_steps)
    z_history = np.zeros(n_steps, dtype=complex)

    # Simular con Euler
    for step in range(n_steps):
        t = step * dt

        # Calcular parámetro de orden
        z = np.mean(np.exp(1j * theta))
        r = np.abs(z)

        # Guardar
        t_history[step] = t
        r_history[step] = r
        z_history[step] = z

        # Calcular derivadas (vectorizado)
        sin_diff = np.sin(theta - phi)
        # Ecuación 1: (K/N) Σ sin(θⱼ - θₙ)
        # theta[np.newaxis, :] broadcastea θⱼ, theta[:, np.newaxis] broadcastea θₙ
        social = np.sin(theta[np.newaxis, :] - theta[:, np.newaxis])
        social_sum = np.mean(social, axis=1)

        dtheta = -rho * sin_diff + K * social_sum

        # Actualizar (Euler)
        theta = theta + dtheta * dt

        # Normalizar a [0, 2π)
        theta = theta % (2 * np.pi)

    return t_history, r_history, z_history, theta
