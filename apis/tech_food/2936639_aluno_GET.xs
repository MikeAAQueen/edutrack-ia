// Query all Aluno records
query aluno verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $aluno
  }

  response = $aluno
}