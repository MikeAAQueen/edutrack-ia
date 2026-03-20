// Delete materias record.
query "materias/{materias_id}" verb=DELETE {
  api_group = "APis Customizadas"

  input {
    int materias_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.materias_id
    }
  }

  response = null
}