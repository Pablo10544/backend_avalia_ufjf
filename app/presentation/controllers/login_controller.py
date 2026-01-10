from app.infrastructure.logger.logger import log
from flask import request, jsonify, make_response, abort
from app.application.services.auth_service import AuthService

class LoginController:

    @staticmethod
    def autenticar():
        """
Autentica o usuário e retorna um token JWT
---
tags:
  - Autenticação
consumes:
  - application/x-www-form-urlencoded
parameters:
  - name: email
    in: formData
    type: string
    required: true
    description: "Email do usuário"
  - name: senha
    in: formData
    type: string
    required: true
    description: "Senha do usuário"
responses:
  200:
    description: Usuário autenticado com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
        token:
          type: string
          example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  401:
    description: Credenciais inválidas
"""

        log.info("Requisição de autenticar iniciada.")
        email = request.form.get("email")
        senha = request.form.get("senha")

        try:
            token = AuthService.autenticar(email, senha)
            log.info("Requisição de autenticar executada com sucesso.")
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
        """
Cria um novo usuário
---
tags:
  - Autenticação
consumes:
  - application/x-www-form-urlencoded
parameters:
  - name: email
    in: formData
    type: string
    required: true
    description: "Email do novo usuário"
  - name: senha
    in: formData
    type: string
    required: true
    description: "Senha do novo usuário"
responses:
  200:
    description: Usuário criado com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  400:
    description: Erro ao criar usuário
"""

        log.info("Requisição de criar usuario iniciada.")
        email = request.form.get("email")
        senha = request.form.get("senha")

        try:
            AuthService.criar_usuario(email, senha)
            log.info("Requisição de criar usuario executada com sucesso.")

            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    def return_secret_key():
        return jsonify({"secret_key": AuthService.get_secret_key()})

    @staticmethod
    def pagina_padrao():
        log.info("Requisição de criar usuario executada com sucesso.")
        return jsonify({"mensagem": "Sucesso"})
