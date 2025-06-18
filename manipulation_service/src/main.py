from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import requests
import json

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

@app.post("/criar_lista_de_contatos")
def criar_lista_de_contatos():
    try:
        contatos = [
            Contato(nome="João da Silva", categoria=Categoria.familiar, telefones=[Telefone(numero="1234567890", tipo=Tipo.fixo)]),
            Contato(nome="Maria Oliveira", categoria=Categoria.pessoal, telefones=[Telefone(numero="1234567890", tipo=Tipo.movel)]),
            Contato(nome="Pedro Santos", categoria=Categoria.comercial, telefones=[Telefone(numero="1234567890", tipo=Tipo.comercial)]),
        ]
        for contato in contatos:
           response = requests.post("http://localhost:8004/contato", json=contato.model_dump(mode="json"))
    except requests.RequestException as e:
        raise e
    return {"message": "Contatos preenchidos com sucesso"}

@app.get("/listar_contatos")
def listar_contatos():
    try:
        response = requests.get("http://localhost:8004/listar_contatos")
        return response.json() 
    except requests.RequestException as e:
        raise e
    
@app.get("/listar_contato_do_joao")
def listar_contato_do_joao():
    try:
        response = requests.get("http://localhost:8004/contato/Jo%C3%A3o%20da%20Silva")
        return response.json() 
    except requests.RequestException as e:
        raise e