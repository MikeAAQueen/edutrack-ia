query pegaUsuario verb=GET {
  api_group = "APis Customizadas"

  input {
    text nome? filters=trim
  }

  stack {
  }

  response = null
}