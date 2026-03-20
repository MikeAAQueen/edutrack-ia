table TRANSACAO {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text clienteasaas? filters=trim
    text idpayment? filters=trim
  
    // Por exemplo CREDT_CARD, BOLETO, PIX
    text tipo? filters=trim
  
    decimal valor?
    date? datavenc?
    text descricao? filters=trim
    int status_transacao_id? {
      table = "STATUS_TRANSACAO"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "gin", field: [{name: "xdo", op: "jsonb_path_op"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}