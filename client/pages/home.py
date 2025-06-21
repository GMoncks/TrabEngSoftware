from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc
import datetime
from main import tool_requests

register_page(
    __name__,
    path="/home",
    title="Martelo Amigo",
    name="home"
)

custom_css = {
        "sidebar": {
            "backgroundColor": "#4B2E2E",  # Marrom escuro
            "color": "white",
            "height": "100vh",
            "padding": "20px"
        },
        "sidebar_link": {
            "color": "white",
            "padding": "10px",
            "textDecoration": "none"
        },
        "sidebar_link_hover": {
            "backgroundColor": "#6E4B4B"
        }
    }

layout = dbc.Container(fluid=True, children=[
        dbc.Row([
            # MENU LATERAL
            dbc.Col(width=2, style=custom_css["sidebar"], children=[
                html.Div([
                    html.Div(id="user-info"),                
                    html.Hr(style={"borderColor": "white"}),
                    # Navegação personalizada
                    html.Div([
                        html.A("Minhas Ferramentas", href="#", className="d-block", style=custom_css["sidebar_link"]),
                        html.A("Meus Empréstimos", href="#", className="d-block", style=custom_css["sidebar_link"]),
                        html.A("Cadastro", href="#", className="d-block", style=custom_css["sidebar_link"])
                    ], id="menu-links")
                ])
            ]),

            # CONTEÚDO PRINCIPAL
            dbc.Col(width=10, children=[
                # TÍTULO
                html.Div([
                    html.Div([
                        html.Img(src="/assets/logo.png", height="60px", className="me-2"),
                        html.H1("Martelo amigo", className="mb-0")
                    ], className="d-flex align-items-center justify-content-center")
                ], className="mt-3 mb-4 d-flex justify-content-center"),

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
                    ])
                ], id="modal-emprestimo", is_open=False),
                html.Div(id="loan_confirmation_message", className="mt-3")
            ])
        ])
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
    Output("modal-emprestimo", "is_open"),
    Output("modal-nome-ferramenta", "children"),
    Output("modal-icone-categoria", "src"),
    Output("modal-categoria", "children"),
    Output("modal-proprietario", "children"),
    Output("data-periodo", "min_date_allowed"),
    Output("data-periodo", "max_date_allowed"),
    Input({"type": "solicitar-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def abrir_modal(n_clicks_list):
    triggered = ctx.triggered_id
    if not triggered or max(n_clicks_list) == 0:
        return no_update

    nome = triggered["index"]

    # Simule os dados com base no nome da ferramenta
    # (em produção, recupere de um dicionário ou banco)
    categoria = "Furadeira"
    proprietario = "João"
    disponibilidade_inicio = datetime.date(2025, 6, 21)
    disponibilidade_fim = datetime.date(2025, 6, 30)
    icone = "/assets/logo.png"

    return (
        True,
        nome,
        icone,
        f"Categoria: {categoria}",
        f"Proprietário: {proprietario}",
        disponibilidade_inicio,
        disponibilidade_fim
    )

@callback(
    Output("modal-emprestimo", "is_open", allow_duplicate=True),
    Input("btn-cancelar-emprestimo", "n_clicks"),
    Input("btn-confirmar-emprestimo", "n_clicks"),
    prevent_initial_call=True
)
def fechar_modal(cancelar, confirmar):
    return False

@callback(
    Output("loan_modal", "is_open", allow_duplicate=True),
    Output("loan_confirmation_message", "children"),
    Input("btn-confirmar-emprestimo", "n_clicks"),
    State("modal_tool_name", "children"),
    State("rental_period", "start_date"),
    State("rental_period", "end_date"),
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

@callback(
    Output("user-info", "children"),
    Input("user-store", "data")
)
def mostrar_usuario(data):
    if data:
        return html.Div([
                html.Img(src="/assets/user.png", height="30px", style={"border-radius": "50%"}),
                html.Span(data["name"], className="ms-2 fw-bold")
            ], className="d-flex align-items-center my-3"),
    return html.Div([
                html.Img(src="/assets/user.png", height="30px", style={"border-radius": "50%"}),
                html.Span("Nome de Usuário", className="ms-2 fw-bold")
            ], className="d-flex align-items-center my-3"),