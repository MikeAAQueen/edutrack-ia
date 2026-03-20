// Query all CEP_01 records
query cep_01 verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query CEP_01 {
      return = {type: "list"}
    } as $model
  }

  response = $model
}