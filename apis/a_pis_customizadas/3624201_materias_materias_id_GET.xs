// Get materias record
query "materias/{materias_id}" verb=GET {
  api_group = "APis Customizadas"

  input {
    int materias_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.materias_id
    } as $materias
  
    precondition ($materias != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $materias
}