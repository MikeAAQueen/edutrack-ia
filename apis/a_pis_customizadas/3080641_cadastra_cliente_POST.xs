query cadastraCliente verb=POST {
  api_group = "APis Customizadas"

  input {
    text nome? filters=trim
    text celular? filters=trim
    text email? filters=trim
    text cod_verif? filters=trim
    text cpf? filters=trim
    text status? filters=trim
    password senha? {
      sensitive = true
      visibility = "internal"
    }
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:mibNtLvt/auth/signup"
      method = "POST"
      params = {
        name    : $input.nome
        email   : $input.email
        password: $input.senha
      }
    
      headers = [\"Content-Type: application/json\"]
    } as $api1
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:mibNtLvt/auth/me"
      method = "GET"
      params = {authToken: $api1.response.result.authToken}
      headers = [
        "Authorization: Bearer " ~ $var.api1.response.result.authToken
        "Content-Type:application/json"
      ]
    
    } as $api2
  
    db.query STATUS_CLIENTE_01 {
      where = $input.status == $db.STATUS_CLIENTE_01.status
      return = {type: "list"}
    } as $STATUS_CLIENTE_011
  
    db.add CLIENTE_01 {
      data = {
        created_at       : "now"
        user_id          : `$var.api2.response.result.id`
        celular          : $input.celular
        email            : $input.email
        cod_verif        : $input.cod_verif
        cpf              : $input.cpf
        status_cliente_id: $var.STATUS_CLIENTE_011[0].id
      }
    } as $CLIENTE_011
  }

  response = {
    user     : $api2.response.result
    cliente  : $CLIENTE_011
    authToken: $api1.response.result.authToken
  }
}