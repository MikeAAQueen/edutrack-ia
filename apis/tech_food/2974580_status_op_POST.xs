// Add STATUS_OP record
query status_op verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "STATUS_OP"
    }
  }

  stack {
    db.add STATUS_OP {
      data = {created_at: "now"}
    } as $status_op
  }

  response = $status_op
}