# 📋 TaskSync - API RESTful

+ Esta parte do repositório refere-se exclusivamente à **API RESTful** desenvolvida com **Flask**, incluindo autenticação com **JWT**, segurança avançada, e integração com banco de dados relacional (**PostgreSQL**) e não relacional (**MongoDB**).
ℹ️ O frontend React ainda está em desenvolvimento. Quando finalizado, terá repositório vinculado ou com link referenciado.
O vídeo demonstrando as funcionalidades estão no arquivo [Apresentação_SI_1x75_Compactado.mp4](https://github.com/Isabel-Santos/tasksync-api/blob/main/Apresenta%C3%A7%C3%A3o_SI_1x75_Compactado.mp4)

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

#### 4.1 Login em Duas Etapas
1. Requisição POST para /auth/login:
 * Envie o email e a senha do usuário. A API retornará uma mensagem de sucesso indicando que um código 2FA foi enviado.
2. Requisição POST para /auth/verify-2fa:
* Envie o email e o `two_factor_code` que você recebeu. Se o código estiver correto, a API retornará o access_token e o refresh_token.

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
  * Cole o access_token no campo Token
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
  * Onde: app/routes/auth.py, app/services/auth_service.py, app/utils/validators.py.
  * Como: Rotas recebem os dados, que são processados pelo AuthService. As validações em validators.py garantem a integridade e força dos dados de entrada (email, username, senha).
- ✅ Autenticação de Dois Fatores (2FA)
  * Onde: app/routes/auth.py (rotas /login e /verify-2fa), app/models/user.py.
  * Como: Após o login com credenciais válidas, um código é gerado, salvo no modelo do usuário (twofa_code) e enviado por e-mail. A rota /verify-2fa confirma esse código para então liberar os tokens de acesso.
- ✅ Autenticação via **JWT** (com `access_token` e `refresh_token`).
  * Onde: app/services/auth_service.py, app/utils/jwt_helper.py.
  * Como: Após a verificação 2FA, access_token e refresh_token são gerados. Rotas protegidas usam o decorador @jwt_required para exigir um access_token válido.
- ✅ Criptografia de senhas com **bcrypt** (com verificação de migração automática de `werkzeug` para `bcrypt`).
  * Onde: app/models/user.py.
  * Como: Os métodos set_password e check_password no modelo User usam bcrypt para gerar o hash e verificar a senha, respectivamente.
- ✅ **Recuperação de senha** segura.
  * Onde: app/routes/auth.py, app/services/auth_service.py.
  * Como: Gera um token seguro e com tempo de expiração que é enviado ao usuário por e-mail para permitir a redefinição da senha.
- ✅ Suporte a login com **Google OAuth2** (em progresso).
  * Onde: app/routes/auth.py.
  * Como: Usa a biblioteca Authlib para o fluxo de autenticação com o Google.
- ✅ Proteção com **Rate Limiting** por IP (com `flask-limiter`):
  - Limite global (padrão: 100/dia, 25/hora)
  - Limite mais restritivo no login e no registro (p.ex., 5 requisições por minuto).
  * Onde: app/__init__.py e app/extensions.py.
  * Como: Flask-Limiter é inicializado e configurado para aplicar limites de requisições globais e específicos para rotas sensíveis como login.
- ✅ Integração com PostgreSQL e MongoDB
- ✅ HTTPS configurado localmente com **certificados mkcert** (TLSv1.3 gerado via `mkcert`).
- ✅ Middleware de CORS ativo
- ✅ Modularização por blueprint e services
- ✅ Respostas padronizadas para erros e exceções.

### 5.2 📦 Backend e Lógica de Negócio
- API RESTful desenvolvida com **Flask**.
- ✅ Arquitetura Modular
  * Onde: Estrutura de diretórios do projeto.
  * Como: O código é organizado em Blueprints (app/routes), separando a lógica de negócio (app/services) e a camada de dados (app/models) para facilitar a manutenção.
- Banco de dados **PostgreSQL** (SQLAlchemy ORM) e Logs e auditoria com **MongoDB**.
- ✅ Integração com Bancos de Dados
  * PostgreSQL: Usado com o ORM SQLAlchemy para dados estruturados como usuários e tarefas (app/models/).
  * MongoDB: Usado para armazenar logs de auditoria de forma flexível (app/models/log.py).
- Armazenamento de sessão futuro com Redis (em progresso).
- ✅ Cache para Otimização de Performance
  * Onde: app/services/task_service.py, app/extensions.py.
  * Como: Flask-Caching é usado para cachear os resultados das consultas de tarefas. O serviço de tarefas (TaskService) verifica primeiro se os dados estão em cache antes de consultar o banco de dados.
- Arquitetura modular: separação clara entre rotas, serviços, modelos, configurações e utilitários.
- ✅ Compartilhamento de Tarefas com Permissões
  * Onde: app/routes/task_share.py, app/services/task_share_service.py, app/models/task_share.py.
  * Como: Um usuário pode compartilhar uma tarefa com outro, definindo permissões de 'view' ou 'edit'. O TaskShareService gerencia essa lógica, que é persistida no modelo TaskShare.

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
tasksync-api/
├── app/
│   ├── __init__.py             # Inicializa a aplicação Flask e suas extensões
│   ├── config.py               # Configurações da aplicação
│   ├── extensions.py           # Inicialização de extensões (SQLAlchemy, JWT, etc.)
│   ├── models/                 # Modelos do banco de dados (SQLAlchemy e Mongo)
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── task_share.py
│   │   ├── two_factor.py
│   │   └── log.py
│   ├── routes/                 # Rotas (endpoints) da API
│   │   ├── auth.py
│   │   ├── log.py
│   │   ├── task.py
│   │   ├── task_share.py
│   │   └── user.py
│   ├── services/               # Lógica de negócios (camada de serviços)
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   ├── log_service.py
│   │   ├── task_service.py
│   │   ├── task_share_service.py
│   │   └── user_service.py
│   └── utils/                  # Utilitários e funções auxiliares
│       ├── validators.py
│       └── jwt_helper.py
├── .env.example                # Arquivo de exemplo para variáveis de ambiente
├── requirements.txt            # Dependências do backend
└── run.py                      # Arquivo principal para iniciar o servidor│   │   ├── task.py
│   │   ├── task_share.py
│   │   └── log.py
│   ├── routes/                 # Rotas (endpoints) da API
│   │   ├── auth.py
│   │   ├── task.py
│   │   ├── task_share.py
│   │   └── user.py
│   ├── services/               # Lógica de negócios (camada de serviços)
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── task_share_service.py
│   │   └── user_service.py
│   └── utils/                  # Utilitários e funções auxiliares
│       ├── validators.py
│       └── jwt_helper.py
├── .env.example                # Arquivo de exemplo para variáveis de ambiente
├── requirements.txt            # Dependências do backend
└── run.py                      # Arquivo principal para iniciar o servidor
```

## 📊 Status do Desenvolvimento
### ✅ Concluído até agora:
* Autenticação completa com JWT e 2FA via e-mail.
* Validações robustas de email, senha e campos
* Rate limiting com Flask-Limiter funcional
* Integração com banco relacional (PostgreSQL) e não relacional (MongoDB)
* Suporte HTTPS local com mkcert
* Funcionalidade de compartilhamento de tarefas com permissões.
* Cache para otimização de consultas de tarefas.
* API testável via Postman

## 🛡️ Em andamento
 - Armazenamento de sessões e limites com Redis
 - Finalização da integração com Google OAuth.
 - Sistema completo de auditoria de ações por usuário
 - Interface administrativa

## 🔜 Próximas etapas:
* Painel administrativo
* Auditoria de ações
* Segurança com Redis como backend para rate limiting
* Implementação de Redis para armazenamento do rate limiting em produção
* Desenvolvimento do frontend React
* Integração completa frontend-backend

### Nota do Projeto
Esta é a API RESTful do projeto TaskSync, desenvolvida em Flask.
- 🔗 A interface de frontend (React) que consome esta API pode ser encontrada em: [[link-para-o-repositorio-da-interface](https://github.com/Isabel-Santos/tasksync-interface.git
)]
- ▶️ Um vídeo de demonstração da aplicação completa está disponível no README do repositório do frontend.

## 💡👩‍💻 Autora
Desenvolvido por Isabel Santos
