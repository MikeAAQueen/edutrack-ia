// Delete disciplinas record.
query "disciplinas/{disciplinas_id}" verb=DELETE {
  api_group = "APis Customizadas"

  input {
    int disciplinas_id? filters=min:1
  }

  stack {
    db.query tarefas {
      where = $db.tarefas.disciplinas_id == $input.disciplinas_id
    } as $tarefas

    foreach ($tarefas) {
      each as $tarefa {
        db.del tarefas {
          field_name = "id"
          field_value = $tarefa.id
        }
      }
    }

    db.del disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
    }
  }

  response = null
}