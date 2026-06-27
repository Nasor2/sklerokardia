"""Tests para los motores de simulación."""

import numpy as np
import pytest

from core.engine import initialize_agents, run_simulation
from core.params import SimulationParams


class TestInitializeAgents:
    """Tests para la inicialización de agentes."""

    def test_creates_correct_number(self):
        """Debe crear N agentes."""
        params = SimulationParams(N=500)
        phi, rho, theta, stubborn = initialize_agents(params)
        assert len(phi) == 500
        assert len(rho) == 500
        assert len(theta) == 500
        assert len(stubborn) == 500

    def test_stubborn_percentage(self):
        """Porcentaje de tercos debe ser aproximado."""
        params = SimulationParams(N=1000, stubborn_pct=10)
        _, _, _, stubborn = initialize_agents(params)
        assert abs(sum(stubborn) - 100) < 10

    def test_theta_equals_phi_initially(self):
        """Theta debe ser cercano a phi inicialmente (con perturbación pequeña)."""
        params = SimulationParams(N=100)
        phi, _, theta, _ = initialize_agents(params)
        np.testing.assert_allclose(theta, phi, atol=0.2)

    def test_stubborn_high_rho(self):
        """Agentes tercos deben tener rho alto."""
        params = SimulationParams(N=1000, stubborn_pct=10)
        _, rho, _, stubborn = initialize_agents(params)
        assert np.all(rho[stubborn] == 1000.0)


class TestRunSimulation:
    """Tests para la ejecución de simulación."""

    def test_ode_mode(self):
        """Modo ODE debe funcionar."""
        params = SimulationParams(alpha=1.0, K=2.0, mode="ode", N=100, T=10)
        result = run_simulation(params)
        assert len(result.r_history) > 0
        assert result.mode_used == "ode"

    def test_agent_based_mode(self):
        """Modo agent-based debe funcionar."""
        params = SimulationParams(alpha=1.0, K=2.0, mode="agent_based", N=100, T=10, dt=0.1)
        result = run_simulation(params)
        assert len(result.r_history) > 0
        assert result.mode_used == "agent_based"

    def test_kc_positive(self):
        """Kc debe ser positivo."""
        params = SimulationParams(N=100)
        result = run_simulation(params)
        assert result.Kc > 0

    def test_r_between_0_and_1(self):
        """r debe estar entre 0 y 1 en modo agent-based."""
        params = SimulationParams(alpha=1.0, K=2.0, mode="agent_based", N=100, T=10, dt=0.1)
        result = run_simulation(params)
        assert np.all(result.r_history >= 0)
        assert np.all(result.r_history <= 1)

    def test_invalid_params_raises(self):
        """Parámetros inválidos deben lanzar error."""
        params = SimulationParams(alpha=0.0)
        with pytest.raises(ValueError):
            run_simulation(params)

    def test_high_k_converges_to_consensus(self):
        """K alto debe converger a consenso (sin comunidades)."""
        params = SimulationParams(alpha=1.0, K=4.0, mode="agent_based", mu=1.0, N=100, T=10, dt=0.1)
        result = run_simulation(params)
        assert result.r_current > 0.5

    def test_communities_mode(self):
        """Modo comunidades debe funcionar con mu < 1."""
        params = SimulationParams(alpha=1.0, K=2.0, mode="agent_based", mu=0.5, N=100, T=10, dt=0.1)
        result = run_simulation(params)
        assert len(result.r_history) > 0
        assert np.all(result.r_history >= 0)
        assert np.all(result.r_history <= 1)
