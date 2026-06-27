"""Panel de información y métricas de la simulación."""

import streamlit as st


def show_info_panel(
    N: int,
    Kc: float,
    K_current: float,
    r_current: float,
    lambda_est: float,
    mode: str,
    converged: bool,
    r1: float | None = None,
    r2: float | None = None,
    n_stubborn: int = 0,
) -> None:
    """Muestra el panel de métricas y estado de la simulación.

    Args:
        N: Número de agentes.
        Kc: Acoplamiento crítico teórico.
        K_current: Acoplamiento actual.
        r_current: Grado de consenso actual.
        lambda_est: Tasa de crecimiento estimada.
        mode: Modo de simulación utilizado.
        converged: Si la simulación convergió.
        r1: Consenso comunidad 1 (opcional).
        r2: Consenso comunidad 2 (opcional).
        n_stubborn: Número de agentes tercos.
    """
    # ── Fila principal: métricas clave ──
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("N Agentes", N)

    with col2:
        st.metric("Kc Teórico", f"{Kc:.3f}")

    with col3:
        if K_current > Kc:
            st.metric("K Actual", f"{K_current:.2f}", delta="> Kc ✓", delta_color="normal")
        else:
            st.metric("K Actual", f"{K_current:.2f}", delta="≤ Kc ✗", delta_color="inverse")

    with col4:
        st.metric("r Actual", f"{r_current:.3f}")

    # ── Fila secundaria: estado y métricas ──
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        if r_current < 0.1:
            st.error("🔴 Polarizado")
        elif r_current < 0.5:
            st.warning("🟡 Transición")
        else:
            st.success("🟢 Consenso")

    with col6:
        lam_color = "normal" if lambda_est > 0 else "inverse"
        lam_arrow = "↑" if lambda_est > 0 else "↓"
        st.metric("Crecimiento λ", f"{lambda_est:+.4f}", delta=f"{lam_arrow} {'crece' if lambda_est > 0 else 'decae'}", delta_color=lam_color)

    with col7:
        st.metric("Tercos", n_stubborn)

    with col8:
        if converged:
            st.success("✅ Convergido")
        else:
            st.warning("⏳ En progreso")

    # ── Fila de comunidades (si aplica) ──
    if r1 is not None and r2 is not None:
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Comunidad 1 (r₁)", f"{r1:.3f}")
        with c2:
            st.metric("Comunidad 2 (r₂)", f"{r2:.3f}")
        with c3:
            if r1 > 0.5 and r2 > 0.5 and r_current < 0.2:
                st.error("⚡ Bipolarización")
            elif r1 > 0.5 and r2 > 0.5 and r_current > 0.5:
                st.success("🤝 Consenso Global")
            else:
                st.info("🔄 Transición inter-comunidad")
