query adicionarItem verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    int produto_id?
    int qtd?
  }

  stack {
    db.get PRODUTO {
      field_name = "id"
      field_value = $input.produto_id
    } as $PRODUTO1
  
    precondition ($input.qtd <= $PRODUTO1.qtd_disp) {
      error_type = "inputerror"
      error = '"Erro: Quantidade desejada indisponivel"'
    }
  
    db.query STATUS_ITEM {
      where = $PRODUTO1.precisa_produzir == true && $db.STATUS_ITEM.status == "À PRODUZIR" || ($PRODUTO1.precisa_produzir == false && $db.STATUS_ITEM.status == "NÃO PRECISA PRODUZIR")
      return = {type: "list"}
    } as $STATUS_ITEM1
  
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/abrirPedido"
      method = "POST"
      params = {authToken: $input.authToken}
      headers = ["Content-Type: application/json"]
    } as $api1
  
    db.query ITEM {
      where = $STATUS_ITEM1.0.id == $db.ITEM.status_item_id && $api1.response.result.id == $db.ITEM.pedido_id && $PRODUTO1.id == $db.ITEM.produto_id
      return = {type: "list"}
    } as $ITEM1
  
    conditional {
      if ($var.ITEM1[0].qtd > 0) {
        api.request {
          url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/item/" ~$var.ITEM1[0].id
          method = "PATCH"
          params = {
            item_id       : $ITEM1[0].id
            pedido_id     : $ITEM1[0].pedido_id
            qtd           : $var.ITEM1[0].qtd + $input.qtd
            valor_unit    : $ITEM1[0].valor_unit
            subtotal      : (($var.ITEM1[0].qtd + $input.qtd)*$var.ITEM1[0].valor_unit)
            produto_id    : $ITEM1[0].produto_id
            status_item_id: $ITEM1[0].status_item_id
          }
        
          headers = ["Content-Type: application/json"]
        } as $api2
      
        precondition (`$var.api2.response.result.qtd` <= $PRODUTO1.qtd_disp) {
          error_type = "inputerror"
          error = '"Erro: Quantidade desejada indisponivel"'
        }
      
        api.request {
          url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/atualizarValorPedido"
          method = "POST"
          params = {
            authToken: $input.authToken
            pedido_id: $api1.response.result.id
          }
        
          headers = ["Content-Type: application/json"]
        } as $api3
      }
    
      else {
        api.request {
          url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/item"
          method = "POST"
          params = {
            pedido_id     : $api1.response.result.id
            qtd           : $input.qtd
            valor_unit    : $PRODUTO1.preco
            subtotal      : ($input.qtd * $var.PRODUTO1.preco)
            produto_id    : $PRODUTO1.id
            status_item_id: $STATUS_ITEM1[0].id
          }
        
          headers = ["Content-Type: application/json"]
        } as $api2
      
        api.request {
          url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/atualizarValorPedido"
          method = "POST"
          params = {
            authToken: $input.authToken
            pedido_id: $api1.response.result.id
          }
        
          headers = ["Content-Type: application/json"]
        } as $api3
      }
    }
  }

  response = $api3.response.result
}