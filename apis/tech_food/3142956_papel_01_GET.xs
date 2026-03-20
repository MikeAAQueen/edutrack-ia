// Query all PAPEL_01 records
query papel_01 verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query PAPEL_01 {
      return = {type: "list"}
    } as $model
  }

  response = $model
}