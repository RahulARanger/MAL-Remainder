from dash import Dash, html, dcc
import plotly.express as exp
from MAL_Remainder.calendar_parse import today
from MAL_Remainder.common_utils import EnsurePort
import sys

trust = EnsurePort("/", "dashboard")

if trust.deep_check():
    sys.exit(-1)

app = Dash("MAL-Remainder-DashBoard")


def dark_mode(figure):
    figure.update_layout(
        template="plotly_dark"
    )
    return figure


def color_map():
    return exp.colors.qualitative.D3


def events_chart():
    events = today()
    figure = dark_mode(
        exp.timeline(
            events,
            x_start="started",
            x_end="ended",
            hover_name="summary",
            y="title",
            color="title",
            color_discrete_sequence=color_map(),
            height=250,
            width=600
        )
    )

    return dcc.Graph(
        id="gantt-chart",
        figure=figure
    )


def create_layout():
    return html.Div([
        html.Main(
            [
                events_chart()
            ]
        )])


app.layout = create_layout()

port = trust()
trust.acquire(port)

app.run_server(port=port, host="localhost")
trust.release()


