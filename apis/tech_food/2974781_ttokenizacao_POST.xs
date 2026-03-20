// Add TTOKENIZACAO record
query ttokenizacao verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "TTOKENIZACAO"
    }
  }

  stack {
    db.add TTOKENIZACAO {
      data = {created_at: "now"}
    } as $ttokenizacao
  }

  response = $ttokenizacao
}