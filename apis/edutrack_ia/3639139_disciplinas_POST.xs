// Add disciplinas record
query disciplinas verb=POST {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    dblink {
      table = "disciplinas"
    }
  }

  stack {
    db.add disciplinas {
      data = {
        created_at    : "now"
        nome          : $input.nome
        professor     : $input.professor
        user_id       : $auth.id
        professores_id: $input.professores_id
        carga_horaria : $input.carga_horaria
        faltas        : $input.faltas
      }
    } as $model
  }

  response = $model
}