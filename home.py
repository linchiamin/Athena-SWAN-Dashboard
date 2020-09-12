import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
import os.path,time
import datetime
import dash_table
import pandas as pd
from app import app
from app import server
# external_stylesheets = [dbc.themes.PULSE]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# staff = datetime.datetime.fromtimestamp(os.path.getmtime("4.2(ii)- ftc vs oec - all staff - WMG.xlsx")).strftime('%d-%m-%Y %H:%M:%S')
#Data updated recording
staff = time.ctime(os.path.getmtime("4.2(ii)- ftc vs oec - all staff - WMG.xlsx"))
leaver = time.ctime(os.path.getmtime("4.2(iii) - leavers with reason - all staff - by contract function FT_PT and grade - WMG.xlsx"))
student = time.ctime(os.path.getmtime("student.xlsx"))
recruitment = time.ctime(os.path.getmtime("NEW Copy of Recruitment - gender - WMG.xlsx"))
student_enr = time.ctime(os.path.getmtime("enrolment.xlsx"))

update = {"Data Name":["Staff Data","Staff leaver Data","Student Data","FTMSc Enrollment Data","Recruitment Data" ],"Last Updated Date":[staff,leaver,student,student_enr,recruitment]}
update = pd.DataFrame(data=update)
# update["Data Last Updated Recording"] = update.to_datetime(df["Data Last Updated Recording"])
update = update.sort_values(by=["Last Updated Date"], ascending=False)

layout = html.Div([
     dbc.Container([
            #dbc.Jumbotron(
                #[
                       #dbc.Row([dbc.Col(html.H1("hi"))]),
                       html.H2("Welcome to the WMG Dashboard for Athena Swan Gender Chapter",className="text-center"),
                       html.A(html.Img(src="/assets/3.png", width="1080px"),href="https://warwick.ac.uk/services/equalops/learnmore/chartermarks/athena/",target="_blank"),#,style=dict(marginLeft="2px")),
                       html.H5(" "),
                       html.H5(children="The Athena SWAN Charter is a framework, established in 2005 which is used across the globe to support and,"
                                                "transform gender equality within higher education and research."),
                       html.H3("The Charter covers women (and men where appropriate) in :"),
                       html.Hr(className="my-2"),
                       html.P(children="◆ Academic roles in science, technology, engineering, maths and medicine (STEMM) and "
                                       "arts, humanities, social sciences, business and law (AHSSBL)."),
                       html.P("◆ Professional and support staff."),
                       html.P("◆ Trans staff and students."),
                       html.H5(" "),
                       html.P("In relation to their representation, the progression of students into academia, staff journeys through career milestones, and the working environment for all staff."),
                       dbc.Row([
                       dbc.Col(dbc.Button("Dashobard", color="primary",href="student"),width=1),
                       dbc.Col(dbc.Button("Learn more Athena Swan", color="primary",href="https://www.advance-he.ac.uk/charters/athena-swan-charter",target="_blank"),width=3)
                         ],justify="start"),
                       html.P(" "),
                       html.P(" "),
                       html.H5("Data Updated Recording"),
                       dash_table.DataTable(
                           id='table',
                           columns=[{"name": i, "id": i} for i in update.columns],
                           data= update.to_dict('records'),
                           style_cell_conditional=[
                           {"if":{"column_id":"Data Name"},"width":"170px"},
                           {"if":{"column_id":"Last Updated Date"},"textAlign":"center"}
                           ],
                           style_data_conditional=[
                           {'if': {'row_index': 'odd'},
                           'backgroundColor': 'rgb(248, 248, 248)'}
                            ],
                           style_as_list_view=True,
                           style_header=
                           {'backgroundColor': 'rgb(230, 230, 230)',
        '                   fontWeight': 'bold'}
                           ),
                           html.P(" "),
                           html.P(" ")


                #]
                #    )
          ])
     ])




# if __name__ == '__main__':
    # app.run_server()
