from datetime import date
from utils.api.request_helper import request_helper

class ToolRequest:
    def __init__(self, baseURL):
        self.buscar_ferramentas = '/ferramentas/buscar'
        self.buscar_ferramenta = '/ferramentas/id'
        self.enviar_ferramenta = '/ferramentas/cadastrar'
        self.excluir_ferramenta = '/ferramentas/remover'
        self.editar_ferramenta = '/ferramentas/editar'
        self.request = request_helper(baseURL)

    def consultar_ferramentas(self, nome=None, id_categoria=None, data_emprestimo=None, data_devolucao=None, id_dono=None):
        """
        Consulta a API de ferramentas por nome e disponibilidade

        Retorna uma lista de dicionários com as ferramentas que atendem aos critérios de busca.
        Cada dicionário da lista tem as chaves:
        - id_ferramenta
        - nome
        - descricao
        - id_categoria
        - dt_cadastro
        - id_usuario
        - nome_usuario
        - ferramenta_disponivel
        - foto
        - nome_categoria
        
        """
        
        consulta = {}
        if nome:
            consulta['nome'] = nome
        if id_categoria:
            consulta['id_categoria'] = id_categoria
        if data_emprestimo:
            consulta['data_emprestimo'] = data_emprestimo
        if data_devolucao:
            consulta['data_devolucao'] = data_devolucao
        if id_dono:
            consulta['id_usuario'] = id_dono
        
        return self.request.get(self.buscar_ferramentas, consulta)
    
    def consultar_ferramenta(self, id):
        """
        Consulta a API de ferramenta por id
        """
        
        consulta = {'id' : id}        
        return self.request.get(self.buscar_ferramenta, consulta)

    def cadastrar_ferramenta(self, id_usuario, nome, descricao, id_categoria, foto):
        return self.request.post(self.enviar_ferramenta, {
            'id_usuario':id_usuario,
            'nome':nome,
            'descricao':descricao,
            'id_categoria':id_categoria,
            'foto':foto
        }
    )

    def remover_ferramenta(self, id_ferramenta, id_usuario):
        return self.request.post(self.excluir_ferramenta, 
            {
                'id_ferramenta':id_ferramenta,
                'id_usuario':id_usuario
            }
        )