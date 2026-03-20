// Atualiza o endereço como sendo o padrão dentre todos os endereços do cliente.
query marcarEnderecoPadrao verb=PATCH {
  api_group = "Auxiliares"

  input {
    int endereco_id?
  }

  stack {
    db.get ENDERECO_01 {
      field_name = "id"
      field_value = $input.endereco_id
    } as $ENDERECO1
  
    db.query ENDERECO_01 {
      where = $db.ENDERECO_01.cliente_id == $ENDERECO1.cliente_id
      return = {type: "list"}
    } as $ENDERECO2
  
    array.map ($ENDERECO2) {
      by = {id: $this.id, padrao: false}
    } as $x1
  
    db.bulk.patch ENDERECO_01 {
      items = $x1
    } as $ENDERECO3
  }

  response = $ENDERECO3
}