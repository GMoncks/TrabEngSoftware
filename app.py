
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
    if usuario_logado.logado and pathname != "/":
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - Usuário logado: {usuario_logado.nome}")
        return no_update  # Permite que o usuário continue na página atual
    elif pathname == "/":
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - Usuário não logado, continuando na página de login")
        return no_update  # Permite que o usuário permaneça na página de login
    else:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - Usuário não logado, redirecionando para a página de login")
        return "/"  # Redireciona para a página de login


if __name__ == "__main__":
    app.run(debug=True, port=8050)

