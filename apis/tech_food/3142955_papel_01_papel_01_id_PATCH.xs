// Edit PAPEL_01 record
query "papel_01/{papel_01_id}" verb=PATCH {
  api_group = "Tech_Food"

  input {
    int papel_01_id? filters=min:1
    dblink {
      table = "PAPEL_01"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch PAPEL_01 {
      field_name = "id"
      field_value = $input.papel_01_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
}