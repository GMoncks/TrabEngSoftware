import dash
from dash import html, dcc, page_container, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    update_title="Carregando...",
    )

app.layout = html.Div(
    id="main-container",
    children=[
        dcc.Store(id="user-store", storage_type="session"),
        dcc.Location(
            id="url",
            refresh=True
            ),
        page_container,
    ]
)

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

if __name__ == "__main__":
    app.run(debug=True, port=8050)