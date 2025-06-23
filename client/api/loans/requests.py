from datetime import date
from utils.api.request_helper import request_helper

class LoanRequest:
    def __init__(self, baseURL):
        self.solicitar_reserva = '/emprestimos/solicitar'
        self.buscar_reserva = '/emprestimos/buscar'
        self.autorizar_reserva = '/emprestimos/autorizar'
        self.devolver_reserva = '/emprestimos/devolver'
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
        
    def buscar_emprestimos(self, id_usuario, dono):
        return self.request.get(self.buscar_reserva, 
            {
                'id_usuario':id_usuario,
                'dono':dono
            }
        )
        
    def autorizar_emprestimo(self, id_registro):
        return self.request.post(self.autorizar_reserva, 
            {
                'id_registro':id_registro,
                'autorizado':True
            }
        )
        
    def cancelar_emprestimo(self, id_registro):
        return self.request.post(self.autorizar_reserva, 
            {
                'id_registro':id_registro,
                'autorizado':False
            }
        )
    
    def devolver_emprestimo(self, id_registro):
        return self.request.post(self.devolver_reserva, 
            {
                'id_registro':id_registro
            }
        )



