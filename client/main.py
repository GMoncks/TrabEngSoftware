from config.paths import SERVER_BASE_PATH
from utils.classes.user import Usuario
from api.login.requests import LoginRequest
from api.tools.requests import ToolRequest
from api.loans.requests import LoanRequest

login_requests = LoginRequest(SERVER_BASE_PATH)
tool_requests = ToolRequest(SERVER_BASE_PATH)
loan_requests = LoanRequest(SERVER_BASE_PATH)
usuario_logado = Usuario()