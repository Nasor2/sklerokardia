"""Escenarios predefinidos para la simulación."""

import numpy as np

SCENARIOS = {
    "Personalizado": {
        "description": "Configura los parámetros manualmente.",
        "alpha": 1.0,
        "K": 1.0,
        "stubborn_pct": 5,
        "mu": 0.5,
        "phi0": np.pi / 6,
    },
    "Polarización urbano-rural": {
        "description": "Dos comunidades fuertemente separadas (µ bajo). Simula tensión campo-ciudad.",
        "alpha": 2.0,
        "K": 0.5,
        "stubborn_pct": 15,
        "mu": 0.2,
        "phi0": np.pi / 6,
    },
    "Campaña electoral": {
        "description": "Moderada separación comunitaria con influencia social media. Ideal para estudiar transiciones.",
        "alpha": 1.5,
        "K": 2.0,
        "stubborn_pct": 10,
        "mu": 0.6,
        "phi0": np.pi / 4,
    },
    "Diálogo de paz": {
        "description": "Alta interacción social y comunidades parcialmente conectadas. Busca consenso global.",
        "alpha": 1.0,
        "K": 3.0,
        "stubborn_pct": 5,
        "mu": 0.8,
        "phi0": np.pi / 6,
    },
    "Sociedad homogénea": {
        "description": "Sin estructura comunitaria ni agentes tercos. Caso base del paper.",
        "alpha": 1.0,
        "K": 1.5,
        "stubborn_pct": 0,
        "mu": 1.0,
        "phi0": np.pi / 7,
    },
    "Crítico (K ≈ Kc)": {
        "description": "Justo en el umbral de transición de fase. K se ajusta automáticamente según α. Observa fluctuaciones lentas.",
        "alpha": 1.0,
        "K": 1.9,  # Kc ≈ 2/E[ρ⁻¹] ≈ 1.9 para α=1.0
        "stubborn_pct": 5,
        "mu": 1.0,
        "phi0": np.pi / 6,
    },
}
