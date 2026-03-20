// Add tarefas record
query tarefas verb=POST {
  api_group = "APis Customizadas"

  input {
    dblink {
      table = "tarefas"
    }
  }

  stack {
    db.add tarefas {
      data = {created_at: "now"}
    } as $tarefas
  }

  response = $tarefas
}