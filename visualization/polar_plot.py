"""Gráfico polar de distribución de opiniones."""

import numpy as np
import plotly.graph_objects as go

CONVICTION_COLORS = [
    [0.0, "#3B82F6"],
    [0.25, "#60A5FA"],
    [0.5, "#FCD34D"],
    [0.75, "#F59E0B"],
    [1.0, "#EF4444"],
]


def create_polar_histogram(
    theta: np.ndarray,
    rho: np.ndarray,
    stubborn_mask: np.ndarray,
    z_current: complex | None = None,
    phi_initial: np.ndarray | None = None,
    z1: complex | None = None,
    z2: complex | None = None,
    height: int = 400,
    n_bins: int = 24,
) -> go.Figure:
    """Histograma polar (rose diagram) — muestra densidad de opiniones.

    Cada barra = cuántos agentes hay en esa dirección.
    Color de barra = convicción promedio del sector.

    Args:
        theta: Orientaciones de los agentes (radianes).
        rho: Convicciones de los agentes.
        stubborn_mask: Máscara booleana de agentes tercos.
        z_current: Parámetro de orden actual.
        phi_initial: Orientaciones iniciales φ.
        z1: Parámetro de orden comunidad 1.
        z2: Parámetro de orden comunidad 2.
        height: Altura del gráfico en píxeles.
        n_bins: Número de sectores angulares.

    Returns:
        Figura Plotly con el histograma polar.
    """
    fig = go.Figure()

    bin_edges = np.linspace(0, 2 * np.pi, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width_deg = 360 / n_bins * 0.85

    # Contar agentes por bin
    counts = np.zeros(n_bins)
    rho_means = np.zeros(n_bins)
    for i in range(n_bins):
        if i < n_bins - 1:
            mask = (theta >= bin_edges[i]) & (theta < bin_edges[i + 1])
        else:
            mask = (theta >= bin_edges[i]) | (theta < bin_edges[0])
        counts[i] = np.sum(mask)
        if np.any(mask):
            rho_means[i] = np.mean(rho[mask])

    max_count = np.max(counts) if np.max(counts) > 0 else 1
    bar_radii = counts / max_count

    # Normalizar rho para colores
    rho_min, rho_max = np.min(rho), np.max(rho)
    if rho_max > rho_min:
        rho_norm = (rho_means - rho_min) / (rho_max - rho_min)
    else:
        rho_norm = np.ones(n_bins) * 0.5

    # Barras del histograma
    fig.add_trace(go.Barpolar(
        r=bar_radii,
        theta=np.degrees(bin_centers),
        width=bin_width_deg,
        marker=dict(
            color=rho_norm,
            colorscale=CONVICTION_COLORS,
            opacity=0.8,
            line=dict(width=1, color='rgba(255,255,255,0.15)'),
        ),
        hovertemplate=(
            'Sector: %{theta:.0f}°<br>'
            'Agentes: %{r:.0f}<br>'
            'ρ promedio: %{marker.color:.2f}<extra></extra>'
        ),
        name='Densidad',
    ))

    # Histograma inicial (fondo tenue)
    if phi_initial is not None:
        counts_init = np.zeros(n_bins)
        for i in range(n_bins):
            if i < n_bins - 1:
                mask = (phi_initial >= bin_edges[i]) & (phi_initial < bin_edges[i + 1])
            else:
                mask = (phi_initial >= bin_edges[i]) | (phi_initial < bin_edges[0])
            counts_init[i] = np.sum(mask)
        max_init = np.max(counts_init) if np.max(counts_init) > 0 else 1
        fig.add_trace(go.Barpolar(
            r=counts_init / max_init,
            theta=np.degrees(bin_centers),
            width=bin_width_deg,
            marker=dict(color='rgba(156,163,175,0.12)', line=dict(width=0.5, color='rgba(156,163,175,0.2)')),
            name='Inicial (φ)',
            hovertemplate='Inicial: %{theta:.0f}°<extra></extra>',
        ))

    # Flecha de consenso global
    if z_current is not None and np.abs(z_current) > 0.01:
        z_angle = np.degrees(np.angle(z_current))
        z_mag = np.abs(z_current)
        fig.add_trace(go.Scatterpolar(
            r=[0, z_mag * 1.1],
            theta=[0, z_angle],
            mode='lines+markers',
            name=f'Consenso z (r={z_mag:.2f})',
            line=dict(color='#10B981', width=4),
            marker=dict(size=[0, 16], symbol=['circle', 'arrow-up'], color='#10B981'),
        ))

    # Flechas de comunidad
    if z1 is not None and z2 is not None:
        z1_mag, z2_mag = abs(z1), abs(z2)
        if z1_mag > 0.01:
            fig.add_trace(go.Scatterpolar(
                r=[0, z1_mag * 1.1], theta=[0, np.degrees(np.angle(z1))],
                mode='lines+markers', name=f'Com. 1 (r₁={z1_mag:.2f})',
                line=dict(color='#3B82F6', width=2.5, dash='dash'),
                marker=dict(size=[0, 12], symbol=['circle', 'arrow-up']),
            ))
        if z2_mag > 0.01:
            fig.add_trace(go.Scatterpolar(
                r=[0, z2_mag * 1.1], theta=[0, np.degrees(np.angle(z2))],
                mode='lines+markers', name=f'Com. 2 (r₂={z2_mag:.2f})',
                line=dict(color='#F97316', width=2.5, dash='dash'),
                marker=dict(size=[0, 12], symbol=['circle', 'arrow-up']),
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, gridcolor='rgba(55,65,81,0.3)', tickfont=dict(size=8, color='#9CA3AF')),
            angularaxis=dict(direction="clockwise", rotation=90, tickvals=[0, 90, 180, 270],
                             ticktext=['0°', '90°', '180°', '270°'], gridcolor='rgba(55,65,81,0.4)'),
            bgcolor='rgba(0,0,0,0)',
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_polar_scatter(
    theta: np.ndarray,
    rho: np.ndarray,
    stubborn_mask: np.ndarray,
    z_current: complex | None = None,
    phi_initial: np.ndarray | None = None,
    z1: complex | None = None,
    z2: complex | None = None,
    height: int = 400,
) -> go.Figure:
    """Scatter polar mejorado — cada agente en el círculo unitario.

    Args:
        theta: Orientaciones de los agentes (radianes).
        rho: Convicciones de los agentes.
        stubborn_mask: Máscara booleana de agentes tercos.
        z_current: Parámetro de orden actual.
        phi_initial: Orientaciones iniciales φ.
        z1: Parámetro de orden comunidad 1.
        z2: Parámetro de orden comunidad 2.
        height: Altura del gráfico en píxeles.

    Returns:
        Figura Plotly con el gráfico polar.
    """
    theta_deg = np.degrees(theta)
    rho_min, rho_max = np.min(rho), np.max(rho)
    if rho_max > rho_min:
        rho_norm = (rho - rho_min) / (rho_max - rho_min)
    else:
        rho_norm = np.ones_like(rho) * 0.5

    fig = go.Figure()

    # Círculo de referencia
    ref_theta = np.linspace(0, 360, 100)
    fig.add_trace(go.Scatterpolar(
        r=np.ones(100), theta=ref_theta, mode='lines',
        line=dict(color='rgba(55,65,81,0.3)', width=1, dash='dot'),
        showlegend=False, hoverinfo='skip',
    ))

    # Posiciones iniciales
    if phi_initial is not None:
        fig.add_trace(go.Scatterpolar(
            r=np.ones_like(phi_initial) * 0.92, theta=np.degrees(phi_initial),
            mode='markers', name='Inicial (φ)',
            marker=dict(size=5, color='rgba(156,163,175,0.3)', symbol='circle-open',
                        line=dict(width=1.5, color='rgba(156,163,175,0.4)')),
            hovertemplate='φ₀: %{theta:.1f}°<extra>Inicial</extra>',
        ))

    # Agentes normales
    normal_mask = ~stubborn_mask
    if np.any(normal_mask):
        fig.add_trace(go.Scatterpolar(
            r=np.ones(np.sum(normal_mask)), theta=theta_deg[normal_mask],
            mode='markers', name='Agentes',
            marker=dict(size=7, color=rho_norm[normal_mask], colorscale=CONVICTION_COLORS,
                        opacity=0.6, line=dict(width=0.5, color='rgba(255,255,255,0.15)'),
                        colorbar=dict(title="ρ", tickvals=[0, 0.5, 1],
                                      ticktext=[f"{rho_min:.1f}", f"{(rho_min+rho_max)/2:.1f}", f"{rho_max:.1f}"],
                                      len=0.5, y=0.5)),
            hovertemplate='θ: %{theta:.1f}°<br>ρ: %{marker.color:.2f}<extra></extra>',
        ))

    # Agentes tercos
    if np.any(stubborn_mask):
        fig.add_trace(go.Scatterpolar(
            r=np.ones(np.sum(stubborn_mask)), theta=theta_deg[stubborn_mask],
            mode='markers', name='Terco (ρ=∞)',
            marker=dict(size=11, color='#EF4444', symbol='diamond', opacity=0.9,
                        line=dict(width=1.5, color='white')),
            hovertemplate='TERCO<br>θ: %{theta:.1f}°<br>ρ: ∞<extra></extra>',
        ))

    # Flecha de consenso
    if z_current is not None and np.abs(z_current) > 0.01:
        z_angle = np.degrees(np.angle(z_current))
        z_mag = np.abs(z_current)
        fig.add_trace(go.Scatterpolar(
            r=[0, z_mag], theta=[0, z_angle], mode='lines+markers',
            name=f'Consenso z (r={z_mag:.2f})',
            line=dict(color='#10B981', width=4),
            marker=dict(size=[0, 18], symbol=['circle', 'arrow-up'], color='#10B981'),
        ))

    # Flechas de comunidad
    if z1 is not None and z2 is not None:
        z1_mag, z2_mag = abs(z1), abs(z2)
        if z1_mag > 0.01:
            fig.add_trace(go.Scatterpolar(
                r=[0, z1_mag], theta=[0, np.degrees(np.angle(z1))],
                mode='lines+markers', name=f'Com. 1 (r₁={z1_mag:.2f})',
                line=dict(color='#3B82F6', width=2.5, dash='dash'),
                marker=dict(size=[0, 12], symbol=['circle', 'arrow-up']),
            ))
        if z2_mag > 0.01:
            fig.add_trace(go.Scatterpolar(
                r=[0, z2_mag], theta=[0, np.degrees(np.angle(z2))],
                mode='lines+markers', name=f'Com. 2 (r₂={z2_mag:.2f})',
                line=dict(color='#F97316', width=2.5, dash='dash'),
                marker=dict(size=[0, 12], symbol=['circle', 'arrow-up']),
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1.15], gridcolor='rgba(55,65,81,0.3)',
                            tickfont=dict(size=8, color='#9CA3AF')),
            angularaxis=dict(direction="clockwise", rotation=90, tickvals=[0, 90, 180, 270],
                             ticktext=['0°', '90°', '180°', '270°'], gridcolor='rgba(55,65,81,0.4)'),
            bgcolor='rgba(0,0,0,0)',
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig
