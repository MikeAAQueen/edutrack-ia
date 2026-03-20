query salvaEndereco verb=POST {
  api_group = "APis Customizadas"

  input {
    text logradouro? filters=trim
    text numero? filters=trim
    text bairro? filters=trim
    text complemento? filters=trim
    text referencia? filters=trim
    text cep? filters=trim
    text cidade? filters=trim
    text estado? filters=trim
    bool padrao?
    int cliente_id?
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/upsertCEP"
      method = "POST"
      params = {
        cep   : $input.cep
        cidade: $input.cidade
        estado: $input.estado
      }
    
      headers = ["Content-Type: application/json"]
    } as $api1
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/endereco_01"
      method = "POST"
      params = {
        logradouro : $input.logradouro
        numero     : $input.numero
        bairro     : $input.bairro
        complemento: $input.complemento
        referencia : $input.referencia
        padrao     : $input.padrao
        cliente_id : $input.cliente_id
        cep_id     : $api1.response.result.id
      }
    
      headers = ["Content-Type: application/json"]
    } as $api2
  }

  response = {
    result2: ```
      { 
          "logradouro": $var.api2.response.result.logradouro,
          "numero": $var.api2.response.result.numero,
          "complemento": $var.api2.response.result.complemento,
          "bairro": $var.api2.response.result.bairro,
          "referencia": $var.api2.response.result.referencia,
          "padrao": $var.api2.response.result.padrao,
          "cliente_id": $var.api2.response.result.cliente_id,
          "cep":
              {
                  "cep_id": $var.api1.response.result.id,
                  "cidade": $var.api1.response.result.cidade,
                  "estado": $var.api1.response.result.uf
              
              }
      }
      ```
  }
}