import os
import sqlite3
import tempfile
import time
import pytest
from sql_tools import ComunicacaoBanco

@pytest.fixture
def banco():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE USUARIOS (
        ID_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT,
        DT_CADASTRO TIMESTAMP DEFAULT current_timestamp,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        SENHA VARCHAR(255) NOT NULL,
        NOME VARCHAR(255) NOT NULL,
        ID_CASA VARCHAR(255),
        CPF VARCHAR(255) NOT NULL UNIQUE,
        TELEFONE VARCHAR(255) NOT NULL UNIQUE,
        INADIMPLENTE INT DEFAULT 0 NOT NULL,
        ADMIN INT DEFAULT 0 NOT NULL,
        DT_ULTIMO_ACESSO TIMESTAMP DEFAULT current_timestamp
    );
    CREATE TABLE FERRAMENTAS (
        ID_FERRAMENTA INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_USUARIO INTEGER NOT NULL,
        EMAIL VARCHAR(255) NOT NULL,
        NOME VARCHAR(255) NOT NULL,
        DESCRICAO TEXT NOT NULL,
        DT_CADASTRO TIMESTAMP DEFAULT current_timestamp,
        FERRAMENTA_DISPONIVEL INT DEFAULT 1 NOT NULL
    );
    CREATE TABLE REGISTROS (
        ID_REGISTRO INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_USUARIO INTEGER NOT NULL,
        ID_FERRAMENTA INTEGER NOT NULL,
        DT_EMPRESTIMO TIMESTAMP,
        DT_DEVOLUCAO TIMESTAMP,
        AUTORIZADO INT DEFAULT 0 NOT NULL,
        FINALIZADO INT DEFAULT 0 NOT NULL
    );
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
    cursor.execute("INSERT INTO FERRAMENTAS (ID_USUARIO, EMAIL, NOME, DESCRICAO) VALUES (?, ?, ?, ?)",
                   (user1_id, "user1@example.com", "hammer", "A hammer"))
    ferramenta_id = cursor.lastrowid
    # Insert registro (overdue)
    init_time = "2000-01-01 10:00:00"
    end_time = "2000-01-02 10:00:00"  # Use a fixed past time for testing
    cursor.execute("""INSERT INTO REGISTROS 
        (ID_USUARIO, ID_FERRAMENTA, DT_EMPRESTIMO, DT_DEVOLUCAO, AUTORIZADO, FINALIZADO)
        VALUES (?, ?, ?, ?, 1, 0)""",
        (user2_id, ferramenta_id, init_time, end_time))
    conn.commit()
    conn.close()
    banco = ComunicacaoBanco(db_path)
    yield banco
    os.remove(db_path)

def test_usuario_to_dict_and_ferramenta_to_dict_and_registro_to_dict(banco):
    # Test usuario_to_dict
    with sqlite3.connect(banco.db_path) as conn:
        user = conn.execute("SELECT * FROM USUARIOS WHERE EMAIL=?", ("user1@example.com",)).fetchone()
    user_dict = banco.usuario_to_dict(user)
    assert user_dict["email"] == "user1@example.com"
    # Test ferramenta_to_dict
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT * FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()
    ferramenta_dict = banco.ferramenta_to_dict(ferramenta)
    assert ferramenta_dict["nome"] == "hammer"
    # Test registro_to_dict
    with sqlite3.connect(banco.db_path) as conn:
        registro = conn.execute("SELECT * FROM REGISTROS").fetchone()
    registro_dict = banco.registro_to_dict(registro)
    assert registro_dict["id_usuario"] == 2

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

def test_cadastrar_item_and_remover(banco):
    user_id = 1
    banco.cadastrar_item(user_id, "serrote", "Serrote de corte", "user1@example.com")
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT * FROM FERRAMENTAS WHERE NOME=?", ("serrote",)).fetchone()
        assert ferramenta is not None
        ferramenta_id = ferramenta[0]
    banco.remover_item(ferramenta_id)
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

def test_buscar_itens_disponiveis(banco):
    result = banco.buscar_itens_disponiveis("hammer")
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
        finalizado = conn.execute("SELECT FINALIZADO FROM REGISTROS WHERE ID_REGISTRO=?", (registro_id,)).fetchone()[0]
        assert finalizado == 1

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