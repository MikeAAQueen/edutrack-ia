// Query all PEDIDO records
query pedido verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query PEDIDO {
      return = {type: "list"}
    } as $pedido
  }

  response = $pedido
}