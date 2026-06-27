"""Tests unitarios para core/convergence.py."""

import numpy as np
import pytest

from core.convergence import check_convergence, get_convergence_info


class TestCheckConvergence:
    """Tests para la función check_convergence."""

    def test_converged(self):
        """Valores estables deben converger."""
        r_history = np.ones(100) * 0.5 + np.random.normal(0, 1e-6, 100)
        assert check_convergence(r_history) is True

    def test_not_converged(self):
        """Valores crecientes no deben converger."""
        r_history = np.linspace(0, 1, 100)
        assert check_convergence(r_history) is False

    def test_short_history(self):
        """Historial muy corto no debe converger."""
        r_history = np.array([0.5, 0.5, 0.5])
        assert check_convergence(r_history) is False

    def test_custom_threshold(self):
        """Threshold personalizado."""
        r_history = np.ones(100) * 0.5 + np.random.normal(0, 0.01, 100)
        assert check_convergence(r_history, threshold=0.1) is True


class TestGetConvergenceInfo:
    """Tests para la función get_convergence_info."""

    def test_empty_history(self):
        """Historial vacío."""
        info = get_convergence_info(np.array([]))
        assert info["converged"] is False
        assert info["r_final"] == 0.0
        assert info["steps"] == 0

    def test_normal_history(self):
        """Historial normal."""
        r_history = np.linspace(0, 1, 100)
        info = get_convergence_info(r_history)
        assert info["r_final"] == pytest.approx(1.0)
        assert info["r_min"] == pytest.approx(0.0)
        assert info["r_max"] == pytest.approx(1.0)
        assert info["steps"] == 100

    def test_converged_info(self):
        """Información de convergencia."""
        r_history = np.ones(100) * 0.5
        info = get_convergence_info(r_history)
        assert info["converged"] is True
        assert info["variation"] == pytest.approx(0.0)
