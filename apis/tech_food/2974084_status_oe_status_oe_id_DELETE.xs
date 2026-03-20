// Delete STATUS_OE record.
query "status_oe/{status_oe_id}" verb=DELETE {
  api_group = "Tech_Food"

  input {
    int status_oe_id? filters=min:1
  }

  stack {
    db.del STATUS_OE {
      field_name = "id"
      field_value = $input.status_oe_id
    }
  }

  response = null
}