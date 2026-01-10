import pytest
from app.application.services.admin_service import AdminService

def test_deletar_comentario_sucesso(mocker):
    avaliacao_fake = object()

    mocker.patch(
        "app.application.services.admin_service.AdminRepository.buscar_avaliacao",
        return_value=avaliacao_fake
    )

    mock_remover = mocker.patch(
        "app.application.services.admin_service.AdminRepository.remover_comentario"
    )

    AdminService.deletar_comentario(10)

    mock_remover.assert_called_once_with(avaliacao_fake)
def test_deletar_comentario_id_invalido():
    with pytest.raises(ValueError, match="Avaliação inválida"):
        AdminService.deletar_comentario(None)
def test_deletar_comentario_nao_encontrada(mocker):
    mocker.patch(
        "app.application.services.admin_service.AdminRepository.buscar_avaliacao",
        return_value=None
    )

    with pytest.raises(ValueError, match="Avaliação não encontrada"):
        AdminService.deletar_comentario(99)
def test_aprovar_admin_sucesso(mocker):
    pedido_fake = object()

    mocker.patch(
        "app.application.services.admin_service.AdminRepository.buscar_pedido_admin",
        return_value=pedido_fake
    )

    mock_aprovar = mocker.patch(
        "app.application.services.admin_service.AdminRepository.aprovar_pedido"
    )

    AdminService.aprovar_admin(5)

    mock_aprovar.assert_called_once_with(pedido_fake)
def test_aprovar_admin_id_invalido():
    with pytest.raises(ValueError, match="Pedido inválido"):
        AdminService.aprovar_admin(None)
def test_aprovar_admin_id_invalido():
    with pytest.raises(ValueError, match="Pedido inválido"):
        AdminService.aprovar_admin(None)
def test_deletar_todas_avaliacoes(mocker):
    mock_deletar = mocker.patch(
        "app.application.services.admin_service.AdminRepository.deletar_todas_avaliacoes"
    )

    AdminService.deletar_todas_avaliacoes()

    mock_deletar.assert_called_once()
def test_deletar_docentes_sem_vinculo(mocker):
    mock_deletar = mocker.patch(
        "app.application.services.admin_service.AdminRepository.deletar_docentes_sem_vinculo"
    )

    AdminService.deletar_docentes_sem_vinculo()

    mock_deletar.assert_called_once()
