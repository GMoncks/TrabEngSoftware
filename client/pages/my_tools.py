from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/my_tools",
    title="Minhas Ferramentas",
    name="Minhas Ferramentas",
)

layout = html.Div([
    html.H3("Minhas Ferramentas"),
    html.P("Conteúdo das suas ferramentas cadastradas...")
])
