// Add ENDERECO_01 record
query endereco_01 verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "ENDERECO_01"
    }
  }

  stack {
    db.add ENDERECO_01 {
      data = {
        created_at : "now"
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