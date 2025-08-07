from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Classe base para usuários (abstrata)
class Usuario(db.Model):
    def __init__(self,email,senha,tipo=None):
        self.email = email
        self.set_senha(senha)
        self.tipo = tipo
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(50))  # 'aluno' ou 'administrador'

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self,senha):
        senha_hash_gerada = generate_password_hash(senha)
        print(senha_hash_gerada)
        return check_password_hash(self.senha_hash,senha)
    def salvar(self):
        db.session.add(self)
        db.session.commit()

# Classe Aluno (herda de Usuario)
class Aluno(Usuario):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    curso = db.Column(db.String(100))

    avaliacoes = db.relationship('Avaliacao', backref='aluno', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
    }

class Docentesemvinculo(db.Model):
    def __init__(self,id_usuario,id_professor):
        self.aluno_id = id_usuario
        self.professor_id = id_professor
    __tablename__ = 'docentesemvinculo'
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    def salvar(self):
        db.session.add(self)
        db.session.commit()





# Classe Administrador (herda de Usuario)
class Administrador(Usuario):
    __tablename__ = 'administradores'

    id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrador',
    }

# Classe Professor
class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.Integer,db.ForeignKey('curso.id'))

    avaliacoes = db.relationship('Avaliacao', backref='professor', lazy=True)
    disciplinas = db.relationship('DisciplinaProfessor', back_populates='professor')

# Classe Disciplina
class Disciplina(db.Model):
    __tablename__ = 'disciplinas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    professores = db.relationship('DisciplinaProfessor', back_populates='disciplina')

# Tabela associativa entre Professor e Disciplina (N:N)
class DisciplinaProfessor(db.Model):
    __tablename__ = 'disciplina_professor'

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), primary_key=True)

    professor = db.relationship('Professor', back_populates='disciplinas')
    disciplina = db.relationship('Disciplina', back_populates='professores')

class SolicitacoesAdm(db.Model):
    __tablename__ = 'solicitacoesdeadm'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuarios.id'))
    status=  db.Column(db.Integer,db.ForeignKey('statuspedidoadm.id'))
    def salvar(self):
        db.session.add(self)
        db.session.commit()

class Statuspedidoadm(db.Model):
    __tablename__ = 'statuspedidoadm'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))


# Classe Avaliacao
class Avaliacao(db.Model):
    def __init__(self,nota1,nota2,nota3,aluno_id,professor_id,disciplina_id,comentario=None):
        self.nota1=nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.aluno_id=aluno_id
        self.professor_id=professor_id
        self.disciplina_id=disciplina_id
        self.comentario = comentario

    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True)
    nota1 = db.Column(db.Integer, nullable=False)
    nota2 = db.Column(db.Integer, nullable=False)
    nota3 = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)

    def media(self):
        return (self.nota1 + self.nota2 + self.nota3) / 3
    def salvar(self):
        db.session.add(self)
        db.session.commit()
    def to_dict(self):
        return {
        "id":self.id,
        "nota1":self.nota1,
        "nota2":self.nota2,
        "nota3":self.nota3,
        "comentario":self.comentario
        }

