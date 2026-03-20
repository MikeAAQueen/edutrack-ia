// Update ENDERECO_01 record
query "endereco_01/{endereco_01_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int endereco_01_id? filters=min:1
    dblink {
      table = "ENDERECO_01"
    }
  }

  stack {
    db.edit ENDERECO_01 {
      field_name = "id"
      field_value = $input.endereco_01_id
      data = {
        cliente_id : $input.cliente_id
        logradouro : $input.logradouro
        numero     : $input.numero
        complemento: $input.complemento
        bairro     : $input.bairro
        referencia : $input.referencia
        cep_id     : $input.cep_id
        padrao     : $input.padrao
      }
    } as $model
  }

  response = $model
}