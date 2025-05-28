from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
def read_root():
    return {"mensagem": "API de Monitoramento de Cursistas Rodando!"}

# Carrega o JSON com os dados
with open("cursistas_completo.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Endpoint para buscar cursistas por orientador ou líder
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

# Endpoint que lista todos os orientadores
@app.get("/api/orientadores")
def get_orientadores():
    orientadores = sorted(set(
        c.get("orientador", "").strip()
        for c in dados if c.get("orientador")
    ))
    return orientadores
