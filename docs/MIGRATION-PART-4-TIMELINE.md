# 🗓️ Migração Next.js + Nest.js - PARTE 4: Timeline & Execution

**Deadline:** 31 de Janeiro 2025 (10 semanas)
**Data Início:** 13 de Novembro 2024
**Dias Disponíveis:** 70 dias (10 semanas)

---

## 📊 OVERVIEW DO PROJETO

### Scope Total

**Features a Migrar:** 39 funcionalidades (7 Sprints do Laravel)
**Código Atual:** ~15,000 linhas (Laravel + Vue)
**Código Novo:** ~11,000 linhas (Nest.js + Next.js) = **37% redução**
**Complexidade:** Alta (Auth, RBAC, ITSM workflows, CMDB, Reports)

---

### Success Criteria

✅ **Funcional:**

-   Todos os 39 features dos 7 Sprints implementados
-   Auth + RBAC (JWT + CASL) funcionando
-   Tickets CRUD com SLA automation
-   Knowledge Base com search (Meilisearch)
-   Assets CMDB completo
-   Reports com gráficos (Recharts)

✅ **Qualidade:**

-   80%+ test coverage (Jest + Playwright)
-   Zero security vulnerabilities (CVE checks)
-   API documentation completa (Swagger)
-   Performance: <200ms median API response time

✅ **Deploy:**

-   Docker Compose production-ready
-   CI/CD pipeline (GitHub Actions)
-   Error tracking (Sentry)
-   Demo video (5-10min)

---

## 🏗️ ESTRATÉGIA DE MIGRAÇÃO

### Approach: Big Bang Migration (NOT Incremental)

**Justificativa:**

-   Projeto em estado inicial (18% completo)
-   Stack totalmente diferente (incompatível com gradual migration)
-   Deadline apertado (não há tempo para manter 2 sistemas)
-   Sem produção ativa (não há usuários dependentes)

**Processo:**

1. ✅ Completar Sprint 1 no Laravel (DONE)
2. 📦 Criar backup/tag: `v0.1.0-laravel`
3. 🚀 Migrar tudo de uma vez (10 semanas)
4. 🎯 Entregar projeto final em Next.js + Nest.js

---

### Risk Mitigation

**Risk 1: Learning Curve** (Nest.js + Next.js 15 App Router)
→ **Mitigation:** Week 0 dedicada a tutoriais oficiais, buffer time na Week 9

**Risk 2: Unexpected Bugs** (integração PostgreSQL + Prisma)
→ **Mitigation:** Testar Prisma migrations no Week 1, smoke tests diários

**Risk 3: Complex Features** (SLA calculation, role-based filtering)
→ **Mitigation:** Já temos código Nest.js pronto na Part 2! Copy-paste adaptado

**Risk 4: Docker Issues** (Nest.js + Next.js containers)
→ **Mitigation:** Reutilizar 100% do docker-compose.yml (só trocar app image)

**Risk 5: Scope Creep** (adicionar features não planejadas)
→ **Mitigation:** Strict scope: replicar exatamente o Laravel MVP, não inovar

---

## 📅 DETAILED TIMELINE (10 WEEKS)

---

### **WEEK 0: Setup & Foundations** (Nov 13-16, 2024) — 4 dias

**Objetivo:** Preparar ambiente, estudar docs oficiais, criar projetos base

#### Day 1 (13 Nov): Research & Tutorials

-   [ ] Assistir Nest.js Crash Course (30min): https://docs.nestjs.com/first-steps
-   [ ] Ler Prisma Quickstart (20min): https://www.prisma.io/docs/getting-started
-   [ ] Next.js 15 App Router Tutorial (40min): https://nextjs.org/learn
-   [ ] Ler CVA + Shadcn-ui docs (30min)
-   [ ] **Output:** Notas de estudo em `docs/LEARNING-NOTES.md`

#### Day 2 (14 Nov): Backup & Project Creation

```bash
# Backup Laravel project
git tag v0.1.0-laravel
git push origin v0.1.0-laravel

# Create new branch
git checkout -b feat/migrate-nextjs-nestjs

# Install CLIs
npm install -g @nestjs/cli
npm install -g prisma

# Create projects
nest new nest-backend --strict
cd nest-backend && npm install @prisma/client prisma

npx create-next-app@latest next-frontend --typescript --tailwind --app
cd next-frontend && npx shadcn@latest init

# Create environment files
cd nest-backend
echo 'DATABASE_URL="postgresql://laravel:secret@orionone-db:5432/orionone?schema=public"' > .env
echo 'JWT_SECRET='$(openssl rand -base64 32) >> .env
echo 'JWT_EXPIRATION=7d' >> .env
echo 'REDIS_HOST=orionone-redis' >> .env
echo 'MEILISEARCH_HOST=http://orionone-meilisearch:7700' >> .env
echo 'NODE_ENV=development' >> .env
echo 'PORT=3001' >> .env

cd ../next-frontend
echo 'NEXT_PUBLIC_API_URL=http://localhost:3001' > .env.local
```

-   [ ] Nest.js project criado com TypeScript strict mode
-   [ ] Next.js project criado com App Router + Tailwind
-   [ ] Shadcn-ui inicializado
-   [ ] ⚠️ **NOVO:** .env files criados com JWT_SECRET gerado
-   [ ] **Output:** 2 pastas `nest-backend/` e `next-frontend/` no workspace

#### Day 3 (15 Nov): Docker Configuration + Nginx

-   [ ] Adaptar `docker-compose.yml`: adicionar services backend e frontend
-   [ ] Configurar Dockerfile para Nest.js (Node 20 Alpine)
-   [ ] Configurar Dockerfile para Next.js (Node 20 Alpine)
-   [ ] ⚠️ **NOVO:** Criar `nginx.conf` (reverse proxy: / → frontend, /api → backend)
-   [ ] ⚠️ **NOVO:** Adicionar Nginx service ao docker-compose
-   [ ] ⚠️ **NOVO:** Configurar Docker networks (orionone_network)
-   [ ] Testar `docker-compose up` (verificar health checks)
-   [ ] Testar networking: http://localhost → frontend, http://localhost/api → backend
-   [ ] **Output:** Docker Compose funcionando com 8 containers (backend, frontend, postgres, redis, meilisearch, mailpit, nginx)

#### Day 4 (16 Nov): Prisma Schema + Health Check + CORS

-   [ ] Copiar Prisma schema da Part 2 (`MIGRATION-PART-2-BACKEND.md`)
-   [ ] Criar `prisma/schema.prisma`
-   [ ] Rodar `npx prisma migrate dev --name init` (testar contra PostgreSQL)
-   [ ] Rodar `npx prisma generate` (gerar Prisma Client)
-   [ ] Abrir Prisma Studio: `npx prisma studio` (verificar models)
-   [ ] ⚠️ **NOVO:** Criar HealthController com endpoint `/health`
-   [ ] ⚠️ **NOVO:** Configurar CORS em main.ts (allow localhost:3000)
-   [ ] Testar health check: `curl http://localhost:3001/health`
-   [ ] Testar CORS: fetch de http://localhost:3000 → http://localhost:3001
-   [ ] **Output:** Database com 15 tabelas + health check + CORS funcionando

**Week 0 Deliverables:**

-   ✅ Nest.js + Next.js projects bootstrapped
-   ✅ ⚠️ .env files criados (DATABASE_URL, JWT_SECRET, API URLs)
-   ✅ Docker Compose adapted (8 containers)
-   ✅ ⚠️ Nginx reverse proxy configurado
-   ✅ Prisma schema migrated (15 tables)
-   ✅ ⚠️ Health check endpoint (/health)
-   ✅ ⚠️ CORS configurado

---

### **WEEK 1: Database + Auth Module** (Nov 18-22, 2024) — 5 dias

**Objetivo:** Completar Prisma schema, Auth JWT, CASL permissions

#### Monday (18 Nov): Prisma Models + Seed Completo

-   [ ] Revisar todos os 15 models vs Laravel migrations
-   [ ] Adicionar indexes faltantes (performance)
-   [ ] ⚠️ **DECISÃO CRÍTICA:** Triggers vs Application Layer
    -   **Recomendado:** Application Layer (ticketNumber generation + SLA calculation no Service)
    -   Alternativa: Criar raw SQL triggers via Prisma migrations
-   [ ] ⚠️ **NOVO:** Criar seed script completo: `prisma/seed.ts`
    -   32 permissions (tickets.create, tickets.view, tickets.update, etc.)
    -   RoleHasPermissions mapping (ADMIN: all, AGENT: tickets+comments, USER: own tickets)
    -   3 test users (admin@orionone.com, agent@orionone.com, user@orionone.com)
    -   5 categories, 10 tickets de teste
-   [ ] Rodar `npx prisma db seed`
-   [ ] Verificar no Prisma Studio: users, permissions, role_has_permissions
-   [ ] **Output:** Database populated com dados realistas

#### Tuesday (19 Nov): Auth Module + Error Handling

-   [ ] Criar AuthModule, AuthService, AuthController
-   [ ] Implementar `register()`: bcrypt password, criar User
-   [ ] Implementar `login()`: JWT token generation
-   [ ] Criar JwtStrategy (passport-jwt)
-   [ ] ⚠️ **NOVO:** Criar AllExceptionsFilter (global error handler)
-   [ ] ⚠️ **NOVO:** Registrar em main.ts: `app.useGlobalFilters(new AllExceptionsFilter())`
-   [ ] Testar com Postman: `POST /auth/register` e `POST /auth/login`
-   [ ] Testar error handling: POST /auth/login com senha errada → ver JSON error formatado
-   [ ] **Output:** JWT authentication + error handling funcionando

#### Wednesday (20 Nov): RBAC - CASL Abilities

-   [ ] Criar AbilitiesModule
-   [ ] Copiar AbilityFactory da Part 2
-   [ ] Implementar permissões:
    -   ADMIN: can manage all
    -   AGENT: can manage assigned tickets
    -   USER: can read own tickets
-   [ ] Criar guard `@CheckAbilities()` decorator
-   [ ] Testar role-based access
-   [ ] **Output:** CASL permissions working

#### Thursday (21 Nov): UsersModule

-   [ ] Criar UsersModule, UsersService, UsersController
-   [ ] Implementar CRUD: `GET /users`, `GET /users/:id`, `PATCH /users/:id`, `DELETE /users/:id`
-   [ ] Adicionar Swagger decorators: `@ApiTags('users')`
-   [ ] Integrar CASL: apenas ADMIN pode deletar users
-   [ ] **Output:** Users API completa

#### Friday (22 Nov): Upload Module - Avatar

-   [ ] Criar UploadModule, UploadService
-   [ ] Configurar Multer (file size: 5MB)
-   [ ] Implementar Sharp processing: resize 300x300, WebP 80%
-   [ ] Criar `POST /upload/avatar` endpoint
-   [ ] Salvar Media model com polymorphic relation
-   [ ] Testar upload de avatar
-   [ ] **Output:** Avatar upload funcionando

**Week 1 Deliverables:**

-   ✅ 15 Prisma models + seed data
-   ✅ Auth JWT + CASL permissions
-   ✅ UsersModule + UploadModule
-   ✅ Swagger documentation gerada

**Tests:** 12 Jest tests (Auth, Users, Upload)

---

### **WEEK 2: Tickets Module (Backend)** (Nov 25-29, 2024) — 5 dias

**Objetivo:** Tickets CRUD completo com SLA, filters, assignment

#### Monday (25 Nov): TicketsModule Setup

-   [ ] Criar TicketsModule, TicketsService, TicketsController
-   [ ] Copiar código da Part 2 (já pronto!)
-   [ ] Implementar `create()`: auto-generate ticketNumber (TKT-20241125-0001)
-   [ ] Implementar SLA calculation: `calculateSLA(priority)`
-   [ ] Testar com Postman: `POST /tickets`
-   [ ] **Output:** Ticket creation working

#### Tuesday (26 Nov): Tickets CRUD

-   [ ] Implementar `findAll()`: role-based filtering (USER/AGENT/ADMIN)
-   [ ] Implementar `findOne()`: GET /tickets/:id com relacionamentos (requester, assignee, comments)
-   [ ] Implementar `update()`: PATCH /tickets/:id
-   [ ] Implementar `remove()`: soft delete (deletedAt)
-   [ ] **Output:** Full Tickets CRUD

#### Wednesday (27 Nov): Tickets Advanced Features

-   [ ] Implementar `assignTicket()`: POST /tickets/:id/assign
-   [ ] Implementar `updateStatus()`: POST /tickets/:id/status
-   [ ] Activity Log: registrar todas as mudanças (ActivityLogService)
-   [ ] Notificações: notificar assignee via email (queue job)
-   [ ] **Output:** Tickets workflow completo

#### Thursday (28 Nov): CategoriesModule

-   [ ] Criar CategoriesModule (categories para tickets)
-   [ ] Implementar CRUD categories
-   [ ] Relação Ticket → Category
-   [ ] **Output:** Categories API

#### Friday (29 Nov): Tickets Tests

-   [ ] Escrever 20 Jest tests:
    -   Ticket creation (ticketNumber generation)
    -   SLA calculation (URGENT=1h, HIGH=4h, MEDIUM=8h, LOW=24h)
    -   Role-based filtering (USER sees own, AGENT sees assigned, ADMIN sees all)
    -   Assignment logic
    -   Status transitions
-   [ ] Rodar `npm test` (target: 80% coverage)
-   [ ] **Output:** 20 passing tests

**Week 2 Deliverables:**

-   ✅ TicketsModule completo (CRUD + SLA + assign + activity log)
-   ✅ CategoriesModule
-   ✅ 20 Jest tests passing

---

### **WEEK 3: Tickets Frontend** (Dec 2-6, 2024) — 5 dias

**Objetivo:** Next.js pages para Tickets (list, create, edit, detail)

#### Monday (2 Dec): Next.js Setup + CSS Migration

-   [ ] Configurar `lib/api-client.ts` (Axios com JWT interceptor)
-   [ ] Criar `store/auth-store.ts` (Zustand)
-   [ ] Configurar React Query: `app/providers.tsx`
-   [ ] ⚠️ **NOVO CRÍTICO:** Copiar Tailwind CSS do Laravel
    -   Copiar `resources/css/app.css` → `app/globals.css` (30+ CSS variables)
    -   Copiar `tailwind.config.js` → `tailwind.config.ts` (colors, borderRadius, fonts)
    -   Verificar: --radius, --chart-1 a --chart-5, --background, etc.
-   [ ] ⚠️ **NOVO:** Configurar TypeScript aliases
    -   Atualizar `tsconfig.json` com paths (@/components, @/lib, @/hooks)
    -   Criar `components.json` (Shadcn-ui aliases)
-   [ ] Testar: `import { Button } from '@/components/ui/button'` funciona
-   [ ] Testar: Dark mode toggle (verificar CSS variables aplicadas)
-   [ ] Criar Dashboard layout: `app/(dashboard)/layout.tsx` (Sidebar + Header)
-   [ ] **Output:** Next.js base structure + CSS 100% compatível

#### Tuesday (3 Dec): Tickets List Page

-   [ ] Criar `app/(dashboard)/tickets/page.tsx`
-   [ ] Criar `components/tickets/tickets-list.tsx` (useTickets hook)
-   [ ] Criar `components/tickets/ticket-card.tsx`
-   [ ] Criar `components/tickets/tickets-filters.tsx` (status, priority, search)
-   [ ] Testar filtros (status=OPEN, priority=URGENT)
-   [ ] **Output:** Tickets list funcionando

#### Wednesday (4 Dec): Ticket Create Page

-   [ ] Criar `app/(dashboard)/tickets/create/page.tsx`
-   [ ] Criar `components/tickets/ticket-form.tsx` (react-hook-form + zod)
-   [ ] Integrar TiptapEditor para description
-   [ ] Implementar `useCreateTicket()` mutation
-   [ ] Testar criação de ticket
-   [ ] **Output:** Create ticket working

#### Thursday (5 Dec): Ticket Detail Page

-   [ ] Criar `app/(dashboard)/tickets/[id]/page.tsx`
-   [ ] Mostrar ticket details (title, description, status, priority, SLA)
-   [ ] Criar `components/tickets/ticket-timeline.tsx` (activity log)
-   [ ] Criar `components/tickets/assign-dialog.tsx`
-   [ ] Criar `components/tickets/status-updater.tsx`
-   [ ] **Output:** Ticket detail page completa

#### Friday (6 Dec): Ticket Edit + Polish

-   [ ] Criar `app/(dashboard)/tickets/[id]/edit/page.tsx`
-   [ ] Reutilizar `ticket-form.tsx` com `useUpdateTicket()`
-   [ ] Adicionar badges de status/priority (Shadcn-ui Badge)
-   [ ] Polish UI: loading states, error handling, toast notifications
-   [ ] **Output:** Tickets frontend completo

**Week 3 Deliverables:**

-   ✅ Tickets List, Create, Edit, Detail pages
-   ✅ Tiptap editor integrado
-   ✅ React Query caching funcionando
-   ✅ UI polida com Shadcn-ui
-   ✅ ⚠️ Tailwind CSS variables migradas (100% aparencia idêntica)
-   ✅ ⚠️ TypeScript aliases configurados

---

### **WEEK 4: Comments + Teams Modules** (Dec 9-13, 2024) — 5 dias

**Objetivo:** Comments (backend + frontend), Teams module

#### Monday (9 Dec): CommentsModule Backend

-   [ ] Criar CommentsModule, CommentsService, CommentsController
-   [ ] Implementar CRUD comments
-   [ ] Relação Comment → Ticket
-   [ ] Adicionar flag `isInternal` (visible apenas para AGENT/ADMIN)
-   [ ] **Output:** Comments API

#### Tuesday (10 Dec): Comments Frontend

-   [ ] Criar `components/comments/comment-list.tsx`
-   [ ] Criar `components/comments/comment-form.tsx` (Tiptap)
-   [ ] Criar `components/comments/comment-item.tsx`
-   [ ] Filtrar comments: USER não vê isInternal=true
-   [ ] Adicionar real-time updates (React Query refetch)
-   [ ] **Output:** Comments UI completa

#### Wednesday (11 Dec): TeamsModule Backend

-   [ ] Criar TeamsModule
-   [ ] Implementar CRUD teams
-   [ ] Relação many-to-many: Team ↔ User (TeamMember model)
-   [ ] Adicionar `role` no TeamMember: LEAD | MEMBER
-   [ ] **Output:** Teams API

#### Thursday (12 Dec): Teams Frontend

-   [ ] Criar `app/(dashboard)/teams/page.tsx` (teams list)
-   [ ] Criar `app/(dashboard)/teams/[id]/page.tsx` (team detail + members)
-   [ ] Criar `components/teams/add-member-dialog.tsx`
-   [ ] Mostrar tickets assigned to team
-   [ ] **Output:** Teams frontend completa

#### Friday (13 Dec): Integration Tests

-   [ ] Escrever 10 integration tests:
    -   Create ticket → Add comment → Verify activity log
    -   Assign ticket to team → Verify team members see it
    -   Internal comment visibility
-   [ ] **Output:** 10 integration tests passing

**Week 4 Deliverables:**

-   ✅ CommentsModule (backend + frontend)
-   ✅ TeamsModule (backend + frontend)
-   ✅ 10 integration tests

---

### **WEEK 5: Knowledge Base** (Dec 16-20, 2024) — 5 dias

**Objetivo:** Articles CRUD, Meilisearch integration, version history

#### Monday (16 Dec): ArticlesModule Backend

-   [ ] Criar ArticlesModule
-   [ ] Implementar CRUD articles
-   [ ] Relação Article → Category
-   [ ] Adicionar `slug` (auto-generated from title)
-   [ ] **Output:** Articles API

#### Tuesday (17 Dec): Meilisearch Integration

-   [ ] Instalar `npm install meilisearch`
-   [ ] Criar SearchModule, SearchService
-   [ ] Indexar articles no Meilisearch após create/update
-   [ ] Implementar `GET /search?q=keyword` (full-text search)
-   [ ] Testar search: "password reset" → retorna artigos relevantes
-   [ ] **Output:** Search funcionando

#### Wednesday (18 Dec): Article Versioning

-   [ ] Criar ArticleVersion model (store previous versions)
-   [ ] Implementar `createVersion()` antes de update
-   [ ] Criar endpoint `GET /articles/:id/versions`
-   [ ] Criar endpoint `POST /articles/:id/restore/:versionId`
-   [ ] **Output:** Version history working

#### Thursday (19 Dec): KB Frontend - List & Detail

-   [ ] Criar `app/(dashboard)/knowledge-base/page.tsx` (articles list)
-   [ ] Criar `app/(dashboard)/knowledge-base/[slug]/page.tsx` (article detail)
-   [ ] Mostrar breadcrumbs (category hierarchy)
-   [ ] Adicionar search bar (integração com Meilisearch)
-   [ ] **Output:** KB frontend base

#### Friday (20 Dec): KB Frontend - Editor

-   [ ] Criar `app/(dashboard)/knowledge-base/create/page.tsx`
-   [ ] Criar `components/kb/article-editor.tsx` (Tiptap)
-   [ ] Adicionar voting system: `POST /articles/:id/vote` (upvote/downvote)
-   [ ] Mostrar version history sidebar
-   [ ] **Output:** KB completo

**Week 5 Deliverables:**

-   ✅ ArticlesModule + SearchModule
-   ✅ Meilisearch full-text search
-   ✅ Article versioning
-   ✅ KB frontend completo

---

### **WEEK 6: Assets CMDB** (Dec 23-27, 2024) — 5 dias

**Objetivo:** Assets module, CSV import, warranty tracking

#### Monday (23 Dec): AssetsModule Backend

-   [ ] Criar AssetsModule
-   [ ] Implementar CRUD assets
-   [ ] Adicionar fields: `assetType`, `assetStatus`, `serialNumber`, `warrantyEndDate`
-   [ ] Relação Asset → User (assignedTo)
-   [ ] **Output:** Assets API

#### Tuesday (24 Dec): CSV Import (ExcelJS)

-   [ ] Instalar `npm install exceljs`
-   [ ] Criar `POST /assets/import` (upload CSV)
-   [ ] Parsear CSV com ExcelJS
-   [ ] Validar dados (zod schema)
-   [ ] Bulk insert assets
-   [ ] Retornar report: `{ imported: 50, errors: [] }`
-   [ ] **Output:** CSV import working

#### Wednesday (25 Dec): Assets Frontend

-   [ ] Criar `app/(dashboard)/assets/page.tsx` (assets list)
-   [ ] Criar `app/(dashboard)/assets/[id]/page.tsx` (asset detail)
-   [ ] Adicionar filters: type, status, warranty expiring soon
-   [ ] **Output:** Assets frontend base

#### Thursday (26 Dec): Assets Advanced Features

-   [ ] Criar `components/assets/import-dialog.tsx` (CSV upload)
-   [ ] Mostrar warranty alerts (expiring in <30 days)
-   [ ] Criar `components/assets/asset-history.tsx` (assignment history)
-   [ ] **Output:** Assets CMDB completo

#### Friday (27 Dec): Assets Tests

-   [ ] Escrever 10 Jest tests:
    -   Asset CRUD
    -   CSV import validation
    -   Warranty expiration logic
-   [ ] **Output:** 10 tests passing

**Week 6 Deliverables:**

-   ✅ AssetsModule completo
-   ✅ CSV import (ExcelJS)
-   ✅ Warranty tracking
-   ✅ 10 tests passing

---

### **WEEK 7: Dashboard + Reports** (Dec 30-Jan 3, 2025) — 5 dias

**Objetivo:** Dashboard com gráficos (Recharts), Excel exports

#### Monday (30 Dec): Dashboard Backend - Metrics

-   [ ] Criar DashboardModule
-   [ ] Implementar `GET /dashboard/metrics`:
    -   Total tickets (by status)
    -   SLA compliance rate
    -   Top categories
    -   Agent performance (avg resolution time)
-   [ ] **Output:** Metrics API

#### Tuesday (31 Dec): Dashboard Frontend - Charts

-   [ ] Instalar `npm install recharts`
-   [ ] Criar `app/(dashboard)/page.tsx` (dashboard home)
-   [ ] Criar `components/charts/tickets-by-status.tsx` (Bar Chart)
-   [ ] Criar `components/charts/sla-compliance.tsx` (Pie Chart)
-   [ ] Criar `components/charts/tickets-trend.tsx` (Line Chart)
-   [ ] **Output:** Dashboard charts

#### Wednesday (1 Jan): Reports Module Backend

-   [ ] Criar ReportsModule
-   [ ] Implementar `POST /reports/tickets` (generate Excel)
-   [ ] Usar ExcelJS para criar workbook:
    -   Sheet 1: Tickets list
    -   Sheet 2: SLA compliance
    -   Sheet 3: Agent performance
-   [ ] Retornar arquivo `.xlsx`
-   [ ] **Output:** Excel export working

#### Thursday (2 Jan): Reports Frontend

-   [ ] Criar `app/(dashboard)/reports/page.tsx`
-   [ ] Adicionar filtros: date range, status, priority
-   [ ] Botão "Download Excel Report"
-   [ ] Preview de dados antes de exportar
-   [ ] **Output:** Reports completo

#### Friday (3 Jan): Dashboard Polish

-   [ ] Adicionar KPI cards (total tickets, avg resolution time)
-   [ ] Implementar date range picker (date-fns)
-   [ ] Adicionar loading states para charts
-   [ ] Testar performance (queries otimizadas)
-   [ ] **Output:** Dashboard finalizado

**Week 7 Deliverables:**

-   ✅ Dashboard com 4 charts (Recharts)
-   ✅ Excel exports (ExcelJS)
-   ✅ Reports module completo

---

### **WEEK 8: Notifications + Queue + Polish** (Jan 6-10, 2025) — 5 dias

**Objetivo:** Notificações email, queue jobs (Bull), optimizations

#### Monday (6 Jan): NotificationsModule Backend

-   [ ] Criar NotificationsModule
-   [ ] Implementar CRUD notifications
-   [ ] Criar `GET /notifications` (user's notifications)
-   [ ] Criar `POST /notifications/:id/read`
-   [ ] **Output:** Notifications API

#### Tuesday (7 Jan): Queue Jobs (Bull + Redis) + Mailpit

-   [ ] Instalar `npm install @nestjs/bull bull`
-   [ ] Configurar BullModule (connect Redis)
-   [ ] Criar `EmailProcessor` (process email jobs)
-   [ ] ⚠️ **NOVO:** Instalar `npm install @nestjs-modules/mailer nodemailer`
-   [ ] ⚠️ **NOVO:** Configurar MailModule (Mailpit: host=mailpit, port=1025)
-   [ ] ⚠️ **NOVO:** Adicionar Mailpit ao docker-compose.yml
-   [ ] Criar jobs:
    -   `sendTicketAssignedEmail()`
    -   `sendTicketResolvedEmail()`
    -   `sendSlaBreachAlert()`
-   [ ] Testar queue: criar ticket → assignee recebe email
-   [ ] Verificar emails: http://localhost:8025 (Mailpit UI)
-   [ ] **Output:** Queue + Email funcionando

#### Wednesday (8 Jan): Notifications Frontend + Real-Time (Optional)

-   [ ] Criar `components/layout/notifications-dropdown.tsx` (Header)
-   [ ] Mostrar notificações em tempo real (polling 30s)
-   [ ] Marcar como lida ao clicar
-   [ ] Badge com contagem de não lidas
-   [ ] 💡 **OPCIONAL:** WebSocket Real-Time
    -   Instalar `npm install @nestjs/websockets socket.io`
    -   Criar NotificationsGateway (WebSocket)
    -   Criar useNotifications hook (Next.js client)
    -   Substituir polling por WebSocket emit
    -   ✅ Vantagem: Notificações instantâneas
    -   ❌ Desvantagem: +2 horas de trabalho
-   [ ] **Output:** Notifications UI (polling ou WebSocket)

#### Thursday (9 Jan): Performance Optimizations + Logging

-   [ ] Adicionar database indexes faltantes (Prisma schema)
-   [ ] Implementar caching (Redis): cache metrics por 5min
-   [ ] Otimizar queries: usar `select` para evitar fetch de todos os campos
-   [ ] ⚠️ **NOVO:** Configurar Winston logging
    -   Instalar `npm install nest-winston winston`
    -   Criar LoggerModule (console + file transports)
    -   Adicionar logging em Services críticos (TicketsService, AuthService)
    -   Log levels: info, warn, error
    -   Logs salvos em: `logs/error.log`, `logs/combined.log`
-   [ ] **Output:** Performance melhorada + logging estruturado

#### Friday (10 Jan): UI Polish

-   [ ] Revisar todas as páginas (responsividade mobile)
-   [ ] Adicionar skeleton loaders (Shadcn-ui)
-   [ ] Implementar error boundaries
-   [ ] Validar todos os formulários (mensagens de erro claras)
-   [ ] **Output:** UI finalizada

**Week 8 Deliverables:**

-   ✅ NotificationsModule (backend + frontend)
-   ✅ Queue jobs (Bull + Redis)
-   ✅ ⚠️ Email notifications (Mailpit configurado)
-   ✅ ⚠️ Winston logging (console + file)
-   ✅ 💡 (Opcional) WebSocket real-time notifications
-   ✅ Performance otimizada
-   ✅ UI polida

---

### **WEEK 9: Testing + Documentation** (Jan 13-17, 2025) — 5 dias

**Objetivo:** 80% test coverage, Playwright E2E, Swagger complete

#### Monday (13 Jan): Unit Tests - Backend

-   [ ] Escrever Jest tests para todos os services:
    -   AuthService (10 tests)
    -   TicketsService (20 tests)
    -   CommentsService (8 tests)
    -   ArticlesService (12 tests)
    -   AssetsService (10 tests)
-   [ ] Rodar `npm test -- --coverage` (target: 80%)
-   [ ] **Output:** 60+ unit tests passing

#### Tuesday (14 Jan): Integration Tests

-   [ ] Escrever Supertest tests (API endpoints):
    -   Auth flow (login, register, JWT validation)
    -   Tickets CRUD + assign + status update
    -   Comments creation + internal visibility
    -   Search (Meilisearch)
-   [ ] **Output:** 20 integration tests passing

#### Wednesday (15 Jan): E2E Tests (Playwright)

-   [ ] Instalar `npm install -D @playwright/test`
-   [ ] Escrever E2E tests:
    -   User login → Create ticket → Add comment
    -   Agent assign ticket → Update status → Resolve
    -   Admin create article → Publish → Search
-   [ ] Rodar `npx playwright test`
-   [ ] **Output:** 10 E2E tests passing

#### Thursday (16 Jan): Swagger Documentation

-   [ ] Revisar todos os controllers (adicionar `@ApiOperation`, `@ApiResponse`)
-   [ ] Adicionar exemplos de requests/responses
-   [ ] Gerar Swagger UI: http://localhost:3001/api
-   [ ] Exportar OpenAPI spec: `swagger.json`
-   [ ] **Output:** API docs completa

#### Friday (17 Jan): Documentation

-   [ ] Atualizar `README.md`:
    -   Tech stack (Next.js 15 + Nest.js 10)
    -   Setup instructions
    -   Docker Compose commands
    -   API endpoints
-   [ ] Criar `docs/API.md` (endpoints reference)
-   [ ] Criar `docs/DEPLOYMENT.md` (production guide)
-   [ ] **Output:** Docs completa

**Week 9 Deliverables:**

-   ✅ 80%+ test coverage (90+ tests)
-   ✅ Playwright E2E tests
-   ✅ Swagger documentation
-   ✅ README + docs updated

---

### **WEEK 10: Deployment + Final Polish** (Jan 20-24, 2025) — 5 dias

**Objetivo:** Production deployment, CI/CD, Sentry, demo video

#### Monday (20 Jan): Docker Production

-   [ ] Criar `Dockerfile.prod` (Nest.js + Next.js)
-   [ ] Otimizar images (multi-stage builds)
-   [ ] Criar `docker-compose.prod.yml`
-   [ ] Testar build: `docker-compose -f docker-compose.prod.yml up`
-   [ ] **Output:** Docker production-ready

#### Tuesday (21 Jan): CI/CD Pipeline (GitHub Actions)

-   [ ] Criar `.github/workflows/ci.yml`:
    -   Run Jest tests
    -   Run Playwright tests
    -   Build Docker images
    -   Push to Docker Hub
-   [ ] Testar CI: commit → pipeline runs
-   [ ] **Output:** CI/CD working

#### Wednesday (22 Jan): Error Tracking (Sentry)

-   [ ] Criar conta Sentry (free tier)
-   [ ] Instalar `npm install @sentry/node @sentry/nextjs`
-   [ ] Configurar Sentry no Nest.js (NestFactory.create)
-   [ ] Configurar Sentry no Next.js (`sentry.client.config.ts`)
-   [ ] Testar error tracking: throw error → ver no Sentry dashboard
-   [ ] **Output:** Sentry configured

#### Thursday (23 Jan): Final Testing

-   [ ] Manual testing completo:
    -   Testar todos os 39 features (checklist)
    -   Verificar RBAC (USER, AGENT, ADMIN roles)
    -   Testar edge cases (empty states, errors)
-   [ ] Fix bugs encontrados
-   [ ] **Output:** All features working

#### Friday (24 Jan): Demo Video

-   [ ] Gravar video demo (5-10min):
    -   Intro: ITSM platform, tech stack
    -   Auth + RBAC
    -   Create ticket → Assign → Resolve
    -   Knowledge Base → Search
    -   Assets CMDB → Import CSV
    -   Dashboard → Charts → Excel export
-   [ ] Editar video (adicionar subtítulos)
-   [ ] Upload no YouTube (unlisted)
-   [ ] **Output:** Demo video pronto

**Week 10 Deliverables:**

-   ✅ Docker production deployment
-   ✅ CI/CD pipeline (GitHub Actions)
-   ✅ Sentry error tracking
-   ✅ Demo video (5-10min)

---

### **BUFFER WEEK** (Jan 27-31, 2025) — 5 dias

**Objetivo:** Bug fixes, final polish, contingency time

#### If On Schedule:

-   [ ] Refactor código (remove console.logs, dead code)
-   [ ] Adicionar features extras:
    -   Dark mode toggle
    -   Email templates design
    -   Advanced filters (tickets by SLA breach)
-   [ ] Performance tuning (database query optimization)
-   [ ] Accessibility audit (WCAG 2.1)

#### If Behind Schedule:

-   [ ] Priorizar features críticos (Tickets, KB, Auth)
-   [ ] Cortar features nice-to-have (Assets CMDB, advanced reports)
-   [ ] Focus em funcionalidade core
-   [ ] Testing básico (skip Playwright se necessário)

---

## 📊 FEATURES CHECKLIST (39 TOTAL)

### Sprint 1: Foundation (7 features) ✅

-   [x] Auth (Register, Login, JWT)
-   [x] RBAC (5 roles: ADMIN, AGENT, USER, SUPER_ADMIN, GUEST)
-   [x] Profile (Avatar upload, update profile)
-   [x] Activity Log (audit trail)
-   [x] Dark Mode
-   [x] Responsive layout
-   [x] Tests (Auth, Profile)

### Sprint 2: Tickets Core (8 features)

-   [ ] Tickets CRUD
-   [ ] Auto-generate ticket number (TKT-YYYYMMDD-0001)
-   [ ] SLA calculation (priority-based deadlines)
-   [ ] Ticket assignment (agent/team)
-   [ ] Status transitions (OPEN → IN_PROGRESS → RESOLVED → CLOSED)
-   [ ] Priority levels (LOW, MEDIUM, HIGH, URGENT)
-   [ ] Categories
-   [ ] Tests (Tickets CRUD, SLA logic)

### Sprint 3: Collaboration (5 features)

-   [ ] Comments (public + internal)
-   [ ] File attachments (tickets + comments)
-   [ ] Teams (create team, add members)
-   [ ] Team assignment
-   [ ] Tests (Comments, Teams)

### Sprint 4: Knowledge Base (6 features)

-   [ ] Articles CRUD
-   [ ] Full-text search (Meilisearch)
-   [ ] Categories hierarchy
-   [ ] Article versioning
-   [ ] Voting system (upvote/downvote)
-   [ ] Tests (Articles, Search)

### Sprint 5: Assets CMDB (5 features)

-   [ ] Assets CRUD (6 types: LAPTOP, DESKTOP, SERVER, LICENSE, MOBILE, NETWORK)
-   [ ] Asset assignment (user)
-   [ ] CSV import (ExcelJS)
-   [ ] Warranty tracking
-   [ ] Tests (Assets, CSV import)

### Sprint 6: Dashboard & Reports (5 features)

-   [ ] Dashboard home (KPIs)
-   [ ] Charts (Recharts): tickets by status, SLA compliance, tickets trend
-   [ ] Excel exports (tickets, SLA, agent performance)
-   [ ] Date range filters
-   [ ] Tests (Dashboard queries)

### Sprint 7: Notifications (3 features)

-   [ ] In-app notifications
-   [ ] Email notifications (queue jobs)
-   [ ] Notification preferences
-   [ ] Tests (Notifications)

---

## 🚀 VELOCITY METRICS

**Estimated Effort:**

-   Backend (Nest.js): ~5,000 lines, 50 files, 15 modules
-   Frontend (Next.js): ~6,000 lines, 60 components, 20 pages
-   Tests: ~2,000 lines, 90+ tests
-   **Total:** ~13,000 lines (vs 15,000 Laravel+Vue = 13% redução)

**Velocity Gains:**

-   ⚡ Nest CLI: `nest g resource tickets` gera 90% do boilerplate
-   ⚡ Prisma: auto-migrations, zero SQL escrito
-   ⚡ Shadcn-ui: `npx shadcn add button` instala componentes prontos
-   ⚡ Swagger: auto-documenta APIs (zero config)
-   ⚡ TypeScript: previne 80% dos bugs (type-safety)

**Realistic Velocity:**

-   Week 1-2: Slow (learning curve)
-   Week 3-6: Fast (copy-paste patterns)
-   Week 7-9: Medium (complex features)
-   Week 10: Slow (testing, docs)

---

## 🎯 DAILY ROUTINE (10 WEEKS)

**Morning (2-3 hours):**

-   Check todo list (manage_todo_list tool)
-   Code new feature (TDD: test first, then implement)
-   Commit progress: `git commit -m "feat: ticket assignment"`

**Afternoon (2-3 hours):**

-   Fix bugs/errors (get_errors tool)
-   Write tests (Jest + Playwright)
-   Update docs (README, CHANGELOG)

**Evening (1 hour):**

-   Code review (check Nest.js/Next.js best practices)
-   Refactor (DRY principle, remove duplication)
-   Plan tomorrow (update timeline)

**Weekly Review (Friday):**

-   Retrospective: What worked? What didn't?
-   Adjust timeline if behind schedule
-   Push to GitHub (create PR if needed)

---

## 🏁 FINAL DELIVERY (Jan 31, 2025)

**Entregáveis:**

1. ✅ Código-fonte completo (Next.js + Nest.js)
2. ✅ Docker Compose production-ready
3. ✅ 90+ tests passing (80%+ coverage)
4. ✅ Swagger API documentation
5. ✅ README + docs completa
6. ✅ Demo video (5-10min)
7. ✅ CI/CD pipeline (GitHub Actions)
8. ✅ Sentry error tracking configurado

**Git:**

```bash
git add .
git commit -m "feat: complete Next.js + Nest.js migration"
git push origin feat/migrate-nextjs-nestjs

# Create PR: feat/migrate-nextjs-nestjs → main
# Squash merge (1 commit: "Migrate to Next.js 15 + Nest.js 10")
# Delete branch
```

**Tag:**

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 📈 SUCCESS METRICS

**Functional:**

-   ✅ 39/39 features implemented
-   ✅ Auth + RBAC working (JWT + CASL)
-   ✅ Zero critical bugs

**Quality:**

-   ✅ 80%+ test coverage
-   ✅ <200ms median API response time
-   ✅ Zero security vulnerabilities

**Documentation:**

-   ✅ Swagger API docs complete
-   ✅ README setup instructions
-   ✅ Demo video published

**Deployment:**

-   ✅ Docker Compose production
-   ✅ CI/CD pipeline green
-   ✅ Sentry error tracking

---

## 🎉 CONCLUSÃO

**Prazo:** 31 Janeiro 2025 (70 dias, 10 semanas)
**Scope:** 39 features, 11,000 linhas código
**Stack:** Next.js 15 + Nest.js 10 + Prisma + PostgreSQL + Redis + Meilisearch
**Resultado esperado:** ITSM platform completa, production-ready, testada, documentada

**Próximo passo:** User review → Aprovação → START Week 0! 🚀
