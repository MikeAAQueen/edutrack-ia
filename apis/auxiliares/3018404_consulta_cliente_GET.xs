query consultaCliente verb=GET {
  api_group = "Auxiliares"

  input {
    text authtoken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:Vm9EOxTK/auth/me"
      method = "GET"
      headers = [
        "Authorization: Bearer " ~ $input.authtoken
        "Content-Type: application/json"
      ]
    
    } as $api1
  
    conditional {
      if (`$var.api1.response.status` != 200) {
        var $resultado {
          value = {erro: true, cliente: null}
        }
      }
    
      else {
        db.get CLIENTE_01 {
          field_name = "user_id"
          field_value = `$var.api1.response.result.id`
        } as $CLIENTE1
      
        var $resultado {
          value = {erro: false, cliente: $CLIENTE1}
        }
      }
    }
  }

  response = `$var.resultado`
}