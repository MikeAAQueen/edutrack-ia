// Get feedback record
query "feedback/{feedback_id}" verb=GET {
  api_group = "Auxiliares"

  input {
    int feedback_id? filters=min:1
  }

  stack {
    db.get feedback {
      field_name = "id"
      field_value = $input.feedback_id
    } as $feedback
  
    precondition ($feedback != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $feedback
}