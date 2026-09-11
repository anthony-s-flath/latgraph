from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go


@dataclass(frozen=True)
class FigureStyle:
    font_family: str = 'Georgia, "Times New Roman", serif'

    foreground: str = "#1f2328"
    muted: str = "#666"
    axis: str = "#777"
    grid: str = "#eeeeee"

    width: int = 780
    height: int = 780

    title_size: int = 28
    text_size: int = 28
    tick_size: int = 18
    legend_size: int = 24 
    label_size: int = 22 

    point_size: int = 10
    emphasis_point_size: int = 14
    secondary_point_size: int = 8
    origin_point_size: int = 10
    origin_border_width: float = 2

    arrow_width: float = 1.6
    arrow_size: float = 1.3

    line_width: float = 1.2

    polygon_line_width: float = 1
    polygon_fill: str = "rgba(31, 35, 40, 0.06)"


style = FigureStyle()


def new_figure(title: str = "Lattice", show_axis: bool = True) -> go.Figure:
    fig = go.Figure()
    style_2d(fig)
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

    ticks = "outside" if showticklabels else ""
    fig.update_xaxes(range=x_range, showticklabels=showticklabels, ticks=ticks)
    fig.update_yaxes(
        range=y_range,
        showticklabels=showticklabels,
        ticks=ticks,
    )


def change_title(
    fig: go.Figure,
    title: str = "Lattice",
):
    fig.update_layout(
        title={
            "text": title,
            "x": 0,
            "xanchor": "left",
            "font": {
                "family": style.font_family,
                "size": style.title_size,
                "color": style.foreground,
            },
        }
    )


def _point_marker(
    role: str,
    marker_size: int | None = None,
):
    if role == "default":
        return {
            "size": marker_size or style.point_size,
            "color": style.foreground,
        }

    if role == "emphasis":
        return {
            "size": marker_size or style.emphasis_point_size,
            "color": style.foreground,
        }

    if role == "secondary":
        return {
            "size": marker_size or style.secondary_point_size,
            "color": style.muted,
        }

    if role == "origin":
        return {
            "size": marker_size or style.origin_point_size,
            "color": "white",
            "line": {
                "color": style.foreground,
                "width": style.origin_border_width,
            },
        }

    raise ValueError(f"Unknown point role: {role}")


def add_points(
    fig: go.Figure,
    x,
    y,
    name: str = "Points",
    role: str = "default",
    marker_size: int | None = None,
):
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name=name,
            marker=_point_marker(role, marker_size),
            zorder=1,
        )
    )


def add_point(
    fig: go.Figure,
    x: float,
    y: float,
    name: str = "Point",
    role: str = "default",
    marker_size: int | None = None,
):
    add_points(
        fig,
        [x],
        [y],
        name=name,
        role=role,
        marker_size=marker_size,
    )


def add_arrow(
    fig,
    start,
    end,
    label=None,
    label_t=0.5,
    label_offset=(0.0, 0.0),
):
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)

    fig.add_trace(
        go.Scatter(
            x=[float(start[0]), float(end[0])],
            y=[float(start[1]), float(end[1])],
            mode="lines+markers",
            line={
                "color": style.foreground,
                "width": style.arrow_width,
            },
            marker={
                "symbol": ["circle", "arrow"],
                "size": [0, 10],
                "color": style.foreground,
                "angleref": "previous",
            },
            showlegend=False,
            hoverinfo="skip",
            zorder=-1,
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
):
    fig.add_annotation(
        x=x,
        y=y,
        text=text,
        showarrow=False,
        font={
            "family": style.font_family,
            "size": style.label_size,
            "color": style.foreground,
        },
    )


def add_line(
    fig: go.Figure,
    x,
    y,
    name: str = "Line",
    dashed: bool = False,
):
    line = {
        "color": style.muted,
        "width": style.line_width,
    }

    if dashed:
        line["dash"] = "dash"

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=name,
            line=line,
        )
    )


def add_polygon(
    fig: go.Figure,
    x,
    y,
    name: str = "Polygon",
):
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=name,
            line={
                "color": style.muted,
                "width": style.polygon_line_width,
            },
            fill="toself",
            fillcolor=style.polygon_fill,
        )
    )


def style_2d(
    fig: go.Figure,
):
    fig.update_layout(
        template="plotly_white",
        hovermode="closest",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend={
            "orientation": "h",
            "x": 0,
            "y": 1.01,
            "xanchor": "left",
            "yanchor": "bottom",
            "bgcolor": "rgba(0,0,0,0)",
            "font": {
                "family": style.font_family,
                "size": style.legend_size,
                "color": style.muted,
            },
        },
        margin={
            "l": 52,
            "r": 20,
            "t": 55,
            "b": 48,
        },
        font={
            "family": style.font_family,
            "size": style.text_size,
            "color": style.foreground,
        },
        width=style.width,
        height=style.height,
    )

    axis_style = {
        "zeroline": True,
        "zerolinecolor": style.axis,
        "zerolinewidth": 1,
        "showgrid": True,
        "gridcolor": style.grid,
        "gridwidth": 1,
        "showline": False,
        "ticks": "outside",
        "ticklen": 4,
        "tickwidth": 1,
        "tickcolor": style.axis,
        "tickfont": {
            "family": style.font_family,
            "size": style.tick_size,
            "color": style.muted,
        },
    }

    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
