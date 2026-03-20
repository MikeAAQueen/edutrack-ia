query marcarEnderecoPadrao verb=PATCH {
  api_group = "APis Customizadas"

  input {
    int endereco_id?
  }

  stack {
    db.get ENDERECO_01 {
      field_name = "id"
      field_value = $input.endereco_id
    } as $ENDERECO_011
  
    db.patch ENDERECO_01 {
      field_name = "id"
      field_value = $input.endereco_id
      data = {padrao: true}
    } as $ENDERECO_012
  
    db.query ENDERECO_01 {
      where = $ENDERECO_011.cliente_id == $db.ENDERECO_01.cliente_id && $ENDERECO_011.id != $db.ENDERECO_01.id
      return = {type: "list"}
    } as $ENDERECO_013
  
    array.map ($ENDERECO_013) {
      by = {id: $this.id, padrao: false}
    } as $x1
  
    db.bulk.patch ENDERECO_01 {
      items = $x1
    } as $ENDERECO_014
  }

  response = {Padrao: $ENDERECO_012, NaoPadrao: $ENDERECO_014}
}