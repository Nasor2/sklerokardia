"""Ecuaciones matemáticas del Modelo del Compás Social.

Paper: "Low-dimensional Dynamics of the Social Compass Model"
Autores: Sampson & Restrepo (2026)
"""

import numpy as np


def agent_dynamics(
    theta_n: float,
    phi_n: float,
    rho_n: float,
    theta_all: np.ndarray,
    K: float,
    N: int,
) -> float:
    """Ecuación 1: Dinámica de un agente individual.

    dθₙ/dt = -ρₙ sin(θₙ - φₙ) + (K/N) Σ sin(θⱼ - θₙ)

    Args:
        theta_n: Orientación actual del agente.
        phi_n: Orientación inicial del agente.
        rho_n: Convicción del agente.
        theta_all: Orientaciones de todos los agentes.
        K: Acoplamiento.
        N: Número de agentes.

    Returns:
        Derivada dθ/dt del agente.
    """
    anchor = -rho_n * np.sin(theta_n - phi_n)
    social = (K / N) * np.sum(np.sin(theta_all - theta_n))
    return anchor + social


def order_parameter(theta_array: np.ndarray) -> tuple[complex, float]:
    """Ecuación 2: Parámetro de orden complejo z y magnitud r.

    z = (1/N) Σ e^{iθₙ}
    r = |z|

    Args:
        theta_array: Orientaciones de todos los agentes.

    Returns:
        Tupla (z, r) donde z es complejo y r es real.
    """
    z = np.mean(np.exp(1j * theta_array))
    r = np.abs(z)
    return z, r


def dalpha_dt(
    alpha: complex,
    rho: float,
    phi: float,
    z: complex,
    K: float,
) -> complex:
    """Ecuación 7: ODE de Ott-Antonsen para α.

    ∂α/∂t = -i[ρe^{-iφ} + Kz]α - (iK/2)(z̄α² - ᾱ) + (K/2)(z - z̄α²)

    Args:
        alpha: Coeficiente Fourier actual (complejo).
        rho: Convicción del agente.
        phi: Orientación inicial del agente.
        z: Parámetro de orden global (complejo).
        K: Acoplamiento.

    Returns:
        Derivada dα/dt (complejo).
    """
    z_bar = np.conj(z)
    exp_neg_iphi = np.exp(-1j * phi)

    term1 = -1j * (exp_neg_iphi + K * z) * alpha
    term2 = -1j * (K / 2) * (z_bar * alpha**2 - np.conj(alpha))
    term3 = (K / 2) * (z - z_bar * alpha**2)

    return term1 + term2 + term3


def compute_z(alpha_array: np.ndarray, d_array: np.ndarray) -> complex:
    """Ecuación 8: Parámetro de orden a partir de α.

    z = Σ dₖ αₖ

    Args:
        alpha_array: Array de alphas (complejos).
        d_array: Fracciones de cada cluster.

    Returns:
        Parámetro de orden z (complejo).
    """
    return np.sum(d_array * alpha_array)


def critical_coupling(conviction_samples: np.ndarray) -> float:
    """Ecuación 27: Acoplamiento crítico Kc.

    Kc = 2 / E[ρ⁻¹]

    Args:
        conviction_samples: Array de convicciones ρ.

    Returns:
        Acoplamiento crítico Kc (real positivo).
    """
    inv_rho_mean = np.mean(1.0 / conviction_samples)
    return 2.0 / inv_rho_mean


def growth_rate(
    K: float,
    phi_distribution: np.ndarray,
    conviction_samples: np.ndarray | None = None,
) -> float:
    """Tasa de crecimiento λ del parámetro de orden.

    Implementa la Ecuación 28 del paper (caso general cerca de Kc):
        λ ≈ Δ · E[ρ⁻²] / E[ρ⁻¹]
    donde Δ = (K - Kc) / Kc

    Para el caso P(ρ) = δ(ρ-1), la Ecuación 25 da:
        λ = K(1 + |E[e^{-2iφ}]|) - 1

    Args:
        K: Acoplamiento actual.
        phi_distribution: Distribución de orientaciones iniciales.
        conviction_samples: Array de convicciones ρ (opcional).
            Si se provee, usa la fórmula general (Ec. 28).
            Si no, usa la fórmula simplificada (Ec. 25).

    Returns:
        Tasa de crecimiento λ (real).
    """
    if conviction_samples is not None and len(conviction_samples) > 0:
        # Ecuación 28: λ ≈ (K - Kc) · E[ρ⁻²] / E[ρ⁻¹]
        Kc_val = critical_coupling(conviction_samples)
        E_inv_rho = np.mean(1.0 / conviction_samples)
        E_inv_rho2 = np.mean(1.0 / conviction_samples**2)
        delta = (K - Kc_val) / Kc_val if Kc_val > 0 else 0.0
        lam = delta * E_inv_rho2 / E_inv_rho
    else:
        # Ecuación 25 (simplificada, válida solo para P(ρ) = δ(ρ-1))
        E_exp = np.mean(np.exp(-2j * phi_distribution))
        lam = K * (1 + np.abs(E_exp)) - 1
    return lam


def growth_rate_near_critical(
    delta_K: float,
    Kc: float,
    conviction_samples: np.ndarray,
) -> float:
    """Ecuación 28: Tasa de crecimiento cerca de Kc.

    λ ≈ Δ · E[ρ⁻²] / E[ρ⁻¹]
    donde Δ = (K - Kc) / Kc

    Args:
        delta_K: Distancia al punto crítico (K - Kc).
        Kc: Acoplamiento crítico.
        conviction_samples: Array de convicciones ρ.

    Returns:
        Tasa de crecimiento λ (real).
    """
    E_inv_rho = np.mean(1.0 / conviction_samples)
    E_inv_rho2 = np.mean(1.0 / conviction_samples**2)

    delta = delta_K / Kc
    lambda_rate = delta * E_inv_rho2 / E_inv_rho
    return lambda_rate
