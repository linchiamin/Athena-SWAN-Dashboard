import dash
import dash_bootstrap_components as dbc
import os
# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.PULSE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Hotjar Tracking Code for https://athenaswanwmg.herokuapp.com/ -->
        <script>
        (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:1941148,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
        })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

server = app.server
server.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config.suppress_callback_exceptions = True
