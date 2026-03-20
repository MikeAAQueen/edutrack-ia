table ENDERECO_01 {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    int cliente_id? {
      table = "CLIENTE_01"
    }
  
    text logradouro? filters=trim
    text numero? filters=trim
    text complemento? filters=trim
    text bairro? filters=trim
    text referencia? filters=trim
    int cep_id? {
      table = "CEP_01"
    }
  
    bool padrao?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "gin", field: [{name: "xdo", op: "jsonb_path_op"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}