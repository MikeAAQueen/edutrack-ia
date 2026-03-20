// Add PRODUTO record
query produto verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "PRODUTO"
    }
  }

  stack {
    db.add PRODUTO {
      data = {created_at: "now"}
    } as $produto
  }

  response = $produto
}