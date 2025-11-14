# Guia de Implementação Detalhado do Sprint 0: Setup & Configuração do Ambiente

## Visão Geral do Sprint

**Objetivo:**
Configurar ambiente de desenvolvimento completo e inicializar base de dados PostgreSQL com Prisma ORM.

**User Stories:**

- [Concluído] US0.1: Configurar Variáveis de Ambiente
- [Concluído] US0.2: Configurar Meilisearch Master Key
- [Em Curso] US0.3: Gerar Prisma Client e Tipos TypeScript
- [Em Curso] US0.4: Executar Migrations de Base de Dados
- [Em Curso] US0.5: Popular BD com Dados Iniciais (Seed)

**Pré-requisitos:**
Docker e Docker Compose instalados, containers a correr (`docker-compose ps`)

---

## Funcionalidade 0.1, 0.2: Configuração de Ambiente ( CONCLUÍDO)

### Status Atual

 **Ficheiro `.env` criado** (copiado de `.env.example`)
 **JWT_SECRET atualizado** com chave segura (48 caracteres alfanuméricos)
 **Meilisearch master key** configurada no `docker-compose.yml`

### Validação da Configuração

**Comando:**

```bash
# Verificar ficheiro .env existe
Test-Path .env

# Ver JWT_SECRET configurado
Select-String "JWT_SECRET" .env

# Verificar containers a correr
docker-compose ps
```

**Output Esperado:**

```
 orionone-postgres (healthy)
 orionone-redis (healthy)
 orionone-meilisearch (healthy)
 orionone-mailpit (healthy)
 orionone-backend (healthy)
 orionone-frontend (healthy)
 orionone-nginx (running)
```

---

## Funcionalidade 0.3: Prisma Client (Geração de Tipos TypeScript)

### Fase 1: Gerar Prisma Client

#### 1.1. Aceder ao Container Backend

**Comando:**

```bash
docker exec -it orionone-backend sh
```

**Descrição:**
Entra no shell do container backend onde o Prisma está instalado.

#### 1.2. Executar Geração do Cliente

**Comando:**

```bash
npm run prisma:generate
```

**Objetivo:**
Gera o Prisma Client baseado no schema definido em `prisma/schema.prisma`, criando tipos TypeScript para todos os 15 modelos.

**Output Esperado:**

```
 Generated Prisma Client (6.19.0)
 Generated 15 models:
 - User
 - Ticket
 - Comment
 - Category
 - Priority
 - Status
 - Team
 - TeamMember
 - Article
 - Asset
 - Tag
 - ArticleTag
 - Notification
 - ActivityLog
 - Attachment
```

**Documentação:**
[Guia Oficial do Prisma sobre Client Generation](https://www.prisma.io/docs/concepts/components/prisma-client/working-with-prismaclient/generating-prisma-client)

#### 1.3. Validar Geração

**Comando:**

```bash
ls -la node_modules/.prisma/client
```

**Descrição:**
Verifica que os ficheiros TypeScript foram gerados corretamente.

**Output Esperado:**

```
index.d.ts
index.js
package.json
runtime/
```

**Troubleshooting:**

- **Erro "DATABASE_URL not found"**

 - **Solução:** Verificar que ficheiro `.env` existe na raiz do projeto
 - **Comando:** `ls -la /app/.env`

- **Erro de conexão PostgreSQL**

 - **Solução:** Verificar que postgres está healthy
 - **Comando:** `docker-compose ps postgres`

- **`npm: not found`**
 - **Solução:** Sair e reentrar no container
 - **Comando:** `exit` e depois `docker exec -it orionone-backend sh`

---

## Funcionalidade 0.4: Migrations de Base de Dados

### Fase 2: Executar Migrations (Criar Tabelas)

#### 2.1. Executar Migração Inicial

**Comando:**

```bash
npm run prisma:migrate
```

**Quando Pedir Nome:**

```
? Enter a name for the new migration: › init_database
```

**Objetivo:**
Cria estrutura completa de 15 tabelas no PostgreSQL baseado no schema Prisma.

**Output Esperado:**

```
 Generated Prisma Client (6.19.0)

The following migration(s) have been created and applied from new schema changes:

migrations/
 20251114123456_init_database/
 migration.sql

 Applied migration init_database
 Created 15 tables:
 - users
 - tickets
 - comments
 - categories
 - priorities
 - statuses
 - teams
 - team_members
 - articles
 - assets
 - tags
 - article_tags
 - notifications
 - activity_logs
 - attachments
```

**Documentação:**
[Guia Oficial do Prisma sobre Migrations](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)

#### 2.2. Validar Migrations Criadas

**Comando:**

```bash
ls -la prisma/migrations
```

**Descrição:**
Lista as migrations aplicadas à base de dados.

**Output Esperado:**

```
20251114123456_init_database/
 migration.sql
```

#### 2.3. Abrir Prisma Studio (Opcional)

**Comando:**

```bash
npm run prisma:studio
```

**Descrição:**
Abre interface web para visualizar e editar dados da base de dados.

**Acesso:**
http://localhost:5555

**Validação:**

- Ver 15 tabelas listadas no painel esquerdo
- Todas as tabelas vazias (0 registos)

**Troubleshooting:**

- **"Migration failed"**

 - **Causa:** Erro de conexão ou schema inválido
 - **Solução:** Ver logs do postgres: `docker logs orionone-postgres`

- **"Already applied"**

 - **Causa:** Migration já foi executada
 - **Solução:** Normal, pode ignorar ou usar `prisma:migrate reset` para recomeçar

- **Erro de permissões**
 - **Causa:** DATABASE_URL com credenciais incorretas
 - **Solução:** Verificar `.env` → `DATABASE_URL="postgresql://orionone:secret@postgres:5432/orionone"`

---

## Funcionalidade 0.5: Seed Data (Popular Base de Dados)

### Fase 3: Inserir Dados Iniciais

#### 3.1. Executar Script de Seed

**Comando:**

```bash
npm run prisma:seed
```

**Objetivo:**
Insere dados iniciais necessários para desenvolvimento e testes.

**Output Esperado:**

```
 Seeding database...

Creating users...
 Created 5 users (admin, agent, user, manager, tech)

Creating categories...
 Created 8 categories (Hardware, Software, Network, Security, Database, Cloud, Support, Other)

Creating priorities...
 Created 5 priorities (Critical, High, Medium, Low, Planning)

Creating statuses...
 Created 7 statuses (New, Open, In Progress, Pending, Resolved, Closed, Cancelled)

Creating teams...
 Created 3 teams (IT Support, Infrastructure, Security)

Creating teams...
 Created 3 teams (IT Support, Infrastructure, Security)

Creating sample tickets...
 Created 10 tickets with realistic data

Creating sample articles...
 Created 15 knowledge base articles

Database seeded successfully! 
```

**Documentação:**
[Guia Oficial do Prisma sobre Seeding](https://www.prisma.io/docs/orm/prisma-migrate/workflows/seeding)

#### 3.2. Dados Criados no Seed

**Tabela: users (5 registos)**

| Email | Password | Role | Descrição |
| -------------------- | ---------- | ------- | ------------------------- |
| admin@orionone.com | admin123 | ADMIN | Administrador do sistema |
| agent@orionone.com | agent123 | AGENT | Agente de suporte técnico |
| user@orionone.com | user123 | USER | Utilizador normal |
| manager@orionone.com | manager123 | MANAGER | Gestor de equipa |
| tech@orionone.com | tech123 | AGENT | Técnico de infraestrutura |

**Tabela: categories (8 registos)**

- Hardware, Software, Network, Security, Database, Cloud, Support, Other

**Tabela: priorities (5 registos)**

- Critical (P1), High (P2), Medium (P3), Low (P4), Planning (P5)

**Tabela: statuses (7 registos)**

- New, Open, In Progress, Pending, Resolved, Closed, Cancelled

**Tabela: teams (3 registos)**

- IT Support (2 membros)
- Infrastructure (2 membros)
- Security (1 membro)

**Tabela: tickets (10 registos)**

- Tickets de teste com diferentes status, prioridades e categorias
- Dados realistas para desenvolvimento

**Tabela: articles (15 registos)**

- Artigos de knowledge base
- Categorias variadas
- Conteúdo exemplo

#### 3.3. Validar Dados com Prisma Studio

**Comando:**

```bash
npm run prisma:studio
```

**Acesso:**
http://localhost:5555

**Checklist de Validação:**

- [ ] Tabela `users` tem 5 registos
- [ ] Tabela `categories` tem 8 registos
- [ ] Tabela `priorities` tem 5 registos
- [ ] Tabela `statuses` tem 7 registos
- [ ] Tabela `teams` tem 3 registos
- [ ] Tabela `tickets` tem 10 registos
- [ ] Tabela `articles` tem 15 registos

**Troubleshooting:**

- **"Seed failed"**

 - **Causa:** Migrations não foram executadas
 - **Solução:** Executar `npm run prisma:migrate` primeiro

- **Erro "Unique constraint"**

 - **Causa:** Seed já foi executado anteriormente
 - **Solução:** Limpar BD: `npm run prisma:migrate reset` (CUIDADO: apaga tudo!)

- **Script não encontrado**
 - **Causa:** Ficheiro `prisma/seed.ts` não existe
 - **Solução:** Verificar que o ficheiro existe no projeto

---

## Fase 4: Validação Completa do Setup

### 4.1. Testes de Conectividade dos Serviços

#### 4.1.1. Backend API (Nest.js)

**Comando:**

```bash
curl http://localhost:3001/api/health
```

**Output Esperado:**

```json
{
 "status": "ok",
 "timestamp": "2025-11-14T17:30:00.000Z",
 "database": "connected",
 "redis": "connected"
}
```

**Documentação:**
[Nest.js Health Checks](https://docs.nestjs.com/recipes/terminus)

#### 4.1.2. Frontend (Next.js)

**Comando:**

```bash
# Abrir no browser
Start-Process "http://localhost:3000"
```

**Validação:**

- Página inicial Next.js carrega sem erros
- Console do browser sem erros críticos

**Documentação:**
[Next.js Production Checklist](https://nextjs.org/docs/pages/building-your-application/deploying/production-checklist)

#### 4.1.3. PostgreSQL (Database)

**Comando:**

```bash
# Dentro do container backend
npx prisma db pull
```

**Output Esperado:**

```
Prisma schema loaded from prisma/schema.prisma
Datasource "db": PostgreSQL database "orionone", schema "public"

Introspecting based on datasource defined in prisma/schema.prisma …

 Introspected 15 models and wrote them into prisma/schema.prisma in 123ms
```

**Documentação:**
[Prisma DB Pull](https://www.prisma.io/docs/reference/api-reference/command-reference#db-pull)

#### 4.1.4. Redis (Cache)

**Comando:**

```bash
docker exec -it orionone-redis redis-cli PING
```

**Output Esperado:**

```
PONG
```

**Documentação:**
[Redis CLI Commands](https://redis.io/docs/manual/cli/)

#### 4.1.5. Meilisearch (Search Engine)

**Comando:**

```bash
curl http://localhost:7700/health
```

**Output Esperado:**

```json
{
 "status": "available"
}
```

**Documentação:**
[Meilisearch Health Check](https://docs.meilisearch.com/reference/api/health.html)

#### 4.1.6. Mailpit (Email Testing)

**Comando:**

```bash
# Abrir Web UI
Start-Process "http://localhost:8025"
```

**Validação:**

- Interface Mailpit carrega
- Dashboard mostra 0 emails (inicial)

**Documentação:**
[Mailpit Documentation](https://github.com/axllent/mailpit)

### 4.2. Checklist Final de Validação

**Serviços Acessíveis:**

- [ ] Backend API: http://localhost:3001/api/health → 200 OK
- [ ] Frontend: http://localhost:3000 → Página carrega
- [ ] Prisma Studio: http://localhost:5555 → Interface acessível
- [ ] Mailpit: http://localhost:8025 → Dashboard carrega
- [ ] Meilisearch: http://localhost:7700/health → status: available
- [ ] Nginx Proxy: http://localhost:80 → Redireciona corretamente

**Containers Health:**

```bash
docker-compose ps
```

- [ ] orionone-postgres: (healthy)
- [ ] orionone-redis: (healthy)
- [ ] orionone-meilisearch: (healthy)
- [ ] orionone-mailpit: (healthy)
- [ ] orionone-backend: (healthy)
- [ ] orionone-frontend: (healthy)
- [ ] orionone-nginx: (running)

**Base de Dados:**

- [ ] Prisma Client gerado (`node_modules/.prisma/client` existe)
- [ ] Migrations executadas (`prisma/migrations/` contém init_database)
- [ ] Seed data inserido (5 users, 8 categories, 10 tickets, 15 articles)

---

## Troubleshooting Comum

### Container Não Inicia

**Sintoma:**
Container em estado "Exited" ou "Restarting"

**Diagnóstico:**

```bash
# Ver logs do container
docker logs orionone-backend --tail 50
docker logs orionone-postgres --tail 50
```

**Soluções:**

```bash
# Reiniciar containers
docker-compose restart backend postgres

# Se persistir, recriar containers
docker-compose down
docker-compose up -d
```

### Erro de Conexão à Base de Dados

**Sintoma:**
`Error: P1001: Can't reach database server at postgres:5432`

**Diagnóstico:**

```bash
# Verificar DATABASE_URL no .env
cat .env | Select-String "DATABASE_URL"

# Deve ser: postgresql://orionone:secret@postgres:5432/orionone
```

**Solução:**

```bash
# Testar conexão PostgreSQL direta
docker exec -it orionone-postgres psql -U orionone -d orionone -c "\dt"

# Deve listar 15 tabelas
```

### Prisma Client Desatualizado

**Sintoma:**
Erros de tipos TypeScript ou "Prisma Client not found"

**Solução:**

```bash
# Regenerar Prisma Client
docker exec -it orionone-backend npm run prisma:generate

# Reiniciar backend
docker-compose restart backend
```

### Migrations com Conflitos

**Sintoma:**
`Error: Migration failed to apply` ou tabelas duplicadas

**Solução (CUIDADO: Apaga tudo!):**

```bash
# Reset completo da database
docker exec -it orionone-backend npm run prisma:migrate reset

# Reexecutar migrations
docker exec -it orionone-backend npm run prisma:migrate

# Reexecutar seed
docker exec -it orionone-backend npm run prisma:seed
```

### Node Modules Corrompidos

**Sintoma:**
Erros de dependências ou packages não encontrados

**Solução:**

```bash
# Limpar volumes e reinstalar
docker-compose down
docker volume rm orionone_backend_node_modules
docker-compose up -d backend

# Backend reinstala dependências automaticamente
```

### Portas Já em Uso

**Sintoma:**
`Error: Port 3001 is already in use`

**Diagnóstico:**

```bash
# Ver processos usando portas
netstat -ano | Select-String "3001|3000|5432|6379|7700"
```

**Solução:**

```bash
# Parar processos ou mudar portas no docker-compose.yml
# Exemplo: "3002:3001" em vez de "3001:3001"
```

---

## Estado Final Esperado

### Containers Ativos

```
NAME STATUS PORTS
orionone-postgres Up 5 minutes (healthy) 0.0.0.0:5432->5432/tcp
orionone-redis Up 5 minutes (healthy) 0.0.0.0:6379->6379/tcp
orionone-meilisearch Up 5 minutes (healthy) 0.0.0.0:7700->7700/tcp
orionone-mailpit Up 5 minutes (healthy) 0.0.0.0:1025->1025/tcp, 0.0.0.0:8025->8025/tcp
orionone-backend Up 5 minutes (healthy) 0.0.0.0:3001->3001/tcp
orionone-frontend Up 5 minutes (healthy) 0.0.0.0:3000->3000/tcp
orionone-nginx Up 5 minutes 0.0.0.0:80->80/tcp
```

### Base de Dados Populada

```sql
SELECT
 'users' as table_name, COUNT(*) as records FROM users
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'priorities', COUNT(*) FROM priorities
UNION ALL
SELECT 'statuses', COUNT(*) FROM statuses
UNION ALL
SELECT 'teams', COUNT(*) FROM teams
UNION ALL
SELECT 'tickets', COUNT(*) FROM tickets
UNION ALL
SELECT 'articles', COUNT(*) FROM articles;

-- Output esperado:
-- users: 5
-- categories: 8
-- priorities: 5
-- statuses: 7
-- teams: 3
-- tickets: 10
-- articles: 15
```

### Volumes Docker

```bash
docker volume ls

# Output esperado (8 volumes):
orionone_postgres_data
orionone_redis_data
orionone_meilisearch_data
orionone_backend_node_modules
orionone_backend_uploads
orionone_frontend_node_modules
orionone_frontend_next
fe01bb2648b6... (volume automático postgres)
```

---

## Próximos Passos

### Commit das Alterações

**Comando:**

```bash
git add .env docker-compose.yml prisma/migrations
git commit -m "chore: complete Sprint 0 - environment setup and database initialization"
git push origin feat/migrate-nextjs-nestjs
```

### Iniciar Sprint 1

Após concluir Sprint 0 com sucesso, estás pronto para:

**Sprint 1: Authentication Module**

- Implementar JWT authentication
- Criar guards e decorators
- Sistema de permissões (RBAC)
- Login/Logout/Register endpoints
- Protected routes no frontend

**Duração Estimada**: 2-3 dias

---

## Referências Técnicas

### Prisma

- [Prisma Docs](https://www.prisma.io/docs)
- [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client)
- [Prisma Seeding](https://www.prisma.io/docs/guides/database/seed-database)
- [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)

### Nest.js

- [Nest.js Docs](https://docs.nestjs.com)
- [Prisma + Nest.js Integration](https://docs.nestjs.com/recipes/prisma)
- [Nest.js Health Checks](https://docs.nestjs.com/recipes/terminus)
- [Nest.js Configuration](https://docs.nestjs.com/techniques/configuration)

### Next.js

- [Next.js Docs](https://nextjs.org/docs)
- [Next.js App Router](https://nextjs.org/docs/app)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)

### Docker

- [Docker Compose](https://docs.docker.com/compose)
- [Docker Volumes](https://docs.docker.com/storage/volumes)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)

### PostgreSQL

- [PostgreSQL 18 Docs](https://www.postgresql.org/docs/18/)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)

### Redis

- [Redis Documentation](https://redis.io/docs/)
- [Redis CLI](https://redis.io/docs/manual/cli/)

### Meilisearch

- [Meilisearch Docs](https://docs.meilisearch.com/)
- [Meilisearch API Reference](https://docs.meilisearch.com/reference/api/)

---

## Checklist de Conclusão do Sprint 0

Antes de começar Sprint 1, confirma que completaste:

**Ambiente:**

- [ ] Ficheiro `.env` configurado
- [ ] JWT_SECRET com 32+ caracteres
- [ ] Todos os containers a correr e healthy

**Prisma:**

- [ ] Prisma Client gerado (`npm run prisma:generate`)
- [ ] Migrations executadas (`npm run prisma:migrate`)
- [ ] Seed data inserido (`npm run prisma:seed`)
- [ ] Prisma Studio funciona (`npm run prisma:studio`)

**Validação:**

- [ ] Backend API responde: `curl localhost:3001/api/health` → 200 OK
- [ ] Frontend carrega: http://localhost:3000
- [ ] Database tem dados: 5 users, 8 categories, 10 tickets, 15 articles
- [ ] Redis responde: `docker exec orionone-redis redis-cli PING` → PONG
- [ ] Meilisearch healthy: `curl localhost:7700/health` → available

**Git:**

- [ ] Alterações commitadas: `git commit -m "chore: Sprint 0 complete"`
- [ ] Branch pushed: `git push origin feat/migrate-nextjs-nestjs`

---

**Sprint 0 Concluído!** 

**Tempo Total**: ~30 minutos
**Próximo**: **Sprint 1 - Authentication Module** (2-3 dias)

**Ready to Code!** 
