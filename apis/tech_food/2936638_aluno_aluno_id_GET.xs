// Get Aluno record
query "aluno/{aluno_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int aluno_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.aluno_id
    } as $aluno
  
    precondition ($aluno != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $aluno
}