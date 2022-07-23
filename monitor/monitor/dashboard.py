
from dash import Dash, html, dcc, Input, Output
from plotly.subplots import make_subplots

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from .db import get_connection


app = Dash(__name__, url_base_pathname='/monitor/')
app.layout = html.Div(children=[
    html.H1(children="Traffic admin"),
    dcc.Dropdown(["-6 hours", "-1 day", "-7 days"], "-6 hours", id="period"),
    dcc.Graph(id="graph"),
])
server = app.server


@app.callback(
    Output("graph", "figure"), 
    Input("period", "value")
)
def update_line_chart(period):
    with get_connection() as conn:
        df = pd.read_sql_query(
        """
        SELECT d.owner_name, d.name, m.* FROM "monitor" as m
        JOIN "devices" as d ON (m.public_key = d.public_key)
        WHERE ts > date('now', ?)
        ORDER BY ts
        """, conn, params=(period, ))


    grp = df.groupby(["public_key", "owner_name", "name"])

    def get_mbytes(dt):
        tstart, tend = dt.transmit_bytes.iloc[[0, -1]]
        rstart, rend = dt.receive_bytes.iloc[[0, -1]]

        return (tend + rend - (tstart + rstart)) / 1000000

    titles = [f'{owname} / {name} ({get_mbytes(dt):.2f} MB)' for (_, owname, name), dt in grp]

    fig = make_subplots(
        rows=len(grp),
        cols=1,
        subplot_titles=titles,
        shared_xaxes=True,
        shared_yaxes=True,
    )

    for i, (_, dt) in enumerate(grp, start=1):
        fig.append_trace(
            go.Scatter(x=dt.ts, y=dt.transmit_bytes, line_color="#0000ff"), row=i, col=1,
        )
        fig.append_trace(
            go.Scatter(x=dt.ts, y=dt.receive_bytes, line_color="#ff0000"), row=i, col=1,
        )
    
    fig.update_layout(height=200*len(grp), showlegend=False)
    return fig
