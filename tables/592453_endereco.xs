table ENDERECO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    int? cliente_id? {
      table = "CLIENTE"
    }
  
    text logradouro? filters=trim
    text numero? filters=trim
    text? complemento? filters=trim
    text? referencia? filters=trim
    bool padrao?
    int cep_id? {
      table = "CEP"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {
      type : "btree|unique"
      field: [{name: "cliente_id", op: "asc"}]
    }
  ]
}