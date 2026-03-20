// Get TIPOENDERECO record
query "tipoendereco/{tipoendereco_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int tipoendereco_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.tipoendereco_id
    } as $tipoendereco
  
    precondition ($tipoendereco != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $tipoendereco
}