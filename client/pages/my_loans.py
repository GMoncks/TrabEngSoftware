
from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/my_loans",
    title="Meus Empréstimos",
    name="Meus Empréstimos",
)

layout = html.Div([
    html.H3("Meus Empréstimos"),
    html.P("Histórico e status dos seus empréstimos...")
])
