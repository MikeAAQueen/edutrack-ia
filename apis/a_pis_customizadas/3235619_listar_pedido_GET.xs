query listarPedido verb=GET {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    int pedido_id?
  }

  stack {
    db.get PEDIDO {
      field_name = "id"
      field_value = $input.pedido_id
    } as $PEDIDO1
  
    db.query ITEM {
      where = $db.ITEM.pedido_id == $input.pedido_id
      return = {type: "list"}
      output = [
        "id"
        "created_at"
        "pedido_id"
        "qtd"
        "valor_unit"
        "subtotal"
        "produto_id"
        "status_item_id"
      ]
    
      addon = [
        {
          name  : "PRODUTO"
          output: [
            "id"
            "nome"
            "descricao"
            "qtd_disp"
            "preco"
            "precisa_produzir"
            "imagem.access"
            "imagem.path"
            "imagem.name"
            "imagem.type"
            "imagem.size"
            "imagem.mime"
            "imagem.meta"
            "imagem.url"
          ]
          input : {PRODUTO_id: $output.produto_id}
          as    : "_produto"
        }
        {
          name  : "STATUS_ITEM"
          output: ["status"]
          input : {STATUS_ITEM_id: $output.status_item_id}
          as    : "_status_item"
        }
        {
          name  : "STATUS_PEDIDO"
          output: ["status"]
          input : {STATUS_PEDIDO_id: $PEDIDO1.status_pedido_id}
          as    : "_status_pedido"
        }
        {
          name  : "PEDIDO_1"
          output: ["total"]
          input : {PEDIDO_id: $output.pedido_id}
          as    : "total_pedido"
        }
      ]
    } as $ITEM1
  }

  response = $ITEM1
}