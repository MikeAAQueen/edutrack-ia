// Delete anotacoes record
query "anotacoes/{anotacoes_id}" verb=DELETE {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    int anotacoes_id? filters=min:1
  }

  stack {
    db.del anotacoes {
      field_name = "id"
      field_value = $input.anotacoes_id
    }
  }

  response = null
}