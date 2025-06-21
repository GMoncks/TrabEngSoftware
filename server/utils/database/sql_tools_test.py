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
        HOME_ID VARCHAR(255),
        CPF VARCHAR(255) NOT NULL UNIQUE,
        PHONE VARCHAR(255) NOT NULL UNIQUE,
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
        DT_CADASTRO TIMESTAMP DEFAULT current_timestamp
    );
    CREATE TABLE REGISTROS (
        ID_REGISTRO INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_USUARIO INTEGER NOT NULL,
        ID_FERRAMENTA INTEGER NOT NULL,
        DT_EMPRESTIMO_PREVISTA TIMESTAMP,
        DT_DEVOLUCAO_PREVISTA TIMESTAMP,
        DT_RETIRADA TIMESTAMP DEFAULT NULL,
        DT_RETORNO TIMESTAMP DEFAULT NULL,
        FERRAMENTA_DISPONIVEL INT DEFAULT 1 NOT NULL
    );
    """)
    # Insert user and ferramenta
    cursor.execute("INSERT INTO USUARIOS (EMAIL, SENHA, NOME, CPF, PHONE) VALUES (?, ?, ?, ?, ?)",
                   ("user1@example.com", "hash", "User One", "123", "555"))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO FERRAMENTAS (ID_USUARIO, EMAIL, NOME, DESCRICAO) VALUES (?, ?, ?, ?)",
                   (user_id, "user1@example.com", "hammer", "A hammer"))
    ferramenta_id = cursor.lastrowid
    # Insert registro (overdue)
    past_time = "2000-01-01 10:00:00"
    cursor.execute("""INSERT INTO REGISTROS 
        (ID_USUARIO, ID_FERRAMENTA, DT_EMPRESTIMO_PREVISTA, DT_DEVOLUCAO_PREVISTA, FERRAMENTA_DISPONIVEL)
        VALUES (?, ?, ?, ?, 0)""",
        (user_id, ferramenta_id, past_time, past_time))
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
    assert registro_dict["id_usuario"] == 1

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
    banco.cadastrar_ferramenta(user_id, "serrote", "Serrote de corte", "user1@example.com")
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT * FROM FERRAMENTAS WHERE NOME=?", ("serrote",)).fetchone()
        assert ferramenta is not None
        ferramenta_id = ferramenta[0]
    banco.remover_ferramenta(ferramenta_id)
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT * FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (ferramenta_id,)).fetchone()
        assert ferramenta is None

def test_remover_ferramenta_not_found(banco):
    with pytest.raises(Exception):
        banco.remover_ferramenta(999)

def test_modificar_ferramenta(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()
        ferramenta_id = ferramenta[0]
    banco.modificar_ferramenta(ferramenta_id, user_id, "Nova descrição")
    with sqlite3.connect(banco.db_path) as conn:
        desc = conn.execute("SELECT DESCRICAO FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (ferramenta_id,)).fetchone()[0]
        assert desc == "Nova descrição"

def test_modificar_ferramenta_wrong_owner(banco):
    user_id = 1
    banco.cadastrar_usuario("other@email.com", "pw", "home", "Other", "cpf4", "phone4")
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()
        ferramenta_id = ferramenta[0]
    with pytest.raises(Exception):
        banco.modificar_ferramenta(ferramenta_id, 999, "desc")

def test_buscar_ferramentas_disponiveis(banco):
    result = banco.buscar_ferramentas_disponiveis("hammer", "1999-01-01 00:00:00", "1999-01-02 00:00:00")
    assert isinstance(result, list) or result is None

def test_buscar_ferramentas_disponiveis_invalid(banco):
    with pytest.raises(ValueError):
        banco.buscar_ferramentas_disponiveis("hammer", "", "")

def test_registrar_reserva_and_devolucao(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta_id = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()[0]
    banco.registrar_reserva(user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
    with sqlite3.connect(banco.db_path) as conn:
        registro = conn.execute("SELECT * FROM REGISTROS WHERE ID_USUARIO=? AND ID_FERRAMENTA=?",
                                (user_id, ferramenta_id)).fetchone()
        assert registro is not None
        id_registro = registro[0]
    banco.registrar_devolucao(id_registro)
    with sqlite3.connect(banco.db_path) as conn:
        devolucao = conn.execute("SELECT DT_RETORNO FROM REGISTROS WHERE ID_REGISTRO=?", (id_registro,)).fetchone()[0]
        assert devolucao is not None

def test_registrar_reserva_invalid(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta_id = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()[0]
    with pytest.raises(ValueError):
        banco.registrar_reserva(user_id, ferramenta_id, "", "")

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
    banco.atualizar_cadastro_usuario(user_id, "new@email.com", "pw", 1, "newname", "999", "888")
    with sqlite3.connect(banco.db_path) as conn:
        row = conn.execute("SELECT EMAIL, NOME, CPF, PHONE FROM USUARIOS WHERE ID_USUARIO=?", (user_id,)).fetchone()
        assert row[0] == "new@email.com"
        assert row[1] == "newname"
        assert row[2] == "999"
        assert row[3] == "888"

def test_atualizar_cadastro_usuario_invalid(banco):
    user_id = 1
    with pytest.raises(ValueError):
        banco.atualizar_cadastro_usuario(user_id, "", "", 1, "name", "cpf", "phone")

def test_consultar_historico_emprestimos(banco):
    user_id = 1
    result = banco.consultar_historico_emprestimos(user_id)
    assert result is not None

def test_checar_atrasos_returns_overdue(banco):
    user_id = 1
    result = banco.checar_atrasos(user_id)
    assert result is not False

def test_checar_atrasos_returns_none_for_no_overdue(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        conn.execute("UPDATE REGISTROS SET DT_RETORNO = ?", (time.strftime('%Y-%m-%d %H:%M:%S'),))
    result = banco.checar_atrasos(user_id)
    assert result == [] 

def test_validar_usuario_exists(banco):
    result = banco.validar_usuario("user1@example.com")
    assert result["exists"] is True

def test_validar_usuario_not_exists(banco):
    result = banco.validar_usuario("notfound@example.com")
    assert result["exists"] is False

def test_registrar_retirada(banco):
    user_id = 1
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta_id = conn.execute("SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)).fetchone()[0]
    # Register a new reserva for a future period
    banco.registrar_reserva(user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
    with sqlite3.connect(banco.db_path) as conn:
        registro = conn.execute(
            "SELECT ID_REGISTRO FROM REGISTROS WHERE ID_USUARIO=? AND ID_FERRAMENTA=? AND DT_EMPRESTIMO_PREVISTA=? AND DT_DEVOLUCAO_PREVISTA=?",
            (user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
        ).fetchone()
        id_registro = registro[0]
    banco.registrar_retirada(id_registro)
    with sqlite3.connect(banco.db_path) as conn:
        retirada = conn.execute("SELECT DT_RETIRADA FROM REGISTROS WHERE ID_REGISTRO=?", (id_registro,)).fetchone()[0]
        assert retirada is not None

def test_reserva_retirada_devolucao_workflow(banco):
    user_id = 1
    # Get ferramenta id
    with sqlite3.connect(banco.db_path) as conn:
        ferramenta_id = conn.execute(
            "SELECT ID_FERRAMENTA FROM FERRAMENTAS WHERE NOME=?", ("hammer",)
        ).fetchone()[0]

    # 1. Registrar reserva
    banco.registrar_reserva(user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
    with sqlite3.connect(banco.db_path) as conn:
        registro = conn.execute(
            "SELECT ID_REGISTRO, FERRAMENTA_DISPONIVEL, DT_RETIRADA, DT_RETORNO FROM REGISTROS WHERE ID_USUARIO=? AND ID_FERRAMENTA=? AND DT_EMPRESTIMO_PREVISTA=? AND DT_DEVOLUCAO_PREVISTA=?",
            (user_id, ferramenta_id, "2025-01-01 10:00:00", "2025-01-02 10:00:00")
        ).fetchone()
        id_registro = registro[0]
        assert registro[1] == 1  # FERRAMENTA_DISPONIVEL should be 1 (available)
        assert registro[2] is None  # DT_RETIRADA should be None
        assert registro[3] is None  # DT_RETORNO should be None

    # 2. Registrar retirada
    banco.registrar_retirada(id_registro)
    with sqlite3.connect(banco.db_path) as conn:
        registro = conn.execute(
            "SELECT FERRAMENTA_DISPONIVEL, DT_RETIRADA, DT_RETORNO FROM REGISTROS WHERE ID_REGISTRO=?",
            (id_registro,)
        ).fetchone()
        assert registro[0] == 0  # FERRAMENTA_DISPONIVEL should be 0 (not available)
        assert registro[1] is not None  # DT_RETIRADA should be set
        assert registro[2] is None  # DT_RETORNO should still be None

    # 3. Registrar devolução
    banco.registrar_devolucao(id_registro)
    with sqlite3.connect(banco.db_path) as conn:
        registro = conn.execute(
            "SELECT FERRAMENTA_DISPONIVEL, DT_RETIRADA, DT_RETORNO FROM REGISTROS WHERE ID_REGISTRO=?",
            (id_registro,)
        ).fetchone()
        assert registro[0] == 1  # FERRAMENTA_DISPONIVEL should be 1 (available again)
        assert registro[1] is not None  # DT_RETIRADA should still be set
        assert registro[2] is not None  # DT_RETORNO should be set