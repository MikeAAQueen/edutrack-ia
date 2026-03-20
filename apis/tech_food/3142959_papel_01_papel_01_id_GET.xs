// Get PAPEL_01 record
query "papel_01/{papel_01_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int papel_01_id? filters=min:1
  }

  stack {
    db.get PAPEL_01 {
      field_name = "id"
      field_value = $input.papel_01_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
}