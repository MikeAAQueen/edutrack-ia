query consultaEnderecoDoCliente verb=GET {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/buscaCliente"
      method = "GET"
      params = {authToken: $input.authToken}
      headers = [
        "Authorization: Bearer " ~$input.authToken
        "Content-Type: application/json"
      ]
    
    } as $api1
  
    db.query ENDERECO_01 {
      where = `$var.api1.response.result.id` == $db.ENDERECO_01.cliente_id
      return = {type: "list"}
      output = [
        "id"
        "created_at"
        "cliente_id"
        "logradouro"
        "numero"
        "complemento"
        "bairro"
        "referencia"
        "padrao"
      ]
    
      addon = [
        {
          name : "CEP_01"
          input: {CEP_01_id: $output.cep_id}
          as   : "_cep_01"
        }
      ]
    } as $ENDERECO_011
  }

  response = {endereco1: $ENDERECO_011}
}