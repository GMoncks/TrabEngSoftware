import hashlib
import sqlite3
import time

def codificar_senha(senha):
    """Gera o hash SHA-256 da senha em texto plano."""
    return hashlib.sha256(senha.encode()).hexdigest()

class ComunicacaoBanco:
    def __init__(self, db_path):
        """
        Inicializa o objeto de comunicação com o banco de dados.

        Args:
            db_path (str): Caminho para o arquivo do banco SQLite.
        """
        self.db_path = db_path

    def usuario_to_dict(self, query_return):
        """
        Converte uma linha da tabela USUARIOS em um dicionário.

        Args:
            query_return (tuple): Linha da tabela USUARIOS.

        Returns:
            dict ou None: Dicionário com os campos do usuário ou None se não houver entrada.
        """
        if not query_return:
            return None
        return {
            "id_usuario": query_return[0],
            "dt_cadastro": query_return[1],
            "email": query_return[2],
            "senha": query_return[3],
            "nome": query_return[4],
            "id_casa": query_return[5],
            "cpf": query_return[6],
            "telefone": query_return[7],
            "inadimplente": query_return[8],
            "admin": query_return[9],
            "dt_ultimo_acesso": query_return[10]
        }

    def ferramenta_to_dict(self, query_return):
        """
        Converte uma linha da tabela FERRAMENTAS em um dicionário.

        Args:
            query_return (tuple): Linha da tabela FERRAMENTAS.

        Returns:
            dict ou None: Dicionário com os campos da ferramenta ou None se não houver entrada.
        """
        if not query_return:
            return None
        return {
            "id_ferramenta": query_return[0],
            "nome": query_return[1],
            "descricao": query_return[2],
            "id_categoria": query_return[3],
            "dt_cadastro": query_return[4],
            "id_usuario": query_return[5],
            "ferramenta_disponivel": query_return[6],
            "foto": query_return[7],
            "nome_categoria":  query_return[9],
        }

    def registro_to_dict(self, query_return):
        """
        Converte uma linha da tabela REGISTROS em um dicionário.

        Args:
            query_return (tuple): Linha da tabela REGISTROS.

        Returns:
            dict ou None: Dicionário com os campos do registro ou None se não houver entrada.
        """
        if not query_return:
            return None
        return {
            "id_registro": query_return[0],
            "id_usuario": query_return[1],
            "id_ferramenta": query_return[2],
            "dt_emprestimo": query_return[3],
            "dt_devolucao": query_return[4],
            "autorizado": query_return[5],
            "finalizado": query_return[6]
        }

    def cadastrar_usuario(self, email, password, id_casa, nome, cpf, telefone):
        """
        Cadastra um novo usuário no banco de dados.

        Args:
            email (str): Email do usuário.
            password (str): Senha em texto plano.
            id_casa (str): Identificador da casa.
            nome (str): Nome do usuário.
            cpf (str): CPF do usuário.
            telefone (str): Telefone do usuário.

        Returns:
            None
        """
        senha_codificada = codificar_senha(str(password))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO USUARIOS (EMAIL, SENHA, ID_CASA, NOME, CPF, TELEFONE) VALUES (?, ?, ?, ?, ?, ?)',
                        (email.lower(), senha_codificada, id_casa, nome, cpf, telefone))
            conn.commit()

    def validar_login(self, email, password):
        """
        Valida as credenciais de login do usuário.

        Args:
            email (str): Email do usuário.
            password (str): Senha em texto plano.

        Returns:
            dict: Informações do usuário se as credenciais forem válidas.

        Raises:
            Exception: Se as credenciais forem inválidas.
        """
        if not email or not password:
            raise ValueError("Email e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(password))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM USUARIOS WHERE EMAIL=? AND SENHA=?',
                        (email.lower(), senha_codificada))
            query_return = cursor.fetchone()
            if query_return:
                user_info = self.usuario_to_dict(query_return)
                cursor.execute('UPDATE USUARIOS SET DT_ULTIMO_ACESSO=? WHERE ID_USUARIO=?',
                            (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), user_info["id_usuario"]))
                conn.commit()
                return user_info
            else:
                raise Exception("Usuário não existe. Verifique o login e senha.")

    def validar_usuario(self, email):
        """
        Verifica se um usuário existe pelo email.

        Args:
            email (str): Email do usuário.

        Returns:
            dict: {"exists": True} se existe, {"exists": False} caso contrário.
        """
        if not email:
            raise ValueError("Email não pode ser vazio.")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM USUARIOS WHERE EMAIL=?', (email.lower(),))
            usuario = cursor.fetchone()
            return {"exists": bool(usuario)}

    def cadastrar_item(self, id_usuario: int, nome: str, descricao: str, email: str):
        """
        Cadastra uma nova ferramenta no banco de dados.

        Args:
            id_usuario (int): ID do usuário dono.
            nome (str): Nome da ferramenta.
            descricao (str): Descrição da ferramenta.
            email (str): Email do dono.

        Returns:
            None
        """
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO FERRAMENTAS (ID_USUARIO, EMAIL, NOME, DESCRICAO, DT_CADASTRO) VALUES (?, ?, ?, ?, ?)",
                           (id_usuario, email.lower(), nome, descricao, curr_time))
            conn.commit()

    def buscar_itens_disponiveis(self, nome: str, id_categoria: int = None, data_emprestimo: str = None, data_devolucao: str = None):
        """
        Busca ferramentas disponíveis para empréstimo pelo nome e categoria de interesse.

        Args:
            nome (str): Nome (ou parte) da ferramenta.
            categoria (int, optional): tipo de ferramenta.

        Returns:
            list[dict]: Lista de ferramentas disponíveis.
        """
        with sqlite3.connect(self.db_path) as conn:
            nome = '%' + (nome.lower() if nome else '') + '%'
            cursor = conn.cursor()
            
            if not id_categoria and not (data_emprestimo and data_devolucao):
                cursor.execute("""SELECT * FROM FERRAMENTAS JOIN CATEGORIAS ON CATEGORIAS.ID_CATEGORIA = FERRAMENTAS.ID_CATEGORIA 
                               WHERE lower(NOME) LIKE ?""", (nome,))
            elif not (data_emprestimo and data_devolucao):
                cursor.execute("""SELECT * FROM FERRAMENTAS JOIN CATEGORIAS ON CATEGORIAS.ID_CATEGORIA = FERRAMENTAS.ID_CATEGORIA
                               WHERE lower(NOME) LIKE ? AND FERRAMENTAS.ID_CATEGORIA = ?""", (nome,id_categoria))
            else: 
                cursor.execute("""SELECT * FROM FERRAMENTAS JOIN CATEGORIAS ON CATEGORIAS.ID_CATEGORIA = FERRAMENTAS.ID_CATEGORIA
                               WHERE lower(NOME) LIKE ? AND FERRAMENTAS.ID_CATEGORIA = ? AND ID_FERRAMENTA NOT IN 
                               (SELECT ID_FERRAMENTA FROM REGISTROS WHERE DT_EMPRESTIMO <= ? AND DT_DEVOLUCAO >= ?)""", 
                               (nome, id_categoria, data_devolucao, data_emprestimo))

            ferramentas_disponiveis = cursor.fetchall()
            return [self.ferramenta_to_dict(x) for x in ferramentas_disponiveis] if ferramentas_disponiveis else []

    def remover_item(self, id_ferramenta: int):
        """
        Remove uma ferramenta do banco de dados.

        Args:
            id_ferramenta (int): ID da ferramenta.

        Returns:
            None

        Raises:
            Exception: Se a ferramenta não existir.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            if cursor.fetchone() is None:
                raise Exception("Ferramenta não encontrada.")
            cursor.execute("DELETE FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            conn.commit()

    def modificar_item(self, id_ferramenta: int, nova_descricao: str):
        """
        Modifica a descrição de uma ferramenta.

        Args:
            id_ferramenta (int): ID da ferramenta.
            id_usuario_dono (int): ID do dono.
            nova_descricao (str): Nova descrição.

        Returns:
            None

        Raises:
            Exception: Se a ferramenta não existir ou não for do usuário.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            
            if not cursor.fetchone():
                raise Exception("Ferramenta não encontrada.")
            
            cursor.execute('UPDATE FERRAMENTAS SET DESCRICAO=? WHERE ID_FERRAMENTA=?',
                        (nova_descricao, id_ferramenta))
            conn.commit()

    def reservar_item(self, id_usuario: int, id_ferramenta: int, dt_emprestimo: str, dt_devolucao: str):
        """
        Registra uma solicitação de reserva de ferramenta.

        Args:
            id_usuario (int): ID do usuário solicitante.
            id_ferramenta (int): ID da ferramenta.
            dt_emprestimo (str): Data/hora de início do empréstimo.
            dt_devolucao (str): Data/hora de devolução prevista.

        Returns:
            int: ID do registro criado.

        Raises:
            Exception: Se a ferramenta não estiver disponível.
        """
        if not (dt_emprestimo and dt_devolucao):
            raise ValueError("Data de empréstimo e devolução não podem ser vazias.")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM REGISTROS
                WHERE ID_FERRAMENTA=? AND DT_EMPRESTIMO <= ? AND DT_DEVOLUCAO >= ?
            """, (id_ferramenta, dt_devolucao, dt_emprestimo))
            
            if cursor.fetchone():
                raise Exception("Ferramenta não está disponível no período solicitado.")
            
            cursor.execute("""INSERT INTO REGISTROS (ID_USUARIO, ID_FERRAMENTA, DT_EMPRESTIMO, DT_DEVOLUCAO) 
                           VALUES (?, ?, ?, ?)""", 
                           (id_usuario, id_ferramenta, dt_emprestimo, dt_devolucao))
            id_registro = cursor.lastrowid
            conn.commit()
            return id_registro
            
    def registrar_retirada(self, id_registro: int, autorizado: bool):
        """
        Registra a Autorização ou regeição de retirada de uma ferramenta.

        Args:
            id_registro (int): ID do registro.
            autorizado (bool): True para autorizar, False para rejeitar.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Atualiza o campo AUTORIZADO na tabela REGISTROS
            cursor.execute("UPDATE REGISTROS SET AUTORIZADO=?, FINALIZADO = ? WHERE ID_REGISTRO=?", 
                           (1 if autorizado else 0, 0 if autorizado else 1, id_registro))
            if autorizado:
                cursor.execute("""UPDATE FERRAMENTAS SET FERRAMENTA_DISPONIVEL = 0
                               WHERE ID_FERRAMENTA = (SELECT ID_FERRAMENTA FROM REGISTROS WHERE ID_REGISTRO=?)""", 
                               (id_registro,))
            else:
                cursor.execute("""UPDATE FERRAMENTAS SET FERRAMENTA_DISPONIVEL = 1
                               WHERE ID_FERRAMENTA = (SELECT ID_FERRAMENTA FROM REGISTROS WHERE ID_REGISTRO=?)""", 
                               (id_registro,))
            conn.commit()

    def registrar_devolucao(self, id_registro: int):
        """
        Registra a devolução de uma ferramenta.

        Args:
            id_registro (int): ID do registro.

        Returns:
            None

        Raises:
            Exception: Se o registro já estiver finalizado.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE REGISTROS SET FINALIZADO=1 WHERE ID_REGISTRO=?", (id_registro,))
            cursor.execute("""UPDATE FERRAMENTAS SET FERRAMENTA_DISPONIVEL=1 WHERE ID_FERRAMENTA = 
                           (SELECT ID_FERRAMENTA FROM REGISTROS WHERE ID_REGISTRO=?)""", (id_registro,))
            conn.commit()

    def penalisar_usuario(self, id_usuario: int):
        """
        Marca um usuário como inadimplente.

        Args:
            id_usuario (int): ID do usuário.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE USUARIOS SET INADIMPLENTE=1 WHERE ID_USUARIO=?', (id_usuario,))
            conn.commit()

    def regularizar_usuario(self, id_usuario: int):
        """
        Remove o status de inadimplente de um usuário.

        Args:
            id_usuario (int): ID do usuário.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE USUARIOS SET INADIMPLENTE=0 WHERE ID_USUARIO=?', (id_usuario,))
            conn.commit()

    def atualizar_cadastro_usuario(self, id_usuario: int, email: str, password: str, id_casa: str, nome: str, cpf: str, telefone: str):
        """
        Atualiza os dados de cadastro de um usuário.

        Args:
            id_usuario (int): ID do usuário.
            email (str): Novo email.
            password (str): Nova senha.
            id_casa (str): Nova casa.
            nome (str): Novo nome.
            cpf (str): Novo CPF.
            telefone (str): Novo telefone.

        Returns:
            None

        Raises:
            ValueError: Se email ou senha forem vazios.
        """
        if not email or not password:
            raise ValueError("Email e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(password))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE USUARIOS SET EMAIL=?, SENHA=?, ID_CASA=?, NOME=?, CPF=?, TELEFONE=? WHERE ID_USUARIO=?',
                        (email.lower(), senha_codificada, id_casa, nome.lower(), cpf, telefone, id_usuario))
            conn.commit()

    def consultar_historico(self, id_usuario: int, dono: bool = False):
        """
        Retorna o histórico de empréstimos feitos por um usuário ou pelo dono.

        Args:
            id_usuario (int): ID do usuário.
            dono (bool): Se True, retorna apenas os registros onde o usuário é o dono da ferramenta.

        Returns:
            list[dict]: Lista de registros de empréstimo.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if dono:
                cursor.execute("""
                    SELECT REGISTROS.* FROM REGISTROS
                    JOIN FERRAMENTAS ON REGISTROS.ID_FERRAMENTA = FERRAMENTAS.ID_FERRAMENTA
                    WHERE FERRAMENTAS.ID_USUARIO=?
                """, (id_usuario,))
            else: 
                cursor.execute("SELECT * FROM REGISTROS WHERE ID_USUARIO=?", (id_usuario,))
            
            registros = cursor.fetchall()
            return [self.registro_to_dict(x) for x in registros] if registros else []
 
    def consultar_itens_emprestados(self, id_usuario: int, dono : bool = False):
        """
        Lista as ferramentas pendentes.

        Args:
            id_usuario (int): ID do usuário dono.

        Returns:
            list[dict]: Lista de registros de reservas feitas/recebidas.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if dono:
                cursor.execute("""
                    SELECT REGISTROS.* FROM REGISTROS
                    JOIN FERRAMENTAS ON REGISTROS.ID_FERRAMENTA = FERRAMENTAS.ID_FERRAMENTA
                    WHERE FERRAMENTAS.ID_USUARIO=? AND REGISTROS.FINALIZADO=0 AND REGISTROS.AUTORIZADO=1
                """, (id_usuario,))
            else:
                cursor.execute("SELECT * FROM REGISTROS WHERE ID_USUARIO=? AND FINALIZADO=0 AND AUTORIZADO=1", (id_usuario,))
            
            registros = cursor.fetchall()
            return [self.registro_to_dict(x) for x in registros] if registros else []

    def consultar_solicitacoes(self, id_usuario: int, dono: bool = False):
        """
        Lista as solicitações de empréstimo pendentes de um usuário.

        Args:
            id_usuario (int): ID do usuário dono.

        Returns:
            list[dict]: Lista de registros de solicitações pendentes.
        """
        if dono:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT REGISTROS.* FROM REGISTROS
                    JOIN FERRAMENTAS ON REGISTROS.ID_FERRAMENTA = FERRAMENTAS.ID_FERRAMENTA
                    WHERE FERRAMENTAS.ID_USUARIO=? AND REGISTROS.AUTORIZADO=0 AND REGISTROS.FINALIZADO=0
                """, (id_usuario,))
                registros = cursor.fetchall()
                return [self.registro_to_dict(x) for x in registros] if registros else []
        else:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM REGISTROS
                    WHERE ID_USUARIO=? AND AUTORIZADO=0 AND FINALIZADO=0
                """, (id_usuario,))
        
        registros = cursor.fetchall()
        return [self.registro_to_dict(x) for x in registros] if registros else []

    def checar_atrasos(self, id_usuario: int, dono : bool = False):
        """
        Verifica empréstimos em atraso de um usuário.

        Args:
            id_usuario (int): ID do usuário.

        Returns:
            list[dict]: Lista de registros em atraso.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if dono:
                cursor.execute("""
                    SELECT REGISTROS.* FROM REGISTROS
                    JOIN FERRAMENTAS ON REGISTROS.ID_FERRAMENTA = FERRAMENTAS.ID_FERRAMENTA
                    WHERE FERRAMENTAS.ID_USUARIO=? AND DT_DEVOLUCAO < ? AND FINALIZADO=0
                """, (id_usuario, curr_time))
            else:
                cursor.execute("""
                    SELECT * FROM REGISTROS
                    WHERE ID_USUARIO=? AND DT_DEVOLUCAO < ? AND FINALIZADO=0
                """, (id_usuario, curr_time))
            registros = cursor.fetchall()
            return [self.registro_to_dict(x) for x in registros] if registros else []

    def validar_admin(self, id_usuario: int):
        """
        Verifica se um usuário é administrador.

        Args:
            id_usuario (int): ID do usuário.

        Returns:
            bool: True se for administrador, False caso contrário.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ADMIN FROM USUARIOS WHERE ID_USUARIO=?", (id_usuario,))
            admin_status = cursor.fetchone()
            return bool(admin_status[0]) if admin_status else False