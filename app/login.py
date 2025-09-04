from datetime import datetime, timedelta
from functools import wraps
from time import timezone
import jwt
import app
from app import settings
from app.models import schema
from flask import make_response, request, jsonify

class Login:
    @staticmethod
    def autenticar():
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = schema.Usuario.query.filter_by(email=email).first()
        if usuario:
            print("Encontrado")
            if usuario.check_senha(senha):
                token = jwt.encode({'public_id': usuario.id, 'exp': datetime.now() + timedelta(hours=4)},
                settings.SECRET_KEY, algorithm="HS256")
                response = make_response(jsonify({'mensagem':'Sucesso','token':token}))
                response.set_cookie('jwt_token',token)
                return response
                 
            return jsonify({'mensagem':'erro'})
        else:
            print("Usuário não encontrado")
            return jsonify({'mensagem':'erro'})
        
        # mudar para criar aluno ao inves de usuario
    def criarUsuario():
        email = request.form.get('email')
        senha = request.form.get('senha')
        if not email or not senha:
            return jsonify({'mensagem':'erro'})
        usuarioExiste = schema.Usuario.query.filter_by(email=email).first()
        if usuarioExiste:
            return jsonify({'mensagem':'erro'})
        tipo = 'usuario'
        usuario = schema.Usuario(email,senha,tipo)
        usuario.salvar()
        return jsonify({'mensagem':'Sucesso'})
    @staticmethod
    def returnSecretKey():
        lista = []
        for chave, valor in settings.SECRET_KEY.items():
            lista.append(f"{chave}: {valor}")
        return jsonify({'secret_key':lista})
    @staticmethod
    def paginaPadrao():
        return jsonify({'mensagem':'Sucesso'})

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get('jwt_token')

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            return f( *args, **kwargs)

        return decorated
