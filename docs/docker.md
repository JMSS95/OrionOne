# Docker Setup - OrionOne

## Visão Geral

OrionOne utiliza uma arquitetura Docker multi-container com 4 serviços principais.

### Acesso à Aplicação

**Desenvolvimento com Laragon:**

-   **Laravel:** `http://orionone.test:8888/` (Nginx porta 8888)
-   **Vite HMR:** `http://localhost:5173/` (Frontend dev server)

**Containers Docker:**

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │   App    │──│ Frontend │──│PostgreSQL│──│  Redis  │ │
│  │ Laravel  │  │  Vite    │  │    16    │  │    7    │ │
│  │  :9000   │  │  :5173   │  │  :5432   │  │  :6379  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Containers

### 1. **orionone-app** (Laravel + PHP-FPM)

**Imagem:** `php:8.2-fpm-alpine`
**Porta:** `9000` (FastCGI)
**Volumes:**

-   `./:/var/www/html` - código fonte
-   `./docker/php/php.ini` - configuração PHP customizada

**Responsabilidades:**

-   Executar aplicação Laravel
-   Processar requests HTTP via Nginx
-   Queue workers (background jobs)
-   Scheduled tasks (cron)

**Extensions PHP instaladas:**

-   `pdo_pgsql` - PostgreSQL driver
-   `redis` - Redis client
-   `gd` - Image processing
-   `zip` - Compression
-   `opcache` - Performance

---

### 2. **orionone-frontend** (Vite Dev Server)

**Imagem:** `node:20-alpine`
**Porta:** `5173` (HMR - Hot Module Replacement)
**Volumes:**

-   `./:/app` - código fonte
-   `/app/node_modules` - dependências isoladas

**Responsabilidades:**

-   Build de assets (JS, CSS)
-   Hot Module Replacement (desenvolvimento)
-   Serve frontend em modo dev

**Comandos:**

-   **Dev:** `npm run dev --host`
-   **Build:** `npm run build`

---

### 3. **orionone-db** (PostgreSQL 16)

**Imagem:** `postgres:16-alpine`
**Porta:** `5432`
**Volumes:**

-   `orionone_pgdata:/var/lib/postgresql/data` - persistência

**Environment Variables:**

```env
POSTGRES_DB=orionone
POSTGRES_USER=laravel
POSTGRES_PASSWORD=secret
```

**Features utilizadas:**

-   JSONB indexes (custom_fields)
-   Full-text search (Knowledge Base)
-   Composite indexes
-   Soft deletes

**Healthcheck:**

```bash
pg_isready -U laravel
```

---

### 4. **orionone-redis** (Redis 7)

**Imagem:** `redis:7-alpine`
**Porta:** `6379`
**Volumes:**

-   `orionone_redisdata:/data` - persistência AOF

**Responsabilidades:**

-   **Sessions:** armazenamento de sessões
-   **Cache:** query results, dashboard stats
-   **Queue:** jobs assíncronos (emails, SLA checks)
-   **Locks:** distributed locking

**Persistence:** AOF (Append-Only File) habilitado

---

## Nginx (Opcional - Produção)

Para produção, adicionar container Nginx:

**Imagem:** `nginx:alpine`
**Porta:** `80`, `443`
**Config:** `./docker/nginx/default.conf`

```nginx
server {
    listen 80;
    server_name orionone.test;
    root /var/www/html/public;

    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass orionone-app:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

---

## Network

**Nome:** `orionone_network`
**Driver:** `bridge`

Todos os containers conectados à mesma rede para comunicação interna.

**DNS interno:**

-   `orionone-app` → Laravel/PHP-FPM
-   `orionone-db` → PostgreSQL
-   `orionone-redis` → Redis
-   `orionone-frontend` → Vite

---

## Volumes

### Volumes nomeados (persistentes)

```yaml
volumes:
    orionone_pgdata: # PostgreSQL data
    orionone_redisdata: # Redis AOF
```

**Backup:**

```bash
# PostgreSQL
docker exec orionone_postgres pg_dump -U laravel orionone > backup.sql

# Restore
docker exec -i orionone_postgres psql -U laravel orionone < backup.sql

# Redis
docker exec orionone_redis redis-cli SAVE
docker cp orionone_redis:/data/dump.rdb ./backup/
```

---

## Comandos Úteis

### Iniciar containers

```bash
# Iniciar todos os serviços
docker-compose up -d

# Logs em tempo real
docker-compose logs -f

# Logs de serviço específico
docker-compose logs -f orionone-app
```

### Setup inicial

```bash
# 1. Build das imagens
docker-compose build

# 2. Iniciar containers
docker-compose up -d

# 3. Instalar dependências PHP
docker-compose exec orionone-app composer install

# 4. Instalar dependências Node
docker-compose exec orionone-frontend npm install

# 5. Copiar .env
docker-compose exec orionone-app cp .env.example .env

# 6. Gerar key
docker-compose exec orionone-app php artisan key:generate

# 7. Executar migrations
docker-compose exec orionone-app php artisan migrate

# 8. Seeders (dados de teste)
docker-compose exec orionone-app php artisan db:seed
```

### Desenvolvimento diário

```bash
# Artisan commands
docker-compose exec orionone-app php artisan <comando>

# Composer
docker-compose exec orionone-app composer require <package>

# NPM
docker-compose exec orionone-frontend npm install <package>

# Tinker (REPL)
docker-compose exec orionone-app php artisan tinker

# Migrations
docker-compose exec orionone-app php artisan migrate

# Testes
docker-compose exec orionone-app php artisan test
```

### Queue & Scheduler

```bash
# Queue worker (manual)
docker-compose exec orionone-app php artisan queue:work

# Schedule runner (cron simulation)
docker-compose exec orionone-app php artisan schedule:work
```

### Manutenção

```bash
# Parar containers
docker-compose down

# Parar e remover volumes (⚠️ apaga dados)
docker-compose down -v

# Rebuild containers
docker-compose up -d --build

# Ver status
docker-compose ps

# Acessar shell do container
docker-compose exec orionone-app sh

# Ver uso de recursos
docker stats
```

---

## Troubleshooting

### Erro: "Connection refused" (PostgreSQL)

**Causa:** Container não iniciou ou healthcheck falhou

**Solução:**

```bash
# Verificar logs
docker-compose logs orionone-db

# Verificar healthcheck
docker inspect orionone_postgres | grep -A 10 Health

# Restart
docker-compose restart orionone-db
```

---

### Erro: "Permission denied" (volumes)

**Causa:** Permissões de ficheiros incorretas

**Solução (Linux/macOS):**

```bash
# Dentro do container
docker-compose exec orionone-app chown -R www-data:www-data /var/www/html/storage
docker-compose exec orionone-app chmod -R 775 /var/www/html/storage
```

**Solução (Windows):**

```powershell
# Executar Docker Desktop como Admin
# Ou ajustar permissões do bind mount
```

---

### Vite HMR não funciona

**Causa:** Porta 5173 bloqueada ou host incorreto

**Solução:**

```bash
# Verificar se container está a ouvir em 0.0.0.0
docker-compose logs orionone-frontend

# Deve aparecer:
# VITE ready in XXX ms
# ➜  Local:   http://localhost:5173/
# ➜  Network: http://0.0.0.0:5173/
```

No `.env`:

```env
VITE_HOST=0.0.0.0
VITE_PORT=5173
```

---

### Redis connection failed

**Causa:** Redis não acessível ou credenciais erradas

**Solução:**

```bash
# Testar conexão
docker-compose exec orionone-app php artisan tinker
>>> Redis::ping()
# Deve retornar: "PONG"

# Verificar .env
REDIS_HOST=orionone-redis
REDIS_PORT=6379
```

---

## Performance Tuning

### PHP-FPM

`docker/php/php.ini`:

```ini
memory_limit = 256M
upload_max_filesize = 20M
post_max_size = 20M
max_execution_time = 60

opcache.enable = 1
opcache.memory_consumption = 128
opcache.interned_strings_buffer = 8
opcache.max_accelerated_files = 10000
opcache.revalidate_freq = 2
```

### PostgreSQL

`docker/postgres/postgresql.conf`:

```conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
work_mem = 4MB
max_connections = 100
```

### Redis

```bash
# AOF persistence (desenvolvimento)
appendonly yes
appendfsync everysec

# RDB persistence (produção)
save 900 1
save 300 10
```

---

## Segurança

### Produção Checklist

-   [ ] Alterar passwords default (PostgreSQL, Redis)
-   [ ] Habilitar Redis password authentication
-   [ ] SSL/TLS em PostgreSQL
-   [ ] Nginx com HTTPS (Let's Encrypt)
-   [ ] Firewalls (apenas portas 80, 443)
-   [ ] Secrets via environment variables (não hardcoded)
-   [ ] Scan de vulnerabilidades (`docker scan`)

### Exemplo Redis com password

```yaml
orionone-redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
```

`.env`:

```env
REDIS_PASSWORD=strong_random_password_here
```

---

## Ambientes

### Desenvolvimento (Local)

```yaml
# docker-compose.yml
services:
    orionone-app:
        build: .
        environment:
            APP_ENV: local
            APP_DEBUG: true
```

### Staging

```yaml
# docker-compose.staging.yml
services:
    orionone-app:
        image: registry.example.com/orionone:staging
        environment:
            APP_ENV: staging
            APP_DEBUG: false
```

### Produção

```yaml
# docker-compose.prod.yml
services:
    orionone-app:
        image: registry.example.com/orionone:latest
        environment:
            APP_ENV: production
            APP_DEBUG: false
        restart: always
```

---

## CI/CD Integration

### GitHub Actions

`.github/workflows/deploy.yml`:

```yaml
name: Deploy
on:
    push:
        branches: [main]

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3

            - name: Build Docker images
              run: docker-compose build

            - name: Run tests
              run: docker-compose exec -T orionone-app php artisan test

            - name: Deploy to production
              run: |
                  docker-compose -f docker-compose.prod.yml up -d
                  docker-compose exec -T orionone-app php artisan migrate --force
```

---

## Monitorização

### Docker Stats

```bash
# Uso de recursos em tempo real
docker stats orionone_app orionone_postgres orionone_redis
```

### Healthchecks

Adicionar ao `docker-compose.yml`:

```yaml
orionone-app:
    healthcheck:
        test: ["CMD", "php", "artisan", "health:check"]
        interval: 30s
        timeout: 10s
        retries: 3
```

---

## Recursos

-   [Docker Compose Documentation](https://docs.docker.com/compose/)
-   [PHP Docker Official Images](https://hub.docker.com/_/php)
-   [PostgreSQL Docker](https://hub.docker.com/_/postgres)
-   [Redis Docker](https://hub.docker.com/_/redis)
-   [Node Docker](https://hub.docker.com/_/node)

---

## Conclusão

Esta configuração Docker fornece:

-   ✅ **Isolamento:** cada serviço em container separado
-   ✅ **Portabilidade:** funciona em qualquer OS
-   ✅ **Reproduzibilidade:** ambiente consistente
-   ✅ **Escalabilidade:** fácil adicionar replicas
-   ✅ **Desenvolvimento rápido:** setup em minutos

**Setup total:** < 10 minutos
**Compatível com:** Windows, macOS, Linux
