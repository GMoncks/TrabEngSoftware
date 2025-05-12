from config.paths import SERVER_BASE_PATH
from utils.classes.user import Usuario
from api.login_requests import LoginRequest

login_requests = LoginRequest(SERVER_BASE_PATH)
usuario_logado = Usuario()