from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import plotly.graph_objects as go


@dataclass(frozen=True)
class FigureStyle:
    font_family: str = 'Georgia, "Times New Roman", serif'

    template: str = "plotly_white"
    background: str = "#ffffff"
    foreground: str = "#1f2328"
    muted: str = "#666"
    axis: str = "#777"
    grid: str = "#eeeeee"

    width: int = 780
    height: int = 780
    number_line_height: int = 280

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
    number_line_arrow_size: float = 5.2
    arrow_marker_size: int = 10

    line_width: float = 1.2

    polygon_line_width: float = 1
    polygon_fill: str = "rgba(31, 35, 40, 0.06)"

    margin_left: int = 52
    margin_right: int = 20
    margin_top: int = 55
    margin_bottom: int = 48

    axis_zero_line_width: float = 1
    axis_grid_width: float = 1
    axis_tick_length: int = 4
    axis_tick_width: float = 1
    axis_ticks: str = "outside"

    legend_orientation: str = "h"
    legend_x: float = 0
    legend_y: float = 1.01
    legend_x_anchor: str = "left"
    legend_y_anchor: str = "bottom"
    legend_background: str = "rgba(0,0,0,0)"

    point_z_order: int = 1
    arrow_z_order: int = -1
    line_dash: str = "dash"
    hover_mode: str = "closest"
    hidden_hover_info: str = "skip"

    number_line_arrow_x_shift: int = -20
    number_line_arrow_head: int = 4
    interval_line_width: float = 6.0
    number_line_y_range: tuple[float, float] = (-0.3, 0.3)
    interval_label_offset: float = 0.18
    tick_height: float = 0.08
    tick_label_offset: float = -0.16
    number_line_point_label_offset: float = 0.16

    basis_label_padding: float = 0.035
    arrow_label_t: float = 0.5
    arrow_label_offset: tuple[float, float] = (0.0, 0.0)

    def layout(self, *, height: int | None = None, show_legend: bool = True) -> dict:
        return {
            "template": self.template,
            "hovermode": self.hover_mode,
            "paper_bgcolor": self.background,
            "plot_bgcolor": self.background,
            "showlegend": show_legend,
            "legend": {
                "orientation": self.legend_orientation,
                "x": self.legend_x,
                "y": self.legend_y,
                "xanchor": self.legend_x_anchor,
                "yanchor": self.legend_y_anchor,
                "bgcolor": self.legend_background,
                "font": self.legend_font(),
            },
            "margin": {
                "l": self.margin_left,
                "r": self.margin_right,
                "t": self.margin_top,
                "b": self.margin_bottom,
            },
            "font": self.text_font(),
            "width": self.width,
            "height": self.height if height is None else height,
        }

    def text_font(self) -> dict:
        return {
            "family": self.font_family,
            "size": self.text_size,
            "color": self.foreground,
        }

    def title_font(self) -> dict:
        return {
            "family": self.font_family,
            "size": self.title_size,
            "color": self.foreground,
        }

    def label_font(self) -> dict:
        return {
            "family": self.font_family,
            "size": self.label_size,
            "color": self.foreground,
        }

    def legend_font(self) -> dict:
        return {
            "family": self.font_family,
            "size": self.legend_size,
            "color": self.muted,
        }

    def tick_font(self) -> dict:
        return {
            "family": self.font_family,
            "size": self.tick_size,
            "color": self.muted,
        }

    def title(self, text: str) -> dict:
        return {
            "text": text,
            "x": 0,
            "xanchor": self.legend_x_anchor,
            "font": self.title_font(),
        }

    def axis_config(self) -> dict:
        return {
            "zeroline": True,
            "zerolinecolor": self.axis,
            "zerolinewidth": self.axis_zero_line_width,
            "showgrid": True,
            "gridcolor": self.grid,
            "gridwidth": self.axis_grid_width,
            "showline": False,
            "ticks": self.axis_ticks,
            "ticklen": self.axis_tick_length,
            "tickwidth": self.axis_tick_width,
            "tickcolor": self.axis,
            "tickfont": self.tick_font(),
        }

    def axis_visibility(self, show_tick_labels: bool) -> dict:
        return {
            "showticklabels": show_tick_labels,
            "ticks": self.axis_ticks if show_tick_labels else "",
        }

    def point_marker(self, role: str, marker_size: int | None = None) -> dict:
        sizes = {
            "default": self.point_size,
            "emphasis": self.emphasis_point_size,
            "secondary": self.secondary_point_size,
            "origin": self.origin_point_size,
        }
        colors = {
            "default": self.foreground,
            "emphasis": self.foreground,
            "secondary": self.muted,
            "origin": self.background,
        }
        if role not in sizes:
            raise ValueError(f"Unknown point role: {role}")

        marker = {
            "size": marker_size or sizes[role],
            "color": colors[role],
        }
        if role == "origin":
            marker["line"] = {
                "color": self.foreground,
                "width": self.origin_border_width,
            }
        return marker

    def point_trace(self) -> dict:
        return {"zorder": self.point_z_order}

    def arrow_line(self) -> dict:
        return {"color": self.foreground, "width": self.arrow_width}

    def arrow_marker(self) -> dict:
        return {
            "symbol": ["circle", "arrow"],
            "size": [0, self.arrow_marker_size],
            "color": self.foreground,
            "angleref": "previous",
        }

    def arrow_trace(self) -> dict:
        return {
            "line": self.arrow_line(),
            "marker": self.arrow_marker(),
            "showlegend": False,
            "hoverinfo": self.hidden_hover_info,
            "zorder": self.arrow_z_order,
        }

    def label_annotation(self) -> dict:
        return {"showarrow": False, "font": self.label_font()}

    def line(self, *, dashed: bool = False, width: float | None = None) -> dict:
        line = {
            "color": self.muted,
            "width": self.line_width if width is None else width,
        }
        if dashed:
            line["dash"] = self.line_dash
        return line

    def polygon_line(self) -> dict:
        return {"color": self.muted, "width": self.polygon_line_width}

    def polygon_trace(self) -> dict:
        return {
            "line": self.polygon_line(),
            "fill": "toself",
            "fillcolor": self.polygon_fill,
        }

    def number_line_x_axis(self, show_tick_labels: bool) -> dict:
        return {
            "showgrid": False,
            "zeroline": False,
            "showline": False,
            **self.axis_visibility(show_tick_labels),
            "tickfont": self.tick_font(),
            "fixedrange": True,
        }

    def number_line_y_axis(self) -> dict:
        return {"visible": False, "fixedrange": True}

    def number_line_arrow(self) -> dict:
        return {
            "ax": self.number_line_arrow_x_shift,
            "ay": 0,
            "xref": "x",
            "yref": "y",
            "text": "",
            "showarrow": True,
            "arrowhead": self.number_line_arrow_head,
            "arrowsize": self.number_line_arrow_size,
            "arrowwidth": self.line_width,
            "arrowcolor": self.foreground,
        }

    def number_line(self) -> dict:
        return {"color": self.axis, "width": self.line_width}

    def interval_line(self, role: str, dashed: bool, width: float | None) -> dict:
        colors = {
            "default": self.foreground,
            "secondary": self.muted,
            "axis": self.axis,
        }
        if role not in colors:
            raise ValueError(f"Unknown line role: {role}")

        line = {
            "color": colors[role],
            "width": self.interval_line_width if width is None else width,
        }
        if dashed:
            line["dash"] = self.line_dash
        return line

    def tick_line(self) -> dict:
        return {"color": self.foreground, "width": self.line_width}

    def number_line_marker(
        self,
        role: str,
        filled: bool,
        marker_size: int | None,
    ) -> dict:
        line = self.interval_line(role, dashed=False, width=self.origin_border_width)
        color = line["color"]
        return {
            "size": marker_size or self.point_size,
            "color": color if filled else self.background,
            "line": line,
        }

    def number_line_point_trace(self) -> dict:
        return {
            "showlegend": False,
            "hoverinfo": self.hidden_hover_info,
        }


@dataclass(frozen=True)
class DarkFigureStyle(FigureStyle):
    template: str = "plotly_dark"
    background: str = "#0d1117"
    foreground: str = "#e6edf3"
    muted: str = "#9da7b3"
    axis: str = "#8b949e"
    grid: str = "#30363d"
    polygon_fill: str = "rgba(230, 237, 243, 0.06)"


LIGHT_STYLE = FigureStyle()
DARK_STYLE = DarkFigureStyle()

_STYLE_META_KEY = "latgraph_style"


def bind_style(fig: go.Figure, style: FigureStyle) -> FigureStyle:
    """Attach a style to a figure so later helpers inherit it."""
    meta = dict(fig.layout.meta or {})
    meta[_STYLE_META_KEY] = asdict(style)
    fig.update_layout(meta=meta)
    return style


def resolve_style(
    fig: go.Figure,
    style: FigureStyle | None = None,
) -> FigureStyle:
    """Return an explicit, figure-bound, or default style, in that order."""
    if style is not None:
        return bind_style(fig, style)

    meta = fig.layout.meta
    if meta and _STYLE_META_KEY in meta:
        return FigureStyle(**meta[_STYLE_META_KEY])

    return bind_style(fig, LIGHT_STYLE)
