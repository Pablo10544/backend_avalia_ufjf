from app.logger.logger import log
from flask import request, jsonify, abort
from app.security.auth_decorators import token_required
from app.services.avaliacao_service import AvaliacaoService

class AvaliacaoController:

    @staticmethod
    @token_required
    def criar_avaliacao():
        """
Cria uma nova avaliação
---
tags:
  - Avaliações
security:
  - JwtCookieAuth: []
  - BearerAuth: []
consumes:
  - application/x-www-form-urlencoded
parameters:
  - name: body
    in: formData
    type: string
    required: true
    description: "Dados da avaliação enviados via form-data"
responses:
  200:
    description: Avaliação criada com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  400:
    description: Erro de validação nos dados enviados
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de criar avaliacao iniciada.")

        data = request.form

        try:
            AvaliacaoService.criar_avaliacao(data)
            log.info("requisição de criar avaliacao com sucesso.")
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def buscar_estatisticas_professor():
        """
Busca estatísticas de avaliações de um professor
---
tags:
  - Avaliações
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
    description: Estatísticas do professor retornadas com sucesso
    schema:
      type: object
      properties:
        media:
          type: number
          example: 4.5
        total_avaliacoes:
          type: integer
          example: 12
  400:
    description: Professor inválido
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de listar estatisticas professor iniciada.")
        professor_id = request.args.get("professor_id")
        if not professor_id:
            abort(400, "Professor inválido")

        resultado = AvaliacaoService.buscar_estatisticas_professor(professor_id)
        log.info("requisição de listar estatisticas professor executada com sucesso.")

        return jsonify(resultado)

    @staticmethod
    @token_required
    def listar_avaliacoes_professores():
        """
Lista avaliações dos professores
---
tags:
  - Avaliações
security:
  - JwtCookieAuth: []
  - BearerAuth: []
parameters:
  - name: ids
    in: query
    type: string
    required: true
    description: "Lista de IDs de professores separados por vírgula (ex: 1,2,3)"
responses:
  200:
    description: Lista de avaliações retornada com sucesso
  400:
    description: Parâmetro ids ausente ou inválido
  401:
    description: Token ausente ou inválido
"""



        log.info("Requisição de listar avaliacoes iniciada.")
        ids_param = request.args.get("ids")
        if not ids_param:
            log.info("Nenhum parametro id encontrado na requisição de listar avaliacoes.")
            abort(400,"parametro id esperado.")
        ids = [int(i) for i in ids_param.split(",") if i.isdigit()]

        lista = AvaliacaoService.listar_avaliacoes_professores(ids)    
        log.info("requisição de listar avaliacoes executada com sucesso.")

        return jsonify({"lista": lista})
    

    @staticmethod
    @token_required
    def get_comentario_id():
        """
Lista comentários de um professor
---
tags:
  - Avaliações
security:
  - JwtCookieAuth: []
  - BearerAuth: []
parameters:
  - name: professor_id
    in: query
    type: integer
    required: true
    description: "ID do professor"
  - name: comentario
    in: query
    type: string
    required: false
    description: "Filtro opcional de comentário"
responses:
  200:
    description: Lista de comentários retornada com sucesso
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de listar comentários iniciada.")
        professor_id = request.args.get("professor_id")
        comentario = request.args.get("comentario")

        resultado = AvaliacaoService.get_comentario_id(professor_id, comentario)
        log.info("Requisição de listar comentários executada com sucesso.")

        return jsonify(resultado)