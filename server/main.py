from flask import Flask
from config import paths
from utils.api import login_api
from config.paths import DATABASE_PATH
from utils.database.sql_tools import ComunicacaoBanco

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(        
        DATABASE_PATH = paths.DATABASE_PATH
    )
    return app

app = create_app()
app.register_blueprint(login_api.login)
app.run()