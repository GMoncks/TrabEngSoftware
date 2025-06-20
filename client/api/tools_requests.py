from datetime import date
from utils.api.request_helper import request_helper

class ToolRequest:
    def __init__(self, baseURL):
        self.request = request_helper(baseURL)

    def consultar_ferramentas(self, busca, data_inicio, data_fim, categoria, proprietario):
        """
        Simula uma consulta a uma API de ferramentas.
        """
        ferramentas = [
            {"nome": "Furadeira", "categoria": "Opção 1", "proprietario": "Opção 1", "disponibilidade": "2025-06-25"},
            {"nome": "Martelo", "categoria": "Opção 2", "proprietario": "Opção 2", "disponibilidade": "2025-06-21"},
            {"nome": "Serra Circular", "categoria": "Opção 3", "proprietario": "Opção 3", "disponibilidade": "2025-06-22"},
        ]

        # Filtros básicos (simples para exemplo)
        def corresponde(f):
            if busca and busca.lower() not in f["nome"].lower():
                return False
            if categoria and f["categoria"] != categoria:
                return False
            if proprietario and f["proprietario"] != proprietario:
                return False
            if data_inicio and f["disponibilidade"] < data_inicio:
                return False
            if data_fim and f["disponibilidade"] > data_fim:
                return False
            return True

        return [f for f in ferramentas if corresponde(f)]


