// Add CLIENTE record
query cliente verb=POST {
  api_group = "Tech_Food"
  auth = "USER"

  input {
    dblink {
      table = "CLIENTE"
    }
  }

  stack {
    db.add CLIENTE {
      data = {
        created_at       : "now"
        nome             : $input.Nome
        celular          : $input.celular
        cpf              : $input.cpf
        status_cliente_id: $input.status_cliente_id
        user_id          : $input.user_id
      }
    } as $model
  }

  response = $model
}