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

## Docker Guide para Iniciantes

### O que é Docker?

Docker permite executar aplicações em **containers** - ambientes isolados que incluem tudo o que a aplicação precisa (código, runtime, bibliotecas, etc). No OrionOne, usamos 6 containers:

-   **orionone-app** - PHP 8.3 + Laravel 12 (backend)
-   **orionone-nginx** - Nginx (web server)
-   **orionone-postgres** - PostgreSQL 16 (database)
-   **orionone-redis** - Redis 7 (cache, sessions, queues)
-   **orionone-queue** - Laravel queue worker
-   **orionone-scheduler** - Laravel scheduler (cron jobs)

**Vantagens:**

-   Ambiente idêntico em todos os PCs (dev = produção)
-   Não precisa instalar PHP, PostgreSQL, Redis localmente
-   Setup em 10 minutos vs 2+ horas manual
-   Isolar projetos (cada um com suas versões)

### Conceitos Básicos

| Termo              | Explicação                             | Exemplo                          |
| ------------------ | -------------------------------------- | -------------------------------- |
| **Image**          | Template do container (como um ISO)    | `php:8.3-fpm`                    |
| **Container**      | Instância executável de uma image      | `orionone-app` a correr          |
| **Volume**         | Pasta compartilhada (host ↔ container) | `./storage` ↔ `/var/www/storage` |
| **Port Mapping**   | Expor portas do container              | `8888:80` (host:container)       |
| **docker-compose** | Orquestra múltiplos containers         | `docker-compose.yml`             |

### Comandos Essenciais

#### Gestão de Containers

```bash
# Ver containers a correr
docker-compose ps

# Ver TODOS os containers (incluindo parados)
docker ps -a

# Iniciar containers
docker-compose up -d          # -d = detached (background)

# Parar containers
docker-compose stop           # Apenas para (dados mantidos)
docker-compose down           # Para E remove (volumes mantidos)
docker-compose down -v        # Remove TUDO (incluindo dados!)

# Reiniciar um container específico
docker-compose restart orionone-app

# Ver logs
docker-compose logs -f                    # Todos os containers
docker-compose logs -f orionone-app       # Container específico
docker-compose logs --tail=50 orionone-app # Últimas 50 linhas
```

#### Executar Comandos dentro dos Containers

```bash
# Sintaxe: docker-compose exec <container> <comando>

# Laravel commands
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan test
docker-compose exec orionone-app composer install

# Abrir shell dentro do container
docker-compose exec orionone-app bash
docker-compose exec orionone-app sh        # Se bash não existir

# PostgreSQL commands
docker-compose exec orionone-postgres psql -U postgres -d orionone

# Redis CLI
docker-compose exec orionone-redis redis-cli
```

#### Debugging

```bash
# Ver logs de erro
docker-compose logs --tail=100 orionone-app | grep -i error

# Verificar uso de recursos
docker stats

# Inspecionar container
docker inspect orionone-app

# Ver processos dentro do container
docker-compose exec orionone-app ps aux
```

### Estrutura do docker-compose.yml

```yaml
services:
    orionone-app: # Nome do serviço
        build: # Construir de Dockerfile
            context: .
            dockerfile: Dockerfile
        ports: # Port mapping
            - "8888:80" # host:container
        volumes: # Pastas compartilhadas
            - ./:/var/www
        environment: # Variáveis de ambiente
            DB_HOST: orionone-postgres
        depends_on: # Dependências (iniciar primeiro)
            - orionone-postgres
            - orionone-redis
```

### Troubleshooting Docker

#### Container não inicia

```bash
# Ver erro detalhado
docker-compose logs orionone-app

# Rebuild sem cache
docker-compose build --no-cache orionone-app
docker-compose up -d
```

#### Porta já em uso (Port 8888 already allocated)

```bash
# Ver o que está a usar a porta
# Windows PowerShell:
netstat -ano | findstr :8888
# Linux/Mac:
lsof -i :8888

# Parar o processo OU mudar porta no docker-compose.yml:
ports:
  - "9000:80"  # Usar porta 9000 em vez de 8888
```

#### Container reinicia constantemente (restart loop)

```bash
# Ver logs de erro
docker-compose logs --tail=100 orionone-app

# Causas comuns:
# - Erro no código PHP (syntax error)
# - Dependência falhada (DB não conecta)
# - Porta já ocupada
```

#### Espaço em disco cheio (Docker usa muito espaço)

```bash
# Limpar containers/images não usados
docker system prune -a

# Limpar volumes órfãos
docker volume prune

# Ver uso de espaço
docker system df
```

### Docker vs Local (Quando usar cada um?)

| Tarefa           | Usar      | Comando                                                |
| ---------------- | --------- | ------------------------------------------------------ |
| Rodar aplicação  | ✅ Docker | `docker-compose up -d`                                 |
| Migrations       | ✅ Docker | `docker-compose exec orionone-app php artisan migrate` |
| Testes           | ✅ Docker | `docker-compose exec orionone-app php artisan test`    |
| Composer install | ✅ Docker | `docker-compose exec orionone-app composer install`    |
| NPM install      | ✅ Docker | `docker-compose exec orionone-app npm install`         |
| Editar código    | ❌ Local  | VS Code no host (sync automático via volume)           |
| Git              | ❌ Local  | `git` no host (não precisa Docker)                     |

**Regra de ouro:** Tudo que executa código PHP/Node → Docker. Edição/Git → Local.

### Boas Práticas

1. **Sempre usar `docker-compose exec`** em vez de entrar no container manualmente
2. **Não instalar PHP/PostgreSQL/Redis localmente** - usar apenas Docker
3. **Commit `.env.example`** mas NUNCA commit `.env` (credenciais)
4. **Fazer backup dos volumes** antes de `docker-compose down -v`
5. **Ver logs regularmente** para antecipar problemas

### Recursos de Aprendizagem

-   **Docker Docs:** https://docs.docker.com/get-started/
-   **Docker Compose Docs:** https://docs.docker.com/compose/
-   **Laravel Docker:** https://laravel.com/docs/sail (alternativa oficial)

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

Para informação detalhada, consultar:

-   **[Implementation Checklist](docs/implementation-checklist.md)** - Checklist TDD sprint-by-sprint (Sprint 1 completo)
-   **[Commands Reference](docs/COMMANDS-REFERENCE.md)** - Todos os comandos (Git, Docker, Laravel, NPM)
-   **[Development Guide](docs/development-guide.md)** - Workflow TDD, patterns, conventions
-   **[Tech Stack](docs/tech-stack.md)** - Stack tecnológica completa (Backend, Frontend, DevOps)
-   **[Architecture](docs/architecture.md)** - Arquitetura do sistema (MVC + Services + Actions)

---

## Próximos Passos

Seguir **[Implementation Checklist](docs/implementation-checklist.md)** para começar o desenvolvimento:

1. **Sprint 1:** Auth & Users (Roles, Permissions, Profile, Avatar, Database Views/Triggers) - **COMPLETO**
2. **Sprint 2:** Tickets Core (CRUD, Status, Priority, Filters, API REST)
3. **Sprint 3:** Comments (Colaboração, Mentions, Notifications)
4. **Sprint 4:** Knowledge Base (Articles, Categories, Full-text Search)
5. **Sprint 5:** Dashboard & SLA (Analytics, SLA tracking, Charts)
6. **Sprint 6:** Teams & Automation (Team management, Auto-assignment, Reports)
7. **Sprint 7:** Asset Management (CMDB, 6 asset types, CSV Import/Export)

**Roadmap completo:** Ver [MVP.md](docs/MVP.md) para cronograma de 32 semanas e métricas (ITSM Score: 8.5/10).

---

**Status:** Ambiente 100% configurado, pronto para desenvolvimento!
