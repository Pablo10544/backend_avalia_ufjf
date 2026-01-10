from app.domain.models.schema import Avaliacao

class AvaliacaoRepository:

    @staticmethod
    def salvar(nota1, nota2, nota3, comentario, disciplina_id, aluno_id, professor_id):
        avaliacao = Avaliacao(
            nota1=nota1,
            nota2=nota2,
            nota3=nota3,
            comentario=comentario,
            disciplina_id=disciplina_id,
            aluno_id=aluno_id,
            professor_id=professor_id
        )
        avaliacao.salvar()

    @staticmethod
    def buscar_por_professor(professor_id):
        return Avaliacao.query.filter_by(professor_id=professor_id).all()

    @staticmethod
    def buscar_por_professores(ids):
        return Avaliacao.query.filter(Avaliacao.professor_id.in_(ids)).all()

    @staticmethod
    def buscar_comentario(professor_id, comentario):
        return Avaliacao.query.filter_by(
            professor_id=professor_id,
            comentario=comentario
        ).first()
