from flask import Blueprint, request, jsonify
from config.paths import DATABASE_PATH
from utils.database.sql_tools import ComunicacaoBanco

database = Blueprint('database', __name__)
banco = ComunicacaoBanco(DATABASE_PATH)

# 1. Pesquisar ferramentas por nome e disponibilidade
@database.route('/ferramentas/buscar', methods=['GET'])
def buscar_ferramentas():
    nome = request.args.get('nome', '')
    data_emprestimo = request.args.get('data_emprestimo')
    data_devolucao = request.args.get('data_devolucao')
    categoria = request.args.get('id_categoria')
    id_dono = request.args.get('id_usuario')
    try:
        ferramentas = banco.buscar_ferramentas(nome, categoria, data_emprestimo, data_devolucao, id_dono)
        return jsonify(ferramentas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 2. Registrar ferramenta no sistema
@database.route('/ferramentas/cadastrar', methods=['POST'])
def cadastrar_ferramenta():
    try:
        banco.cadastrar_ferramenta(
            int(request.form['id_usuario']),
            request.form['nome'],
            request.form['descricao'],
            request.form['id_categoria'],
            request.form['foto']
        )
        return jsonify({"message": "Ferramenta cadastrada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 5. Solicitar reserva da ferramenta
@database.route('/emprestimos/solicitar', methods=['POST'])
def solicitar_reserva():
    try:
        id_usuario = int(request.form['id_usuario'])
        id_ferramenta = int(request.form['id_ferramenta'])
        dt_emprestimo = request.form['dt_emprestimo']
        dt_devolucao = request.form['dt_devolucao']
        # 10. Verificar pendências antes de registrar reserva
        atrasos = banco.checar_atrasos(id_usuario)
        if atrasos:
            return jsonify({"error": "Usuário possui pendências/atrasos e não pode reservar novas ferramentas."}), 403
        registro_id = banco.reservar_item(id_usuario, id_ferramenta, dt_emprestimo, dt_devolucao)
        return jsonify({"message": "Reserva solicitada com sucesso!", "id_registro": registro_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 6. Autorizar ou rejeitar retirada da ferramenta
@database.route('/emprestimos/autorizar', methods=['POST'])
def autorizar_retirada():
    try:
        id_registro = int(request.form['id_registro'])
        autorizado = request.form['autorizado'].lower() == 'true'
        banco.registrar_retirada(id_registro, autorizado)
        return jsonify({"message": "Retirada autorizada!" if autorizado else "Retirada rejeitada!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 7. Confirmar devolução da ferramenta
@database.route('/emprestimos/devolver', methods=['POST'])
def confirmar_devolucao():
    try:
        id_registro = int(request.form['id_registro'])
        banco.registrar_devolucao(id_registro)
        return jsonify({"message": "Devolução registrada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 8. Remover ferramenta do sistema
@database.route('/ferramentas/remover', methods=['POST'])
def remover_ferramenta():
    # TODO : Implementar autenticação para garantir que apenas administradores possam remover ferramentas ou usuários donos da ferramenta
    try:

        banco.remover_item(
            id_ferramenta = int(request.form['id_ferramenta']),
            id_usuario = int(request.form['id_usuario'])  # ID do usuário que está removendo
            )
        
        return jsonify({"message": "Ferramenta removida com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 10. Editar descrição da ferramenta
@database.route('/ferramentas/editar', methods=['POST'])
def editar_ferramenta():
    try:
        id_ferramenta = int(request.form['id_ferramenta'])
        nova_descricao = request.form['descricao']
        banco.modificar_item(id_ferramenta, nova_descricao)
        return jsonify({"message": "Descrição atualizada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 11. Busca emprestimos ativos
@database.route('/emprestimos/buscar', methods=['GET'])
def buscar_registros():
    try:
        id_usuario = int(request.args.get('id_usuario'))
        dono = request.args.get('dono').lower() == 'true'
        registros = banco.consultar_historico(id_usuario, dono)
        return jsonify(registros), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# 12. Buscar ferramenta por id
@database.route('/ferramentas/id', methods=['GET'])
def buscar_ferramenta():
    id = request.args.get('id')
    try:
        ferramenta = banco.buscar_item(id)
        return jsonify(ferramenta), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400