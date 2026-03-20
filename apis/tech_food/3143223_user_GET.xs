// Query all user records
query user verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query user {
      return = {type: "list"}
    } as $model
  }

  response = $model
}