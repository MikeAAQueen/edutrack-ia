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
        created_at: "now"
        nome      : $input.nome
        professor : $input.professor
        creditos  : $input.creditos
        user_id   : $auth.id
      }
    } as $model
  }

  response = $model
}