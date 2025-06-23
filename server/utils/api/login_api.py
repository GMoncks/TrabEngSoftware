from flask import Blueprint, request, jsonify
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
            request.form.get('id_casa'),   # Mudou de home_id para id_casa
            request.form['name'],
            request.form['cpf'],
            request.form['telefone']       # Mudou de phone para telefone
        )
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@login.route('/login/validar_login', methods=['POST'])
def validar_login():
    try:  
        db_comm = ComunicacaoBanco(DATABASE_PATH)
        user = db_comm.validar_login(request.form['email'], request.form['password'])
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@login.route('/login/validar_usuario', methods=['GET'])
def validar_usuario():
    try:  
        db_comm = ComunicacaoBanco(DATABASE_PATH)
        result = db_comm.validar_usuario(request.args['email'])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500