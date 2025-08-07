import app
from app.models import schema
from flask import request, jsonify

class Login:
    @staticmethod
    def autenticar():
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = schema.Usuario.query.filter_by(email=email).first()
        if usuario:
            print("Encontrado")
            if usuario.check_senha(senha):
                return jsonify({'mensagem':'Sucesso'})
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