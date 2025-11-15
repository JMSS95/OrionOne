# Setup Rápido - OrionOne

## Pré-requisitos (Instalar num PC Novo)

### Software Obrigatório

| Software           | Versão Mínima | Link Download                                                 | Propósito                     |
| ------------------ | ------------- | ------------------------------------------------------------- | ----------------------------- |
| **Git**            | 2.40+         | [git-scm.com](https://git-scm.com/)                           | Controlo de versão            |
| **Docker Desktop** | 4.25+         | [docker.com](https://www.docker.com/products/docker-desktop/) | Containers (PostgreSQL, etc.) |
| **Node.js**        | 20.x LTS      | [nodejs.org](https://nodejs.org/)                             | Next.js + Nest.js runtimes    |

### Software Opcional (Recomendado)

| Software | Propósito |
| -------------------------- | ---------------------------------- |
| **Visual Studio Code** | IDE recomendado |
| **Postman** | Testar API endpoints |
| **pgAdmin** ou **DBeaver** | Cliente PostgreSQL (visualizar DB) |

### Extensões VS Code Recomendadas

```json
{
    "recommendations": [
        "bradlc.vscode-tailwindcss",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "editorconfig.editorconfig",
        "ms-azuretools.vscode-docker",
        "prisma.prisma"
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
# Backend (Nest.js)
cd nest-backend
cp .env.example .env
# Editar .env: DATABASE_URL, JWT_SECRET, etc.
cd ..

# Frontend (Next.js)
cd next-frontend
cp .env.local.example .env.local
# Editar .env.local: NEXT_PUBLIC_API_URL, etc.
cd ..
```

### 3. Iniciar Docker

```bash
# Iniciar containers (PostgreSQL + Redis + Mailpit + Nginx)
docker-compose up -d

# Verificar se containers estão a correr
docker-compose ps
```

### 4. Instalar Dependências

```bash
# Backend (Nest.js)
cd nest-backend
npm install
cd ..

# Frontend (Next.js)
cd next-frontend
npm install
cd ..
```

### 5. Configurar Base de Dados

```bash
# Entrar na pasta do backend
cd nest-backend

# Executar migrations (criar tabelas)
npx prisma migrate dev

# (Opcional) Seed de dados iniciais
npx prisma db seed

cd ..
```

### 6. Iniciar Aplicação

```bash
# Backend (porta 3001)
cd nest-backend
npm run start:dev
# Deixar correr em terminal separado

# Frontend (porta 3000)
cd next-frontend
npm run dev
# Deixar correr em terminal separado
```

### 7. Verificar Funcionamento

```bash
# Backend: Executar testes
cd nest-backend
npm run test
cd ..

# Frontend: Executar testes
cd next-frontend
npm run test
cd ..

# Verificar dados seedados (opcional)
docker-compose exec orionone-db psql -U postgres -d orionone -c "SELECT * FROM roles;"
```

**Aceder à Aplicação:**

-   **Frontend (Next.js):** http://localhost:3000
-   **Backend API (Nest.js):** http://localhost:3001/api
-   **API Docs (Swagger):** http://localhost:3001/api/docs
-   **PostgreSQL:** localhost:5432 (user: postgres, password: postgres, db: orionone)
-   **Mailpit (Email testing):** http://localhost:8025

---

## Comandos do Dia-a-Dia

### Iniciar Projeto

```bash
# 1. Iniciar containers Docker
docker-compose up -d

# 2. Backend (terminal 1)
cd nest-backend
npm run start:dev

# 3. Frontend (terminal 2)
cd next-frontend
npm run dev
```

### Parar Projeto

```bash
# Parar aplicações (Ctrl+C nos terminais)

# Parar containers Docker (mantém volumes/dados)
docker-compose stop

# Parar E remover containers (mantém volumes/dados)
docker-compose down

# Remover TUDO (containers + volumes + dados)
docker-compose down -v
```

### Trabalhar com Base de Dados

```bash
# Resetar DB + re-seed
cd nest-backend
npx prisma migrate reset # Warning: Apaga todos os dados!
npx prisma db seed
cd ..

# Criar nova migration
cd nest-backend
npx prisma migrate dev --name create_example_table
cd ..

# Executar migrations pendentes (produção)
cd nest-backend
npx prisma migrate deploy
cd ..

# Aceder ao PostgreSQL (psql)
docker-compose exec orionone-db psql -U postgres -d orionone

# Prisma Studio (visualizar DB no browser)
cd nest-backend
npx prisma studio # Abre em http://localhost:5555
cd ..
```

### Executar Testes

```bash
# Backend (Jest)
cd nest-backend
npm run test # Testes unitários
npm run test:watch # Watch mode
npm run test:cov # Com coverage
npm run test:e2e # Testes E2E
cd ..

# Frontend (Vitest)
cd next-frontend
npm run test # Testes unitários
npm run test:watch # Watch mode
npm run test:ui # UI interativa
cd ..
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

### Backend não inicia (Nest.js)

```bash
# Verificar logs
cd nest-backend
npm run start:dev # Ver erros no terminal

# Reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# Verificar .env (DATABASE_URL, JWT_SECRET)
cat .env
```

### Frontend não compila (Next.js)

```bash
# Reinstalar dependências
cd next-frontend
rm -rf node_modules .next package-lock.json
npm install

# Limpar cache do Next.js
rm -rf .next

# Verificar .env.local (NEXT_PUBLIC_API_URL)
cat .env.local
```

### Base de dados não conecta

```bash
# Verificar se PostgreSQL está a correr
docker-compose ps

# Ver logs do PostgreSQL
docker-compose logs orionone-db

# Recriar base de dados
docker-compose exec orionone-db psql -U postgres -c "DROP DATABASE IF EXISTS orionone;"
docker-compose exec orionone-db psql -U postgres -c "CREATE DATABASE orionone;"

# Executar migrations novamente
cd nest-backend
npx prisma migrate dev
cd ..
```

### Erro de porta já em uso

```bash
# Ver o que está a usar a porta
# Windows PowerShell:
netstat -ano | findstr :3000
netstat -ano | findstr :3001

# Linux/Mac:
lsof -i :3000
lsof -i :3001

# Matar processo ou mudar porta em:
# - nest-backend/src/main.ts (backend port)
# - next-frontend/package.json (frontend port)
```

---

## Docker Guide para Iniciantes

### O que é Docker?

Docker permite executar aplicações em **containers** - ambientes isolados que incluem tudo o que a aplicação precisa (código, runtime, bibliotecas, etc). No OrionOne, usamos 8 containers:

-   **orionone-backend** - Nest.js 10 (Node 20, porta 3001)
-   **orionone-frontend** - Next.js 15 (Node 20, porta 3000)
-   **orionone-postgres** - PostgreSQL 16 (database, porta 5432)
-   **orionone-redis** - Redis 7 (cache, sessions, queues)
-   **orionone-mailpit** - Mailpit (email testing, porta 8025)
-   **orionone-nginx** - Nginx (reverse proxy, porta 80)

**Vantagens:**

-   Ambiente idêntico em todos os PCs (dev = produção)
-   Não precisa instalar PostgreSQL, Redis localmente
-   Setup em 10 minutos vs 2+ horas manual
-   Isolar projetos (cada um com suas versões)

### Conceitos Básicos

| Termo              | Explicação                           | Exemplo                      |
| ------------------ | ------------------------------------ | ---------------------------- |
| **Image**          | Template do container (como um ISO)  | `node:20-alpine`             |
| **Container**      | Instância executável de uma image    | `orionone-backend` a correr  |
| **Volume**         | Pasta compartilhada (host container) | `./nest-backend` `/app`      |
| **Port Mapping**   | Expor portas do container            | `3000:3000` (host:container) |
| **docker-compose** | Orquestra múltiplos containers       | `docker-compose.yml`         |

### Comandos Essenciais

#### Gestão de Containers

```bash
# Ver containers a correr
docker-compose ps

# Ver TODOS os containers (incluindo parados)
docker ps -a

# Iniciar containers
docker-compose up -d # -d = detached (background)

# Parar containers
docker-compose stop # Apenas para (dados mantidos)
docker-compose down # Para E remove (volumes mantidos)
docker-compose down -v # Remove TUDO (incluindo dados!)

# Reiniciar um container específico
docker-compose restart orionone-backend

# Ver logs
docker-compose logs -f # Todos os containers
docker-compose logs -f orionone-backend # Container específico
docker-compose logs --tail=50 orionone-backend # Últimas 50 linhas
```

#### Executar Comandos dentro dos Containers

```bash
# Sintaxe: docker-compose exec <container> <comando>

# PostgreSQL commands
docker-compose exec orionone-postgres psql -U postgres -d orionone

# Redis CLI
docker-compose exec orionone-redis redis-cli

# Abrir shell dentro do container
docker-compose exec orionone-backend sh
```

#### Debugging

```bash
# Ver logs de erro
docker-compose logs --tail=100 orionone-backend | grep -i error

# Verificar uso de recursos
docker stats

# Inspecionar container
docker inspect orionone-backend

# Ver processos dentro do container
docker-compose exec orionone-backend ps aux
```

### Estrutura do docker-compose.yml

```yaml
services:
    orionone-backend: # Nome do serviço
    build: # Construir de Dockerfile
    context: ./nest-backend
    dockerfile: Dockerfile
    ports: # Port mapping
        - "3001:3001" # host:container
    volumes: # Pastas compartilhadas
        - ./nest-backend:/app
    environment: # Variáveis de ambiente
    DATABASE_URL: postgresql://postgres:postgres@orionone-postgres:5432/orionone
    depends_on: # Dependências (iniciar primeiro)
        - orionone-postgres
        - orionone-redis
```

### Troubleshooting Docker

#### Container não inicia

```bash
# Ver erro detalhado
docker-compose logs orionone-backend

# Rebuild sem cache
docker-compose build --no-cache orionone-backend
docker-compose up -d
```

#### Porta já em uso (Port 3000/3001 already allocated)

```bash
# Ver o que está a usar a porta
# Windows PowerShell:
netstat -ano | findstr :3000
# Linux/Mac:
lsof -i :3000

# Parar o processo OU mudar porta no docker-compose.yml:
ports:
 - "3002:3001" # Usar porta 3002 em vez de 3001
```

#### Container reinicia constantemente (restart loop)

```bash
# Ver logs de erro
docker-compose logs --tail=100 orionone-backend

# Causas comuns:
# - Erro no código TypeScript (syntax error)
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

| Tarefa         | Usar   | Comando                                     |
| -------------- | ------ | ------------------------------------------- |
| Rodar backend  | Local  | `cd nest-backend && npm run start:dev`      |
| Rodar frontend | Local  | `cd next-frontend && npm run dev`           |
| Migrations     | Local  | `cd nest-backend && npx prisma migrate dev` |
| Testes         | Local  | `npm run test` (em cada projeto)            |
| PostgreSQL     | Docker | `docker-compose up -d orionone-postgres`    |
| Redis          | Docker | `docker-compose up -d orionone-redis`       |
| Mailpit        | Docker | `docker-compose up -d orionone-mailpit`     |
| Nginx          | Docker | `docker-compose up -d orionone-nginx`       |
| Editar código  | Local  | VS Code no host                             |
| Git            | Local  | `git` no host                               |

**Regra de ouro:** Serviços (PostgreSQL, Redis, Mailpit) → Docker. Código (Next.js, Nest.js) → Local.

### Boas Práticas

1. **Usar Docker para serviços** (PostgreSQL, Redis, Mailpit) e **Local para código** (Next.js, Nest.js)
2. **Não instalar PostgreSQL/Redis localmente** - usar apenas Docker
3. **Commit `.env.example`** mas NUNCA commit `.env` ou `.env.local` (credenciais)
4. **Fazer backup dos volumes** antes de `docker-compose down -v`
5. **Ver logs regularmente** para antecipar problemas

### Recursos de Aprendizagem

-   **Docker Docs:** https://docs.docker.com/get-started/
-   **Docker Compose Docs:** https://docs.docker.com/compose/
-   **Next.js Docs:** https://nextjs.org/docs
-   **Nest.js Docs:** https://docs.nestjs.com/
-   **Prisma Docs:** https://www.prisma.io/docs

---

## Estrutura de Containers Docker

| Container           | Serviço       | Porta | Propósito                  |
| ------------------- | ------------- | ----- | -------------------------- |
| `orionone-backend`  | Nest.js 10    | 3001  | Backend API                |
| `orionone-frontend` | Next.js 15    | 3000  | Frontend Application       |
| `orionone-postgres` | PostgreSQL 16 | 5432  | Base de dados principal    |
| `orionone-redis`    | Redis 7       | 6379  | Cache + Sessions + Queues  |
| `orionone-mailpit`  | Mailpit       | 8025  | Email testing (dev only)   |
| `orionone-nginx`    | Nginx         | 80    | Reverse proxy (production) |

---

## Credenciais Padrão (Desenvolvimento)

### Utilizadores Seedados

| Email               | Password      | Role  | Permissões           |
| ------------------- | ------------- | ----- | -------------------- |
| admin@orionone.test | your_password | admin | Todas                |
| agent@orionone.test | your_password | agent | Tickets + Comments   |
| user@orionone.test  | your_password | user  | Criar tickets apenas |

### Base de Dados

-   **Host:** localhost
-   **Porta:** 5432
-   **Database:** orionone
-   **User:** postgres
-   **Password:** your_db_password

---

## Configuração de Tecnologias

### Winston Logging

**Status:** Configurado

Winston está configurado como sistema de logging estruturado no backend.

**Ficheiros criados:**

-   `nest-backend/src/config/logger.config.ts` - Configuração Winston
-   `nest-backend/logs/` - Diretório de logs (ignorado no Git)

**Níveis de log:**

-   `error` - Erros críticos
-   `warn` - Avisos
-   `info` - Informação geral (default)
-   `http` - Requisições HTTP
-   `verbose` - Detalhes adicionais
-   `debug` - Debug mode

**Logs gerados:**

```
logs/
├── combined.log      # Todos os logs (JSON format)
├── error.log         # Apenas erros
├── exceptions.log    # Uncaught exceptions
└── rejections.log    # Unhandled promise rejections
```

**Uso em serviços:**

```typescript
import { Inject, LoggerService } from "@nestjs/common";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";

@Injectable()
export class YourService {
    constructor(
        @Inject(WINSTON_MODULE_NEST_PROVIDER)
        private readonly logger: LoggerService
    ) {}

    async someMethod() {
        this.logger.log("Action performed", "YourService");
        this.logger.error("Error occurred", error.stack, "YourService");
    }
}
```

**Configurar nível de log:**

```bash
# .env
LOG_LEVEL=info  # production
LOG_LEVEL=debug # development
```

---

### Swagger/OpenAPI Documentation

**Status:** Configurado em `/api/docs`

API documentation interativa disponível em `http://localhost:3001/api/docs`

**Decorators disponíveis:**

```typescript
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
} from "@nestjs/swagger";

@ApiTags("incidents")
@Controller("incidents")
@ApiBearerAuth()
export class IncidentsController {
    @Post()
    @ApiOperation({ summary: "Create incident" })
    @ApiResponse({ status: 201, description: "Created" })
    @ApiResponse({ status: 400, description: "Bad Request" })
    async create(@Body() dto: CreateIncidentDto) {}
}
```

**Documentar DTOs:**

```typescript
import { ApiProperty } from "@nestjs/swagger";

export class CreateIncidentDto {
    @ApiProperty({ example: "Server Down", description: "Incident title" })
    title: string;

    @ApiProperty({ enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"] })
    priority: string;
}
```

---

### Helmet Security Headers

**Status:** Configurado globalmente

Helmet está ativo e configura headers HTTP seguros automaticamente.

**Headers configurados:**

-   `Content-Security-Policy` - Previne XSS
-   `X-DNS-Prefetch-Control` - Controla DNS prefetch
-   `X-Frame-Options` - Previne clickjacking
-   `X-Content-Type-Options` - Previne MIME sniffing
-   `Strict-Transport-Security` - Force HTTPS

**Verificar headers:**

```bash
curl -I http://localhost:3001/api/health
```

---

### Compression (Gzip/Deflate)

**Status:** Configurado globalmente

Todas as respostas HTTP são comprimidas automaticamente (redução ~60-80%).

**Testar compressão:**

```bash
curl -H "Accept-Encoding: gzip" http://localhost:3001/api/health -v
# Verificar header: Content-Encoding: gzip
```

---

### Rate Limiting (Throttler)

**Status:** Configurado (10 req/min global)

Proteção contra brute-force e abuso de API.

**Configuração global:**

-   10 requisições por minuto (padrão)
-   Ajustável em `app.module.ts`

**Override por rota:**

```typescript
import { Throttle, ThrottlerGuard } from "@nestjs/throttler";

@Controller("auth")
@UseGuards(ThrottlerGuard)
export class AuthController {
    @Post("login")
    @Throttle({ default: { limit: 3, ttl: 60000 } }) // 3 tentativas/min
    async login() {}
}
```

**Ajustar limites globais:**

```typescript
// app.module.ts
ThrottlerModule.forRoot([
    {
        ttl: 60000, // 60 segundos
        limit: 20, // 20 requisições
    },
]);
```

---

### Environment Variables (ConfigModule)

**Status:** Configurado globalmente

Variáveis de ambiente geridas pelo `@nestjs/config`.

**Ficheiros:**

-   `.env.example` - Template (commit)
-   `.env` - Valores reais (NÃO commit)

**Variáveis disponíveis:**

```bash
# Environment
NODE_ENV=development
PORT=3001
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/orionone

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_EXPIRES_IN=7d

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Meilisearch
MEILISEARCH_HOST=http://localhost:7700
MEILISEARCH_KEY=masterKey

# CORS
FRONTEND_URL=http://localhost:3000

# Email (Mailpit dev)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_FROM=noreply@orionone.local
```

**Uso em serviços:**

```typescript
import { ConfigService } from "@nestjs/config";

@Injectable()
export class AuthService {
    constructor(private config: ConfigService) {}

    getSecret(): string {
        return this.config.get<string>("JWT_SECRET");
    }
}
```

---

### CASL Authorization

**Status:** Configurado com 3 roles

Sistema de autorização baseado em roles (RBAC).

**Roles disponíveis:**

-   `ADMIN` - Acesso total
-   `AGENT` - Gestão de incidents e knowledge base
-   `USER` - Criar e ver próprios incidents

**Permissions matrix:**

```typescript
// ADMIN
can(Action.Manage, "all");

// AGENT
can(Action.Read, "all");
can(Action.Create, "Incident");
can(Action.Update, "Incident");
can(Action.Create, "Comment");
can(Action.Create, "KnowledgeBase");

// USER
can(Action.Read, "Incident");
can(Action.Create, "Incident");
can(Action.Update, "Incident"); // apenas próprios
```

**Uso em serviços:**

```typescript
import { CaslAbilityFactory, Action } from "./casl/casl-ability.factory";

@Injectable()
export class IncidentsService {
    constructor(private casl: CaslAbilityFactory) {}

    async update(user: User, incident: Incident) {
        const ability = this.casl.createForUser(user);

        if (!ability.can(Action.Update, "Incident")) {
            throw new ForbiddenException();
        }
        // proceder com update
    }
}
```

---

### Validation Pipe

**Status:** Configurado globalmente

Validação automática de DTOs usando `class-validator`.

**Configuração:**

-   `whitelist: true` - Remove propriedades não definidas
-   `forbidNonWhitelisted: true` - Rejeita se tiver extras
-   `transform: true` - Transforma tipos automaticamente

**Criar DTO validado:**

```typescript
import {
    IsString,
    IsEmail,
    IsEnum,
    MinLength,
    MaxLength,
} from "class-validator";

export class CreateUserDto {
    @IsEmail()
    email: string;

    @IsString()
    @MinLength(8)
    @MaxLength(128)
    password: string;

    @IsEnum(["ADMIN", "AGENT", "USER"])
    role: string;
}
```

**Erros de validação:**

```json
{
    "statusCode": 400,
    "message": [
        "email must be an email",
        "password must be longer than or equal to 8 characters"
    ],
    "error": "Bad Request"
}
```

---

### Docker Configuration

**Status:** Configurado com 7 services

**Services running:**

```yaml
services:
    postgres: # PostgreSQL 18
    redis: # Redis 7-alpine
    meilisearch: # Meilisearch v1.25
    mailpit: # Email testing
    backend: # Nest.js (development mode)
    frontend: # Next.js (development mode)
    nginx: # Reverse proxy
```

**Comandos úteis:**

```bash
# Iniciar tudo
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart um serviço
docker-compose restart backend

# Parar tudo
docker-compose down

# Parar e remover volumes (CUIDADO: perde dados!)
docker-compose down -v

# Ver status
docker-compose ps

# Entrar num container
docker exec -it orionone-backend sh
docker exec -it orionone-postgres psql -U orionone -d orionone
```

**Health checks:**

```bash
# PostgreSQL
docker exec orionone-postgres pg_isready -U orionone

# Redis
docker exec orionone-redis redis-cli ping

# Backend API
curl http://localhost:3001/api/health

# Frontend
curl http://localhost:3000
```

**Volumes criados:**

-   `postgres_data` - Dados PostgreSQL (persistente)
-   `redis_data` - Dados Redis (persistente)
-   `meilisearch_data` - Índices Meilisearch (persistente)
-   `backend_node_modules` - Dependências backend
-   `backend_uploads` - Ficheiros enviados
-   `frontend_node_modules` - Dependências frontend
-   `frontend_next` - Cache Next.js build

---

## Documentação Completa

Para informação detalhada, consultar:

-   **[Migration Timeline](docs/MIGRATION-PART-4-TIMELINE.md)** - Cronograma de 10 semanas (14 Nov - 31 Jan)
-   **[Architecture](docs/architecture.md)** - Arquitetura Next.js + Nest.js (3-layer, patterns, security)
-   **[Migration Parts 1-5](docs/)** - Setup, Backend, Frontend, Timeline, Cleanup
-   **[MVP Document](docs/MVP.md)** - MVP completo com 39 features
-   **[Requirements](docs/requirements.md)** - Requisitos funcionais e não-funcionais

### Documentação Arquivada (Laravel/Vue)

-   **[Archive](docs/archive-laravel-vue/)** - Documentação completa da implementação Laravel 12 + Vue 3

---

## Próximos Passos

Seguir **[Migration Timeline](docs/MIGRATION-PART-4-TIMELINE.md)** para cronograma completo:

1. **Week 0 (14-15 Nov):** Setup inicial (projects criados, Docker + Nginx, Database + Prisma)
2. **Week 1 (18-22 Nov):** Auth & Users (JWT, CASL, Profile, Avatar)
3. **Week 2 (25-29 Nov):** Tickets Core (CRUD, Status, Priority, Filters)
4. **Week 3-9:** Knowledge Base, Comments, Dashboard, SLA, Teams, Assets
5. **Week 10 (27-31 Jan):** Testing + Cleanup → MVP COMPLETE

**Roadmap completo:** Ver [MVP.md](docs/MVP.md) para features e métricas (ITSM Score: 8.5/10).

---

**Status:** Projetos Next.js + Nest.js criados. Próximo: Week 0 Day 3 (Docker + Nginx).
