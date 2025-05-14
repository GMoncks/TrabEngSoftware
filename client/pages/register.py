from dash import (
    register_page, dcc, html, callback, Input, Output, State, no_update
)
import dash_bootstrap_components as dbc
import time

from main import (
    login_requests,
    usuario_logado
)

register_page(
    __name__,
    path="/signup",
    title="Cadastro",
    name="Cadastro",
    description="Tela de cadastro do sistema.",
)

layout = dbc.Container([
    html.H2("Cadastro de Morador", className="my-4"),

    dbc.Form([
        dbc.Row([
            dbc.Col([
                dbc.Label("Email"),
                dbc.Input(id="input-email", type="email", placeholder="email@exemplo.com")
            ])
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Senha"),
                dbc.Input(id="input-password", type="password", placeholder="Senha")
            ])
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Nome completo"),
                dbc.Input(id="input-name", type="text", placeholder="Nome completo")
            ])
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Identificação da casa/apartamento"),
                dbc.Input(id="input-home_id", type="text", placeholder="Ex: Bloco B, Apto 101")
            ])
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("CPF"),
                dbc.Input(id="input-cpf", type="text", placeholder="000.000.000-00")
            ])
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Label("Telefone"),
                dbc.Input(id="input-phone", type="text", placeholder="(99) 99999-9999")
            ])
        ], className="mb-4"),

        dbc.Button("Cadastrar", id="btn-submit", color="primary", className="me-2"),
    ]),

    html.Hr(),

    html.Div(id="output", className="mt-3")
], fluid=True)


@callback(
    Output("output", "children"),
    Input("btn-submit", "n_clicks"),
    State("input-email", "value"),
    State("input-password", "value"),
    State("input-home_id", "value"),
    State("input-name", "value"),
    State("input-cpf", "value"),
    State("input-phone", "value"),
    prevent_initial_call=True
)
def cadastrar(n_clicks, email, password, home_id, name, cpf, phone):
    
    login_requests.cadastrar_usuario(email, password, home_id, name, cpf, phone)
    
    return dbc.Alert([
        html.H5("Cadastro realizado com sucesso!", className="alert-heading"),
        html.P(f"Identificação: {id}"),
        html.P(f"Nome: {name}"),
        html.P(f"CPF: {cpf}"),
        html.P(f"Email: {email}"),
        html.P(f"Telefone: {phone}")
    ], color="success")
    

@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('output', 'children'),
    prevent_initial_call=True
)
def callback_trocar_tela(children):
        if children:
            time.sleep(3)
            return "/home"
        return no_update
        