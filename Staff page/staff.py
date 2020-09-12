#import the module that I need
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
#import dataframe from
from staff_1 import fig
import dash_table
from leaver_1 import table_Ay,table_Sy,table_ovr_y,table_Sa,table_ovr_a,table_Aa,join_df3,join_df3A,join_df3S,join_df2,join_df2A,join_df2S
from leaver_2 import df3_T,df3A,df3S
from app import app


#Running it when testing the single page
# external_stylesheets = [dbc.themes.PULSE]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read data
df = pd.read_excel("4.2(ii)- ftc vs oec - all staff - WMG.xlsx",header=[0,1])
###################### changing data that can be read by dash
df = df.rename(columns={"Unnamed: 0_level_0":"WMG",
                        "Unnamed: 1_level_0":"function","Unnamed: 1_level_1":"function2",
                        "Unnamed: 2_level_0":"grade1","Unnamed: 2_level_1":"grade2"})
df = df.replace({"Research Only":"2.Research Only", #give oder for label
                 "Support and Professional Staff":"4.Support and Professional Staff",
                 "Teaching Only":"3.Teaching Only",
                 "Teaching and Research":"1.Teaching and Research"
                    })

df = df.drop(["WMG"],axis=1)
df["type"] = df["function"] # rebuilding the "function column" to make filter function work
df = df.drop("function",axis=1)
df = df.set_index("type")
df = df.stack(0)
df = df.fillna(method="bfill")
df = df.reset_index()
df = df.rename(columns={"level_1":"year",
                        "grade2":"grade",
                        "type":"function"
                         })
df = df[df["year"] != "grade1"]
df = df.query('grade == ["FA 5","FA 6","FA 7","FA 8","FA 9","NON FA GRADE"]')
#############################################################################################
df1 = df.groupby(["year","function"],as_index=False)[["Male FTC headcount","Female FTC headcount"]].sum()
df1a= df1[df1["function"] != "4.Support and Professional Staff"] #academic data FTC
df1s= df1[df1["function"] == "4.Support and Professional Staff"] #PSS data FTC
df2 = df.groupby(["year","function"],as_index=False)[["Male OEC headcount","Female OEC headcount"]].sum()
df2a= df2[df2["function"] != "4.Support and Professional Staff"] #academic data FTC
df2s= df2[df2["function"] == "4.Support and Professional Staff"] #PSS data FTC
df2["year"] = df2["year"].astype(int)
#############################################################################################

type_options = ["Fix Term Contract (FTC)","Open Ended Contract (OEC)"] #Dropdown options list
function_options = ["Overall","Academic","Support and Professional Staff"]
#Creating year options - which grab the data in the year columns
year_options=df2["year"].unique().tolist()
year_options.sort(reverse=True)
year_options.insert(0,"ALL")
new_year = 2014+len(year_options)-2

#Creating function year_options
function_options2=["Overall","Academic","Professional & Support Staff"]
#Creating function reason_options
function_options3 = ["Overall","Academic","Professional and Support Staff"]
# df3_T.reason.str.replace("<br>","")

reason_options=df3_T["reason"].unique().tolist()

vale=["Redundancy, FTC","better job prospects","Retirement(Normal)","Other non-work<br>related reason",
      "Other work<br>related reason","Relocating","Resignation<br>(no reason given)"]


tab1= dbc.Card(dbc.CardBody([
        html.Div([
        dbc.Container([
             dbc.Row([
                dbc.Col(html.H1("Academic and Professional Staff Data"),className="mb-2")
                     ]),
             dbc.Row([
                 dbc.Col(dbc.Card(html.H5(children="All Staff by grade on fixed-term, open-ended/permanent and zero-hour contracts by gender",
                                          className="text-center text-light bg-primary"), body=True, color="primary")
                                                        , className="mb-4")
                     ]),
             dbc.Row([
                 dbc.Col(html.H5("All staff headcount by role and gender"),className="mb-4")
             ]),
        html.Div([
        html.Label("◆ Select contract type:"),
        dcc.Dropdown(
             id="contry-picker",
             options=[dict(label=i,value=i) for i in type_options],
             value="Fix Term Contract (FTC)",
             #style=dict(width="80%")
             )] , style=dict(display="inline-block",verticalAlign="top",width="30%",marginLeft="3px")
                 ),
         html.Div([
         html.Label("◆ Select function type:"),
         dcc.Dropdown(
             id="function-picker",
             options=[dict(label=i,value=i) for i in function_options],
             value="Overall",
             #style=dict(width="80%")
             )], style=dict(display="inline-block",verticalAlign="top",width="30%",marginLeft="5px")
                 ),
         dcc.Graph(id="AFB"),
         html.Hr(),
         dbc.Row([
             dbc.Col(html.H5("Headcount for FTC and OEC by grade by proportion"),className="mb-4")
         ]),
         dcc.Graph(id="by protion",figure=fig)

         ])
         ])
         ])
         )

tab2= dbc.Card(
        dbc.CardBody([
        html.Div([
        dbc.Container([
              dbc.Row([
                 dbc.Col(html.H1("Academic and Professional Staff Data"),className="mb-2")
                      ]),

             dbc.Row([
                 dbc.Col(dbc.Card(html.H3(children="All leavers by grade and gender and full/part-time status",
                                          className="text-center text-light bg-primary"), body=True, color="primary")
                                                        , className="mb-4")
                     ]),

             dbc.Row([
                 dbc.Col(html.H5(children="All leavers by function and FT/PT status 2014-"+str(new_year)
                                 ),className="mb-4")
             ]),
         html.Div([
         html.Label("◆ Select year:"),
         dcc.Dropdown(
             id="year-picker",
             options=[dict(label=str(i),value=i) for i in year_options],
             value="ALL")
             ], style=dict(display="inline-block",verticalAlign="top",width="30%",marginLeft="5px")),
          html.Div([
          html.Label("◆ Select function type:"),
          dcc.Dropdown(
             id="function-picker2",
             options=[dict(label=i,value=i) for i in function_options2],
             value="Overall")
             ], style=dict(display="inline-block",verticalAlign="top",width="30%",marginLeft="5px")),
          html.Div([
          dcc.Graph(id="leaver")],style=dict(height=425,marginLeft="-60px")),
          dash_table.DataTable(
             id='table',
             style_cell=dict(
             textAlign="left",
             minWidth = '40px', width = '40px', maxWidth = '40px'),
             style_cell_conditional=[
             {"if":dict(column_id="Gender"),"width":"75px"},
             {"if":dict(column_id="Non FA grade"),"width":"90px"}]
             ),
          dbc.Row(dbc.Col(html.H3(""))),
          dbc.Row(dbc.Col(html.H3(""))),
          dbc.Row(dbc.Col(html.H3(""))),
          html.Hr(),
          dbc.Row([
            dbc.Col(html.H5(children="All leavers by reason over the period 2014-"+str(new_year)+", headcount"
                            ),className="mb-4")
            ]),
          html.Label("Select function type"),
          dcc.Dropdown(
          id="function-picker3",
          options=[dict(label=str(i),value=i) for i in function_options3],
          value="Overall"
          ),
          html.Label("◆ Select leaving Reasons:"),
          dcc.Dropdown(
             id="reason",
             options=[dict(label=str(i),value=i) for i in reason_options],
             value=vale,
             multi=True),
          html.Div([
          html.Label("*Orange: Numbers of female leavers",style={"fontsize":50,"color":"rgb(255,127,14)"}),
          html.Label("  *Blue: Numbers of male leavers",style={"fontsize":80,"color":"rgb(31,119,180)"})
             ]),#style={"marginLeft":"6%"}),
          html.Div([
          dcc.Graph(id="leaver2")],style=dict(marginLeft="-60px"))
             ])
             ])
             ])
             )

tabs = html.Div([
dbc.Tabs(
    [
        dbc.Tab(tab1, label="➤ Fixed-term,Open-ended/permanent and zero-hour contracts by gender"),
        dbc.Tab(tab2, label="➤ All leavers by grade and gender and full/part-time status"),
    ]
)])


layout=html.Div(tabs)

@app.callback(Output("AFB","figure"),
              [Input("contry-picker","value"),
               Input("function-picker","value")])

def update_ABFBARchart(selected_type,selected_function):

    if selected_type == "Fix Term Contract (FTC)":

        yaxis = ["Male FTC headcount","Female FTC headcount"]

        if selected_function == "Overall":

            filtered_df = df1

        elif selected_function == "Academic":

            filtered_df = df1a

        else:

            filtered_df = df1s

    else:

        yaxis = ["Male OEC headcount","Female OEC headcount"]

        if selected_function == "Overall":

            filtered_df = df2

        elif selected_function == "Academic":

            filtered_df = df2a

        else:

            filtered_df = df2s


    trace = [go.Bar(

         x=[filtered_df["function"],filtered_df["year"]],
         y=filtered_df[i],
         name=i,
         hovertext=i,
         ) for i in yaxis]


    layout = go.Layout(title=str(selected_type)+" Headcount",
                       barmode="stack",
                       legend=dict(title=None,
                                   y=1.02, yanchor="bottom",
                                   x=1, xanchor="right",
                                   orientation="h"),
                       yaxis=dict(nticks=10))

    fig = dict(data=trace, layout=layout)

    return fig

@app.callback(Output("leaver","figure"),
              [Input("year-picker","value"),
               Input("function-picker2","value")])

def leaver_upgraded(selected_year,selected_function):

    if selected_year == "ALL":

         if selected_function == "Overall":

             filter_df = join_df3

             n="All"

         elif selected_function == "Academic":

             filter_df = join_df3A

             n="Academic"

         else :

             filter_df = join_df3S

             n="Professional"

    else:
          if selected_function == "Overall":

              filter_df = join_df2[join_df2["year"]==selected_year]

              n="All"

          elif selected_function == "Academic":

              filter_df = join_df2A[join_df2A["year"]==selected_year]

              n="Academic"

          else:

              filter_df = join_df2S[join_df2S["year"]==selected_year]

              n="Professional"



    yaxis=["Male FT","Female FT","Male PT","Female PT"]

    trace = [go.Bar(
         x=[filter_df["function"],filter_df["grade"]],
         y=filter_df[i],
         name=i)
         for i in yaxis]

    layout = go.Layout(title=n+" leavers by job function and FT/PT status "+ str(selected_year),
                       barmode="stack",
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=10)),
                       yaxis=dict(nticks=10),
                       legend=dict(title=None,
                                   y=1.02, yanchor="bottom",
                                   x=1, xanchor="right",
                                   orientation="h"),
                                   font=dict(size=10),
                       autosize=False,
                       width=1240,
                       height=400
                       )

    fig3 = dict(data=trace, layout=layout)

    return fig3

@app.callback([Output("table","data"),
               Output("table","columns")],
              [Input("year-picker","value"),
               Input("function-picker2","value")])

def table_upgraded(selected_year,selected_function):

    if selected_year == "ALL":

         if selected_function == "Overall":

             filter_df = table_ovr_a

         elif selected_function == "Academic":

             filter_df = table_Aa

         else :

             filter_df = table_Sa

    else:
          if selected_function == "Overall":

              filter_df = table_ovr_y[table_ovr_y["year"]==selected_year]

          elif selected_function == "Academic":

              filter_df = table_Ay[table_Ay["year"]==selected_year]

          else:

              filter_df = table_Sy[table_Sy["year"]==selected_year]


    columns=[dict(name=i,id=i) for i in filter_df.columns]

    data=filter_df.to_dict("records")

    return  data,columns

@app.callback(Output("leaver2","figure"),
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

     layout = go.Layout(title=dict(text="Leavers by reason over the period 2014-"+str(new_year)+" headcount",
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

# if __name__ == "__main__":
    # app.run_server()
