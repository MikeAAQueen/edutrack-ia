// Add CEP record
query cep verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "CEP"
    }
  }

  stack {
    db.add CEP {
      data = {created_at: "now"}
    } as $cep
  }

  response = $cep
}