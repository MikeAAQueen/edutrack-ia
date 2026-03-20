// Query all STATUS_SOLCANCELAMENTO records
query status_solcancelamento verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query STATUS_SOLCANCELAMENTO {
      return = {type: "list"}
    } as $status_solcancelamento
  }

  response = $status_solcancelamento
}