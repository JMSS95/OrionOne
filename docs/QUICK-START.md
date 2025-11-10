# Quick Start - Setup em PC Novo

**Última Atualização:** 10 Novembro 2025
**Stack:** PHP 8.4 + Laravel 12 + Vue 3 + PostgreSQL 16

> **IMPORTANTE:** Este projeto usa **Docker exclusivamente**. Não é necessário instalar PHP, PostgreSQL ou Redis localmente.

---

## Pré-requisitos Obrigatórios

### Software Necessário

-   **Git** (2.40+) - [Download](https://git-scm.com/)
-   **Docker Desktop** (4.25+) - [Download](https://www.docker.com/products/docker-desktop/)
-   **Node.js** (20.x LTS) - [Download](https://nodejs.org/)
-   **VS Code** (recomendado) - [Download](https://code.visualstudio.com/)

### NÃO É NECESSÁRIO Instalar

-   PHP local (usamos Docker com PHP 8.4)
-   Composer local (incluído no container Docker)
-   PostgreSQL local (container Docker)
-   Redis local (container Docker)
-   Meilisearch local (container Docker)

---

## Setup em 10 Minutos

### 1. Clonar Repositório

```bash
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne
```

### 2. Configurar Ambiente

```bash
# Copiar .env exemplo
cp .env.example .env

# Atualizar .env se necessário (defaults funcionam)
# DB_CONNECTION=pgsql
# DB_HOST=orionone-db
# DB_DATABASE=orionone
# MEILISEARCH_HOST=http://orionone-meilisearch:7700
```

### 3. Iniciar Todos os Containers Docker

```bash
docker-compose up -d
```

**Verifica que está tudo a correr:**

```bash
docker-compose ps
```

**Deves ver 6 containers:**

-   orionone-app (PHP 8.4)
-   orionone-frontend (Node 20)
-   orionone-db (PostgreSQL 16)
-   orionone-redis (Redis 7)
-   orionone-meilisearch (Meilisearch 1.12)
-   orionone-nginx (Nginx)

### 4. Instalar Dependências Backend

```bash
docker-compose exec orionone-app composer install
```

### 5. Configurar Laravel

```bash
# Gerar chave da aplicação
docker-compose exec orionone-app php artisan key:generate

# Executar migrations
docker-compose exec orionone-app php artisan migrate

# Executar seeders (roles + permissions)
docker-compose exec orionone-app php artisan db:seed --class=RolePermissionSeeder
```

### 6. Publicar Configs Spatie

```bash
# Activity Log
docker-compose exec orionone-app php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider" --tag="activitylog-migrations"
docker-compose exec orionone-app php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider" --tag="activitylog-config"
docker-compose exec orionone-app php artisan migrate

# IDE Helper (autocomplete)
docker-compose exec orionone-app php artisan ide-helper:generate
docker-compose exec orionone-app php artisan ide-helper:models --write
docker-compose exec orionone-app php artisan ide-helper:meta
```

### 7. Instalar Dependências Frontend

```bash
# NPM install
docker-compose exec orionone-frontend npm install --legacy-peer-deps

# Build assets (produção)
docker-compose exec orionone-frontend npm run build

# OU Dev mode (hot reload)
docker-compose exec orionone-frontend npm run dev
```

### 8. Verificar Setup

```bash
# Verificar tabelas criadas
docker-compose exec orionone-app php artisan db:show --counts

# Verificar roles e permissions
docker-compose exec orionone-app php artisan tinker
>>> \Spatie\Permission\Models\Role::with('permissions')->get()
>>> exit

# Rodar tests (Pest PHP)
docker-compose exec orionone-app php artisan test
```

---

## Acesso à Aplicação

### URLs

-   **Frontend:** http://localhost
-   **Laravel Pulse:** http://localhost/pulse (monitoring)
-   **API Docs (Scribe):** http://localhost/docs
-   **Meilisearch:** http://localhost:7700
-   **Telescope:** http://localhost/telescope (debug)

### Utilizadores de Teste

Após executar seeders:

```
Admin:
  Email: admin@orionone.test
  Password: password
  Role: admin (todas as permissões)

Agent:
  Email: agent@orionone.test
  Password: password
  Role: agent (manage tickets + comments)

User:
  Email: user@orionone.test
  Password: password
  Role: user (create tickets only)
```

---

## Comandos Úteis

### Docker

```bash
# Ver containers a correr
docker-compose ps

# Ver logs de um container
docker-compose logs -f orionone-app

# Parar todos os containers
docker-compose down

# Parar e remover volumes (CUIDADO: apaga BD)
docker-compose down -v

# Rebuild containers (após mudar Dockerfile)
docker-compose up -d --build
```

### Laravel (via Docker)

```bash
# Artisan commands
docker-compose exec orionone-app php artisan [command]

# Migrations
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan migrate:fresh --seed

# Cache
docker-compose exec orionone-app php artisan config:clear
docker-compose exec orionone-app php artisan cache:clear
docker-compose exec orionone-app php artisan route:clear

# Tinker (REPL)
docker-compose exec orionone-app php artisan tinker

# Tests (Pest PHP)
docker-compose exec orionone-app php artisan test
docker-compose exec orionone-app php artisan test --filter RolePermissionTest
```

### Frontend (via Docker)

```bash
# Dev mode (hot reload)
docker-compose exec orionone-frontend npm run dev

# Build produção
docker-compose exec orionone-frontend npm run build

# Verificar erros
docker-compose exec orionone-frontend npm run type-check
```

---

## Troubleshooting

### "could not find driver" (PDO PostgreSQL)

**Solução:** Usar Docker SEMPRE. PHP local não tem extensão pgsql.

```bash
# ERRADO (PHP local)
php artisan migrate

# CERTO (Docker)
docker-compose exec orionone-app php artisan migrate
```

### Containers não iniciam

```bash
# Ver erros específicos
docker-compose logs orionone-app

# Rebuild completo
docker-compose down
docker-compose up -d --build
```

### Porta 80 já em uso

**Solução:** Parar Apache/Nginx local ou mudar porta no docker-compose.yml

```yaml
# docker-compose.yml
services:
    orionone-nginx:
        ports:
            - "8080:80" # Usar porta 8080
```

### Frontend não atualiza (HMR não funciona)

```bash
# Rebuild frontend container
docker-compose restart orionone-frontend

# Ver logs
docker-compose logs -f orionone-frontend
```

---

## Próximos Passos

1. **Ler documentação:** [docs/README.md](README.md)
2. **Ver roadmap MVP:** [docs/MVP.md](MVP.md)
3. **Metodologia TDD:** [docs/development-guide.md](development-guide.md)
4. **Implementar Sprint 2:** [docs/implementation-checklist.md](implementation-checklist.md)

---

## Stack Técnica

| Componente      | Versão | Container            |
| --------------- | ------ | -------------------- |
| **PHP**         | 8.4    | orionone-app         |
| **Laravel**     | 12.x   | orionone-app         |
| **Vue**         | 3.4    | orionone-frontend    |
| **Vite**        | 6.4    | orionone-frontend    |
| **PostgreSQL**  | 16     | orionone-db          |
| **Redis**       | 7      | orionone-redis       |
| **Meilisearch** | 1.12   | orionone-meilisearch |
| **Nginx**       | alpine | orionone-nginx       |

**Score Stack:** 8.7/10 (EXCELENTE) - Ver [STACK-ANALYSIS-2025.md](STACK-ANALYSIS-2025.md)

---

**Última Atualização:** 10 Novembro 2025, 06:00
**Status:** DOCKER-FIRST APPROACH - 100% VIA CONTAINERS

### Frontend não compila

```bash
docker-compose exec orionone-frontend rm -rf node_modules
docker-compose exec orionone-frontend npm install --legacy-peer-deps
```

---

**Ver mais:** [SETUP.md](../SETUP.md) para troubleshooting completo
