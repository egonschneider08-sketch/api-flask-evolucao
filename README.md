# 📚 API Flask Books (com PostgreSQL e Docker)

Uma API RESTful desenvolvida em **Python** utilizando **Flask**, **SQLAlchemy** e **Flask-Migrate**, conectada a um banco de dados relacional **PostgreSQL** em container **Docker**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask** (Framework web minimalista)
- **Flask-SQLAlchemy** (ORM para persistência de dados)
- **Flask-Migrate / Alembic** (Gerenciamento de migrações de banco)
- **PostgreSQL 16** (Banco de dados relacional com suporte nativo a UUID)
- **Docker & Docker Compose** (Containerização e orquestração do banco de dados)
- **psycopg (v3) / psycopg2-binary** (Drivers de conexão PostgreSQL)

---

## 📁 Estrutura do Projeto

```text
api-flask-evolucao/
├── migrations/             # Scripts de migração de banco (Flask-Migrate / Alembic)
│   ├── versions/           # Histórico de versões das migrations
│   ├── alembic.ini         # Configurações do Alembic
│   ├── env.py              # Contexto de execução das migrações
│   └── script.py.mako      # Template para novas revisões
├── models/
│   ├── __init__.py         # Exportador dos modelos da aplicação
│   └── book.py             # Modelo Book (espelho/módulo)
├── .env.example            # Modelo de variáveis de ambiente para versionamento
├── .gitignore              # Regras de exclusão do Git (ignora .venv, .env, __pycache__)
├── app.py                  # Ponto de entrada da API Flask e definição das rotas
├── book.py                 # Modelo da tabela 'books' com identificador UUID
├── db.py                   # Instância compartilhada do SQLAlchemy (db)
├── docker-compose.yml      # Configuração do serviço PostgreSQL no Docker
├── postman_collection.json # Coleção pronta para importação no Postman
├── README.md               # Documentação completa do projeto
└── requirements.txt        # Dependências do projeto Python
```

---

## 🛠️ Passo a Passo para Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/egonschneider08-sketch/api-flask-evolucao.git
cd api-flask-evolucao
```

### 2. Criar e Ativar o Ambiente Virtual (`.venv`)

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Copie o arquivo de exemplo `.env.example` para `.env`:

**No Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**No Linux / macOS:**
```bash
cp .env.example .env
```

> O arquivo `.env` já vem configurado por padrão com:
> ```env
> DATABASE_URL=postgresql://postgres:postgres@localhost:5432/books_db
> FLASK_APP=app.py
> FLASK_DEBUG=1
> ```

### 5. Iniciar o Banco de Dados PostgreSQL no Docker
Certifique-se de que o **Docker Desktop** esteja aberto e execute:

```bash
docker compose up -d
```

Para conferir se o container está saudável:
```bash
docker ps
```
*(Você verá o container `postgres_books` ativo na porta `5432`).*

### 6. Executar a Aplicação Flask
Com o banco rodando, inicie o servidor:

```bash
python app.py
```

A API estará disponível em: **`http://127.0.0.1:5000`**

---

## 📌 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Retorna o status da API |
| `GET` | `/books` | Lista todos os livros cadastrados |
| `GET` | `/books/<id>` | Busca um livro específico pelo seu UUID |
| `POST` | `/books` | Cadastra um novo livro |
| `PUT` | `/books/<id>` | Atualiza os dados de um livro |
| `DELETE` | `/books/<id>` | Remove um livro do banco de dados |

---

## 📬 Como Utilizar com o Postman

Você pode testar a API no **Postman** de duas formas: importando a coleção pronta com um clique ou configurando cada rota manualmente.

### Método 1: Importando a Coleção Pronta (Recomendado)

O projeto inclui o arquivo [`postman_collection.json`](postman_collection.json) com todas as rotas e exemplos configurados:

1. Abra o **Postman**.
2. No canto superior esquerdo, clique no botão **Import**.
3. Arraste ou selecione o arquivo **`postman_collection.json`** localizado na raiz deste projeto.
4. Clique em **Import**.
5. Uma pasta chamada **`API Flask Books`** aparecerá na aba *Collections* com todas as requisições prontas!

---

### Método 2: Criando as Requisições Manualmente no Postman

Certifique-se de que o servidor Flask está rodando (`python app.py`).

#### 1. Verificar Status da API (GET)
- **Método**: `GET`
- **URL**: `http://127.0.0.1:5000/`
- Clique em **Send**.
- **Resposta esperada (`200 OK`)**:
  ```json
  {
    "message": "API Flask Books conectada ao PostgreSQL",
    "status": "online"
  }
  ```

---

#### 2. Cadastrar um Livro (POST)
- **Método**: `POST`
- **URL**: `http://127.0.0.1:5000/books`
- Clique na aba **Headers** e verifique se contém:
  - `Content-Type`: `application/json`
- Clique na aba **Body**, selecione a opção **raw** e mude o formato para **JSON**.
- Insira o seguinte payload:
  ```json
  {
    "title": "O Programador Pragmático",
    "author": "Andy Hunt & Dave Thomas",
    "description": "Um dos livros mais influentes sobre desenvolvimento de software profissional.",
    "is_finished": false
  }
  ```
- Clique em **Send**.
- **Resposta esperada (`201 Created`)**:
  ```json
  {
    "id": "e4b2d5a1-7c98-4c8d-93d3-1a2f3b4c5d6e",
    "title": "O Programador Pragmático",
    "author": "Andy Hunt & Dave Thomas",
    "description": "Um dos livros mais influentes sobre desenvolvimento de software profissional.",
    "is_finished": false,
    "created_at": "2026-10-20T21:20:00.000000"
  }
  ```
> 💡 **Dica**: Copie o valor do `"id"` retornado na resposta para usar nas rotas seguintes.

---

#### 3. Listar Todos os Livros (GET)
- **Método**: `GET`
- **URL**: `http://127.0.0.1:5000/books`
- Clique em **Send**.
- **Resposta esperada (`200 OK`)**:
  ```json
  [
    {
      "id": "e4b2d5a1-7c98-4c8d-93d3-1a2f3b4c5d6e",
      "title": "O Programador Pragmático",
      "author": "Andy Hunt & Dave Thomas",
      "description": "Um dos livros mais influentes sobre desenvolvimento de software profissional.",
      "is_finished": false,
      "created_at": "2026-10-20T21:20:00.000000"
    }
  ]
  ```

---

#### 4. Consultar Livro por ID (GET)
- **Método**: `GET`
- **URL**: `http://127.0.0.1:5000/books/SEU_UUID_AQUI`
  *(ex: `http://127.0.0.1:5000/books/e4b2d5a1-7c98-4c8d-93d3-1a2f3b4c5d6e`)*
- Clique em **Send**.
- **Resposta esperada (`200 OK`)**.

---

#### 5. Atualizar Dados de um Livro (PUT)
- **Método**: `PUT`
- **URL**: `http://127.0.0.1:5000/books/SEU_UUID_AQUI`
- Na aba **Body** -> **raw** -> **JSON**, insira os dados alterados:
  ```json
  {
    "title": "O Programador Pragmático (Edição Especial)",
    "author": "Andy Hunt & Dave Thomas",
    "description": "Edição de 20 anos com conteúdos atualizados.",
    "is_finished": true
  }
  ```
- Clique em **Send**.
- **Resposta esperada (`200 OK`)**.

---

#### 6. Deletar um Livro (DELETE)
- **Método**: `DELETE`
- **URL**: `http://127.0.0.1:5000/books/SEU_UUID_AQUI`
- Clique em **Send**.
- **Resposta esperada (`200 OK`)**:
  ```json
  {
    "message": "Livro removido com sucesso"
  }
  ```

---

## 🗄️ Comandos Úteis do Docker

- **Verificar status do PostgreSQL**:
  ```bash
  docker ps
  ```

- **Ver logs do banco de dados**:
  ```bash
  docker logs -f postgres_books
  ```

- **Acessar o terminal interativo do PostgreSQL (`psql`)**:
  ```bash
  docker exec -it postgres_books psql -U postgres -d books_db
  ```
  *(Dentro do psql: `\dt` lista tabelas e `\q` sai).*

- **Parar o banco de dados**:
  ```bash
  docker compose down
  ```

- **Reiniciar o banco de dados**:
  ```bash
  docker compose up -d
  ```
