from __future__ import annotations

import plotly.graph_objects as go

from figure import add_label, change_title, style

NUMBER_LINE_HEIGHT = 280


def _role_color(role: str) -> str:
    if role == "default":
        return style.foreground
    if role == "secondary":
        return style.muted
    if role == "axis":
        return style.axis
    raise ValueError(f"Unknown line role: {role}")

def plot_number_line(
    x_range,
    title: str = "",
    showticklabels: bool = False,
    show_axis_arrow: bool = True,
    y_range=(-0.3, 0.3),
) -> go.Figure:
    """Create a one-dimensional number-line figure."""
    start, end = map(float, x_range)

    if start >= end:
        raise ValueError("x_range must satisfy start < end.")

    fig = go.Figure()

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        margin={"l": 52, "r": 20, "t": 55, "b": 48},
        font={
            "family": style.font_family,
            "size": style.text_size,
            "color": style.foreground,
        },
        width=style.width,
        height=NUMBER_LINE_HEIGHT,
    )

    change_title(fig, title)

    fig.update_xaxes(
        range=[start, end],
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=showticklabels,
        ticks="outside" if showticklabels else "",
        tickfont={
            "family": style.font_family,
            "size": style.tick_size,
            "color": style.muted,
        },
        fixedrange=True,
    )

    fig.update_yaxes(
        range=list(y_range),
        visible=False,
        fixedrange=True,
    )

    add_number_line(
        fig,
        start,
        end,
    )

    if show_axis_arrow:
        add_axis_arrow(
            fig,
            end,
        )

    return fig

def add_axis_arrow(
    fig: go.Figure,
    x: float,
    y: float = 0.0,
):
    """Add a right-facing arrowhead to a number line."""
    fig.add_annotation(
        x=x,
        y=y,
        ax=-20,
        ay=0,
        xref="x",
        yref="y",
        text="",
        showarrow=True,
        arrowhead=4,
        arrowsize=5.2,
        arrowwidth=style.line_width,
        arrowcolor=style.foreground,
    )

def add_number_line(
    fig: go.Figure,
    start: float,
    end: float,
):
    """Draw the horizontal number line."""
    fig.add_shape(
        type="line",
        x0=start,
        x1=end,
        y0=0,
        y1=0,
        line={
            "color": style.axis,
            "width": style.line_width,
        },
    )

def add_interval(
    fig: go.Figure,
    start: float,
    end: float,
    label: str | None = None,
    y: float = 0.0,
    label_offset: float = 0.18,
    role: str = "default",
    dashed: bool = False,
    line_width: float = 6.0,
):
    """Highlight an interval on the number line."""
    if start > end:
        raise ValueError("Interval must satisfy start <= end.")

    line = {
        "color": _role_color(role),
        "width": line_width,
    }
    if dashed:
        line["dash"] = "dash"

    fig.add_shape(
        type="line",
        x0=start,
        x1=end,
        y0=y,
        y1=y,
        line=line,
    )

    if label is not None:
        add_label(
            fig,
            (start + end) / 2,
            y + label_offset,
            label,
        )


def add_tick(
    fig: go.Figure,
    x: float,
    label: str | None = None,
    y: float = 0.0,
    height: float = 0.08,
    label_offset: float = -0.16,
):
    """Add a marked position to the number line."""
    fig.add_shape(
        type="line",
        x0=x,
        x1=x,
        y0=y - height,
        y1=y + height,
        line={
            "color": style.foreground,
            "width": style.line_width,
        },
    )

    if label is not None:
        add_label(
            fig,
            x,
            y + label_offset,
            label,
        )


def add_number_line_point(
    fig: go.Figure,
    x: float,
    label: str | None = None,
    y: float = 0.0,
    label_offset: float = 0.16,
    role: str = "default",
    filled: bool = True,
    marker_size: int | None = None,
):
    """Add an open or closed point to the number line."""
    color = _role_color(role)

    marker = {
        "size": marker_size or style.point_size,
        "color": color if filled else "white",
        "line": {
            "color": color,
            "width": style.origin_border_width,
        },
    }

    fig.add_trace(
        go.Scatter(
            x=[x],
            y=[y],
            mode="markers",
            marker=marker,
            showlegend=False,
            hoverinfo="skip",
        )
    )

    if label is not None:
        add_label(
            fig,
            x,
            y + label_offset,
            label,
        )
