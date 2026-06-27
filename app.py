import time

import numpy as np
import streamlit as st

from config.scenarios import SCENARIOS
from core.engine import run_simulation
from core.params import SimulationParams
from visualization.info_panel import show_info_panel
from visualization.polar_plot import create_polar_histogram, create_polar_scatter
from visualization.temporal_plot import create_temporal_plot
from visualization.equations_panel import show_equations_panel

st.set_page_config(
    page_title="Sklerokardia",
    page_icon="🧭",
    layout="wide",
)

# ── Header ──────────────────────────────────────────────────────────
st.title("🧭 Sklerokardia")
st.caption("Simulador de Dinámica de Opiniones — Modelo del Compás Social · Sampson & Restrepo (2026)")

# ── Session state ───────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "scenario_name" not in st.session_state:
    st.session_state.scenario_name = "Personalizado"


def on_scenario_change():
    st.session_state.scenario_name = st.session_state.scenario_selector


# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Parámetros")

    # Escenario
    scenario_name = st.selectbox(
        "Escenario predefinido",
        list(SCENARIOS.keys()),
        key="scenario_selector",
        on_change=on_scenario_change,
    )
    scenario = SCENARIOS[scenario_name]
    if scenario.get("description"):
        st.info(scenario["description"])

    st.divider()

    # ── Convicción ──
    with st.expander("🎯 Convicción", expanded=True):
        alpha = st.slider(
            "α — Amarre ideológico (ρ base)",
            min_value=0.1, max_value=10.0,
            value=scenario["alpha"], step=0.1,
            help="Firmeza promedio de creencias. Equivale a la convicción ρ de cada agente. Mayor valor = más resistencia al cambio.",
        )
        st.caption(f"ρ promedio de la población: **{alpha:.1f}**")

    # ── Interacción Social ──
    with st.expander("🔗 Interacción Social", expanded=True):
        K = st.slider(
            "K — Influencia social / algoritmo",
            min_value=0.0, max_value=5.0,
            value=scenario["K"], step=0.1,
            help="Fuerza de interacción entre agentes. Cuando K > Kc, emerge consenso global. Representa la presión social o la fuerza de algoritmos de recomendación.",
        )

    # ── Distribución Inicial ──
    with st.expander("📐 Distribución Inicial", expanded=False):
        phi0 = st.slider(
            "φ₀ — Separación angular",
            min_value=0.0, max_value=1.5708,
            value=scenario.get("phi0", 0.5236), step=0.05, format="%.2f",
            help="Separa los clusters de opiniones. φ₀=0: correlacionadas (bimodal). φ₀=π/4: no correlacionadas (cuadrimodal).",
        )

    # ── Población ──
    with st.expander("👥 Población", expanded=False):
        stubborn_pct = st.slider(
            "% Agentes inamovibles",
            min_value=0, max_value=30,
            value=scenario["stubborn_pct"], step=1,
            help="Porcentaje de agentes con ρ extremadamente alta (1000). Practicamente no cambian de opinión.",
        )
        N = st.slider(
            "N — Agentes totales",
            min_value=100, max_value=2000,
            value=1000, step=100,
            help="Tamaño de la población simulada.",
        )

    # ── Estructura Social ──
    with st.expander("🏘️ Estructura Social", expanded=False):
        mu = st.slider(
            "µ — Separación comunitaria",
            min_value=0.0, max_value=1.0,
            value=scenario["mu"], step=0.05,
            help="0 = comunidades completamente aisladas (imposible consenso global). 1 = sin estructura de comunidad (comportamiento base del modelo).",
        )

    # ── Simulación ──
    with st.expander("⚡ Simulación", expanded=False):
        T = st.slider(
            "T — Tiempo de simulación",
            min_value=10.0, max_value=200.0,
            value=50.0, step=10.0,
        )
        dt = st.slider(
            "dt — Paso temporal",
            min_value=0.01, max_value=0.1,
            value=0.05, step=0.01, format="%.2f",
        )
        if mu < 1.0:
            st.info("Con µ < 1 se usa automáticamente el modo comunidades (agent-based).")
            mode = "Agent-Based (detallado)"
        else:
            mode = st.radio(
                "Motor",
                ["Euler Vectorizado (rápido)", "Agent-Based (detallado)"],
                help="Vectorizado: operaaciones vectorizadas con NumPy. Agent-Based: cada agente por separado.",
            )

    # ── Visualización ──
    with st.expander("📊 Visualización", expanded=False):
        polar_view = st.radio(
            "Vista polar",
            ["Histograma (densidad)", "Scatter (agentes)"],
        )
        chart_height = st.slider(
            "Altura de gráficos",
            min_value=300, max_value=600,
            value=400, step=50,
        )

    st.divider()

    # ── Botones ──
    col1, col2 = st.columns(2)
    with col1:
        run = st.button("▶ Ejecutar", type="primary", use_container_width=True)
    with col2:
        reset = st.button("↻ Reset", use_container_width=True)

# ── Ejecución ───────────────────────────────────────────────────────
if run:
    mode_str = "ode" if "Vectorizado" in mode or "ODE" in mode else "agent_based"

    params = SimulationParams(
        alpha=alpha,
        K=K,
        stubborn_pct=float(stubborn_pct),
        mu=mu,
        phi0=phi0,
        N=N,
        T=T,
        dt=dt,
        mode=mode_str,
        scenario=scenario_name,
    )

    progress = st.progress(0, text="Iniciando...")
    try:
        progress.progress(20, text="Validando parámetros...")
        progress.progress(40, text="Ejecutando simulación...")
        result = run_simulation(params)
        progress.progress(80, text="Generando visualizaciones...")
        st.session_state.results = result
        progress.progress(100, text="¡Completado!")
        time.sleep(0.3)
        progress.empty()
    except Exception as e:
        progress.empty()
        st.error(f"Error en la simulación: {e}")

if reset:
    st.session_state.results = None
    st.rerun()

# ── Resultados ──────────────────────────────────────────────────────
if st.session_state.results is not None:
    r = st.session_state.results

    # Métricas principales
    show_info_panel(
        N=len(r.rho_values),
        Kc=r.Kc,
        K_current=K,
        r_current=r.r_current,
        lambda_est=r.lambda_est,
        mode=r.mode_used,
        converged=r.converged,
        r1=float(abs(r.z1_history[-1])) if hasattr(r, 'z1_history') and r.z1_history is not None and len(r.z1_history) > 0 else None,
        r2=float(abs(r.z2_history[-1])) if hasattr(r, 'z2_history') and r.z2_history is not None and len(r.z2_history) > 0 else None,
        n_stubborn=int(np.sum(r.stubborn_mask)),
    )

    st.divider()

    # Gráficos
    col_polar, col_temporal = st.columns([3, 2])

    with col_polar:
        st.subheader("Distribución de Opiniones")
        z1_val = r.z1_history[-1] if hasattr(r, 'z1_history') and r.z1_history is not None and len(r.z1_history) > 0 else None
        z2_val = r.z2_history[-1] if hasattr(r, 'z2_history') and r.z2_history is not None and len(r.z2_history) > 0 else None

        polar_args = dict(
            theta=r.theta_final, rho=r.rho_values, stubborn_mask=r.stubborn_mask,
            z_current=r.z_history[-1] if len(r.z_history) > 0 else None,
            phi_initial=r.phi_values, z1=z1_val, z2=z2_val, height=chart_height,
        )

        if "Histograma" in polar_view:
            fig_polar = create_polar_histogram(**polar_args)
        else:
            fig_polar = create_polar_scatter(**polar_args)

        st.plotly_chart(fig_polar, use_container_width=True)

    with col_temporal:
        st.subheader("Evolución Temporal r(t)")
        fig_temporal = create_temporal_plot(
            r_history=r.r_history,
            t_history=r.t_history,
            Kc=r.Kc,
            K_current=K,
            height=chart_height,
        )
        st.plotly_chart(fig_temporal, use_container_width=True)

    st.divider()

    # Panel de ecuaciones
    show_equations_panel(mu=mu)

else:
    # Estado vacío
    st.info("👈 Configura los parámetros y presiona **▶ Ejecutar** para iniciar la simulación.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("N Agentes", "1000")
    with col2:
        st.metric("Kc Teórico", "—")
    with col3:
        st.metric("K Actual", "—")
    with col4:
        st.metric("r Actual", "—")
