import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import app

######################## PT PGT
df = pd.read_excel("student.xlsx",sheet_name="PT PGT")

df = df.drop(["Centre","Acronym","SPR_CODE","SCJ_STAC","WD-reason","PRG_CODE","MOA_CODE","Grade"],axis=1)
df = df.rename(columns={"SPR_GEND":"gender",
                        "SPR_AYRS":"year",})

df_f = df[df["gender"]=="F"]
df_f = df_f.groupby(["year"],as_index=True)[["gender"]].count()

#caculate grade by gender - male
df_m = df[df["gender"]=="M"]
df_m = df_m.groupby(["year"],as_index=True)[["gender"]].count()

#createing dataset
df_o = df_m.merge(df_f,how="left",left_index=True,right_index=True)
df_o = df_o.rename(columns={"gender_x":"Male","gender_y":"Female"})
df_o.loc["Total"] = df_o.apply(lambda x:x.sum())
df_op = df_o.div(df_o.sum(axis=1),axis=0)
###########################################
df2_f = df[df["gender"]=="F"]
df2_f = df2_f.groupby(["year","award"],as_index=True)[["gender"]].count()

#caculate grade by gender - male
df2_m = df[df["gender"]=="M"]
df2_m = df2_m.groupby(["year","award"],as_index=True)[["gender"]].count()

#createing dataset
df2 = df2_m.merge(df2_f,how="left",left_index=True,right_index=True)
df2 = df2.rename(columns={"gender_x":"Male","gender_y":"Female"})

#make the columns consistent becasue some year withou full "award" columns
df2 = df2.unstack(level=1)
df2 = df2.fillna(value=0)
df2 = df2.stack(level=1)
df2 = df2.reset_index()

# Do not caculate the newset year
years = df2["year"].unique().tolist()
years.sort(reverse=True)
df2 = df2[df2["year"] != years[0]]
# caculate total 各course
df2t = df2.groupby(["award"],as_index=False)[["Male","Female"]].sum()
df2t["year"] = "Total"
df_3 = pd.concat([df2,df2t]) #1 headcount by award

# protion each course
df_3p = df_3.set_index(["year","award"],drop=True)
df_3p = df_3p.div(df_3p.sum(axis=1),axis=0)
df_3p = df_3p.reset_index() #2 protion by award

#overall - headcount and  protion
df_3o = df_3.groupby(["year"],as_index=True)[["Male","Female"]].sum()#3 headcount
df_3op = df_3o.div(df_3o.sum(axis=1),axis=0) #4 protion
#################  creating graph  #################
methods = ["by Headcount","by Proportion"]
genders = ["Male","Female"]
##################################################
dfl = df_o.reset_index()
dfl = dfl[dfl["year"]!="Total"]
trace9 = [go.Scatter(
           x=dfl["year"],
           y=dfl[i],
           mode="markers+lines",
           name=i
) for i in genders]

layout9 = go.Layout(title = "Total PTMSc Students by Gender over Time",legend=dict(title=None,
            y=1.02, yanchor="bottom",
            x=1, xanchor="right",
            orientation="h",
            font=dict(size=10)))


PTy = dict(data=trace9,layout=layout9)
###################################################

trace5 =  [go.Bar(
               x=df_3op.index,
               y=df_3op[i],
               name=i
) for i in genders]

layout5 = go.Layout(title = dict(text="WMG PTMSc Registered/Completion rate by degree (Overall)",
                                font=dict(size=16)),
                    yaxis = dict(tickformat="%")
                             )


Ptro = dict(data=trace5,layout=layout5)

##################################################


# external_stylesheets = [dbc.themes.PULSE]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tab4 = dbc.Card(
       dbc.CardBody([
           html.Div([
      dbc.Container([
            dbc.Row([
                  dbc.Col(html.H1("WMG Student Data"),className="mb-2")
               ]),
            dbc.Row([
                  dbc.Col(dbc.Card(html.H3(children="Part time Master of Science | PTMSc",className="text-center text-light bg-primary"),
                                                                     body=True,color="primary"),className="mb-4")
            ]),
            dbc.Row([
                  dbc.Col(html.H5("Total PTMSc Students"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m9",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="pt")]),
            dcc.Graph(id="ptl",figure=PTy),
            html.Hr(),
            dbc.Row([
                  dbc.Col(html.H5("WMG PTMSc Registered/Completion by degree"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m5",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="pcompletion rates")]), #graph4
            dcc.Graph(id="Ptro",figure=Ptro)

            ])
      ])
   ])
)

@app.callback(Output("pt","figure"),
              [Input("c-m9","value")])

def ug_PT(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_o
        n=None
    else:

        filter_df = df_op
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=filter_df.index,
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="Total PTMSc Students "+selected_method,
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
    pt = dict(data=trace,layout=layout)

    return pt

@app.callback(Output("pcompletion rates","figure"),
              [Input("c-m5","value")])

def completion(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_3
        n=None
    else:

        filter_df = df_3p
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=[filter_df["year"],filter_df["award"]],
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="WMG PTMSc Registered/Completion with degree "+selected_method,
                       margin=dict(l=50, r=50, b=105, t=70),
                       yaxis=dict(tickformat=n),
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=10),tickangle=65),
                       legend=dict(title=None,
                                       y=1.02, yanchor="bottom",
                                       x=1, xanchor="right",
                                       orientation="h"),
                                       font=dict(size=10),
                          #autosize=False,
                          #width=1240,
                          #height=350,
                       )
    ptc = dict(data=trace,layout=layout)

    return ptc

# if __name__ == "__main__":
     # app.run_server()
