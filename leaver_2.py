import plotly.graph_objs as go
import pandas as pd
import plotly.offline as pyo
from leaver_1 import df
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State

df3 = df.groupby(["reason","year","function"],as_index=False)[["No. of male leavers","No. of female leavers"]].sum()


df3 = df3.replace({"Going for better job prospects":"better job prospects","Comp. redundancy - fixed term ":"Redundancy, FTC",
                    "Other work related reason     ":"Other work<br>related reason","Resignation (no reason given) ":"Resignation<br>(no reason given)",
                    "Relocating                    ":"Relocating","Other non work related reason ":"Other non-work<br>related reason",
                    "Normal retirement             ":"Retirement(Normal)"})

df3 = df3.reset_index(drop=True)
df3 = df3.drop([0,1,2,3,4,5])

df3_T= df3.groupby(["reason","year"],as_index=False)[["No. of male leavers","No. of female leavers"]].sum()# make hover data show correct value
df3A = df3[df3["function"] != "Professional and Support Staff"]
df3A = df3A.groupby(["reason","year"],as_index=False)[["No. of male leavers","No. of female leavers"]].sum()# make hover data show correct value
df3S = df3[df3["function"] == "Professional and Support Staff"]
df3S = df3S.groupby(["reason","year"],as_index=False)[["No. of male leavers","No. of female leavers"]].sum()# make hover data show correct value

reason_options=df3["reason"].unique().tolist()

vale=["Redundancy, FTC","better job prospects","Retirement(Normal)","Other non-work<br>related reason",
      "Other work<br>related reason","Relocating","Resignation<br>(no reason given)"]

function_options3 = ["Overall","Academic","Professional and Support Staff"]
'''
app = dash.Dash()
app.layout= html.Div ([
                    html.Div([
                    html.Label("Select function type"),
                    dcc.Dropdown(
                    id="function-picker3",
                    options=[dict(label=str(i),value=i) for i in function_options3],
                    value="Overall"
                    ),
                    html.Label("Select Leaving Reasons"),
                    dcc.Dropdown(
                    id="reason",
                    options=[dict(label=str(i),value=i) for i in reason_options],
                    value=vale,
                    multi=True
                    )
                    ],style={"width":"90%","marginLeft":"6%"}),
                    html.Div([
                    html.Div([
                    html.Label("*Orange: Numbers of female leavers",style={"fontsize":50,"color":"rgb(255,127,14)"}),
                    html.Label("  *Blue: Numbers of male leavers",style={"fontsize":80,"color":"rgb(31,119,180)"})
                    ],style={"marginLeft":"6%"}),
                    dcc.Graph(id="leaver")])
                    ])
@app.callback(Output("leaver","figure"),
              [Input("function-picker3","value")
              ,Input("reason","value")])

def reason_upgratd(selected_function,selected_reasons):



     data=[]
     for i in selected_reasons:

                 if selected_function=="Overall":

                    filter_df=df3_T

                 elif selected_function=="Academic":

                    filter_df=df3A

                 else:

                    filter_df=df3S

                 filter_df=filter_df[filter_df["reason"]==i]
                 trace1 = go.Bar(
                 x=[filter_df["reason"],filter_df["year"]],
                 y=filter_df["No. of male leavers"],
                 name="Numbers of male leavers - ",
                 marker_color="rgb(31,119,180)"
                 )

                 trace2 = go.Bar(
                 x=[filter_df["reason"],filter_df["year"]],
                 y=filter_df["No. of female leavers"],
                 name="Numbers of female leavers - "+i,
                 marker_color="rgb(255,127,14)"
                 )

                 data.append(trace1)
                 data.append(trace2)

     layout = go.Layout(title=dict(text="Leavers by reason over the period 2014-2018, headcount",
                            y=0.9,
                            x=0.5,
                            xanchor="center",
                            yanchor="top"),
                            barmode="stack",
                            legend=dict(title=None,
                                        y=1.02, yanchor="bottom",
                                        x=1, xanchor="right",
                                        orientation="h"),
                            showlegend=False,
                            font=dict(size=10),
                            yaxis=dict(nticks=10)
                            )


     fig = dict(data=data, layout=layout)

     return fig

if __name__ == "__main__":
    app.run_server()
'''
