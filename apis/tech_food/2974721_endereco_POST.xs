// Add ENDERECO record
query endereco verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "ENDERECO"
    }
  }

  stack {
    db.add ENDERECO {
      data = {created_at: "now"}
    } as $endereco
  }

  response = $endereco
}