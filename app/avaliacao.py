from flask import abort, jsonify, request
from app.models import schema
class Avaliacao:
    @staticmethod
    def Avaliar():
        valormaximo=5
        nota1=Avaliacao.min_value(request.form.get('nota1'),valormaximo)
        nota2=Avaliacao.min_value(request.form.get('nota2'),valormaximo)
        nota3=Avaliacao.min_value(request.form.get('nota3'),valormaximo)
        aluno_id =  request.form.get('aluno_id')
        professor_id = request.form.get('professor_id')
        disciplina_id = request.form.get('disciplina_id')
        comentario = request.form.get('comentario')
        campos = [nota1, nota2, nota3, aluno_id, professor_id, disciplina_id]
        if any(not campo for campo in campos):
            raise abort(400,"Erro")
        avaliacao = schema.Avaliacao(nota1=nota1,nota2=nota2,nota3=nota3,comentario=comentario,disciplina_id=disciplina_id,aluno_id=aluno_id,professor_id=professor_id)
        avaliacao.salvar()
        return jsonify({'mensagem':'Sucesso'})
    def min_value(value,min_val):
        minimo= min(abs(int(value)),abs(int(min_val)))
        return minimo
    @staticmethod
    def BuscarAvaliacaoGeralProfessor():
        professor_id = request.args.get('professor_id')
        if not professor_id:
            raise abort(400,"Erro")
        medianota1,medianota2,medianota3,comentarios,total,quantidade_nota_5,quantidade_nota_4,quantidade_nota_3,quantidade_nota_2,quantidade_nota_1=Avaliacao.pega_stats_avaliacao_professor(professor_id)
        return jsonify({'id':int(professor_id),"NotaDidatica":medianota1,'quantidade_nota_5':quantidade_nota_5,'quantidade_nota_4':quantidade_nota_4,'quantidade_nota_3':quantidade_nota_3,'quantidade_nota_2':quantidade_nota_2,'quantidade_nota_1':quantidade_nota_1,
                        "NotaDificuldadeProva":medianota2,"NotaPlanoEnisno":medianota3,'TotalAvaliacoes':total,"comentarios":comentarios})
    @staticmethod
    def BuscarAvaliacoesProfesores():
        ids_param = request.args.get('ids')
        ids = [int(id_str) for id_str in ids_param.split(',') if id_str.strip().isdigit()]
        professores = schema.Avaliacao.query.filter(schema.Avaliacao.professor_id.in_(ids)).all()
        lista = [prof.to_dict() for prof in professores]
        return jsonify({'lista':lista})
    @staticmethod
    def pega_stats_avaliacao_professor(professor_id):
        avaliacoes_professor = schema.Avaliacao.query.filter_by(professor_id=professor_id).all()
        quantidade_nota_5 = sum(1 for a in avaliacoes_professor if a.nota1 == 5)
        quantidade_nota_5 +=sum(1 for a in avaliacoes_professor if a.nota2 == 5)
        quantidade_nota_5 +=sum(1 for a in avaliacoes_professor if a.nota3 == 5)
        quantidade_nota_4 = sum(1 for a in avaliacoes_professor if a.nota1 == 4)
        quantidade_nota_4 +=sum(1 for a in avaliacoes_professor if a.nota2 == 4)
        quantidade_nota_4 +=sum(1 for a in avaliacoes_professor if a.nota3 == 4)
        quantidade_nota_3 = sum(1 for a in avaliacoes_professor if a.nota1 == 3)
        quantidade_nota_3 +=sum(1 for a in avaliacoes_professor if a.nota2 == 3)
        quantidade_nota_3 +=sum(1 for a in avaliacoes_professor if a.nota3 == 3)
        quantidade_nota_2 = sum(1 for a in avaliacoes_professor if a.nota1 == 2)
        quantidade_nota_2 +=sum(1 for a in avaliacoes_professor if a.nota2 == 2)
        quantidade_nota_2 +=sum(1 for a in avaliacoes_professor if a.nota3 == 2)
        quantidade_nota_1 = sum(1 for a in avaliacoes_professor if a.nota1 == 1)
        quantidade_nota_1 +=sum(1 for a in avaliacoes_professor if a.nota2 == 1)
        quantidade_nota_1 +=sum(1 for a in avaliacoes_professor if a.nota3 == 1)
        total = len(avaliacoes_professor)*3
        notas1 = 0
        notas2 =0
        notas3 =0
        comentarios=[]
        for avaliacao in avaliacoes_professor:
            notas1+=avaliacao.nota1
            notas2+=avaliacao.nota2
            notas3+=avaliacao.nota3
            if avaliacao.comentario:
                comentarios.append(avaliacao.comentario)
        tamanho =len(avaliacoes_professor)
        if not tamanho:
            tamanho=1
        medianota1 = int(notas1)/tamanho
        medianota2 = int(notas2)/tamanho
        medianota3 = int(notas3)/tamanho
        return medianota1,medianota2,medianota3,comentarios,total,quantidade_nota_5,quantidade_nota_4,quantidade_nota_3,quantidade_nota_2,quantidade_nota_1



    