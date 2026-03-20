// Add PEDIDO record
query pedido verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "PEDIDO"
    }
  }

  stack {
    db.add PEDIDO {
      data = {created_at: "now"}
    } as $pedido
  }

  response = $pedido
}