from flask import request, jsonify, abort
from app.security.auth_decorators import token_required
from app.services.avaliacao_service import AvaliacaoService

class AvaliacaoController:

    @staticmethod
    @token_required
    def criar_avaliacao():
        data = request.form

        try:
            AvaliacaoService.criar_avaliacao(data)
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def buscar_estatisticas_professor():
        professor_id = request.args.get("professor_id")
        if not professor_id:
            abort(400, "Professor inválido")

        resultado = AvaliacaoService.buscar_estatisticas_professor(professor_id)
        return jsonify(resultado)

    @staticmethod
    @token_required
    def listar_avaliacoes_professores():
        ids_param = request.args.get("ids")
        if not ids_param:
            abort(400,"parametro id esperado.")
        ids = [int(i) for i in ids_param.split(",") if i.isdigit()]

        lista = AvaliacaoService.listar_avaliacoes_professores(ids)
        return jsonify({"lista": lista})

    @staticmethod
    @token_required
    def get_comentario_id():
        professor_id = request.args.get("professor_id")
        comentario = request.args.get("comentario")

        resultado = AvaliacaoService.get_comentario_id(professor_id, comentario)
        return jsonify(resultado)