"""Motor de simulación - orquestador principal."""

import numpy as np

from core.convergence import check_convergence
from core.model import critical_coupling, growth_rate, order_parameter
from core.params import SimulationParams, SimulationResult
from simulation.agent_based import run_agent_based
from simulation.communities import critical_coupling_communities, run_communities
from simulation.ode_reducer import run_ode


def initialize_agents(params: SimulationParams) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Inicializa las propiedades de los agentes.

    Distribución cuadrimodal asimétrica para φ y variación normal para ρ.

    Args:
        params: Parámetros de la simulación.

    Returns:
        Tupla (phi, rho, theta, stubborn_mask).
    """
    N = params.N
    phi0 = params.phi0

    # Distribución cuadrimodal asimétrica para phi (tamaños diferentes para romper simetría)
    sizes = [int(N * 0.30), int(N * 0.20), int(N * 0.25)]
    sizes.append(N - sum(sizes))
    phi = np.concatenate([
        np.full(sizes[0], phi0),
        np.full(sizes[1], phi0 - np.pi),
        np.full(sizes[2], -phi0),
        np.full(sizes[3], -phi0 + np.pi),
    ])

    # Convicciones: base alpha + variación
    rho_base = params.alpha
    rho = np.abs(np.random.normal(rho_base, rho_base * 0.2, N))

    # Agentes tercos
    n_stubborn = int(N * params.stubborn_pct / 100)
    stubborn_mask = np.zeros(N, dtype=bool)
    if n_stubborn > 0:
        stubborn_indices = np.random.choice(N, n_stubborn, replace=False)
        stubborn_mask[stubborn_indices] = True
        rho[stubborn_mask] = 1000.0  # rho_max para tercos

    # Theta inicial = phi + perturbación para romper simetría residual
    theta = phi.copy() + np.random.normal(0, 0.05, N)

    return phi, rho, theta, stubborn_mask


def run_simulation(params: SimulationParams) -> SimulationResult:
    """Punto de entrada principal de la simulación.

    Args:
        params: Parámetros configurados por el usuario.

    Returns:
        SimulationResult con todos los resultados.

    Raises:
        ValueError: Si los parámetros no son válidos.
    """
    # Validar parámetros
    errors = params.validate()
    if errors:
        raise ValueError(f"Parámetros inválidos: {'; '.join(errors)}")

    # Inicializar agentes
    phi, rho, theta, stubborn_mask = initialize_agents(params)

    # Calcular Kc teórico (con comunidades si mu < 1)
    if params.mu < 1.0:
        Kc = critical_coupling_communities(rho, params.mu)
    else:
        Kc = critical_coupling(rho)

    # Ejecutar según el modo
    z1_hist = None
    z2_hist = None
    theta_final = theta.copy()

    if params.mu < 1.0:
        t_hist, r_hist, z_hist, z1_hist, z2_hist, theta_final = run_communities(
            K=params.K,
            N=params.N,
            T=params.T,
            dt=params.dt,
            phi=phi,
            rho=rho,
            mu=params.mu,
            stubborn_mask=stubborn_mask,
        )
    elif params.mode == "ode":
        t_hist, r_hist, z_hist, theta_final = run_ode(
            K=params.K,
            N=params.N,
            T=params.T,
            dt=params.dt,
            phi=phi,
            rho=rho,
        )
    else:
        t_hist, r_hist, z_hist, theta_final = run_agent_based(
            K=params.K,
            N=params.N,
            T=params.T,
            dt=params.dt,
            phi=phi,
            rho=rho,
            theta_init=theta,
            stubborn_mask=stubborn_mask,
        )

    # Calcular lambda estimado (usando fórmula general con ρ)
    lambda_est = growth_rate(params.K, phi, conviction_samples=rho)

    # Verificar convergencia
    converged = check_convergence(r_hist)

    return SimulationResult(
        t_history=t_hist,
        r_history=r_hist,
        z_history=z_hist,
        theta_final=theta_final,
        rho_values=rho,
        phi_values=phi,
        stubborn_mask=stubborn_mask,
        Kc=Kc,
        lambda_est=lambda_est,
        converged=converged,
        mode_used=params.mode,
        z1_history=z1_hist,
        z2_history=z2_hist,
    )
