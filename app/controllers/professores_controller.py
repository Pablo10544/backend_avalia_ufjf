from app.logger.logger import log
from flask import request, jsonify, abort, send_from_directory
from app.security.auth_decorators import token_required
from app.services.professores_service import ProfessoresService

class ProfessoresController:

    @staticmethod
    @token_required
    def listar_professores():
        log.info("Requisição de listar professores executada com sucesso.")
        return jsonify(ProfessoresService.listar_professores())

    @staticmethod
    @token_required
    def listar_por_nome():
        nome = request.args.get("professor_nome")
        log.info("Requisição de listar professores por nome executada com sucesso.")

        return jsonify(ProfessoresService.listar_por_nome(nome))

    @staticmethod
    @token_required
    def rejeitar_professor():
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
        aluno_id = request.args.get("aluno_id")
        curso = request.args.get("curso")
        log.info("Requisição de buscar cards executada com sucesso.")
        return jsonify(ProfessoresService.buscar_cards(aluno_id, curso))

    @staticmethod
    @token_required
    def buscar_foto():
        professor_id = request.args.get("professor_id")
        caminho, arquivo = ProfessoresService.buscar_foto(professor_id)
        log.info("Requisição de buscar foto professor executada com sucesso.")
        return send_from_directory(caminho, arquivo)
