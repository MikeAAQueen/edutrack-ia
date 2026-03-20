// Query all TTOKENIZACAO records
query ttokenizacao verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query TTOKENIZACAO {
      return = {type: "list"}
    } as $ttokenizacao
  }

  response = $ttokenizacao
}