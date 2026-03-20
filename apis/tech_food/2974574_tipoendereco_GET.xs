// Query all TIPOENDERECO records
query tipoendereco verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $tipoendereco
  }

  response = $tipoendereco
}