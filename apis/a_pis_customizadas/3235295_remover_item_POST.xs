query removerItem verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    int produto_id?
    int qtd?
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/buscaCliente"
      method = "GET"
      params = {authToken: $input.authToken}
      headers = ["Content-Type: application/json"]
    } as $api1
  
    db.get STATUS_PEDIDO {
      field_name = "status"
      field_value = "CRIADO"
    } as $STATUS_PEDIDO1
  
    db.query PEDIDO {
      where = `$var.api1.response.result.id` == $db.PEDIDO.cliente_01_id && `$var.STATUS_PEDIDO1.id` == $db.PEDIDO.status_pedido_id
      return = {type: "list"}
    } as $PEDIDO1
  
    var $pedido_id {
      value = $PEDIDO1.0.id
    }
  
    db.query ITEM {
      where = $db.ITEM.produto_id == $input.produto_id && $db.ITEM.pedido_id == $pedido_id
      return = {type: "list"}
    } as $ITEM1
  
    conditional {
      if ($ITEM1 != null) {
        api.request {
          url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/item/" ~$var.ITEM1[0].id
          method = "PATCH"
          params = {
            item_id       : $ITEM1[0].id
            pedido_id     : $ITEM1[0].pedido_id
            qtd           : $var.ITEM1[0].qtd - $input.qtd
            valor_unit    : $ITEM1[0].valor_unit
            subtotal      : (($var.ITEM1[0].qtd - $input.qtd)*$var.ITEM1[0].valor_unit)
            produto_id    : $ITEM1[0].produto_id
            status_item_id: $ITEM1[0].status_item_id
          }
        
          headers = ["Content-Type: application/json"]
        } as $api2
      }
    }
  
    db.get ITEM {
      field_name = "id"
      field_value = $api2.response.result.id
    } as $ITEM2
  
    conditional {
      if ($ITEM2.qtd <= 0) {
        db.del ITEM {
          field_name = "id"
          field_value = $ITEM2.id
        }
      }
    }
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/atualizarValorPedido"
      method = "POST"
      params = {authToken: $input.authToken, pedido_id: $pedido_id}
      headers = ["Content_Type: application/json"]
    } as $api3
  }

  response = $api4.response.result
}