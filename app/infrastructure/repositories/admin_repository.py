from app import db
from app.domain.models import schema

class AdminRepository:

    @staticmethod
    def buscar_avaliacao(avaliacao_id):
        return schema.Avaliacao.query.filter_by(id=avaliacao_id).first()

    @staticmethod
    def remover_comentario(avaliacao):
        avaliacao.comentario = None
        db.session.add(avaliacao)
        db.session.commit()

    @staticmethod
    def buscar_pedido_admin(id_pedido):
        return schema.SolicitacoesAdm.query.filter_by(id=id_pedido).first()

    @staticmethod
    def aprovar_pedido(pedido):
        pedido.status = 2
        db.session.add(pedido)
        db.session.commit()

    @staticmethod
    def deletar_todas_avaliacoes():
        db.session.query(schema.Avaliacao).delete()
        db.session.commit()

    @staticmethod
    def deletar_docentes_sem_vinculo():
        db.session.query(schema.Docentesemvinculo).delete()
        db.session.commit()
