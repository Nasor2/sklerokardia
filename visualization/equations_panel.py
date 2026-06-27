"""Panel expandible con las ecuaciones del modelo."""

import streamlit as st


def show_equations_panel(mu: float = 1.0) -> None:
    """Muestra las ecuaciones fundamentales del Modelo del Compás Social.

    Args:
        mu: Separación comunitaria actual. Si mu < 1, muestra ecuaciones de comunidades.
    """
    with st.expander("📐 Ecuaciones del Modelo", expanded=False):
        # Ecuación 1 — Siempre relevante
        st.markdown("**Ecuación 1 — Dinámica de un agente:**")
        st.latex(r"\frac{d\theta_n}{dt} = -\rho_n \sin(\theta_n - \phi_n) + \frac{K}{N} \sum_j \sin(\theta_j - \theta_n)")
        st.caption("Primer término: anclaje a opinión original. Segundo término: búsqueda de consenso social (tipo Kuramoto).")

        st.divider()

        # Ecuación 2 — Siempre relevante
        st.markdown("**Ecuación 2 — Parámetro de orden:**")
        st.latex(r"z = \frac{1}{N} \sum_n e^{i\theta_n}, \quad r = |z|")
        st.caption("r = 0 → polarización completa. r = 1 → consenso total.")

        st.divider()

        if mu < 1.0:
            # Ecuación 43 — Comunidades
            st.markdown("**Ecuación 43 — Modelo con comunidades:**")
            st.latex(
                r"\frac{d\theta_n^\sigma}{dt} = -\rho_n^\sigma \sin(\theta_n^\sigma - \phi_n^\sigma)"
                r" + \frac{K}{N/2} \sum_{j \in \sigma} \sin(\theta_j^\sigma - \theta_n^\sigma)"
                r" + \frac{\mu K}{N/2} \sum_{j \in \sigma'} \sin(\theta_j^{\sigma'} - \theta_n^\sigma)"
            )
            st.caption("K intra-comunidad = K. K inter-comunidad = μK. μ=0: aisladas. μ=1: sin estructura.")

            st.divider()

            # Ecuación 67 — Kc con comunidades
            st.markdown("**Ecuación 67 — Kc con comunidades:**")
            st.latex(r"K_c = \frac{2(1 + \mu R)}{\mathbb{E}[\rho^{-1}](1 + \mu)}")
            st.caption("A menor μ, mayor Kc necesario para alcanzar consenso.")
        else:
            # Ecuación 25 — Dispersión
            st.markdown("**Ecuación 25 — Relación de dispersión:**")
            st.latex(r"\lambda = K(1 + |\mathbb{E}[e^{-2i\phi}]|) - 1")
            st.caption("λ < 0: polarización estable. λ > 0: consenso emerge. λ = 0: punto crítico.")

            st.divider()

            # Ecuación 27 — Kc
            st.markdown("**Ecuación 27 — Acoplamiento crítico:**")
            st.latex(r"K_c = \frac{2}{\mathbb{E}[\rho^{-1}]}")
            st.caption("Si K > Kc, la polarización es inestable y emerge consenso. Kc depende solo de E[ρ⁻¹].")

            st.divider()

            # Ecuación 28 — Tasa cercana a Kc
            st.markdown("**Ecuación 28 — Tasa de despolarización (cerca de Kc):**")
            st.latex(r"\lambda \approx (K - K_c) \cdot \frac{\mathbb{E}[\rho^{-2}]}{\mathbb{E}[\rho^{-1}]}")
            st.caption("La velocidad de despolarización depende de E[ρ⁻²]. Poblaciones con el mismo Kc pueden despolarizar a velocidades muy diferentes.")
