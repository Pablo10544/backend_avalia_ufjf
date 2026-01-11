# Backend Avalia UFJF

Backend desenvolvido para o sistema Avalia UFJF, cujo objetivo é gerenciar avaliações acadêmicas, fornecendo uma API REST organizada, testável e de fácil manutenção.

O projeto foi estruturado seguindo boas práticas de Engenharia de Software, com foco em arquitetura limpa, separação de responsabilidades e testes automatizados.

##  Tecnologias Utilizadas
Linguagem: Python
Framework Web: Flask
Banco de Dados: SQLite / PostgreSQL (configurável)
ORM: SQLAlchemy
Testes: Pytest
Documentação de API: Swagger / OpenAPI
Gerenciamento de dependências: pip / requirements.txt

##  Arquitetura do Software

O projeto segue uma arquitetura em camadas, inspirada em Clean Architecture, promovendo baixo acoplamento e alta coesão.

## Como rodar
1. crie ative o ambiente virtual
```
python -m venv .venv
venv\Scripts\activate
```
2. rode o pip install
```
pip install -r requirements.txt
```
3. rode o backend
```
python run.py
```
4. se quiser rodar os testes
```
pytest
```