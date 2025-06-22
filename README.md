O projeto é composto por 2 microsserviços e 1 gateway GraphQL:

1- contact_service (porta 8004): serviço principal, que retém os dados e as operações de inserção (/contato), pesquisa de um contato (/contato) e a listagem de todos os contatos (/listar_contatos) já cadastrados.

2- manipulation_service (porta 8005): serviço que interage com o contact_service usando usando a API rest. Possui o script para carregar uma lista de contatos prédefinida (/criar_lista_de_contatos), listar os contatos e listar o contato do "João".

3- gateway_graphql (porta 8006): Gateway SQL conecta com ambos os serviços e realiza as querys e mutations. Chamadas de exemplo abaixo:

// carregar lista de contato
mutation {
  fillListaDeContatos {
    message
    contato {
      nome
      categoria
      telefones {
        numero
        tipo
      }
    }
  }
}

// listar o nome dos integrantes da lista
{contatos{nome}}

// criar o contato chamado "Luigi"
mutation{
  createContato(input: 
    {
      nome: "Luigi"  
      categoria: "familiar"
      telefones: {
        numero: "0987654321"
        tipo: "movel"
      }
    }
  ){
    message
    contato {
      nome
    }
  }
}

//pesquisar o contato
{contato(nome: "Luigi"){nome categoria}}
