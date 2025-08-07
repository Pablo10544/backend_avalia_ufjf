from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Instanciar as extensões fora da função create_app
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurações do Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avaliufjf.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'chave_super_secreta'
    app.config['JWT_SECRET_KEY'] = 'jwt_super_secreta'

    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)

    # Importar os modelos para garantir que as tabelas sejam registradas
    from app.models import schema

    # Registrar blueprints de rotas (você pode ativar isso conforme cria as rotas)
    # from app.routes.auth_routes import auth_bp
    # app.register_blueprint(auth_bp)

    return app
