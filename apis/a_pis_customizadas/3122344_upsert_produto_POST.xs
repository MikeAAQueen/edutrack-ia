query upsertProduto verb=POST {
  api_group = "APis Customizadas"

  input {
    text nome? filters=trim
    text descricao? filters=trim
    decimal preco?
    int qtd_disp?
  }

  stack {
    db.add_or_edit PRODUTO {
      field_name = "nome"
      field_value = $input.nome
      data = {
        descricao: $input.descricao
        qtd_disp : $input.qtd_disp
        preco    : $input.preco
      }
    } as $PRODUTO1
  }

  response = $PRODUTO1
}