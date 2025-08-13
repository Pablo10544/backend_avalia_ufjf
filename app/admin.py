from app import db, create_app
from app.models import schema
from flask import request, jsonify

class Admin():
    @staticmethod
    def deletar_comentario():
        avaliacao_id = request.args.get('avaliacao_id')
        avaliacao = schema.Avaliacao.query.filter_by(id=avaliacao_id).first()
        if avaliacao:
            avaliacao.comentario=None
            avaliacao.salvar()
            return jsonify({'mensagem':'Sucesso'})
        return jsonify({'mensagem':'erro'})
    @staticmethod
    def aprovar_adm():
        id_pedido = request.form.get('id_pedido')
        pedido = schema.SolicitacoesAdm.query.filter_by(id=id_pedido).first()
        pedido.status = 2
        pedido.salvar()
        return jsonify({'mensagem':'Sucesso'})
    @staticmethod
    def delete_review():
        app = create_app()

        with app.app_context():
            db.session.query(schema.Avaliacao).delete()
            db.session.commit()
        return jsonify({'mensagem':'Sucesso'})
    @staticmethod
    def delete_nao_tive_aula():
        app = create_app()

        with app.app_context():
            db.session.query(schema.Docentesemvinculo).delete()
            db.session.commit()
        return jsonify({'mensagem':'Sucesso'})


        #pedente aprovado reprovado
