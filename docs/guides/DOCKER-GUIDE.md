# Guia Docker - OrionOne ITSM

## Visão Geral

Este guia explica:

1. **Como chegámos ao setup atual** - Evolução da arquitetura Docker
2. **Como funciona** - Estrutura dos containers e networking
3. **Como gerir** - Comandos práticos para operações do dia-a-dia
4. **Como debugar** - Resolução de problemas comuns

---

## Evolução da Arquitetura Docker

### Fase 1: Laravel Monolítico (Antes de Nov 2024)

**Estrutura Original:**

```
docker-compose.yml (Laravel)
 orionone-app (PHP 8.3-FPM)
 orionone-nginx (Nginx)
 orionone-db (PostgreSQL 16)
 orionone-redis (Redis 7)
 orionone-mailpit (Mailpit)
 orionone-meilisearch (Meilisearch)
```

**Problemas:**

- Monolítico difícil de escalar
- Laravel + Vue.js acoplados
- Deploy único para frontend + backend
- Difícil separar equipes de trabalho

### Fase 2: Migração Next.js + Nest.js (Nov 2024 - Atual)

**Estrutura Atual:**

```
docker-compose.yml (Novo)
 orionone-postgres (PostgreSQL 18.0)
 orionone-redis (Redis 8.2)
 orionone-mailpit (Mailpit latest)
 orionone-meilisearch (Meilisearch 1.12)
 orionone-nginx (Nginx reverse proxy)
 orionone-pgadmin (pgAdmin 4) - Opcional
```

**Frontend & Backend:**

- **Next.js** (Frontend): Roda fora do Docker em dev (`npm run dev` no `next-frontend/`)
- **Nest.js** (Backend): Roda fora do Docker em dev (`npm run start:dev` no `nest-backend/`)

**Vantagens:**

- Frontend e backend independentes
- Hot reload rápido (sem rebuild Docker)
- Infraestrutura isolada em containers
- Fácil deployment separado (frontend em Vercel, backend em AWS/Azure)

---

## Arquitetura Docker Atual

### Estrutura de Ficheiros

```
OrionOne/
 docker-compose.yml # ← Orchestração de todos os containers
 .env # ← Variáveis de ambiente Docker

 nest-backend/
 Dockerfile # ← Build do backend (para produção)
 .env # ← Config backend (DATABASE_URL, JWT_SECRET)
 ...

 next-frontend/
 Dockerfile # ← Build do frontend (para produção)
 .env.local # ← Config frontend (NEXT_PUBLIC_API_URL)
 ...
```

---

## Containers Detalhados

### 1. PostgreSQL 18.0 (`orionone-postgres`)

**Propósito:** Base de dados principal

**Configuração:**

```yaml
services:
 orionone-postgres:
 image: postgres:18.0-alpine
 container_name: orionone-postgres
 environment:
 POSTGRES_DB: orionone
 POSTGRES_USER: orionone
 POSTGRES_PASSWORD: secret
 ports:
 - "5432:5432"
 volumes:
 - postgres_data:/var/lib/postgresql/data
 networks:
 - orionone_network
```

**Acesso:**

- **Host:** `localhost`
- **Porta:** `5432`
- **Database:** `orionone`
- **User:** `orionone`
- **Password:** `secret` (definida no `.env`)

**Connection String (Prisma):**

```env
DATABASE_URL="postgresql://orionone:secret@localhost:5432/orionone?schema=public"
```

**Comandos Úteis:**

```bash
# Conectar ao PostgreSQL
docker exec -it orionone-postgres psql -U orionone -d orionone

# Ver tabelas
docker exec -it orionone-postgres psql -U orionone -d orionone -c "\dt"

# Backup da base de dados
docker exec orionone-postgres pg_dump -U orionone orionone > backup.sql

# Restore da base de dados
docker exec -i orionone-postgres psql -U orionone -d orionone < backup.sql

# Ver logs
docker logs orionone-postgres

# Ver logs em tempo real
docker logs -f orionone-postgres
```

---

### 2. Redis 8.2 (`orionone-redis`)

**Propósito:** Cache, sessões, queues (Bull/BullMQ)

**Configuração:**

```yaml
services:
 orionone-redis:
 image: redis:8.2-alpine
 container_name: orionone-redis
 ports:
 - "6379:6379"
 volumes:
 - redis_data:/data
 networks:
 - orionone_network
 command: redis-server --appendonly yes
```

**Acesso:**

- **Host:** `localhost`
- **Porta:** `6379`
- **Sem password** (dev environment)

**Connection String:**

```env
REDIS_URL="redis://localhost:6379"
```

**Comandos Úteis:**

```bash
# Conectar ao Redis CLI
docker exec -it orionone-redis redis-cli

# Ver todas as chaves
docker exec -it orionone-redis redis-cli KEYS '*'

# Ver valor de uma chave
docker exec -it orionone-redis redis-cli GET user:123

# Limpar cache completo
docker exec -it orionone-redis redis-cli FLUSHALL

# Monitorizar comandos em tempo real
docker exec -it orionone-redis redis-cli MONITOR

# Ver info do Redis
docker exec -it orionone-redis redis-cli INFO

# Ver logs
docker logs orionone-redis
```

---

### 3. Mailpit (`orionone-mailpit`)

**Propósito:** Servidor SMTP falso (captura emails em dev)

**Configuração:**

```yaml
services:
 orionone-mailpit:
 image: axllent/mailpit:latest
 container_name: orionone-mailpit
 ports:
 - "1025:1025" # SMTP
 - "8025:8025" # Web UI
 networks:
 - orionone_network
```

**Acesso:**

- **SMTP:** `localhost:1025`
- **Web UI:** [http://localhost:8025](http://localhost:8025)

**Configuração Nest.js:**

```env
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USER=""
MAIL_PASSWORD=""
MAIL_FROM="noreply@orionone.com"
```

**Comandos Úteis:**

```bash
# Abrir Web UI (ver emails)
# Browser: http://localhost:8025

# Ver logs
docker logs orionone-mailpit

# Testar envio de email (via curl)
curl -X POST http://localhost:1025 \
 -H "Content-Type: message/rfc822" \
 --data-binary @test-email.eml
```

---

### 4. Meilisearch 1.12 (`orionone-meilisearch`)

**Propósito:** Motor de pesquisa (full-text search)

**Configuração:**

```yaml
services:
 orionone-meilisearch:
 image: getmeili/meilisearch:v1.12
 container_name: orionone-meilisearch
 environment:
 MEILI_MASTER_KEY: masterKey
 MEILI_ENV: development
 ports:
 - "7700:7700"
 volumes:
 - meilisearch_data:/meili_data
 networks:
 - orionone_network
```

**Acesso:**

- **API:** `http://localhost:7700`
- **Master Key:** `masterKey` (definida no `.env`)

**Configuração Nest.js:**

```env
MEILISEARCH_HOST=http://localhost:7700
MEILISEARCH_KEY=masterKey
```

**Comandos Úteis:**

```bash
# Ver índices
curl http://localhost:7700/indexes \
 -H "Authorization: Bearer masterKey"

# Ver logs
docker logs orionone-meilisearch

# Ver stats
curl http://localhost:7700/stats \
 -H "Authorization: Bearer masterKey"
```

---

### 5. Nginx (`orionone-nginx`) - Opcional

**Propósito:** Reverse proxy (agregar frontend + backend numa porta)

**Configuração:**

```nginx
server {
 listen 80;

 # Frontend (Next.js)
 location / {
 proxy_pass http://host.docker.internal:3000;
 }

 # Backend (Nest.js)
 location /api/ {
 proxy_pass http://host.docker.internal:8000/;
 }
}
```

**Acesso:**

- **URL Unificado:** [http://localhost:80](http://localhost:80)

---

### 6. pgAdmin 4 (`orionone-pgadmin`) - Opcional

**Propósito:** UI gráfica para PostgreSQL

**Configuração:**

```yaml
services:
 orionone-pgadmin:
 image: dpage/pgadmin4:latest
 container_name: orionone-pgadmin
 environment:
 PGADMIN_DEFAULT_EMAIL: admin@orionone.com
 PGADMIN_DEFAULT_PASSWORD: admin
 ports:
 - "5050:80"
 networks:
 - orionone_network
```

**Acesso:**

- **Web UI:** [http://localhost:5050](http://localhost:5050)
- **Email:** `admin@orionone.com`
- **Password:** `admin`

**Configurar Conexão:**

1. Abrir pgAdmin → Add New Server
2. **Name:** OrionOne
3. **Host:** `orionone-postgres` (nome do container)
4. **Port:** `5432`
5. **Username:** `orionone`
6. **Password:** `secret`

---

## Networking

### Rede Docker (`orionone_network`)

Todos os containers estão na mesma rede bridge:

```yaml
networks:
 orionone_network:
 driver: bridge
```

**Comunicação Interna:**

- Containers comunicam pelo **nome do container**
- Exemplo: `orionone-postgres` em vez de `localhost:5432`

**Comunicação Externa (Host):**

- Aplicações fora do Docker (Next.js, Nest.js em dev) usam `localhost`

---

## Volumes

### Persistência de Dados

```yaml
volumes:
 postgres_data: # Dados PostgreSQL
 redis_data: # Dados Redis (AOF)
 meilisearch_data: # Índices Meilisearch
```

**Localização (Windows):**

```
C:\ProgramData\docker\volumes\orionone_postgres_data
C:\ProgramData\docker\volumes\orionone_redis_data
C:\ProgramData\docker\volumes\orionone_meilisearch_data
```

**Comandos Úteis:**

```bash
# Listar volumes
docker volume ls

# Ver detalhes de um volume
docker volume inspect orionone_postgres_data

# Remover volume (CUIDADO: apaga dados!)
docker volume rm orionone_postgres_data

# Backup de um volume
docker run --rm \
 -v orionone_postgres_data:/data \
 -v $(pwd):/backup \
 alpine tar czf /backup/postgres_backup.tar.gz /data
```

---

## Comandos de Gestão

### Ciclo de Vida dos Containers

```bash
# Iniciar todos os containers
docker-compose up -d

# Iniciar containers específicos
docker-compose up -d orionone-postgres orionone-redis

# Ver status
docker-compose ps

# Ver logs de todos os containers
docker-compose logs

# Ver logs de um container específico
docker-compose logs orionone-postgres

# Ver logs em tempo real
docker-compose logs -f

# Parar todos os containers
docker-compose stop

# Parar container específico
docker-compose stop orionone-postgres

# Reiniciar containers
docker-compose restart

# Parar e remover containers (mantém volumes)
docker-compose down

# Remover containers + volumes (CUIDADO: apaga dados!)
docker-compose down -v
```

---

### Rebuild e Cache

```bash
# Rebuild de todos os containers
docker-compose build

# Rebuild sem usar cache
docker-compose build --no-cache

# Rebuild e iniciar
docker-compose up -d --build

# Rebuild de um serviço específico
docker-compose build orionone-postgres
```

---

### Inspeção e Debug

```bash
# Entrar no container (shell interativa)
docker exec -it orionone-postgres sh

# Executar comando único
docker exec orionone-postgres ls -la /var/lib/postgresql/data

# Ver processos em execução num container
docker top orionone-postgres

# Ver estatísticas de recursos (CPU, RAM)
docker stats

# Ver configuração de um container
docker inspect orionone-postgres

# Ver IPs dos containers
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' orionone-postgres
```

---

### Limpeza

```bash
# Remover containers parados
docker container prune

# Remover imagens não usadas
docker image prune

# Remover volumes não usados
docker volume prune

# Remover redes não usadas
docker network prune

# Limpeza completa (CUIDADO!)
docker system prune -a --volumes
```

---

## Resolução de Problemas

### Problema 1: Container não inicia

**Sintomas:**

```bash
$ docker-compose ps
orionone-postgres Exit 1
```

**Diagnóstico:**

```bash
# Ver logs de erro
docker-compose logs orionone-postgres

# Ver últimas 50 linhas
docker-compose logs --tail=50 orionone-postgres
```

**Soluções Comuns:**

1. **Porta já em uso:**

 ```bash
 # Windows
 netstat -ano | findstr :5432

 # Linux/Mac
 lsof -i :5432

 # Mudar porta no docker-compose.yml:
 ports:
 - "5433:5432" # Usa 5433 em vez de 5432
 ```

2. **Volume corrompido:**

 ```bash
 docker-compose down -v
 docker volume rm orionone_postgres_data
 docker-compose up -d
 ```

3. **Falta de recursos (RAM/CPU):**
 - Docker Desktop → Settings → Resources
 - Aumentar RAM (mínimo 4GB)

---

### Problema 2: "Connection refused" no Nest.js

**Sintomas:**

```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**Diagnóstico:**

```bash
# Verificar se PostgreSQL está a correr
docker ps | grep postgres

# Testar conexão manualmente
docker exec -it orionone-postgres psql -U orionone -d orionone
```

**Soluções:**

1. **Container não está a correr:**

 ```bash
 docker-compose up -d orionone-postgres
 ```

2. **Connection string errada:**

 ```env
 # nest-backend/.env
 DATABASE_URL="postgresql://orionone:secret@localhost:5432/orionone?schema=public"
 # ↑ Deve ser localhost (não orionone-postgres)
 ```

3. **Prisma não gerou cliente:**
 ```bash
 cd nest-backend
 npx prisma generate
 ```

---

### Problema 3: Emails não aparecem no Mailpit

**Sintomas:**

- Backend envia email
- Mailpit UI vazia ([http://localhost:8025](http://localhost:8025))

**Diagnóstico:**

```bash
# Ver logs do Mailpit
docker logs orionone-mailpit

# Ver logs do Nest.js
cd nest-backend
npm run start:dev
# Procurar por erros de SMTP
```

**Soluções:**

1. **Configuração errada:**

 ```env
 # nest-backend/.env
 MAIL_HOST=localhost
 MAIL_PORT=1025
 MAIL_USER="" # Vazio
 MAIL_PASSWORD="" # Vazio
 ```

2. **Container Mailpit não está a correr:**

 ```bash
 docker-compose up -d orionone-mailpit
 ```

3. **Nest.js não configurado:**
 ```typescript
 // nest-backend/src/app.module.ts
 MailerModule.forRoot({
 transport: {
 host: process.env.MAIL_HOST,
 port: parseInt(process.env.MAIL_PORT),
 ignoreTLS: true, // ← Importante para Mailpit
 },
 }),
 ```

---

### Problema 4: Redis não guarda sessões

**Sintomas:**

- Login funciona mas logout imediato
- Sessões não persistem

**Diagnóstico:**

```bash
# Ver se Redis tem dados
docker exec -it orionone-redis redis-cli KEYS '*'

# Ver logs
docker logs orionone-redis
```

**Soluções:**

1. **Redis não está a guardar (AOF desativado):**

 ```yaml
 # docker-compose.yml
 command: redis-server --appendonly yes
 ```

2. **Nest.js não usa Redis:**

 ```typescript
 // nest-backend/src/app.module.ts
 import { CacheModule } from '@nestjs/cache-manager';
 import * as redisStore from 'cache-manager-redis-store';

 CacheModule.register({
 isGlobal: true,
 store: redisStore,
 host: 'localhost',
 port: 6379,
 }),
 ```

---

### Problema 5: Meilisearch não indexa

**Sintomas:**

- Pesquisa não retorna resultados
- Índices vazios

**Diagnóstico:**

```bash
# Ver índices
curl http://localhost:7700/indexes \
 -H "Authorization: Bearer masterKey"

# Ver logs
docker logs orionone-meilisearch
```

**Soluções:**

1. **Master key errada:**

 ```env
 # nest-backend/.env
 MEILISEARCH_HOST=http://localhost:7700
 MEILISEARCH_KEY=masterKey
 ```

2. **Nest.js não configurado:**

 ```typescript
 // nest-backend/src/app.module.ts
 import { MeiliSearchModule } from 'nestjs-meilisearch';

 MeiliSearchModule.forRoot({
 host: process.env.MEILISEARCH_HOST,
 apiKey: process.env.MEILISEARCH_KEY,
 }),
 ```

---

## Workflows Comuns

### Workflow 1: Primeira Vez (Fresh Setup)

```bash
# 1. Iniciar Docker
docker-compose up -d

# 2. Verificar containers
docker-compose ps

# 3. Setup Backend
cd nest-backend
npm install
npx prisma generate
npx prisma migrate dev
npx prisma db seed
npm run start:dev

# 4. Setup Frontend (outra terminal)
cd next-frontend
npm install
npm run dev

# 5. Verificar
# - Backend: http://localhost:8000/api/health
# - Frontend: http://localhost:3000
# - Mailpit: http://localhost:8025
```

---

### Workflow 2: Dia-a-Dia (Desenvolvimento)

```bash
# 1. Iniciar Docker (se não estiver a correr)
docker-compose up -d

# 2. Iniciar Backend
cd nest-backend
npm run start:dev

# 3. Iniciar Frontend (outra terminal)
cd next-frontend
npm run dev

# 4. Trabalhar normalmente
# Hot reload funciona automaticamente

# 5. No fim do dia (opcional)
docker-compose stop
```

---

### Workflow 3: Reset Completo (Problemas)

```bash
# 1. Parar tudo
docker-compose down -v

# 2. Limpar volumes
docker volume prune

# 3. Rebuild
docker-compose build --no-cache
docker-compose up -d

# 4. Reset Backend
cd nest-backend
rm -rf node_modules
npm install
npx prisma generate
npx prisma migrate reset # ← Apaga DB e recria
npx prisma db seed

# 5. Reset Frontend
cd next-frontend
rm -rf node_modules .next
npm install
```

---

### Workflow 4: Backup & Restore

**Backup:**

```bash
# 1. Backup PostgreSQL
docker exec orionone-postgres pg_dump -U orionone orionone > backup_$(date +%Y%m%d).sql

# 2. Backup Redis (se necessário)
docker exec orionone-redis redis-cli --rdb /data/dump.rdb
docker cp orionone-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb

# 3. Backup Meilisearch
docker cp orionone-meilisearch:/meili_data ./meilisearch_backup_$(date +%Y%m%d)
```

**Restore:**

```bash
# 1. Restore PostgreSQL
docker exec -i orionone-postgres psql -U orionone -d orionone < backup_20241114.sql

# 2. Restore Redis
docker cp redis_backup_20241114.rdb orionone-redis:/data/dump.rdb
docker-compose restart orionone-redis

# 3. Restore Meilisearch
docker cp meilisearch_backup_20241114 orionone-meilisearch:/meili_data
docker-compose restart orionone-meilisearch
```

---

## Produção vs Desenvolvimento

### Diferenças

| Aspecto | Desenvolvimento | Produção |
| ------------------- | --------------------------------- | --------------------------------- |
| **Frontend** | `npm run dev` (fora do Docker) | Container Docker + Nginx |
| **Backend** | `npm run start:dev` (fora Docker) | Container Docker |
| **PostgreSQL** | Container Docker | Container Docker + Volume externo |
| **Redis** | Container Docker | Container Docker + AOF |
| **Mailpit** | Container Docker (captura emails) | Não usado (SMTP real) |
| **Meilisearch** | Container Docker | Container Docker + Volume externo |
| **Hot Reload** | Sim | Não |
| **Secrets** | `.env` files | Azure Key Vault / AWS Secrets |
| **Health Checks** | Opcional | Obrigatório |
| **Resource Limits** | Não definido | CPU/RAM limits |

### docker-compose.prod.yml (Exemplo)

```yaml
version: "3.8"

services:
 orionone-backend:
 build:
 context: ./nest-backend
 dockerfile: Dockerfile
 container_name: orionone-backend-prod
 environment:
 NODE_ENV: production
 DATABASE_URL: ${DATABASE_URL}
 JWT_SECRET: ${JWT_SECRET}
 REDIS_URL: redis://orionone-redis:6379
 ports:
 - "8000:8000"
 depends_on:
 - orionone-postgres
 - orionone-redis
 networks:
 - orionone_network
 restart: always
 deploy:
 resources:
 limits:
 cpus: "2"
 memory: 2G

 orionone-frontend:
 build:
 context: ./next-frontend
 dockerfile: Dockerfile
 container_name: orionone-frontend-prod
 environment:
 NEXT_PUBLIC_API_URL: https://api.orionone.com
 ports:
 - "3000:3000"
 networks:
 - orionone_network
 restart: always
 deploy:
 resources:
 limits:
 cpus: "1"
 memory: 1G

 orionone-postgres:
 image: postgres:18.0-alpine
 container_name: orionone-postgres-prod
 environment:
 POSTGRES_DB: ${POSTGRES_DB}
 POSTGRES_USER: ${POSTGRES_USER}
 POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
 volumes:
 - /mnt/data/postgres:/var/lib/postgresql/data
 networks:
 - orionone_network
 restart: always
 deploy:
 resources:
 limits:
 cpus: "2"
 memory: 4G

 orionone-redis:
 image: redis:8.2-alpine
 container_name: orionone-redis-prod
 command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
 volumes:
 - /mnt/data/redis:/data
 networks:
 - orionone_network
 restart: always
 deploy:
 resources:
 limits:
 cpus: "1"
 memory: 1G

 orionone-nginx:
 image: nginx:alpine
 container_name: orionone-nginx-prod
 volumes:
 - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
 - ./nginx/ssl:/etc/nginx/ssl:ro
 ports:
 - "80:80"
 - "443:443"
 depends_on:
 - orionone-frontend
 - orionone-backend
 networks:
 - orionone_network
 restart: always

networks:
 orionone_network:
 driver: bridge

volumes:
 postgres_data:
 redis_data:
```

**Deploy em produção:**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Checklist de Manutenção

### Diário

- [ ] Verificar containers a correr: `docker-compose ps`
- [ ] Ver logs de erros: `docker-compose logs --tail=100`

### Semanal

- [ ] Backup PostgreSQL: `docker exec orionone-postgres pg_dump`
- [ ] Verificar uso de disco: `docker system df`
- [ ] Limpar recursos: `docker system prune`

### Mensal

- [ ] Atualizar imagens: `docker-compose pull && docker-compose up -d`
- [ ] Verificar volumes órfãos: `docker volume ls`
- [ ] Testar restore de backup

---

## Recursos

### Documentação Oficial

- **Docker:** [docs.docker.com](https://docs.docker.com/)
- **Docker Compose:** [docs.docker.com/compose](https://docs.docker.com/compose/)
- **PostgreSQL:** [postgresql.org/docs](https://www.postgresql.org/docs/)
- **Redis:** [redis.io/docs](https://redis.io/docs/)
- **Meilisearch:** [docs.meilisearch.com](https://docs.meilisearch.com/)

### Ferramentas

- **Portainer:** UI gráfica para gerir Docker - [portainer.io](https://www.portainer.io/)
- **Lazydocker:** TUI para Docker - [github.com/jesseduffield/lazydocker](https://github.com/jesseduffield/lazydocker)
- **ctop:** Monitor de containers - [github.com/bcicen/ctop](https://github.com/bcicen/ctop)

---

## Próximos Passos

Depois de dominares este guia:

1. Lê o [SETUP.md](../SETUP.md) para setup inicial
2. Lê o [sprint1-guide.md](sprint1-guide.md) para começar implementação
3. Lê o [DEPLOYMENT.md](../DEPLOYMENT.md) para deploy em produção
