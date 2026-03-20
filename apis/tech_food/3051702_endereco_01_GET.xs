// Query all ENDERECO_01 records
query endereco_01 verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query ENDERECO_01 {
      return = {type: "list"}
    } as $model
  }

  response = $model
}