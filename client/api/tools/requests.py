from datetime import date
from utils.api.request_helper import request_helper

class ToolRequest:
    def __init__(self, baseURL):
        self.buscar_ferramentas = '/ferramentas/buscar'
        self.buscar_ferramenta = '/ferramentas/id'
        self.cadastrar_ferramenta = '/ferramentas/cadastrar'
        self.remover_ferramenta = '/ferramentas/remover'
        self.editar_ferramenta = '/ferramentas/editar'
        self.request = request_helper(baseURL)

    def consultar_ferramentas(self, nome, id_categoria, data_emprestimo, data_devolucao):
        """
        Consulta a API de ferramentas por nome e disponibilidade
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
        
        return self.request.get(self.buscar_ferramentas, consulta)
    
    def consultar_ferramenta(self, id):
        """
        Consulta a API de ferramenta por id
        """
        
        consulta = {'id' : id}        
        return self.request.get(self.buscar_ferramenta, consulta)

