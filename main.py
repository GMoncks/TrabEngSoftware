from config.paths import DATABASE_PATH
from utils.database.sql_tools import ComunicacaoBanco
from utils.classes.user import Usuario

db_comm = ComunicacaoBanco(DATABASE_PATH)
usuario_logado = Usuario()

