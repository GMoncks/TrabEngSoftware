from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc

from main import login_requests

register_page(
    __name__,
    path="/register",
    title="Martelo Amigo - Cadastro de Morador",
    name="Cadastro de Morador",
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

            dbc.Button("Cadastrar", id="btn-submit", color="primary", className="me-2", 
                        style={
                            "backgroundColor": "#4B2E2E",
                            "borderColor": "#4B2E2E",
                            "color": "white"
                        }),
        ]),

        html.Hr(),

        html.Div([
            dbc.Alert(id="alert", is_open=False, duration=4000)
            ], 
            id="output", 
            className="mt-3"
            )
    ], fluid=True)




@callback(
    Output("alert", "children"),
    Output("alert", "color"),
    Output("alert", "is_open"),
    Input("btn-submit", "n_clicks"),
    State("input-email", "value"),
    State("input-password", "value"),
    State("input-home_id", "value"),
    State("input-name", "value"),
    State("input-cpf", "value"),
    State("input-phone", "value"),
    State("user-store", "data"),
    prevent_initial_call=True
)
def cadastrar(n_clicks, email, password, home_id, name, cpf, phone, usuario):    
    try:
        if n_clicks:
            if not email or not password or not home_id or not name or not cpf or not phone:
                return "Todos os campos são obrigatórios.", "warning", True
            exists = login_requests.validar_usuario(email)
            if not exists["exists"]:
                login_requests.cadastrar_usuario(usuario["id_usuario"], email, password, home_id, name, cpf, phone)
                return [
                    html.H5("Cadastro realizado com sucesso!", className="alert-heading"),
                    html.P(f"Identificação: {home_id}"),
                    html.P(f"Nome: {name}"),
                    html.P(f"CPF: {cpf}"),
                    html.P(f"Email: {email}"),
                    html.P(f"Telefone: {phone}")
                ], "success", True
            else:
                return "Usuário já existe.", "danger", True

    except Exception as e:
        return f"Erro ao cadastrar usuário: {e}", "danger", True
   