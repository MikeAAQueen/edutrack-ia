// Delete Aluno record.
query "aluno/{aluno_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int aluno_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.aluno_id
    }
  }

  response = null
}