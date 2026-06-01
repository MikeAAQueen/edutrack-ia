# Guia de Apresentação e Defesa do Projeto: EduTrack AI 🎓

Este documento é o seu guia definitivo para apresentar o **EduTrack AI** e se blindar contra as perguntas mais difíceis da banca de professores. Ele explica as decisões arquiteturais, o funcionamento do código e como justificar cada ferramenta utilizada.

---

## 1. Visão Geral da Arquitetura
O EduTrack AI é uma aplicação construída em **Python**, utilizando o **Streamlit** para o Frontend (interface do usuário) e o **Xano** (uma plataforma No-Code/Low-Code robusta) para o Backend e Banco de Dados.

- **Frontend (Streamlit):** Responsável por renderizar a interface, gerenciar as sessões de login e exibir os gráficos de desempenho acadêmico.
- **Backend (Xano):** Guarda os dados dos usuários, disciplinas, professores, tarefas e notas, além de expor as rotas da API (endpoints) para comunicação segura com o Streamlit.

---

## 2. Estrutura do Projeto Explicada (Para a Banca)

Se a banca pedir para você abrir o código ou explicar a estrutura de pastas, use estes argumentos:

* **`app.py`**: É o coração da aplicação no Frontend. Ele configura o estado inicial (Session State) para manter o usuário logado, injeta estilos CSS e utiliza o roteador nativo do Streamlit (`st.navigation`) para exibir o Dashboard, Disciplinas, Professores, Tarefas e Anotações.
* **`components/`**: Onde residem as páginas e blocos visuais da aplicação. Separamos o código em componentes (como `auth.py`, `dashboard.py`, `professores.py`, etc.) para manter o projeto escalável, limpo e modularizado (o que demonstra boas práticas de Engenharia de Software).
* **`services/xano.py`**: É a camada de serviço (Service Layer). Este arquivo concentra TODA a comunicação via HTTP/Requests com as APIs do Xano. Nele implementamos as funções de CRUD (Criar, Ler, Atualizar, Deletar), estratégias de "retry" (tentar de novo se a internet falhar) e cache (`@st.cache_data`) para deixar o app super rápido e não sobrecarregar o servidor do Xano.
* **`utils/report.py`**: É responsável pela lógica de geração do Relatório Acadêmico em PDF. Usamos a biblioteca `fpdf` para desenhar o PDF e `matplotlib` para gerar os gráficos (Notas, Faltas e Tarefas) injetados dentro do relatório.
* **`apis/authentication` e `apis/edutrack_ia`**: Pastas que espelham as APIs e rotas utilizadas no Xano. A `authentication` lida com login, tokens JWT e registro. A `edutrack_ia` lida com as regras de negócio de educação (disciplinas, tarefas). Isso mostra que nossa arquitetura divide responsabilidades.
* **`tables/`, `.xano/config` e `.xano/objects.json`**: Estes arquivos e pastas representam a modelagem do nosso Banco de Dados Relacional configurado no Xano. O arquivo `objects.json` funciona como um "schema" (esquema) que mapeia nossas entidades. Mostra para a banca que o backend está documentado na raiz do projeto.
* **`.env`**: Arquivo crucial de Segurança da Informação. Ele guarda as chaves de API (`XANO_API_URL` e `AUTH_API_URL`) e variáveis sensíveis, que **nunca** devem ser "commitadas" num repositório público do GitHub.
* **`.gemini/skills/streamlit-expert`**: A ÚNICA skill (habilidade de IA) utilizada no desenvolvimento. Nós usamos a IA de forma **guiada e controlada** como um "Pair Programmer" para otimizar componentes do Streamlit, mas a lógica de negócios e arquitetura nós definimos.
* **`.venv`**: É a pasta do Ambiente Virtual Python. Embora vocês não a usem diretamente para rodar no dia a dia, **diga à banca**: *"O `.venv` está no projeto como uma boa prática global da linguagem Python para isolar as dependências (bibliotecas) do projeto, evitando conflitos com outras versões instaladas na máquina."*

---

## 3. Blindagem: Perguntas Frequentes da Banca e Como Responder

Aqui estão as perguntas mais capciosas que os professores costumam fazer e como você deve responder para demonstrar domínio absoluto do projeto.

### ❓ Pergunta 1: *"Por que vocês usaram o Xano (ferramenta Low-Code) no backend em vez de subir um banco local ou usar Django/Flask?"*
**Sua Resposta:** *"Escolhemos o Xano para acelerar o desenvolvimento, focando no que realmente importa: a experiência do usuário e as regras de negócio. O Xano nos provê escalabilidade, segurança em nuvem (Endpoints RESTful e autenticação via Token), e a facilidade de gerenciar o banco de dados sem precisar lidar com a complexidade de configuração de infraestrutura. Isso simula um ambiente moderno e ágil."*

### ❓ Pergunta 2: *"Como é feita a segurança das informações e senhas dos alunos?"*
**Sua Resposta:** *"A segurança é feita em duas frentes. No Frontend, nós nunca guardamos senhas no código; usamos o arquivo `.env` para esconder as URLs sensíveis do backend. No login, os dados vão para o Xano. O Xano não retorna a senha, mas sim um **Token de Autenticação (Bearer Token)**. O Streamlit armazena esse token no `session_state` e o envia de forma segura no cabeçalho (Header) de todas as requisições (como é visível em `services/xano.py`)."*

### ❓ Pergunta 3: *"Como contornaram as limitações do Streamlit, que recarrega a página toda hora?"*
**Sua Resposta:** *"Para evitar lentidão, aplicamos duas técnicas de otimização em `services/xano.py`: a primeira foi usar o decorador `@st.cache_data`, que salva em memória os retornos da API (como listas de disciplinas). A segunda foi implementar a biblioteca `tenacity` para realizar 'retries' em caso de falha de internet ou Rate Limit, garantindo resiliência e estabilidade."*

### ❓ Pergunta 4: *"Onde exatamente está o banco de dados e como ocorrem exclusões dependentes?"*
**Sua Resposta:** *"O banco de dados relacional está hospedado na nuvem do Xano. Para garantir a integridade, quando um professor é deletado, nosso código em `services/xano.py` implementa uma **exclusão em cascata (Cascade Delete)** automatizada: ele busca todas as disciplinas daquele professor e deleta, e em seguida, deleta as tarefas dessas disciplinas para não deixar dados órfãos."*

### ❓ Pergunta 5: *"Vi menção à skill 'streamlit-expert'. Vocês usaram IA para fazer o projeto?"*
**Sua Resposta:** *"A IA foi utilizada estritamente como um **assistente de produtividade**, nunca como o cérebro do projeto. Nós idealizamos as tabelas, as regras de negócio, a estrutura do relatório e a arquitetura. A IA ajudou com a sintaxe visual do frontend e geração rápida de código repetitivo (Boilerplate). A revisão de segurança, arquitetura REST e testes fomos nós que fizemos, garantindo autoria."*

### ❓ Pergunta 6: *"Se tivessem mais tempo, o que melhorariam no sistema?"*
**Sua Resposta:** *"Criaríamos um sistema de notificações automático (por email ou push) avisando os alunos sobre tarefas próximas do vencimento, e implementaríamos perfis de acesso diferentes (Visão Aluno vs Visão Professor). Também faríamos testes unitários automatizados cobrindo todo o gerador de PDF (`utils/report.py`)."*

---

## 4. Roteiro de Apresentação (Passo a Passo Sugerido)

1. **Apresentação do Problema (2 min):** Falar da dificuldade de gerenciar notas, disciplinas e faltas.
2. **Apresentação da Solução - EduTrack AI (2 min):** Dizer que é um sistema unificado, em nuvem e rápido.
3. **Demonstração Prática (5 min):**
   - Fazer login.
   - Mostrar o **Dashboard** e gráficos de análise.
   - Cadastrar um Professor e uma Disciplina (CRUD).
   - Gerar e mostrar um **Relatório em PDF** (`utils/report.py`).
4. **Arquitetura Técnica (3 min):**
   - Mostrar a pasta `services/xano.py` (citar integrações, APIs e Cache).
   - Citar a separação inteligente entre as páginas (`components/`).
5. **Conclusão e Agradecimentos.**

Boa sorte na apresentação! Se você dominar esses tópicos, a banca ficará impressionada com a maturidade técnica do seu projeto. 🚀
