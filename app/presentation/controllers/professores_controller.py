from app.infrastructure.logger.logger import log
from flask import request, jsonify, abort, send_from_directory
from app.infrastructure.security.auth_decorators import token_required
from app.application.services.professores_service import ProfessoresService

class ProfessoresController:

    @staticmethod
    @token_required
    def listar_professores():
        """
Lista todos os professores
---
tags:
  - Professores
security:
  - JwtCookieAuth: []
  - BearerAuth: []
responses:
  200:
    description: Lista de professores retornada com sucesso
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de listar professores executada com sucesso.")
        return jsonify(ProfessoresService.listar_professores())

    @staticmethod
    @token_required
    def listar_por_nome():
        """
Lista professores filtrando pelo nome
---
tags:
  - Professores
security:
  - JwtCookieAuth: []
  - BearerAuth: []
parameters:
  - name: professor_nome
    in: query
    type: string
    required: true
    description: "Nome ou parte do nome do professor"
responses:
  200:
    description: Lista de professores retornada com sucesso
  401:
    description: Token ausente ou inválido
"""

        nome = request.args.get("professor_nome")
        log.info("Requisição de listar professores por nome executada com sucesso.")

        return jsonify(ProfessoresService.listar_por_nome(nome))

    @staticmethod
    @token_required
    def rejeitar_professor():
        """
Rejeita um professor para um aluno
---
tags:
  - Professores
security:
  - JwtCookieAuth: []
  - BearerAuth: []
consumes:
  - application/x-www-form-urlencoded
parameters:
  - name: professor_id
    in: formData
    type: integer
    required: true
    description: "ID do professor"
  - name: aluno_id
    in: formData
    type: integer
    required: true
    description: "ID do aluno"
responses:
  200:
    description: Professor rejeitado com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  400:
    description: Erro ao rejeitar professor
  401:
    description: Token ausente ou inválido
"""

        professor_id = request.form.get("professor_id")
        aluno_id = request.form.get("aluno_id")

        try:
            ProfessoresService.rejeitar_professor(professor_id, aluno_id)
            log.info("Requisição de rejeitar professores executada com sucesso.")
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def buscar_cards():
        """
Busca cards de professores para um aluno
---
tags:
  - Professores
security:
  - JwtCookieAuth: []
  - BearerAuth: []
parameters:
  - name: aluno_id
    in: query
    type: integer
    required: true
    description: "ID do aluno"
  - name: curso
    in: query
    type: string
    required: false
    description: "Curso para filtragem"
responses:
  200:
    description: Cards retornados com sucesso
  401:
    description: Token ausente ou inválido
"""

        aluno_id = request.args.get("aluno_id")
        curso = request.args.get("curso")
        log.info("Requisição de buscar cards executada com sucesso.")
        return jsonify(ProfessoresService.buscar_cards(aluno_id, curso))

    @staticmethod
    def buscar_foto():
        """
Busca a foto de um professor
---
tags:
  - Professores
security:
  - JwtCookieAuth: []
  - BearerAuth: []
parameters:
  - name: professor_id
    in: query
    type: integer
    required: true
    description: "ID do professor"
responses:
  200:
    description: Foto do professor retornada com sucesso
    schema:
      type: file
  401:
    description: Token ausente ou inválido
"""

        professor_id = request.args.get("professor_id")
        caminho, arquivo = ProfessoresService.buscar_foto(professor_id)
        log.info("Requisição de buscar foto professor executada com sucesso.")
        return send_from_directory(caminho, arquivo)
