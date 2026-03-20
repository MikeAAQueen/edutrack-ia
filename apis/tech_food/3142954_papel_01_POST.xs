// Add PAPEL_01 record
query papel_01 verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "PAPEL_01"
    }
  }

  stack {
    db.add PAPEL_01 {
      data = {created_at: "now", papel: $input.papel}
    } as $model
  }

  response = $model
}