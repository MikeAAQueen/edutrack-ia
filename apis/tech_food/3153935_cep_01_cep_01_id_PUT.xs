// Update CEP_01 record
query "cep_01/{cep_01_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int cep_01_id? filters=min:1
    dblink {
      table = "CEP_01"
    }
  }

  stack {
    db.edit CEP_01 {
      field_name = "id"
      field_value = $input.cep_01_id
      data = {cep: $input.cep, uf: $input.uf, cidade: $input.cidade}
    } as $model
  }

  response = $model
}