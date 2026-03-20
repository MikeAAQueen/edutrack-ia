table PRODUTO {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      sensitive = true
    }
  
    text nome? filters=trim
    text descricao? filters=trim
    int qtd_disp?
    decimal preco?
    image? imagem?
    bool precisa_produzir?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "nome", op: "asc"}]}
  ]
}