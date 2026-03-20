// Add CARTAOTOKNZD record
query cartaotoknzd verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "CARTAOTOKNZD"
    }
  }

  stack {
    db.add CARTAOTOKNZD {
      data = {created_at: "now"}
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
}