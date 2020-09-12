import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
from app import server
from PT import tab4
from PR import tab5
from UG import tab6
# The fist Graph - transform dataset
df_b = pd.read_excel("enrolment.xlsx")
df_b = df_b.set_index(["Year","Gender"],drop=True)
df_b = df_b.unstack(level=1)
df_b = df_b.stack(level=0)
df_b = df_b.reset_index()
df_b = df_b.rename(columns={"level_1":"action"})
df_bt = df_b.groupby(["action"],as_index=False)[["Male","Female"]].sum()
df_bt["Year"] = "Total"
df_b = pd.concat([df_b,df_bt]) #I headcount
#give the label order
df_b = df_b.replace({"Applications":"1.Applications","Offers":"2.Offers","Acceptances":"3.Acceptances","Registered":"4.Registered","Total":"5.Total"})
df_b = df_b.sort_values(["action","Year"])

df_bp = df_b.set_index(["Year","action"])
df_bp = df_bp.div(df_bp.sum(axis=1),axis=0)
df_bp = df_bp.reset_index()
################# Read Data - FTMSC ####################
df_a = pd.read_excel("student.xlsx",sheet_name="FTMSC")
#The course graph
df_c = df_a.drop(["Centre","SPR_CODE","SCJ_STAC","WD-reason","PRG_CODE","MOA_CODE","award","Grade"],axis=1)
df_c = df_c.rename(columns={"SPR_GEND":"gender",
                        "SPR_AYRS":"year",
                        "Acronym":"course"})
df_cf = df_c[df_c["gender"]=="F"]
df_cm = df_c[df_c["gender"]=="M"]
df_cf = df_cf.groupby(["year","course"],as_index=True)[["gender"]].count()
df_cm = df_cm.groupby(["year","course"],as_index=True)[["gender"]].count()
df_c = df_cm.merge(df_cf,how="left",left_index=True,right_index=True)
df_c = df_c.rename(columns={"gender_x":"Male","gender_y":"Female"})
df_c = df_c.fillna(value=0)
# Proportion
df_cp = df_c.div(df_c.sum(axis=1),axis=0)
df_cp = df_cp.drop("Male",axis=1)
df_cp = df_cp.unstack(level=0)
df_cp = df_cp.drop("SCLM DA",axis=0)
df_cp = df_cp.stack(level=0)
df_cp = df_cp.reset_index()
df_cp = df_cp.drop("level_1",axis=1)
df_cp = df_cp.fillna(value=0) #9

# headcount
df_ch = df_c.drop("Male",axis=1)
df_ch = df_ch.unstack(level=0)
df_ch = df_ch.drop("SCLM DA",axis=0)
df_ch = df_ch.stack(level=0)
df_ch = df_ch.reset_index()
df_ch = df_ch.drop("level_1",axis=1)
df_ch = df_ch.fillna(value=0) #9

#Other dataframe Base on "award" and "grade"
#drop columns that do not be needed
df_a = df_a.drop(["Centre","Acronym","SPR_CODE","SCJ_STAC","WD-reason","PRG_CODE","MOA_CODE"],axis=1)

df_a = df_a.rename(columns={"SPR_GEND":"gender",
                        "SPR_AYRS":"year",
                        "Grade":"grade"})
#data cleaning
#chosse the data that are needed
df_a = df_a.query('gender == ["M","F"]')
df_a["award"] = df_a["award"].fillna(value="Fail")
df = df_a.query('award == ["MSC","Fail"]')
#chosse the null in grade columns and fill the nan based on the award column
df.loc[df['grade'].isnull(),'grade']=df.award.apply(lambda x:"2.Pass" if "MSC" in x else "1.Fail")
df = df.drop("award",axis=1)

#caculate grade by gender - female
df_f = df[df["gender"]=="F"]
df_f = df_f.groupby(["year","grade"],as_index=False)[["gender"]].count()
#caculate grade by gender - male
df_m = df[df["gender"]=="M"]
df_m = df_m.groupby(["year","grade"],as_index=False)[["gender"]].count()
df_m = df_m.drop(["year","grade"],axis=1)
#final dataset
df = df_f.merge(df_m,how="left",left_index=True,right_index=True)
df = df.rename(columns={"gender_x":"Female","gender_y":"Male"})
df = df.replace({"Merit":"3.Merit","Distinction":"4.Distinction"})

#1. FTMSc Degree Awards by Year and Gender data set
df = df.sort_values(by=["grade"]) #1

#2. Total Students by Year and Gender、Total Students by Gender over Time
df_T = df.groupby(["year"],as_index=False)[["Female","Male"]].sum()
df_T = df_T.set_index("year")
df_T.loc["Total"] =df_T.apply(lambda x:x.sum()) #- dataset #2
df_TL = df_T[df_T.index != "Total"] #- dataset #3

################
# To make the data keep the newest year
new_year = df["year"].unique().tolist()
new_year.sort(reverse=True)

#3. total grade  Proportion
dfp = df[df["year"] != new_year[0]  ]
dfp = dfp.groupby("grade",as_index=False)[["Female","Male"]].sum()
dfp = dfp.set_index("grade") #headcount
dfpp = dfp.div(dfp.sum(axis=0),axis=1) # dataset #4、#5


#4.Total pass or higher dataset #6
df_P = df[df["grade"] != "1.Fail"]
df_P = df_P.groupby(["year"],as_index=False)[["Female","Male"]].sum()
df_P = df_P.set_index("year")
df_P.loc["Total"] =df_P.apply(lambda x:x.sum())
df_PP = df_P.div(df_P.sum(axis=1),axis=0) # Proportion

#Totall Merit or higher dataset #7
df_hP = df.query('grade == ["3.Merit","4.Distinction"]')
df_hP = df_hP.groupby(["year"],as_index=False)[["Female","Male"]].sum()
df_hP = df_hP.set_index("year")
df_hP.loc["Total"] =df_hP.apply(lambda x:x.sum())
df_hPP = df_hP.div(df_hP.sum(axis=1),axis=0) #Proportion

# WMG FT registered/completion rates by degree #8
df2 = df_a[df_a["award"] != "Fail"]
df2_f = df2[df2["gender"]=="F"]
df2_f = df2_f.groupby(["year","award"],as_index=True)[["gender"]].count()

#caculate grade by gender - male
df2_m = df2[df2["gender"]=="M"]
df2_m = df2_m.groupby(["year","award"],as_index=True)[["gender"]].count()

#dataset #8
df2 = df2_m.merge(df2_f,how="left",left_index=True,right_index=True)
df2 = df2.rename(columns={"gender_x":"Male","gender_y":"Female"})
df2 = df2.fillna(value=0)
df2 = df2.reset_index()

# caculate total by award
df2t = df2.groupby(["award"],as_index=False)[["Male","Female"]].sum()
df2t["year"] = "Total"
#8. By headcount
df2 = pd.concat([df2,df2t])#
#8. by Proportion
df2 = df2.set_index(["year","award"],drop=True)
df2p = df2.div(df2.sum(axis=1),axis=0)
df2p = df2p.reset_index() #
#8. overall
df2 = df2.reset_index()
df_o = df2.groupby("year",as_index=True)[["Male","Female"]].sum()  #by headcount
df_op =  df_o.div(df_o.sum(axis=1),axis=0) #by Proportion


#####################################################
#################### creating graph #############################################
methods = ["by Headcount","by Proportion"]
course_options = df_cp["course"].unique().tolist()
genders = ["Male","Female"]

# FT MSc course demographic change with the year by gender #graph2
df_bo = df_b[df_b["Year"] != "5.Total"]
df_bo = df_bo[df_bo["action"] == "4.Registered"]
trace =  [go.Scatter(
               x=df_bo["Year"],
               y=df_bo[i],
               mode="markers+lines",
               name=i
) for i in genders]

layout0 = go.Layout(title = "Total Students by Gender over Time",legend=dict(title=None,
            y=1.02, yanchor="bottom",
            x=1, xanchor="right",
            orientation="h",
            font=dict(size=10)))


ftd2 = dict(data=trace,layout=layout0)
############################################################################
#Over all
trace4 =  [go.Bar(
               x=df_op.index,
               y=df_op[i],
               name=i
) for i in genders]

layout4 = go.Layout(title = dict(text="WMG FT registered/completion rate by degree (Overall)",
                                font=dict(size=16)),
                    yaxis = dict(tickformat="%")
                             )


ftro = dict(data=trace4,layout=layout4)
################################################################################
dfta= df[df["year"]!= new_year[0]]
trace2 =  [go.Bar(
               x=[dfta["year"],dfta["grade"]],
               y=dfta[i],
               name=i
) for i in genders]

layout2 = go.Layout(title =dict(text="FTMSc Degree Awards by Year and Gender",
                                font=dict(size=16)),
                    legend=dict(title=None,
                    y=1.02, yanchor="bottom",
                    x=1, xanchor="right",
                    orientation="h",
                    font=dict(size=10)))


fta = dict(data=trace2,layout=layout2)
############################################
#Funnel figure
dfp = dfp.reset_index()
trace3 = [go.Funnel(
                 y=dfp["grade"],
                 x=dfp[i],
                 name=i,
                 orientation = "h",
                 textposition = "inside",
                 textinfo = "value+percent total",
                 ) for i in genders]

layout3=go.Layout(title = "Percentage of Degree Classifications by gender",
                  legend=dict(title=None,
                  y=1.02, yanchor="bottom",
                  x=1, xanchor="right",
                  orientation="h",
                  font=dict(size=10))
                  )


ftgf = dict(data=trace3,layout=layout3)
#####################################################################
#Side bar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 100,
    "left": 0,
    "bottom": 10,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem ",
}

sidebar = html.Div([
dbc.Container
  ([
        html.P("FTMSc Fast Navigation"),
        dbc.Nav(
            [
                 dbc.NavItem(html.A("➤ Course Demographic", href="#one", id="1")),
                 html.P(" "),
                 dbc.NavItem(html.A("➤ Course Demographic change with the year by gender", href="#two", id="2")),
                 html.P(" "),
                 dbc.NavItem(html.A("➤ Average of Female by Course and Year", href="#three", id="3")),
                 html.P(" "),
                 dbc.NavItem(html.A("➤ Registered/Completion by Degree", href="#four", id="4")),
                 html.P(" "),
                 dbc.NavItem(html.A("➤ Degree Awards by Year and Gender", href="#five", id="5")),
                 html.P(" "),
                 dbc.NavItem(html.A("➤ Percentage of Degree Classifications Total", href="#six", id="6")),
                 html.P(" "),
                 dbc.NavItem(html.A("➤ Percentage of Student Grades", href="#seven", id="7")),
                 # html.P(" "),
                 dbc.NavItem(html.A("Back to Top", href="#Top", id="top"))
            ],
            vertical=True,
            pills=True,
        )

  ]
  )
],
style=SIDEBAR_STYLE)

############################################
# external_stylesheets = [dbc.themes.PULSE]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tab3 = dbc.Card(
       dbc.CardBody([
   html.Div([
      dbc.Container([
            dbc.Row([
                  dbc.Col(html.H1("WMG Student Data"),className="mb-2")
               ]),
            html.A(id="one"),
            dbc.Row([
                  dbc.Col(dbc.Card(html.H3(children="Full Time Master of Science | FTMSc",className="text-center text-light bg-primary"),
                                                                     body=True,color="primary"),className="mb-4")
            ]),
            dbc.Row([
                  dbc.Col(html.H5("WMG FTMSc Course Demographic"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m1",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="demographic")], #graph1
            style=dict(height=470)
            ),
            html.A(id="two"),
            html.Hr(),
            dbc.Row([
                  dbc.Col(html.H5("WMG FT MSc Course Demographic change with the year by gender"),className="mb-4")
            ]),
            dcc.Graph(id="linechart1",figure=ftd2), #graph2
            html.A(id="three"),
            html.Hr(),

            dbc.Row([
                  dbc.Col(html.H5("FTMSc Average of Female by Course and Year"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m2",
            options=[dict(label=i,value=i) for i in methods],
            value="by Proportion"
            ),
            dcc.Graph(id="course"), #graph3
            html.A(id="four"),
            html.Hr(),
            dbc.Row([
                  dbc.Col(html.H5("WMG FTMSC Registered/Completion by degree"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m3",
            options=[dict(label=i,value=i) for i in methods],
            value="by Headcount"
            ),
            html.Div([
            dcc.Graph(id="completion rates")]), #graph4
            dcc.Graph(id="ftro",figure=ftro),
            html.A(id="five"),
            dbc.Row([
                  dbc.Col(dbc.Card(html.H3(children="FTMSc Student Learning Status",className="text-center text-light bg-primary"),
                                                                     body=True,color="primary"),className="mb-4")
                                                                     ]),

            dbc.Row([
                  dbc.Col(html.H5("FTMSc Degree Awards by Year and Gender"),className="mb-4")
            ]),
            dcc.Graph(id="grade",figure=fta),
            html.A(id="six"),
            html.Hr(),
            dbc.Row([
                  dbc.Col(html.H5("Percentage of Degree Classifications"),className="mb-4")
            ]),
            dcc.Graph(id="grade-F",figure=ftgf),
            html.A(id="seven"),
            html.Hr(),
            dbc.Row([
                  dbc.Col(html.H5("Percentage of Student Grades"),className="mb-4")
            ]),
            html.Label("◆ Select the calculated method:"),
            dcc.Dropdown(
            id="c-m4",
            options=[dict(label=i,value=i) for i in methods],
            value="by Proportion"),
            dbc.Row([
                 dbc.Col([
                 dcc.Graph(id="pass")
                 ],width=6),
                 dbc.Col([
                 dcc.Graph(id="merit")
                 ],width=6)


            ])

   ])
   ,sidebar
],style=CONTENT_STYLE)
])
)

tabs2 = html.Div([html.A(id="Top"),
          dbc.Tabs(
              [
                 dbc.Tab(tab3, label="➤ FT MSc",tabClassName="ml-auto",style={"top":260}),
                 dbc.Tab(tab4, label="➤ PT MSc"),
                 dbc.Tab(tab5, label="➤ PGR and PhD"),
                 dbc.Tab(tab6, label="➤ Undergraduate")
              ])
                ])


layout=html.Div(tabs2)



@app.callback(Output("demographic","figure"),
              [Input("c-m1","value")])

def demographic(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_b
        n=None
    else:

        filter_df = df_bp
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=[filter_df["Year"],filter_df["action"]],
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="FTMSc Enrolment "+selected_method,
                       margin=dict(l=30, r=30, b=105, t=70),
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
    ftd1 = dict(data=trace,layout=layout)

    return ftd1

@app.callback(Output("completion rates","figure"),
              [Input("c-m3","value")])

def completion(selected_method):

    if selected_method == "by Headcount":

        filter_df = df2
        n=None
    else:

        filter_df = df2p
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=[filter_df["year"],filter_df["award"]],
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="WMG FT Registered/Completion with degrees "+selected_method,
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
    ftc = dict(data=trace,layout=layout)

    return ftc

@app.callback(Output("course","figure"),
              [Input("c-m2","value")])

def select_course(selected_method):


    if selected_method == "by Headcount":

        filter_df = df_ch
        n=None


    else:

        filter_df = df_cp
        n="%"

    year= df_ch.columns.tolist()
    year.pop(0)
    data = [go.Bar(
    x=filter_df["course"],
    y=filter_df[i],
    name=i,
    #marker_color="rgb(31,119,180)"
    ) for i in year]



    layout = go.Layout(title=dict(text="Average of % Female by Course and Year",
                            y=0.9,
                            x=0.5,
                            xanchor="center",
                            yanchor="top"),
                            legend=dict(title=None,
                                        y=1.02, yanchor="bottom",
                                        x=1, xanchor="right",
                                        orientation="h"),
                            #showlegend=False,
                            font=dict(size=10),
                            yaxis=dict(nticks=10)
                            )


    figc = dict(data=data, layout=layout)

    return figc

@app.callback(Output("pass","figure"),
              [Input("c-m4","value")])

def grade(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_P
        n=None
    else:

        filter_df = df_PP
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=filter_df.index,
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="Percentage of Students Pass<br>or Higher by Year and Gender "+selected_method,
                       #margin=dict(l=50, r=50, b=105, t=70),
                       yaxis=dict(tickformat=n),
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=10))
                       )
    psp = dict(data=trace,layout=layout)

    return psp


@app.callback(Output("merit","figure"),
              [Input("c-m4","value")])

def grade_2(selected_method):

    if selected_method == "by Headcount":

        filter_df = df_hP
        n=None
    else:

        filter_df = df_hPP
        n="%"

    yaxis = ["Male","Female"]
    trace = [go.Bar(
            x=filter_df.index,
            y=filter_df[i],
            name=i) for i in yaxis]

    layout = go.Layout(title="Percentage of Students Merit<br>or Higher by Year and Gender "+selected_method,
                       #margin=dict(l=50, r=50, b=105, t=70),
                       yaxis=dict(tickformat=n),
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=10))
                       )
    hsp = dict(data=trace,layout=layout)

    return hsp


# if __name__ == "__main__":
     # app.run_server()
