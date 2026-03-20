// Add Prova record
query prova verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      data = {created_at: "now"}
    } as $prova
  }

  response = $prova
}