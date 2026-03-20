// Add FAQ record
query faq verb=POST {
  api_group = "Auxiliares"

  input {
    dblink {
      table = "FAQ"
    }
  }

  stack {
    db.add FAQ {
      data = {created_at: "now"}
    } as $faq
  }

  response = $faq
}