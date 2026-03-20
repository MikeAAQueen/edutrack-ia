query atualizarValorPedido verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    int pedido_id?
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/item"
      method = "GET"
      headers = ["Content_Type: application/json"]
    } as $api1
  
    db.query ITEM {
      where = $input.pedido_id == $db.ITEM.pedido_id
      return = {type: "list"}
    } as $ITEM1
  
    var $novo_total {
      value = 0
    }
  
    foreach ($ITEM1) {
      each as $item {
        math.add $novo_total {
          value = $item.subtotal
        }
      }
    }
  
    db.patch PEDIDO {
      field_name = "id"
      field_value = $input.pedido_id
      data = {total: $novo_total}
    } as $PEDIDO1
  }

  response = {self: $PEDIDO1}
}