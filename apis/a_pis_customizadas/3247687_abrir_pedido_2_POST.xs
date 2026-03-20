query abrirPedido2 verb=POST {
  api_group = "APis Customizadas"

  input {
    text authToken? filters=trim
    int status_item_id?
    object[] itens_carrinho {
      schema {
        int idProduto?
        int qtdSelecionadaProduto?
        decimal precoProduto?
      }
    }
  }

  stack {
    api.request {
      url = "https://x8ki-letl-twmt.n7.xano.io/api:voP_Xcib/abrirPedido"
      method = "POST"
      params = {authToken: $input.authToken}
      headers = ["Content-Type: application/json"]
    } as $api1
  
    foreach ($input.intens_carrinho) {
      each as $item {
        db.add ITEM {
          data = {
            created_at    : "now"
            pedido_id     : `$api1.response.result.id`
            qtd           : $item.qtdSelecionadaProduto
            valor_unit    : $item.precoProduto
            subtotal      : $item.precoProduto|multiply:$item.qtdSelecionadaProduto
            produto_id    : $item.idProduto
            status_item_id: 1
          }
        } as $ITEM1
      }
    }
  }

  response = $ITEM1
}