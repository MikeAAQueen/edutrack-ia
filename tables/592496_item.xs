table ITEM {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    int pedido_id? {
      table = "PEDIDO"
    }
  
    int? qtd?
    decimal valor_unit?
    decimal subtotal?
    int produto_id? {
      table = "PRODUTO"
    }
  
    int status_item_id?=3 {
      table = "STATUS_ITEM"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {
      type : "btree|unique"
      field: [
        {name: "produto_id", op: "asc"}
        {name: "pedido_id", op: "asc"}
      ]
    }
  ]
}