import jwt
from datetime import datetime, timedelta
from app import settings
from app.repositories.usuario_repository import UsuarioRepository

class AuthService:

    TOKEN_EXPIRACAO_HORAS = 4

    @staticmethod
    def autenticar(email, senha):
        if not email or not senha:
            raise ValueError("Credenciais inválidas")

        usuario = UsuarioRepository.buscar_por_email(email)
        if not usuario or not usuario.validar_senha(senha):
            raise ValueError("Usuário ou senha inválidos")

        payload = {
            "public_id": usuario.id,
            "exp": datetime.utcnow() + timedelta(hours=AuthService.TOKEN_EXPIRACAO_HORAS)
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def criar_usuario(email, senha):
        if not email or not senha:
            raise ValueError("Email e senha são obrigatórios")

        if UsuarioRepository.buscar_por_email(email):
            raise ValueError("Usuário já existe")

        UsuarioRepository.criar(email, senha, tipo="usuario")

    @staticmethod
    def get_secret_key():
        return settings.SECRET_KEY
