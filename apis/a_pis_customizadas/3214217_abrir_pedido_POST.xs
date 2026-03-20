query abrirPedido verb=POST {
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
  
    db.get STATUS_PEDIDO {
      field_name = "status"
      field_value = "CRIADO"
    } as $STATUS_PEDIDO1
  
    db.query PEDIDO {
      where = `$var.api1.response.result.id` == $db.PEDIDO.cliente_01_id && `$var.STATUS_PEDIDO1.id` == $db.PEDIDO.status_pedido_id
      return = {type: "list"}
    } as $PEDIDO1
  
    conditional {
      if (`$var.api1.response.result.id` == $var.PEDIDO1.[0].cliente_01_id && `$var.STATUS_PEDIDO1.id` == $var.PEDIDO1.[0].status_pedido_id) {
        var $resultado {
          value = $var.PEDIDO1[0]
        }
      }
    
      else {
        api.request {
          url = "https://x8ki-letl-twmt.n7.xano.io/api:Y1wXhL7_/pedido"
          method = "POST"
          params = {
            total           : 0
            nfc_e           : null
            cod_entrega     : null
            cliente_01_id   : $api1.response.result.id
            status_pedido_id: $STATUS_PEDIDO1.id
          }
        
          headers = ["Content-Type: application/json"]
        } as $api2
      
        var $resultado {
          value = `$var.api2.response.result`
        }
      }
    }
  }

  response = $resultado
}