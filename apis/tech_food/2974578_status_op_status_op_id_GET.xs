// Get STATUS_OP record
query "status_op/{status_op_id}" verb=GET {
  api_group = "Tech_Food"

  input {
    int status_op_id? filters=min:1
  }

  stack {
    db.get STATUS_OP {
      field_name = "id"
      field_value = $input.status_op_id
    } as $status_op
  
    precondition ($status_op != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $status_op
}