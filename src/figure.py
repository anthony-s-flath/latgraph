from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from style import LIGHT_STYLE, FigureStyle, resolve_style

# Backwards-compatible alias. New code should pass a style to a figure constructor.
style = LIGHT_STYLE


def new_figure(
    title: str = "Lattice",
    show_axis: bool = True,
    style: FigureStyle = LIGHT_STYLE,
) -> go.Figure:
    fig = go.Figure()
    style_2d(fig, style)
    change_title(fig, title)
    return fig


def equal_axis_range(
    x_range,
    y_range,
):
    """Return one origin-centered range containing both axis ranges."""
    extent = max(
        abs(float(x_range[0])),
        abs(float(x_range[1])),
        abs(float(y_range[0])),
        abs(float(y_range[1])),
    )
    return [-extent, extent]


def set_axes(
    fig: go.Figure,
    x_range=None,
    y_range=None,
    showticklabels: bool = True,
    equal_range: bool = True,
):
    """
    Configure the numerical ranges and keep x and y at the same visual scale.

    If equal_range is True and both ranges are supplied, both axes use one
    common origin-centered range large enough to contain both.
    """
    if equal_range and x_range is not None and y_range is not None:
        axis_range = equal_axis_range(x_range, y_range)
        x_range = axis_range
        y_range = axis_range

    style = resolve_style(fig)
    visibility = style.axis_visibility(showticklabels)
    fig.update_xaxes(range=x_range, **visibility)
    fig.update_yaxes(
        range=y_range,
        **visibility,
    )


def change_title(
    fig: go.Figure,
    title: str = "Lattice",
    style: FigureStyle | None = None,
):
    style = resolve_style(fig, style)
    fig.update_layout(title=style.title(title))


def _point_marker(
    style: FigureStyle,
    role: str,
    marker_size: int | None = None,
):
    return style.point_marker(role, marker_size)


def add_points(
    fig: go.Figure,
    x,
    y,
    name: str = "Points",
    role: str = "default",
    marker_size: int | None = None,
    style: FigureStyle | None = None,
):
    style = resolve_style(fig, style)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name=name,
            marker=_point_marker(style, role, marker_size),
            **style.point_trace(),
        )
    )


def add_point(
    fig: go.Figure,
    x: float,
    y: float,
    name: str = "Point",
    role: str = "default",
    marker_size: int | None = None,
    style: FigureStyle | None = None,
):
    add_points(
        fig,
        [x],
        [y],
        name=name,
        role=role,
        marker_size=marker_size,
        style=style,
    )


def add_arrow(
    fig,
    start,
    end,
    label=None,
    label_t: float | None = None,
    label_offset=None,
    style: FigureStyle | None = None,
):
    style = resolve_style(fig, style)
    label_t = style.arrow_label_t if label_t is None else label_t
    label_offset = style.arrow_label_offset if label_offset is None else label_offset
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)

    fig.add_trace(
        go.Scatter(
            x=[float(start[0]), float(end[0])],
            y=[float(start[1]), float(end[1])],
            mode="lines+markers",
            **style.arrow_trace(),
        )
    )

    if label is not None:
        position = start + label_t * (end - start)
        add_label(
            fig,
            position[0] + label_offset[0],
            position[1] + label_offset[1],
            label,
        )


def add_label(
    fig: go.Figure,
    x: float,
    y: float,
    text: str,
    style: FigureStyle | None = None,
):
    style = resolve_style(fig, style)
    fig.add_annotation(
        x=x,
        y=y,
        text=text,
        **style.label_annotation(),
    )


def add_line(
    fig: go.Figure,
    x,
    y,
    name: str = "Line",
    dashed: bool = False,
    style: FigureStyle | None = None,
):
    style = resolve_style(fig, style)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=name,
            line=style.line(dashed=dashed),
        )
    )


def add_polygon(
    fig: go.Figure,
    x,
    y,
    name: str = "Polygon",
    style: FigureStyle | None = None,
):
    style = resolve_style(fig, style)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=name,
            **style.polygon_trace(),
        )
    )


def style_2d(
    fig: go.Figure,
    style: FigureStyle = LIGHT_STYLE,
):
    style = resolve_style(fig, style)
    fig.update_layout(**style.layout())
    fig.update_xaxes(**style.axis_config())
    fig.update_yaxes(**style.axis_config())
