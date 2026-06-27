# Skleokardia — Simulador de Dinámica de Opiniones

Simulador interactivo basado en el **Modelo del Compás Social** para explorar la dinámica de opiniones, la polarización y la despolarización en poblaciones con opiniones interdependientes.

Desarrollado con [Streamlit](https://streamlit.io/) y [Plotly](https://plotly.com/python/).

---

## Base Teórica

Este implementa el modelo propuesto por Sampson & Restrepo (2026), que extiende el Modelo del Compás Social original de Ojer, Starnini & Pastor-Satorras (2023).

### Ecuaciones Principales

**Dinámica de un agente (Ecuación 1):**

$$\frac{d\theta_n}{dt} = -\rho_n \sin(\theta_n - \phi_n) + \frac{K}{N} \sum_j \sin(\theta_j - \theta_n)$$

**Parámetro de orden (Ecuación 2):**

$$z = \frac{1}{N} \sum_n e^{i\theta_n}, \quad r = |z|$$

**Acoplamiento crítico (Ecuación 27):**

$$K_c = \frac{2}{\mathbb{E}[\rho^{-1}]}$$

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Nasor2/skleokardia.git
cd skleokardia

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`.

---

## Parámetros del Modelo

| Parámetro | Símbolo | Rango | Descripción |
|-----------|---------|-------|-------------|
| Amarre ideológico | α (ρ base) | 0.1 – 10.0 | Firmeza promedio de creencias. Mayor valor = más resistencia al cambio. |
| Influencia social | K | 0.0 – 5.0 | Fuerza de interacción entre agentes. K > Kc → consenso emerge. |
| Separación comunitaria | µ | 0.0 – 1.0 | 0 = comunidades aisladas, 1 = sin estructura comunitaria. |
| Separación angular | φ₀ | 0 – π/2 | Separa los clusters de opiniones iniciales. |
| Agentes inamovibles | — | 0 – 30% | Porcentaje de agentes con ρ extremadamente alta (tercos). |

---

## Modos de Simulación

| Modo | Descripción |
|------|-------------|
| **Euler Vectorizado** | Operaciones vectorizadas con NumPy. Rápido para N grande. |
| **Agent-Based** | Cada agente se simula por separado. Más detallado, más lento. |
| **Comunidades** | Dos comunidades con acoplamiento intra/inter (µ). Se activa automáticamente cuando µ < 1. |

---

## Estructura del Proyecto

```
skleokardia/
├── app.py                  # Punto de entrada Streamlit
├── requirements.txt        # Dependencias
├── config/
│   ├── defaults.py         # Valores por defecto
│   └── scenarios.py        # Escenarios predefinidos
├── core/
│   ├── model.py            # Ecuaciones del modelo (1, 2, 7, 8, 25, 27, 28)
│   ├── params.py           # SimulationParams / SimulationResult
│   ├── engine.py           # Orquestador principal
│   └── convergence.py      # Detección de convergencia
├── simulation/
│   ├── ode_reducer.py      # Euler vectorizado (NumPy)
│   ├── agent_based.py      # Euler paso a paso
│   └── communities.py      # Modelo de dos comunidades (µ)
├── visualization/
│   ├── polar_plot.py       # Gráfico polar (Plotly)
│   ├── temporal_plot.py    # Evolución temporal r(t)
│   ├── info_panel.py       # Panel de métricas
│   └── equations_panel.py  # Ecuaciones en LaTeX
├── utils/
│   ├── validators.py       # Validación de entrada
│   └── formatters.py       # Formateo de display
└── tests/
    ├── test_model.py       # Tests de ecuaciones
    ├── test_params.py      # Tests de parámetros
    ├── test_engine.py      # Tests del motor
    ├── test_convergence.py # Tests de convergencia
    └── test_integration.py # Tests de comportamiento físico
```

---

## Testing

```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# Ejecutar un test específico
python -m pytest tests/test_engine.py::TestRunSimulation::test_ode_mode -v
```

---

## Referencias

1. **C. R. Sampson & J. G. Restrepo**, "Low-dimensional Dynamics of the Social Compass Model," arXiv:2606.26378 (2026).

2. **J. Ojer, M. Starnini & R. Pastor-Satorras**, "Modeling Explosive Opinion Depolarization in Interdependent Topics," *Physical Review Letters* 130, 207401 (2023).

3. **E. Ott & T. M. Antonsen**, "Low dimensional behavior of large systems of globally coupled oscillators," *Chaos* 18, 037113 (2008).

4. **Y. Kuramoto**, "Self-entrainment of a population of coupled non-linear oscillators," *International Symposium on Mathematical Problems in Theoretical Physics*, Lecture Notes in Physics vol 39 (1975).

---

## Licencia

[MIT](LICENSE)
