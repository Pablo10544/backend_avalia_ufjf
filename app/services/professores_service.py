import os
from app import settings
from app.repositories.professores_repository import ProfessoresRepository
from app.repositories.docentes_sem_vinculo_repository import DocenteSemVinculoRepository

class ProfessoresService:

    @staticmethod
    def listar_professores():
        professores = ProfessoresRepository.listar_todos()
        return [{"id": int(p.id), "nome": p.nome} for p in professores]

    @staticmethod
    def listar_por_nome(nome):
        professores = ProfessoresRepository.buscar_por_nome(nome)
        return {"professores": [p.nome for p in professores]}

    @staticmethod
    def rejeitar_professor(professor_id, aluno_id):
        if not professor_id or not aluno_id:
            raise ValueError("Dados inválidos")

        DocenteSemVinculoRepository.salvar(aluno_id, professor_id)

    @staticmethod
    def buscar_cards(aluno_id, curso):
        if not aluno_id or not curso:
            raise ValueError("Aluno ou curso inválido")

        professores = ProfessoresRepository.buscar_por_curso(curso)
        rejeitados = DocenteSemVinculoRepository.buscar_ids_rejeitados(aluno_id)

        professores_validos = [
            p for p in professores if p.id not in rejeitados
        ]

        return [
            {
                "id": p.id,
                "nome": p.nome,
                "disciplinas": [d.disciplina.nome for d in p.disciplinas]
            }
            for p in professores_validos
        ]

    @staticmethod
    def buscar_foto(professor_id):
        caminho = settings.MEDIA_ROOT
        arquivo = f"{professor_id}.jpg"

        if not os.path.exists(os.path.join(caminho, arquivo)):
            raise FileNotFoundError("Imagem não encontrada")

        return caminho, arquivo
