import pytest
from app.services.avaliacao_service import AvaliacaoService

class AvaliacaoFake:
    def __init__(self, nota1=5, nota2=5, nota3=5, comentario=None, id=1):
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.comentario = comentario
        self.id = id

    def to_dict(self):
        return {
            "nota1": self.nota1,
            "nota2": self.nota2,
            "nota3": self.nota3,
            "comentario": self.comentario
        }

def test_limitar_nota_dentro_do_limite():
    assert AvaliacaoService.limitar_nota(3) == 3

def test_limitar_nota_acima_do_limite():
    assert AvaliacaoService.limitar_nota(10) == 5

def test_limitar_nota_negativa():
    assert AvaliacaoService.limitar_nota(-4) == 4
def test_criar_avaliacao_sucesso(mocker):
    mock_salvar = mocker.patch(
        "app.services.avaliacao_service.AvaliacaoRepository.salvar"
    )

    data = {
        "nota1": 4,
        "nota2": 5,
        "nota3": 3,
        "aluno_id": 1,
        "professor_id": 2,
        "disciplina_id": 3,
        "comentario": "Bom professor"
    }

    AvaliacaoService.criar_avaliacao(data)

    mock_salvar.assert_called_once_with(
        4, 5, 3,
        "Bom professor",
        3, 1, 2
    )

def test_criar_avaliacao_campos_ausentes():
    data = {
        "nota1": 5,
        "nota2": 4
        # faltam campos
    }

    with pytest.raises(ValueError, match="Campos obrigatórios ausentes"):
        AvaliacaoService.criar_avaliacao(data)

def test_buscar_estatisticas_professor(mocker):
    avaliacoes = [
        AvaliacaoFake(5, 4, 3, "Ótimo"),
        AvaliacaoFake(4, 4, 4, None)
    ]

    mocker.patch(
        "app.services.avaliacao_service.AvaliacaoRepository.buscar_por_professor",
        return_value=avaliacoes
    )

    resultado = AvaliacaoService.buscar_estatisticas_professor(10)

    assert resultado["id"] == 10
    assert resultado["NotaDidatica"] == 4.5
    assert resultado["NotaDificuldadeProva"] == 4
    assert resultado["NotaPlanoEnsino"] == 3.5
    assert resultado["TotalAvaliacoes"] == 6
    assert resultado["comentarios"] == ["Ótimo"]

def test_listar_avaliacoes_professores(mocker):
    avaliacoes = [AvaliacaoFake(), AvaliacaoFake()]

    mocker.patch(
        "app.services.avaliacao_service.AvaliacaoRepository.buscar_por_professores",
        return_value=avaliacoes
    )

    resultado = AvaliacaoService.listar_avaliacoes_professores([1, 2])

    assert resultado == [{"comentario":None,"nota1": 5,"nota2": 5,"nota3":5},{"comentario":None,"nota1": 5,"nota2": 5,"nota3":5}]
    
def test_get_comentario_id_encontrado(mocker):
    mocker.patch(
        "app.services.avaliacao_service.AvaliacaoRepository.buscar_comentario",
        return_value=AvaliacaoFake(id=99)
    )

    resultado = AvaliacaoService.get_comentario_id(1, "teste")

    assert resultado == {"id": 99}

def test_get_comentario_id_nao_encontrado(mocker):
    mocker.patch(
        "app.services.avaliacao_service.AvaliacaoRepository.buscar_comentario",
        return_value=None
    )

    resultado = AvaliacaoService.get_comentario_id(1, "teste")

    assert resultado == {"id": -1}
