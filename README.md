# 📺 AnimeList - Sistema de Gerenciamento de Animes

## 📋 Sobre o Projeto

O **AnimeList** é uma aplicação web desenvolvida com **Flask** e **PostgreSQL** que permite aos usuários organizar e gerenciar uma lista de animes de forma simples e prática.

### ✨ Funcionalidades Principais

- 🔐 **Autenticação de usuários** (login/cadastro)
- 📝 **Organizar animes nas categorias:**
  - Assistindo
  - Concluídos
  - Favoritos
- 👤 **Controlar seu perfil** dentro do sistema
- 👨‍💼 **Área administrativa** onde usuários admin podem:
  - Visualizar todos os usuários cadastrados
  - Editar dados dos usuários (exceto CPF)
  - Excluir usuários do sistema

---

## 🏗️ 1. Arquitetura do Projeto

O projeto segue o padrão **MVC (Model-View-Controller)** com camadas adicionais para melhor organização:

```
AnimeList/
│
├── controller/          # Controladores (rotas Flask)
│   ├── usuario_controller.py
│   └── anime_controller.py
│
├── service/            # Camada de negócio
│   ├── usuario_service.py
│   └── anime_service.py
│
├── repository/         # Camada de acesso ao banco
│   ├── usuario_repository.py
│   └── anime_repository.py
│
├── model/             # Modelos de dados
│   ├── usuario.py
│   └── anime.py
│
├── templates/         # Views HTML
│   ├── login.html
│   ├── painel.html
│   └── ...
│
├── static/           # CSS, JS, imagens
│   ├── css/
│   ├── js/
│   └── images/
│
├── utils/            # Utilitários
│   └── api_utils.py
│
├── db.py            # Conexão com banco de dados
└── app.py           # Aplicação principal
```

### 📐 Padrão Arquitetural

**Controller → Service → Repository → Database**

- **Controller**: Recebe requisições HTTP e retorna respostas
- **Service**: Contém a lógica de negócio e validações
- **Repository**: Faz acesso direto ao banco de dados
- **Model**: Define a estrutura dos dados

---

## 🔐 2. Autenticação

### Sistema de Login e Sessão

```python
# usuario_controller.py - Login
@usuario_bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    senha = request.form.get("senha")
    
    # Autentica usando bcrypt
    usuario = UsuarioService.autenticar(email, senha)
    
    if usuario:
        # Cria sessão
        session["id_usuario"] = usuario["id"]
        session["nome"] = usuario["nome"]
        session["perfil"] = usuario["perfil"]
        
        return redirect(url_for("usuario.painel"))
```

### Verificação de Senha com bcrypt

```python
# usuario_service.py
def autenticar(email, senha):
    usuario = UsuarioRepository.buscar_por_email(email)
    
    # Compara senha hash
    senha_valida = bcrypt.checkpw(
        senha.encode("utf-8"),
        usuario["senha"].encode("utf-8")
    )
    
    return usuario if senha_valida else None
```

---

## 🔒 5. Armazenamento Seguro de Senha

### Hash de Senha com bcrypt

```python
# usuario_service.py - Cadastro
def cadastrar(dados):
    # Gera hash da senha
    senha_hash = bcrypt.hashpw(
        dados["senha"].encode("utf-8"),
        bcrypt.gensalt()
    )
    dados["senha"] = senha_hash.decode("utf-8")
    
    # Salva no banco
    usuario = Usuario(**dados)
    return UsuarioRepository.adicionar(usuario)
```

**Por que bcrypt?**
- ✅ Algoritmo de hash seguro
- ✅ Salt automático (proteção contra rainbow tables)
- ✅ Custo computacional ajustável
- ✅ Não armazena senha em texto puro

---

## 🛡️ 6. Proteção de Rotas

### Decoradores de Proteção

```python
# utils/api_utils.py

# Verifica se usuário está logado
@requer_autenticacao
def rota_protegida():
    # Somente usuários logados podem acessar
    pass

# Verifica se é administrador
@requer_admin
def rota_admin():
    # Somente admins podem acessar
    pass
```

### Implementação dos Decoradores

```python
def requer_autenticacao(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            if request.is_json:
                return resposta_padrao(False, "Autenticação necessária", codigo=401)
            return redirect(url_for("usuario.login_get"))
        return funcao(*args, **kwargs)
    return wrapper

def requer_admin(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if session.get("perfil") != "admin":
            return resposta_padrao(False, "Acesso negado", codigo=403)
        return funcao(*args, **kwargs)
    return wrapper
```

---

## ✏️ 3. Operações CRUD

### Usuários

| Operação | Método | Rota | Descrição |
|----------|--------|------|-----------|
| Create | POST | `/cadastro-usuario` | Cadastra novo usuário |
| Read | GET | `/usuarios` | Lista todos (admin) |
| Update | PUT | `/usuarios/<id>` | Atualiza usuário |
| Delete | DELETE | `/usuarios/<id>` | Remove usuário |

### Animes

| Operação | Método | Rota | Descrição |
|----------|--------|------|-----------|
| Create | POST | `/animes` | Adiciona anime |
| Read | GET | `/animes` | Lista animes do usuário |
| Update | PUT | `/animes/<id>` | Atualiza anime |
| Delete | DELETE | `/animes/<id>` | Remove anime |

### Exemplo CRUD Completo (Animes)

```python
# CREATE - anime_controller.py
@anime_bp.route("/animes", methods=["POST"])
@requer_autenticacao
def criar_anime():
    dados = request.get_json()
    dados["usuario_id"] = session.get("id_usuario")
    AnimeService.criar(dados)
    return resposta_padrao(True, "Anime criado!", codigo=201)

# READ
@anime_bp.route("/animes", methods=["GET"])
@requer_autenticacao
def listar_animes():
    usuario_id = session.get("id_usuario")
    status = request.args.get("status")  # Filtro opcional
    animes = AnimeService.listar(usuario_id, status)
    return resposta_padrao(True, "Listado", dados={"animes": animes})

# UPDATE
@anime_bp.route("/animes/<int:id>", methods=["PUT"])
@requer_autenticacao
def atualizar_anime(id):
    # Verifica permissão
    anime = AnimeService.buscar_por_id(id)
    if anime["usuario_id"] != session.get("id_usuario"):
        return resposta_padrao(False, "Acesso negado", codigo=403)
    
    dados = request.get_json()
    AnimeService.atualizar(id, dados)
    return resposta_padrao(True, "Atualizado")

# DELETE
@anime_bp.route("/animes/<int:id>", methods=["DELETE"])
@requer_autenticacao
def deletar_anime(id):
    # Verifica permissão
    anime = AnimeService.buscar_por_id(id)
    if anime["usuario_id"] != session.get("id_usuario"):
        return resposta_padrao(False, "Acesso negado", codigo=403)
    
    AnimeService.deletar(id)
    return resposta_padrao(True, "Removido")
```

---

## 🎨 4. Frontend (HTML + CSS)

### Estrutura HTML

```html
<!-- templates/login.html -->
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/login.css') }}">
</head>
<body>
    <form method="POST" action="/login">
        <input type="email" name="email" required>
        <input type="password" name="senha" required>
        <button type="submit">Entrar</button>
    </form>
</body>
</html>
```

### Estilização CSS

```css
/* static/css/style.css */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.anime-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px;
}
```

### JavaScript para Interatividade

```javascript
// static/js/animes.js
async function marcarEpisodio(animeId) {
    const response = await fetch(`/animes/${animeId}/proximo-episodio`, {
        method: 'POST'
    });
    const data = await response.json();
    alert(data.mensagem);
}
```

---

## 🗄️ 9. Modelo Lógico do Banco de Dados

### Entidades e Relacionamentos

```
┌─────────────────┐         ┌─────────────────┐
│    USUÁRIOS     │         │     ANIMES      │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │─────┐   │ id (PK)         │
│ nome            │     │   │ usuario_id (FK) │
│ cpf (UNIQUE)    │     └──>│ nome            │
│ email (UNIQUE)  │         │ descricao       │
│ idade           │         │ status          │
│ senha           │         │ eps_assistidos  │
│ perfil          │         │ total_eps       │
└─────────────────┘         │ imagem          │
                            └─────────────────┘

Relacionamento: 1 USUÁRIO possui N ANIMES (1:N)
```

---

## 🛠️ 10. Modelo Físico do Banco de Dados

### Tabela: usuarios

```sql
CREATE TABLE usuarios (
    id VARCHAR(36) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    idade INT NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil VARCHAR(10) DEFAULT 'user' CHECK (perfil IN ('user', 'admin'))
);
```

### Tabela: animes

```sql
CREATE TABLE animes (
    id SERIAL PRIMARY KEY,
    usuario_id VARCHAR(36) NOT NULL,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    status VARCHAR(20) DEFAULT 'assistindo' CHECK (status IN ('assistindo', 'concluido', 'favorito')),
    eps_assistidos INT DEFAULT 0,
    total_eps INT DEFAULT 0,
    imagem VARCHAR(500),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

### Índices para Performance

```sql
-- Índice para buscar animes por usuário
CREATE INDEX idx_animes_usuario ON animes(usuario_id);

-- Índice para filtrar por status
CREATE INDEX idx_animes_status ON animes(status);

-- Índice para buscar por email
CREATE INDEX idx_usuarios_email ON usuarios(email);
```

---

## 📊 11. Normalização de Dados

### Formas Normais Aplicadas

#### ✅ 1ª Forma Normal (1FN)
- Todos os atributos são atômicos (não há listas ou arrays)
- Cada coluna contém apenas um valor
- Exemplo: `status` = 'assistindo' (não 'assistindo, favorito')

#### ✅ 2ª Forma Normal (2FN)
- Está na 1FN
- Não há dependências parciais (todos os atributos dependem da chave completa)
- Tabelas separadas: `usuarios` e `animes`

#### ✅ 3ª Forma Normal (3FN)
- Está na 2FN
- Não há dependências transitivas
- Exemplo: `nome` do anime não depende de `usuario_id`, mas sim de `id` do anime

### Análise de Normalização

**Tabela usuarios:**
```
Dependência funcional: id → nome, cpf, email, idade, senha, perfil
✅ Todos os atributos dependem diretamente da chave primária
```

**Tabela animes:**
```
Dependência funcional: id → usuario_id, nome, descricao, status, eps_assistidos, total_eps, imagem
✅ Todos os atributos dependem diretamente da chave primária
```

---

## 📡 14. API RESTful

### Princípios REST Aplicados

#### 1️⃣ **Recursos Identificados por URIs**
```
/usuarios          → Coleção de usuários
/usuarios/{id}     → Usuário específico
/animes            → Coleção de animes
/animes/{id}       → Anime específico
```

#### 2️⃣ **Métodos HTTP Corretos**
```
GET    /animes           → Listar (Safe & Idempotent)
POST   /animes           → Criar (Não idempotent)
PUT    /animes/{id}      → Atualizar completo (Idempotent)
DELETE /animes/{id}      → Remover (Idempotent)
```

#### 3️⃣ **Códigos de Status HTTP**
```python
200 OK              → Sucesso geral
201 Created         → Recurso criado
400 Bad Request     → Dados inválidos
401 Unauthorized    → Não autenticado
403 Forbidden       → Sem permissão
404 Not Found       → Recurso não existe
```

#### 4️⃣ **Stateless (Sem Estado)**
- Cada requisição contém todas as informações necessárias
- Session é usada apenas para autenticação
- Não há estado de conversação no servidor

#### 5️⃣ **Representação JSON**
```json
{
    "sucesso": true,
    "mensagem": "Anime criado com sucesso",
    "dados": {
        "anime": {
            "id": 1,
            "nome": "One Piece",
            "status": "assistindo"
        }
    }
}
```

### Exemplos de Endpoints RESTful

```python
# Listar com filtro (Query Parameters)
GET /animes?status=assistindo

# Buscar específico
GET /animes/1

# Criar novo
POST /animes
Body: {"nome": "Naruto", "total_eps": 220}

# Atualizar
PUT /animes/1
Body: {"status": "concluido"}

# Deletar
DELETE /animes/1
```

---

## 📚 12. Documentação da API com Postman

### Collection: AnimeList API

#### 🔐 Autenticação

**1. Login**
```http
POST http://localhost:5000/login
Content-Type: application/json

{
    "email": "usuario@email.com",
    "senha": "senha123"
}

Response 200:
{
    "sucesso": true,
    "mensagem": "Bem-vindo(a), João!",
    "dados": {
        "usuario": {
            "id": "uuid-123",
            "nome": "João",
            "perfil": "user"
        }
    }
}
```

**2. Cadastro**
```http
POST http://localhost:5000/cadastro-usuario
Content-Type: application/json

{
    "nome": "João Silva",
    "cpf": "12345678900",
    "email": "joao@email.com",
    "idade": 25,
    "senha": "senha123",
    "perfil": "user"
}

Response 201:
{
    "sucesso": true,
    "mensagem": "Cadastro realizado com sucesso!"
}
```

#### 📺 Animes

**3. Listar Animes**
```http
GET http://localhost:5000/animes
Authorization: Session Cookie

Response 200:
{
    "sucesso": true,
    "mensagem": "Animes listados com sucesso",
    "dados": {
        "animes": [
            {
                "id": 1,
                "nome": "One Piece",
                "status": "assistindo",
                "eps_assistidos": 50,
                "total_eps": 1000
            }
        ],
        "total": 1
    }
}
```

**4. Criar Anime**
```http
POST http://localhost:5000/animes
Content-Type: application/json

{
    "nome": "Naruto",
    "descricao": "História de um ninja",
    "status": "assistindo",
    "total_eps": 220,
    "imagem": "url_da_imagem"
}

Response 201:
{
    "sucesso": true,
    "mensagem": "Anime criado com sucesso!"
}
```

**5. Atualizar Anime**
```http
PUT http://localhost:5000/animes/1
Content-Type: application/json

{
    "status": "concluido",
    "eps_assistidos": 220
}

Response 200:
{
    "sucesso": true,
    "mensagem": "Anime atualizado com sucesso"
}
```

**6. Deletar Anime**
```http
DELETE http://localhost:5000/animes/1

Response 200:
{
    "sucesso": true,
    "mensagem": "Anime removido com sucesso"
}
```

**7. Estatísticas**
```http
GET http://localhost:5000/animes/estatisticas

Response 200:
{
    "sucesso": true,
    "mensagem": "Estatísticas calculadas",
    "dados": {
        "estatisticas": {
            "total_animes": 10,
            "assistindo": 3,
            "concluidos": 5,
            "favoritos": 2,
            "total_episodios_assistidos": 450
        }
    }
}
```

---

## ⚠️ 13. Tratamento de Erros nas Rotas

### Decorator de Tratamento de Erros

```python
# utils/api_utils.py
def api_error_handler(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        
        except ValueError as e:
            # Erros de validação
            return resposta_padrao(False, str(e), codigo=400)
        
        except KeyError as e:
            # Campos obrigatórios ausentes
            return resposta_padrao(
                False, 
                f"Campo obrigatório ausente: {str(e)}", 
                codigo=400
            )
        
        except Exception as e:
            # Erros inesperados
            print(f"Erro inesperado: {e}")
            return resposta_padrao(
                False, 
                "Erro interno do servidor", 
                codigo=500
            )
    
    return wrapper
```

### Aplicação nas Rotas

```python
@anime_bp.route("/animes", methods=["POST"])
@requer_autenticacao
@api_error_handler  # ← Captura todos os erros
def criar_anime():
    dados = request.get_json()
    
    # Se não enviar dados, gera ValueError
    if not dados:
        raise ValueError("Nenhum dado fornecido")
    
    # Se faltar campo, gera KeyError ou ValueError
    if not dados.get("nome"):
        raise ValueError("Campo 'nome' é obrigatório")
    
    # Service pode lançar exceções
    AnimeService.criar(dados)
    
    return resposta_padrao(True, "Criado!", codigo=201)
```

### Tipos de Erros Tratados

| Erro | Código | Descrição |
|------|--------|-----------|
| `ValueError` | 400 | Dados inválidos |
| `KeyError` | 400 | Campo obrigatório ausente |
| `Exception` | 500 | Erro interno |
| Autenticação | 401 | Não logado |
| Permissão | 403 | Sem acesso |
| Não encontrado | 404 | Recurso inexistente |

---

## 🌐 7. Deploy

### Deploy realizado no Render

O projeto foi implantado no **Render**, uma plataforma moderna de deploy que oferece:
- ✅ Deploy gratuito
- ✅ PostgreSQL gerenciado
- ✅ SSL automático (HTTPS)
- ✅ Deploy automático via Git
- ✅ Logs em tempo real

### Arquivos de Configuração

**requirements.txt:**
```
Flask==3.0.0
psycopg2-binary==2.9.9
bcrypt==4.1.2
gunicorn==21.2.0
```

**Procfile ou Build Command:**
```bash
# Build Command no Render
pip install -r requirements.txt

# Start Command no Render
gunicorn app:app
```

### Configuração no Render

**1. Web Service:**
- Environment: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Instance Type: Free

**2. PostgreSQL Database:**
- Criado automaticamente no Render
- Conexão via variável de ambiente `DATABASE_URL`

**3. Variáveis de Ambiente:**
```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=sua_chave_secreta_aqui
FLASK_ENV=production
```

### Conexão com PostgreSQL no Render

```python
# db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    # Render fornece DATABASE_URL automaticamente
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Produção (Render)
        return psycopg2.connect(database_url, cursor_factory=RealDictCursor)
    else:
        # Desenvolvimento (Local)
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "animelist"),
            cursor_factory=RealDictCursor
        )
```

### Vantagens do Render

1. **Deploy Automático** - Conecta com GitHub/GitLab
2. **PostgreSQL Gratuito** - Banco gerenciado sem configuração
3. **SSL/HTTPS** - Certificado automático
4. **Zero Downtime** - Deploy sem parar a aplicação
5. **Logs Integrados** - Monitoramento fácil
6. **Fácil Configuração** - Interface intuitiva

### URL da Aplicação

Após o deploy, a aplicação fica disponível em:
```
https://seu-projeto.onrender.com
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **Flask** - Framework web
- **PostgreSQL** - Banco de dados relacional
- **psycopg2** - Driver PostgreSQL para Python
- **bcrypt** - Hash de senhas
- **HTML/CSS** - Frontend
- **JavaScript** - Interatividade

---

## 📦 Como Executar o Projeto

### 1. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 2. Configure o banco de dados:
```sql
CREATE DATABASE animelist;
USE animelist;
-- Execute os scripts SQL das tabelas
```

### 3. Execute a aplicação:
```bash
python app.py
```

### 4. Acesse no navegador:
```
http://127.0.0.1:5000
```

---

## 👨‍💻 Autor

Desenvolvido como projeto acadêmico para demonstrar conhecimentos em:
- Arquitetura de software
- Desenvolvimento web full-stack
- Segurança da informação
- Boas práticas de programação

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais.