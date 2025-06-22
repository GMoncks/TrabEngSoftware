from dash import register_page, dcc, html, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import datetime

from main import tool_requests

register_page(
    __name__,
    path="/home",
    title="Martelo Amigo",
    name="home",
)

layout = html.Div([
    # CABEÇALHO DE BUSCA (RESPONSIVO)
    dbc.Row([
        # Campo de busca: 5 colunas em tela grande, 12 em pequenas
        dbc.Col(xs=12, md=6, lg=5, children=[
            html.Label("Buscar"),
            dbc.InputGroup([
                dbc.InputGroupText(html.I(className="bi bi-search")),
                dbc.Input(id="busca-input", placeholder="Buscar ferramenta...")
            ])
        ]),

        # Data de intervalo: 12 cols no XS, 6 no MD, 3 no LG
        dbc.Col(xs=12, md=6, lg=3, className="mt-2 mt-md-0", children=[
            html.Label("Data de intervalo"),
            dcc.DatePickerRange(
                id='data-disponibilidade',
                start_date_placeholder_text="Início",
                end_date_placeholder_text="Fim",
                display_format='DD/MM/YYYY',
                className='w-100'
            )
        ]),

        # Categoria: 12 cols no XS, 6 no MD, 2 no LG
        dbc.Col(xs=12, md=6, lg=2, className="mt-2 mt-lg-0", children=[
            html.Label("Categoria"),
            dcc.Dropdown(
                id="input-categoria",
                options=[{"label": f"Opção {i}", "value": f"opcao{i}"} for i in range(1, 4)],
                placeholder="Selecione",
                clearable=True
            )
        ]),

        # Proprietário: 12 cols no XS, 6 no MD, 2 no LG
        dbc.Col(xs=12, md=6, lg=2, className="mt-2 mt-lg-0", children=[
            html.Label("Proprietário"),
            dcc.Dropdown(
                id="input-proprietario",
                options=[{"label": f"Opção {i}", "value": f"opcao{i}"} for i in range(1, 4)],
                placeholder="Selecione",
                clearable=True
            )
        ])
    ]),


    html.Br(),

    # Resultado
    html.Div(id="resultado-busca", className="mt-3"),
    
    dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle(
                html.Div([
                    html.Img(id="modal-icone-categoria", height="30px", className="me-2"),
                    html.Span(id="modal-nome-ferramenta", className="fw-bold")
                ], className="d-flex align-items-center")
            ),
            style={"backgroundColor": "#D2B48C"}  # Marrom claro
        ),
        dbc.ModalBody([
            html.P(id="modal-categoria", className="mb-1"),
            html.P(id="modal-proprietario", className="mb-3"),
            html.Div("Selecione o período desejado:", className="mb-2"),
            dcc.DatePickerRange(
                id="data-periodo",
                start_date_placeholder_text="Início",
                end_date_placeholder_text="Fim",
                display_format="DD/MM/YYYY",
                className="mb-2"
            )
        ]),
        dbc.ModalFooter([
            dbc.Button("Confirmar", id="btn-confirmar-emprestimo", style={
                "backgroundColor": "#4B2E2E",
                "borderColor": "#4B2E2E",
                "color": "white"
            }),
            dbc.Button("Cancelar", id="btn-cancelar-emprestimo", color="secondary", className="ms-2")
        ]),
        html.Div(id="loan_confirmation_message", className="mt-3")
    ], id="modal-emprestimo", is_open=False)
])

@callback(
    Output("resultado-busca", "children"),
    Input("busca-input", "value"),
    Input("data-disponibilidade", "start_date"),
    Input("data-disponibilidade", "end_date"),
    Input("input-categoria", "value"),
    Input("input-proprietario", "value"),
)
def atualizar_resultado(busca, data_inicio, data_fim, categoria, proprietario):
    ferramentas = tool_requests.consultar_ferramentas(busca, data_inicio, data_fim, categoria, proprietario)

    if not ferramentas:
        return html.P("Nenhuma ferramenta encontrada.", className="text-muted")

    categoria_icone = {
        "Opção 1": "🔧",
        "Opção 2": "🔨",
        "Opção 3": "🪚"
    }

    cards = []
    for f in ferramentas:
        icone = categoria_icone.get(f["categoria"], "🛠️")
        card = dbc.Card([
            # Cabeçalho do card com fundo marrom claro e ícone
            html.Div([
                html.Span(icone, className="me-2"),
                html.Span(f["nome"], className="fw-bold")
            ], className="p-2", style={"backgroundColor": "#D2B48C", "borderTopLeftRadius": "0.25rem", "borderTopRightRadius": "0.25rem"}),

            dbc.CardBody([
                html.P(f["categoria"], className="card-text text-muted mb-1"),
                html.P(f["proprietario"], className="card-text text-muted mb-1"),
                html.P(f"Disponível de {f['disponibilidade_inicio']} até {f['disponibilidade_fim']}", className="card-text text-success mb-2"),
                dbc.Button(
                    "Solicitar Empréstimo",
                    id={"type": "solicitar-btn", "index": f["nome"]},
                    n_clicks=0,
                    style={
                        "backgroundColor": "#4B2E2E",
                        "borderColor": "#4B2E2E",
                        "color": "white"
                    }
                )
            ])
        ], className="mb-3 shadow-sm")
        cards.append(card)

    return html.Div([
        dbc.Row([
            dbc.Col(card, xs=12, sm=6, md=4, lg="auto") for card in cards
        ], className="gy-4 gx-3"),
        html.Div(id="mensagem-emprestimo", className="mt-3")
    ])


@callback(
    Output("modal-emprestimo", "is_open", allow_duplicate=True),
    Output("loan_confirmation_message", "children"),
    Input("btn-confirmar-emprestimo", "n_clicks"),
    State("modal-nome-ferramenta", "children"),
    State("data-periodo", "start_date"),
    State("data-periodo", "end_date"),
    prevent_initial_call=True
)
def confirmar_emprestimo(n_clicks, tool_name, start_date, end_date):
    if not tool_name or not start_date or not end_date:
        return no_update, dbc.Alert("Preencha todos os campos antes de confirmar o empréstimo.", color="warning")

    # Simula envio da solicitação para a API
    sucesso = tool_requests.solicitar_emprestimo(tool_name, start_date, end_date)  # true ou false

    if sucesso:
        return False, dbc.Alert(f"Empréstimo de '{tool_name}' solicitado com sucesso!", color="success")
    else:
        return no_update, dbc.Alert(f"Falha ao solicitar empréstimo de '{tool_name}'.", color="danger")

