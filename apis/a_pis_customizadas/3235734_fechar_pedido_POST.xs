query fecharPedido verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    int pedido_id?
  }

  stack {
    db.patch PEDIDO {
      field_name = "id"
      field_value = $input.pedido_id
      data = {status_pedido_id: 7}
    } as $PEDIDO1
  }

  response = $PEDIDO1
}