// Add STATUS_TESTORNO record
query status_testorno verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "STATUS_TESTORNO"
    }
  }

  stack {
    db.add STATUS_TESTORNO {
      data = {created_at: "now"}
    } as $status_testorno
  }

  response = $status_testorno
}