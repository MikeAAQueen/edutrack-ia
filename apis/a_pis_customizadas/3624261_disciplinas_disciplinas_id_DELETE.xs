// Delete disciplinas record.
query "disciplinas/{disciplinas_id}" verb=DELETE {
  api_group = "APis Customizadas"

  input {
    int disciplinas_id? filters=min:1
  }

  stack {
    db.del disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
    }
  }

  response = null
}