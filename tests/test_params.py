"""Tests unitarios para core/params.py."""

import numpy as np
import pytest

from core.params import SimulationParams, SimulationResult


class TestSimulationParams:
    """Tests para la clase SimulationParams."""

    def test_default_values(self):
        """Valores por defecto deben ser válidos."""
        params = SimulationParams()
        errors = params.validate()
        assert len(errors) == 0

    def test_custom_values(self):
        """Valores personalizados deben ser válidos."""
        params = SimulationParams(alpha=2.0, K=3.0, stubborn_pct=10, mu=0.3)
        errors = params.validate()
        assert len(errors) == 0

    def test_invalid_alpha(self):
        """Alpha fuera de rango debe fallar."""
        params = SimulationParams(alpha=0.0)
        errors = params.validate()
        assert any("Alpha" in e for e in errors)

    def test_invalid_K(self):
        """K fuera de rango debe fallar."""
        params = SimulationParams(K=6.0)
        errors = params.validate()
        assert any("K debe" in e for e in errors)

    def test_invalid_stubborn_pct(self):
        """Stubborn_pct fuera de rango debe fallar."""
        params = SimulationParams(stubborn_pct=40)
        errors = params.validate()
        assert any("Stubborn_pct" in e for e in errors)

    def test_invalid_mu(self):
        """Mu fuera de rango debe fallar."""
        params = SimulationParams(mu=1.5)
        errors = params.validate()
        assert any("Mu" in e for e in errors)

    def test_invalid_mode(self):
        """Modo inválido debe fallar."""
        params = SimulationParams(mode="invalid")
        errors = params.validate()
        assert any("Mode" in e for e in errors)


class TestSimulationResult:
    """Tests para la clase SimulationResult."""

    def _create_result(self, r_values: np.ndarray) -> SimulationResult:
        """Crea un SimulationResult de prueba."""
        n = len(r_values)
        return SimulationResult(
            t_history=np.linspace(0, 50, n),
            r_history=r_values,
            z_history=r_values * np.exp(1j * np.zeros(n)),
            theta_final=np.zeros(100),
            rho_values=np.ones(100),
            phi_values=np.zeros(100),
            stubborn_mask=np.zeros(100, dtype=bool),
            Kc=2.0,
            lambda_est=0.5,
            converged=True,
            mode_used="ode",
        )

    def test_r_current_low(self):
        """r bajo debe ser 'Polarizado'."""
        result = self._create_result(np.array([0.05, 0.05, 0.05]))
        assert result.state == "Polarizado"

    def test_r_current_medium(self):
        """r medio debe ser 'Transición'."""
        result = self._create_result(np.array([0.3, 0.3, 0.3]))
        assert result.state == "Transición"

    def test_r_current_high(self):
        """r alto debe ser 'Consenso'."""
        result = self._create_result(np.array([0.8, 0.8, 0.8]))
        assert result.state == "Consenso"

    def test_r_current_property(self):
        """r_current debe retornar el último valor."""
        result = self._create_result(np.array([0.1, 0.5, 0.9]))
        assert result.r_current == pytest.approx(0.9)
