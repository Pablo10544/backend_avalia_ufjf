from flask import request, jsonify, make_response, abort
from app.services.auth_service import AuthService

class LoginController:

    @staticmethod
    def autenticar():
        email = request.form.get("email")
        senha = request.form.get("senha")

        try:
            token = AuthService.autenticar(email, senha)
            response = make_response(jsonify({
                "mensagem": "Sucesso",
                "token": token
            }))
            response.set_cookie("jwt_token", token)
            return response
        except ValueError as e:
            abort(401, str(e))

    @staticmethod
    def criar_usuario():
        email = request.form.get("email")
        senha = request.form.get("senha")

        try:
            AuthService.criar_usuario(email, senha)
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    def return_secret_key():
        return jsonify({"secret_key": AuthService.get_secret_key()})

    @staticmethod
    def pagina_padrao():
        return jsonify({"mensagem": "Sucesso"})
