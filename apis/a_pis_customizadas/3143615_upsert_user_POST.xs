query upsertUser verb=POST {
  api_group = "APis Customizadas"

  input {
    email email? filters=trim|lower
    text nome? filters=trim
    password senha? {
      sensitive = true
      visibility = "internal"
    }
  
    int papel_id?
  }

  stack {
    db.add_or_edit user {
      field_name = "email"
      field_value = $input.email
      data = {
        name    : $input.nome
        password: $input.senha
        papel_id: $input.papel_id
      }
    } as $user1
  }

  response = $user1
}