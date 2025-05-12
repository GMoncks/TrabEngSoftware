import hashlib
import pandas as pd
import sqlite3

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
                return True
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





