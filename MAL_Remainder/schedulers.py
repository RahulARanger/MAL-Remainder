import plotly.express as exp
import plotly.graph_objects as go
import pandas
import pathlib
from dash import dcc, html

def ensure_data():
    data = pathlib.Path(__file__).parent / "data"
    data.mkdir(exist_ok=True)

    return data


class ScheduleCharts:
    def __init__(self):
        self.root = ensure_data() / "schedules.csv"

    def extract(self):
        columns = ["Day", "From_Time", "To_Time", "Message"]
        return pandas.read_csv(self.root, use_cols=columns) if self.root.exists() else pandas.DataFrame([], columns=columns)

    def graph(self):
        figure = exp.timeline(self.extract(), x_start="From_Time", x_end="To_Time", y="Day")
        ...
        return figure

    def html_marked_up(self):
        return html.Div(
            dcc.Graph(
                id="schedule-graph",
                figure=self.graph(),
            )
        )
