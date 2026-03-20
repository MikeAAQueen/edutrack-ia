// Dado um CEP, atualize se já existir, inserir se não, sempre devolver um CEP
query upsertCEP verb=POST {
  api_group = "APis Customizadas"

  input {
    text cep? filters=trim
    text cidade? filters=trim
    text estado? filters=trim
  }

  stack {
    db.query CEP_01 {
      where = $db.CEP_01.cep == $input.cep
      return = {type: "list"}
    } as $CEP_011
  
    conditional {
      if ($var.CEP_011[0].cep == $input.cep) {
        db.patch CEP_01 {
          field_name = "id"
          field_value = $var.CEP_011[0].id
          data = {cidade: $input.cidade, uf: $input.estado}
        } as $CEP_012
      }
    
      else {
        db.add CEP_01 {
          data = {
            created_at: "now"
            cep       : $input.cep
            uf        : $input.estado
            cidade    : $input.cidade
          }
        } as $CEP_012
      }
    }
  }

  response = $CEP_012
}