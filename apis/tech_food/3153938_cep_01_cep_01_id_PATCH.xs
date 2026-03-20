// Edit CEP_01 record
query "cep_01/{cep_01_id}" verb=PATCH {
  api_group = "Tech_Food"

  input {
    int cep_01_id? filters=min:1
    dblink {
      table = "CEP_01"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch CEP_01 {
      field_name = "id"
      field_value = $input.cep_01_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
}