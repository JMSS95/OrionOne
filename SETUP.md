# Setup Rápido - OrionOne

## Pré-requisitos (Instalar num PC Novo)

### Software Obrigatório

| Software           | Versão Mínima | Link Download                                                 | Propósito                         |
| ------------------ | ------------- | ------------------------------------------------------------- | --------------------------------- |
| **Git**            | 2.40+         | [git-scm.com](https://git-scm.com/)                           | Controlo de versão                |
| **Docker Desktop** | 4.25+         | [docker.com](https://www.docker.com/products/docker-desktop/) | Containers (Laravel + PostgreSQL) |
| **Node.js**        | 20.x LTS      | [nodejs.org](https://nodejs.org/)                             | Frontend (Vue.js + Vite)          |
| **Composer**       | 2.6+          | [getcomposer.org](https://getcomposer.org/)                   | Dependências PHP                  |

### Software Opcional (Recomendado)

| Software                   | Propósito                          |
| -------------------------- | ---------------------------------- |
| **Visual Studio Code**     | IDE recomendado                    |
| **Postman**                | Testar API endpoints               |
| **pgAdmin** ou **DBeaver** | Cliente PostgreSQL (visualizar DB) |

### Extensões VS Code Recomendadas

```json
{
    "recommendations": [
        "bmewburn.vscode-intelephense-client",
        "bradlc.vscode-tailwindcss",
        "vue.volar",
        "editorconfig.editorconfig",
        "ms-azuretools.vscode-docker",
        "esbenp.prettier-vscode"
    ]
}
```

---

## Setup Inicial (Primeira Vez)

### 1. Clonar Repositório

```bash
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne
```

### 2. Configurar Ambiente

```bash
# Copiar ficheiro de ambiente
cp .env.example .env

# Editar .env se necessário (portas, credenciais, etc)
```

### 3. Iniciar Docker

```bash
# Iniciar containers (Laravel + PostgreSQL + Redis)
docker-compose up -d

# Verificar se containers estão a correr
docker-compose ps
```

### 4. Instalar Dependências

```bash
# Backend (PHP/Laravel)
docker-compose exec orionone-app composer install

# Frontend (Node/Vue)
docker-compose exec orionone-frontend npm install --legacy-peer-deps
```

### 5. Configurar Laravel

```bash
# Gerar chave da aplicação
docker-compose exec orionone-app php artisan key:generate

# Criar base de dados de testes (se não existir)
docker-compose exec orionone-db psql -U laravel -d postgres -c "CREATE DATABASE orionone_test;"

# Executar migrations + seeders
docker-compose exec orionone-app php artisan migrate:fresh --seed
```

### 6. Compilar Frontend

```bash
# Desenvolvimento (HMR - Hot Module Replacement)
docker-compose exec orionone-frontend npm run dev

# OU Build para produção
docker-compose exec orionone-frontend npm run build
```

### 7. Verificar Funcionamento

```bash
# Executar testes
docker-compose exec orionone-app php artisan test

# Verificar dados seedados
docker-compose exec orionone-db psql -U laravel -d orionone -c "SELECT * FROM roles;"
```

**Aceder à Aplicação:**

-   **Laravel (Backend):** http://localhost:8888
-   **Vite (Frontend HMR):** http://localhost:5173
-   **PostgreSQL:** localhost:5433 (user: laravel, password: laravel, db: orionone)

---

## Comandos do Dia-a-Dia

### Iniciar Projeto

```bash
# Iniciar todos os containers
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Iniciar frontend (se ainda não estiver)
docker-compose exec orionone-frontend npm run dev
```

### Parar Projeto

```bash
# Parar containers (mantém volumes/dados)
docker-compose stop

# Parar E remover containers (mantém volumes/dados)
docker-compose down

# Remover TUDO (containers + volumes + dados)
docker-compose down -v
```

### Trabalhar com Base de Dados

```bash
# Resetar DB + re-seed
docker-compose exec orionone-app php artisan migrate:fresh --seed

# Criar nova migration
docker-compose exec orionone-app php artisan make:migration create_example_table

# Criar novo seeder
docker-compose exec orionone-app php artisan make:seeder ExampleSeeder

# Aceder ao PostgreSQL (psql)
docker-compose exec orionone-db psql -U laravel -d orionone
```

### Executar Testes

```bash
# Todos os testes
docker-compose exec orionone-app php artisan test

# Teste específico
docker-compose exec orionone-app php artisan test --filter=RolePermissionTest

# Com coverage
docker-compose exec orionone-app php artisan test --coverage
```

---

## Resolução de Problemas

### Containers não iniciam

```bash
# Ver logs de erros
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Erro "could not find driver" (PostgreSQL)

**Causa:** Tentaste correr `php artisan` **localmente** em vez de dentro do container Docker.

**Solução:** Sempre usar `docker-compose exec orionone-app php artisan ...`

### Erro de permissões (Linux/Mac)

```bash
# Dar permissões corretas
sudo chown -R $USER:$USER storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

### Frontend não compila / Vite não inicia

```bash
# Reinstalar dependências
docker-compose exec orionone-frontend rm -rf node_modules package-lock.json
docker-compose exec orionone-frontend npm install --legacy-peer-deps

# Verificar portas (5173 deve estar livre)
docker-compose ps
```

### Base de dados não conecta

```bash
# Verificar se PostgreSQL está a correr
docker-compose ps

# Verificar logs do PostgreSQL
docker-compose logs orionone-db

# Recriar base de dados
docker-compose exec orionone-db psql -U laravel -d postgres -c "DROP DATABASE IF EXISTS orionone;"
docker-compose exec orionone-db psql -U laravel -d postgres -c "CREATE DATABASE orionone;"
docker-compose exec orionone-app php artisan migrate:fresh --seed
```

---

## Estrutura de Containers Docker

| Container           | Serviço              | Porta | Propósito                   |
| ------------------- | -------------------- | ----- | --------------------------- |
| `orionone-app`      | Laravel 11 (PHP 8.4) | 8888  | Backend API + Aplicação     |
| `orionone-db`       | PostgreSQL 16        | 5433  | Base de dados principal     |
| `orionone-frontend` | Node.js 20 + Vite    | 5173  | Frontend (Vue 3 + Tailwind) |
| `orionone-redis`    | Redis 7              | 6379  | Cache + Sessions + Queues   |

---

## Credenciais Padrão (Desenvolvimento)

### Utilizadores Seedados

| Email               | Password | Role  | Permissões           |
| ------------------- | -------- | ----- | -------------------- |
| admin@orionone.test | password | admin | Todas                |
| agent@orionone.test | password | agent | Tickets + Comments   |
| user@orionone.test  | password | user  | Criar tickets apenas |

### Base de Dados

-   **Host:** localhost (ou orionone-db dentro do Docker)
-   **Porta:** 5433 (externa) / 5432 (interna)
-   **Database:** orionone
-   **User:** laravel
-   **Password:** laravel

---

## Documentação Completa

Para informação detalhada sobre o setup, consultar:

-   **[Setup Changelog](docs/setup-changelog.md)** - Histórico completo de instalação, pacotes, configurações
-   **[Commands Reference](docs/commands-reference.md)** - Todos os comandos (Git, Docker, Laravel, NPM)
-   **[Docker Guide](docs/docker-guide.md)** - Guia Docker para iniciantes
-   **[Tech Stack](docs/tech-stack.md)** - Stack tecnológica completa

---

## Próximos Passos

Seguir **[Implementation Checklist](docs/implementation-checklist.md)** para começar o desenvolvimento:

1. **Sprint 1:** Auth & Users (Roles, Permissions, Seeders)
2. **Sprint 2:** Tickets Core (CRUD, Status, Priority)
3. **Sprint 3:** Colaboração (Comments, Teams, Notifications)
4. **Sprint 4:** Knowledge Base
5. **Sprint 5:** Dashboard & Reports
6. **Sprint 6:** Polish & Deploy

---

**Status:** Ambiente 100% configurado, pronto para desenvolvimento!
