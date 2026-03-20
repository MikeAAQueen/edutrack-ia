// Update tarefas record
query "tarefas/{tarefas_id}" verb=PUT {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
    dblink {
      table = "tarefas"
    }
  }

  stack {
    db.edit tarefas {
      field_name = "id"
      field_value = $input.tarefas_id
      data = {
        disciplinas_id: $input.disciplinas_id
        titulo        : $input.titulo
        data_entrega  : $input.data_entrega
        completado    : $input.completado
      }
    } as $model
  }

  response = $model
}