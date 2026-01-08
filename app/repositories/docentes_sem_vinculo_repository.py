from app.models.schema import Docentesemvinculo

class DocenteSemVinculoRepository:

    @staticmethod
    def salvar(aluno_id, professor_id):
        registro = Docentesemvinculo(aluno_id, professor_id)
        registro.salvar()

    @staticmethod
    def buscar_ids_rejeitados(aluno_id):
        registros = Docentesemvinculo.query.filter_by(aluno_id=aluno_id).all()
        return [r.professor_id for r in registros]
