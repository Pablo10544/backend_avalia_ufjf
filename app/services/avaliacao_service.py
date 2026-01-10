from app.repositories.avaliacao_repository import AvaliacaoRepository

class AvaliacaoService:

    VALOR_MAXIMO = 5

    @staticmethod
    def criar_avaliacao(data):
        nota1 = AvaliacaoService.limitar_nota(data.get("nota1"))
        nota2 = AvaliacaoService.limitar_nota(data.get("nota2"))
        nota3 = AvaliacaoService.limitar_nota(data.get("nota3"))

        aluno_id = data.get("aluno_id")
        professor_id = data.get("professor_id")
        disciplina_id = data.get("disciplina_id")
        comentario = data.get("comentario")
        
        if not all([nota1, nota2, nota3, aluno_id, professor_id, disciplina_id]) or any([nota1==0,nota2==0,nota3==0]):
            raise ValueError("Campos obrigatórios ausentes")

        AvaliacaoRepository.salvar(
            nota1, nota2, nota3,
            comentario, disciplina_id,
            aluno_id, professor_id
        )

    @staticmethod
    def limitar_nota(valor):
        if valor:
            valor = int(valor)
            return min(abs(valor), AvaliacaoService.VALOR_MAXIMO)
        return 0

    @staticmethod
    def buscar_estatisticas_professor(professor_id):
        avaliacoes = AvaliacaoRepository.buscar_por_professor(professor_id)
        return AvaliacaoService.calcular_estatisticas(avaliacoes, professor_id)

    @staticmethod
    def calcular_estatisticas(avaliacoes, professor_id):
        total = len(avaliacoes) * 3 or 1

        notas1 = sum(a.nota1 for a in avaliacoes)
        notas2 = sum(a.nota2 for a in avaliacoes)
        notas3 = sum(a.nota3 for a in avaliacoes)

        comentarios = [a.comentario for a in avaliacoes if a.comentario]

        contagem = {i: 0 for i in range(1, 6)}
        for a in avaliacoes:
            contagem[a.nota1] += 1
            contagem[a.nota2] += 1
            contagem[a.nota3] += 1

        return {
            "id": int(professor_id),
            "NotaDidatica": notas1 / len(avaliacoes),
            "NotaDificuldadeProva": notas2 / len(avaliacoes),
            "NotaPlanoEnsino": notas3 / len(avaliacoes),
            "TotalAvaliacoes": total,
            "comentarios": comentarios,
            **{f"quantidade_nota_{k}": v for k, v in contagem.items()}
        }

    @staticmethod
    def listar_avaliacoes_professores(ids):
        avaliacoes = AvaliacaoRepository.buscar_por_professores(ids)
        return [a.to_dict() for a in avaliacoes]

    @staticmethod
    def get_comentario_id(professor_id, comentario):
        avaliacao = AvaliacaoRepository.buscar_comentario(professor_id, comentario)
        return {"id": avaliacao.id if avaliacao else -1}
