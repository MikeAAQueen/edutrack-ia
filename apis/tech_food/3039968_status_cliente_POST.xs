// Add STATUS_CLIENTE record
query status_cliente verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "STATUS_CLIENTE"
    }
  }

  stack {
    db.add STATUS_CLIENTE {
      data = {created_at: "now", status: $input.status}
    } as $model
  }

  response = $model
}