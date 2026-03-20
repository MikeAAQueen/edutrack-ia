// Dado um CEP, verificar se este já existe na tabela
query buscaCEP verb=GET {
  api_group = "APis Customizadas"

  input {
    // CEP a ser pesquisado
    text cep? filters=trim
  }

  stack {
    db.query CEP_01 {
      where = $db.CEP_01.cep == $input.cep
      return = {type: "list"}
    } as $CEP_011
  }

  response = $CEP_011
}