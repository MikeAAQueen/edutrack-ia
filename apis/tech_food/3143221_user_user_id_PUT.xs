// Update user record
query "user/{user_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int user_id? filters=min:1
    dblink {
      table = "user"
    }
  }

  stack {
    db.edit user {
      field_name = "id"
      field_value = $input.user_id
      data = {
        name    : $input.name
        email   : $input.email
        papel_id: $input.papel_id
      }
    } as $model
  }

  response = $model
}