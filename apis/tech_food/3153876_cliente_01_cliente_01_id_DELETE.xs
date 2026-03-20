// Delete CLIENTE_01 record
query "cliente_01/{cliente_01_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int cliente_01_id? filters=min:1
  }

  stack {
    db.del CLIENTE_01 {
      field_name = "id"
      field_value = $input.cliente_01_id
    }
  }

  response = null
}