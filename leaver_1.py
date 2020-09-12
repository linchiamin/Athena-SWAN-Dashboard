import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import dash_table
import pandas as pd
from numpy.random import randint
df = pd.read_excel("4.2(iii) - leavers with reason - all staff - by contract function FT_PT and grade - WMG.xlsx",header=[0,1,2])

# Data Cleaning
# Rename no name columns
df = df.rename(columns={"Unnamed: 0_level_0":"WMG","Unnamed: 0_level_1":"WMG1","Unnamed: 0_level_2":"WMG2",
                        "Unnamed: 1_level_0":"type","Unnamed: 1_level_1":"function2","Unnamed: 1_level_2":"function3",
                        "Unnamed: 2_level_0":"zgrade","Unnamed: 2_level_1":"zgrade2","Unnamed: 2_level_2":"zgrade3",
                        "Unnamed: 3_level_0":"zreason","Unnamed: 3_level_1":"zreason2","Unnamed: 3_level_2":"zreason3"})
# fill the empty cell
df = df.fillna(value=0)
########### chaing the format that can be read by plotly dash
df = df.drop("WMG",axis=1)
# rebuilding the "function column" to make filter function work
df["function"] = df["type"]
df = df.drop("type",axis=1)
df = df.set_index("function")
# building the dash graph dataset
df = df.stack(0)
df = df.stack()
df = df.fillna(method="bfill")
df = df.reset_index()
df = df.rename(columns={"level_1":"year",
                        "level_2":"contract",
                        "zgrade2":"grade",
                        "zreason2":"reason"})
############## filter the data I need

df = df[df["year"] != "zgrade"]
df = df[df["year"] != "zreason"]

# The Finally standard dataset that can be read by dash
df = df.groupby(["year","contract","function","grade","reason"],as_index=False)[["No. of male leavers","No. of female leavers"]].sum()


# chose the grade 5 to 9 and non FA grade
df2 = df.query('grade  == ["FA 5","FA 6","FA 7","FA 8","FA 9","Non FA grade"]')
df2["year"] = df2["year"].astype(int) #changing data type so that can be filtered
############################################
# starting build graph dataset
df2 = df2.groupby(["year","contract","function","grade"],as_index=False)[["No. of male leavers","No. of female leavers"]].sum()
a = df2[df2["contract"]=="FT"]
b = df2[df2["contract"]=="PT"]
a = a.rename(columns={"No. of male leavers":"Male FT","No. of female leavers":"Female FT"})
b = b.rename(columns={"No. of male leavers":"Male PT","No. of female leavers":"Female PT"})
a = a.drop(["contract"],axis=1)
b = b.drop(["year","contract","function","grade"],axis=1)
a = a.reset_index(drop=True) #reset order
b = b.reset_index(drop=True)
a = a.reset_index()  #add new column "index"
b = b.reset_index()
join_df2 = a.merge(b,how="left",left_on="index",right_on="index") #"merger two dataset by index"
join_df3 = join_df2.groupby(["function","grade"],as_index=False)[["Male FT","Female FT","Male PT","Female PT"]].sum()
###############################################################################
#Academic data - By year
join_df2A = join_df2[join_df2["function"]!= "Professional and Support Staff"]
join_df2A = join_df2A.drop("index",axis=1)

#add new row "FA 8" for each each research only, which is to keep the x label with correct oreder
rows = pd.DataFrame(columns=["year","function","grade","Male FT","Female FT","Male PT","Female PT"])
rows_num = len(join_df2A["year"].unique().tolist()) #caculate the how many "rows" and "year"need to be add by data frame inormation
for i in range(rows_num):
    rows.loc[i] = [2014+i,"Research Only","FA 8"]+list(randint(1, size=4))
# changing the new row data frame type - int
gender = ["year","Male FT","Female FT","Male PT","Female PT"]
for i in gender:
    rows[i] = rows[i].astype(int)
join_df2A = pd.concat([join_df2A,rows])
join_df2A = join_df2A.reset_index()
join_df2A = join_df2A.sort_values(["year","function","grade"]) #Academic data - By year

#PSS data - By year
join_df2S = join_df2[join_df2["function"] == "Professional and Support Staff"] #PSS data - By year
#Academic data - all year
join_df3A = join_df3[join_df3["function"]!= "Professional and Support Staff"]
#add new row "FA 8" for each each research only, which is to keep the x label with correct oreder
join_df3A.loc[15]=["Research Only","FA 8",0,0,0,0]
join_df3A = join_df3A.sort_values(["function","grade"])
#pss data = all year
join_df3S = join_df3[join_df3["function"] == "Professional and Support Staff"] #pss data = all year
################################################################################
############################# Building table data set ##########################
#### Creating a function to deal with the same format data
#year Table data function

def data_deal_by_year (data):
       a = data.set_index(["year","grade","function"],drop=True)
       a = a.drop("index",axis=1)
       a = a.unstack(level=2)
       a = a.unstack(level=1)
       a = a.stack(0)
       a = a.dropna(axis=1,how="all")
       a = a.droplevel("function",axis=1)
       a = a.reset_index()
       a = a.rename(columns={"level_1":"gender"})
    #sorting a for matching graph
       a = a.replace({"Male FT":"4.Male FT","Female FT":"3.Female FT",
                                 "Male PT":"2.Male PT","Female PT":"1.Female PT"})
       a = a.sort_values(by=["gender"])

       return a
# table data- By year
table_Ay = data_deal_by_year(join_df2A)
# rename column make tabale have correct vaule - becasue the same name make them omiited some Columns
table_Ay.columns=["year","Gender","FA 5","FA 6","FA 7","FA 8","Non FA grade","FA 6 ","FA 7 ","FA 9 "," FA 7"," FA 8"," FA 9"]
table_Sy = data_deal_by_year(join_df2S)
table_ovr_y = data_deal_by_year(join_df2)
table_ovr_y.columns=["year","Gender","FA 5","FA 6","FA 7","FA 8","FA 9","FA 5 ","FA 6 ","FA 7 ","Non FA grade"," FA 6"," FA 7","FA 9 ","FA 7  "," FA 8"," FA 9"]
#all - table data function
def data_deal_by_all (data):
    b = data.set_index(["grade","function"],drop=True)
    b = b.stack()
    b = b.unstack(level=1)
    b = b.unstack(level=0)
    b = b.dropna(axis=1,how="all")
    b = b.fillna(value=0)
    b = b.droplevel("function",axis=1)
    b = b.reset_index()
    b = b.rename(columns={"index":"gender"})
    #sorting a for matching graph
    b = b.replace({"Male FT":"4.Male FT","Female FT":"3.Female FT",
                   "Male PT":"2.Male PT","Female PT":"1.Female PT"})
    b = b.sort_values(by=["gender"])

    return b

table_Aa = data_deal_by_all(join_df3A)
table_Aa.columns=["Gender","FA 5","FA 6","FA 7","FA 8","Non FA grade","FA 6 ","FA 7 ","FA 9 "," FA 7"," FA 8"," FA 9"]
table_Sa = data_deal_by_all(join_df3S)
table_ovr_a = data_deal_by_all(join_df3)
table_ovr_a.columns=["Gender","FA 5","FA 6","FA 7","FA 8","FA 9","FA 5 ","FA 6 ","FA 7 ","Non FA grade"," FA 6"," FA 7","FA 9 ","FA 7  "," FA 8"," FA 9"]

#Creating year options - which grab the data in the year columns
year_options=df2["year"].unique().tolist()
year_options.sort(reverse=True)
year_options.insert(0,"ALL")

#Creating function year_options
function_options=["Overall","Academic","Professional & Support Staff"]

table_dataset = table_Ay,table_Sy,table_ovr_y,table_Sa,table_ovr_a,table_Aa
graph_dataset = join_df3,join_df3A,join_df3S,join_df2,join_df2A,join_df2S
'''
app = dash.Dash()
app.layout = html.Div([
                      html.Div([
                      html.Label("Select Year"),
                      dcc.Dropdown(
                      id="year-picker1",
                      options=[dict(label=str(i),value=i) for i in year_options],
                      value="ALL")
                      ],
                      style=dict(display="inline-block",verticalAlign="top",width="30%")),
                      html.Div([
                      html.Label("Select Function"),
                      dcc.Dropdown(
                      id="function-picker",
                      options=[dict(label=i,value=i) for i in function_options],
                      value="Overall")
                      ],
                      style=dict(display="inline-block",verticalAlign="top",width="30%")),
                      html.Div([
                      dcc.Graph(id="leaver")],
                      #style={"height":"auto","width":"auto",'padding-left':'3%'}
                      ),
                      html.Div([
                      dash_table.DataTable(
                      id='table',
                      style_cell=dict(
                      textAlign="left",
                      minWidth = '40px', width = '40px', maxWidth = '40px'),
                      style_cell_conditional=[
                      {"if":dict(column_id="Gender"),"width":"75px"},
                      {"if":dict(column_id="Non FA grade"),"width":"90px"}]
                      )
                      ],style={'width':'93%','padding-left':'2%'})
                      ])

@app.callback(Output("leaver","figure"),
              [Input("year-picker1","value"),
               Input("function-picker","value")])

def leaver_upgraded(selected_year,selected_function):

    if selected_year == "ALL":

         if selected_function == "Overall":

             filter_df = join_df3

         elif selected_function == "Academic":

             filter_df = join_df3A

         else :

             filter_df = join_df3S

    else:
          if selected_function == "Overall":

              filter_df = join_df2[join_df2["year"]==selected_year]

          elif selected_function == "Academic":

              filter_df = join_df2A[join_df2A["year"]==selected_year]

          else:

              filter_df = join_df2S[join_df2S["year"]==selected_year]



    yaxis=["Male FT","Female FT","Male PT","Female PT"]

    trace = [go.Bar(
         x=[filter_df["function"],filter_df["grade"]],
         y=filter_df[i],
         name=i)
         for i in yaxis]

    layout = go.Layout(title="Academic leavers by job function and FT/PT status "+ str(selected_year),
                       barmode="stack",
                       xaxis=dict(categoryorder="category ascending",tickfont=dict(size=10)),
                       yaxis=dict(nticks=10),
                       legend=dict(title=None,
                                   y=1.02, yanchor="bottom",
                                   x=1, xanchor="right",
                                   orientation="h"),
                                   font=dict(size=10)
                       )

    fig3 = dict(data=trace, layout=layout)

    return fig3

@app.callback([Output("table","data"),
               Output("table","columns")],
              [Input("year-picker1","value"),
               Input("function-picker","value")])

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

if __name__ == "__main__":
    app.run_server()
'''
