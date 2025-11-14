# Arquitetura OrionOne - Sistema ITSM Moderno

**Stack Tecnológico**: Next.js 16 + Nest.js 11 + Prisma + PostgreSQL + TypeScript
**Versão**: v0.2.0 (Week 0 + Week 1 Monday completo)
**Última atualização**: 13 Nov 2024

---

## Visão Geral

OrionOne é um **sistema ITSM (IT Service Management)** completo baseado em frameworks ITIL v4, projetado com arquitetura moderna de 3 camadas para suportar:

### Requisitos Funcionais ITSM

- **Incident Management**: Registro, rastreamento e resolução de incidentes IT
- **Request Fulfillment**: Gestão de requisições de serviço e aprovações
- **Problem Management**: Análise de causa raiz e gestão de problemas conhecidos
- **Knowledge Management**: Base de conhecimento com artigos e FAQs
- **Asset Management (CMDB)**: Rastreamento de ativos IT e configurações
- **Service Catalog**: Catálogo de serviços disponíveis
- **SLA Management**: Monitoramento de SLAs e escalações automáticas
- **Multi-tenancy**: Suporte a múltiplas organizações/equipes

### Princípios Arquiteturais

- **Modular e Desacoplado**: Separação clara entre frontend, API e dados
- **Type-Safe End-to-End**: TypeScript garante contratos entre camadas
- **API-First**: Backend REST API permite integrações futuras
- **Escalável**: Arquitetura preparada para crescimento horizontal
- **Auditável**: Activity logs de todas as operações críticas
- **Seguro**: RBAC granular (Role-Based Access Control) com CASL

---

## Arquitetura de 3 Camadas

```

 CAMADA 1: APRESENTAÇÃO (Frontend) 
 Next.js 16 + React 19 

 Portal do Utilizador Portal do Agente/Admin 
 Dashboard (tickets overview) Dashboard (stats) 
 Criar Ticket Gestão de Tickets 
 Meus Tickets Gestão de Utilizadores 
 Knowledge Base (pesquisa) Knowledge Base (edição) 
 Perfil Asset Management (CMDB) 
 Reports & Analytics 
 Configurações 

 Tecnologias: 
 - React Server Components (performance, SEO) 
 - Shadcn-ui (componentes acessíveis) 
 - React Query (caching, optimistic updates) 
 - Zustand (auth state, UI state) 
 - Zod (validação de formulários) 

 ↓
 HTTP/REST (Axios)
 ↓

 CAMADA 2: LÓGICA DE NEGÓCIO (API) 
 Nest.js 11 REST API 

 Módulos ITSM (Domain-Driven Design): 

 Auth & Security Incident Management 
 JWT Authentication Ticket CRUD 
 RBAC (CASL) Status workflow (Open→Resolved) 
 Password reset Assignment & escalation 
 Audit logs SLA calculation & monitoring 
 Priority management 
 User Management Comments & attachments 
 Users CRUD 
 Teams & roles Knowledge Management 
 Permissions Articles CRUD 
 Avatar upload Categories & tags 
 Version control 
 Asset Management Full-text search (Meilisearch) 
 Assets CRUD Views counter 
 Asset types 
 Status tracking Reporting & Analytics 
 Relationships Ticket metrics (open, resolved) 
 SLA compliance reports 
 Notifications Agent performance 
 Real-time alerts Asset inventory reports 
 Email notifications 
 In-app notifications System Configuration 
 Categories management 
 SLA policies 
 Email templates 

 Cross-Cutting Concerns: 
 - Validation (DTOs, Pipes) 
 - Error handling (Global exception filter) 
 - Logging (Winston) 
 - Caching (Redis) 
 - API documentation (Swagger) 

 ↓
 Prisma ORM (Type-safe)
 ↓

 CAMADA 3: PERSISTÊNCIA (Dados) 

 PostgreSQL 16 (Relational Data) Redis 7.2 (Cache & Sessions) 
 users Session store 
 permissions API response cache 
 role_has_permissions Queue jobs 
 tickets (incident records) 
 comments Meilisearch 1.9 (Search) 
 categories Tickets index 
 articles (KB) Articles index 
 article_versions Assets index 
 assets (CMDB) 
 teams File Storage 
 team_members Avatars (local/S3) 
 media (attachments) Ticket attachments 
 activity_log (audit) Article images 
 notifications 

 Design Patterns: 
 - Relational normalization (3NF) 
 - Soft deletes (deletedAt) 
 - Timestamps (createdAt, updatedAt) 
 - UUID primary keys (security) 
 - Indexes (performance) 

```

---

## Modelo de Dados ITSM

### Domínios Principais

**1. Identity & Access Management (IAM)**

- Users: Agentes, técnicos, utilizadores finais
- Roles: ADMIN, AGENT, USER (hierarquia de permissões)
- Permissions: 32 permissões granulares (tickets.create, users.delete, etc.)
- Teams: Equipas de suporte (Help Desk, Network Team, etc.)

**2. Incident & Request Management**

- Tickets: Registo central de incidentes/requisições
- Status Workflow: OPEN → IN_PROGRESS → ON_HOLD → RESOLVED → CLOSED
- Prioridades: LOW, MEDIUM, HIGH, URGENT (escalação automática)
- SLA Tracking: Tempo de resposta e resolução por prioridade
- Categories: Classificação (Hardware, Software, Network, Access, Other)
- Comments: Thread de comunicação ticket
- Attachments: Anexos (screenshots, logs)

**3. Knowledge Management**

- Articles: Base de conhecimento técnica
- Categories: Organização hierárquica de artigos
- Versions: Controle de versão de artigos
- Search: Full-text search com Meilisearch
- Views Counter: Métricas de popularidade

**4. Asset Management (CMDB)**

- Assets: Inventário IT (laptops, servidores, licenças)
- Asset Types: Classificação de ativos
- Status: ACTIVE, MAINTENANCE, RETIRED, DISPOSED
- Relationships: Dependências entre ativos
- Assignment: Vinculação a utilizadores

**5. Audit & Notifications**

- Activity Logs: Rastreamento de todas as operações críticas
- Notifications: Sistema de notificações em tempo real
- Email Alerts: Notificações por email para SLA violations

### Relações Críticas

- User → Tickets (requester, assignee)
- User → Teams (many-to-many via team_members)
- Ticket → Category (classificação)
- Ticket → Comments (thread)
- Article → User (author tracking)
- Asset → User (assignment)
- RoleHasPermission → Role + Permission (RBAC)

---

## Estrutura de Pastas

### Backend: nest-backend/

```
nest-backend/
 src/
 main.ts # Bootstrap (CORS, global prefix)
 app.module.ts # Root module (imports PrismaModule)
 app.controller.ts # Health check endpoint
 app.service.ts

 prisma/ # Database module (IMPLEMENTED)
 prisma.module.ts # Global module
 prisma.service.ts # PrismaClient wrapper

 auth/ # Authentication (PENDING Week 1 Tue)
 auth.module.ts
 auth.controller.ts # Login, register endpoints
 auth.service.ts # JWT generation, bcrypt
 jwt.strategy.ts # Passport JWT strategy
 dto/
 login.dto.ts
 register.dto.ts

 users/ # User management (PENDING Week 1 Thu)
 users.module.ts
 users.controller.ts
 users.service.ts
 dto/

 tickets/ # Tickets CRUD (PENDING Week 3)
 tickets.module.ts
 tickets.controller.ts
 tickets.service.ts # SLA calculation, ticketNumber
 dto/

 upload/ # File uploads (PENDING Week 1 Fri)
 upload.module.ts
 upload.controller.ts
 upload.service.ts # Sharp processing, WebP
 dto/

 casl/ # Authorization (PENDING Week 1 Wed)
 casl.module.ts
 ability.factory.ts # Define permissions
 casl.guard.ts # Permission checking

 common/ # Shared code (PENDING Week 1 Tue)
 filters/
 all-exceptions.filter.ts # Global error handler
 interceptors/
 logging.interceptor.ts # Request logging
 guards/
 jwt-auth.guard.ts
 decorators/
 current-user.decorator.ts

 prisma/
 schema.prisma # 15 models, 6 enums (IMPLEMENTED)
 migrations/ # 1 migration: 20251113171344_init
 seed.ts # Professional seed (340 lines, IMPLEMENTED)

 test/ # E2E tests (PENDING Week 9)
 .env # Environment variables (CONFIGURED)
 .env.example
 package.json # 18 prod deps, 23 dev deps
 tsconfig.json # TypeScript strict mode
 nest-cli.json
 Dockerfile # Multi-stage build
 .dockerignore
```

### Frontend: next-frontend/

```
next-frontend/
 app/
 layout.tsx # Root layout (IMPLEMENTED)
 page.tsx # Home page (IMPLEMENTED)
 globals.css # Tailwind 4 CSS
 favicon.ico

 (auth)/ # Auth group (PENDING Week 2)
 layout.tsx
 login/
 page.tsx
 register/
 page.tsx
 forgot-password/
 page.tsx

 (dashboard)/ # Dashboard group (PENDING Week 2-7)
 layout.tsx # Sidebar + header
 page.tsx # Overview cards
 tickets/
 page.tsx # Tickets list
 [id]/
 page.tsx # Ticket detail
 new/
 page.tsx # Create ticket
 knowledge-base/
 page.tsx
 [slug]/
 page.tsx
 assets/
 teams/
 users/
 reports/
 settings/

 api/ # Edge API routes (optional)
 health/
 route.ts

 components/
 ui/ # Shadcn-ui (PENDING Week 2)
 button.tsx
 card.tsx
 input.tsx
 form.tsx
 dialog.tsx
 toast.tsx
 ...

 layout/ # Layout components (PENDING)
 sidebar.tsx
 header.tsx
 footer.tsx

 tickets/ # Feature components (PENDING Week 3)
 ticket-form.tsx
 ticket-card.tsx
 ticket-status-badge.tsx
 tickets-table.tsx

 forms/ # Reusable forms (PENDING Week 2)
 login-form.tsx
 register-form.tsx
 ticket-form.tsx

 lib/
 utils.ts # cn() utility (IMPLEMENTED)
 api.ts # Axios instance (PENDING Week 2)

 hooks/ # React Query hooks (PENDING Week 2-7)
 use-tickets.ts
 use-auth.ts
 use-users.ts

 stores/ # Zustand stores (PENDING Week 2)
 auth-store.ts
 theme-store.ts
 sidebar-store.ts

 types/ # TypeScript types (PENDING Week 2)
 ticket.ts
 user.ts
 api.ts

 public/ # Static files
 .env.local # Environment variables (CONFIGURED)
 .env.example
 components.json # Shadcn-ui config
 package.json # 11 prod deps, 9 dev deps
 tsconfig.json # TypeScript 5
 next.config.ts # Next.js 16 config
 tailwind.config.ts # Tailwind 4 config
 postcss.config.mjs
 Dockerfile # Multi-stage build
 .dockerignore
```

---

## Segurança & Controle de Acesso

### Autenticação (JWT)

- **Stateless Tokens**: JWT armazenado no client (Zustand)
- **Token Expiration**: 7 dias (renovação automática)
- **Password Hashing**: bcrypt com 10 salt rounds
- **Email Verification**: Validação obrigatória para novos utilizadores

### Autorização (RBAC com CASL)

**Níveis de Acesso:**

**ADMIN (Administrador)**

- Acesso total ao sistema
- Gestão de utilizadores e equipas
- Configuração de SLAs e categorias
- Relatórios avançados
- Permissões: manage all

**AGENT (Técnico de Suporte)**

- Ver todos os tickets
- Editar tickets assignados a si
- Criar/editar artigos da KB
- Ver assets
- Permissões: tickets._, comments._, categories.view, articles.\*, teams.view

**USER (Utilizador Final)**

- Criar tickets próprios
- Ver apenas seus tickets
- Comentar em seus tickets
- Ver Knowledge Base (read-only)
- Permissões: tickets.create, tickets.view (own), comments.create (own), articles.view

### Auditoria

- Activity Logs registam:
 - Quem (userId)
 - O quê (action: created, updated, deleted)
 - Quando (timestamp)
 - Onde (entity type e entityId)
 - Detalhes (changes JSON)

---

## Performance & Escalabilidade

### Estratégias de Caching

**Redis (Server-Side)**

- Session storage (7 dias TTL)
- API response cache (5 minutos TTL)
- Job queues (background tasks)

**React Query (Client-Side)**

- staleTime: 5 minutos (dados considerados frescos)
- cacheTime: 10 minutos (permanência em cache)
- Optimistic updates (UX imediata)
- Automatic background refetching

### Search & Indexação

**Meilisearch**

- Full-text search em tickets (título, descrição)
- Full-text search em articles
- Typo tolerance (tolerância a erros)
- Faceted search (filtros por categoria, status)
- Response time: <50ms

### Database Optimization

- Indexes estratégicos:
 - users.email (unique)
 - tickets.status, tickets.priority
 - tickets.createdById, tickets.assignedTo
 - articles.slug (unique)
- Connection pooling (Prisma)
- Query optimization (select only needed fields)

---

## Deployment & DevOps

### Containerização (Docker)

**7 Services:**

1. **orionone-postgres**: PostgreSQL 16 (port 5432)
2. **orionone-redis**: Redis 7.2 (port 6379)
3. **orionone-meilisearch**: Meilisearch 1.9 (port 7700)
4. **orionone-mailpit**: SMTP testing (ports 1025, 8025)
5. **orionone-backend**: Nest.js API (port 3001)
6. **orionone-frontend**: Next.js app (port 3000)
7. **orionone-nginx**: Reverse proxy (port 80)

**Network**: Bridge network `orionone_network` para comunicação interna

**Volumes Persistentes:**

- `orionone_pgdata`: Database persistence
- `orionone_redis`: Cache persistence
- `orionone_meilisearch`: Search indexes

### Reverse Proxy (Nginx)

- Frontend: http://localhost → orionone-frontend:3000
- Backend API: http://localhost/api → orionone-backend:3001
- WebSocket support para real-time notifications
- Gzip compression
- Security headers (Helmet.js)

### Ambientes

**Development:**

- Hot reload (watch mode)
- Debug logging
- Mailpit para email testing
- Prisma Studio para database GUI

**Production:**

- Multi-stage Docker builds
- Environment variables via .env
- Error logging (Winston)
- Health checks (/api/health)
- Rate limiting (Throttler)

---

## Comparação com ITSM Líderes de Mercado

### vs ServiceNow

**Vantagens OrionOne:**

- Open-source e customizável
- Stack moderno (TypeScript full-stack)
- Deployment simples (Docker)
- Zero licensing costs

**Desvantagens:**

- Menos features out-of-the-box
- Sem ITIL v4 compliance completo
- Sem integração CMDB avançada (CI/CD)

### vs Jira Service Management

**Vantagens OrionOne:**

- Focado em ITSM (não project management)
- UI moderna (Shadcn-ui)
- Performance superior (React Server Components)

**Desvantagens:**

- Menos marketplace de integrações
- Sem automação Jira Automation

### vs Zendesk

**Vantagens OrionOne:**

- Self-hosted (controlo total dos dados)
- RBAC mais granular (CASL)
- Knowledge Base com version control

**Desvantagens:**

- Sem omnichannel (chat, phone, social)
- Menos analytics out-of-the-box

### Posicionamento

OrionOne é ideal para:

- **SMBs** (50-500 colaboradores)
- **Equipas IT internas** (não customer support)
- **Organizações que valorizam open-source**
- **Casos onde controlo de dados é crítico**

---

## Status de Implementação

### Week 0 (13-16 Nov) - Foundation (100% COMPLETE)

- [x] Day 1: Research & Tutorials
- [x] Day 2: Projetos criados (Nest.js 11 + Next.js 16)
- [x] Day 2: .env files configurados (DATABASE_URL, JWT_SECRET)
- [x] Day 3: Docker Compose (7 containers funcionando)
- [x] Day 3: Nginx reverse proxy
- [x] Day 4: Prisma schema (15 models)
- [x] Day 4: Migration executada: 20251113171344_init
- [x] Day 4: Health check endpoint (/api/health)
- [x] Day 4: CORS configurado

### Week 1 Monday (18 Nov) - Database (100% COMPLETE)

- [x] Prisma models revisados (15 models, 6 enums)
- [x] Indexes adicionados (email, role, status, priority)
- [x] Seed script criado (340 lines, modular, professional)
- [x] 32 permissions criadas
- [x] Role permissions mapping (ADMIN: all, AGENT: tickets+comments, USER: own tickets)
- [x] 3 test users criados
- [x] 5 categories, 5 tickets, 1 team criados
- [x] Database populated e verificado
- [x] Refactoring: Código profissional (sem emojis, constants, type-safe)

### Week 1 Tue-Fri (19-22 Nov) - Auth Module (0% PENDING)

- [ ] Tuesday: AuthModule (register, login, JWT)
- [ ] Tuesday: AllExceptionsFilter (global error handler)
- [ ] Wednesday: CASL AbilityFactory (permissions)
- [ ] Thursday: UsersModule CRUD
- [ ] Friday: UploadModule (avatar, Sharp)

### Week 2-3 (25 Nov - 6 Dec) - Frontend + Tickets (0% PENDING)

- [ ] Shadcn-ui components installation
- [ ] Login/Register pages
- [ ] Dashboard layout (sidebar + header)
- [ ] TicketsModule backend (CRUD, SLA calculation)
- [ ] Tickets frontend (list, create, detail)
- [ ] Comments system

### Week 4 (9-13 Dec) - Knowledge Base (0% PENDING)

- [ ] ArticlesModule backend
- [ ] Tiptap rich text editor
- [ ] Articles frontend
- [ ] Meilisearch integration

---

## Packages Instalados

### Backend (nest-backend/package.json)

**Production Dependencies (18):**

- @casl/ability: 6.7.3 (RBAC)
- @nestjs/common: 11.1.8
- @nestjs/config: 4.0.2 (environment variables)
- @nestjs/core: 11.1.8
- @nestjs/jwt: 11.0.1 (JWT tokens)
- @nestjs/passport: 11.0.5 (authentication)
- @nestjs/platform-express: 11.1.8
- @nestjs/swagger: 11.2.1 (API docs)
- @nestjs/throttler: 6.4.0 (rate limiting)
- @prisma/client: 6.19.0 (ORM)
- bcrypt: 6.0.0 (password hashing)
- class-transformer: 0.5.1
- class-validator: 0.14.2
- compression: 1.8.1 (gzip)
- helmet: 8.1.0 (security headers)
- passport: 0.7.0
- passport-jwt: 4.0.1
- prisma: 6.19.0

**Dev Dependencies (23):**

- @nestjs/cli: 11.0.10
- @nestjs/schematics: 11.0.9
- @nestjs/testing: 11.1.8
- @types/bcrypt: 6.0.0
- @types/compression: 1.8.0
- @types/jest: 29.5.16
- @types/node: 22.13.1
- @types/passport-jwt: 4.0.1
- @types/supertest: 6.0.2
- @typescript-eslint/eslint-plugin: 8.18.2
- @typescript-eslint/parser: 8.18.2
- eslint: 9.18.0
- eslint-config-prettier: 10.1.8
- jest: 29.7.0
- prettier: 3.4.2
- source-map-support: 0.5.21
- supertest: 7.0.0
- ts-jest: 29.2.5
- ts-loader: 9.5.1
- ts-node: 10.9.2
- tsconfig-paths: 4.2.0
- typescript: 5.7.3

**Scripts:**

- npm run start:dev (development mode with watch)
- npm run prisma:migrate (run migrations)
- npm run prisma:seed (seed database)
- npm run prisma:studio (Prisma Studio UI)
- npm run test (Jest tests)

### Frontend (next-frontend/package.json)

**Production Dependencies (11):**

- @hookform/resolvers: 5.2.2 (form validation)
- @tanstack/react-query: 5.90.8 (server state)
- axios: 1.13.2 (HTTP client)
- class-variance-authority: 0.7.1 (CVA)
- clsx: 2.1.1 (classnames)
- lucide-react: 0.553.0 (icons)
- next: 16.0.3
- react: 19.2.0
- react-dom: 19.2.0
- react-hook-form: 7.66.0
- tailwind-merge: 3.4.0
- zod: 4.1.12 (schema validation)
- zustand: 5.0.8 (state management)

**Dev Dependencies (9):**

- @tailwindcss/postcss: 4
- @types/node: 20
- @types/react: 19
- @types/react-dom: 19
- babel-plugin-react-compiler: 1.0.0
- eslint: 9
- eslint-config-next: 16.0.3
- tailwindcss: 4
- tw-animate-css: 1.4.0
- typescript: 5

**Scripts:**

- npm run dev (development server)
- npm run build (production build)
- npm run start (production server)

---

## Referências

### Documentação Oficial

- [Next.js 16 Docs](https://nextjs.org/docs)
- [Nest.js 11 Docs](https://docs.nestjs.com)
- [Prisma 6 Docs](https://www.prisma.io/docs)
- [Shadcn-ui](https://ui.shadcn.com)
- [Tailwind CSS 4](https://tailwindcss.com/docs)
- [React 19 Docs](https://react.dev)

### Documentação do Projeto

**Migração:**

- `MIGRATION-PART-1-SETUP.md` - Infrastructure & Setup
- `MIGRATION-PART-2-BACKEND.md` - Nest.js + Prisma Backend
- `MIGRATION-PART-3-FRONTEND.md` - Next.js + React Frontend
- `MIGRATION-PART-4-TIMELINE.md` - 10-week development plan
- `MIGRATION-PART-5-CLEANUP.md` - Cleanup & Laravel archive
- `MIGRATION-VALIDATION.md` - Status validation (CURRENT)

**Business:**

- `business-model.md` - Business model & MVP scope
- `requirements.md` - Functional requirements
- `database-schema.md` - Database design & ERD
- `implementation-checklist.md` - Sprint checklist

**Setup:**

- `SETUP.md` - Development environment setup
- `DEPLOYMENT.md` - Production deployment guide
- `CONTRIBUTING.md` - Contributing guidelines

### Git Repository

- Branch atual: `feat/migrate-nextjs-nestjs`
- Last commit: `c917b91d` - "refactor: professional seed + install security packages"
- Laravel backup tag: `v0.1.0-laravel`
- Repository: https://github.com/JMSS95/OrionOne

---

**Última atualização**: 13 Nov 2024
**Versão**: v0.2.0 (Week 0 + Week 1 Monday)
**Mantido por**: [@JMSS95](https://github.com/JMSS95)
**Status**: READY FOR SPRINT 1 (Week 1 Tuesday - Auth Module)
