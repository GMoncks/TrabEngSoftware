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
        """
        Initialize the database communication object.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
    
    def usuario_to_dict(self, query_return):
        """
        Convert a user database row to a dictionary.

        Args:
            query_return (tuple): Row from the USUARIOS table.

        Returns:
            dict or None: Dictionary with user fields or None if input is None.
        """
        if not query_return:
            return None
        return {
            "id_usuario": query_return[0],
            "dt_cadastro": query_return[1],
            "email": query_return[2],
            "senha": query_return[3],
            "name": query_return[4],
            "home_id": query_return[5],
            "cpf": query_return[6],
            "phone": query_return[7],
            "inadimplente": query_return[8],
            "admin": query_return[9],
            "dt_last_acess": query_return[10]
        }
    
    def ferramenta_to_dict(self, query_return):
        """
        Convert a tool (ferramenta) database row to a dictionary.

        Args:
            query_return (tuple): Row from the FERRAMENTAS table.

        Returns:
            dict or None: Dictionary with ferramenta fields or None if input is None.
        """
        if not query_return:
            return None
        return {
            "id_usuario": query_return[0],
            "email": query_return[1],
            "id_ferramenta": query_return[2],
            "nome": query_return[3],
            "descricao": query_return[4],
            "dt_cadastro": query_return[5]
        }
    
    def registro_to_dict(self, query_return):
        """
        Convert a loan/record (registro) database row to a dictionary.

        Args:
            query_return (tuple): Row from the REGISTROS table.

        Returns:
            dict or None: Dictionary with registro fields or None if input is None.
        """
        if not query_return:
            return None
        return {
            "id_registro": query_return[0],
            "id_usuario": query_return[1],
            "id_ferramenta": query_return[2],
            "dt_emprestimo_prevista": query_return[3],
            "dt_devolucao_prevista": query_return[4],
            "dt_retirada": query_return[5],
            "dt_retorno": query_return[6],
            "ferramenta_disponivel": query_return[7]
        }
        
    def cadastrar_usuario(self, email, password, home_id, name, cpf, phone):
        """
        Register a new user in the database.

        Args:
            email (str): User's email.
            password (str): User's password (plain text, will be hashed).
            home_id (str): Home identifier.
            name (str): User's name.
            cpf (str): User's CPF.
            phone (str): User's phone number.

        Returns:
            None

        Workflow:
            Call this method to create a new user before any login or reservation.
        """
        senha_codificada = codificar_senha(str(password))
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO "USUARIOS" ("DT_CADASTRO", "EMAIL", "SENHA", "HOME_ID", "NOME", "CPF", "PHONE") VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (curr_time, email.lower(), senha_codificada, home_id, name, cpf, phone))
            conn.commit()
            
    def validar_login(self, email, password):
        """
        Validate user login credentials.

        Args:
            email (str): User's email.
            password (str): User's password (plain text).

        Returns:
            dict: User information if credentials are valid.

        Raises:
            Exception: If credentials are invalid.

        Workflow:
            Call this method to authenticate a user before allowing access to restricted actions.
        """
        if not email or not password:
            raise ValueError("Email e senha não podem ser vazios.")
    
        senha_codificada = codificar_senha(str(password))
    
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "USUARIOS" WHERE EMAIL=? AND SENHA=?',
                        (email.lower(), senha_codificada))
            query_return = cursor.fetchone()
    
            if query_return:
                user_info = self.usuario_to_dict(query_return)
                # Atualiza o último login
                cursor.execute('UPDATE "USUARIOS" SET DT_ULTIMO_ACESSO=? WHERE ID_USUARIO=?',
                            (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), user_info["id_usuario"]))
                conn.commit()
                return user_info
            
            else:
                raise Exception("Usuario não existe. Verifique o login e senha.")

    def validar_usuario(self, email):
        """
        Check if a user exists by email.

        Args:
            email (str): User's email.

        Returns:
            dict: {"exists": True} if user exists, {"exists": False} otherwise.
        """
        if not email:
            raise ValueError("Email não pode ser vazio.")
                
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM "USUARIOS" WHERE EMAIL=?', (email.lower(),))
            usuario = cursor.fetchone()
            
            if usuario:
                return {"exists":True}
            else:
                return {"exists":False}

    def cadastrar_ferramenta(self, id_usuario: int, nome: str, descricao: str, email: str): 
        """
        Register a new tool (ferramenta) in the database.

        Args:
            id_usuario (int): ID of the user registering the tool.
            nome (str): Name of the tool.
            descricao (str): Description of the tool.
            email (str): Email of the owner.

        Returns:
            None

        Workflow:
            Call this method to add a new tool before it can be reserved.
        """
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO FERRAMENTAS (ID_USUARIO, EMAIL, NOME, DESCRICAO, DT_CADASTRO) VALUES (?, ?, ?, ?, ?)", 
                           (id_usuario, email.lower(), nome.lower(), descricao, curr_time))
            conn.commit()

    def buscar_ferramentas_disponiveis(self, nome: str, data_emprestimo: str, data_devolucao: str):
        """
        Search for available tools for a given period and name.

        Args:
            nome (str): Tool name (partial or full, case-insensitive).
            data_emprestimo (str): Desired start date (YYYY-MM-DD HH:MM:SS).
            data_devolucao (str): Desired end date (YYYY-MM-DD HH:MM:SS).

        Returns:
            list[dict]: List of available tools as dicts, or empty list if none found.

        Workflow:
            Use this method to show users which tools are available for reservation.
        """
        if not data_emprestimo or not data_devolucao:
            raise ValueError("Data de empréstimo e devolução não podem ser vazias.")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM FERRAMENTAS WHERE NOME LIKE ? AND ID_FERRAMENTA NOT IN 
                (SELECT ID_FERRAMENTA FROM REGISTROS WHERE DT_EMPRESTIMO_PREVISTA <= ? AND DT_DEVOLUCAO_PREVISTA >= ?)""", 
                ('%' + (nome.lower() if nome else '') + '%', data_devolucao, data_emprestimo  ))

            ferramentas_disponiveis = cursor.fetchall()
            return [self.ferramenta_to_dict(x) for x in ferramentas_disponiveis] if ferramentas_disponiveis else []

    def remover_ferramenta(self, id_ferramenta: int):
        """
        Remove a tool from the database.

        Args:
            id_ferramenta (int): Tool ID.

        Returns:
            None

        Raises:
            Exception: If the tool does not exist.

        Workflow:
            Use this method to delete a tool (admin or owner only).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            
            if cursor.fetchone() is None:
                raise Exception("Ferramenta não encontrada.")
            
            cursor.execute("DELETE FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            conn.commit()

    def modificar_ferramenta(self, id_ferramenta: int, id_usuario_dono: int, nova_descricao: str):
        """
        Modify the description of a tool.

        Args:
            id_ferramenta (int): Tool ID.
            id_usuario_dono (int): ID of the user requesting the change.
            nova_descricao (str): New description.

        Returns:
            None

        Raises:
            Exception: If the tool does not exist or user is not the owner.

        Workflow:
            Use this method to update tool details.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM FERRAMENTAS WHERE ID_FERRAMENTA=?", (id_ferramenta,))
            ferramenta = cursor.fetchone()
            
            if not ferramenta:
                raise Exception("Ferramenta não encontrada.")
            
            if id_usuario_dono != self.ferramenta_to_dict(ferramenta)["id_usuario"]:
                raise Exception("Apenas o dono ou administrador da ferramenta pode modificá-la.")
            
            cursor.execute('UPDATE FERRAMENTAS SET DESCRICAO=? WHERE ID_FERRAMENTA=?',
                        (nova_descricao, id_ferramenta))
            conn.commit()

    def registrar_reserva(self, id_usuario: int, id_ferramenta: int, data_emprestimo: str, data_devolucao: str):
        """
        Register a reservation for a tool.

        Args:
            id_usuario (int): User ID making the reservation.
            id_ferramenta (int): Tool ID.
            data_emprestimo (str): Reservation start date (YYYY-MM-DD HH:MM:SS).
            data_devolucao (str): Reservation end date (YYYY-MM-DD HH:MM:SS).

        Returns:
            None

        Raises:
            Exception: If the tool is not available for the period.

        Workflow:
            Step 1: Call this method to reserve a tool.
            Step 2: Call registrar_retirada when the user picks up the tool.
            Step 3: Call registrar_devolucao when the tool is returned.
        """
        
        if not data_emprestimo or not data_devolucao:
            raise ValueError("Data de empréstimo e devolução não podem ser vazias.")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM REGISTROS
                WHERE ID_FERRAMENTA=? AND DT_EMPRESTIMO_PREVISTA <= ? AND DT_DEVOLUCAO_PREVISTA >= ?
            """, (id_ferramenta, data_devolucao, data_emprestimo))
            
            if cursor.fetchone():
                raise Exception("Ferramenta não está disponível no período solicitado.")
            
            cursor.execute("""INSERT INTO REGISTROS (ID_USUARIO, ID_FERRAMENTA, DT_EMPRESTIMO_PREVISTA, DT_DEVOLUCAO_PREVISTA) 
                           VALUES (?, ?, ?, ?)""", 
                           (id_usuario, id_ferramenta, data_emprestimo, data_devolucao))
            conn.commit()
        
    
    def registrar_retirada(self, id_registro): 
        """
        Register the pickup (retirada) of a reserved tool.

        Args:
            id_registro (int): Reservation record ID.

        Returns:
            None

        Raises:
            Exception: If the tool is not available for pickup or already picked up.

        Workflow:
            Call after registrar_reserva, when the user actually picks up the tool.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Set retirada time and mark as not available
            cursor.execute('SELECT * FROM REGISTROS WHERE ID_REGISTRO=? AND FERRAMENTA_DISPONIVEL=0', (id_registro,))

            if cursor.fetchone():
                raise Exception("Ferramenta não disponível para retirada ou já retirada.")

            cursor.execute('UPDATE REGISTROS SET DT_RETIRADA=?, FERRAMENTA_DISPONIVEL=0 WHERE ID_REGISTRO=? AND FERRAMENTA_DISPONIVEL=1', 
                           (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), id_registro))
            conn.commit()
    
    def registrar_devolucao(self, id_registro: int):
        """
        Register the return (devolução) of a tool.

        Args:
            id_registro (int): Reservation record ID.

        Returns:
            None

        Workflow:
            Call after registrar_retirada, when the user returns the tool.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE REGISTROS SET DT_RETORNO=?, FERRAMENTA_DISPONIVEL=1 
                           WHERE ID_REGISTRO=? AND FERRAMENTA_DISPONIVEL=0""",
                        (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), id_registro))
            conn.commit()        
            
            
    def penalisar_usuario(self, id_usuario: int):
        """
        Mark a user as delinquent (inadimplente).

        Args:
            id_usuario (int): User ID.

        Returns:
            None

        Workflow:
            Use this method to penalize users with overdue returns.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE USUARIOS SET INADIMPLENTE=1 WHERE ID_USUARIO=?', (id_usuario,))
            conn.commit()
    
    def regularizar_usuario(self, id_usuario: int):
        """
        Remove delinquency status from a user.

        Args:
            id_usuario (int): User ID.

        Returns:
            None

        Workflow:
            Use this method to regularize a user's status after resolving issues.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE USUARIOS SET INADIMPLENTE=0 WHERE ID_USUARIO=?', (id_usuario,))
            conn.commit()
    
    def atualizar_cadastro_usuario(self, id_usuario: int, email: str, password: str, home_id: int, name: str, cpf: str, phone: str):
        """
        Update user registration data.

        Args:
            id_usuario (int): User ID.
            email (str): New email.
            password (str): New password (plain text).
            home_id (int): New home ID.
            name (str): New name.
            cpf (str): New CPF.
            phone (str): New phone number.

        Returns:
            None

        Raises:
            ValueError: If email or password are empty.

        Workflow:
            Use this method to update user profile information.
        """
        if not email or not password:
            raise ValueError("Email e senha não podem ser vazios.")
        senha_codificada = codificar_senha(str(password))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE "USUARIOS" SET EMAIL=?, SENHA=?, HOME_ID=?, NOME=?, CPF=?, PHONE=? WHERE ID_USUARIO=?',
                        (email.lower(), senha_codificada, home_id, name.lower(), cpf, phone, id_usuario))
            conn.commit()
    
    def consultar_historico_emprestimos(self, id_usuario: int):
        """
        Get the loan/reservation history for a user.

        Args:
            id_usuario (int): User ID.

        Returns:
            list[dict]: List of reservation records as dicts, or empty list if none found.

        Workflow:
            Use this method to show a user's borrowing history.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM REGISTROS WHERE ID_USUARIO=?", (id_usuario,))
            registros = cursor.fetchall()
            return [self.registro_to_dict(x) for x in registros] if registros else []

    def checar_atrasos(self, id_usuario: int):
        """
        Check for overdue reservations for a user.

        Args:
            id_usuario (int): User ID.

        Returns:
            list[dict]: List of overdue reservation records as dicts, or empty list if none found.

        Workflow:
            Use this method to identify users with overdue returns for penalties or notifications.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            cursor.execute("""
                SELECT * FROM REGISTROS
                WHERE ID_USUARIO=? AND DT_DEVOLUCAO_PREVISTA < ? AND DT_RETORNO IS NULL""", (id_usuario, curr_time))
            registros = cursor.fetchall()
            return [self.registro_to_dict(x) for x in registros] if registros else []
