table FAQ {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text pergunta? filters=trim
    text resposta? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}