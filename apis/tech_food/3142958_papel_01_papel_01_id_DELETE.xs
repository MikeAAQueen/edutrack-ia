// Delete PAPEL_01 record
query "papel_01/{papel_01_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int papel_01_id? filters=min:1
  }

  stack {
    db.del PAPEL_01 {
      field_name = "id"
      field_value = $input.papel_01_id
    }
  }

  response = null
}