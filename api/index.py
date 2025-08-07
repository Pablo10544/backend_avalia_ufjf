from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import admin, avaliacao, create_app, login, professores

# Cria a aplicação Flask
app = create_app()
CORS(app)

# Registra as rotas
app.add_url_rule('/login', view_func=login.Login.autenticar, methods=['POST'])
app.add_url_rule('/criar-usuario', view_func=login.Login.criarUsuario, methods=['POST'])
app.add_url_rule('/avaliar', view_func=avaliacao.Avaliacao.Avaliar, methods=['POST'])
app.add_url_rule('/buscar-avaliacao', view_func=avaliacao.Avaliacao.BuscarAvaliacaoGeralProfessor, methods=['GET'])
app.add_url_rule('/listar-professores', view_func=professores.Professores.listar_professores, methods=['GET'])
app.add_url_rule('/listar-professores-nome', view_func=professores.Professores.list_professores_por_nome, methods=['GET'])
app.add_url_rule('/rejeitar-professor', view_func=professores.Professores.rejeitar_professor, methods=['POST'])
app.add_url_rule('/buscar-cards', view_func=professores.Professores.buscar_cards_professor, methods=['GET'])
app.add_url_rule('/deletar-comentario', view_func=admin.Admin.deletar_comentario, methods=['DELETE'])
app.add_url_rule('/aprovar-adm', view_func=admin.Admin.aprovar_adm, methods=['POST'])
app.add_url_rule('/foto-professor', view_func=professores.Professores.foto, methods=['GET'])
app.add_url_rule('/buscar-avaliacoes', view_func=avaliacao.Avaliacao.BuscarAvaliacoesProfesores, methods=['GET'])
app.add_url_rule('/', view_func=login.Login.paginaPadrao, methods=['GET'])

# 🔥 Linha obrigatória para Vercel identificar a aplicação
handler = app
