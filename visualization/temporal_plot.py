"""Gráfico temporal de evolución de r(t)."""

import numpy as np
import plotly.graph_objects as go


def create_temporal_plot(
    r_history: np.ndarray,
    t_history: np.ndarray,
    Kc: float,
    K_current: float,
    height: int = 300,
) -> go.Figure:
    """Gráfico temporal de r(t) con fill, anotaciones y dr/dt.

    - Línea azul: r(t) con fill degradado
    - Línea naranja punteada: dr/dt (velocidad de cambio)
    - Línea vertical roja punteada: Kc teórico
    - Marcador de fase que cambia de color

    Args:
        r_history: Historial del grado de consenso r(t).
        t_history: Historial de tiempo.
        Kc: Acoplamiento crítico teórico.
        K_current: Acoplamiento actual.
        height: Altura del gráfico en píxeles.

    Returns:
        Figura Plotly con el gráfico temporal.
    """
    fig = go.Figure()

    # Calcular dr/dt (derivada discreta)
    if len(t_history) > 1:
        dt_vals = np.diff(t_history)
        dr = np.diff(r_history)
        dr_dt = dr / dt_vals
        t_dr = t_history[1:]
    else:
        dr_dt = np.array([])
        t_dr = np.array([])

    # ── Regiones de referencia ──
    fig.add_hrect(y0=0, y1=0.1, fillcolor="rgba(239,68,68,0.05)", line_width=0,
                  annotation_text="Polarizado", annotation_position="top left",
                  annotation_font_size=9, annotation_font_color="#9CA3AF")
    fig.add_hrect(y0=0.5, y1=1.0, fillcolor="rgba(16,185,129,0.05)", line_width=0,
                  annotation_text="Consenso", annotation_position="bottom left",
                  annotation_font_size=9, annotation_font_color="#9CA3AF")

    # Líneas horizontales de referencia
    fig.add_hline(y=0.1, line_dash="dot", line_color="rgba(239,68,68,0.3)", line_width=1)
    fig.add_hline(y=0.5, line_dash="dot", line_color="rgba(16,185,129,0.3)", line_width=1)

    # ── Línea vertical de Kc ──
    t_max = max(t_history) if len(t_history) > 0 else 50
    if 0 < Kc < t_max:
        fig.add_vline(
            x=Kc, line_dash="dash", line_color="rgba(239,68,68,0.5)", line_width=1.5,
        )
        fig.add_annotation(
            x=Kc, y=1.02, yref="paper",
            text=f"Kc={Kc:.2f}", showarrow=False,
            font=dict(size=9, color="#EF4444"),
        )

    # ── Línea principal r(t) ──
    fig.add_trace(go.Scatter(
        x=t_history, y=r_history, mode='lines', name='r(t)',
        line=dict(color='#3B82F6', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(59,130,246,0.08)',
        hovertemplate='t: %{x:.1f}<br>r: %{y:.4f}<extra></extra>',
    ))

    # ── dr/dt como segunda línea ──
    if len(dr_dt) > 0:
        fig.add_trace(go.Scatter(
            x=t_dr, y=dr_dt, mode='lines', name='dr/dt',
            line=dict(color='#F97316', width=1.2, dash='dot'),
            yaxis='y2',
            hovertemplate='t: %{x:.1f}<br>dr/dt: %{y:.4f}<extra></extra>',
            opacity=0.7,
        ))

    # ── Marcador inicial ──
    if len(t_history) > 0:
        fig.add_trace(go.Scatter(
            x=[t_history[0]], y=[r_history[0]], mode='markers+text',
            name='Inicio', marker=dict(color='#9CA3AF', size=8, symbol='circle'),
            text=[f'r₀={r_history[0]:.3f}'], textposition='top center',
            textfont=dict(size=9, color='#9CA3AF'),
            hovertemplate='t₀=%{x:.1f}<br>r₀=%{y:.4f}<extra>Inicio</extra>',
        ))

    # ── Marcador final con color por fase ──
    if len(t_history) > 1:
        r_final = r_history[-1]
        if r_final < 0.1:
            mcolor, phase = '#EF4444', 'Polarizado'
        elif r_final < 0.5:
            mcolor, phase = '#F59E0B', 'Transición'
        else:
            mcolor, phase = '#10B981', 'Consenso'
        fig.add_trace(go.Scatter(
            x=[t_history[-1]], y=[r_final], mode='markers+text',
            name='Final', marker=dict(color=mcolor, size=10, symbol='diamond'),
            text=[f'r={r_final:.3f} ({phase})'], textposition='top center',
            textfont=dict(size=9, color=mcolor),
            hovertemplate='t=%{x:.1f}<br>r=%{y:.4f}<extra>Final</extra>',
        ))

    # ── Anotaciones en cruces de fase ──
    if len(t_history) > 1:
        for threshold, label, color in [(0.1, 'r=0.1', '#EF4444'), (0.5, 'r=0.5', '#10B981')]:
            crossings = np.where(np.diff(np.sign(r_history - threshold)))[0]
            for idx in crossings[:2]:
                fig.add_annotation(
                    x=t_history[idx], y=threshold,
                    text=f'↕ {label}', showarrow=True,
                    arrowhead=2, arrowsize=0.7, arrowcolor=color,
                    font=dict(size=8, color=color),
                    bgcolor='rgba(14,17,23,0.7)',
                )

    # ── Anotación K vs Kc ──
    relation = "K > Kc" if K_current > Kc else "K ≤ Kc"
    rcolor = "#10B981" if K_current > Kc else "#EF4444"
    fig.add_annotation(
        x=0.98, y=0.98, xref="paper", yref="paper",
        text=f"<b>K={K_current:.2f}</b> vs <b>Kc={Kc:.2f}</b> → {relation}",
        showarrow=False, font=dict(size=11, color=rcolor),
        bgcolor="rgba(14,17,23,0.8)", bordercolor=rcolor,
        borderwidth=1, borderpad=4, align="right",
    )

    # ── Layout ──
    fig.update_layout(
        xaxis_title="Tiempo",
        yaxis=dict(title=dict(text="r (Grado de consenso)", font=dict(color='#3B82F6')),
                   range=[0, 1.05], dtick=0.25, tickfont=dict(color='#3B82F6')),
        yaxis2=dict(title=dict(text="dr/dt", font=dict(color='#F97316')), overlaying='y', side='right',
                    showgrid=False, tickfont=dict(color='#F97316')),
        margin=dict(l=40, r=60, t=30, b=40),
        height=height,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig
