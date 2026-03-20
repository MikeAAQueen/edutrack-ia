// Query all tarefas records
query tarefas verb=GET {
  api_group = "APis Customizadas"

  input {
  }

  stack {
    db.query tarefas {
      return = {type: "list"}
    } as $tarefas
  }

  response = $tarefas
}