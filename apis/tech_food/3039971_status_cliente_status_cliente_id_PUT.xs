// Update STATUS_CLIENTE record
query "status_cliente/{status_cliente_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int status_cliente_id? filters=min:1
    dblink {
      table = "STATUS_CLIENTE"
    }
  }

  stack {
    db.edit STATUS_CLIENTE {
      field_name = "id"
      field_value = $input.status_cliente_id
      data = {status: $input.status}
    } as $model
  }

  response = $model
}