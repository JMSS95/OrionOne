# Guia Docker - OrionOne

**Data:** 08 Novembro 2025
**Público-Alvo:** Iniciantes em Docker

---

## O Que É Docker?

Docker é uma plataforma que permite executar aplicações em **containers** - ambientes isolados que contêm tudo o que a aplicação precisa para funcionar (código, bibliotecas, dependências).

### Analogia

Pensa no Docker como **contentores de transporte marítimo**:

-   **Sem Docker:** Cada aplicação precisa de um servidor dedicado, instalação manual de PHP, PostgreSQL, Redis, etc. Se mudares de máquina, tens de reinstalar tudo.

-   **Com Docker:** A aplicação e todas as suas dependências são empacotadas num "contentor". Podes mover esse contentor para qualquer máquina com Docker e vai funcionar exatamente da mesma forma.

### Vantagens

1. **Consistência:** "Funciona na minha máquina" → funciona em TODAS as máquinas
2. **Isolamento:** Cada projeto tem as suas próprias versões de PHP, PostgreSQL, etc.
3. **Rapidez:** Iniciar um container demora segundos (vs. minutos de uma VM)
4. **Portabilidade:** Mesmo ambiente em desenvolvimento, staging e produção
5. **Fácil onboarding:** Novos developers fazem `docker-compose up` e está pronto

---

## Conceitos Básicos

### Container

Um processo isolado que executa a aplicação. É **efémero** (pode ser destruído e recriado sem perder dados importantes).

**Exemplo:** Container do Laravel executa PHP 8.2-FPM + a tua aplicação.

### Imagem

Template para criar containers. Define o sistema operativo, software instalado, configurações.

**Exemplo:** `php:8.2-fpm` é uma imagem oficial do PHP 8.2 com FPM.

### Volume

Forma de persistir dados fora do container. Quando o container é destruído, os dados no volume permanecem.

**Exemplo:** Base de dados PostgreSQL usa volume para não perder dados ao reiniciar.

### Network

Rede virtual que permite comunicação entre containers.

**Exemplo:** Container Laravel comunica com container PostgreSQL via network `orionone-network`.

### Docker Compose

Ferramenta para definir e executar múltiplos containers de uma vez, usando ficheiro YAML.

**Exemplo:** OrionOne tem 5 containers (Laravel, Vite, Nginx, PostgreSQL, Redis) orquestrados via `docker-compose.yml`.

---

## Arquitetura OrionOne

O projeto OrionOne usa **5 containers** que trabalham juntos:

```
┌─────────────────────────────────────────────────────────────┐
│                      DOCKER HOST                            │
│                                                             │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │  Nginx        │  │  Vite         │  │  Laravel      │  │
│  │  (Web Server) │  │  (Dev Server) │  │  (PHP 8.2)    │  │
│  │  Port: 80     │  │  Port: 5173   │  │  PHP-FPM      │  │
│  └───────┬───────┘  └───────────────┘  └───────┬───────┘  │
│          │                                      │          │
│          │         ┌───────────────┐            │          │
│          └────────▶│  PostgreSQL   │◀───────────┘          │
│                    │  Port: 5432   │                       │
│                    └───────────────┘                       │
│                                                             │
│                    ┌───────────────┐                       │
│                    │  Redis        │                       │
│                    │  Port: 6379   │                       │
│                    └───────────────┘                       │
│                                                             │
│  Network: orionone-network                                 │
└─────────────────────────────────────────────────────────────┘
```

### 1. orionone-app (Laravel PHP)

-   **Imagem:** `php:8.2-fpm`
-   **Função:** Executa código PHP da aplicação Laravel
-   **Portas:** Interna (9000 para Nginx comunicar)
-   **Volumes:**
    -   `./:/var/www/html` (código da aplicação)
    -   `./storage` (logs, cache)
-   **Dependências:** PostgreSQL, Redis

### 2. orionone-vite (Vite Dev Server)

-   **Imagem:** `node:20-alpine`
-   **Função:** Hot module replacement (HMR) para Vue 3
-   **Portas:** 5173 (acessível em `http://localhost:5173`)
-   **Comando:** `npm run dev`

### 3. orionone-nginx (Web Server)

-   **Imagem:** `nginx:alpine`
-   **Função:** Servir aplicação (recebe requests HTTP, passa para PHP-FPM)
-   **Portas:** 80 (acessível em `http://localhost`)
-   **Volumes:**
    -   `./:/var/www/html` (para servir assets estáticos)
    -   `./docker/nginx/default.conf` (configuração)

### 4. orionone-db (PostgreSQL)

-   **Imagem:** `postgres:16-alpine`
-   **Função:** Base de dados relacional
-   **Portas:** 5432
-   **Volumes:** `postgres-data` (persistir dados)
-   **Credenciais:**
    -   User: `orionone_user`
    -   Password: `secret`
    -   Database: `orionone_db`

### 5. orionone-redis (Redis)

-   **Imagem:** `redis:7-alpine`
-   **Função:** Cache, sessions, queues
-   **Portas:** 6379
-   **Volumes:** `redis-data` (persistir cache)

---

## Ficheiro docker-compose.yml Explicado

```yaml
services:
    # Container Laravel PHP
    orionone-app:
        build:
            context: . # Usa Dockerfile na raiz
            dockerfile: Dockerfile
        container_name: orionone-app
        volumes:
            - ./:/var/www/html # Monta código no container
            - ./storage:/var/www/html/storage
        networks:
            - orionone-network # Conecta à rede interna
        depends_on:
            - orionone-db # Espera DB iniciar primeiro
            - orionone-redis

    # Container PostgreSQL
    orionone-db:
        image: postgres:16-alpine
        container_name: orionone-db
        environment:
            POSTGRES_DB: orionone_db
            POSTGRES_USER: orionone_user
            POSTGRES_PASSWORD: secret
        volumes:
            - postgres-data:/var/lib/postgresql/data # Volume persistente
        networks:
            - orionone-network
        ports:
            - "5432:5432" # Expõe para host (opcional)

    # (outros containers...)

# Volumes nomeados (persistem entre restarts)
volumes:
    postgres-data:
    redis-data:

# Rede interna (containers comunicam entre si)
networks:
    orionone-network:
        driver: bridge
```

---

## Comandos Docker Essenciais

### Gestão de Containers

#### Iniciar todos os containers

```bash
docker-compose up -d
```

-   `-d` = detached mode (corre em background)

#### Ver containers a correr

```bash
docker-compose ps
```

**Output esperado:**

```
NAME              STATUS    PORTS
orionone-app      Up        9000/tcp
orionone-vite     Up        5173/tcp
orionone-nginx    Up        80/tcp
orionone-db       Up        5432/tcp
orionone-redis    Up        6379/tcp
```

#### Parar containers

```bash
docker-compose stop
```

#### Parar e remover containers

```bash
docker-compose down
```

#### Parar, remover containers E volumes (apaga dados!)

```bash
docker-compose down -v
```

**CUIDADO:** Apaga base de dados!

---

### Executar Comandos Dentro de Containers

#### Executar comando Artisan

```bash
docker-compose exec orionone-app php artisan [comando]
```

**Exemplos:**

```bash
# Executar migrations
docker-compose exec orionone-app php artisan migrate

# Criar controller
docker-compose exec orionone-app php artisan make:controller TicketController

# Limpar cache
docker-compose exec orionone-app php artisan cache:clear

# Executar testes
docker-compose exec orionone-app php artisan test
```

#### Executar Composer

```bash
docker-compose exec orionone-app composer install
docker-compose exec orionone-app composer require spatie/laravel-data
```

#### Executar NPM (no host, NÃO no container)

```bash
npm install
npm run dev
npm run build
```

---

### Entrar no Container (Shell Interativo)

#### Bash no container Laravel

```bash
docker-compose exec orionone-app bash
```

Agora estás "dentro" do container:

```bash
root@abc123:/var/www/html# ls
app  bootstrap  composer.json  config  database  ...

root@abc123:/var/www/html# php artisan --version
Laravel Framework 11.31.0
```

Para sair:

```bash
exit
```

#### Psql no container PostgreSQL

```bash
docker-compose exec orionone-db psql -U orionone_user -d orionone_db
```

**Comandos úteis:**

```sql
\dt              -- Listar tabelas
\d users         -- Descrever tabela users
SELECT * FROM users;
\q               -- Sair
```

---

### Ver Logs

#### Logs de todos os containers

```bash
docker-compose logs -f
```

-   `-f` = follow (continua a mostrar novos logs)

#### Logs de um container específico

```bash
docker-compose logs -f orionone-app
docker-compose logs -f orionone-db
```

#### Últimas 100 linhas

```bash
docker-compose logs --tail=100 orionone-app
```

---

### Rebuild Containers

#### Rebuild após alterar Dockerfile

```bash
docker-compose up -d --build
```

#### Rebuild forçado (ignora cache)

```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## Workflows Comuns

### Primeira Vez (Setup Inicial)

```bash
# 1. Clonar repo
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# 2. Copiar .env
cp .env.example .env

# 3. Iniciar Docker
docker-compose up -d

# 4. Instalar dependências PHP
docker-compose exec orionone-app composer install

# 5. Gerar APP_KEY
docker-compose exec orionone-app php artisan key:generate

# 6. Executar migrations
docker-compose exec orionone-app php artisan migrate

# 7. Instalar dependências NPM (no host)
npm install

# 8. Iniciar Vite dev server (no host)
npm run dev

# 9. Aceder à aplicação
# http://localhost
```

---

### Dia-a-Dia (Desenvolvimento)

```bash
# Manhã: Iniciar ambiente
docker-compose up -d
npm run dev

# Criar nova migration
docker-compose exec orionone-app php artisan make:migration create_tickets_table

# Executar migration
docker-compose exec orionone-app php artisan migrate

# Executar testes
docker-compose exec orionone-app php artisan test

# Ver logs do Laravel
docker-compose logs -f orionone-app

# Noite: Parar ambiente
docker-compose stop
```

---

### Reset Completo (Recomeçar do Zero)

```bash
# 1. Parar e remover tudo (incluindo volumes)
docker-compose down -v

# 2. Remover imagens (opcional)
docker-compose down --rmi all

# 3. Rebuild
docker-compose up -d --build

# 4. Reinstalar
docker-compose exec orionone-app composer install
docker-compose exec orionone-app php artisan key:generate
docker-compose exec orionone-app php artisan migrate:fresh --seed
```

---

## Troubleshooting

### Problema: Port already in use

**Erro:**

```
Error: bind: address already in use (port 80)
```

**Solução 1:** Parar serviço que usa a porta

```bash
# Windows (parar Apache/IIS)
net stop w3svc

# Verificar o que usa a porta 80
netstat -ano | findstr :80
```

**Solução 2:** Mudar porta no `docker-compose.yml`

```yaml
orionone-nginx:
    ports:
        - "8080:80" # Mudar para 8080
```

Aceder via `http://localhost:8080`

---

### Problema: Container não inicia

**Verificar logs:**

```bash
docker-compose logs orionone-app
```

**Causas comuns:**

1. Erro no `.env` (credenciais DB erradas)
2. Dependência falhada (DB não está pronto)
3. Erro no Dockerfile

**Solução:**

```bash
# Rebuild forçado
docker-compose down
docker-compose up -d --build
```

---

### Problema: Permission denied (storage)

**Erro:**

```
The stream or file "storage/logs/laravel.log" could not be opened
```

**Solução (dentro do container):**

```bash
docker-compose exec orionone-app chmod -R 775 storage bootstrap/cache
docker-compose exec orionone-app chown -R www-data:www-data storage bootstrap/cache
```

---

### Problema: Migrations falham

**Erro:**

```
SQLSTATE[08006] Connection refused
```

**Solução:**

```bash
# 1. Verificar se DB está a correr
docker-compose ps orionone-db

# 2. Verificar logs do DB
docker-compose logs orionone-db

# 3. Testar conexão manual
docker-compose exec orionone-db psql -U orionone_user -d orionone_db

# 4. Verificar .env
DB_CONNECTION=pgsql
DB_HOST=orionone-db    # Nome do container, NÃO localhost!
DB_PORT=5432
DB_DATABASE=orionone_db
DB_USERNAME=orionone_user
DB_PASSWORD=secret
```

---

### Problema: Vite HMR não funciona

**Solução:**

```bash
# 1. Parar Vite
Ctrl+C

# 2. Limpar cache
rm -rf node_modules/.vite

# 3. Reiniciar
npm run dev
```

Se não resolver, verificar `vite.config.js`:

```js
server: {
    host: '0.0.0.0',
    port: 5173,
    hmr: {
        host: 'localhost',
    },
}
```

---

## Boas Práticas

### 1. Nunca Editar Dentro do Container

**Errado:**

```bash
docker-compose exec orionone-app bash
vim app/Models/User.php  # NUNCA FAZER ISTO!
```

**Correto:**
Editar no host (VSCode, PhpStorm). Mudanças são automaticamente sincronizadas via volume mount.

---

### 2. Usar .dockerignore

Evitar copiar ficheiros desnecessários para imagem:

```
.git
.env
node_modules
vendor
storage/logs
```

---

### 3. Separar Dev vs Produção

**Dev:** `docker-compose.yml` (com Vite, volumes, debug)
**Prod:** `docker-compose.prod.yml` (otimizado, sem dev tools)

```bash
# Produção
docker-compose -f docker-compose.prod.yml up -d
```

---

### 4. Usar Multi-Stage Builds

Dockerfile otimizado (reduz tamanho da imagem):

```dockerfile
# Stage 1: Builder
FROM php:8.2-fpm AS builder
COPY . /var/www/html
RUN composer install --no-dev --optimize-autoloader

# Stage 2: Runtime
FROM php:8.2-fpm
COPY --from=builder /var/www/html /var/www/html
```

---

## Recursos Adicionais

### Documentação Oficial

-   Docker: https://docs.docker.com/
-   Docker Compose: https://docs.docker.com/compose/
-   Laravel Docker: https://laravel.com/docs/sail

### Cheat Sheet

```bash
# Ver todas as imagens
docker images

# Ver todos os containers (incluindo parados)
docker ps -a

# Remover containers parados
docker container prune

# Remover imagens não usadas
docker image prune

# Remover tudo (containers, volumes, imagens)
docker system prune -a --volumes

# Ver uso de espaço
docker system df
```

---

## Conclusão

Docker simplifica drasticamente o setup de ambientes de desenvolvimento. Com OrionOne:

1. **Clone o repo**
2. **`docker-compose up -d`**
3. **Está pronto!**

Sem instalar PHP, PostgreSQL, Redis, Nginx manualmente. Tudo isolado, reproduzível e portável.

---

**Última Atualização:** 08 Novembro 2025, 00:45
