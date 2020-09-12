# package imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
from flask import session, copy_current_request_context
# local imports
from auth import authenticate_user, validate_login_session
import home
import recruitment
import staff
import FT
from app import app
from app import server

logout_button = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Log out", color="danger", className="ml-2",href="/leave"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar =  dbc.Navbar(
       dbc.Container(
        [
            dbc.Row([
            html.A(dbc.Col([
                       html.Img(src="/assets/Logo3.png", height="50px"),
                       dbc.NavbarBrand("Athena Swan DashBoard", className="ml-2")],width="auto"),href="/home"),

                   dbc.Col(dbc.Nav([
                             dbc.NavItem(dbc.NavLink("Home", href="home")),
                             dbc.NavItem(dbc.NavLink("Student Data", href="student")),
                             dbc.NavItem(dbc.NavLink("Academic and Professional Staff", href="A&S")),
                             dbc.NavItem(dbc.NavLink("Career Transition", href="CT"))
                                ], className="mr-auto", navbar=True),width="auto"),

                      ],align="center",no_gutters=True,),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(logout_button, id="navbar-collapse", navbar=True),

        ],
            ),
    color="primary",
    dark=True,
    className="mb-4",
)

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# login layout content
def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url',pathname='/login',refresh=False),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Login',className='card-title'),
                                    dbc.Input(id='login-email',placeholder='User'),
                                    dbc.Input(id='login-password',placeholder='Assigned password',type='password'),
                                    dbc.Button('Submit',id='login-button',color='success',block=True),
                                    html.Br(),
                                    html.Div(id='login-alert')
                                ],
                                body=True,
                                className="card border-secondary mb-3"
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )


# home layout content

@validate_login_session
def app_layout():
    return  \
        html.Div([
            dcc.Location(id='leave',pathname='/leave'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                                dbc.Card([
                                    html.H4('Are you leaving now ?',className='card-title'),
                                    html.P("Or you can keep going to look by selecting the option on the menu bar",className="card-text"),
                                    html.Br(),
                                    dbc.Button('Yes, I am leaving now.',id='logout-button',color='danger',block=True,size='sm'),

                                ],
                                body=True,
                                className="card border-danger mb-3"
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )



# main app layout

app.layout = html.Div(
    [
        dcc.Location(id='url',refresh=False),
        navbar,
        html.Div(
            login_layout(),
            id='page-content'
        ),
    ]
)


###############################################################################
# utilities
###############################################################################

# router
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def router(url):
 if "authed" in session:
    if url=='/home':
        #session['authed'] = True
        return home.layout

    if url=='/leave':
        #session['authed'] = True
        return app_layout()
    if url == '/student':

        return FT.layout
    elif url == '/A&S':
        #session['authed'] = True
        return staff.layout
    elif url== '/CT':
        #session['authed'] = True
        return recruitment.layout
    elif url=='/login':
        #session['authed'] = True
        return login_layout()
    else:
        return login_layout()

 else:
    return login_layout()

 #session['authed'] = False

# authenticate
@app.callback(
    [Output('url','pathname'),
     Output('login-alert','children')],
    [Input('login-button','n_clicks')],
    [State('login-email','value'),
     State('login-password','value')])
def login_auth(n_clicks,email,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update,no_update
    credentials = {'user':email,"password":pw}
    if authenticate_user(credentials):
        session['authed'] = True
        return '/home',''
    session['authed'] = False
    return no_update,dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)

@app.callback(
     Output('leave','pathname'),
    [Input('logout-button','n_clicks')])

def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session.clear()
    return '/login'



if __name__ == "__main__":
    app.run_server(debug=True)
