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
            "nome_usuario":  query_return[14],
            "ferramenta_disponivel": query_return[6],
            "foto": query_return[7],
            "nome_usuario_dono":  query_return[15],
            "id_usuario_dono": query_return[16],
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
            "id_ferramenta": query_return[1],
            "id_usuario": query_return[2],
            "dt_emprestimo": query_return[3],
            "dt_devolucao": query_return[4],
            "id_status": query_return[5],
            "nome_ferramenta": query_return[8],
            "id_categoria": query_return[10],
            "nome_usuario": query_return[15],
            "nome_usuario_dono": query_return[16],
            "id_usuario_dono": query_return[17],
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

    def cadastrar_ferramenta(self, id_usuario: int, nome: str, descricao: str, id_categoria: str, foto: str):
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
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO FERRAMENTAS (ID_USUARIO, NOME, DESCRICAO, ID_CATEGORIA, FOTO) VALUES (?, ?, ?, ?, ?)",
                           (id_usuario, nome, descricao, id_categoria, foto))
            conn.commit()

    def buscar_ferramentas(self, nome: str = None, id_categoria: int = None, data_emprestimo: str = None, data_devolucao: str = None, id_dono: int = None):
        """
        Busca ferramentas disponíveis para empréstimo pelo nome e categoria de interesse.

        Args:
            nome (str, optional): Nome (ou parte) da ferramenta.
            id_categoria (int, optional): tipo de ferramenta.
            data_emprestimo (str, optional): Data/hora de início do empréstimo.
            data_devolucao (str, optional): Data/hora de devolução prevista.
            id_dono (int, optional): ID do usuário dono da ferramenta.

        Returns:
            list[dict]: Lista de ferramentas disponíveis.
        """

        # Limpeza dos filtros
        if nome == "None":
            nome = None
        if id_categoria == "None":
            id_categoria = None
        if data_emprestimo == "None":
            data_emprestimo = None
        if data_devolucao == "None":
            data_devolucao = None
        if id_dono == "None":
            id_dono = None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM FERRAMENTAS JOIN CATEGORIAS ON CATEGORIAS.ID_CATEGORIA = FERRAMENTAS.ID_CATEGORIA JOIN USUARIOS ON USUARIOS.ID_USUARIO = FERRAMENTAS.ID_USUARIO"
            filters = ()

            # Se o dono for um admin, não filtra por dono
            if id_dono:
                cursor.execute("SELECT ADMIN FROM USUARIOS WHERE ID_USUARIO=?", (id_dono,))
                resultado = cursor.fetchone()
                if resultado[0] == 1:  # Se for admin, não filtra por dono
                    id_dono = None
            
            if nome or id_categoria or data_emprestimo or data_devolucao or id_dono:
                query += " WHERE"

            if nome:
                query += " lower(FERRAMENTAS.NOME) LIKE ?"
                nome = '%' + (nome.lower() if nome else '') + '%'
                filters += (nome,)

            if id_categoria:
                if nome:
                    query += " AND"
                query += " FERRAMENTAS.ID_CATEGORIA = ?"
                filters += (id_categoria,)

            if data_emprestimo and data_devolucao:
                if nome or id_categoria:
                    query += " AND"
                query += " ID_FERRAMENTA NOT IN (SELECT ID_FERRAMENTA FROM REGISTROS WHERE DT_EMPRESTIMO <= ? AND DT_DEVOLUCAO >= ?)"
                filters += (data_devolucao, data_emprestimo)
                
            if id_dono:
                if nome or id_categoria or (data_emprestimo and data_devolucao):
                    query += " AND"
                query += " FERRAMENTAS.ID_USUARIO = ?"
                filters += (id_dono,)
                
            cursor.execute(query, filters)

            ferramentas = cursor.fetchall()
            return [self.ferramenta_to_dict(x) for x in ferramentas] if ferramentas else []
        
    def buscar_item(self, id: int):
        """
        Busca ferramenta por id.

        Args:
            id (int): Id da ferramenta.

        Returns:
            list[dict]: Lista de ferramentas disponíveis.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""SELECT * FROM FERRAMENTAS JOIN CATEGORIAS ON CATEGORIAS.ID_CATEGORIA = FERRAMENTAS.ID_CATEGORIA 
                           JOIN USUARIOS ON USUARIOS.ID_USUARIO = FERRAMENTAS.ID_USUARIO
                               WHERE FERRAMENTAS.ID_FERRAMENTA = ? LIMIT 1""", (id,))

            ferramenta = cursor.fetchone()
            return self.ferramenta_to_dict(ferramenta)

    def remover_item(self, id_ferramenta: int, id_usuario: int):
        """
        Remove uma ferramenta do banco de dados se o usuário for o dono ou um admin.

        Args:
            id_ferramenta (int): ID da ferramenta.
            id_usuario (int): ID do usuário que está removendo a ferramenta.

        Raises:
            Exception: Se a ferramenta não existir ou o usuário não tiver permissão.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Verifica se a ferramenta existe e obtém o id do dono
            cursor.execute("SELECT ID_USUARIO FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            resultado = cursor.fetchone()
            if resultado is None:
                raise Exception("Ferramenta não encontrada.")
            
            id_dono = resultado[0]

            # Verifica se o usuário é admin
            cursor.execute("SELECT ADMIN FROM USUARIOS WHERE ID_USUARIO=?", (id_usuario,))
            resultado = cursor.fetchone()
            if resultado is None:
                raise Exception("Usuário não encontrado.")

            is_admin = resultado[0] == 1

            # Só permite deletar se for dono ou admin
            if id_usuario != id_dono and not is_admin:
                raise Exception("Você não tem permissão para excluir esta ferramenta.")

            # Deleta a ferramenta
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
            cursor.execute("UPDATE REGISTROS SET ID_STATUS=? WHERE ID_REGISTRO=?", 
                           (3 if autorizado else 2, id_registro))
            if autorizado:
                cursor.execute("""UPDATE FERRAMENTAS SET FERRAMENTA_DISPONIVEL = 0
                               WHERE ID_FERRAMENTA = (SELECT ID_FERRAMENTA FROM REGISTROS WHERE ID_REGISTRO=?)""", 
                               (id_registro,))
            else:
                cursor.execute("""UPDATE FERRAMENTAS SET FERRAMENTA_DISPONIVEL = 1
                               WHERE ID_FERRAMENTA = (SELECT ID_FERRAMENTA FROM REGISTROS WHERE ID_REGISTRO=?)""", 
                               (id_registro,))
                cursor.execute("UPDATE REGISTROS SET DT_DEVOLUCAO=DATETIME('now', '-3 hours') WHERE ID_REGISTRO=?", (id_registro,))
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
            cursor.execute("UPDATE REGISTROS SET ID_STATUS=4 WHERE ID_REGISTRO=?", (id_registro,))
            cursor.execute("UPDATE REGISTROS SET DT_DEVOLUCAO=DATETIME('now', '-3 hours') WHERE ID_REGISTRO=?", (id_registro,))
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
                    SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE F.ID_USUARIO=?
                """, (id_usuario,))
            else: 
                cursor.execute("""SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE R.ID_USUARIO=?""",
                (id_usuario,))
            
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
                    SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE F.ID_USUARIO=? AND R.ID_STATUS=3
                """, (id_usuario,))
            else:
                cursor.execute("""SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE R.ID_USUARIO=? AND ID_STATUS=3""", (id_usuario,))
            
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
                    SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE F.ID_USUARIO=? AND R.ID_STATUS=1
                """, (id_usuario,))
                registros = cursor.fetchall()
                return [self.registro_to_dict(x) for x in registros] if registros else []
        else:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE R.ID_USUARIO=? AND R.ID_STATUS=1
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
                    SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE F.ID_USUARIO=? AND R.DT_DEVOLUCAO < ? AND R.ID_STATUS=3
                """, (id_usuario, curr_time))
            else:
                cursor.execute("""
                    SELECT R.*, F.*, UR.NOME, UF.NOME as NOME_DONO, F.ID_USUARIO as ID_USUARIO_DONO FROM REGISTROS R
                    JOIN FERRAMENTAS F ON R.ID_FERRAMENTA = F.ID_FERRAMENTA
                    JOIN USUARIOS UF ON UF.ID_USUARIO = F.ID_USUARIO
                    JOIN USUARIOS UR ON UR.ID_USUARIO = R.ID_USUARIO
                    WHERE R.ID_USUARIO=? AND R.DT_DEVOLUCAO < ? AND R.ID_STATUS=3
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