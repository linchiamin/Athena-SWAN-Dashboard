import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import app

df = pd.read_excel("student.xlsx",sheet_name="Research")

df = df.drop(["Centre","Acronym","SPR_CODE","SCJ_STAC","WD-reason","PRG_CODE","MOA_CODE","award","Grade"],axis=1)
df = df.rename(columns={"SPR_GEND":"gender",
                        "SPR_AYRS":"year",})

df_f = df[df["gender"]=="F"]
df_f = df_f.groupby(["year"],as_index=True)[["gender"]].count()

#caculate grade by gender - male
df_m = df[df["gender"]=="M"]
df_m = df_m.groupby(["year"],as_index=True)[["gender"]].count()

#createing dataset
df = df_m.merge(df_f,how="left",left_index=True,right_index=True)
df = df.rename(columns={"gender_x":"Male","gender_y":"Female"})
#By headcount
df.loc["Total"] = df.apply(lambda x:x.sum())
#by protion
df_p = df.div(df.sum(axis=1),axis=0)

###############
methods = ["by Headcount","by Proportion"]
genders = ["Male","Female"]
######################
dfi = df.reset_index()
dfi = dfi[dfi["year"]!="Total"]

trace6 = [go.Scatter(
           x=dfi["year"],
           y=dfi[i],
           mode="markers+lines",
           name=i
) for i in genders]

layout6 = go.Layout(title = "Total PGR Students by Gender over Time",legend=dict(title=None,
            y=1.02, yanchor="bottom",
            x=1, xanchor="right",
            orientation="h",
            font=dict(size=10)))


Pgry = dict(data=trace6,layout=layout6)
######################
#external_stylesheets = [dbc.themes.PULSE]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tab5 = dbc.Card(
       dbc.CardBody([
           html.Div([
      dbc.Container([
            dbc.Row([
                  dbc.Col(html.H1("WMG Student Data"),className="mb-2")
               ]),
            dbc.Row([
                  dbc.Col(dbc.Card(html.H3(children="Postgraduate Research | PGR",className="text-center text-light bg-primary"),
                                                                     body=True,color="primary"),className="mb-4")
            ]),
            dbc.Row([
                  dbc.Col(html.H5("Total PGR Students including PhD"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m6",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="research")]), #graph4
            dcc.Graph(id="Pgry",figure=Pgry)

            ])
      ])
   ])
)

@app.callback(Output("research","figure"),
              [Input("c-m6","value")])

def ug_research(selected_method):

    if selected_method == "by Headcount":

        filter_df = df
        n=None
    else:

        filter_df = df_p
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=filter_df.index,
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="Total PGR Students including PhD "+selected_method,
                       margin=dict(l=50, r=50, b=105, t=70),
                       yaxis=dict(tickformat=n),
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=12)),
                       legend=dict(title=None,
                                       y=1.02, yanchor="bottom",
                                       x=1, xanchor="right",
                                       orientation="h"),
                                       font=dict(size=10),
                          #autosize=False,
                          #width=1240,
                          #height=350,
                       )
    pgr = dict(data=trace,layout=layout)

    return pgr

#if __name__ == "__main__":
    # app.run_server()
