// Query all disciplinas records
query disciplinas verb=GET {
  api_group = "APis Customizadas"

  input {
  }

  stack {
    db.query disciplinas {
      return = {type: "list"}
    } as $disciplinas
  }

  response = $disciplinas
}