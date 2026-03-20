// Add OP record
query op verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "OP"
    }
  }

  stack {
    db.add OP {
      data = {created_at: "now"}
    } as $op
  }

  response = $op
}