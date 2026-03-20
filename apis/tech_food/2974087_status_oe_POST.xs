// Add STATUS_OE record
query status_oe verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "STATUS_OE"
    }
  }

  stack {
    db.add STATUS_OE {
      data = {created_at: "now"}
    } as $status_oe
  }

  response = $status_oe
}