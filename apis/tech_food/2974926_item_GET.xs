// Query all ITEM records
query item verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query ITEM {
      return = {type: "list"}
    } as $item
  }

  response = $item
}