// Add user record
query user verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "user"
    }
  }

  stack {
    db.add user {
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        papel_id  : $input.papel_id
      }
    } as $model
  }

  response = $model
}