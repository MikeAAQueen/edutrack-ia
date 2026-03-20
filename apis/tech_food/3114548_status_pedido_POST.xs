// Add STATUS_PEDIDO record
query status_pedido verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "STATUS_PEDIDO"
    }
  }

  stack {
    db.add STATUS_PEDIDO {
      data = {
        created_at : "now"
        status     : $input.status
        status_para: $input.status_para
      }
    } as $model
  }

  response = $model
}