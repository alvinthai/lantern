from bokeh.plotting import figure, show, output_notebook
from bokeh.models import Legend, Span
# from bokeh.models import HoverTool
from ..utils import in_ipynb
from .plotobj import BasePlot


if in_ipynb():
    output_notebook()
_BF = None


class BokehPlot(BasePlot):
    def __init__(self, theme):
        self.figure = figure(toolbar_location="below",
                             toolbar_sticky=False,
                             x_axis_type='datetime')  # TODO remove
        self.legend = []

    def show(self, title='', xlabel='', ylabel='', xaxis=True, yaxis=True, xticks=True, yticks=True, legend=True, grid=True, **kwargs):
        # self.figure.add_tools(*[HoverTool(
        #     tooltips=[('x', '@x{%F}'), ('y', '@y')],
        #     formatters={'x': 'datetime'},
        #     mode='vline'
        # ) for _ in data])

        self.figure.outline_line_color = None
        # vline = Span(location=0, dimension='height', line_color='red', line_width=3)
        hline = Span(location=0, dimension='width', line_color='black', line_width=1)
        self.figure.renderers.append(hline)

        if xlabel:
            self.figure.xaxis.axis_label = kwargs.get('xlabel')
        if ylabel:
            self.figure.yaxis.axis_label = kwargs.get('ylabel')
        if title:
            self.figure.title.text = kwargs.get('title')

        self.figure.legend.location = None
        if legend:
            legend = Legend(items=self.legend, location=(10, 100))
            legend.click_policy = "mute"
            self.figure.add_layout(legend, 'right')

        if not grid:
            self.figure.xgrid.grid_line_color = None
            self.figure.ygrid.grid_line_color = None

        # FIXME
        if not yaxis:
            for ax in self.figure.yaxis:
                ax.axis_line_color = 'white'
        if not xaxis:
            for ax in self.figure.xaxis:
                ax.axis_line_color = 'white'

        # Turn off labels:
        # self.figure.xaxis.major_label_text_font_size = '0pt'

        show(self.figure)
        return self.figure

    def line(self, data, **kwargs):
        for col in data:
            l = self.figure.line(x=data.index, y=data[col].values, legend=col, **kwargs)
            self.legend.append((col, [l]))
