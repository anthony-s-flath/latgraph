from __future__ import annotations

import numpy as np

from figure import LatFigure
from lattice_math import Lattice


def add_origin(
    fig: LatFigure,
    name: str = "Origin",
    marker_size: int | None = None,
):
    fig.add_point(
        0,
        0,
        name=name,
        role="origin",
        marker_size=marker_size,
    )


def add_lattice_points(
    fig: LatFigure,
    lattice: Lattice,
    radius: int = 4,
    name: str = "Lattice",
    role: str = "default",
    marker_size: int | None = None,
):
    pts = lattice.points(radius)

    fig.add_points(
        pts[:, 0],
        pts[:, 1],
        name=name,
        role=role,
        marker_size=marker_size,
    )


def basis_label_offset(
    fig: LatFigure,
    lattice: Lattice,
    vector,
    radius: int,
):
    b = np.asarray(vector, dtype=float)

    x_range = lattice.x_range(radius)
    y_range = lattice.y_range(radius)

    x_span = x_range[1] - x_range[0]
    y_span = y_range[1] - y_range[0]

    x_offset = fig.style.basis_label_padding * x_span * np.sign(b[0])
    y_offset = fig.style.basis_label_padding * y_span * np.sign(b[1])

    return x_offset, y_offset


def add_basis_vectors(
    fig: LatFigure,
    lattice: Lattice,
    radius: int = 4,
    labels=None,
):
    if labels is None:
        labels = [f"b{i + 1}" for i in range(lattice.rank)]

    for i in range(lattice.rank):
        b = lattice.basis[:, i]

        fig.add_arrow(
            start=[0, 0],
            end=b,
        )

        x_offset, y_offset = basis_label_offset(
            fig,
            lattice,
            b,
            radius,
        )

        fig.add_label(
            float(b[0]) + x_offset,
            float(b[1]) + y_offset,
            labels[i],
        )


def add_rank1_span(
    fig: LatFigure,
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

    fig.add_line(
        x=[-extent * u[0], extent * u[0]],
        y=[-extent * u[1], extent * u[1]],
        name=name,
        dashed=True,
    )


def add_fundamental_parallelogram(
    fig: LatFigure,
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

    fig.add_polygon(
        x=vertices[:, 0],
        y=vertices[:, 1],
        name=name,
    )


def plot_lattice(
    lattice: Lattice,
    radius: int = 4,
    title: str = "Lattice",
    showticklabels: bool = True,
    is_light: bool = True,
) -> LatFigure:
    fig = LatFigure(
        title=title,
        is_light=is_light,
    )

    fig.set_axes(
        lattice.x_range(radius),
        lattice.y_range(radius),
        showticklabels,
    )

    add_lattice_points(
        fig,
        lattice,
        radius=radius,
    )

    return fig


def plot_parent_and_sublattice(
    parent: Lattice,
    A,
    radius: int = 5,
    show_span: bool = True,
    title: str = "Parent lattice and sublattice",
    is_light: bool = True,
) -> LatFigure:
    """
    Plot L(B) together with the sublattice L(B A).

    This is especially useful for primitive vs non-primitive examples.
    """
    sub = parent.sublattice(A)

    primitive = parent.is_primitive_sublattice(A)
    subtitle = "primitive" if primitive else "not primitive"

    fig = LatFigure(
        title=f"{title} — {subtitle}",
        is_light=is_light,
    )

    fig.set_axes(
        x_range=[-6, 6],
        y_range=[-6, 6],
    )

    add_lattice_points(
        fig,
        parent,
        radius=radius,
        name="Parent lattice",
        role="secondary",
    )

    add_lattice_points(
        fig,
        sub,
        radius=radius,
        name="Sublattice",
        role="emphasis",
    )

    add_basis_vectors(
        fig,
        sub,
        radius=radius,
        labels=[f"b'_{i + 1}" for i in range(sub.rank)],
    )

    if show_span and sub.rank == 1:
        add_rank1_span(
            fig,
            sub.basis[:, 0],
            name="span(L')",
        )

    return fig


def plot_primal_and_dual(
    lattice: Lattice,
    radius: int = 4,
    title: str = "Primal and dual lattices",
    is_light: bool = True,
) -> LatFigure:
    dual = lattice.dual

    fig = LatFigure(
        title=title,
        is_light=is_light,
    )

    add_lattice_points(
        fig,
        lattice,
        radius=radius,
        name="L",
    )

    add_lattice_points(
        fig,
        dual,
        radius=radius,
        name="L*",
        role="secondary",
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

    return fig

def add_ball(
    self,
    center,
    radius: float,
    role: str = "default",
):
    radius = abs(radius)
    x, y = map(float, center)

    self.fig.add_shape(
        type="circle",
        x0=x - radius,
        x1=x + radius,
        y0=y - radius,
        y1=y + radius,
        **self.style.ball(role),
    )
