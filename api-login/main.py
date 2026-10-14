from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel
from sqlmodel import create_engine, select

# o banco: o MariaDB do XAMPP, banco "ponto"
URL_DO_BANCO = "mysql+pymysql://root@localhost/ponto"
engine = create_engine(URL_DO_BANCO)

# a tabela "usuarios": cada atributo vira uma coluna
class Usuario(SQLModel, table=True):
   __tablename__ = "usuarios"
   id: int | None = Field(default=None, primary_key=True)
   nome: str
   email: str = Field(unique=True)
   senha: str


# cria as tabelas que ainda nao existem
SQLModel.metadata.create_all(engine)

# tabela vazia? cadastra o usuario de teste
with Session(engine) as sessao:
   if sessao.exec(select(Usuario)).first() is None:
       teste = Usuario(
           nome="Usuário de Teste",
           email="user@email.com",
           senha="123456",
       )
       sessao.add(teste)
       sessao.commit()

# a aplicacao: as rotas sao penduradas nela
app = FastAPI(title="API do Ponto Eletrônico")

# CORS: os enderecos que podem chamar a API pelo navegador
app.add_middleware(
   CORSMiddleware,
   allow_origins=[
       "http://localhost:5173",
       "http://127.0.0.1:5173",
   ],
   allow_methods=["*"],
   allow_headers=["*"],
)

# o formato do corpo que o front-end manda
class DadosLogin(BaseModel):
   email: str
   senha: str


# o formato do corpo do cadastro
class DadosCadastro(BaseModel):
   nome: str
   email: str
   senha: str


# POST /usuarios: grava um usuario novo na tabela
@app.post("/usuarios", status_code=201)
def cadastrar(dados: DadosCadastro):
   with Session(engine) as sessao:
       consulta = select(Usuario).where(
           Usuario.email == dados.email
       )
       if sessao.exec(consulta).first():
           # o e-mail ja esta na tabela: status 409
           raise HTTPException(
               status_code=409,
               detail="E-mail já cadastrado.",
           )
       usuario = Usuario(
           nome=dados.nome,
           email=dados.email,
           senha=dados.senha,
       )
       sessao.add(usuario)
       sessao.commit()
       sessao.refresh(usuario)
       # a senha NAO volta na resposta
       return {
           "mensagem": "Usuário cadastrado!",
           "id": usuario.id,
           "email": usuario.email,
       }


# POST /login: procura o e-mail na tabela e confere a senha
@app.post("/login")
def login(dados: DadosLogin):
   with Session(engine) as sessao:
       consulta = select(Usuario).where(
           Usuario.email == dados.email
       )
       usuario = sessao.exec(consulta).first()
       achou = usuario is not None
       senha_certa = achou and usuario.senha == dados.senha
       if senha_certa:
           # o dicionario vira JSON, status 200
           return {
               "mensagem": "Login realizado com sucesso!",
               "email": dados.email,
           }
       # e-mail que nao existe ou senha errada: status 401
       raise HTTPException(
           status_code=401,
           detail="E-mail ou senha incorretos.",
       )