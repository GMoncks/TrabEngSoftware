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

layout = dbc.Container([
    dbc.Container(id="home-container"),       
    dbc.Button("Cadastrar", id="btn-home-register", color="primary", className="me-2")
])

@callback(
    Output("home-container", "children"),
    Input("url", "pathname"),
)
def callback_atualizar_home(pathname):
    if pathname == "/home":
        pages = [
            html.H1("Martelo Amigo"),
            html.Hr(),
            html.H4("Informações do usuário"),
            html.P(f"Usuário logado: {usuario_logado.name}"),  
            html.P(f"Email: {usuario_logado.email}"),  
            html.P(f"Identificação da casa: {usuario_logado.home_id}"),  
            html.P(f"CPF: {usuario_logado.cpf}"),  
            html.P(f"Telefone: {usuario_logado.phone}"),  
            html.P(f"Data do último acesso: {usuario_logado.dt_ultimo_acesso if usuario_logado.dt_ultimo_acesso else 'Nunca'}"),
            html.P(f"Data de cadastro: {usuario_logado.dt_cadastro}"),
            html.P(f"ID do usuário: {usuario_logado.id_usuario}"),
            html.P(f"Score do usuário: {usuario_logado.score}"),
        ]
        if usuario_logado.admin:
            pages.append(html.P(f"Administrador"))
        
        return pages

@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input("btn-home-register", "n_clicks"),
    prevent_initial_call=True
)
def callback_register(n_clicks):
    if n_clicks:
        return '/signup'