
import dash
from dash import (
    html,
    dcc,
    page_container,
    callback,
    Input,
    Output,
    no_update
)
import dash_bootstrap_components as dbc
import time

from main import usuario_logado

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    update_title="Carregando...",
    )

# Layout da tela de login
app.layout = html.Div(
    id="main-container",
    children=[
        dcc.Location(
            id="url",
            refresh=True
            ),
        page_container,
    ]
)


@callback(
    Output("url", "pathname"),
    Input("url", "pathname"),
)
def callback_login_check(pathname):
    if not usuario_logado.logado and pathname != "/":
        return "/"
    return no_update

if __name__ == "__main__":
    app.run(debug=True, port=8050)

