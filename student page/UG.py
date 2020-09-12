import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import app

df = pd.read_excel("student.xlsx",sheet_name="UG")

df = df.drop(["Centre","SPR_CODE","SCJ_STAC","WD-reason","PRG_CODE","MOA_CODE","award","Grade"],axis=1)
df = df.rename(columns={"SPR_GEND":"gender",
                        "SPR_AYRS":"year",
                        "Acronym":"course"})

# main dataset
df = df.query('gender == ["M","F"]')
df = df.reset_index(drop=True)
#1 UG no.student by gender
df_TM = df[df["gender"]== "M"]
df_TF = df[df["gender"]== "F"]
df_TM = df_TM.groupby(["year"],as_index=False)[["gender"]].count()
df_TF = df_TF.groupby(["year"],as_index=False)[["gender"]].count()
df_T = df_TM.merge(df_TF,how="left",left_index=True,right_index=True) #1
df_T = df_T.drop("year_y",axis=1)
df_T = df_T.rename(columns={"year_x":"year",
                        "gender_x":"Male",
                        "gender_y":"Female"})
df_T = df_T.set_index("year")

df_T.loc["Total"] = df_T.apply(lambda x:x.sum()) #Headcount
df_Tp = df_T.div(df_T.sum(axis=1),axis=0)


#2 2019/20 dataset by course and gender
df2 = pd.DataFrame((x.split(' ') for x in df['course']),columns=['course','B',"C"])
df2 = df2.merge(df,how="left",left_index=True,right_index=True)
df2 = df2.drop(["course_y","B","C"],axis=1)
df2 = df2.rename(columns={"course_x":"course"})
# To make the data keep the newest year
new_year = df2["year"].unique().tolist()
new_year.sort(reverse=True)
#
df2 = df2[df2["year"]== new_year[0] ]
df_CM = df2[df2["gender"]== "M"]
df_CF = df2[df2["gender"]== "F"]
df_CM = df_CM.groupby(["course"],as_index=False)[["gender"]].count()
df_CF = df_CF.groupby(["course"],as_index=False)[["gender"]].count()
df_CT = df_CM.merge(df_CF,how="left",left_index=True,right_index=True)
df_CT = df_CT.drop("course_y",axis=1)
df_CT = df_CT.rename(columns={"course_x":"course",
                        "gender_x":"Male",
                        "gender_y":"Female"})

df_CT = df_CT.set_index("course")
df_CTp = df_CT.div(df_CT.sum(axis=1),axis=0)


#############################################
#3 Percentage Growth by Course and Gender: 2019/20 vs 2018/19 (Comparing this year and last year automotically)
a = df[df["year"] == new_year[0]]
b = df[df["year"] == new_year[1]]
def upgrate_year(df3_1):
    df_3M = df3_1[df3_1["gender"]== "M"]
    df_3F = df3_1[df3_1["gender"]== "F"]
    df_3M = df_3M.groupby(["course"],as_index=True)[["gender"]].count()
    df_3F = df_3F.groupby(["course"],as_index=True)[["gender"]].count()
    df_3T = df_3M.merge(df_3F,how="left",left_index=True,right_index=True)
    df_3T = df_3T.rename(columns={"gender_x":"Male","gender_y":"Female"})
    return df_3T

df_a = upgrate_year(a) # This Year
df_b = upgrate_year(b) # Last Year
df3 = df_a.merge(df_b,how="left",left_index=True,right_index=True)
df3 = df3.fillna(value=0)
df3["neg_M"] = df3["Male_x"]-df3["Male_y"]
df3["neg_F"] = df3["Female_x"]-df3["Female_y"]
df3 = df3.abs() # take the absoulte number
df3["M_p"]= df3["Male_x"]/df3["neg_M"]
df3["F_p"]= df3["Female_x"]/df3["neg_F"]
# Need to be validated
##############################################
methods = ["by Headcount","by Proportion"]
genders = ["Male","Female"]
##################################################
dfl = df_T.reset_index()
dfl = dfl[dfl["year"]!="Total"]

trace7 = [go.Scatter(
           x=dfl["year"],
           y=dfl[i],
           mode="markers+lines",
           name=i
) for i in genders]

layout7 = go.Layout(title = "Total Undergraduate Students by Gender over Time",legend=dict(title=None,
            y=1.02, yanchor="bottom",
            x=1, xanchor="right",
            orientation="h",
            font=dict(size=10)))


UGo = dict(data=trace7,layout=layout7)



##################################################
# external_stylesheets = [dbc.themes.PULSE]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tab6 = dbc.Card(
       dbc.CardBody([
           html.Div([
      dbc.Container([
            dbc.Row([
                  dbc.Col(html.H1("WMG Student Data"),className="mb-2")
               ]),
            dbc.Row([
                  dbc.Col(dbc.Card(html.H3(children="Undergraduate | UG",className="text-center text-light bg-primary"),
                                                                     body=True,color="primary"),className="mb-4")
            ]),
            dbc.Row([
                  dbc.Col(html.H5("Total Undergraduate Students"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m7",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="UG")]), #graph4
            html.Hr(),
            dcc.Graph(id="UGo",figure=UGo),
            html.Hr(),
            dbc.Row([
                  dbc.Col(html.H5("WMG Undergraduate Course Demographic"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m8",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="UGC")])
            ])
      ])
   ])
)


@app.callback(Output("UG","figure"),
              [Input("c-m7","value")])

def ug_research(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_T
        n=None
    else:

        filter_df = df_Tp
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=filter_df.index,
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="Total Undergraduate Students "+selected_method,
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
    ug = dict(data=trace,layout=layout)

    return ug

@app.callback(Output("UGC","figure"),
              [Input("c-m8","value")])

def ug_UG(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_CT
        n=None
        a=None
    else:

        filter_df = df_CTp
        n="%"
        a="stack"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=filter_df.index,
            y=filter_df[i],
            name=i
            ) for i in yaxis]

    layout = go.Layout(title="The Undergraduate Course Demographic "+selected_method+" "+new_year[0],
                       margin=dict(l=50, r=50, b=105, t=70),
                       yaxis=dict(tickformat=n),
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=12)),
                       legend=dict(title=None,
                                       y=1.02, yanchor="bottom",
                                       x=1, xanchor="right",
                                       orientation="h"),
                                       font=dict(size=10),
                       barmode=a
                          #autosize=False,
                          #width=1240,
                          #height=350,
                       )
    ug = dict(data=trace,layout=layout)

    return ug

# if __name__ == "__main__":
     # app.run_server()
