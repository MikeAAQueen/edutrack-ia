// Update STATUS_PEDIDO record
query "status_pedido/{status_pedido_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int status_pedido_id? filters=min:1
    dblink {
      table = "STATUS_PEDIDO"
    }
  }

  stack {
    db.edit STATUS_PEDIDO {
      field_name = "id"
      field_value = $input.status_pedido_id
      data = {status: $input.status, status_para: $input.status_para}
    } as $model
  }

  response = $model
}