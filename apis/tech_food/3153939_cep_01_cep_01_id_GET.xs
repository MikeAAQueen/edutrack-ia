// Get CEP_01 record
query "cep_01/{cep_01_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int cep_01_id? filters=min:1
  }

  stack {
    db.get CEP_01 {
      field_name = "id"
      field_value = $input.cep_01_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
}