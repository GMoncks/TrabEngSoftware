import time
from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc
import datetime
from utils.enums.categorias import Tool

from main import tool_requests, loan_requests, login_requests

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
        dbc.Col(xs=12, md=6, lg=6, children=[
            html.Label("Buscar"),
            dbc.InputGroup([
                dbc.InputGroupText(html.I(className="bi bi-search")),
                dbc.Input(id="busca-input", placeholder="Buscar ferramenta...")
            ], style={"height":"50px"})
        ]),

        # Data de intervalo: 12 cols no XS, 6 no MD, 3 no LG
        dbc.Col(xs=12, md=6, lg=3, className="mt-2 mt-md-0", children=[
            html.Label("Data de intervalo"),
            dcc.DatePickerRange(
                id='data-disponibilidade',
                min_date_allowed=datetime.datetime.now(),
                start_date_placeholder_text="Início",
                end_date_placeholder_text="Fim",
                display_format='DD/MM/YYYY',
                style={"height":"50px"},
                start_date=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                end_date=(datetime.datetime.now() + datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
            )
        ]),

        # Categoria: 12 cols no XS, 6 no MD, 2 no LG
        dbc.Col(xs=12, md=6, lg=2, className="mt-2 mt-lg-0", children=[
            html.Label("Categoria"),
            dcc.Dropdown(
                id="input-categoria",
                options=[{"label": t.label(), "value": t.value} for t in Tool],
                placeholder="Selecione",
                clearable=True, 
                style={"height":"50px"}
            )
        ])
    ]),


    html.Br(),

    # Resultado
    html.Div(id="resultado-busca", className="mt-3"),
    
    dbc.Modal([
        dcc.Store(id='id_ferramenta-store'),
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
    Input("modal-emprestimo", "is_open")
)
def atualizar_resultado(busca, data_inicio, data_fim, id_categoria, modal_open):
    ferramentas = tool_requests.consultar_ferramentas(busca, id_categoria, data_inicio, data_fim)

    if not ferramentas:
        return html.P("Nenhuma ferramenta encontrada.", className="text-muted")

    cards = []
    for f in ferramentas:
        categoria = Tool.from_value(int(f['id_categoria']))
        icone = categoria.icone()
        card = dbc.Card([
            # Cabeçalho do card com fundo marrom claro e ícone
            html.Div([
                html.Img(src=icone, className="me-2", height="30px"),
                html.Span(f["nome"], className="fw-bold")
            ], className="p-2", style={
                "backgroundColor": "#D2B48C",
                "borderTopLeftRadius": "0.25rem",
                "borderTopRightRadius": "0.25rem"
            }),

            dbc.CardBody([
                # Imagem centralizada
                html.Div(
                    html.Img(
                        src=f["foto"],
                        style={
                            "max-width": "200px",
                            "min-height": "200px"
                        }
                    ),
                    className="d-flex justify-content-center mb-3"
                ),

                # Categoria e descrição
                html.P(categoria.label(), className="card-text text-muted mb-1 text-center"),
                html.P(f["descricao"], className="card-text text-muted mb-1 text-center"),

                # Botão
                dbc.Button(
                    "Solicitar Empréstimo",
                    id={"type": "solicitar-btn", "index": f["id_ferramenta"]},
                    n_clicks=0,
                    style={
                        "backgroundColor": "#4B2E2E",
                        "borderColor": "#4B2E2E",
                        "color": "white"
                    },
                    className="d-block mx-auto"  # Centraliza o botão
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
    Output("id_ferramenta-store", "data"),
    Output("data-periodo", "start_date"),
    Output("data-periodo", "end_date"),
    Output("data-periodo", "min_date_allowed"),
    Output("data-periodo", "max_date_allowed"),
    Output("loan_confirmation_message", "children", allow_duplicate=True),
    Input({"type": "solicitar-btn", "index": ALL}, "n_clicks"),
    State("data-disponibilidade", "start_date"),
    State("data-disponibilidade", "end_date"),
    prevent_initial_call=True
)
def abrir_modal(n_clicks_list, data_inicio, data_fim):
    triggered = ctx.triggered_id
    if not triggered or max(n_clicks_list) == 0:
        return no_update

    id = triggered["index"]
    ferramenta = tool_requests.consultar_ferramenta(id)
    categoria = Tool.from_value(int(ferramenta['id_categoria']))

    return (
        True,
        ferramenta['nome'],
        categoria.icone(),
        f"Categoria: {categoria.label()}",
        f"Proprietário: {ferramenta['nome_usuario']}",
        ferramenta['id_ferramenta'],
        data_inicio,
        data_fim,
        data_inicio,
        data_fim,
        html.Div(),
    )

@callback(
    Output("modal-emprestimo", "is_open", allow_duplicate=True),
    Input("btn-cancelar-emprestimo", "n_clicks"),
    prevent_initial_call=True
)
def fechar_modal(cancelar):
    return False

@callback(
    Output("modal-emprestimo", "is_open", allow_duplicate=True),
    Output("loan_confirmation_message", "children"),
    Input("btn-confirmar-emprestimo", "n_clicks"),
    State("modal-nome-ferramenta", "children"),
    State("data-periodo", "start_date"),
    State("data-periodo", "end_date"),
    State('user-store', 'data'),
    State('id_ferramenta-store', 'data'),
    prevent_initial_call=True
)
def confirmar_emprestimo(n_clicks, tool_name, start_date, end_date, usuario, id_ferramenta):
    print(f"Confirmar empréstimo: {tool_name}, Início: {start_date}, Fim: {end_date}, Usuário: {usuario['id_usuario']}, ID Ferramenta: {id_ferramenta}")

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None

    if login_requests.validar_admin(usuario['id_usuario'])['is_admin']:
        return no_update, dbc.Alert("Administrador não pode solicitar empréstimos.", color="warning")
    if not tool_name or not start_date or not end_date:
        return no_update, dbc.Alert("Preencha todos os campos antes de confirmar o empréstimo.", color="warning")

    if start_date > end_date:
        return no_update, dbc.Alert("A data de início não pode ser posterior à data de fim.", color="warning")
    if start_date < datetime.datetime.now().date():
        return no_update, dbc.Alert("A data de início não pode ser anterior à data atual.", color="warning")

    try:
        loan_requests.solicitar_emprestimo(usuario['id_usuario'], id_ferramenta, start_date, end_date)  # true ou false
        return False, dbc.Alert(f"Empréstimo de '{tool_name}' solicitado com sucesso!", color="success")
    except Exception as e:
        return no_update, dbc.Alert(f"Falha ao solicitar empréstimo de '{tool_name}': {e}", color="danger")
        

