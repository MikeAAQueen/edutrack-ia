// Papel do Usuário. Por exemplo, Adm, Cozinheiro, Atendente, etc.
table PAPEL_01 {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text papel filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}