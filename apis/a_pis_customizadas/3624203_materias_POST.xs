// Add materias record
query materias verb=POST {
  api_group = "APis Customizadas"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      data = {created_at: "now"}
    } as $materias
  }

  response = $materias
}