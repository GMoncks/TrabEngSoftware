
import time

class Usuario:

    def __init__(self):
        self.id_usuario = None
        self.nome = None
        self.senha = None
        self.logado = False
        # self.permissao = None
        self.ultimo_login = None

    def login(self, id_usuario, nome, senha):
        self.id_usuario = id_usuario
        self.nome = nome
        self.senha = senha
        self.logado = True
        # self.permissao = "admin"
        self.ultimo_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def logout(self):
        self.id_usuario = None
        self.nome = None
        self.senha = None
        self.logado = False
        # self.permissao = None
        self.ultimo_login = None





 
    