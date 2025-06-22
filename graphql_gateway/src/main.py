from fastapi import FastAPI
from ariadne import load_schema_from_path 
from ariadne import make_executable_schema
from ariadne import QueryType
from ariadne import MutationType
from ariadne.asgi import GraphQL
import requests
from requests.exceptions import HTTPError
import os

app = FastAPI()

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
mutation = MutationType()

#estruturas para retorno de mensagem de erro
contato_vazio = {
            "nome": "",
            "categoria": "",
            "telefones": [{
                "numero": "",
                "tipo": ""
            }]
        }

lista_vazia_contatos = []
lista_vazia_contatos.append(contato_vazio)

@query.field("contatos")
def resolve_contatos(_, info):
    try:
        response = requests.get("http://api_contato:8004/listar_contatos")
        response.raise_for_status()

        return response.json() 
    except HTTPError as e:
        return lista_vazia_contatos
            
    except requests.RequestException as e:
        return lista_vazia_contatos

@query.field("contato")
def resolve_contato(_, info, nome: str):
    try:
        response = requests.get(f"http://api_contato:8004/contato/{nome}")
        response.raise_for_status()

        return response.json() 
    except HTTPError as e:
        return contato_vazio
    
    except requests.RequestException as e:
        return contato_vazio

@mutation.field("createContato")
def resolve_create_contato(_, info, input):

    try:
        response = requests.post(
            "http://api_contato:8004/contato",
            json=input
        )
        response.raise_for_status()

        return{
            "message": "Contato criado com sucesso",
            "contato": input
        }
    except HTTPError as e:
        return{
            "message": f"Falha ao criar o contato: {response.json()}",
            "contato": contato_vazio
            }
    except requests.RequestException as e:
        
        return{
            "message": f"Erro interno",
            "contato": contato_vazio
            }

@mutation.field("fillListaDeContatos")
def resolve_fill_lista_de_contatos(_, info):
    try:
        response = requests.post('http://api_manipulation:8005/criar_lista_de_contatos')
        response.raise_for_status()

        response = requests.get('http://api_manipulation:8005/listar_contatos')
        response.raise_for_status()

        return{
            "message": "Lista de contatos criada com sucesso!",
            "contato": response.json()
        }
    except HTTPError as e:
        
        return{
            "message": f"Falha ao criar os contatos: {response.json()}",
            "contato": lista_vazia_contatos
            }
    except requests.RequestException as e:
        
        return{
            "message": "deu problema",
            "contato": lista_vazia_contatos
        }

schema = make_executable_schema(type_defs, [query, mutation])

# Adiciona o Endpoint GraphQL ao FastAPI 
app.mount("/graphql", GraphQL(schema, debug=True)) # debug=True para habilitar o GraphQL IDE