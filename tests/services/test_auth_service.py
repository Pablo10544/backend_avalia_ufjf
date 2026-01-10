import pytest
from datetime import datetime, timedelta

from app.application.services.auth_service import AuthService
class UsuarioFake:
    def __init__(self, id=1, senha_valida=True):
        self.id = id
        self._senha_valida = senha_valida

    def validar_senha(self, senha):
        return self._senha_valida
def test_autenticar_sem_email_ou_senha():
    with pytest.raises(ValueError, match="Credenciais inválidas"):
        AuthService.autenticar(None, "123")

    with pytest.raises(ValueError, match="Credenciais inválidas"):
        AuthService.autenticar("email@test.com", None)
def test_autenticar_sem_email_ou_senha():
    with pytest.raises(ValueError, match="Credenciais inválidas"):
        AuthService.autenticar(None, "123")

    with pytest.raises(ValueError, match="Credenciais inválidas"):
        AuthService.autenticar("email@test.com", None)
def test_autenticar_senha_invalida(mocker):
    usuario = UsuarioFake(senha_valida=False)

    mocker.patch(
        "app.application.services.auth_service.UsuarioRepository.buscar_por_email",
        return_value=usuario
    )

    with pytest.raises(ValueError, match="Usuário ou senha inválidos"):
        AuthService.autenticar("email@test.com", "123")
def test_autenticar_sucesso(mocker):
    usuario = UsuarioFake(id=42)

    mocker.patch(
        "app.application.services.auth_service.UsuarioRepository.buscar_por_email",
        return_value=usuario
    )

    mock_jwt_encode = mocker.patch(
        "app.application.services.auth_service.jwt.encode",
        return_value="token-fake"
    )

    token = AuthService.autenticar("email@test.com", "123")

    assert token == "token-fake"

    args, kwargs = mock_jwt_encode.call_args
    payload = args[0]

    assert payload["public_id"] == 42
    assert "exp" in payload
    assert kwargs["algorithm"] == "HS256"
def test_criar_usuario_dados_ausentes():
    with pytest.raises(ValueError, match="Email e senha são obrigatórios"):
        AuthService.criar_usuario(None, "123")

    with pytest.raises(ValueError, match="Email e senha são obrigatórios"):
        AuthService.criar_usuario("email@test.com", None)
def test_criar_usuario_ja_existe(mocker):
    mocker.patch(
        "app.application.services.auth_service.UsuarioRepository.buscar_por_email",
        return_value=object()
    )

    with pytest.raises(ValueError, match="Usuário já existe"):
        AuthService.criar_usuario("email@test.com", "123")
def test_criar_usuario_sucesso(mocker):
    mocker.patch(
        "app.application.services.auth_service.UsuarioRepository.buscar_por_email",
        return_value=None
    )

    mock_criar = mocker.patch(
        "app.application.services.auth_service.UsuarioRepository.criar"
    )

    AuthService.criar_usuario("email@test.com", "123")

    mock_criar.assert_called_once_with(
        "email@test.com",
        "123",
        tipo="usuario"
    )
