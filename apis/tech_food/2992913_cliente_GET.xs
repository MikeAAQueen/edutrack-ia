// Query all CLIENTE records
query cliente verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query CLIENTE {
      return = {type: "list"}
    } as $model
  }

  response = $model
}