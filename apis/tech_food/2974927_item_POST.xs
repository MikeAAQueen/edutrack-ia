// Add ITEM record
query item verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "ITEM"
    }
  }

  stack {
    db.add ITEM {
      data = {created_at: "now"}
    } as $item
  }

  response = $item
}