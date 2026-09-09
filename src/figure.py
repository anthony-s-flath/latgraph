from __future__ import annotations

import plotly.graph_objects as go

FONT_FAMILY = 'Georgia, "Times New Roman", serif'


def new_figure(
    title: str = "Lattice",
) -> go.Figure:
    fig = go.Figure()
    _style_2d(fig)
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

    fig.update_xaxes(range=x_range)
    fig.update_yaxes(
        range=y_range,
        scaleanchor="x",
        scaleratio=1,
    )


def change_title(fig: go.Figure, title: str = "Lattice"):
    fig.update_layout(
        title={
            "text": title,
            "x": 0,
            "xanchor": "left",
            "font": {
                "family": FONT_FAMILY,
                "size": 18,
                "color": "#1f2328",
            },
        }
    )

def add_points(
    fig: go.Figure,
    x,
    y,
    name: str = "Points",
    marker_size: int = 7,
    marker_color: str = "#30343b",
    marker_line_color=None,
    marker_line_width: float = 0,
):
    marker = {
        "size": marker_size,
        "color": marker_color,
    }

    if marker_line_color is not None:
        marker["line"] = {
            "color": marker_line_color,
            "width": marker_line_width,
        }

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name=name,
            marker=marker,
        )
    )


def add_point(
    fig: go.Figure,
    x: float,
    y: float,
    name: str = "Point",
    marker_size: int = 7,
    marker_color: str = "#30343b",
    marker_line_color=None,
    marker_line_width: float = 0,
):
    add_points(
        fig,
        [x],
        [y],
        name=name,
        marker_size=marker_size,
        marker_color=marker_color,
        marker_line_color=marker_line_color,
        marker_line_width=marker_line_width,
    )

def _style_2d(
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
                "family": FONT_FAMILY,
                "size": 12,
                "color": "#555",
            },
        },
        margin={
            "l": 52,
            "r": 20,
            "t": 55,
            "b": 48,
        },
        font={
            "family": FONT_FAMILY,
            "size": 14,
            "color": "#1f2328",
        },
        width=780,
        height=780,
    )

    axis_style = {
        "zeroline": True,
        "zerolinecolor": "#777",
        "zerolinewidth": 1,
        "showgrid": True,
        "gridcolor": "#eeeeee",
        "gridwidth": 1,
        "showline": False,
        "ticks": "outside",
        "ticklen": 4,
        "tickwidth": 1,
        "tickcolor": "#777",
        "tickfont": {
            "family": FONT_FAMILY,
            "size": 12,
            "color": "#555",
        },
    }

    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
