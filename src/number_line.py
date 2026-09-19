

import plotly.graph_objects as go

from figure import add_label, change_title
from style import LIGHT_STYLE, FigureStyle, resolve_style


def plot_number_line(
    x_range,
    title: str = "",
    showticklabels: bool = False,
    show_axis_arrow: bool = True,
    y_range=None,
    style: FigureStyle = LIGHT_STYLE,
) -> go.Figure:
    """Create a one-dimensional number-line figure."""
    start, end = map(float, x_range)

    if start >= end:
        raise ValueError("x_range must satisfy start < end.")

    fig = go.Figure()
    style = resolve_style(fig, style)
    y_range = style.number_line_y_range if y_range is None else y_range

    fig.update_layout(**style.layout(height=style.number_line_height, show_legend=False))

    change_title(fig, title)

    fig.update_xaxes(
        range=[start, end],
        **style.number_line_x_axis(showticklabels),
    )

    fig.update_yaxes(
        range=list(y_range),
        **style.number_line_y_axis(),
    )

    add_number_line(fig, start, end)

    if show_axis_arrow:
        add_axis_arrow(fig, end)

    return fig


def add_axis_arrow(
    fig: go.Figure,
    x: float,
    y: float = 0.0,
    style: FigureStyle | None = None,
):
    """Add a right-facing arrowhead to a number line."""
    style = resolve_style(fig, style)
    fig.add_annotation(
        x=x,
        y=y,
        **style.number_line_arrow(),
    )


def add_number_line(
    fig: go.Figure,
    start: float,
    end: float,
    style: FigureStyle | None = None,
):
    """Draw the horizontal number line."""
    style = resolve_style(fig, style)
    fig.add_shape(
        type="line",
        x0=start,
        x1=end,
        y0=0,
        y1=0,
        line=style.number_line(),
    )


def add_interval(
    fig: go.Figure,
    start: float,
    end: float,
    label: str | None = None,
    y: float = 0.0,
    label_offset: float | None = None,
    role: str = "default",
    dashed: bool = False,
    line_width: float | None = None,
    style: FigureStyle | None = None,
):
    """Highlight an interval on the number line."""
    if start > end:
        raise ValueError("Interval must satisfy start <= end.")

    style = resolve_style(fig, style)
    label_offset = style.interval_label_offset if label_offset is None else label_offset
    fig.add_shape(
        type="line",
        x0=start,
        x1=end,
        y0=y,
        y1=y,
        line=style.interval_line(role, dashed, line_width),
    )

    if label is not None:
        add_label(fig, (start + end) / 2, y + label_offset, label)


def add_tick(
    fig: go.Figure,
    x: float,
    label: str | None = None,
    y: float = 0.0,
    height: float | None = None,
    label_offset: float | None = None,
    style: FigureStyle | None = None,
):
    """Add a marked position to the number line."""
    style = resolve_style(fig, style)
    height = style.tick_height if height is None else height
    label_offset = style.tick_label_offset if label_offset is None else label_offset
    fig.add_shape(
        type="line",
        x0=x,
        x1=x,
        y0=y - height,
        y1=y + height,
        line=style.tick_line(),
    )

    if label is not None:
        add_label(fig, x, y + label_offset, label)


def add_number_line_point(
    fig: go.Figure,
    x: float,
    label: str | None = None,
    y: float = 0.0,
    label_offset: float | None = None,
    role: str = "default",
    filled: bool = True,
    marker_size: int | None = None,
    style: FigureStyle | None = None,
):
    """Add an open or closed point to the number line."""
    style = resolve_style(fig, style)
    label_offset = (
        style.number_line_point_label_offset if label_offset is None else label_offset
    )
    fig.add_trace(
        go.Scatter(
            x=[x],
            y=[y],
            mode="markers",
            marker=style.number_line_marker(role, filled, marker_size),
            **style.number_line_point_trace(),
        )
    )

    if label is not None:
        add_label(fig, x, y + label_offset, label)
