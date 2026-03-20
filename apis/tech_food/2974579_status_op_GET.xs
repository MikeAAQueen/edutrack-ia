// Query all STATUS_OP records
query status_op verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query STATUS_OP {
      return = {type: "list"}
    } as $status_op
  }

  response = $status_op
}