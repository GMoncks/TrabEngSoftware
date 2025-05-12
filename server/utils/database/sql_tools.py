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

    def cadastrar_usuario(self, nome, senha):
        if not nome or not senha:
            raise ValueError("Nome e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(senha))
        nome = nome.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO "USUARIOS" (NOME, SENHA) VALUES (?, ?)',
                        (nome, senha_codificada))
            cursor.execute('UPDATE "USUARIOS" SET DT_CADASTRO=? WHERE NOME=? AND SENHA=?',
                        (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), nome, senha_codificada))
            conn.commit()

    def validar_login(self, nome, senha):
        if not nome or not senha:
            raise ValueError("Nome e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(senha))
        nome = nome.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "USUARIOS" WHERE NOME=? AND SENHA=?',
                        (nome, senha_codificada))
            query_return = cursor.fetchone()
            if query_return:
                user_info = {
                    "id": query_return[0],
                    "dt_cadastro": query_return[1],
                    "nome": query_return[2],
                    "senha": query_return[3],
                    "score": query_return[4],
                    "admin": query_return[5],
                    "dt_ultimo_acesso": query_return[6]
                }
                # Atualiza o último login
                cursor.execute('UPDATE "USUARIOS" SET DT_ULTIMO_ACESSO=? WHERE ID_USUARIO=?',
                            (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), user_info["id"]))
                conn.commit()
                return user_info
            else:
                return False

    def validar_usuario(self, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        nome = nome.lower()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "USUARIOS" WHERE NOME=?', (nome,))
            usuario = cursor.fetchone()
            if usuario:
                return True
            else:
                return False

    def cadastrar_item():
        pass





