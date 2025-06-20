from config.paths import SERVER_BASE_PATH
from utils.classes.user import Usuario
from api.login_requests import LoginRequest
from api.tools_requests import ToolRequest

login_requests = LoginRequest(SERVER_BASE_PATH)
tool_requests = ToolRequest(SERVER_BASE_PATH)
usuario_logado = Usuario()