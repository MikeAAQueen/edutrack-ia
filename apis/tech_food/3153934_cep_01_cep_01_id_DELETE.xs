// Delete CEP_01 record
query "cep_01/{cep_01_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int cep_01_id? filters=min:1
  }

  stack {
    db.del CEP_01 {
      field_name = "id"
      field_value = $input.cep_01_id
    }
  }

  response = null
}