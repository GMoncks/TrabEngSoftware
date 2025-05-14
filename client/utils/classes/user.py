

class Usuario:

    def __init__(self):
        self.id_usuario = None
        self.dt_cadastro = None
        self.email = None
        self.password = None
        self.home_id = None
        self.name = None
        self.cpf = None
        self.phone = None
        self.score = None
        self.admin = None
        self.dt_ultimo_acesso = None

        self.logado = False

    def login(self, id_usuario, dt_cadastro, email, password, name, home_id, cpf, phone, score, admin, dt_ultimo_acesso):
        self.id_usuario = id_usuario
        self.dt_cadastro = dt_cadastro
        self.email = email
        self.password = password
        self.home_id = home_id
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.score = score
        self.admin = admin
        self.dt_ultimo_acesso = dt_ultimo_acesso

        self.logado = True

    
    def logout(self):
        self.id_usuario = None
        self.dt_cadastro = None
        self.email = None
        self.password = None
        self.home_id = None
        self.name = None
        self.cpf = None
        self.phone = None
        self.score = None
        self.admin = None
        self.dt_ultimo_acesso = None

        self.logado = False







 
    