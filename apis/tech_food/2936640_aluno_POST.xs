// Add Aluno record
query aluno verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      data = {created_at: "now"}
    } as $aluno
  }

  response = $aluno
}