table TESTORNO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    decimal valor?
    int solcancelamento_id? {
      table = "SOLCANCELAMENTO"
    }
  
    int status_testorno_id?=1 {
      table = "STATUS_TESTORNO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}