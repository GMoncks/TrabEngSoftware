import hashlib
import pandas as pd
import sqlite3
import time

# O nome sempre será em letras minúsculas
# Senha será em hash
# botar docstring nas funções

# TIRAR ESSA FUNÇÃO DO MODULO DATABASE, USAR A FUNCAO PRONTA SÓ OU N FAZER NADA?
def codificar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

class ComunicacaoBanco:
    def __init__(self, db_path):
        self.db_path = db_path

    def cadastrar_usuario(self, email, password, home_id, name, cpf, phone):
        if not email or not password:
            raise ValueError("Email e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(password))
        email = email.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO "USUARIOS" ("DT_CADASTRO", "EMAIL", "SENHA", "HOME_ID", "NOME", "CPF", "PHONE") VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), email, senha_codificada, home_id, name, cpf, phone))
            conn.commit()

    def validar_login(self, email, password):
        if not email or not password:
            raise ValueError("Email e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(password))
        email = email.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "USUARIOS" WHERE EMAIL=? AND SENHA=?',
                        (email, senha_codificada))
            query_return = cursor.fetchone()
            if query_return:
                user_info = {
                    "id": query_return[0],
                    "dt_cadastro": query_return[1],
                    "email": query_return[2],
                    "senha": query_return[3],
                    "name": query_return[4],
                    "home_id": query_return[5],
                    "cpf": query_return[6],
                    "phone": query_return[7],
                    "score": query_return[8],
                    "admin": query_return[9],
                    "dt_last_acess": query_return[10]
                }
                # Atualiza o último login
                cursor.execute('UPDATE "USUARIOS" SET DT_ULTIMO_ACESSO=? WHERE ID_USUARIO=?',
                            (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), user_info["id"]))
                conn.commit()
                return user_info
            else:
                raise Exception("Usuario não existe. Verifique o login e senha.")

    def validar_usuario(self, email):
        if not email:
            raise ValueError("Email não pode ser vazio.")
        email = email.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "USUARIOS" WHERE EMAIL=?', (email,))
            usuario = cursor.fetchone()
            if usuario:
                return {"exists":True}
            else:
                return {"exists":False}

    def cadastrar_item():
        pass





