from app.logger.logger import log
from flask import request, jsonify, abort
from app.security.auth_decorators import token_required
from app.services.avaliacao_service import AvaliacaoService

class AvaliacaoController:

    @staticmethod
    @token_required
    def criar_avaliacao():
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
        log.info("Requisição de listar comentários iniciada.")
        professor_id = request.args.get("professor_id")
        comentario = request.args.get("comentario")

        resultado = AvaliacaoService.get_comentario_id(professor_id, comentario)
        log.info("Requisição de listar comentários executada com sucesso.")

        return jsonify(resultado)