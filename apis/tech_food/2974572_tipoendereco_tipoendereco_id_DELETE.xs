// Delete TIPOENDERECO record.
query "tipoendereco/{tipoendereco_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int tipoendereco_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.tipoendereco_id
    }
  }

  response = null
}