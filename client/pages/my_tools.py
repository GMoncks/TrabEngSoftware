import time
from dash import register_page, dcc, html, callback, Input, Output, State, no_update, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
from main import tool_requests
from utils.enums.categorias import Tool

register_page(
    __name__,
    path="/my_tools",
    title="Minhas Ferramentas",
    name="Minhas Ferramentas",
)

layout = html.Div([
    html.H3("Minhas Ferramentas", className="mb-4 text-center"),

    # Tabela de ferramentas
    dcc.Loading(
        dbc.Card([
            dbc.CardHeader("Lista de Ferramentas", className="bg-primary text-white fw-bold"),
            dbc.CardBody(id="tabela-ferramentas", className="mt-3")
        ], className="mb-4 shadow")
    ),

    # Formulário de cadastro
    dbc.Card([
        dbc.CardHeader("Adicionar Nova Ferramenta", className="bg-success text-white fw-bold"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Nome"),
                    dbc.Input(id="input-nome-ferramenta", type="text", placeholder="Digite o nome"),
                ], md=3),
                dbc.Col([
                    dbc.Label("Descrição"),
                    dbc.Input(id="input-descricao-ferramenta", type="text", placeholder="Descrição"),
                ], md=3),
                dbc.Col([
                    dbc.Label("Categoria"),
                    dcc.Dropdown(
                        id="dropdown-categoria", 
                        options=[{"label": t.label(), "value": t.value} for t in Tool],
                        placeholder="Selecione"
                    ),
                ], md=3),
                dbc.Col([
                    dbc.Label("URL da Foto"),
                    dbc.Input(id="input-foto-ferramenta", type="url", placeholder="https://..."),
                ], md=3),
            ]),
            dbc.Button("Cadastrar", id="btn-cadastrar-ferramenta", color="success", className="mt-3")
        ])
    ], className="mb-4 shadow"),

    # Exclusão por ID
    dbc.Card([
        dbc.CardHeader("Excluir Ferramenta por ID", className="bg-danger text-white fw-bold"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("ID da Ferramenta"),
                    dbc.Input(id="input-id-excluir", type="number", placeholder="Digite o ID"),
                ], md=6),
                dbc.Col([
                    dbc.Button("Excluir", id="btn-excluir-ferramenta", color="danger", className="mt-4"),
                ], md=6)
            ])
        ])
    ], className="shadow"),

    # Mensagem de status
    dbc.Alert(id="mensagem-status", is_open=False, duration=4000,
              style={"textAlign": "center", "marginTop": "20px"}, color="info"),
], className="p-4")

@callback(
    Output("tabela-ferramentas", "children"),
    Input("btn-cadastrar-ferramenta", "n_clicks"),
    Input("btn-excluir-ferramenta", "n_clicks"),
    Input("url", "pathname"),
    State("user-store", "data"),
)
def carregar_ferramentas(n_clicks_cadastrar, n_clicks_excluir, pathname, user_data):
    if pathname != "/my_tools":
        return no_update  # Evita carregar quando estiver em outra página
    
    time.sleep(0.5)  # Simula um pequeno atraso para o carregamento

    ferramentas = tool_requests.consultar_ferramentas(id_dono=user_data["id_usuario"])
    if not ferramentas:
        return html.P("Nenhuma ferramenta cadastrada.")
    
    df = pd.DataFrame(ferramentas)
    df.drop(columns=["id_usuario", "id_categoria", "foto", "nome_usuario"], inplace=True)
    df.columns = ["Descrição", "Data Cadastro", "Disponível", "ID", "Nome", "Categoria"]
    df = df[["ID", "Nome", "Descrição", "Categoria", "Data Cadastro", "Disponível"]]
    df["Disponível"] = df["Disponível"].apply(lambda x: "Sim" if x else "Não")
    
    return dbc.Table.from_dataframe(
        pd.DataFrame(df),
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        class_name="table-sm align-middle"
    )

@callback(
    Output("mensagem-status", "children"),
    Output("mensagem-status", "color"),
    Output("mensagem-status", "is_open"),
    Input("btn-cadastrar-ferramenta", "n_clicks"),
    State("input-nome-ferramenta", "value"),
    State("input-descricao-ferramenta", "value"),
    State("dropdown-categoria", "value"),
    State("input-foto-ferramenta", "value"),
    State("user-store", "data"),
    prevent_initial_call=True
)
def cadastrar_ferramenta(n, nome, descricao, id_categoria, url_foto, user_data):
    if not nome or not descricao or not id_categoria or not url_foto:
        return "Preencha todos os campos!", "warning", True
    
    try:
        tool_requests.cadastrar_ferramenta(
            nome=nome,
            descricao=descricao,
            id_categoria=id_categoria,
            id_usuario=user_data["id_usuario"],
            foto=url_foto
        )
        return "Ferramenta cadastrada com sucesso!", "success", True
    except Exception as e:
        return f"Erro: {e}", "danger", True


@callback(
    Output("mensagem-status", "children",allow_duplicate=True),
    Output("mensagem-status", "color",allow_duplicate=True),
    Output("mensagem-status", "is_open",allow_duplicate=True),
    Input("btn-excluir-ferramenta", "n_clicks"),
    State("input-id-excluir", "value"),
    State("user-store", "data"),
    prevent_initial_call=True
)
def excluir_ferramenta(n_clicks, id_ferramenta, user_data):
    if not id_ferramenta:
        return "Informe um ID válido.", "warning", True

    try:
        tool_requests.remover_ferramenta(id_ferramenta=id_ferramenta, id_usuario=user_data["id_usuario"])
        return f"Ferramenta ID {id_ferramenta} removida com sucesso!", "success", True
    except Exception as e:
        return f"Erro ao remover: {e}", "danger", True
