// Get user record
query "user/{user_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
}