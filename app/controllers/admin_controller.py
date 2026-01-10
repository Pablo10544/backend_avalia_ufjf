from flask import request, jsonify, abort
from app.logger.logger import log
from app.security.auth_decorators import token_required
from app.services.admin_service import AdminService

class AdminController:

    @staticmethod
    @token_required
    def deletar_comentario():
        """
Deleta um comentário por ID
---
tags:
  - Administração
security:
  - JwtCookieAuth: []
  - BearerAuth: []
parameters:
  - name: avaliacao_id
    in: query
    type: integer
    required: true
    description: "ID da avaliação a ser deletada"
responses:
  200:
    description: Comentário deletado com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  400:
    description: Erro ao deletar comentário
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de deletar comentario iniciada.")
        avaliacao_id = request.args.get("avaliacao_id")

        try:
            AdminService.deletar_comentario(avaliacao_id)
            log.info("requisição de deletar comentario executada com sucesso.")
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def aprovar_admin():
        """
Aprova um pedido de administrador
---
tags:
  - Administração
security:
  - JwtCookieAuth: []
  - BearerAuth: []
consumes:
  - application/x-www-form-urlencoded
parameters:
  - name: id_pedido
    in: formData
    type: integer
    required: true
    description: "ID do pedido de aprovação de administrador"
responses:
  200:
    description: Pedido aprovado com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  400:
    description: Erro ao aprovar administrador
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de aprovar admin iniciada.")

        id_pedido = request.form.get("id_pedido")

        try:
            AdminService.aprovar_admin(id_pedido)
            log.info("requisição de aprovar admin executada com sucesso.")
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def deletar_todas_avaliacoes():
        """
Deleta todas as avaliações cadastradas
---
tags:
  - Administração
security:
  - JwtCookieAuth: []
  - BearerAuth: []
responses:
  200:
    description: Todas as avaliações foram deletadas com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de deletar todas avaliacoes iniciada.")
        AdminService.deletar_todas_avaliacoes()
        log.info("requisição de deletar todas avaliacoes executada com sucesso.")
        return jsonify({"mensagem": "Sucesso"})

    @staticmethod
    @token_required
    def deletar_docentes_sem_vinculo():
        """
Deleta docentes sem vínculo com avaliações
---
tags:
  - Administração
security:
  - JwtCookieAuth: []
  - BearerAuth: []
responses:
  200:
    description: Docentes sem vínculo deletados com sucesso
    schema:
      type: object
      properties:
        mensagem:
          type: string
          example: "Sucesso"
  401:
    description: Token ausente ou inválido
"""

        log.info("Requisição de deletar docentes sem vinculo iniciada.")
        AdminService.deletar_docentes_sem_vinculo()
        log.info("requisição de deletar docente sem vinculo executada com sucesso.")

        return jsonify({"mensagem": "Sucesso"})
