table CLIENTE {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text nome? filters=trim
    text celular? filters=trim
    text cpf? filters=trim
    int status_cliente_id?=1 {
      table = "STATUS_CLIENTE"
    }
  
    int user_id? {
      table = "USER"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "cpf", op: "asc"}]}
  ]
}