from dash import (
    register_page,dcc, html, callback, Input, Output, State, no_update
)
import dash_bootstrap_components as dbc
import time

from main import (
    db_comm,
    usuario_logado
)


register_page(
    __name__,
    path="/page1",
    title="page1",
    name="page1",
)

layout = dbc.Container(
    id="page1-container",
    children = "Page 1",
    )

@callback(
    Output("page1-container", "children"),
    Input("url", "pathname"),
)
def callback_atualizar_page1(pathname):
    if pathname == "/page1":
        return [
            html.H1("Martelo Amigo"),
            html.Hr(),
            html.H4("Informações do usuário"),
            html.P(f"Usuário logado: {usuario_logado.nome.title()}"),  
            html.P(f"Tipo de acesso: {"Administrador" if usuario_logado.admin else "Morador"}"),	
            html.P(f"Data do último acesso: {usuario_logado.dt_ultimo_acesso if usuario_logado.dt_ultimo_acesso else 'Nunca'}"),
            html.P(f"Data de cadastro: {usuario_logado.dt_cadastro}"),
            html.P(f"ID do usuário: {usuario_logado.id_usuario}"),
            html.P(f"Score do usuário: {usuario_logado.score}"),
        ]
    