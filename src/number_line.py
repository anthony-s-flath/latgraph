import plotly.graph_objects as go

from style import FigureStyle


class NumberLineFigure:
    def __init__(
        self,
        x_range,
        title: str = "",
        showticklabels: bool = False,
        show_axis_arrow: bool = True,
        y_range=None,
        is_light: bool = True,
    ):
        start, end = map(float, x_range)

        if start >= end:
            raise ValueError("x_range must satisfy start < end.")

        self.fig = go.Figure()
        self.style = FigureStyle(is_light)
        self.start = start
        self.end = end

        y_range = (
            self.style.number_line_y_range
            if y_range is None
            else y_range
        )

        self.fig.update_layout(
            **self.style.layout(
                height=self.style.number_line_height,
                show_legend=False,
            )
        )

        self.fig.update_layout(
            title=self.style.title(title)
        )

        self.fig.update_xaxes(
            range=[start, end],
            **self.style.number_line_x_axis(showticklabels),
        )

        self.fig.update_yaxes(
            range=list(y_range),
            **self.style.number_line_y_axis(),
        )

        self.add_number_line()

        if show_axis_arrow:
            self.add_axis_arrow(end)

    def write(self, filename: str):
        self.fig.write_image(filename)
    
    def show(self):
        self.fig.show()

    def add_number_line(self):
        self.fig.add_shape(
            type="line",
            x0=self.start,
            x1=self.end,
            y0=0,
            y1=0,
            line=self.style.number_line(),
        )

    def add_axis_arrow(
        self,
        x: float,
        y: float = 0.0,
    ):
        self.fig.add_annotation(
            x=x,
            y=y,
            **self.style.number_line_arrow(),
        )

    def add_interval(
        self,
        start: float,
        end: float,
        label: str | None = None,
        y: float = 0.0,
        label_offset: float | None = None,
        role: str = "default",
        dashed: bool = False,
        line_width: float | None = None,
    ):
        if start > end:
            raise ValueError("Interval must satisfy start <= end.")

        label_offset = (
            self.style.interval_label_offset
            if label_offset is None
            else label_offset
        )

        self.fig.add_shape(
            type="line",
            x0=start,
            x1=end,
            y0=y,
            y1=y,
            line=self.style.interval_line(
                role,
                dashed,
                line_width,
            ),
        )

        if label is not None:
            self.add_label(
                (start + end) / 2,
                y + label_offset,
                label,
            )

    def add_tick(
        self,
        x: float,
        label: str | None = None,
        y: float = 0.0,
        height: float | None = None,
        label_offset: float | None = None,
    ):
        height = (
            self.style.tick_height
            if height is None
            else height
        )

        label_offset = (
            self.style.tick_label_offset
            if label_offset is None
            else label_offset
        )

        self.fig.add_shape(
            type="line",
            x0=x,
            x1=x,
            y0=y - height,
            y1=y + height,
            line=self.style.tick_line(),
        )

        if label is not None:
            self.add_label(
                x,
                y + label_offset,
                label,
            )

    def add_point(
        self,
        x: float,
        label: str | None = None,
        y: float = 0.0,
        label_offset: float | None = None,
        role: str = "default",
        filled: bool = True,
        marker_size: int | None = None,
    ):
        label_offset = (
            self.style.number_line_point_label_offset
            if label_offset is None
            else label_offset
        )

        self.fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker=self.style.number_line_marker(
                    role,
                    filled,
                    marker_size,
                ),
                **self.style.number_line_point_trace(),
            )
        )

        if label is not None:
            self.add_label(
                x,
                y + label_offset,
                label,
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
