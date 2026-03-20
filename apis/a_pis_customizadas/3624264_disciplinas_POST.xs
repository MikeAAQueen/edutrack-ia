// Add disciplinas record
query disciplinas verb=POST {
  api_group = "APis Customizadas"

  input {
    dblink {
      table = "disciplinas"
    }
  }

  stack {
    db.add disciplinas {
      data = {created_at: "now"}
    } as $disciplinas
  }

  response = $disciplinas
}