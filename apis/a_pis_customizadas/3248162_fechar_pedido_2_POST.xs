query fecharPedido2 verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    decimal valorTotal?
    int status_pedido_id?
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/abrirPedido"
      method = "POST"
      params = {authToken: $input.authToken}
      headers = ["Content-Type: application/json"]
    } as $api1
  
    db.patch PEDIDO {
      field_name = "id"
      field_value = $api1.response.result.id
      data = {
        total           : $input.valorTotal
        status_pedido_id: $input.status_pedido_id
      }
    } as $PEDIDO1
  }

  response = $PEDIDO1
}