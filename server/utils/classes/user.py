

class Usuario:

    def __init__(self):
        self.id_usuario = None
        self.dt_cadastro = None
        self.nome = None
        self.senha = None
        self.score = None
        self.admin = None
        self.dt_ultimo_acesso = None

        self.logado = False

    def login(self, id_usuario, dt_cadastro, nome, senha, score, admin, dt_ultimo_acesso):
        self.id_usuario = id_usuario
        self.dt_cadastro = dt_cadastro
        self.nome = nome
        self.senha = senha
        self.score = score
        self.admin = admin
        self.dt_ultimo_acesso = dt_ultimo_acesso


        self.logado = True

    
    def logout(self):
        self.id_usuario = None
        self.dt_cadastro = None
        self.nome = None
        self.senha = None
        self.score = None
        self.admin = None
        self.dt_ultimo_acesso = None

        self.logado = False







 
    