# Database Schema - OrionOne ITSM

**Última Atualização:** 13 Novembro 2025
**Status:** Implementado & Testado (Sprint 0 - Week 1)
**Database:** PostgreSQL 18.0 (Alpine)
**ORM:** Prisma 6.19.0
**Models:** 15 | **Enums:** 6 | **Relations:** 28
**Optimization:** Indexes, Foreign Keys, Soft Deletes

---

## Overview da Implementação

### Stack Database

- **PostgreSQL 18.0** - RDBMS enterprise com JSONB, full-text search, partitioning, enhanced vacuum
- **Prisma 6.19.0** - Type-safe ORM com Prisma Client gerado, totalmente compatível com PG18
- **UUID v4** - Identificadores únicos distribuídos (não BIGSERIAL)
- **Enums nativos** - PostgreSQL enums para type safety
- **Indexes estratégicos** - Single, composite e partial indexes
- **Bcrypt v6.0.0** - Password hashing com security fixes (CVE-2025)

### Estatísticas

```
 15 Models (Users, Tickets, KB, CMDB, Activity)
 3 Roles (ADMIN, AGENT, USER)
 32 Permissions seeded
 6 Status (OPEN → CLOSED)
 4 Priorities (LOW → URGENT)
 15 Tabelas PostgreSQL
 28 Relations (1:N, N:M, self-referencing)
 25+ Indexes (single, composite, unique)
 Foreign Keys com Cascade Rules
 Soft Deletes em todos os models principais
 JSONB para campos customizáveis
```

### Otimizações Implementadas

- **Indexes Estratégicos**: 25+ indexes (B-tree) em campos de alta consulta
- **Composite Indexes**: `(status, priority)` para queries complexas
- **Foreign Key Indexes**: Todos os FKs indexados para JOIN performance
- **Unique Constraints**: `email`, `ticket_number` com indexes únicos
- **Cascade Rules**: DELETE CASCADE, SET NULL, RESTRICT configurados
- **Soft Deletes**: `deletedAt` em Users, Tickets, Categories, etc
- **JSONB Fields**: `customFields` com suporte a GIN indexes (futuro)
- **Enum Types**: PostgreSQL native enums (4 bytes vs VARCHAR)
- **UUID v4**: IDs não-sequenciais, distribuídos, security-friendly

---

## Arquitetura de Dados

### Domínios ITSM

```

 ORIONONE ITSM DATABASE 

1⃣ AUTHENTICATION & AUTHORIZATION
 User (users)
 Permission (permissions)
 RoleHasPermission (role_has_permissions)

2⃣ INCIDENT MANAGEMENT
 Ticket (tickets)
 Comment (comments)
 Category (categories)

3⃣ TEAM COLLABORATION
 Team (teams)
 TeamMember (team_members)

4⃣ KNOWLEDGE BASE
 Article (articles)
 ArticleVersion (article_versions)

5⃣ ASSET MANAGEMENT (CMDB)
 Asset (assets)

6⃣ SYSTEM
 Media (media) - File uploads polymorphic
 ActivityLog (activity_log) - Audit trail
 Notification (notifications) - User alerts
```

---

## Models Detalhados

### 1⃣ Authentication & Authorization

#### Model: User

**Propósito:** Utilizadores do sistema (Admin, Agent, End-User)

**Schema Prisma:**

```prisma
model User {
 id String @id @default(uuid())
 name String
 email String @unique
 emailVerifiedAt DateTime? @map("email_verified_at")
 password String // bcrypt hash
 rememberToken String? @map("remember_token")
 avatar String? // URL or path
 isActive Boolean @default(true)
 role Role @default(USER) // ADMIN | AGENT | USER
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 deletedAt DateTime? // Soft delete

 // Relations (8 types)
 ticketsCreated Ticket[] @relation("TicketRequester")
 ticketsAssigned Ticket[] @relation("TicketAssignee")
 comments Comment[]
 articles Article[]
 teamMembers TeamMember[]
 activityLogs ActivityLog[]
 assets Asset[]
 notifications Notification[]

 @@index([email])
 @@index([role])
 @@index([isActive])
 @@map("users")
}

enum Role {
 ADMIN // Full system access
 AGENT // Manage tickets, KB, assets
 USER // Create tickets, view KB
}
```

**Campos Chave:**

- `role`: Enum direto (simplificação de Spatie Permission)
- `emailVerifiedAt`: Email verification (opcional)
- `isActive`: Enable/disable account sem delete
- `deletedAt`: Soft delete para auditoria

**Indexes:**

- `email`: UNIQUE index para login
- `role`: Filter by role queries
- `isActive`: Active users dashboard

**Seed Data (Week 1 Monday):**

```typescript
// 3 users criados
admin@orionone.test // Role: ADMIN
agent@orionone.test // Role: AGENT
user@orionone.test // Role: USER
// Password: bcrypt("password123")
```

**Queries Comuns:**

```typescript
// Login
const user = await prisma.user.findUnique({ where: { email } });

// Active agents
const agents = await prisma.user.findMany({
 where: { role: "AGENT", isActive: true, deletedAt: null },
});

// User with tickets
const userWithTickets = await prisma.user.findUnique({
 where: { id },
 include: { ticketsCreated: true, ticketsAssigned: true },
});
```

---

#### Model: Permission

**Propósito:** Permissões granulares RBAC (usado com CASL no frontend)

**Schema Prisma:**

```prisma
model Permission {
 id String @id @default(uuid())
 name String @unique // "tickets:create", "tickets:delete"
 guardName String @map("guard_name") // "api" (JWT)
 description String?
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 roles RoleHasPermission[]

 @@map("permissions")
}
```

**Convenção de Nomes:** `resource:action`

```
tickets:view, tickets:create, tickets:update, tickets:delete
tickets:assign, tickets:close
comments:create, comments:delete
users:view, users:manage
articles:publish
```

**Seed Data (32 permissions):**

```typescript
// Tickets: 6 permissions
tickets:view, tickets:create, tickets:update, tickets:delete,
tickets:assign, tickets:close

// Comments: 3 permissions
comments:create, comments:update, comments:delete

// Categories: 4 permissions
categories:view, categories:create, categories:update, categories:delete

// Teams: 5 permissions
teams:view, teams:create, teams:update, teams:delete, teams:manage-members

// Articles: 5 permissions
articles:view, articles:create, articles:update, articles:delete, articles:publish

// Assets: 5 permissions
assets:view, assets:create, assets:update, assets:delete, assets:assign

// Users: 4 permissions
users:view, users:create, users:update, users:delete
```

---

#### Model: RoleHasPermission

**Propósito:** Mapping N:M entre Role enum e Permissions

**Schema Prisma:**

```prisma
model RoleHasPermission {
 id String @id @default(uuid())
 roleName Role // ADMIN, AGENT, USER (enum)
 permissionId String
 permission Permission @relation(fields: [permissionId], references: [id], onDelete: Cascade)

 @@unique([roleName, permissionId])
 @@map("role_has_permissions")
}
```

**Diferença do Spatie Permission:**

- Laravel: `roles` table + `model_has_roles` pivot
- Prisma: Role enum + RoleHasPermission mapping

**Seed Data (permissions por role):**

```typescript
ADMIN: todas 32 permissions
AGENT: 20 permissions (tickets, comments, categories, teams, articles)
USER: 5 permissions (tickets:view, tickets:create, comments:create,
 articles:view, categories:view)
```

**Query Permissions:**

```typescript
// Get permissions for role
const permissions = await prisma.roleHasPermission.findMany({
 where: { roleName: "AGENT" },
 include: { permission: true },
});

// Check permission
const hasPermission = await prisma.roleHasPermission.findFirst({
 where: {
 roleName: user.role,
 permission: { name: "tickets:delete" },
 },
});
```

---

### 2⃣ Incident Management

#### Model: Ticket

**Propósito:** Tickets/Incidentes ITSM com SLA tracking

**Schema Prisma:**

```prisma
model Ticket {
 id String @id @default(uuid())
 ticketNumber String @unique // TKT-00001, TKT-00002
 title String
 description String @db.Text
 status TicketStatus @default(OPEN)
 priority TicketPriority @default(MEDIUM)
 requesterId String
 assignedTo String?
 teamId String?
 categoryId String?

 // SLA Tracking
 firstResponseAt DateTime?
 firstResponseDeadline DateTime?
 resolutionDeadline DateTime?
 resolvedAt DateTime?
 closedAt DateTime?
 isEscalated Boolean @default(false)

 customFields Json? // JSONB para campos dinâmicos
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 deletedAt DateTime?

 // Relations
 requester User @relation("TicketRequester", fields: [requesterId], references: [id])
 assignee User? @relation("TicketAssignee", fields: [assignedTo], references: [id])
 team Team? @relation(fields: [teamId], references: [id])
 category Category? @relation(fields: [categoryId], references: [id])
 comments Comment[]
 attachments Media[]
 activities ActivityLog[]

 @@index([ticketNumber])
 @@index([status, priority]) // Dashboard queries
 @@index([requesterId])
 @@index([assignedTo])
 @@index([teamId])
 @@index([createdAt])
 @@map("tickets")
}

enum TicketStatus {
 OPEN // Novo ticket criado
 IN_PROGRESS // Agent trabalhando
 ON_HOLD // Aguardando terceiros
 RESOLVED // Resolvido (aguarda confirmação)
 CLOSED // Fechado definitivamente
 CANCELLED // Cancelado pelo requester
}

enum TicketPriority {
 LOW // SLA: 48h
 MEDIUM // SLA: 24h
 HIGH // SLA: 8h
 URGENT // SLA: 2h
}
```

**Campos Chave:**

- `ticketNumber`: Identificador amigável (TKT-00001)
- `customFields`: JSONB para campos dinâmicos por categoria
- `firstResponseDeadline`: SLA primeira resposta
- `resolutionDeadline`: SLA resolução
- `isEscalated`: Flag para tickets escalados

**Indexes Estratégicos:**

```sql
-- Composite index para dashboard
CREATE INDEX idx_tickets_status_priority ON tickets(status, priority);

-- Dashboard query otimizada
SELECT * FROM tickets
WHERE status IN ('OPEN', 'IN_PROGRESS')
AND deleted_at IS NULL
ORDER BY priority DESC, created_at ASC;
-- Usa idx_tickets_status_priority
```

**Seed Data (5 tickets):**

```typescript
TKT-00001: OPEN, HIGH, assigned to agent
TKT-00002: IN_PROGRESS, MEDIUM, assigned to agent
TKT-00003: ON_HOLD, LOW, no assignee
TKT-00004: RESOLVED, URGENT, resolved 1h ago
TKT-00005: CLOSED, MEDIUM, closed 2d ago
```

**Queries Comuns:**

```typescript
// Open tickets por priority
const openTickets = await prisma.ticket.findMany({
 where: { status: "OPEN", deletedAt: null },
 orderBy: [{ priority: "desc" }, { createdAt: "asc" }],
 include: { requester: true, assignee: true, category: true },
});

// Tickets overdue (SLA breached)
const overdueTickets = await prisma.ticket.findMany({
 where: {
 status: { in: ["OPEN", "IN_PROGRESS"] },
 resolutionDeadline: { lt: new Date() },
 resolvedAt: null,
 },
});

// Agent workload
const workload = await prisma.ticket.groupBy({
 by: ["assignedTo", "status"],
 where: { status: { in: ["OPEN", "IN_PROGRESS"] } },
 _count: true,
});
```

**Workflow Automático (Future - Triggers):**

```sql
-- Auto-calculate SLA deadlines baseado em priority
CREATE OR REPLACE FUNCTION calculate_sla_deadlines()
RETURNS TRIGGER AS $$
BEGIN
 NEW.first_response_deadline := CASE NEW.priority
 WHEN 'URGENT' THEN NEW.created_at + INTERVAL '30 minutes'
 WHEN 'HIGH' THEN NEW.created_at + INTERVAL '2 hours'
 WHEN 'MEDIUM' THEN NEW.created_at + INTERVAL '8 hours'
 WHEN 'LOW' THEN NEW.created_at + INTERVAL '24 hours'
 END;

 NEW.resolution_deadline := CASE NEW.priority
 WHEN 'URGENT' THEN NEW.created_at + INTERVAL '2 hours'
 WHEN 'HIGH' THEN NEW.created_at + INTERVAL '8 hours'
 WHEN 'MEDIUM' THEN NEW.created_at + INTERVAL '24 hours'
 WHEN 'LOW' THEN NEW.created_at + INTERVAL '48 hours'
 END;

 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tickets_sla_deadlines
BEFORE INSERT ON tickets
FOR EACH ROW
EXECUTE FUNCTION calculate_sla_deadlines();
```

---

#### Model: Category

**Propósito:** Categorias hierárquicas para tickets e articles

**Schema Prisma:**

```prisma
model Category {
 id String @id @default(uuid())
 name String
 slug String @unique
 description String?
 parentId String? // Self-referencing (hierarquia)
 order Int @default(0)
 isActive Boolean @default(true)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 parent Category? @relation("CategoryHierarchy", fields: [parentId], references: [id])
 children Category[] @relation("CategoryHierarchy")
 tickets Ticket[]
 articles Article[]

 @@index([slug])
 @@index([parentId])
 @@map("categories")
}
```

**Hierarquia (Tree Structure):**

```
Hardware
 Laptops
 Desktops
 Printers

Software
 Microsoft Office
 Adobe Suite
 Browsers

Network
 Wi-Fi
 VPN
```

**Seed Data (5 categories):**

```typescript
Hardware, Software, Network, Security, Other;
// Flat structure no MVP (hierarquia futura)
```

**Queries Comuns:**

```typescript
// Categories com count de tickets
const categoriesWithCount = await prisma.category.findMany({
 where: { isActive: true },
 include: {
 _count: { select: { tickets: true, articles: true } },
 },
 orderBy: { order: "asc" },
});

// Tree structure (recursive)
const tree = await prisma.category.findMany({
 where: { parentId: null },
 include: {
 children: {
 include: { children: true }, // 3 levels
 },
 },
});
```

---

#### Model: Comment

**Propósito:** Comentários em tickets (public/internal)

**Schema Prisma:**

```prisma
model Comment {
 id String @id @default(uuid())
 ticketId String
 userId String
 content String @db.Text
 isInternal Boolean @default(false) // Internal notes (agents only)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 deletedAt DateTime?

 ticket Ticket @relation(fields: [ticketId], references: [id], onDelete: Cascade)
 user User @relation(fields: [userId], references: [id])
 attachments Media[]
 activities ActivityLog[]

 @@index([ticketId])
 @@index([userId])
 @@index([createdAt])
 @@map("comments")
}
```

**Campos Chave:**

- `isInternal`: Notas internas (visível apenas para agents)
- `onDelete: Cascade`: Apagar comments se ticket for deletado

**Seed Data (5 comments):**

```typescript
// 5 comments distribuídos nos tickets
// Mix de public e internal
```

**Queries Comuns:**

```typescript
// Public comments para ticket
const publicComments = await prisma.comment.findMany({
 where: { ticketId, isInternal: false, deletedAt: null },
 include: { user: { select: { id: true, name: true, avatar: true } } },
 orderBy: { createdAt: "asc" },
});

// All comments (agents only)
const allComments = await prisma.comment.findMany({
 where: { ticketId, deletedAt: null },
 include: { user: true, attachments: true },
 orderBy: { createdAt: "asc" },
});
```

---

### 3⃣ Team Collaboration

#### Model: Team

**Propósito:** Equipas de suporte especializadas

**Schema Prisma:**

```prisma
model Team {
 id String @id @default(uuid())
 name String
 slug String @unique
 description String?
 email String? // Team email (support@hardware.company.com)
 isActive Boolean @default(true)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 members TeamMember[]
 tickets Ticket[]

 @@index([slug])
 @@map("teams")
}
```

**Exemplos:**

```
Hardware Team (hardware)
Software Team (software)
Network Team (network)
Security Team (security)
```

**Seed Data (1 team):**

```typescript
{
 name: "Support Team",
 slug: "support",
 members: 2 (admin, agent)
}
```

---

#### Model: TeamMember

**Propósito:** Membros de equipas com roles (LEAD, MEMBER)

**Schema Prisma:**

```prisma
model TeamMember {
 id String @id @default(uuid())
 teamId String
 userId String
 role TeamRole @default(MEMBER)
 joinedAt DateTime @default(now())

 team Team @relation(fields: [teamId], references: [id], onDelete: Cascade)
 user User @relation(fields: [userId], references: [id], onDelete: Cascade)

 @@unique([teamId, userId])
 @@map("team_members")
}

enum TeamRole {
 LEAD // Team leader
 MEMBER // Regular member
}
```

**Queries Comuns:**

```typescript
// Team members with user data
const teamMembers = await prisma.teamMember.findMany({
 where: { teamId },
 include: {
 user: { select: { id: true, name: true, email: true, avatar: true } },
 },
 orderBy: { role: "asc" }, // LEADs first
});

// User teams
const userTeams = await prisma.teamMember.findMany({
 where: { userId },
 include: { team: true },
});
```

---

### 4⃣ Knowledge Base

#### Model: Article

**Propósito:** Artigos da Knowledge Base com versioning

**Schema Prisma:**

```prisma
model Article {
 id String @id @default(uuid())
 title String
 slug String @unique
 content String @db.Text // Markdown/HTML
 excerpt String?
 categoryId String
 authorId String
 isPublished Boolean @default(false)
 viewCount Int @default(0)
 helpfulVotes Int @default(0) // "Was helpful" counter
 notHelpfulVotes Int @default(0) // "Not helpful" counter
 publishedAt DateTime?
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 deletedAt DateTime?

 category Category @relation(fields: [categoryId], references: [id])
 author User @relation(fields: [authorId], references: [id])
 versions ArticleVersion[]

 @@index([slug])
 @@index([categoryId])
 @@index([authorId])
 @@index([isPublished])
 @@map("articles")
}
```

**Campos Chave:**

- `slug`: URL-friendly (how-to-reset-password)
- `isPublished`: Draft vs Published
- `helpfulVotes` / `notHelpfulVotes`: Feedback system
- `viewCount`: Analytics

**Queries Comuns:**

```typescript
// Published articles
const articles = await prisma.article.findMany({
 where: { isPublished: true, deletedAt: null },
 include: {
 category: true,
 author: { select: { name: true, avatar: true } },
 },
 orderBy: { publishedAt: "desc" },
});

// Popular articles
const popular = await prisma.article.findMany({
 where: { isPublished: true },
 orderBy: [{ viewCount: "desc" }, { helpfulVotes: "desc" }],
 take: 10,
});

// Search articles (future - full-text)
const results = await prisma.article.findMany({
 where: {
 isPublished: true,
 OR: [
 { title: { contains: query, mode: "insensitive" } },
 { content: { contains: query, mode: "insensitive" } },
 ],
 },
});
```

---

#### Model: ArticleVersion

**Propósito:** Versioning histórico de articles

**Schema Prisma:**

```prisma
model ArticleVersion {
 id String @id @default(uuid())
 articleId String
 title String
 content String @db.Text
 version Int // 1, 2, 3, ...
 createdAt DateTime @default(now())

 article Article @relation(fields: [articleId], references: [id], onDelete: Cascade)

 @@index([articleId])
 @@map("article_versions")
}
```

**Usage:**

- Guardar snapshot quando article é editado
- Rollback para versão anterior
- Audit trail de mudanças

---

### 5⃣ Asset Management (CMDB)

#### Model: Asset

**Propósito:** Configuration Management Database (IT assets)

**Schema Prisma:**

```prisma
model Asset {
 id String @id @default(uuid())
 assetTag String @unique // AST-00001
 name String
 type AssetType
 manufacturer String?
 model String?
 serialNumber String?
 purchaseDate DateTime?
 purchaseCost Decimal? @db.Decimal(10, 2)
 warrantyExpiry DateTime?
 status AssetStatus @default(AVAILABLE)
 assignedTo String?
 location String?
 notes String? @db.Text
 customFields Json? // JSONB para campos específicos
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt
 deletedAt DateTime?

 assignedUser User? @relation(fields: [assignedTo], references: [id])

 @@index([assetTag])
 @@index([type])
 @@index([status])
 @@index([assignedTo])
 @@map("assets")
}

enum AssetType {
 LAPTOP
 DESKTOP
 SERVER
 LICENSE // Software licenses
 MOBILE
 NETWORK // Routers, switches
}

enum AssetStatus {
 AVAILABLE // Não atribuído
 IN_USE // Atribuído a user
 MAINTENANCE // Em manutenção
 RETIRED // Descontinuado
}
```

**Campos Chave:**

- `assetTag`: Identificador físico (etiqueta)
- `customFields`: JSONB (specs técnicas: RAM, CPU, storage)
- `purchaseCost`: Decimal(10,2) para precisão financeira
- `warrantyExpiry`: Tracking de garantias

**Queries Comuns:**

```typescript
// Available assets
const available = await prisma.asset.findMany({
 where: { status: "AVAILABLE", deletedAt: null },
 orderBy: { type: "asc" },
});

// User assets
const userAssets = await prisma.asset.findMany({
 where: { assignedTo: userId },
 include: { assignedUser: { select: { name: true, email: true } } },
});

// Warranty expiring soon
const expiring = await prisma.asset.findMany({
 where: {
 warrantyExpiry: {
 gte: new Date(),
 lte: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
 },
 },
});
```

---

### 6⃣ System Models

#### Model: Media (Polymorphic)

**Propósito:** File uploads (avatars, attachments)

**Schema Prisma:**

```prisma
model Media {
 id String @id @default(uuid())
 modelType String // "Ticket", "Comment", "User"
 modelId String // UUID do model
 collection String // "attachments", "avatars"
 name String
 fileName String
 mimeType String
 disk String @default("public")
 size Int // bytes
 customProperties Json?
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 ticket Ticket? @relation(fields: [modelId], references: [id])
 comment Comment? @relation(fields: [modelId], references: [id])

 @@index([modelType, modelId])
 @@map("media")
}
```

**Polymorphic Pattern:**

```typescript
// Upload avatar (User)
await prisma.media.create({
 data: {
 modelType: "User",
 modelId: userId,
 collection: "avatars",
 name: "profile.jpg",
 fileName: "uuid-profile.jpg",
 mimeType: "image/jpeg",
 size: 125000,
 },
});

// Upload attachment (Ticket)
await prisma.media.create({
 data: {
 modelType: "Ticket",
 modelId: ticketId,
 collection: "attachments",
 name: "screenshot.png",
 fileName: "uuid-screenshot.png",
 mimeType: "image/png",
 size: 450000,
 },
});
```

---

#### Model: ActivityLog (Audit Trail)

**Propósito:** Audit trail completo do sistema

**Schema Prisma:**

```prisma
model ActivityLog {
 id String @id @default(uuid())
 logName String? // "ticket", "user", "asset"
 description String // "Ticket #TKT-00001 created"
 subjectType String? // "Ticket", "Comment"
 subjectId String?
 causerId String? // User que causou a ação
 properties Json? // { old: {}, new: {} }
 event String? // "created", "updated", "deleted"
 batchUuid String? // Agrupar ações relacionadas
 createdAt DateTime @default(now())

 causer User? @relation(fields: [causerId], references: [id])
 ticket Ticket? @relation(fields: [subjectId], references: [id])
 comment Comment? @relation(fields: [subjectId], references: [id])

 @@index([logName])
 @@index([subjectType, subjectId])
 @@index([causerId])
 @@index([createdAt])
 @@map("activity_log")
}
```

**Example Logs:**

```typescript
{
 logName: "ticket",
 description: "Ticket #TKT-00001 status changed from OPEN to IN_PROGRESS",
 subjectType: "Ticket",
 subjectId: "ticket-uuid",
 causerId: "agent-uuid",
 event: "updated",
 properties: {
 old: { status: "OPEN" },
 new: { status: "IN_PROGRESS" }
 }
}
```

---

#### Model: Notification

**Propósito:** Notificações in-app para users

**Schema Prisma:**

```prisma
model Notification {
 id String @id @default(uuid())
 userId String
 type String // "ticket_assigned", "comment_added"
 title String
 message String @db.Text
 data Json? // { ticketId, ticketNumber }
 readAt DateTime?
 createdAt DateTime @default(now())

 user User @relation(fields: [userId], references: [id], onDelete: Cascade)

 @@index([userId])
 @@index([readAt])
 @@map("notifications")
}
```

**Notification Types:**

```typescript
ticket_assigned; // "Ticket #TKT-00001 assigned to you"
ticket_updated; // "Ticket #TKT-00001 updated by Admin"
comment_added; // "New comment on ticket #TKT-00001"
ticket_resolved; // "Ticket #TKT-00001 marked as resolved"
mention; // "@john mentioned you in ticket #TKT-00001"
```

---

## Indexes & Performance

### Strategy

1. **Single Indexes** - Campos únicos e foreign keys
2. **Composite Indexes** - Queries com múltiplos filtros
3. **Partial Indexes** - Subset de dados (WHERE condition)

### Implemented Indexes

```prisma
// User indexes
@@index([email]) // Login queries
@@index([role]) // Filter by role
@@index([isActive]) // Active users

// Ticket indexes
@@index([ticketNumber]) // Lookup by TKT-00001
@@index([status, priority]) // Dashboard (composite)
@@index([requesterId]) // User's tickets
@@index([assignedTo]) // Agent's workload
@@index([teamId]) // Team tickets
@@index([createdAt]) // Sort by date

// Category indexes
@@index([slug]) // URL lookup
@@index([parentId]) // Tree queries

// Comment indexes
@@index([ticketId]) // Ticket comments
@@index([userId]) // User activity
@@index([createdAt]) // Timeline

// Asset indexes
@@index([assetTag]) // Physical lookup
@@index([type]) // Filter by type
@@index([status]) // Available assets
@@index([assignedTo]) // User assets

// ActivityLog indexes
@@index([logName]) // Filter by entity
@@index([subjectType, subjectId]) // Entity history (composite)
@@index([causerId]) // User activity
@@index([createdAt]) // Timeline

// Notification indexes
@@index([userId]) // User notifications
@@index([readAt]) // Unread filter
```

### Future Indexes (Post-MVP)

```sql
-- Full-text search (PostgreSQL)
CREATE INDEX idx_tickets_fulltext ON tickets
USING GIN(to_tsvector('english', title || ' ' || description));

CREATE INDEX idx_articles_fulltext ON articles
USING GIN(to_tsvector('english', title || ' ' || content));

-- JSONB indexes
CREATE INDEX idx_tickets_custom_fields ON tickets
USING GIN(custom_fields);

CREATE INDEX idx_assets_custom_fields ON assets
USING GIN(custom_fields);

-- Partial indexes (active records only)
CREATE INDEX idx_users_active_agents ON users(role, name)
WHERE is_active = true AND role = 'AGENT' AND deleted_at IS NULL;

CREATE INDEX idx_tickets_open ON tickets(priority, created_at)
WHERE status IN ('OPEN', 'IN_PROGRESS') AND deleted_at IS NULL;
```

---

## Prisma Queries Avançadas

### Aggregations

```typescript
// Ticket stats
const stats = await prisma.ticket.aggregate({
 where: { deletedAt: null },
 _count: { id: true },
 _avg: {
 /* SLA calculations */
 },
});

// Tickets by status
const byStatus = await prisma.ticket.groupBy({
 by: ["status"],
 _count: true,
 orderBy: { _count: { id: "desc" } },
});
```

### Transactions

```typescript
// Assign ticket + create activity log
await prisma.$transaction([
 prisma.ticket.update({
 where: { id: ticketId },
 data: { assignedTo: agentId, status: "IN_PROGRESS" },
 }),
 prisma.activityLog.create({
 data: {
 logName: "ticket",
 description: `Ticket assigned to ${agent.name}`,
 subjectType: "Ticket",
 subjectId: ticketId,
 causerId: currentUserId,
 event: "updated",
 },
 }),
]);
```

### Nested Writes

```typescript
// Create ticket with comment
await prisma.ticket.create({
 data: {
 title: "Laptop not working",
 description: "Screen is black",
 ticketNumber: "TKT-00010",
 requesterId: userId,
 status: "OPEN",
 priority: "HIGH",
 comments: {
 create: {
 userId: userId,
 content: "Tried restarting but no luck",
 isInternal: false,
 },
 },
 },
});
```

---

## Migration & Seeding

### Prisma Migrate

```bash
# Create migration
cd nest-backend
npx prisma migrate dev --name init

# Apply production
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset
```

### Seeding

**Arquivo:** `nest-backend/prisma/seed.ts`

```typescript
import { PrismaClient } from "@prisma/client";
import * as bcrypt from "bcrypt";

const prisma = new PrismaClient();

async function main() {
 // 1. Create permissions (32)
 await createPermissions();

 // 2. Assign role permissions
 await assignRolePermissions();

 // 3. Create users (3)
 await createUsers();

 // 4. Create categories (5)
 await createCategories();

 // 5. Create tickets (5)
 await createTickets();

 // 6. Create comments (5)
 await createComments();

 // 7. Create team (1)
 await createTeam();
}

main()
 .catch(console.error)
 .finally(() => prisma.$disconnect());
```

**Execute:**

```bash
cd nest-backend
npm run prisma:seed
```

---

## Database Performance Tips

### 1. Connection Pooling

```env
DATABASE_URL="postgresql://user:pass@localhost:5432/orionone?schema=public&connection_limit=10&pool_timeout=20"
```

### 2. Query Optimization

```typescript
// N+1 Problem
const tickets = await prisma.ticket.findMany();
for (const ticket of tickets) {
 const user = await prisma.user.findUnique({
 where: { id: ticket.requesterId },
 });
}

// Include relation
const tickets = await prisma.ticket.findMany({
 include: { requester: true, assignee: true },
});
```

### 3. Select Specific Fields

```typescript
// Fetch all fields
const users = await prisma.user.findMany();

// Select only needed
const users = await prisma.user.findMany({
 select: { id: true, name: true, email: true },
});
```

### 4. Pagination

```typescript
// Cursor-based (melhor performance)
const tickets = await prisma.ticket.findMany({
 take: 20,
 skip: 1,
 cursor: { id: lastTicketId },
 orderBy: { createdAt: "desc" },
});

// Offset-based (mais simples)
const tickets = await prisma.ticket.findMany({
 take: 20,
 skip: (page - 1) * 20,
});
```

---

## Security Considerations

### 1. Soft Deletes

```typescript
// Middleware para excluir soft deleted automaticamente
prisma.$use(async (params, next) => {
 if (params.action === "findMany" || params.action === "findFirst") {
 params.args.where = { ...params.args.where, deletedAt: null };
 }
 return next(params);
});
```

### 2. Input Validation

```typescript
// Use class-validator + class-transformer
import { IsEmail, IsNotEmpty, MinLength } from "class-validator";

export class CreateUserDto {
 @IsNotEmpty()
 name: string;

 @IsEmail()
 email: string;

 @MinLength(8)
 password: string;
}
```

### 3. SQL Injection Prevention

Prisma previne SQL injection automaticamente (parameterized queries).

```typescript
// Safe (Prisma)
await prisma.user.findMany({ where: { email } });

// Unsafe (raw SQL sem sanitização)
await prisma.$queryRaw`SELECT * FROM users WHERE email = ${email}`;

// Safe (raw SQL com parametrização)
await prisma.$queryRaw`SELECT * FROM users WHERE email = ${Prisma.sql`${email}`}`;
```

---

## Otimizações de Performance

### Indexes Estratégicos Implementados

**Users Table (Alta Frequência de Consultas)**

```sql
-- Autenticação (lookup por email)
CREATE INDEX "users_email_idx" ON users(email);
CREATE UNIQUE INDEX "users_email_key" ON users(email);

-- Filtros de autorização
CREATE INDEX "users_role_idx" ON users(role);
CREATE INDEX "users_is_active_idx" ON users(is_active);
```

**Tickets Table (Core ITSM)**

```sql
-- Business identifier
CREATE UNIQUE INDEX "tickets_ticket_number_key" ON tickets(ticket_number);
CREATE INDEX "tickets_ticket_number_idx" ON tickets(ticket_number);

-- Composite index para dashboard queries (status + priority)
CREATE INDEX "tickets_status_priority_idx" ON tickets(status, priority);

-- Foreign keys para joins frequentes
CREATE INDEX "tickets_requester_id_idx" ON tickets(requester_id);
CREATE INDEX "tickets_assigned_to_idx" ON tickets(assigned_to);
CREATE INDEX "tickets_team_id_idx" ON tickets(team_id);

-- Ordenação temporal
CREATE INDEX "tickets_created_at_idx" ON tickets(created_at);
```

**Comments Table (High Volume)**

```sql
-- Parent lookups
CREATE INDEX "comments_ticket_id_idx" ON comments(ticket_id);
CREATE INDEX "comments_user_id_idx" ON comments(user_id);

-- Ordenação temporal
CREATE INDEX "comments_created_at_idx" ON comments(created_at);
```

### Foreign Keys com Cascade Rules

**Delete Cascade (Dados dependentes)**

```prisma
// Quando user é deletado, suas notificações também são
notifications Notification[] // ON DELETE CASCADE

// Quando ticket é deletado, comments também são
comments Comment[] // ON DELETE CASCADE
```

**Set NULL (Dados opcionais)**

```prisma
// Quando user é deletado, tickets ficam sem assignee
assignedTo String? // ON DELETE SET NULL

// Quando team é deletado, tickets ficam sem team
teamId String? // ON DELETE SET NULL
```

**Restrict (Proteção de integridade)**

```prisma
// Não pode deletar user que criou tickets
ticketsCreated Ticket[] // ON DELETE RESTRICT

// Não pode deletar category com tickets ativos
tickets Ticket[] // ON DELETE RESTRICT
```

### Query Performance Features

**1. Soft Deletes (Preservação de Dados)**

```typescript
// Todos os models principais têm deletedAt
deletedAt DateTime? @map("deleted_at")

// Queries excluem automaticamente deleted records
await prisma.ticket.findMany({
 where: { deletedAt: null }
});
```

**2. JSONB para Custom Fields (Flexibilidade)**

```prisma
customFields Json? // PostgreSQL JSONB com GIN index support

// Permite queries JSON nativas
await prisma.ticket.findMany({
 where: {
 customFields: {
 path: ['priority'],
 equals: 'high'
 }
 }
});
```

**3. Enum Types (Type Safety + Performance)**

```sql
-- PostgreSQL enums são mais eficientes que strings
CREATE TYPE "Role" AS ENUM ('ADMIN', 'AGENT', 'USER');
CREATE TYPE "TicketStatus" AS ENUM ('OPEN', 'IN_PROGRESS', ...);

-- 4 bytes vs VARCHAR, com validação nativa
```

### Otimizações PostgreSQL 18

**Vacuum Performance (Novo em PG18)**

- Improved VACUUM performance para tabelas grandes
- Melhor gestão de bloat em tabelas com updates frequentes
- Tickets/Comments se beneficiam diretamente

**Query Parallelism**

- Parallel sequential scans para full-table queries
- Útil em relatórios e dashboards

**Partitioning (Futuro)**

```sql
-- Para escala, particionar tickets por data
CREATE TABLE tickets_2025_q1 PARTITION OF tickets
 FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
```

### Estatísticas de Uso (Seed Data)

```
 3 Users (ADMIN, AGENT, USER)
 32 Permissions seeded
 5 Categories (Hardware, Software, Network, Access, Other)
 5 Tickets (diferentes status/priorities)
 5 Comments
 1 Team (Support Team)

Total records: ~51
Database size: ~2MB (fresh install)
```

### Security Features

**Password Hashing**

- **Bcrypt v6.0.0** com security fixes
- Protegido contra CVE-2025 (password truncation >255 chars)
- Salt rounds: 10 (configurável via env)

**UUID v4 para IDs**

- Não sequenciais (security by obscurity)
- Distribuídos (multi-region ready)
- 128-bit (colisão ~0%)

**Cascade Delete Protection**

- RESTRICT em relações críticas (users → tickets)
- Previne perda acidental de dados históricos

---

## Referências

- [Prisma Documentation](https://www.prisma.io/docs)
- [PostgreSQL 18 Release Notes](https://www.postgresql.org/docs/18/release-18.html)
- [Prisma Best Practices](https://www.prisma.io/docs/guides/performance-and-optimization)
- [ITSM Best Practices (ITIL v4)](https://www.axelos.com/certifications/itil-service-management)
- [PostgreSQL Index Types](https://www.postgresql.org/docs/18/indexes-types.html)

---

**Status Final:** Database Schema 100% implementado e documentado
