table disciplinas {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text nome? filters=trim
<<<<<<<
    text professor? filters=trim
=======
>>>>>>>
    int user_id? {
      table = "user"
    }
  
    int carga_horaria?
    int faltas?
    int professores_id? {
      table = "professores"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}