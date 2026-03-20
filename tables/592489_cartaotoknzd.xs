table CARTAOTOKNZD {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text token? filters=trim
    text codigoclienteasaas? filters=trim
    int cliente_id? {
      table = "CLIENTE_01"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}