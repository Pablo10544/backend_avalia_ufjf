from flask_cors import CORS
from flasgger import Swagger
from app import create_app

# Controllers
from app.presentation.controllers.login_controller import LoginController
from app.presentation.controllers.avaliacao_controller import AvaliacaoController
from app.presentation.controllers.professores_controller import ProfessoresController
from app.presentation.controllers.admin_controller import AdminController

def create_routes(app):
    app.add_url_rule('/login', view_func=LoginController.autenticar, methods=['POST'])
    app.add_url_rule('/criar-usuario', view_func=LoginController.criar_usuario, methods=['POST'])

    app.add_url_rule('/avaliar', view_func=AvaliacaoController.criar_avaliacao, methods=['POST'])
    app.add_url_rule('/buscar-avaliacao', view_func=AvaliacaoController.buscar_estatisticas_professor, methods=['GET'])
    app.add_url_rule('/buscar-avaliacoes', view_func=AvaliacaoController.listar_avaliacoes_professores, methods=['GET'])
    app.add_url_rule('/buscar-id-avaliacao', view_func=AvaliacaoController.get_comentario_id, methods=['GET'])

    app.add_url_rule('/listar-professores', view_func=ProfessoresController.listar_professores, methods=['GET'])
    app.add_url_rule('/listar-professores-nome', view_func=ProfessoresController.listar_por_nome, methods=['GET'])
    app.add_url_rule('/buscar-cards', view_func=ProfessoresController.buscar_cards, methods=['GET'])
    app.add_url_rule('/foto-professor', view_func=ProfessoresController.buscar_foto, methods=['GET'])
    app.add_url_rule('/rejeitar-professor', view_func=ProfessoresController.rejeitar_professor, methods=['POST'])

    app.add_url_rule('/deletar-comentario', view_func=AdminController.deletar_comentario, methods=['DELETE'])
    app.add_url_rule('/aprovar-adm', view_func=AdminController.aprovar_admin, methods=['POST'])
    app.add_url_rule('/delete_review', view_func=AdminController.deletar_todas_avaliacoes, methods=['GET'])
    app.add_url_rule('/delete_nao_tive_aula', view_func=AdminController.deletar_docentes_sem_vinculo, methods=['GET'])

    app.add_url_rule('/', view_func=LoginController.pagina_padrao, methods=['GET'])
    #app.add_url_rule('/secret-key', view_func=LoginController.return_secret_key, methods=['GET'])

def main():
    app = create_app()
    CORS(app)
    create_routes(app)
    swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Backend Avalia UFJF",
        "description": "API de avaliações da UFJF",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Header Authorization (não obrigatório se cookie estiver presente)"
        }
    }
}

    swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/swagger.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger"
}
    Swagger(app,config=swagger_config,template=swagger_template)  
    app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
