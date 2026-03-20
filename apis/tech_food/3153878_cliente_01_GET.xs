// Query all CLIENTE_01 records
query cliente_01 verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query CLIENTE_01 {
      return = {type: "list"}
    } as $model
  }

  response = $model
}