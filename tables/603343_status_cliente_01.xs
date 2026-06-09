table STATUS_CLIENTE_01 {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    // Estado da Solicitação de Cancelamento.
    text status filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "status", op: "asc"}]}
  ]
}