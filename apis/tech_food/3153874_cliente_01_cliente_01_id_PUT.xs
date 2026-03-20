// Update CLIENTE_01 record
query "cliente_01/{cliente_01_id}" verb=PUT {
  api_group = "Tech_Food"

  input {
    int cliente_01_id? filters=min:1
    dblink {
      table = "CLIENTE_01"
    }
  }

  stack {
    db.edit CLIENTE_01 {
      field_name = "id"
      field_value = $input.cliente_01_id
      data = {
        user_id          : $input.user_id
        celular          : $input.celular
        email            : $input.email
        cod_verif        : $input.cod_verif
        cpf              : $input.cpf
        status_cliente_id: $input.status_cliente_id
      }
    } as $model
  }

  response = $model
}