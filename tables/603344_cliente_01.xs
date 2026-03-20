table CLIENTE_01 {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    int? user_id? {
      table = "user"
    }
  
    text celular filters=trim
    email email? filters=trim|lower
    text cod_verif? filters=trim
    text cpf? filters=trim
    int status_cliente_01_id?=1 {
      table = "STATUS_CLIENTE_01"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "gin", field: [{name: "xdo", op: "jsonb_path_op"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "user_id", op: "asc"}]}
  ]
}