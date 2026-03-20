// Query all Prova records
query prova verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $prova
  }

  response = $prova
}