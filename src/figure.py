from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from style import FigureStyle


class LatFigure:
    def __init__(
        self,
        title: str = "Lattice",
        show_axis: bool = True,
        is_light: bool = True,
    ):
        self.fig = go.Figure()
        self.style = FigureStyle(is_light)

        self.fig.update_layout(**self.style.layout())
        self.fig.update_xaxes(**self.style.axis_config())
        self.fig.update_yaxes(**self.style.axis_config())

        self.change_title(title)
        self.set_axes(showticklabels=show_axis)

    def write(self, filename: str):
        self.fig.write_image(filename)
    
    def show(self):
        self.fig.show()

    def change_title(self, title: str = "Lattice"):
        self.fig.update_layout(title=self.style.title(title))

    def set_axes(
        self,
        x_range=None,
        y_range=None,
        showticklabels: bool = True,
        equal_range: bool = True,
    ):
        if equal_range and x_range is not None and y_range is not None:
            axis_range = equal_axis_range(x_range, y_range)
            x_range = axis_range
            y_range = axis_range

        visibility = self.style.axis_visibility(showticklabels)

        self.fig.update_xaxes(
            range=x_range,
            **visibility,
        )
        self.fig.update_yaxes(
            range=y_range,
            **visibility,
        )

    def add_point(
        self,
        x: float,
        y: float,
        name: str = "Point",
        role: str = "default",
        marker_size: int | None = None,
    ):
        self.add_points(
            [x],
            [y],
            name=name,
            role=role,
            marker_size=marker_size,
        )

    def add_points(
        self,
        x,
        y,
        name: str = "Points",
        role: str = "default",
        marker_size: int | None = None,
    ):
        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                name=name,
                marker=self.style.point_marker(role, marker_size),
                **self.style.point_trace(),
            )
        )

    def add_label(
        self,
        x: float,
        y: float,
        text: str,
    ):
        self.fig.add_annotation(
            x=x,
            y=y,
            text=text,
            **self.style.label_annotation(),
        )

    def add_line(
        self,
        x,
        y,
        name: str = "Line",
        dashed: bool = False,
    ):
        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=name,
                line=self.style.line(dashed=dashed),
            )
        )

    def add_polygon(
        self,
        x,
        y,
        name: str = "Polygon",
    ):
        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=name,
                **self.style.polygon_trace(),
            )
        )

    def add_arrow(
        self,
        start,
        end,
        label=None,
        label_t: float | None = None,
        label_offset=None,
    ):
        label_t = self.style.arrow_label_t if label_t is None else label_t

        label_offset = (
            self.style.arrow_label_offset if label_offset is None else label_offset
        )

        start = np.asarray(start, dtype=float)
        end = np.asarray(end, dtype=float)

        self.fig.add_trace(
            go.Scatter(
                x=[float(start[0]), float(end[0])],
                y=[float(start[1]), float(end[1])],
                mode="lines+markers",
                **self.style.arrow_trace(),
            )
        )

        if label is not None:
            position = start + label_t * (end - start)

            self.add_label(
                position[0] + label_offset[0],
                position[1] + label_offset[1],
                label,
            )


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
