from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import re

app = FastAPI()

# CORS Middleware (libera para frontend no Firebase, por exemplo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ajustar para restringir por domínio
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
def read_root():
    return {"mensagem": "API de Monitoramento de Cursistas Rodando!"}

# Carregamento do JSON com correção de NaN
with open("cursistas_completo.json", "r", encoding="utf-8") as f:
    conteudo = f.read()
    conteudo_corrigido = re.sub(r'\bNaN\b', 'null', conteudo)
    dados = json.loads(conteudo_corrigido)

# Rota para buscar cursistas por orientador ou líder
@app.get("/api/cursistas")
def get_cursistas(usuario: str = Query(...)):
    usuario = usuario.strip().lower()

    orientados = [c for c in dados if c.get("orientador", "").strip().lower() == usuario]
    liderados = [c for c in dados if c.get("lider", "").strip().lower() == usuario]

    if orientados:
        return orientados
    elif liderados:
        return liderados
    else:
        return {"erro": "Usuário não encontrado"}

# Rota para listar todos os orientadores
@app.get("/api/orientadores")
def get_orientadores():
    orientadores = sorted(set(
        c.get("orientador", "").strip()
        for c in dados if c.get("orientador")
    ))
    return orientadores
