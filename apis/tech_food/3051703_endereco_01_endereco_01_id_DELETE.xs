// Delete ENDERECO_01 record
query "endereco_01/{endereco_01_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int endereco_01_id? filters=min:1
  }

  stack {
    db.del ENDERECO_01 {
      field_name = "id"
      field_value = $input.endereco_01_id
    }
  }

  response = null
}