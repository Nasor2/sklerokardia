"""Configuración por defecto del simulador Skleokardia."""

DEFAULTS = {
    "alpha": 1.0,
    "K": 1.0,
    "stubborn_pct": 5,
    "mu": 0.5,
    "mode": "ode",
    "scenario": "Personalizado",
}

RANGES = {
    "alpha": {"min": 0.1, "max": 10.0, "step": 0.1},
    "K": {"min": 0.0, "max": 5.0, "step": 0.1},
    "stubborn_pct": {"min": 0, "max": 30, "step": 1},
    "mu": {"min": 0.0, "max": 1.0, "step": 0.05},
}

SIMULATION_PARAMS = {
    "N": 1000,
    "T": 50.0,
    "dt": 0.05,
    "rho_max": 1000.0,
}

CONVERGENCE_PARAMS = {
    "window": 50,
    "threshold": 1e-4,
}
