table professores {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text nome filters=trim
    text email? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}
