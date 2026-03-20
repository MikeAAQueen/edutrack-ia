// Query all SOLCANCELAMENTO records
query solcancelamento verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query SOLCANCELAMENTO {
      return = {type: "list"}
    } as $solcancelamento
  }

  response = $solcancelamento
}