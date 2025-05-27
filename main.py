from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS (libera para frontend externo, como Firebase)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # você pode restringir isso depois
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega dados
with open("cursistas_completo.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

@app.get("/api/cursistas")
def get_cursistas(usuario: str = Query(...)):
    usuario = usuario.strip().lower()
    # Verifica se é orientador ou líder
    is_orientador = any(c["orientador"].lower() == usuario for c in dados)
    is_lider = any(c["lider"].lower() == usuario for c in dados)

    if is_orientador:
        return [c for c in dados if c["orientador"].lower() == usuario]
    elif is_lider:
        return [c for c in dados if c["lider"].lower() == usuario]
    else:
        return {"erro": "Usuário não encontrado"}
