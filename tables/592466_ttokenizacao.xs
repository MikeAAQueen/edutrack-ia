table TTOKENIZACAO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text? det_cartao_encript? filters=trim
    int status_ttokenizacao_id?=1 {
      table = "STATUS_TTOKENIZACAO"
    }
  
    int cliente_id? {
      table = "CLIENTE_01"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}