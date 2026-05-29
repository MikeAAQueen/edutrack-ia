// Query all anotacoes records
query anotacoes verb=GET {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
  }

  stack {
    db.query anotacoes {
      where = $db.anotacoes.user_id == $auth.id
      return = {type: "list"}
    } as $model
  }

  response = $model
}