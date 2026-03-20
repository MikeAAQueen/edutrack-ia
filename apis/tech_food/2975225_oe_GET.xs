// Query all OE records
query oe verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query OE {
      return = {type: "list"}
    } as $oe
  }

  response = $oe
}