from app.models.schema import Usuario

class UsuarioRepository:

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def criar(email, senha, tipo):
        usuario = Usuario(email, senha, tipo)
        usuario.salvar()
