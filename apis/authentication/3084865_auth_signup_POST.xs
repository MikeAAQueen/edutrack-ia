// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name?
    email email? filters=lower|trim
    password password?
    int papel_id?
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    precondition ($user == null) {
      error_type = "accessdenied"
      error = "This account is already in use."
    }
  
    db.add user {
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
        papel_id  : ($input.papel_id)|first_notempty:7|first_notnull:7
      }
    } as $user
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 3600
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken}
}