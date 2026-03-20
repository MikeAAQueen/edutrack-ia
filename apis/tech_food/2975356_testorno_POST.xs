// Add TESTORNO record
query testorno verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "TESTORNO"
    }
  }

  stack {
    db.add TESTORNO {
      data = {created_at: "now"}
    } as $testorno
  }

  response = $testorno
}