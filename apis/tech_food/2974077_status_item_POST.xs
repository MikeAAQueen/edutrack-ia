// Add STATUS_ITEM record
query status_item verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "STATUS_ITEM"
    }
  }

  stack {
    db.add STATUS_ITEM {
      data = {created_at: "now"}
    } as $status_item
  }

  response = $status_item
}