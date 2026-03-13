# EduTrack AI - Guia de Contexto e Regras para IA (Antigravity Agent)

Este arquivo define o escopo, arquitetura, stack tecnológica e regras de negócio do projeto **EduTrack AI**. O objetivo é prover contexto imediato para o agente de IA (Antigravity) para que atue de forma mais assertiva, mantendo a consistência do código e evitando refatorações desnecessárias ou arquiteturas conflitantes.

---

## 1. Visão Geral do Projeto
O **EduTrack AI** é um Web App Responsivo acadêmico com foco na gestão de disciplinas e tarefas por estudantes. A principal característica é a delegação do backend para o **Xano**, enquanto o frontend e a lógica de apresentação residem puramente em **Python + Streamlit**.

- **Objetivo Principal:** Permitir CRUD de disciplinas e tarefas e dispor de Dashboards avançados (com métricas via Pandas e gráficos via Plotly) e emissão de relatórios semanais.

## 2. Stack Tecnológica (Imutável)
- **Frontend / UI:** Python (Streamlit). *Nenhum framework HTML/JS/CSS nativo (React, Vue, etc.) deve ser introduzido.*
- **Backend / DB / API:** Xano (Plataforma No-Code).
- **Tratamento de Dados Locais:** Pandas.
- **Gráficos:** Plotly (via `plotly.express` e renderizado com `st.plotly_chart`).
- **Geração de PDF:** Biblioteca genérica `fpdf`.
- **Estabilidade / Resiliência de Rede:** Biblioteca `tenacity` (utilizada para lidar com Rate Limiting).

## 3. Arquitetura do Repositório
O projeto modularizado segue o padrão (Root: `c:\Projects\edutrack-ia`):

```text
/
├── .venv/                   # Ambiente virtual (ignorar em commits/buscas)
├── .streamlit/
│   └── secrets.toml         # Configurações do ambiente Streamlit (Não deve conter a URL de dev)
├── components/              # Componentes de UI modulares
│   ├── auth.py              # Tela de Login (`st.form` e validações)
│   ├── dashboard.py         # Métricas (`st.metric`) e gráficos (`Plotly`)
│   ├── subjects.py          # Gerenciamento (CRUD) de Disciplinas
│   └── tasks.py             # Gerenciamento (CRUD) e filtragem de Tarefas
├── services/
│   └── xano.py              # Camada EXCLUSIVA de comunicação com a API (requests), Mapeamento inglês/português e retry logic (`tenacity`)
├── utils/                   # Lógicas reaproveitáveis sem UI nativa
│   ├── progress.py          # Lógica de cálculo atrelada a métricas (Pandas)
│   └── report.py            # Responsável apenas pela formatação e geração do binário PDF
├── app.py                   # Ponto de entrada (`st.set_page_config`, Router e Controle de Sessão)
├── .env                     # Variáveis de ambiente locais (`XANO_API_URL`, `AUTH_API_URL`)
└── requirements.txt         # Lista de dependências Python
```

## 4. Banco de Dados e Mapeamento de API (Xano)
O Xano utiliza nomenclaturas em **português**, mas a nossa aplicação processa a UI utilizando nomenclaturas em **inglês**. O adaptador `services/xano.py` é responsável exclusivo por essa tradução bidirecional.

### Tabela: `disciplinas`
- API Endpoint base: `/disciplinas`
- Dicionário de envio/recebimento:
  - `id` -> `id`
  - `nome` -> `name`
  - `professor` -> `professor`
  - `creditos` -> `credits`

### Tabela: `tarefas`
- API Endpoint base: `/tarefas`
- Dicionário de envio/recebimento:
  - `id` -> `id`
  - `disciplinas_id` -> `subject_id`
  - `titulo` -> `title`
  - `data_entrega` -> `due_date`
  - `completado` -> `completed`
  - `nota` -> `grade`

### Regra de API Calls:
1. Nenhuma view (arquivos em `/components/`) ou ferramenta (arquivos em `/utils/`) deve implementar a biblioteca `requests` ou realizar HTTP calls diretamente. **Qualquer contato HTTP deve sempre passar pelo wrapper em `services/xano.py`**.
2. **Rate Limiting:** Todas as funções `GET` e `POST` listadas em `services/xano.py` devem possuir decorators `@get_retry_decorator()` ou similar da biblioteca Tenacity para lidar com respostas HTTP 429 do Xano.
3. Funções `GET` devem ser decoradas com `@st.cache_data(ttl=X)` (onde aplicável) após a proteção do Tenacity.

## 5. Convenções e Regras de UI/UX
- **Estado Global:** O estado atual (Autenticação, Token do Xano, Nome do Usuário logado) fica unicamente em `st.session_state`.
- **Feedbacks:** Interações positivas ou finalização de tarefas exigem gratificação visual, como `st.balloons()` ou `st.toast()`.
- **Dataframes:** A renderização de arrays de dados crús deve passar pelo Pandas (transformação em DataFrame) antes de ser enviada ao `st.data_editor` ou filtrada (usando máscaras).
- **Semantismo de Exceção:** Informações irrelevantes ao usuário não podem ser impressas com `st.error`. Falhas de requisição por queda da API do Xano devem resultar em mensagens amigáveis ("Serviço instável, tente em instantes").

## 6. Procedimentos do Agente Antigravity
Sempre que for solicitado a criar uma nova feature:
1. Verifique onde a adição lógica deve ocorrer com base na **Arquitetura**.
2. Atualize o `services/xano.py` primeiro (se houver endpoints novos no Xano). Lembre-se do mapeamento PT-BR <-> EN e inclua Retry Logic.
3. Se for UI, crie em `components/` e importe em `app.py`, garantindo o padrão Responsivo.
4. Qualquer arquivo, ao ser atualizado, deve ser avaliado no isolamento de pacotes (não exportar nada que já não esteja no escopo previsto).
