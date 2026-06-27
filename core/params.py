"""Definición de parámetros y resultados de simulación."""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimulationParams:
    """Parámetros de entrada para la simulación.

    Attributes:
        alpha:ρ base (amarre ideológico).
        K: Acoplamiento (influencia social).
        stubborn_pct: Porcentaje de agentes tercos.
        mu: Separación comunitaria.
        N: Número de agentes.
        T: Tiempo final de simulación.
        dt: Paso temporal.
        mode: Modo de simulación ('ode' o 'agent_based').
        scenario: Nombre del escenario seleccionado.
    """

    alpha: float = 1.0
    K: float = 1.0
    stubborn_pct: float = 5.0
    mu: float = 0.5
    phi0: float = np.pi / 6
    N: int = 1000
    T: float = 50.0
    dt: float = 0.05
    mode: str = "ode"
    scenario: str = "Personalizado"

    def validate(self) -> list[str]:
        """Valida que los parámetros estén en rangos aceptables.

        Returns:
            Lista de mensajes de error. Vacía si es válido.
        """
        errors = []

        if not 0.1 <= self.alpha <= 10.0:
            errors.append(f"Alpha debe estar entre 0.1 y 10.0, got {self.alpha}")

        if not 0.0 <= self.K <= 5.0:
            errors.append(f"K debe estar entre 0.0 y 5.0, got {self.K}")

        if not 0 <= self.stubborn_pct <= 30:
            errors.append(f"Stubborn_pct debe estar entre 0 y 30, got {self.stubborn_pct}")

        if not 0.0 <= self.mu <= 1.0:
            errors.append(f"Mu debe estar entre 0.0 y 1.0, got {self.mu}")

        if not 0.0 <= self.phi0 <= np.pi / 2:
            errors.append(f"Phi0 debe estar entre 0.0 y π/2, got {self.phi0}")

        if not 100 <= self.N <= 2000:
            errors.append(f"N debe estar entre 100 y 2000, got {self.N}")

        if not 10.0 <= self.T <= 200.0:
            errors.append(f"T debe estar entre 10.0 y 200.0, got {self.T}")

        if not 0.01 <= self.dt <= 0.1:
            errors.append(f"dt debe estar entre 0.01 y 0.1, got {self.dt}")

        if self.mode not in ("ode", "agent_based"):
            errors.append(f"Mode debe ser 'ode' o 'agent_based', got {self.mode}")

        return errors


@dataclass
class SimulationResult:
    """Resultados de la simulación.

    Attributes:
        t_history: Historial de tiempo.
        r_history: Historial del grado de consenso r(t).
        z_history: Historial del parámetro de orden complejo z(t).
        theta_final: Orientaciones finales de los agentes.
        rho_values: Convicciones de los agentes.
        phi_values: Orientaciones iniciales de los agentes.
        stubborn_mask: Máscara booleana de agentes tercos.
        Kc: Acoplamiento crítico teórico.
        lambda_est: Tasa de crecimiento estimada.
        converged: Si la simulación convergió.
        mode_used: Modo de simulación utilizado.
    """

    t_history: np.ndarray
    r_history: np.ndarray
    z_history: np.ndarray
    theta_final: np.ndarray
    rho_values: np.ndarray
    phi_values: np.ndarray
    stubborn_mask: np.ndarray
    Kc: float
    lambda_est: float
    converged: bool
    mode_used: str
    z1_history: np.ndarray | None = None
    z2_history: np.ndarray | None = None

    @property
    def r_current(self) -> float:
        """Grado de consenso actual (último valor de r)."""
        return float(self.r_history[-1]) if len(self.r_history) > 0 else 0.0

    @property
    def state(self) -> str:
        """Estado actual del sistema."""
        r = self.r_current
        if r < 0.1:
            return "Polarizado"
        elif r < 0.5:
            return "Transición"
        else:
            return "Consenso"
