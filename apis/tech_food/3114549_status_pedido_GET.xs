// Query all STATUS_PEDIDO records
query status_pedido verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query STATUS_PEDIDO {
      return = {type: "list"}
    } as $model
  }

  response = $model
}