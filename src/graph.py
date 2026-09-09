from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from lattice_math import Lattice


@dataclass
class PlotParams:
    label_padding = 0.035
    label_xshift = 5
    label_yshift = 5


params = PlotParams()


def add_origin(
    fig: go.Figure,
    name: str = "Origin",
    marker_size: int = 9,
):
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name=name,
            marker={"size": marker_size},
        )
    )


def change_title(
    fig: go.Figure,
    title: str = "Lattice",
):
    fig.update_layout(title=title)


def add_lattice_points(
    fig: go.Figure,
    lattice: Lattice,
    radius: int = 4,
    name: str = "Lattice",
    marker_size: int = 9,
):
    pts = lattice.points(radius)

    fig.add_trace(
        go.Scatter(
            x=pts[:, 0],
            y=pts[:, 1],
            mode="markers",
            name=name,
            marker={"size": marker_size},
        )
    )


def basis_label_position(
    lattice: Lattice,
    vector,
    radius: int,
):
    b = np.asarray(vector, dtype=float)

    x_range = lattice.x_range(radius)
    y_range = lattice.y_range(radius)

    x_span = x_range[1] - x_range[0]
    y_span = y_range[1] - y_range[0]

    offset = params.label_padding * min(x_span, y_span)

    norm = np.linalg.norm(b)

    if norm == 0:
        return b

    direction = b / norm

    return b + offset * direction


def add_basis_vectors(
    fig: go.Figure,
    lattice: Lattice,
    radius: int = 4,
    labels=None,
):
    if labels is None:
        labels = [f"b{i + 1}" for i in range(lattice.rank)]

    for i in range(lattice.rank):
        b = lattice.basis[:, i]

        # Vector from origin to b_i
        fig.add_annotation(
            x=float(b[0]),
            y=float(b[1]),
            ax=0,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowwidth=2,
            text="",
        )

        # Label a plot-relative distance beyond the vector endpoint
        label_pos = basis_label_position(
            lattice,
            b,
            radius,
        )

        fig.add_annotation(
            x=float(label_pos[0]),
            y=float(label_pos[1]),
            text=labels[i],
            showarrow=False,
            font={"size": 16},
        )


def add_rank1_span(
    fig: go.Figure,
    vector,
    extent: float = 6.0,
    name: str = "span",
):
    """
    Draw the real span of one vector:
        span(v) = {a v : a in R}.
    """
    v = np.asarray(vector, dtype=float).reshape(2)

    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("Span vector must be nonzero.")

    u = v / norm

    fig.add_trace(
        go.Scatter(
            x=[-extent * u[0], extent * u[0]],
            y=[-extent * u[1], extent * u[1]],
            mode="lines",
            name=name,
            line={"dash": "dash"},
        )
    )


def add_fundamental_parallelogram(
    fig: go.Figure,
    lattice: Lattice,
    name: str = "Fundamental parallelogram",
):
    if lattice.rank != 2:
        raise ValueError("Need two basis vectors.")

    b1 = lattice.basis[:, 0]
    b2 = lattice.basis[:, 1]

    vertices = np.array(
        [
            [0.0, 0.0],
            b1,
            b1 + b2,
            b2,
            [0.0, 0.0],
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=vertices[:, 0],
            y=vertices[:, 1],
            mode="lines",
            fill="toself",
            opacity=0.20,
            name=name,
        )
    )


def finish_2d(
    fig: go.Figure,
    title: str,
    x_range=None,
    y_range=None,
):
    fig.update_layout(
        title={
            "text": title,
            "font": {
                "family": 'Georgia, "Times New Roman", serif',
                "size": 22,
                "color": "#1f2328",
            },
        },
        template="plotly_white",
        hovermode="closest",
        legend={
            "orientation": "h",
            "font": {
                "family": 'Georgia, "Times New Roman", serif',
                "size": 13,
                "color": "#666",
            },
        },
        margin={"l": 40, "r": 40, "t": 70, "b": 40},
        font={
            "family": 'Georgia, "Times New Roman", serif',
            "color": "#1f2328",
        },
    )

    fig.update_xaxes(
        zeroline=True,
        zerolinecolor="#999",
        showgrid=True,
        gridcolor="#e8e8e8",
        tickfont={"color": "#666"},
        range=x_range,
    )

    fig.update_yaxes(
        zeroline=True,
        zerolinecolor="#999",
        showgrid=True,
        gridcolor="#e8e8e8",
        tickfont={"color": "#666"},
        range=y_range,
    )

    return fig


def plot_lattice(
    lattice: Lattice,
    radius: int = 4,
    title: str = "Lattice",
):
    fig = go.Figure()

    add_lattice_points(fig, lattice, radius=radius)

    return finish_2d(
        fig,
        title,
        lattice.y_range(radius),
        lattice.x_range(radius),
    )


def plot_parent_and_sublattice(
    parent: Lattice,
    A,
    radius: int = 5,
    show_span: bool = True,
    title: str = "Parent lattice and sublattice",
):
    """
    Plot L(B) together with the sublattice L(B A).

    This is especially useful for primitive vs non-primitive examples.
    """
    sub = parent.sublattice(A)

    fig = go.Figure()

    add_lattice_points(
        fig,
        parent,
        radius=radius,
        name="Parent lattice",
        marker_size=8,
    )

    add_lattice_points(
        fig,
        sub,
        radius=radius,
        name="Sublattice",
        marker_size=13,
    )

    add_basis_vectors(
        fig,
        sub,
        radius=radius,
        labels=[f"b'_{i+1}" for i in range(sub.rank)],
    )

    if show_span and sub.rank == 1:
        add_rank1_span(fig, sub.basis[:, 0], name="span(L')")

    primitive = parent.is_primitive_sublattice(A)

    subtitle = "primitive" if primitive else "not primitive"

    return finish_2d(
        fig,
        f"{title} — {subtitle}",
        x_range=[-6, 6],
        y_range=[-6, 6],
    )


def plot_primal_and_dual(
    lattice: Lattice,
    radius: int = 4,
    title: str = "Primal and dual lattices",
):
    dual = lattice.dual

    fig = go.Figure()

    add_lattice_points(
        fig,
        lattice,
        radius=radius,
        name="L",
        marker_size=9,
    )

    add_lattice_points(
        fig,
        dual,
        radius=radius,
        name="L*",
        marker_size=7,
    )

    add_basis_vectors(
        fig,
        lattice,
        radius=radius,
        labels=["b1", "b2"],
    )

    add_basis_vectors(
        fig,
        dual,
        radius=radius,
        labels=["b1*", "b2*"],
    )

    return finish_2d(fig, title)
