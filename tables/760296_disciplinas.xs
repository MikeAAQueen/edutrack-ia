table disciplinas {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text nome? filters=trim
    text professor? filters=trim
    int creditos?
    int user_id? {
      table = "user"
    }
  
    int carga_horaria?
    int faltas?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}