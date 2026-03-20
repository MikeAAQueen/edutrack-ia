// Get TTOKENIZACAO record
query "ttokenizacao/{ttokenizacao_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int ttokenizacao_id? filters=min:1
  }

  stack {
    db.get TTOKENIZACAO {
      field_name = "id"
      field_value = $input.ttokenizacao_id
    } as $ttokenizacao
  
    precondition ($ttokenizacao != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $ttokenizacao
}