from fastapi import FastAPI 
from ariadne import load_schema_from_path 
from ariadne import make_executable_schema
from ariadne import QueryType
from ariadne import MutationType
from ariadne.asgi import GraphQL
import requests
import os

app = FastAPI()

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
#mutation = MutationType()

@query.field("contatos")
def resolve_contatos(_, info):
    try:
        response = requests.get("http://api_contato:8004/listar_contatos")
        return response.json() 
    except requests.RequestException as e:
        raise e

schema = make_executable_schema(type_defs, [query])#, mutation])

# Adiciona o Endpoint GraphQL ao FastAPI 
app.mount("/graphql", GraphQL(schema, debug=True)) # debug=True para habilitar o GraphQL IDE