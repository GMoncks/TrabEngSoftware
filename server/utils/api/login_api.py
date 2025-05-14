from flask import Blueprint, request
from config.paths import DATABASE_PATH
from utils.database.sql_tools import ComunicacaoBanco

login = Blueprint('login', __name__)

@login.route('/login/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    try:  
        db_comm = ComunicacaoBanco(DATABASE_PATH)
        db_comm.cadastrar_usuario(
            request.form['email'],
            request.form['password'],
            request.form['home_id'],
            request.form['name'],
            request.form['cpf'],
            request.form['phone']
            )
        return {}
    except Exception as e:
        return {"error":str(e)}, 500

@login.route('/login/validar_login', methods=['POST'])
def validar_login():
    try:  
        db_comm = ComunicacaoBanco(DATABASE_PATH)
        return db_comm.validar_login(request.form['email'], request.form['password'])
    except Exception as e:
        return {"error":str(e)}, 500

@login.route('/login/validar_usuario', methods=['GET'])
def validar_usuario():
    try:  
        db_comm = ComunicacaoBanco(DATABASE_PATH)
        return db_comm.validar_usuario(request.args['email'])
    except Exception as e:
        return {"error":str(e)}, 500

@login.route('/login/cadastrar_item', methods=['POST'])
def cadastrar_item():
    try:  
        db_comm = ComunicacaoBanco(DATABASE_PATH)
        return db_comm.cadastrar_item()
    except Exception as e:
        return {"error":str(e)}, 500