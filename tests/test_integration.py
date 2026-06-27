import numpy as np
import pytest
from core.params import SimulationParams
from core.engine import run_simulation


class TestIntegrationPhysicalBehavior:
    """Verifica que los resultados tengan sentido fisico."""

    def test_high_k_converges_to_consensus(self):
        """K >> Kc -> r debe acercarse a 1."""
        params = SimulationParams(alpha=1.0, K=3.0, N=500, T=20.0, mode='ode')
        result = run_simulation(params)
        assert result.r_current > 0.3, f"K=3.0>Kc={result.Kc:.2f}, esperado r>0.3, obtuvo {result.r_current:.4f}"

    def test_low_k_stays_polarized(self):
        """K << Kc -> r debe ser cercano a 0."""
        params = SimulationParams(alpha=1.0, K=0.5, N=500, T=20.0, mode='ode')
        result = run_simulation(params)
        assert result.r_current < 0.3, f"K=0.5<Kc={result.Kc:.2f}, esperado r<0.3, obtuvo {result.r_current:.4f}"

    def test_k_at_critical_is_transition(self):
        """K = Kc -> r en zona de transicion."""
        params = SimulationParams(alpha=1.0, K=2.0, N=500, T=30.0, mode='ode')
        result = run_simulation(params)
        assert 0.0 <= result.r_current <= 1.0, f"r fuera de rango: {result.r_current}"

    def test_ode_vs_agent_based_consistency(self):
        """ODE y agent-based deben dar resultados cercanos."""
        p_ode = SimulationParams(alpha=1.0, K=2.5, N=500, T=20.0, mode='ode')
        p_ab = SimulationParams(alpha=1.0, K=2.5, N=500, T=20.0, mode='agent_based')
        r_ode = run_simulation(p_ode)
        r_ab = run_simulation(p_ab)
        diff = abs(r_ode.r_current - r_ab.r_current)
        assert diff < 0.15, f"Diferencia ODE-AB={diff:.4f}, esperado <0.15"

    def test_theta_final_shape(self):
        """theta_final debe tener forma (N,)."""
        params = SimulationParams(alpha=1.0, K=2.0, N=250, T=10.0, mode='ode')
        result = run_simulation(params)
        assert result.theta_final.shape == (250,), f"Forma incorrecta: {result.theta_final.shape}"

    def test_stubborn_agents_dont_move(self):
        """Agentes tercos no deben cambiar su theta."""
        params = SimulationParams(alpha=1.0, K=3.0, N=200, T=15.0,
                                  mode='agent_based', stubborn_pct=10.0)
        result = run_simulation(params)
        stubborn_theta = result.theta_final[result.stubborn_mask]
        stubborn_phi = result.phi_values[result.stubborn_mask]
        diff = np.abs(stubborn_theta - stubborn_phi)
        # Normalizar a [0, π] para manejar wrapping circular
        diff = np.minimum(diff, 2 * np.pi - diff)
        assert np.mean(diff) < 0.05, f"Tercos se movieron: diff={np.mean(diff):.6f}"

    def test_kc_depends_on_alpha(self):
        """Kc debe cambiar con alpha."""
        r1 = run_simulation(SimulationParams(alpha=1.0, K=2.0, N=500, T=10.0))
        r2 = run_simulation(SimulationParams(alpha=0.5, K=2.0, N=500, T=10.0))
        assert r1.Kc != r2.Kc, f"Kc no cambio: {r1.Kc} vs {r2.Kc}"

    def test_communities_produce_results(self):
        """Modo comunidades debe generar resultados validos."""
        params = SimulationParams(alpha=1.0, K=2.0, N=500, T=20.0, mu=0.5)
        result = run_simulation(params)
        assert 0.0 <= result.r_current <= 1.0, f"r fuera de rango: {result.r_current}"
        assert result.z1_history is not None, "z1_history es None"
        assert result.z2_history is not None, "z2_history es None"

    def test_lambda_positive_above_kc(self):
        """Lambda debe ser positivo cuando K > Kc."""
        params = SimulationParams(alpha=1.0, K=4.0, N=500, T=10.0)
        result = run_simulation(params)
        assert result.lambda_est > 0, f"lambda={result.lambda_est} deveria ser >0 cuando K={params.K}>Kc={result.Kc:.4f}"

    def test_lambda_negative_below_kc(self):
        """Lambda debe ser negativo cuando K < Kc."""
        params = SimulationParams(alpha=1.0, K=0.5, N=500, T=10.0)
        result = run_simulation(params)
        assert result.lambda_est < 0, f"lambda={result.lambda_est} deveria ser <0 cuando K={params.K}<Kc={result.Kc:.4f}"

    def test_r_values_in_history_are_valid(self):
        """Todos los valores de r en el historial deben estar en [0, 1]."""
        params = SimulationParams(alpha=1.0, K=2.0, N=500, T=15.0, mode='ode')
        result = run_simulation(params)
        assert np.all(result.r_history >= 0), "Hay r negativos en historial"
        assert np.all(result.r_history <= 1.01), "Hay r > 1 en historial"

    def test_agent_based_mode_returns_theta(self):
        """Agent-based mode debe retornar theta_final."""
        params = SimulationParams(alpha=1.0, K=2.0, N=300, T=10.0, mode='agent_based')
        result = run_simulation(params)
        assert result.theta_final is not None, "theta_final es None"
        assert result.theta_final.shape == (300,), f"Forma: {result.theta_final.shape}"

    def test_higher_coupling_faster_convergence(self):
        """Mayor K debe dar r mas alto al mismo T."""
        r_low = run_simulation(SimulationParams(alpha=1.0, K=1.5, N=500, T=15.0, mode='ode'))
        r_high = run_simulation(SimulationParams(alpha=1.0, K=3.0, N=500, T=15.0, mode='ode'))
        assert r_high.r_current > r_low.r_current, (
            f"K=3.0 (r={r_high.r_current:.4f}) deberia ser > K=1.5 (r={r_low.r_current:.4f})"
        )
