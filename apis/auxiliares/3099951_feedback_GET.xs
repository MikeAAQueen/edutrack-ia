// Query all feedback records
query feedback verb=GET {
  api_group = "Auxiliares"

  input {
  }

  stack {
    db.query feedback {
      return = {type: "list"}
    } as $feedback
  }

  response = $feedback
}