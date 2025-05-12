from utils.api.request_helper import request_helper

class LoginRequest:
    def __init__(self, baseURL):
        self.createUserUrl = '/login/cadastrar_usuario'
        self.validateLoginUrl = '/login/validar_login'
        self.validateUserUrl = '/login/validar_usuario'
        self.request = request_helper(baseURL)

    def cadastrar_usuario(self, nome, senha):
        return self.request.post(self.createUserUrl, {'name':nome, 'password':senha})

    def validar_login(self, nome, senha):
        return self.request.post(self.validateLoginUrl, {'name':nome, 'password':senha})

    def validar_usuario(self, nome):
        return self.request.get(self.validateUserUrl, {'name':nome})

    def cadastrar_item():
        pass





