import pytest
from app.services.professores_service import ProfessoresService
class DisciplinaFake:
    def __init__(self, nome):
        self.nome = nome


class ProfessorFake:
    def __init__(self, id, nome, disciplinas=None):
        self.id = id
        self.nome = nome
        self.disciplinas = disciplinas or []
def test_listar_professores(mocker):
    professores = [
        ProfessorFake(1, "Ana"),
        ProfessorFake(2, "Bruno"),
    ]

    mocker.patch(
        "app.services.professores_service.ProfessoresRepository.listar_todos",
        return_value=professores
    )

    resultado = ProfessoresService.listar_professores()

    assert resultado == [
        {"id": 1, "nome": "Ana"},
        {"id": 2, "nome": "Bruno"},
    ]
def test_listar_por_nome(mocker):
    professores = [
        ProfessorFake(1, "Carlos"),
        ProfessorFake(2, "Carla"),
    ]

    mocker.patch(
        "app.services.professores_service.ProfessoresRepository.buscar_por_nome",
        return_value=professores
    )

    resultado = ProfessoresService.listar_por_nome("Car")

    assert resultado == {
        "professores": ["Carlos", "Carla"]
    }
def test_rejeitar_professor_dados_invalidos():
    with pytest.raises(ValueError, match="Dados inválidos"):
        ProfessoresService.rejeitar_professor(None, 1)

    with pytest.raises(ValueError, match="Dados inválidos"):
        ProfessoresService.rejeitar_professor(1, None)
def test_rejeitar_professor_sucesso(mocker):
    mock_salvar = mocker.patch(
        "app.services.professores_service.DocenteSemVinculoRepository.salvar"
    )

    ProfessoresService.rejeitar_professor(10, 20)

    mock_salvar.assert_called_once_with(20, 10)
def test_buscar_cards_parametros_invalidos():
    with pytest.raises(ValueError, match="Aluno ou curso inválido"):
        ProfessoresService.buscar_cards(None, "SI")

    with pytest.raises(ValueError, match="Aluno ou curso inválido"):
        ProfessoresService.buscar_cards(1, None)
def test_buscar_cards_filtra_professores_rejeitados(mocker):
    professores = [
        ProfessorFake(
            1,
            "Ana",
            disciplinas=[type("X", (), {"disciplina": DisciplinaFake("POO")})()]
        ),
        ProfessorFake(
            2,
            "Bruno",
            disciplinas=[type("X", (), {"disciplina": DisciplinaFake("BD")})()]
        ),
    ]

    mocker.patch(
        "app.services.professores_service.ProfessoresRepository.buscar_por_curso",
        return_value=professores
    )

    mocker.patch(
        "app.services.professores_service.DocenteSemVinculoRepository.buscar_ids_rejeitados",
        return_value=[2]
    )

    resultado = ProfessoresService.buscar_cards(aluno_id=1, curso="SI")

    assert resultado == [
        {
            "id": 1,
            "nome": "Ana",
            "disciplinas": ["POO"]
        }
    ]
def test_buscar_foto_inexistente(mocker):
    mocker.patch(
        "app.services.professores_service.settings.MEDIA_ROOT",
        "/fake/path"
    )

    mocker.patch(
        "app.services.professores_service.os.path.exists",
        return_value=False
    )

    with pytest.raises(FileNotFoundError, match="Imagem não encontrada"):
        ProfessoresService.buscar_foto(10)
def test_buscar_foto_sucesso(mocker):
    mocker.patch(
        "app.services.professores_service.settings.MEDIA_ROOT",
        "/fake/path"
    )

    mocker.patch(
        "app.services.professores_service.os.path.exists",
        return_value=True
    )

    caminho, arquivo = ProfessoresService.buscar_foto(10)

    assert caminho == "/fake/path"
    assert arquivo == "10.jpg"
