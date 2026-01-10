from flask import request, jsonify, abort
from app.logger.logger import log
from app.security.auth_decorators import token_required
from app.services.admin_service import AdminService

class AdminController:

    @staticmethod
    @token_required
    def deletar_comentario():
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
        log.info("Requisição de deletar todas avaliacoes iniciada.")
        AdminService.deletar_todas_avaliacoes()
        log.info("requisição de deletar todas avaliacoes executada com sucesso.")
        return jsonify({"mensagem": "Sucesso"})

    @staticmethod
    @token_required
    def deletar_docentes_sem_vinculo():
        log.info("Requisição de deletar docentes sem vinculo iniciada.")
        AdminService.deletar_docentes_sem_vinculo()
        log.info("requisição de deletar docente sem vinculo executada com sucesso.")

        return jsonify({"mensagem": "Sucesso"})
