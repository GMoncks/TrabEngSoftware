from dash import dcc, html, register_page, callback, Input, Output, State, no_update
import time
from utils.classes.user import Usuario
from main import login_requests
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/login",
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
                        )
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
    Output("user-store", "data"),
    Output("login-output", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("login-button", "n_clicks"),
    State("input-user", "value"),
    State("input-password", "value"),
    prevent_initial_call=True
)
def callback_login(n_clicks, user, password):
        try:
            if n_clicks:
                time.sleep(1)  # Simulando um atraso para o carregamento
                user_info = login_requests.validar_login(user, password)
                if user_info:
                    user = Usuario()
                    user.login(
                        user_info["id_usuario"],
                        user_info["dt_cadastro"],
                        user_info["email"],
                        user_info["senha"],
                        user_info["name"],
                        user_info["home_id"],
                        user_info["cpf"],
                        user_info["phone"],
                        user_info["inadimplente"],
                        user_info["admin"],
                        user_info["dt_last_acess"]
                        )
                    return user.__dict__, "Login bem-sucedido!", "/home"
                else:
                    return no_update, "Usuário ou senha incorretos.", no_update
        except Exception as e:
            return no_update,f"Erro ao fazer login: {e}", no_update