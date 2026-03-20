query criarClienteAsaas verb=POST {
  api_group = "Asaas"

  input {
    text authToken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/buscaCliente"
      method = "GET"
      params = {authToken: $input.authToken}
      headers = ["Content-Type: application/json"]
    } as $api1
  
    conditional {
      if (`$api1.response.result.erro` == false) {
        db.get user {
          field_name = "id"
          field_value = `$var.api1.response.result.user_id`
        } as $user1
      
        db.get tokens {
          field_name = "plataforma"
          field_value = "Asaas"
        } as $tokens1
      
        api.request {
          url = "https://api-sandbox.asaas.com/v3/customers"
          method = "POST"
          params = {name: $user1.name, cpfCnpj: $api1.response.result.cpf}
          headers = [
            $tokens1.token
            "Content_Type: application/json"
            "Accept: application/json"
            "User-Agent: curl/8.0.1"
          ]
        
        } as $api2
      
        var $codigoClienteAsaas {
          value = `$var.api2.response.result.id`
        }
      
        db.get STATUS_TTOKENIZACAO {
          field_name = "status"
          field_value = "CRIADA"
        } as $STATUS_TTOKENIZACAO1
      
        db.add TTOKENIZACAO {
          data = {
            created_at            : "now"
            cliente_id            : `$var.api1.response.result.id`
            det_cartao_encript    : null
            status_ttokenizacao_id: `$var.STATUS_TTOKENIZACAO1.id`
          }
        } as $TTOKENIZACAO1
      
        db.add CARTAOTOKNZD {
          data = {
            created_at        : "now"
            token             : null
            codigoclienteasaas: `$var.codigoClienteAsaas`
            cliente_id        : `$var.api1.response.result.id`
          }
        } as $CARTAOTOKNZD1
      
        var $status {
          value = {status: true, mensagem: "Cliente cadastrado no Asaas."}
        }
      }
    
      else {
        var $status {
          value = {
            status  : false
            mensagem: "Cliente não pode ser cadastrado no Asaas"
          }
        }
      }
    }
  }

  response = $api1.response.result
}