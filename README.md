# TaskFlow Agent

**Assistente virtual inteligente para gerenciamento de tarefas, desenvolvido com Python, LangChain e Ollama.**

O TaskFlow Agent é um agente conversacional integrado ao [TaskFlow API](https://github.com/Florido-hub/TaskFlow), permitindo que usuários interajam com suas tarefas por meio de linguagem natural.

Utilizando modelos de linguagem (LLMs) executados localmente com Ollama e o mecanismo de *Tool Calling* do LangChain, o agente interpreta solicitações e utiliza ferramentas para consultar e gerenciar informações disponibilizadas pelo backend.

## Arquitetura

O projeto possui uma arquitetura independente do backend, comunicando-se com ele por meio de requisições HTTP à API REST.

```text
┌──────────────────────────────┐
│           Usuário            │
└──────────────┬───────────────┘
               │ Mensagem
               ▼
┌──────────────────────────────┐
│       TaskFlow Agent         │
│                              │
│  Python + LangChain          │
│  Ollama (LLM)                │
│                              │
│  ┌────────────────────────┐  │
│  │     Agent / Tools      │  │
│  └───────────┬────────────┘  │
│              │               │
│  ┌───────────▼────────────┐  │
│  │      API Client        │  │
│  └───────────┬────────────┘  │
└──────────────┼───────────────┘
               │ HTTP / REST
               ▼
┌──────────────────────────────┐
│        TaskFlow API          │
│       Java + Spring Boot     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│            MySQL             │
└──────────────────────────────┘
```

O agente não acessa diretamente o banco de dados. Toda operação sobre as tarefas é realizada por meio dos endpoints disponibilizados pelo backend.

## Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de desenvolvimento |
| LangChain | Construção e orquestração do agente |
| LangGraph | Execução do fluxo de agentes |
| Ollama | Execução local dos modelos de linguagem |
| ChatOllama | Integração entre LangChain e Ollama |
| Requests | Comunicação HTTP com a API |
| Python-dotenv | Gerenciamento de variáveis de ambiente |

## Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

- Python 3.10 ou superior.
- Git.
- Ollama instalado e em execução.
- Um modelo de linguagem compatível com Tool Calling.
- TaskFlow API em execução.

## 1. Instalação do Ollama

O [Ollama](https://ollama.com/) permite executar modelos de linguagem localmente, sem depender de uma API de inferência hospedada externamente.

Acesse o site oficial e faça o download da versão compatível com seu sistema operacional:

**[Download do Ollama](https://ollama.com/download)**

Após a instalação, verifique se ele está disponível no terminal:

```bash
ollama --version
```

Por padrão, o serviço local do Ollama utiliza o endereço:

```text
http://localhost:11434
```

## 2. Escolha do modelo de linguagem

**Atenção: o modelo precisa oferecer suporte a Tool Calling.**

O agente utiliza ferramentas para interagir com a API TaskFlow. Portanto, modelos que não suportam chamadas de ferramentas não funcionarão corretamente com essa arquitetura.

Algumas opções disponíveis no Ollama:

| Modelo | Identificador | Tool Calling |
|---|---|---|
| Qwen 3 | `qwen3` | Sim |
| Qwen 2.5 | `qwen2.5:7b` | Sim |
| Llama 3.1 | `llama3.1:8b` | Sim |

Consulte também a [documentação oficial de Tool Calling do Ollama](https://docs.ollama.com/capabilities/tool-calling).

### Baixando um modelo

Como exemplo, utilizando Qwen 2.5:

```bash
ollama pull qwen2.5:7b
```

Para verificar os modelos instalados:

```bash
ollama list
```

Para testar o modelo:

```bash
ollama run qwen2.5:7b
```

**Observação:** o tamanho do modelo influencia os requisitos de memória e desempenho. Escolha uma variante compatível com os recursos disponíveis no seu computador.

## 3. Clonando o projeto

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO_TASKFLOW_AGENT>
```

Entre na pasta:

```bash
cd Taskflow-Agent
```

## 4. Configurando o ambiente Python

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Caso ainda não exista um arquivo `requirements.txt`, instale os pacotes manualmente:

```bash
pip install langchain langgraph langchain-ollama requests python-dotenv
```

## 5. Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência.

Exemplo:

```env
# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b | llama3.1:8b

# TaskFlow API
TASKFLOW_API_URL=chave_api_aqui
```

Ajuste os valores de acordo com seu ambiente.

- `OLLAMA_URL`: endereço do serviço Ollama.
- `OLLAMA_MODEL`: modelo instalado e compatível com Tool Calling.
- `TASKFLOW_API_URL`: endereço-base da API TaskFlow.

**Importante:** não compartilhe seu arquivo `.env` nem envie credenciais ou informações sensíveis para o repositório.

## 6. Integração com a TaskFlow API

O agente utiliza o backend Java para acessar as informações das tarefas.

A comunicação é realizada pelo módulo `api_client.py`, responsável por enviar requisições HTTP aos endpoints da API.

Exemplo de consulta:

```http
GET /api/tasks
```

O fluxo de integração funciona da seguinte maneira:

1. O usuário envia uma solicitação em linguagem natural.
2. O agente interpreta a intenção utilizando o modelo de linguagem.
3. O modelo seleciona uma ferramenta disponível.
4. A ferramenta executa uma requisição HTTP para a TaskFlow API.
5. O backend processa a solicitação e retorna os dados.
6. O agente utiliza o resultado para formular uma resposta.

O backend permanece responsável pelas regras de negócio, validações, autorização e persistência dos dados.

**Projeto relacionado:** [TaskFlow API — GitHub](https://github.com/Florido-hub/TaskFlow)

## 7. Estrutura do projeto

```text
Taskflow-Agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── tools.py
│   └── api_client.py
│
├── tests/
│
├── prompt.txt
├── .env
├── .env.example
├── .gitignore
└── requirements.txt
```

### Responsabilidade dos módulos

| Arquivo | Descrição |
|---|---|
| `main.py` | Ponto de entrada e interação com o usuário |
| `agent.py` | Configuração do modelo, prompt e agente LangChain |
| `tools.py` | Definição das ferramentas disponíveis para o agente |
| `api_client.py` | Comunicação HTTP com a TaskFlow API |
| `prompt.txt` | Instruções e comportamento do assistente |
| `tests/` | Testes automatizados do agente e de suas ferramentas |

## 8. Executando o projeto

Antes de iniciar o agente, certifique-se de que:

- O Ollama está instalado e em execução.
- O modelo configurado foi baixado.
- A TaskFlow API está disponível.
- As variáveis de ambiente estão configuradas.

Com o ambiente virtual ativado, execute a partir da raiz do projeto:

```bash
python -m app.main
```

O agente será iniciado no terminal e estará pronto para receber mensagens.

Exemplo de interação:

```text
TaskFlow Agent — provedor: Ollama | modelo: qwen2.5:7b

Digite sua pergunta (ou 'sair' para encerrar).

Você: Quais são minhas tarefas?

Bot: ...
```

Para encerrar:

```text
Você: sair
```

## Funcionalidades

O projeto está sendo desenvolvido para permitir a interação com o gerenciamento de tarefas por linguagem natural.

- [x] Integração com modelos locais utilizando Ollama.
- [x] Construção do agente com LangChain.
- [x] Estrutura para definição de ferramentas (*Tool Calling*).
- [x] Comunicação HTTP com a TaskFlow API.
- [ ] Consulta de tarefas por linguagem natural.
- [ ] Criação de tarefas por linguagem natural.
- [ ] Atualização e conclusão de tarefas.
- [ ] Memória conversacional.
- [ ] Disponibilização do agente por meio de uma API HTTP com FastAPI.
- [ ] Testes automatizados com Deepeval metrics
- [ ] Integração contínua.

*O status das funcionalidades deve ser atualizado conforme a implementação e os testes forem concluídos.*

## Segurança e arquitetura

O TaskFlow Agent foi projetado como um serviço independente do backend principal.

Alguns princípios importantes da integração:

- O agente não possui acesso direto ao banco de dados.
- As operações são realizadas por meio da API REST.
- A validação das regras de negócio permanece no backend Java.
- A autorização de acesso às tarefas deve ser garantida pelo backend, considerando o usuário autenticado.
- Credenciais e configurações sensíveis são mantidas em variáveis de ambiente.

## Licença

> Este projeto está em desenvolvimento como parte do ecossistema TaskFlow.
