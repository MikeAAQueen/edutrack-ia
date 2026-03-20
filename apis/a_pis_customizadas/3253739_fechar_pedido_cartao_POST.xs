query fecharPedidoCartao verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/buscaCliente"
      method = "GET"
      params = {authToken: $input.authToken}
      headers = ["Content-Type: application/json"]
    } as $api1
  
    db.query PEDIDO {
      where = $db.PEDIDO.cliente_01_id == $api1.response.result.id && $db.PEDIDO.status_pedido_id == 1
      return = {type: "list"}
    } as $PEDIDO1
  
    db.patch PEDIDO {
      field_name = "id"
      field_value = $PEDIDO1.0.id
      data = {status_pedido_id: 7}
    } as $PEDIDO2
  }

  response = $PEDIDO2
}