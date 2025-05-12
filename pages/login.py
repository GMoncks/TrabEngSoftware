from dash import (
    register_page, dcc, html, callback, Input, Output, State, no_update
)
import dash_bootstrap_components as dbc
import time

from main import (
     db_comm,
     usuario_logado
)


register_page(
    __name__,
    path="/",
    title="Login",
    name="Login",
    description="Tela de login do sistema.",

)

layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H3("Login", className="text-center mb-4"),
                    dbc.Label("Usuário", html_for="input-user"),
                    dbc.Input(type="text", id="input-user", placeholder="Digite seu usuário"),
                    html.Br(),
                    dbc.Label("Senha", html_for="input-password"),
                    dbc.Input(type="password", id="input-password", placeholder="Digite sua senha"),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Button("Entrar", id="login-button", color="primary", className="w-100"),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Button(children="Cadastrar", id="signup-button", color="secondary", className="w-100"),
                            width=6
                        ),
                    ]),
                    dcc.Loading(
                        html.Div(id="login-output", className="mt-3", style={'min-height':"20px"})
                        )
                ]),
                className="shadow p-4"
            ),
            width=12, md=6, lg=4, className="mx-auto mt-5"
        )
    )
)

@callback(
    Output("login-output", "children", allow_duplicate=True),
    Input("login-button", "n_clicks"),
    State("input-user", "value"),
    State("input-password", "value"),
    State("url", "pathname"),
    prevent_initial_call=True
)
def callback_login(n_clicks, user, password, caminho_atual):
        try:
            if n_clicks:
                time.sleep(1)  # Simulando um atraso para o carregamento
                if db_comm.validar_login(user, password):
                    usuario_logado.login(user, user, password)
                    return "Login bem-sucedido!"
                else:
                    return "Usuário ou senha incorretos."
        except Exception as e:
            return f"Erro ao fazer login: {e}"

@callback(
    Output("login-output", "children", allow_duplicate=True),
    Input("signup-button", "n_clicks"),
    State("input-user", "value"),
    State("input-password", "value"),
    prevent_initial_call=True
)
def callback_cadastro(n_clicks, user, password):
    try:
        if n_clicks:
            time.sleep(1)  # Simulando um atraso para o carregamento
            if not db_comm.validar_usuario(user):
                db_comm.cadastrar_usuario(user, password)
                return "Usuário cadastrado com sucesso!"
            else:
                return "Usuário já existe."

    except Exception as e:
        return f"Erro ao cadastrar usuário: {e}"

@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('login-output', 'children'),
    prevent_initial_call=True
)
def callback_trocar_tela(n_clicks):
    if n_clicks == "Login bem-sucedido!":
        time.sleep(1)
        return "/page1"
    else:
        return no_update
    
