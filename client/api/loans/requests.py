from datetime import date
from utils.api.request_helper import request_helper

class LoanRequest:
    def __init__(self, baseURL):
        self.solicitar_reserva = '/emprestimos/solicitar'
        self.request = request_helper(baseURL)
    
    def solicitar_emprestimo(self, id_usuario, id_ferramenta, dt_emprestimo, dt_devolucao):
        return self.request.post(self.solicitar_reserva, 
            {
                'id_usuario':id_usuario,
                'id_ferramenta':id_ferramenta,
                'dt_emprestimo':dt_emprestimo,
                'dt_devolucao':dt_devolucao,
            }
        )


