// Query all STATUS_ITEM records
query status_item verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query STATUS_ITEM {
      return = {type: "list"}
    } as $status_item
  }

  response = $status_item
}