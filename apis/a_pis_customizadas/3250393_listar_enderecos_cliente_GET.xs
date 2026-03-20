query listar_enderecos_cliente verb=GET {
  api_group = "APis Customizadas"

  input {
    int cliente_id?
  }

  stack {
    db.query ENDERECO_01 {
      where = $db.ENDERECO_01.cliente_id == $input.cliente_id
      return = {type: "list"}
    } as $ENDERECO_011
  }

  response = $ENDERECO_011
}