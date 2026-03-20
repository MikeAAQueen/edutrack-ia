table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1 {
      sensitive = true
    }
  
    int papel_id?=7 {
      table = "PAPEL_01"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
    {type: "gin", field: [{name: "xdo", op: "jsonb_path_op"}]}
  ]
}