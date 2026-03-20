// Add CEP_01 record
query cep_01 verb=POST {
  api_group = "Tech_Food"

  input {
    dblink {
      table = "CEP_01"
    }
  }

  stack {
    db.add CEP_01 {
      data = {
        created_at: "now"
        cep       : $input.cep
        uf        : $input.uf
        cidade    : $input.cidade
      }
    } as $model
  }

  response = $model
}