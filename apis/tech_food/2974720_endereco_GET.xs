// Query all ENDERECO records
query endereco verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query ENDERECO {
      return = {type: "list"}
    } as $endereco
  }

  response = $endereco
}