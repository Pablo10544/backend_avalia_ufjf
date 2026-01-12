from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# USUÁRIO (ABSTRATO)
# =========================
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "usuario",
        "polymorphic_on": tipo
    }

    def definir_senha(self, senha: str):
        self.senha_hash = generate_password_hash(senha)

    def validar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.email}>"

class Aluno(Usuario):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), primary_key=True)
    curso = db.Column(db.String(100), nullable=False)

    avaliacoes = db.relationship("Avaliacao", backref="aluno", lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "aluno"
    }

    def __repr__(self):
        return f"<Aluno {self.email}>"
class Administrador(Usuario):
    __tablename__ = "administradores"

    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "administrador"
    }

    def __repr__(self):
        return f"<Administrador {self.email}>"
class Professor(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.Integer, db.ForeignKey("curso.id"))

    avaliacoes = db.relationship("Avaliacao", backref="professor", lazy=True)
    disciplinas = db.relationship("DisciplinaProfessor", back_populates="professor")

    def __repr__(self):
        return f"<Professor {self.nome}>"
class Disciplina(db.Model):
    __tablename__ = "disciplinas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    professores = db.relationship("DisciplinaProfessor", back_populates="disciplina")

    def __repr__(self):
        return f"<Disciplina {self.nome}>"


class DisciplinaProfessor(db.Model):
    __tablename__ = "disciplina_professor"

    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), primary_key=True)

    professor = db.relationship("Professor", back_populates="disciplinas")
    disciplina = db.relationship("Disciplina", back_populates="professores")
class DocenteSemVinculo(db.Model):
    __tablename__ = "docentesemvinculo"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), nullable=False)

    def __repr__(self):
        return f"<DocenteSemVinculo aluno={self.aluno_id} professor={self.professor_id}>"
class StatusPedidoAdm(db.Model):
    __tablename__ = "status_pedido_adm"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<StatusPedidoAdm {self.status}>"


class SolicitacaoAdm(db.Model):
    __tablename__ = "solicitacoes_adm"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status_pedido_adm.id"), nullable=False)

    def __repr__(self):
        return f"<SolicitacaoAdm usuario={self.usuario_id}>"
class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"

    id = db.Column(db.Integer, primary_key=True)
    nota1 = db.Column(db.Integer, nullable=False)
    nota2 = db.Column(db.Integer, nullable=False)
    nota3 = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)

    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)

    def media(self) -> float:
        return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "nota1": self.nota1,
            "nota2": self.nota2,
            "nota3": self.nota3,
            "comentario": self.comentario,
            "media": self.media()
        }

    def __repr__(self):
        return f"<Avaliacao id={self.id}>"
