<!-- prettier-ignore -->
<div align="center">
    
# Sklerokardia: Simulador interactivo de dinámica de opiniones basado en el **Modelo del Compás Social**.

<img src="./banner.jpg" alt="Sklerokardia banner" width="100%" />

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Citation](https://img.shields.io/badge/Cite-this_repository-2ea44f?style=flat-square&logo=github&logoColor=white)](#citing-this-project)


[Overview](#overview) · [Quick start](#quick-start) · [Model](#model-parameters) · [Testing](#testing) · [Citing](#citing-this-project)

</div>

## Overview

Sklerokardia es un simulador que modela la evolución de opiniones en poblaciones con opiniones interdependientes, implementando el modelo propuesto por [Sampson & Restrepo (2026)](https://arxiv.org/abs/2606.26378). Permite explorar cómo parámetros sociales (influencia, convicción, estructura comunitaria) determinan la transición entre polarización y consenso.

> [!NOTE]
> El modelo extiende el Modelo del Compás Social original de [Ojer, Starnini & Pastor-Satorras (PRL, 2023)](https://doi.org/10.1103/PhysRevLett.130.207401), utilizando el Ansatz de Ott-Antonsen para derivar ecuaciones de baja dimensión que describen la dinámica macroscópica.

### Features

- Tres modos de simulación: Euler vectorizado (rápido), agent-based (detallado), comunidades (con µ)
- Panel interactivo con sliders para todos los parámetros del modelo
- Escenarios predefinidos (polarización urbano-rural, campaña electoral, diálogo de paz)
- Gráficos polar y temporales con Plotly
- Ecuaciones renderizadas en LaTeX directamente en la interfaz
- Detección automática de convergencia

## Quick start

```bash
# Clone the repository
git clone https://github.com/Nasor2/sklerokardia.git
cd sklerokardia

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

> [!TIP]
> La aplicación se abrirá en `http://localhost:8501`. Configura los parámetros en el sidebar y presiona **Ejecutar** para iniciar una simulación.

## Model Parameters

| Parameter | Symbol | Range | Description |
|-----------|--------|-------|-------------|
| Ideological anchor | α (ρ base) | 0.1 – 10.0 | Average belief firmness. Higher = more resistance to change. |
| Social influence | K | 0.0 – 5.0 | Interaction strength. K > Kc triggers consensus. |
| Community separation | µ | 0.0 – 1.0 | 0 = isolated communities, 1 = no community structure. |
| Angular separation | φ₀ | 0 – π/2 | Separates initial opinion clusters. |
| Stubborn agents | — | 0 – 30% | Percentage of agents with extremely high ρ (never change). |

The critical coupling K_c = 2 / E[ρ⁻¹] determines the phase transition. When K > K_c, the polarized state becomes unstable and consensus emerges.

## Simulation Modes

| Mode | When | Description |
|------|------|-------------|
| **Euler Vectorizado** | µ = 1, user selects | Vectorized NumPy operations. Fast for large N. |
| **Agent-Based** | User selects | Step-by-step Euler integration. More detailed, slower. |
| **Communities** | µ < 1 (auto) | Two communities with intra/inter coupling. Overrides user selection. |

> [!IMPORTANT]
> When µ < 1, the simulator automatically switches to agent-based mode for the community model (Eq. 43), regardless of the user's mode selection.

## Project Structure

```
sklerokardia/
├── app.py                  # Streamlit entry point
├── requirements.txt
├── config/
│   ├── defaults.py         # Default parameter values
│   └── scenarios.py        # Preset simulation scenarios
├── core/
│   ├── model.py            # Equations (1, 2, 7, 8, 25, 27, 28)
│   ├── params.py           # SimulationParams / SimulationResult
│   ├── engine.py           # Main orchestrator
│   └── convergence.py      # Convergence detection
├── simulation/
│   ├── ode_reducer.py      # Vectorized Euler (NumPy)
│   ├── agent_based.py      # Step-by-step Euler
│   └── communities.py      # Two-community model (µ)
├── visualization/
│   ├── polar_plot.py       # Polar scatter (Plotly)
│   ├── temporal_plot.py    # r(t) time series
│   ├── info_panel.py       # Metrics panel
│   └── equations_panel.py  # LaTeX equations display
├── utils/
│   ├── validators.py       # Input validation
│   └── formatters.py       # Display formatting
└── tests/
    ├── test_model.py       # Equation tests
    ├── test_params.py      # Parameter tests
    ├── test_engine.py      # Engine tests
    ├── test_convergence.py # Convergence tests
    └── test_integration.py # Physical behavior tests
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run a specific test
python -m pytest tests/test_engine.py::TestRunSimulation::test_ode_mode -v
```

> [!NOTE]
> Tests verify physical behavior: high K converges to consensus, low K stays polarized, stubborn agents don't move, and ODE vs agent-based modes produce consistent results.

## Citing This Project

If you use Sklerokardia in your research, please cite the underlying paper:

```bibtex
@article{sampson2026socialcompass,
  author    = {Sampson, Corbit R. and Restrepo, Juan G.},
  title     = {Low-dimensional Dynamics of the Social Compass Model},
  journal   = {arXiv preprint arXiv:2606.26378},
  year      = {2026},
  url       = {https://arxiv.org/abs/2606.26378},
  doi       = {10.48550/arXiv.2606.26378}
}
```

You can also click the **Cite this repository** button on the GitHub sidebar for APA and BibTeX formats.

## References

1. **C. R. Sampson & J. G. Restrepo**, "Low-dimensional Dynamics of the Social Compass Model," [arXiv:2606.26378](https://arxiv.org/abs/2606.26378) (2026).

2. **J. Ojer, M. Starnini & R. Pastor-Satorras**, "Modeling Explosive Opinion Depolarization in Interdependent Topics," [*Physical Review Letters* 130, 207401](https://doi.org/10.1103/PhysRevLett.130.207401) (2023).

3. **E. Ott & T. M. Antonsen**, "Low dimensional behavior of large systems of globally coupled oscillators," [*Chaos* 18, 037113](https://doi.org/10.1063/1.2963115) (2008).

4. **Y. Kuramoto**, "Self-entrainment of a population of coupled non-linear oscillators," *International Symposium on Mathematical Problems in Theoretical Physics*, Lecture Notes in Physics vol 39 (1975).
