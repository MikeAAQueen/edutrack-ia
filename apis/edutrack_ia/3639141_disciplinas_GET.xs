// Query all disciplinas records
query disciplinas verb=GET {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
  }

  stack {
    db.query disciplinas {
      where = $db.disciplinas.user_id == $auth.id
      return = {type: "list"}
    } as $model
  }

  response = $model
}