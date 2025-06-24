
from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc
import requests
from main import loan_requests 
from utils.enums.status import LoanStatus
from utils.enums.categorias import Tool

register_page(
    __name__,
    path="/my_loans",
    title="Emprestar",
    name="Emprestar",
)

layout = html.Div([
    dcc.Store(id='meus-emprestimos-refresh'),
    html.Div(id='meus-emprestimos-container')
], style={"padding": "20px"})

# Função para criar os cards dos empréstimos
def criar_card_emprestimo(emprestimo):    
    botoes = []
    status = LoanStatus.from_value(int(emprestimo["id_status"]))
    categoria = Tool.from_value(int(emprestimo["id_categoria"]))
    if status == LoanStatus.AGUARDANDO_AUTORIZACAO:
        botoes.append(
            dbc.Button("Aceitar", style={
                "backgroundColor": "#4B2E2E",
                "borderColor": "#4B2E2E",
                "color": "white",
                "marginBottom": "10px",
                "width": "100%"
            }, id={"type": "btn-autorizar-emprestimo", "index": emprestimo["id_registro"]})
        )        
        botoes.append(
            dbc.Button("Rejeitar", style={
                "backgroundColor": "#4B2E2E",
                "borderColor": "#4B2E2E",
                "color": "white",
                "width": "100%"
            }, id={"type": "btn-rejeitar-emprestimo", "index": emprestimo["id_registro"]})
        )
    elif status == LoanStatus.EMPRESTADO:
        botoes.append(
            dbc.Button("Encerrar empréstimo", style={
                "backgroundColor": "#4B2E2E",
                "borderColor": "#4B2E2E",
                "color": "white",
                "width": "100%"
            }, id={"type": "btn-devolver-emprestimo", "index": emprestimo["id_registro"]})
        )

    return dbc.Card(
        dbc.CardBody(
            dbc.Row([
                dbc.Col(html.Div(emprestimo["nome_ferramenta"]), width=2),
                dbc.Col(html.Div(categoria.label()), width=2),
                dbc.Col(html.Div(emprestimo['nome_usuario']), width=2),
                dbc.Col(html.Div(emprestimo["dt_emprestimo"]), width=2),
                dbc.Col(html.Div(emprestimo["dt_devolucao"]), width=2),
                dbc.Col(html.Div(status.label()), width=1),
                dbc.Col(html.Div(botoes), width=1),
            ], align="center", className="g-2")
        ),
        style={"marginBottom": "10px", "backgroundColor": "white", "width": "100%"},
        className="shadow-sm p-2"
    )


# Callback para carregar os empréstimos do usuário
@callback(
    Output('meus-emprestimos-container', 'children'),
    Input('meus-emprestimos-refresh', 'data'),
    State('user-store', 'data')
)
def carregar_emprestimos(_, user_data):
    id_usuario = user_data.get("id_usuario")
    if not id_usuario:
        return html.P("Usuário não encontrado.")

    try:
        emprestimos = loan_requests.buscar_emprestimos(id_usuario, True)    
    except Exception as e:
        return html.P(f"Erro ao carregar os dados: {str(e)}")

    if not emprestimos:
        return html.P("Nenhum empréstimo encontrado.")

    cabecalho = dbc.Row([
        dbc.Col(html.Strong("Ferramenta"), width=2),
        dbc.Col(html.Strong("Categoria"), width=2),
        dbc.Col(html.Strong("Morador"), width=2),
        dbc.Col(html.Strong("Início"), width=2),
        dbc.Col(html.Strong("Devolução"), width=2),
        dbc.Col(html.Strong("Status"), width=1),
        dbc.Col(html.Span(""), width=1),
    ], className="p-2",
                        style={
                            "marginBottom": "5px", 
                            "backgroundColor": "#D2B48C",
                            "borderTopLeftRadius": "0.25rem",
                            "borderTopRightRadius": "0.25rem",
                            "borderBottomLeftRadius": "0.25rem",
                            "borderBottomRightRadius": "0.25rem",
                        })
    
    cards = [criar_card_emprestimo(emp) for emp in emprestimos[::-1]]

    return [cabecalho] + cards


# Callback para lidar com os botões de aceitar/encerrar empréstimo
@callback(
    Output('meus-emprestimos-refresh', 'data', allow_duplicate=True),
    Input({'type': 'btn-autorizar-emprestimo', 'index': ALL}, 'n_clicks'),
    State({'type': 'btn-autorizar-emprestimo', 'index': ALL}, 'id'),
    prevent_initial_call=True
)
def tratar_click_botoes(n_clicks, ids):
    triggered_id = ctx.triggered_id
    if all(v is None for v in n_clicks):
        return no_update

    id_registro = triggered_id['index']
    try:
        loan_requests.autorizar_emprestimo(id_registro)
        return 1
    except Exception as e:
        return f"Erro: {str(e)}"

@callback(
    Output('meus-emprestimos-refresh', 'data', allow_duplicate=True),
    Input({'type': 'btn-rejeitar-emprestimo', 'index': ALL}, 'n_clicks'),
    State({'type': 'btn-rejeitar-emprestimo', 'index': ALL}, 'id'),
    prevent_initial_call=True
)
def tratar_click_botoes(n_clicks, ids):
    triggered_id = ctx.triggered_id
    if all(v is None for v in n_clicks):
        return no_update

    id_registro = triggered_id['index']
    try:
        loan_requests.cancelar_emprestimo(id_registro)
        return 1
    except Exception as e:
        return f"Erro: {str(e)}"

@callback(
    Output('meus-emprestimos-refresh', 'data', allow_duplicate=True),
    Input({'type': 'btn-devolver-emprestimo', 'index': ALL}, 'n_clicks'),
    State({'type': 'btn-devolver-emprestimo', 'index': ALL}, 'id'),
    prevent_initial_call=True
)
def tratar_click_botoes(n_clicks, ids):
    triggered_id = ctx.triggered_id
    if all(v is None for v in n_clicks):
        return no_update

    id_registro = triggered_id['index']
    try:
        loan_requests.devolver_emprestimo(id_registro)
        return 1
    except Exception as e:
        return f"Erro: {str(e)}"