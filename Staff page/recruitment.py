import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
from app import server
#Running it when testing the single page
# external_stylesheets = [dbc.themes.PULSE]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel("NEW Copy of Recruitment - gender - WMG.xlsx",header=[0,1])
############### change the datasetformet

df = df.fillna(value=0) #give value for empty cell
df["year"] = str(20)+df["Year"] #change year for mat e.g 14/15 to 2014/15
df = df.drop("Year",axis=1)
df = df.set_index("year")       #set index for preparing stack

df = df.rename(columns={"Grade":"ZGrade"})
df = df.stack(0)
df = df.fillna(method="bfill")
df = df.reset_index()
############### Keeping the Columns and Rows, which I need.
df = df.rename(columns={"year":"Year",
                        "level_1":"Gender",
                        "Unnamed: 1_level_1":"Type",
                        "Unnamed: 2_level_1":"Grade"})

df = df.groupby(["Year","Gender","Type","Grade"],as_index=False)[["Applied","Shortlisted","Offered"]].sum()
df = df.query('Gender == ["Female","Male","Total"]') #filter Gender I need
df = df.query('Grade  == ["Level 5","Level 6","Level 7","Level 8","Level 9","KTP","Other"]') # filter grade I need
df = df.replace({"Level 5":"FA 5","Level 6":"FA 6","Level 7":"FA 7","Level 8":"FA 8","Level 9":"FA 9"})
#Final Recruitment dataset
df = df.reset_index(drop=True)
#Final Recruitment dataset

#Overall data set
df_A = df.groupby(["Year","Gender","Grade"],as_index=False)[["Applied","Shortlisted","Offered"]].sum()
df_Ah = df_A.query('Gender == ["Female","Male"]')
df_Ah = df_Ah.set_index(["Year","Gender","Grade"],drop=True)
df_Ah = df_Ah.unstack(level=1)
df_Ah = df_Ah.stack(0)
df_Ah = df_Ah.reset_index()
df_Ah = df_Ah.rename(columns={"level_2":"Action"}) # Overallc Headcount data (1)

df_Ahp = df_Ah.set_index(["Year","Grade","Action"],drop=True)
df_Ahp = df_Ahp.astype(int)
df_Ahp = df_Ahp.div(df_Ahp.sum(axis=1),axis=0) # Overall protion
df_Ahp = df_Ahp.reset_index()

##### split acadmic and pss data
# academic dataset
df1 = df.query('Type == ["Academic - Research Focussed","Academic - Teaching & Research","Academic - Teaching Focussed","Academic"]')
df1 = df1.groupby(["Year","Gender","Grade"],as_index=False)[["Applied","Shortlisted","Offered"]].sum()
df_h = df1.query('Gender == ["Female","Male"]')

df_h = df_h.set_index(["Year","Gender","Grade"],drop=True)
df_h = df_h.unstack(level=1)
df_h = df_h.stack(0)
df_h = df_h.reset_index()
df_h = df_h.rename(columns={"level_2":"Action"}) # academic Headcount data (1)

df_hp = df_h.set_index(["Year","Grade","Action"],drop=True)
df_hp = df_hp.astype(int)
df_hp = df_hp.div(df_hp.sum(axis=1),axis=0) # academicl protion
df_hp = df_hp.reset_index()

# PSS dataset
df2 = df.query('Type == ["Professional & Support Staff"]')
df2 = df2.groupby(["Year","Gender","Grade"],as_index=False)[["Applied","Shortlisted","Offered"]].sum()
df_sh = df2.query('Gender == ["Female","Male"]') # PSS Headcount data (1)

df_sh = df_sh.set_index(["Year","Gender","Grade"],drop=True)
df_sh = df_sh.unstack(level=1)
df_sh = df_sh.stack(0)
df_sh = df_sh.reset_index()
df_sh = df_sh.rename(columns={"level_2":"Action"}) # academic Headcount data (1)

df_shp = df_sh.set_index(["Year","Grade","Action"],drop=True)
df_shp = df_shp.astype(int)
df_shp = df_shp.div(df_shp.sum(axis=1),axis=0) # Overall protion
df_shp = df_shp.reset_index()

################## Creat Academic dataset By Proportion -def an function to deal with data


########################################################################################################################### data cleaning


year_options = df_Ah["Year"].unique().tolist()
year_options.sort(reverse=True)
method_options = ["by Headcount","by Proportion"]
vacancy_options =["Overall","Academic","Professional & Support Staff"]

layout=html.Div([
      dbc.Container([

            dbc.Row([
                dbc.Col(html.H1("Key Career Transition Points: Academic and Professional Staff"),className="mb-2")
                     ]),

            dbc.Row([
                 dbc.Col(dbc.Card(html.H5(children="Recruitment",
                                          className="text-center text-light bg-primary"), body=True, color="primary")
                                                        , className="mb-4")
                     ]),
            dbc.Row([
                 dbc.Col(html.H5("Applications, shortlisting, and offer rates by grade and gender"),className="mb-4")
             ]),

            html.Div([
                    html.Label("◆ Select vacancy type:"),
                    dcc.Dropdown(
                    id="vacancy-picker",
                    options=[dict(label=i,value=i) for i in vacancy_options],
                    value="Overall"
                    )],style=dict(display="inline-block",verticalAlign="top",width="30%")),
            html.Div([
                    html.Label("◆ Select year:"),
                    dcc.Dropdown(
                    id="year-picker",
                    options=[dict(label=i,value=i) for i in year_options],
                    value="2018/19"
                    )],style=dict(display="inline-block",verticalAlign="top",width="30%")),
            html.Div([
                    html.Label("◆ Select caculated method:"),
                    dcc.Dropdown(
                    id="method-picker",
                    options=[dict(label=i,value=i) for i in method_options],
                    value="by Headcount"),
                    ],style=dict(display="inline-block",verticalAlign="top",width="30%")),
            dcc.Graph(id="recruitment")
                    ])
                    ])

@app.callback(Output("recruitment","figure"),
              [Input("vacancy-picker","value"),
               Input("year-picker","value"),
               Input("method-picker","value")])

def recruitment_updated(select_van,select_year,select_met):

      if select_van == "Academic":

          if select_met == "by Headcount":
            filter_df = df_h
            i = None
            n = "Headcount of "
            s = None
          else:
            filter_df = df_hp
            i = "%"
            n = "Proportion of "
            s = "stack"

      elif select_van == "Overall":

          if select_met == "by Headcount":
            filter_df = df_Ah
            i = None
            n = "Headcount of "
            s = None
          else:
            filter_df = df_Ahp
            i = "%"
            n = "Proportion of "
            s = "stack"

      else:

          if select_met == "by Headcount":
            filter_df = df_sh
            i = None
            n = "Headcount of "
            s = None
          else:
            filter_df = df_shp
            i = "%"
            n = "Proportion of "
            s = "stack"

      filter_df2 = filter_df[filter_df["Year"]==select_year]

      yaxis = ["Male","Female"]

      trace = [go.Bar(
                 x=[filter_df2["Action"],filter_df2["Grade"]],
                 y= filter_df2[i],
                 name=n+i)
                 for i in yaxis
                 ]

      layout = go.Layout(title=select_year+" Applied,Shortlisted,Offered "+select_met+" ("+select_van+")",
                       xaxis=dict(tickfont=dict(size=10)),
                       yaxis=dict(tickformat=i),
                       legend=dict(title=None,
                                   y=1.02, yanchor="bottom",
                                   x=1, xanchor="right",
                                   orientation="h"),
                                   font=dict(size=10),
                       barmode=s,
                       )

      fig = dict(data=trace,layout=layout)

      return fig

# if __name__ == "__main__":
    # app.run_server()
