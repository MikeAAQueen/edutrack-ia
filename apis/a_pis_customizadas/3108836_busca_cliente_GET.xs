query buscaCliente verb=GET {
  api_group = "APis Customizadas"

  input {
    // Token de Identificação
    text authToken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:mibNtLvt/auth/me"
      method = "GET"
      params = $input.authToken
      headers = [
        "Authorization: Bearer " ~ $input.authToken
        "Content-Type: application/json"
      ]
    
    } as $api1
  
    conditional {
      if ($api1.response.status == 200) {
        db.get CLIENTE_01 {
          field_name = "user_id"
          field_value = `$var.api1.response.result.id`
        } as $CLIENTE_011
      }
    
      else {
        var $CLIENTE_011 {
          value = {}
        }
      }
    }
  }

  response = $CLIENTE_011
}