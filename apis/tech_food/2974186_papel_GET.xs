// Query all PAPEL records
query papel verb=GET {
  api_group = "Tech_Food"

  input {
  }

  stack {
    db.query PAPEL {
      return = {type: "list"}
    } as $papel
  }

  response = $papel
}