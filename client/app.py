import dash
from dash import html, dcc, page_container, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc
from main import tool_requests, login_requests
import datetime

custom_css = {
    "sidebar": {
        "backgroundColor": "#4B2E2E",
        "color": "white",
        "min-height": "100vh",
        "padding": "20px"
    },
    "sidebar_link": {
        "color": "white",
        "padding": "10px",
        "backgroundColor": "#4B2E2E",
        "border": "none",
        "textAlign": "left",
        "textDecoration": "none",
        "width": "100%",
    },
    "sidebar_link_hover": {
        "color": "white",
        "padding": "10px",
        "backgroundColor": "#5A3D3D",
        "border": "none",
        "textAlign": "left",
        "textDecoration": "none",
        "width": "100%",
    }
}

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    update_title="Carregando...",
    )

app.layout = dbc.Container(id="main-container", fluid=True, children=[
    dcc.Store(id="user-store", storage_type="session", data=None),
    dcc.Location(
        id="url",
        refresh=True
        ),
    dbc.Row([
        # MENU LATERAL
        dbc.Col(id="sidebar",width=2, style={"display":"none"}, children=[
            html.Div([
                html.Div(id="user-info"),
                html.Hr(style={"borderColor": "white"}),
                html.Div([
            dbc.Button("Buscar Ferramentas",n_clicks=0, color="primary", style=custom_css["sidebar_link"], className="w-100 text-start", href="/home", id="btn-home"),
            dbc.Button("Minhas Ferramentas",n_clicks=0, color="primary", style=custom_css["sidebar_link"], className="w-100 text-start", href="/my_tools", id="btn-my-tools"),
            dbc.Button("Emprestar",n_clicks=0, color="primary", style=custom_css["sidebar_link"], className="w-100 text-start", href="/my_loans", id="btn-my-loans"),
            dbc.Button("Pedir Emprestado",n_clicks=0, color="primary", style=custom_css["sidebar_link"], className="w-100 text-start", href="/loans", id="btn-loans"),
            dbc.Button("Cadastro",n_clicks=0, color="primary", style=custom_css["sidebar_link"], className="w-100 text-start", href="/register", id="btn-register"),
            dbc.Button("Sair",n_clicks=0, color="primary", style=custom_css["sidebar_link"], className="w-100 text-start", href="/login", id="btn-logout"),
                ], id="menu_links")
            ])
        ]),

        # CONTEÚDO PRINCIPAL
        dbc.Col(id="page_container", width=12, children=[
            html.Div([
                html.Div([
                    html.Img(src="/assets/logo.png", height="100px", className="me-2"),
                    html.H1("Martelo Amigo", className="mb-0", style={"color":"brown", "maxWidth": "400px", "fontSize":"50px"})
                ], className="d-flex align-items-center justify-content-center")
            ], className="mt-3 mb-4 d-flex justify-content-center"),
            page_container
        ]),
    ]),
])

@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("user-store", "clear_data"),
    Input("btn-logout", "n_clicks"),
    prevent_initial_call=True
)
def deslogar(n_clicks):
    if n_clicks:
        return "/login", True
    else:
        return no_update, False 

@callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("url", "pathname"),
    State("user-store", "data"),
    prevent_initial_call=True
)
def redirecionar_se_nao_logado(pathname, data):
    if not data:
        return "/login"
    return "/home" if pathname == "/" or pathname == "/login" else no_update


@callback(
    Output("user-info", "children"),
    Output("sidebar", "style"),
    Output("page_container", "width"),
    Input("user-store", "data")
)
def mostrar_usuario(data):
    if data:
        return html.Div([
                html.Img(src="/assets/user.png", height="30px", style={"border-radius": "50%"}),
                html.Span(data["name"], className="ms-2 fw-bold")
            ], className="d-flex align-items-center my-3"), custom_css["sidebar"], 10
    return html.Div([
                html.Img(src="/assets/user.png", height="30px", style={"border-radius": "50%"}),
                html.Span("Nome de Usuário", className="ms-2 fw-bold")
            ], className="d-flex align-items-center my-3"), {"display": "none"}, 12

@callback(
    Output("btn-home", "style"),
    Output("btn-my-tools", "style"),
    Output("btn-my-loans", "style"),
    Output("btn-loans", "style"),
    Output("btn-register", "style"),
    Input("url", "pathname"),
    prevent_initial_call=True
)
def atualizar_style_botoes(pathname):
    if pathname == "/home":
        return custom_css["sidebar_link_hover"], custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link"]
    elif pathname == "/my_tools":
        return custom_css["sidebar_link"], custom_css["sidebar_link_hover"], custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link"]
    elif pathname == "/my_loans":
        return custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link_hover"], custom_css["sidebar_link"], custom_css["sidebar_link"]
    elif pathname == "/loans":
        return custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link_hover"], custom_css["sidebar_link"]
    elif pathname == "/register":
        return custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link"], custom_css["sidebar_link_hover"]
    else:
        return no_update, no_update, no_update, no_update, no_update


if __name__ == "__main__":
    # TODO: Retirar debug=True
    app.run(debug=True, port=8050)