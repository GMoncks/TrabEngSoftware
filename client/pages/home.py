from dash import (
    register_page,dcc, html, callback, Input, Output, State, no_update
)
import dash_bootstrap_components as dbc

from main import (
    usuario_logado
)


register_page(
    __name__,
    path="/home",
    title="home",
    name="home",
)

layout = dbc.Container(
    id="home-container",
    children = "Home",
    )

@callback(
    Output("home-container", "children"),
    Input("url", "pathname"),
)
def callback_atualizar_home(pathname):
    if pathname == "/home":
        return [
            html.H1("Martelo Amigo"),
            html.Hr(),
            html.H4("Informações do usuário"),
            html.P(f"Usuário logado: {usuario_logado.nome.title()}"),  
            html.P(f"Data do último acesso: {usuario_logado.dt_ultimo_acesso if usuario_logado.dt_ultimo_acesso else 'Nunca'}"),
            html.P(f"Data de cadastro: {usuario_logado.dt_cadastro}"),
            html.P(f"ID do usuário: {usuario_logado.id_usuario}"),
            html.P(f"Score do usuário: {usuario_logado.score}"),
        ]
    