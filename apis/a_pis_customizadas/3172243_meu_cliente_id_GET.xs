query meu_cliente_id verb=GET {
  api_group = "APis Customizadas"
  auth = "user"

  input {
  }

  stack {
    db.query CLIENTE_01 {
      where = `$db.CLIENTE_01.user_id == \`\\\`auth.id\\\`\``
      return = {type: "list"}
    } as $CLIENTE_011
  }

  response = "cliente_011.0.cliente_id"
}