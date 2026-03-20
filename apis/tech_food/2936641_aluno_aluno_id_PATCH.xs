// Edit Aluno record
query "aluno/{aluno_id}" verb=PATCH {
  api_group = "Tech_Food"

  input {
    int aluno_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.aluno_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $aluno
  }

  response = $aluno
}