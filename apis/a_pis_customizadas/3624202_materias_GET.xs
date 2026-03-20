// Query all materias records
query materias verb=GET {
  api_group = "APis Customizadas"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $materias
  }

  response = $materias
}