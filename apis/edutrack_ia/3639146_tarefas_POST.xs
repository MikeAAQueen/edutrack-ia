// Add tarefas record
query tarefas verb=POST {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    dblink {
      table = "tarefas"
    }
  }

  stack {
    db.add tarefas {
      data = {
        created_at    : "now"
        disciplinas_id: $input.disciplinas_id
        titulo        : $input.titulo
        data_entrega  : $input.data_entrega
        completado    : $input.completado
        user_id       : $auth.id
      }
    } as $model
  }

  response = $model
}