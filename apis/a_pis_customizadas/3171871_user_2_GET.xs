// Query all user records
query user_2 verb=GET {
  api_group = "APis Customizadas"

  input {
  }

  stack {
    db.query user {
      return = {type: "list"}
    } as $model
  }

  response = $model
}