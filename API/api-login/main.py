from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
# POST /login: confere o e-mail e a senha
@app.post("/login")
def login(dados: DadosLogin):
	email_certo = dados.email == "user@email.com"
	senha_certa = dados.senha == "123456"
	if email_certo and senha_certa:
		# o dicionario vira JSON, status 200
		return {
			"mensagem": "Login realizado com sucesso!",
			"email": dados.email,
		}
	# chegou aqui: algo nao bateu, status 401
	raise HTTPException(
		status_code=401,
		detail="E-mail ou senha incorretos.",
	)
