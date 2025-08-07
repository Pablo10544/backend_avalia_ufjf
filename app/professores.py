from flask import jsonify, request, send_from_directory, abort
from app import settings
from app.models import schema
import os
class Professores:
    @staticmethod
    def listar_professores():
        professores = schema.Professor.query.all()
        lista_professores = []
        for item in professores:
            lista_professores.append({"id":int(item.id),"nome":item.nome})
        return jsonify(lista_professores) 
    @staticmethod
    def list_professores_por_nome():
        professor_nome = request.args.get('professor_nome')
        professores = schema.Professor.query.filter(schema.Professor.nome.ilike('%'+professor_nome+'%')).all()
        nomes = []
        for nome in professores:
            nomes.append(nome.nome)
        return jsonify({"professores":nomes})    
    @staticmethod
    def rejeitar_professor():
        professor_id = request.form.get('professor_id')
        aluno_id = request.form.get('aluno_id')
        if not professor_id or not aluno_id:
            return jsonify({'mensagem':'erro'})
        docente_sem_vinculo = schema.Docentesemvinculo(aluno_id,professor_id)
        docente_sem_vinculo.salvar()
        return jsonify({'mensagem':'Sucesso'})
    @staticmethod
    def buscar_cards_professor():
        aluno_id = request.args.get('aluno_id')
        curso = request.args.get('curso')
        if not aluno_id and not curso:
           return jsonify({'mensagem':'erro'})
        lista_professores = schema.Professor.query.filter_by(curso=curso).all()
        Docentesemvinculo = schema.Docentesemvinculo.query.with_entities(schema.Docentesemvinculo.professor_id).filter_by(aluno_id=aluno_id).all()
        ids_docentes_sem_vinculo = [doc.professor_id for doc in Docentesemvinculo]
        lista_professores_filtrada = [prof for prof in lista_professores if prof.id not in ids_docentes_sem_vinculo]
        professores_json = [
    {
        'id': prof.id,
        'nome': prof.nome,
        'disciplinas':[d.disciplina.nome for d in prof.disciplinas]
    }
    for prof in lista_professores_filtrada
]
        return jsonify(professores_json)
    @staticmethod
    def foto():
        professor_id = request.args.get('professor_id')
        caminho_imagem = os.path.join(settings.MEDIA_ROOT)

        if os.path.exists(caminho_imagem):
         return send_from_directory(caminho_imagem, professor_id+".jpg")
        else:
         raise abort(404,"Imagem não encontrada")


