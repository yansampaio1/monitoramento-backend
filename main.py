from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

# Criação da app
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ajustar depois
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mensagem da rota raiz
@app.get("/")
def read_root():
    return {"mensagem": "API de Monitoramento de Cursistas Rodando!"}

# ✅ Carregamento do JSON
with open("cursistas_completo.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# ✅ Rota para buscar cursistas por orientador ou líder
@app.get("/api/cursistas")
def get_cursistas(usuario: str = Query(...)):
    usuario = usuario.strip().lower()
    is_orientador = any(c["orientador"].lower() == usuario for c in dados)
    is_lider = any(c["lider"].lower() == usuario for c in dados)

    if is_orientador:
        return [c for c in dados if c["orientador"].lower() == usuario]
    elif is_lider:
        return [c for c in dados if c["lider"].lower() == usuario]
    else:
        return {"erro": "Usuário não encontrado"}

# ✅ NOVO ENDPOINT: Lista de orientadores
@app.get("/api/orientadores")
def get_orientadores():
    orientadores = sorted(set(c["orientador"] for c in dados if "orientador" in c))
    return orientadores
