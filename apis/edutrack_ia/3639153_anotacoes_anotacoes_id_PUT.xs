// Update anotacoes record
query "anotacoes/{anotacoes_id}" verb=PUT {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    int anotacoes_id? filters=min:1
    dblink {
      table = "anotacoes"
    }
  }

  stack {
    db.edit anotacoes {
      field_name = "id"
      field_value = $input.anotacoes_id
      data = {
        disciplinas_id: $input.disciplinas_id
        titulo        : $input.titulo
        conteudo      : $input.conteudo
      }
    } as $model
  }

  response = $model
}