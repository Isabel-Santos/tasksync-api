# 📋 TaskSync - API RESTful

+ Esta parte do repositório refere-se exclusivamente à **API RESTful** desenvolvida com **Flask**, incluindo autenticação com **JWT**, segurança avançada, e integração com banco de dados relacional (**PostgreSQL**) e não relacional (**MongoDB**).
ℹ️ O frontend React ainda está em desenvolvimento. Quando finalizado, terá repositório vinculado ou com link referenciado.

## 1. Requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados:

- Python 3.x
- Git para clonagem do repositório
- Flask + Flask-JWT-Extended
- PostgreSQL + SQLAlchemy
- MongoDB
- Authlib (Google OAuth)
- Flask-Limiter
- Flask-CORS, Flask-Caching
- mkcert (TLS local)

Caso ainda não tenha essas dependências instaladas:

- Baixe o Python
- Instale o Git
- PostgreSQL e MongoDB instalados e rodando localmente (ou usar conexões remotas)


## ⚙️ 2. Configuração do backend (Flask)

### 2.1 Clonar o repositório
```bash
git clone https://github.com/Isabel-Santos/tasksync-api.git
cd tasksync-api
```

### 2.2 Criar e ativar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

### 2.3 Instalar dependências do backend
```bash
pip install -r requirements.txt
```

### 2.4 Gerar certificados locais com mkcert
```bash
mkcert -install
mkcert localhost 127.0.0.1 ::1
```
Isso irá gerar arquivos como:
* localhost+2.pem
* localhost+2-key.pem

Coloque-os no mesmo diretório que run.py.

### 2.5 Configurando o Ambiente
Copie o arquivo `.env.example`, renomeie para `.env` e preencha com seus dados locais:
```bash
cp .env.example .env  # Linux/macOS
copy .env.example .env  # Windows
```

## 3. Executando o backend
Para rodar o servidor, execute o seguinte comando:
```bash
python run.py
```
Isso vai iniciar o servidor Flask e a API estará acessível via HTTPS em:
 * https://127.0.0.1:5000/ 
 * https://seu-ip-local:5000


## 🧪 4. Testando a API com Postman
Como o frontend ainda está em desenvolvimento, recomendamos usar o Postman para testar as rotas da API.
Depois de iniciar a API (backend):

#### 4.1 Importe as rotas manualmente ou use uma coleção do Postman (se disponível futuramente).

#### 4.2 Certifique-se de que o servidor está rodando com HTTPS (https://localhost:5000) e acesse o endereço.

#### 4.3 Nas requisições POST (ex: /auth/signup e /auth/login), envie dados no formato JSON:
```bash
{
  "username": "seuNome",
  "email": "seu@email.com",
  "password": "SenhaForte@123"
}
```
#### 4.4 Para rotas protegidas, inclua o token JWT retornado no login:
  * Vá na aba "Authorization"
  * Escolha o tipo "Bearer Token"
  * Cole o access_token
#### 4.5 Se estiver usando o Postman com HTTPS e mkcert, pode marcar a opção:
⚙️ Settings > SSL certificate verification: Off

### 📌 Exemplo de requisições:
* POST /auth/signup: Para cadastrar um usuário e gerar token
Body (JSON):
```bash
{
  "username": "novousuario",
  "email": "email@exemplo.com",
  "password": "SenhaForte@123"
}
```

* POST /auth/login – Para autenticar usuário
Body (JSON):
```bash
{
  "email": "email@exemplo.com",
  "password": "SenhaForte@123"
}
```
* ### Outros Endpoints
* GET /tasks – Lista tarefas (protegida com JWT)
* POST /tasks – Cria nova tarefa (protegida com JWT)

* ###  Para acessar rotas protegidas:
##### 1. Copie o access_token retornado no login
##### 2. Use o token de acesso no parâmetro **Authorization**
##### 3. Cole <*acess-token*> no campo Token
##### 4. Execute o teste em **Send**, por exemplo, a rota GET /auth/protected
  
  Authorization: Bearer <access_token>
⚠️ No Postman, desative a verificação SSL:
⚙️ Settings > General > SSL certificate verification → Off
Importante: A API possui limite de requisições por IP para evitar abuso (rate limiting).


## 🚀 5. Funcionalidades implementadas
### 🔐 5.1 Autenticação e Segurança
- ✅ Registro e login com validação de campos (e-mail, senha forte, username).
- ✅ Autenticação via **JWT** (com `access_token` e `refresh_token`).
- ✅ Criptografia de senhas com **bcrypt** (com verificação de migração automática de `werkzeug` para `bcrypt`).
- ✅ **Recuperação de senha** via token temporário (simulado com link).
- ✅ Suporte a login com **Google OAuth2** (em progresso).
- ✅ Proteção com **Rate Limiting** por IP (com `flask-limiter`):
  - Limite global (padrão: 100/dia, 25/hora)
  - Limite mais restritivo no login e no registro (p.ex., 5 requisições por minuto).
- ✅ Integração com PostgreSQL e MongoDB
- ✅ HTTPS configurado localmente com **certificados mkcert** (TLSv1.3 gerado via `mkcert`).
- ✅ Servidor de fallback em HTML estático (`/static/status.html`)
- ✅ Middleware de CORS ativo
- ✅ Modularização por blueprint e services
- ✅ Respostas padronizadas para erros e exceções.

### 5.2 📦 Backend
- API RESTful desenvolvida com **Flask**.
- Banco de dados **PostgreSQL** (SQLAlchemy ORM).
- Logs e auditoria com **MongoDB**.
- Armazenamento de sessão futuro com Redis (em progresso).
- Arquitetura modular: separação clara entre rotas, serviços, modelos, configurações e utilitários.

### 5.3 🧪 Validações (server-side)
- E-mail com regex.
- Username alfanumérico com mínimo de 3 caracteres.
- Senhas fortes com:
  - Letra maiúscula
  - Letra minúscula
  - Número
  - Caractere especial
  - Mínimo de 8 caracteres


## Estrutura Geral do Projeto
```arduino
projeto-tasksync/
│
├── server/                      # Diretório do Backend (Flask)
│   ├── app/
│   │   ├── __init__.py             # Inicializa a aplicação Flask
│   │   ├── config.py               # Configurações do Flask
│   │   ├── models/                 # Modelos do banco de dados
│   │   │   ├── __init__.py         # Inicializa o módulo de modelos
│   │   │   ├── user.py             # Modelo de Usuários
│   │   │   ├── task.py             # Modelo de tarefas
│   │   │   └── log.py              # Modelo de Logs de Alterações
│   │   ├── routes/                  # Rotas (endpoints) da API REST
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Rotas de autenticação
│   │   │   ├── user.py              # Rotas de usuários
│   │   │   ├── task.py              # Rotas de tarefas
│   │   │   └── log.py               # Rotas de logs
│   │   ├── services/                # Lógica de negócios (camada de serviços)
│   │   │   ├── __init__.py          # Inicializa o módulo de serviços
│   │   │   ├── auth_service.py      # Lógica de autenticação
│   │   │   ├── user_service.py      # Lógica relacionada a usuários
│   │   │   ├── task_service.py      # Lógica de tarefas
│   │   │   └── log_service.py       # Lógica de logs
│   │   ├── utils/                   # Utilitários e funções auxiliares
│   │   │   ├── __init__.py          # Inicializa o módulo de utilitários
│   │   │   ├── validators.py        # Validações de entrada de dados
│   │   │   └── jwt_helper.py        # Geração e validação de tokens JWT
│   │   ├── static/                  # elementos estáticos
│   │   │   └── status.html          # página de status do servidor
│   │   └── extensions.py            # Inicialização de extensões (e.g., SQLAlchemy, JWT)
│   ├── .env                       # Configurações do Flask
│   ├── requirements.txt           # Dependências do backend
│   └── run.py                     # Arquivo principal para iniciar o backend
│
│
├── Redis/ 
│
├── client/                        # Frontend React
├── requirements.txt               # Dependências do projeto (pip)
├── .env                           # Variáveis de ambiente(configuração segura)
├── .gitignore                     # Arquivos e pastas ignorados pelo Git
├── run.py                         # Arquivo principal para execução da aplicação
└── README.md                      # Documentação do projeto
```

## 📊 Status do Desenvolvimento
### ✅ Concluído até agora:
* Autenticação e cadastro com JWT
* Validações robustas de email, senha e campos
* Rate limiting com Flask-Limiter funcional
* Integração com banco relacional (PostgreSQL) e não relacional (MongoDB)
* Suporte HTTPS local com mkcert
* Página fallback para status em HTML
* API testável via Postman

## ✅ Status: Desenvolvimento Ativo
Sistema funcional com autenticação robusta e proteção de rotas. Pronto para testes em ambiente seguro.

## 🛡️ Em andamento
 - Armazenamento de sessões e limites com Redis
 - Compartilhamento de tarefas com permissões
 - Autenticação em duas etapas (2FA)
 - Sistema completo de auditoria de ações por usuário
 - Interface administrativa

## 🔜 Próximas etapas:
* Integração OAuth finalizada
* Painel administrativo
* Auditoria de ações
* Compartilhamento de tarefas por permissão
* Segurança com Redis como backend para rate limiting
* Implementação de Redis para armazenamento do rate limiting em produção
* Desenvolvimento do frontend React
* Integração completa frontend-backend

## 💡👩‍💻 Autora
Desenvolvido por Isabel Santos
