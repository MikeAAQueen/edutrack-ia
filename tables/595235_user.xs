// Meu primeiro comentário via VS Code.
table USER {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text nome? filters=trim
    email email? filters=trim|lower
    password password filters=min:8|minAlpha:1|minDigit:1 {
      sensitive = true
    }
  
    int papel_id?=6 {
      table = "PAPEL"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]
}