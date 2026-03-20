query consultaEnderecosCliente verb=GET {
  api_group = "Auxiliares"

  input {
    text authtoken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:E6SddUC-/consultaCliente"
      method = "GET"
      params = {}|set:"authtoken":$input.authtoken
      headers = []|push:"accept: application/json"
    } as $api1
  
    db.query ENDERECO_01 {
      where = $db.ENDERECO_01.cliente_id == `$var.api1.response.result.cliente.id`
      return = {type: "list"}
    } as $ENDERECO1
  }

  response = `$var.ENDERECO1`
}