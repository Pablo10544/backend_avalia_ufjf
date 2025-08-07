import app
from app.models import schema
from flask import request, jsonify

class Admin():
    @staticmethod
    def deletar_comentario():
        avaliacao_id = request.form.get('avaliacao_id')
        avaliacao = schema.Avaliacao.query.filter_by(id=avaliacao_id).first()
        if avaliacao:
            avaliacao.comentario=None
            avaliacao.salvar()
        return jsonify({'mensagem':'Sucesso'})
    @staticmethod
    def aprovar_adm():
        id_pedido = request.form.get('id_pedido')
        pedido = schema.SolicitacoesAdm.query.filter_by(id=id_pedido).first()
        pedido.status = 2
        pedido.salvar()
        return jsonify({'mensagem':'Sucesso'})

        #pedente aprovado reprovado