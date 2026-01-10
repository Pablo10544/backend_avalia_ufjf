from app.domain.models.schema import Professor

class ProfessoresRepository:

    @staticmethod
    def listar_todos():
        return Professor.query.all()

    @staticmethod
    def buscar_por_nome(nome):
        return Professor.query.filter(
            Professor.nome.ilike(f"%{nome}%")
        ).all()

    @staticmethod
    def buscar_por_curso(curso):
        return Professor.query.filter_by(curso=curso).all()
