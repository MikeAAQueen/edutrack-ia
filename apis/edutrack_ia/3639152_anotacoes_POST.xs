// Add anotacoes record
query anotacoes verb=POST {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    dblink {
      table = "anotacoes"
    }
  }

  stack {
    db.add anotacoes {
      data = {
        created_at    : "now"
        disciplinas_id: $input.disciplinas_id
        titulo        : $input.titulo
        conteudo      : $input.conteudo
        user_id       : $auth.id
      }
    } as $model
  }

  response = $model
}