query atualizaEndereco verb=PATCH {
  api_group = "APis Customizadas"

  input {
    int endereco_01_id? {
      table = "ENDERECO_01"
    }
  
    text logradouro? filters=trim
    text numero? filters=trim
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
    
      headers = ["Content_Type: application/json"]
    } as $api1
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/endereco_01/" ~$input.endereco_01_id
      method = "PATCH"
      params = {
        endereco_id: $input.endereco_01_id
        cliente_id : $input.cliente_id
        logradouro : $input.logradouro
        numero     : $input.numero
        complemento: $input.complemento
        referencia : $input.referencia
        cep_id     : $api1.response.result.id
        padrao     : $input.padrao
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