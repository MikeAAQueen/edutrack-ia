// Delete feedback record.
query "feedback/{feedback_id}" verb=DELETE {
  api_group = "Auxiliares"

  input {
    int feedback_id? filters=min:1
  }

  stack {
    db.del feedback {
      field_name = "id"
      field_value = $input.feedback_id
    }
  }

  response = null
}