// Add TIPOENDERECO record
query tipoendereco verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      data = {created_at: "now"}
    } as $tipoendereco
  }

  response = $tipoendereco
}