from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

# Criação da app (só uma vez!)
app = FastAPI()

# Middleware CORS (mantém)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ajustar para algo mais restrito no futuro
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
def read_root():
    return {"mensagem": "API de Monitoramento de Cursistas Rodando!"}

# Carregamento do JSON
with open("cursistas_completo.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Rota para buscar cursistas por orientador ou líder
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
