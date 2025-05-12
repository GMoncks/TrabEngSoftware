from dash import (
    register_page,dcc, html, callback, Input, Output, State, no_update
)
import dash_bootstrap_components as dbc
import time




register_page(
    __name__,
    path="/page1",
    title="page1",
    name="page1",
)

layout = html.Div("Page 1")

    