// Add CLIENTE_01 record
query cliente_01 verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "CLIENTE_01"
    }
  }

  stack {
    db.add CLIENTE_01 {
      data = {
        created_at       : "now"
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