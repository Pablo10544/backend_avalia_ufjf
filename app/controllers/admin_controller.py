from flask import request, jsonify, abort
from app.security.auth_decorators import token_required
from app.services.admin_service import AdminService

class AdminController:

    @staticmethod
    @token_required
    def deletar_comentario():
        avaliacao_id = request.args.get("avaliacao_id")

        try:
            AdminService.deletar_comentario(avaliacao_id)
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def aprovar_admin():
        id_pedido = request.form.get("id_pedido")

        try:
            AdminService.aprovar_admin(id_pedido)
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def deletar_todas_avaliacoes():
        AdminService.deletar_todas_avaliacoes()
        return jsonify({"mensagem": "Sucesso"})

    @staticmethod
    @token_required
    def deletar_docentes_sem_vinculo():
        AdminService.deletar_docentes_sem_vinculo()
        return jsonify({"mensagem": "Sucesso"})
