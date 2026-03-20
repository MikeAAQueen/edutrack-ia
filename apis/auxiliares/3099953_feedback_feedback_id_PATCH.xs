// Edit feedback record
query "feedback/{feedback_id}" verb=PATCH {
  api_group = "Auxiliares"

  input {
    int feedback_id? filters=min:1
    dblink {
      table = "feedback"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch feedback {
      field_name = "id"
      field_value = $input.feedback_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $feedback
  }

  response = $feedback
}