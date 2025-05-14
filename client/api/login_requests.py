from utils.api.request_helper import request_helper

class LoginRequest:
    def __init__(self, baseURL):
        self.createUserUrl = '/login/cadastrar_usuario'
        self.validateLoginUrl = '/login/validar_login'
        self.validateUserUrl = '/login/validar_usuario'
        self.request = request_helper(baseURL)

    def cadastrar_usuario(self, email, password, home_id, name, cpf, phone):
        return self.request.post(self.createUserUrl, 
            {
                'email':email,
                'password':password,
                'home_id':home_id,
                'name':name,
                'cpf':cpf,
                'phone':phone,                                    
            }
        )

    def validar_login(self, email, password):
        return self.request.post(self.validateLoginUrl, {'email':email, 'password':password})

    def validar_usuario(self, nome):
        return self.request.get(self.validateUserUrl, {'name':nome})

    def cadastrar_item():
        pass





