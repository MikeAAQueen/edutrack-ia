// Delete ITEM record.
query "item/{item_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int item_id? filters=min:1
  }

  stack {
    db.del ITEM {
      field_name = "id"
      field_value = $input.item_id
    }
  }

  response = null
}