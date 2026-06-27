"""Simulación paso a paso con agentes individuales (modo Agent-Based)."""

import numpy as np

from core.model import agent_dynamics, order_parameter


def run_agent_based(
    K: float,
    N: int,
    T: float,
    dt: float,
    phi: np.ndarray,
    rho: np.ndarray,
    theta_init: np.ndarray,
    stubborn_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Simula N agentes usando método de Euler.

    En cada paso:
    1. Calcular z actual
    2. Para cada agente: dθ = f(θ, φ, ρ, z, K)
    3. Actualizar θ
    4. Calcular r = |z|

    Agentes tercos (stubborn_mask=True) mantienen θ = φ.

    Args:
        K: Acoplamiento.
        N: Número de agentes.
        T: Tiempo final.
        dt: Paso temporal.
        phi: Orientaciones iniciales.
        rho: Convicciones.
        theta_init: Orientaciones iniciales (= φ inicialmente).
        stubborn_mask: Máscara booleana de agentes tercos.

    Returns:
        Tupla (t_history, r_history, z_history, theta_final).
    """
    n_steps = int(T / dt)

    theta = theta_init.copy()
    if stubborn_mask is None:
        stubborn_mask = np.zeros(N, dtype=bool)

    t_history = np.zeros(n_steps)
    r_history = np.zeros(n_steps)
    z_history = np.zeros(n_steps, dtype=complex)

    for step in range(n_steps):
        t = step * dt

        z, r = order_parameter(theta)

        t_history[step] = t
        r_history[step] = r
        z_history[step] = z

        dtheta = np.zeros(N)
        for n in range(N):
            if not stubborn_mask[n]:
                dtheta[n] = agent_dynamics(theta[n], phi[n], rho[n], theta, K, N)

        theta += dtheta * dt
        theta = theta % (2 * np.pi)

    return t_history, r_history, z_history, theta
