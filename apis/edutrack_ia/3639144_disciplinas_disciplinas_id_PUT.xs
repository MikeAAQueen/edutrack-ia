// Update disciplinas record
query "disciplinas/{disciplinas_id}" verb=PUT {
  api_group = "Edutrack-ia"
  auth = "user"

  input {
    int disciplinas_id? filters=min:1
    dblink {
      table = "disciplinas"
    }
  }

  stack {
    db.edit disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
      data = {
        nome     : $input.nome
        professor: $input.professor
        creditos : $input.creditos
      }
    } as $model
  }

  response = $model
}