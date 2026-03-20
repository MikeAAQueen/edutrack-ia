// Query all STATUS_OE records
query status_oe verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query STATUS_OE {
      return = {type: "list"}
    } as $status_oe
  }

  response = $status_oe
}