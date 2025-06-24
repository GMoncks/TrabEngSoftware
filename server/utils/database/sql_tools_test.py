import os
import sqlite3
import tempfile
import time
import pytest
from sql_tools import ComunicacaoBanco
import sys
sys.path.append("..") 
from enums.status import LoanStatus

@pytest.fixture
def banco():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE USUARIOS (
        "ID_USUARIO" INTEGER PRIMARY KEY AUTOINCREMENT,
        "DT_CADASTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL,
        "EMAIL" VARCHAR(255) NOT NULL UNIQUE,
        "SENHA" VARCHAR(255) NOT NULL,
        "NOME" VARCHAR(255) NOT NULL,
        "ID_CASA" VARCHAR(255) DEFAULT NULL,
        "CPF" VARCHAR(255) NOT NULL UNIQUE,
        "TELEFONE" VARCHAR(255) NOT NULL UNIQUE,
        "INADIMPLENTE" INT DEFAULT 0 NOT NULL,
        "ADMIN" INT DEFAULT 0 NOT NULL,
        "DT_ULTIMO_ACESSO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL
    );
    CREATE TABLE FERRAMENTAS (
        "ID_FERRAMENTA" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        "NOME" VARCHAR(255) NOT NULL,
        "DESCRICAO" TEXT NOT NULL,
        "ID_CATEGORIA" INTEGER NOT NULL,
        "DT_CADASTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL,
        "ID_USUARIO" INTEGER NOT NULL, -- Usuário que cadastrou a ferramenta
        "FERRAMENTA_DISPONIVEL" INT DEFAULT 1 NOT NULL, -- Ferramenta disponível para empréstimo no presente momento
        "FOTO" TEXT DEFAULT NULL -- URL da foto da ferramenta
    );
    CREATE TABLE REGISTROS (
        "ID_REGISTRO" INTEGER PRIMARY KEY AUTOINCREMENT,
        "ID_FERRAMENTA" integer NOT NULL, -- Ferramenta emprestada
        "ID_USUARIO" INTEGER NOT NULL, -- Usuario que fez o empréstimo
        "DT_EMPRESTIMO" TIMESTAMP NOT NULL, -- Data do empréstimo
        "DT_DEVOLUCAO" TIMESTAMP, -- Data da devolução
        "ID_STATUS" INT DEFAULT 1 NOT NULL, -- Status do empréstimo
        "DT_REGISTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL 
    );
    CREATE TABLE CATEGORIAS (
        id_categoria   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nome_categoria TEXT    NOT NULL
    );
    INSERT INTO CATEGORIAS (nome_categoria)
    VALUES
        ('Tesoura'),
        ('Pá'),
        ('Esmerilhadeira'),
        ('Lixadeira'),
        ('Parafusadeira'),
        ('Furradeira'),
        ('Marreta'),
        ('Trena'),
        ('Chave Phillips'),
        ('Serra'),
        ('Alicate'),
        ('Chave de Fenda'),
        ('Martelo');    
    CREATE TABLE STATUS (
        ID_STATUS   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NOME_STATUS TEXT    NOT NULL
    );

    INSERT INTO STATUS (NOME_STATUS)
    VALUES
        ('Aguardando autorização'),
        ('Não Autorizado'),
        ('Emprestado'),
        ('Devolvido');    
    """)
    # Usuário 1 (dono)
    cursor.execute("INSERT INTO USUARIOS (EMAIL, SENHA, NOME, CPF, TELEFONE) VALUES (?, ?, ?, ?, ?)",
                   ("user1@example.com", "hash", "User One", "123", "555"))
    user1_id = cursor.lastrowid
    # Usuário 2 (quem pega emprestado)
    cursor.execute("INSERT INTO USUARIOS (EMAIL, SENHA, NOME, CPF, TELEFONE) VALUES (?, ?, ?, ?, ?)",
                   ("user2@example.com", "hash2", "User Two", "456", "556"))
    user2_id = cursor.lastrowid
    # Ferramenta do usuário 1
    cursor.execute("INSERT INTO FERRAMENTAS (ID_USUARIO, NOME, DESCRICAO, ID_CATEGORIA) VALUES (?, ?, ?, ?)",
                   (user1_id, "hammer", "A hammer", 1))
    ferramenta_id = cursor.lastrowid
    # Insert registro (overdue)
    init_time = "2000-01-01 10:00:00"
    end_time = "2000-01-02 10:00:00"  # Use a fixed past time for testing
    cursor.execute("""INSERT INTO REGISTROS 
        (ID_USUARIO, ID_FERRAMENTA, DT_EMPRESTIMO, DT_DEVOLUCAO, ID_STATUS)
        VALUES (?, ?, ?, ?, 3)""",
        (user2_id, ferramenta_id, init_time, end_time))
    conn.commit()
    conn.close()
    banco = ComunicacaoBanco(db_path)
    yield banco
    #os.remove(db_path)

def test_usuario_to_dict_and_ferramenta_to_dict_and_registro_to_dict(banco):
    # Test usuario_to_dict
    with sqlite3.connect(banco.db_path) as conn:
        user = conn.execute("SELECT * FROM USUARIOS WHERE EMAIL=?", ("user1@example.com",)).fetchone()
    user_dict = banco.usuario_to_dict(user)
    assert user_dict["email"] == "user1@example.com"
    # Test ferramenta_to_dict
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("""SELECT * FROM FERRAMENTAS 
            JOIN CATEGORIAS ON CATEGORIAS.ID_CATEGORIA = FERRAMENTAS.ID_CATEGORIA 
            JOIN USUARIOS ON USUARIOS.ID_USUARIO = FERRAMENTAS.ID_USUARIO 
            WHERE FERRAMENTAS.NOME=?""", ("hammer",)).fetchone()
    ferramenta_dict = banco.ferramenta_to_dict(ferramenta)
    assert ferramenta_dict["nome"] == "hammer"
    # Test registro_to_dict
    with sqlite3.connect(banco.db_path) as conn:
        user_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("user2@example.com",)).fetchone()[0]
        registro = conn.execute("""
            SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO
            FROM REGISTROS R
            JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
            JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
            JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
            WHERE R.ID_USUARIO=? LIMIT 1
        """, (user_id,)).fetchone()
    registro_dict = banco.registro_to_dict(registro)
    assert registro_dict["id_usuario"] == user_id

def test_cadastrar_usuario_and_validar_login(banco):
    banco.cadastrar_usuario("test2@email.com", "pw123", "home", "Test Two", "cpf2", "phone2")
    user = banco.validar_usuario("test2@email.com")
    assert user["exists"] is True
    login = banco.validar_login("test2@email.com", "pw123")
    assert login["email"] == "test2@email.com"

def test_validar_login_wrong_password(banco):
    banco.cadastrar_usuario("test3@email.com", "pw123", "home", "Test Three", "cpf3", "phone3")
    with pytest.raises(Exception):
        banco.validar_login("test3@email.com", "wrongpw")

def test_cadastrar_ferramenta_and_remover(banco):
    user_id = 1
    banco.cadastrar_ferramenta(user_id, "serrote", "Serrote de corte", 1, "http://example.com/serrote.jpg")
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT * FROM FERRAMENTAS WHERE NOME=?", ("serrote",)).fetchone()
        assert ferramenta is not None
        ferramenta_id = ferramenta[0]
    banco.remover_item(ferramenta_id, user_id)
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT * FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (ferramenta_id,)).fetchone()
        assert ferramenta is None

def test_remover_item_not_found(banco):
    with pytest.raises(Exception):
        banco.remover_item(999)

def test_modificar_item(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()
        ferramenta_id = ferramenta[0]
    banco.modificar_item(ferramenta_id, "Nova descrição")
    with sqlite3.connect(banco.db_path) as conn:
        desc = conn.execute("SELECT DESCRICAO FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (ferramenta_id,)).fetchone()[0]
        assert desc == "Nova descrição"

def test_modificar_item_wrong_owner(banco):
    user_id = 1
    banco.cadastrar_usuario("other@email.com", "pw", "home", "Other", "cpf4", "phone4")
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()
        ferramenta_id = ferramenta[0]
    with pytest.raises(Exception):
        banco.modificar_item(ferramenta_id, 999, "desc")

def test_buscar_ferramentas(banco):
    result = banco.buscar_ferramentas("hammer")
    assert isinstance(result, list)

def test_reservar_item_and_retirada_and_devolucao(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta_id = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()[0]
    # Reservar
    registro_id = banco.reservar_item(user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
    
    # Retirada
    banco.registrar_retirada(registro_id, autorizado=True)
    with sqlite3.connect(banco.db_path) as conn:
        disp = conn.execute("SELECT FERRAMENTA_DISPONIVEL FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (ferramenta_id,)).fetchone()[0]
        assert disp == 0
    # Devolução
    banco.registrar_devolucao(registro_id)
    with sqlite3.connect(banco.db_path) as conn:
        disp = conn.execute("SELECT FERRAMENTA_DISPONIVEL FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (ferramenta_id,)).fetchone()[0]
        assert disp == 1
        finalizado = conn.execute("SELECT ID_STATUS FROM REGISTROS WHERE ID_REGISTRO=?", (registro_id,)).fetchone()[0]
        assert finalizado == LoanStatus.DEVOLVIDO.value

def test_reservar_item_indisponivel(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta_id = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()[0]
        banco.reservar_item(user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
    # Ferramenta já está emprestada (registro inserido no setup)
    with pytest.raises(Exception):
        banco.reservar_item(user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")

def test_penalisar_and_regularizar_usuario(banco):
    user_id = 1
    banco.penalisar_usuario(user_id)
    with sqlite3.connect(banco.db_path) as conn:
        inad = conn.execute("SELECT INADIMPLENTE FROM USUARIOS WHERE ID_USUARIO=?", (user_id,)).fetchone()[0]
        assert inad == 1
    banco.regularizar_usuario(user_id)
    with sqlite3.connect(banco.db_path) as conn:
        inad = conn.execute("SELECT INADIMPLENTE FROM USUARIOS WHERE ID_USUARIO=?", (user_id,)).fetchone()[0]
        assert inad == 0

def test_atualizar_cadastro_usuario(banco):
    user_id = 1
    banco.atualizar_cadastro_usuario(user_id, "new@email.com", "pw", "newhome", "newname", "999", "888")
    with sqlite3.connect(banco.db_path) as conn:
        row = conn.execute("SELECT EMAIL, NOME, CPF, TELEFONE FROM USUARIOS WHERE ID_USUARIO=?", (user_id,)).fetchone()
        assert row[0] == "new@email.com"
        assert row[1] == "newname"
        assert row[2] == "999"
        assert row[3] == "888"

def test_atualizar_cadastro_usuario_invalid(banco):
    user_id = 1
    with pytest.raises(ValueError):
        banco.atualizar_cadastro_usuario(user_id, "", "", "home", "name", "cpf", "phone")

def test_consultar_historico_usuario(banco):
    # Usuário 2 pegou emprestado
    with sqlite3.connect(banco.db_path) as conn:
        user2_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("user2@example.com",)).fetchone()[0]
    result = banco.consultar_historico(user2_id)
    assert isinstance(result, list)
    assert len(result) > 0

def test_consultar_historico_usuario_dono(banco):
    # Usuário 1 é dono da ferramenta
    with sqlite3.connect(banco.db_path) as conn:
        user1_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("user1@example.com",)).fetchone()[0]
    result = banco.consultar_historico(user1_id, dono=True)
    assert isinstance(result, list)
    assert len(result) > 0

def test_consultar_solicitacoes_usuario(banco):
    user_id = 1
    result = banco.consultar_solicitacoes(user_id)
    assert isinstance(result, list)

def test_consultar_solicitacoes_dono(banco):
    user_id = 1
    result = banco.consultar_solicitacoes(user_id, dono=True)
    assert isinstance(result, list)

def test_checar_atrasos(banco):
    user_id = 1
    result = banco.checar_atrasos(user_id)
    assert isinstance(result, list)

def test_consultar_itens_emprestados_usuario(banco):
    # Usuário 2 pegou emprestado a ferramenta do usuário 1
    with sqlite3.connect(banco.db_path) as conn:
        user2_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("user2@example.com",)).fetchone()[0]
    result = banco.consultar_itens_emprestados(user2_id)
    assert isinstance(result, list)
    assert len(result) > 0
    # Deve conter registros onde o usuário é o tomador do empréstimo
    for reg in result:
        assert reg["id_usuario"] == user2_id

def test_consultar_itens_emprestados_dono(banco):
    # Usuário 1 é dono da ferramenta emprestada
    with sqlite3.connect(banco.db_path) as conn:
        user1_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("user1@example.com",)).fetchone()[0]
    result = banco.consultar_itens_emprestados(user1_id, dono=True)
    assert isinstance(result, list)
    assert len(result) > 0
    # Deve conter registros de ferramentas cujo dono é user1
    for reg in result:
        assert reg["id_ferramenta"] is not None

def test_validar_admin(banco):
    # Adiciona um usuário admin
    with sqlite3.connect(banco.db_path) as conn:
        conn.execute("INSERT INTO USUARIOS (EMAIL, SENHA, NOME, CPF, TELEFONE, ADMIN) VALUES (?, ?, ?, ?, ?, ?)",
                     ("admin@email.com", "hash", "Admin", "999", "888", 1))
        admin_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("admin@email.com",)).fetchone()[0]
    # Deve retornar True para admin
    assert banco.validar_admin(admin_id) is True
    # Deve retornar False para usuário comum
    with sqlite3.connect(banco.db_path) as conn:
        user_id = conn.execute("SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL=?", ("user1@example.com",)).fetchone()[0]
    assert banco.validar_admin(user_id) is False