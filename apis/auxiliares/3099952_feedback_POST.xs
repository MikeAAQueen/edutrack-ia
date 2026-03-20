// Add feedback record
query feedback verb=POST {
  api_group = "Auxiliares"

  input {
    dblink {
      table = "feedback"
    }
  }

  stack {
    db.add feedback {
      data = {created_at: "now"}
    } as $feedback
  }

  response = $feedback
}