from utils.api.request_helper import request_helper

class LoginRequest:
    def __init__(self, baseURL):
        self.createUserUrl = '/login/cadastrar_usuario'
        self.validateLoginUrl = '/login/validar_login'
        self.validateUserUrl = '/login/validar_usuario'
        self.validateAdminUrl = '/usuarios/validar_admin'
        self.request = request_helper(baseURL)

    def cadastrar_usuario(self, email, password, id_casa, name, cpf, telefone):
        return self.request.post(self.createUserUrl, 
            {
                'email':email,
                'password':password,
                'id_casa':id_casa,
                'name':name,
                'cpf':cpf,
                'telefone':telefone,                                    
            }
        )

    def validar_login(self, email, password):
        return self.request.post(self.validateLoginUrl, {'email':email, 'password':password})

    def validar_usuario(self, nome):
        return self.request.get(self.validateUserUrl, {'email':nome})

    def validar_admin(self, id_usuario):
        return self.request.get(self.validateAdminUrl, {'id_usuario':id_usuario})





