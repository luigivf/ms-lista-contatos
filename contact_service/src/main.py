from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Categoria(Enum):
    familiar = "familiar"
    pessoal = "pessoal"
    comercial = "comercial"

class Tipo(Enum):
    movel = "movel"
    fixo = "fixo"
    comercial = "comercial"

class Telefone(BaseModel):
    numero: str
    tipo: Tipo

class Contato(BaseModel):
    nome: str
    categoria: Categoria
    telefones: list[Telefone]

contatos_db = {}

@app.post("/contato")
def create_contato(contato: Contato):
    if contato.nome in contatos_db:
        raise HTTPException(status_code=400, detail="Contato já existe")
    contatos_db[contato.nome] = contato
    return {"message": "Contato criado com sucesso"}

@app.get("/contato/{nome}")
def get_contato(nome: str):
    if nome not in contatos_db:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contatos_db[nome]

@app.get("/listar_contatos")
def listar_contatos():
    if len(contatos_db) == 0:
        raise HTTPException(status_code=404, detail="Lista vazia")
    return list(contatos_db.values())

@app.delete("/contato/{nome}")
def delete_contato(nome: str):
    if nome not in contatos_db:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    del contatos_db[nome]
    return {"message": "Contato deletado com sucesso"}