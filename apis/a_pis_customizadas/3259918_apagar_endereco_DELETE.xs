query apagarEndereco verb=DELETE {
  api_group = "APis Customizadas"

  input {
    int idEndereco?
  }

  stack {
    db.del ENDERECO_01 {
      field_name = "id"
      field_value = $input.idEndereco
    }
  }

  response = $ENDERECO_011
}