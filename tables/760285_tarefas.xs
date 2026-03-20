table tarefas {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    int disciplinas_id? {
      table = "disciplinas"
    }
  
    text titulo? filters=trim
    date? data_entrega?
    bool completado?
    decimal nota?
    int user_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}