from flask import request, jsonify, abort, send_from_directory
from app.security.auth_decorators import token_required
from app.services.professores_service import ProfessoresService

class ProfessoresController:

    @staticmethod
    @token_required
    def listar_professores():
        return jsonify(ProfessoresService.listar_professores())

    @staticmethod
    @token_required
    def listar_por_nome():
        nome = request.args.get("professor_nome")
        return jsonify(ProfessoresService.listar_por_nome(nome))

    @staticmethod
    @token_required
    def rejeitar_professor():
        professor_id = request.form.get("professor_id")
        aluno_id = request.form.get("aluno_id")

        try:
            ProfessoresService.rejeitar_professor(professor_id, aluno_id)
            return jsonify({"mensagem": "Sucesso"})
        except ValueError as e:
            abort(400, str(e))

    @staticmethod
    @token_required
    def buscar_cards():
        aluno_id = request.args.get("aluno_id")
        curso = request.args.get("curso")

        return jsonify(ProfessoresService.buscar_cards(aluno_id, curso))

    @staticmethod
    @token_required
    def buscar_foto():
        professor_id = request.args.get("professor_id")
        caminho, arquivo = ProfessoresService.buscar_foto(professor_id)
        return send_from_directory(caminho, arquivo)
