// Query all CEP records
query cep verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query CEP {
      return = {type: "list"}
    } as $cep
  }

  response = $cep
}