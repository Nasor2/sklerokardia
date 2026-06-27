"""Tests unitarios para core/model.py."""

import numpy as np
import pytest

from core.model import (
    agent_dynamics,
    compute_z,
    critical_coupling,
    dalpha_dt,
    growth_rate,
    order_parameter,
)


class TestOrderParameter:
    """Tests para la ecuación 2: parámetro de orden."""

    def test_all_aligned(self):
        """Agentes alineados deben dar r = 1."""
        theta = np.array([0.0, 0.0, 0.0, 0.0])
        z, r = order_parameter(theta)
        assert abs(r - 1.0) < 1e-10

    def test_opposed(self):
        """Agentes opuestos deben dar r ≈ 0."""
        theta = np.array([0.0, np.pi, 0.0, np.pi])
        z, r = order_parameter(theta)
        assert r < 0.01

    def test_partial_alignment(self):
        """Agentes parcialmente alineados."""
        theta = np.array([0.0, 0.1, 0.0, 0.1])
        z, r = order_parameter(theta)
        assert 0.9 < r < 1.0

    def test_uniform_distribution(self):
        """Distribución uniforme debe dar r ≈ 0."""
        theta = np.linspace(0, 2 * np.pi, 1000, endpoint=False)
        z, r = order_parameter(theta)
        assert r < 0.05

    def test_z_is_complex(self):
        """z debe ser un número complejo."""
        theta = np.array([0.0, np.pi / 2])
        z, r = order_parameter(theta)
        assert isinstance(z, complex)


class TestCriticalCoupling:
    """Tests para la ecuación 27: acoplamiento crítico."""

    def test_uniform_conviction(self):
        """Para ρ = 1 uniforme, Kc = 2."""
        rho = np.ones(1000)
        Kc = critical_coupling(rho)
        assert abs(Kc - 2.0) < 1e-10

    def test_high_conviction(self):
        """Mayor ρ → mayor Kc (menos interacción necesaria)."""
        rho_low = np.ones(1000) * 0.5
        rho_high = np.ones(1000) * 2.0
        Kc_low = critical_coupling(rho_low)
        Kc_high = critical_coupling(rho_high)
        assert Kc_high > Kc_low

    def test_mixed_conviction(self):
        """Mezcla de convicciones."""
        rho = np.concatenate([np.ones(500) * 0.5, np.ones(500) * 2.0])
        Kc = critical_coupling(rho)
        assert 1.0 < Kc < 3.0


class TestGrowthRate:
    """Tests para la ecuación 25: tasa de crecimiento."""

    def test_zero_coupling(self):
        """K = 0 debe dar λ < 0."""
        phi = np.array([0.0, np.pi, np.pi / 2, -np.pi / 2])
        lam = growth_rate(0.0, phi)
        assert lam < 0

    def test_high_coupling(self):
        """K alto debe dar λ > 0."""
        phi = np.array([0.0, np.pi, np.pi / 2, -np.pi / 2])
        lam = growth_rate(10.0, phi)
        assert lam > 0

    def test_symmetric_distribution(self):
        """Distribución simétrica: |E[e^{-2iφ}]| = 0."""
        phi = np.array([0.0, np.pi / 2, np.pi, 3 * np.pi / 2])
        lam = growth_rate(1.0, phi)
        assert abs(lam - 0.0) < 1e-10


class TestAlphaDt:
    """Tests para la ecuación 7: ODE de Ott-Antonsen."""

    def test_equilibrium_polarized(self):
        """En equilibrio polarizado (z=0), dα/dt debe ser específico."""
        alpha = np.exp(-1j * 0.0)
        rho = 1.0
        phi = 0.0
        z = 0.0
        K = 1.0

        d_alpha = dalpha_dt(alpha, rho, phi, z, K)
        # Verificar que es un número complejo
        assert isinstance(d_alpha, complex)

    def test_returns_complex(self):
        """Debe retornar un número complejo."""
        alpha = 0.5 + 0.5j
        rho = 1.0
        phi = 0.0
        z = 0.1 + 0.1j
        K = 1.0

        d_alpha = dalpha_dt(alpha, rho, phi, z, K)
        assert isinstance(d_alpha, complex)


class TestComputeZ:
    """Tests para la ecuación 8: z a partir de α."""

    def test_single_cluster(self):
        """Un solo cluster."""
        alpha = np.array([0.5 + 0.5j])
        d = np.array([1.0])
        z = compute_z(alpha, d)
        assert abs(z - (0.5 + 0.5j)) < 1e-10

    def test_two_clusters(self):
        """Dos clusters con fracciones iguales."""
        alpha = np.array([1.0 + 0.0j, 0.0 + 1.0j])
        d = np.array([0.5, 0.5])
        z = compute_z(alpha, d)
        expected = 0.5 * (1.0 + 1.0j)
        assert abs(z - expected) < 1e-10


class TestAgentDynamics:
    """Tests para la ecuación 1: dinámica de agentes."""

    def test_no_interaction(self):
        """Sin interacción (K=0), solo convicción."""
        theta_n = 0.0
        phi_n = 0.1
        rho_n = 1.0
        theta_all = np.array([0.0, 0.0, 0.0])
        K = 0.0
        N = 3

        d_theta = agent_dynamics(theta_n, phi_n, rho_n, theta_all, K, N)
        expected = -rho_n * np.sin(theta_n - phi_n)
        assert abs(d_theta - expected) < 1e-10

    def test_symmetric_interaction(self):
        """Interacción simétrica (todos en la misma posición)."""
        theta_n = 0.0
        phi_n = 0.0
        rho_n = 1.0
        theta_all = np.array([0.0, 0.0, 0.0])
        K = 1.0
        N = 3

        d_theta = agent_dynamics(theta_n, phi_n, rho_n, theta_all, K, N)
        # Si todos están en la misma posición, la interacción es 0
        assert abs(d_theta) < 1e-10
