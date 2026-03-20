query fecharTransacao verb=POST {
  api_group = "Asaas"

  input {
    text idPay? filters=trim
  }

  stack {
    db.query TRANSACAO {
      where = $db.TRANSACAO.idpayment == $input.idPay && $db.TRANSACAO.status_transacao_id == 1
      return = {type: "list"}
    } as $TRANSACAO1
  
    db.edit TRANSACAO {
      field_name = "id"
      field_value = $TRANSACAO1.0.id
      data = {status_transacao_id: 5}
    } as $TRANSACAO2
  }

  response = $TRANSACAO2
}