// Update PAPEL_01 record
query "papel_01/{papel_01_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int papel_01_id? filters=min:1
    dblink {
      table = "PAPEL_01"
    }
  }

  stack {
    db.edit PAPEL_01 {
      field_name = "id"
      field_value = $input.papel_01_id
      data = {papel: $input.papel}
    } as $model
  }

  response = $model
}