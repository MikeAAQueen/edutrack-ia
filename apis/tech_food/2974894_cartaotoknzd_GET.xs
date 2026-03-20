// Query all CARTAOTOKNZD records
query cartaotoknzd verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query CARTAOTOKNZD {
      return = {type: "list"}
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
}