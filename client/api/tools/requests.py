from datetime import date
from utils.api.request_helper import request_helper

class ToolRequest:
    def __init__(self, baseURL):
        self.buscar_ferramentas = '/ferramentas/buscar'
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
    
    def solicitar_emprestimo(self, nome_ferramenta, data_inicio, data_fim):
        try:
            # Aqui você enviaria para a API
            print(f"Enviando empréstimo: {nome_ferramenta} de {data_inicio} até {data_fim}")
            return True
        except Exception:
            return False


