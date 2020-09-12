import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
from app import server
from FT import tab3
from PT import tab4
from PR import tab5
from UG import tab6

tabs3 = dbc.Card(
    [
      dbc.CardHeader(
        dbc.Tabs(
            [
                 dbc.Tab(label="➤ FT MSc" , tab_id="tab-1"),
                 dbc.Tab(label="➤ PT MSc" , tab_id="tab-2"),
                 dbc.Tab(label="➤ PGR and PHD" , tab_id="tab-3"),
                 dbc.Tab(label="➤ Undergrate" , tab_id="tab-4")
            ],
            id="Card-tabs",
            card=True,
            active_tab="tab-1",
        )
        ),
      dbc.CardBody(html.Div(id="content")),
    ]
)

app.layout = html.Div(tabs3)

@app.callback(Output("content", "children"), [Input("Card-tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab3
    elif at == "tab-2":
        return tab4
    elif at == "tab-3":
        return tab5
    elif at == "tab-4":
        return tab6
    return html.P("This shouldn't ever be displayed...")

if __name__ == "__main__":
     app.run_server()
