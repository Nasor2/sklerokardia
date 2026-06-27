"""Simulación con estructura de dos comunidades (ec. 43)."""

import numpy as np

from core.model import order_parameter


def run_communities(
    K: float,
    N: int,
    T: float,
    dt: float,
    phi: np.ndarray,
    rho: np.ndarray,
    mu: float,
    stubborn_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Simula dos comunidades con acoplamiento intra/inter.

    Ecuación 43:
    dθₙ^σ/dt = -ρₙ^σ sin(θₙ^σ - φₙ^σ)
                + (K_σσ / (N/2)) Σ_{j∈σ} sin(θⱼ^σ - θₙ^σ)
                + (K_σσ' / (N/2)) Σ_{j∈σ'} sin(θⱼ^σ' - θₙ^σ)

    Donde:
    - K_σσ = K (intra-comunidad)
    - K_σσ' = µK (inter-comunidad)
    - µ ∈ [0, 1]: separación comunitaria

    Args:
        K: Acoplamiento base.
        N: Número total de agentes (par).
        T: Tiempo final.
        dt: Paso temporal.
        phi: Orientaciones iniciales.
        rho: Convicciones.
        mu: Separación comunitaria (0 = aisladas, 1 = sin estructura).

    Returns:
        Tupla (t_history, r_history, z_history, z1_history, z2_history, theta_final).
    """
    n_steps = int(T / dt)
    half_N = N // 2

    # Acoplamientos
    K_intra = K  # K_σσ
    K_inter = mu * K  # K_σσ'

    theta = phi.copy()
    if stubborn_mask is None:
        stubborn_mask = np.zeros(N, dtype=bool)

    t_history = np.zeros(n_steps)
    r_history = np.zeros(n_steps)
    z_history = np.zeros(n_steps, dtype=complex)
    z1_history = np.zeros(n_steps, dtype=complex)
    z2_history = np.zeros(n_steps, dtype=complex)

    for step in range(n_steps):
        t = step * dt

        theta1 = theta[:half_N]
        theta2 = theta[half_N:]
        z1 = np.mean(np.exp(1j * theta1))
        z2 = np.mean(np.exp(1j * theta2))

        z = (z1 + z2) / 2
        r = np.abs(z)

        t_history[step] = t
        r_history[step] = r
        z_history[step] = z
        z1_history[step] = z1
        z2_history[step] = z2

        social_intra = np.zeros(N)
        for sigma, (start, end) in enumerate([(0, half_N), (half_N, N)]):
            theta_sigma = theta[start:end]
            diff = np.sin(theta_sigma[np.newaxis, :] - theta_sigma[:, np.newaxis])
            social_intra[start:end] = K_intra * np.mean(diff, axis=1)

        social_inter = np.zeros(N)
        diff_12 = np.sin(theta2[np.newaxis, :] - theta1[:, np.newaxis])
        social_inter[:half_N] = K_inter * np.mean(diff_12, axis=0)
        diff_21 = np.sin(theta1[np.newaxis, :] - theta2[:, np.newaxis])
        social_inter[half_N:] = K_inter * np.mean(diff_21, axis=0)

        dtheta = np.zeros(N)
        for n in range(N):
            if not stubborn_mask[n]:
                dtheta[n] = -rho[n] * np.sin(theta[n] - phi[n]) + social_intra[n] + social_inter[n]

        theta = theta + dtheta * dt
        theta = theta % (2 * np.pi)

    return t_history, r_history, z_history, z1_history, z2_history, theta


def critical_coupling_communities(
    rho: np.ndarray,
    mu: float,
    phi0: float = np.pi / 6,
) -> float:
    """Ecuación 67: Acoplamiento crítico con comunidades.

    Kc = 2(1 + µR) / (E[ρ⁻¹](1 + µ))

    Donde R = (sin(η₁) + sin(η₃))/2 y η son los ángulos de equilibrio.

    Args:
        rho: Convicciones de los agentes.
        mu: Separación comunitaria.
        phi0: Ángulo de separación cuadrimodal.

    Returns:
        Acoplamiento crítico Kc (real positivo).
    """
    inv_rho_mean = np.mean(1.0 / rho)
    R = np.sin(phi0)  # Simplificación para distribución simétrica
    Kc = 2 * (1 + mu * R) / (inv_rho_mean * (1 + mu))
    return Kc
