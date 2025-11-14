# MVP - Roadmap & Status - OrionOne ITSM

**Date:** 13 November 2024
**Status:** Infrastructure Complete - Ready for Development
**Target Market:** SMEs (10-200 employees) - Professional ITSM
**Target Launch:** 31 January 2025 (11 weeks)
**Positioning:** Affordable ITSM Platform - Modern Stack, Open Source

---

## Executive Summary

**OrionOne MVP:**

- Incident Management (Rich Text editor + AI search)
- Comments & Attachments (file uploads)
- Knowledge Base (Meilisearch typo-tolerant search)
- Advanced SLA Management (configurable policies)
- Dashboard + Email Notifications

**Value Proposition:** Professional ITSM for growing teams ($20/agent/month)
**Differentiators:** Rich UX, AI-powered search, Modern stack, Open source

### Tech Stack - 9.5/10 (ServiceNow-Grade)

| Component | Version | Status | Notes |
| ------------------ | ------- | ---------- | ------------------------------ |
| **Next.js** | 15.5.6 | Production | App Router + Server Components |
| **Nest.js** | 11.1.8 | Production | Enterprise backend framework |
| **React** | 19.2.0 | Production | Latest framework |
| **Prisma** | 6.4.0 | Production | Type-safe ORM |
| **PostgreSQL** | 18.0 | Production | Advanced RDBMS + full-text |
| **Redis** | 8.2 | Production | Cache + sessions |
| **Meilisearch** | 1.25 | Production | AI-ready search engine |
| **TypeScript** | 5.6 | Production | Strict mode enabled |
| **Jest** | 29.x | Production | Testing framework |
| **shadcn/ui** | Latest | Configured | Accessible component library |
| **Tailwind CSS** | v4 | Production | Utility-first CSS |
| **Zod** | 4.x | Production | Schema validation |
| **TanStack Query** | 5.x | Production | Server state management |
| **Docker** | Latest | Production | Containerized development |

**Conclusion:** Stack is PRODUCTION-READY for MVP. **ITSM Score: 9.5/10** (ServiceNow-grade platform at 10% the cost).

### MVP Feature Scope

| Feature | Status | Priority |
| --------------------------- | ----------- | -------- |
| **Incident Management** | MVP | CRITICAL |
| **Rich Text Editor** | MVP | HIGH |
| **Meilisearch Integration** | MVP | HIGH |
| **Comments & Files** | MVP | HIGH |
| **Knowledge Base** | MVP | MEDIUM |
| **Advanced SLA** | MVP | MEDIUM |
| **Dashboard** | MVP | MEDIUM |
| **Teams & Assignment** | Post-MVP | P3 |
| **CMDB/Assets** | Post-MVP | P5 |
| **Advanced Analytics** | Post-MVP | P6 |
| **REST API** | Post-MVP | P4 |
| **SSO/SAML** | Post-MVP | P7 |

### Current Status

**Sprint 0:** Infrastructure Setup (Complete)
**Sprint 1:** Authentication & User Management (In Progress - 85%)

**Next Steps:**

1. Complete Sprint 1 (Auth + RBAC)
2. Deploy staging environment
3. Begin Sprint 2 (Tickets CRUD)

---

## Sprint Roadmap (0-6) - 11 Weeks Total

**Timeline:** November 16, 2024 → January 31, 2025
**Methodology:** Agile Scrum, TDD, Feature-Driven Development
**Goal:** Launch professional ITSM platform with rich UX
**Focus:** Incident management + AI search + Advanced SLA

### Sprint 0: Infrastructure Setup (COMPLETE)

**Duration:** 2 weeks (Nov 1-15, 2025)
**Status:** 100% Complete

**Deliverables:**

- Docker environment: PostgreSQL 18, Redis 8.2, Meilisearch 1.25
- Nest.js 11.1.8 backend with Prisma 6.4.0 ORM
- Next.js 15.5.6 frontend with shadcn/ui + Tailwind v4
- JWT authentication foundation + RBAC structure
- API documentation with Swagger (auto-generated)
- CI/CD pipeline with GitHub Actions

**ServiceNow Equivalent:** Platform installation + basic configuration

---

### Sprint 1: Authentication & User Management (IN PROGRESS)

**Duration:** 1 week (Nov 16-22, 2025)
**Status:** 85% Complete
**Priority:** CRITICAL
**ServiceNow Module:** User Administration + Security

**Features:**

1. **Enterprise Authentication**

 - JWT access tokens (15min) + refresh tokens (7 days)
 - Multi-factor authentication ready (hooks for post-MVP)
 - Password policies (complexity, expiration, history)
 - Bcrypt v6 password hashing (12 rounds)
 - Session management with Redis
 - Account lockout after failed attempts

2. **User Management (ServiceNow-style)**

 - User CRUD with audit logging
 - Profile management + avatar upload (S3)
 - Department/location assignment
 - User preferences (timezone, language, notifications)
 - Bulk user import/export (CSV)

3. **RBAC (ServiceNow-equivalent)**

 - Roles: ADMIN, ITIL_ADMIN, AGENT, END_USER
 - Granular permissions: 32 permissions across 8 resources
 - Role inheritance support
 - Dynamic permission checking
 - Row-level security (users see only their tickets/dept)

4. **Security Features**
 - Rate limiting (100 req/min per IP)
 - CORS configuration (whitelist domains)
 - Helmet security headers (CSP, HSTS, etc.)
 - Input validation + sanitization
 - SQL injection prevention (Prisma ORM)
 - XSS protection

**Tech Stack:**

- Backend: Nest.js Guards, Prisma middleware, JWT strategy
- Frontend: Next.js middleware, React Context, protected routes
- Security: @nestjs/throttler, Helmet, Zod validation

---

### Sprint 2: Incident Management + Rich Text (CRITICAL)

**Duration:** 2 weeks (Nov 23 - Dec 6, 2024)
**Status:** Planned
**Priority:** CRITICAL
**ServiceNow Module:** Incident Management (Professional)

**Features:**

1. **Incident CRUD (Enhanced)**

 - Create, Read, Update, Delete incidents
 - Auto-generate number: INC-YYYYMMDD-NNNN
 - Fields:
 - Title (text)
 - Description (**Tiptap rich text editor**)
 - Status: New, In Progress, Resolved, Closed
 - Priority: P1, P2, P3, P4
 - Category (single level only)
 - Assigned To (user dropdown)
 - Full validation (required fields + business rules)

2. **Rich Text Editor (Tiptap)**

 - WYSIWYG editor for incident descriptions
 - Formatting: **bold**, _italic_, lists, code blocks, links
 - Markdown shortcuts (##, \*\*, -, etc.)
 - Image paste support (auto-upload to S3)
 - Character counter + placeholder text
 - Mobile-responsive editor

3. **Meilisearch Integration**

 - Typo-tolerant search (1-2 character errors)
 - Instant search as-you-type (<50ms response)
 - Search highlights in results
 - Relevance ranking (title > description > comments)
 - Index: incidents, users, knowledge articles
 - Auto-sync on create/update (background job)

4. **Advanced Filtering**

 - Filter builder UI (multiple conditions)
 - Quick filters: My Incidents, Unassigned, Overdue
 - Saved filters (personal + team shared)
 - Filter by: Status, Priority, Assigned To, Category, Created Date
 - Sort by: Created, Updated, Priority, SLA breach risk
 - Pagination: Cursor-based (limit 50)

5. **Assignment**
 - Manual assignment to agent (dropdown)
 - Reassignment (simple update)
 - No auto-assignment (post-MVP)
 - No teams (post-MVP)

**Tech Stack:**

- Backend: Prisma complex queries, DTOs with validation, Guards, Meilisearch SDK
- Frontend: TanStack Query (caching), React Hook Form, shadcn/ui tables, **Tiptap editor**
- Search: **Meilisearch 1.25** (primary), PostgreSQL full-text (fallback)
- Validation: Zod schemas (backend + frontend)
- Storage: AWS S3 for pasted images

---

### Sprint 3: Comments & Attachments

**Duration:** 1.5 weeks (Dec 7-17, 2024)
**Status:** Planned
**Priority:** HIGH
**ServiceNow Module:** Comments + Attachments (Simplified)

**Features:**

1. **Comments (Essential)**

 - Add comment to incident (textarea)
 - List all comments (chronological)
 - No rich text (plain text only)
 - No edit/delete (append only)
 - Show: author, timestamp, comment text
 - No @mentions (post-MVP)
 - No internal vs public (all visible to agents)

2. **File Attachments (Basic)**

 - Upload files: max 3 files, 5MB each
 - Allowed: jpg, png, pdf, txt, log
 - Local storage (upload/ folder - S3 post-MVP)
 - Download individual files
 - Delete file (soft delete)
 - No drag & drop (simple file input)
 - No image preview (just filename + size)

3. **Activity Log (Minimal)**
 - Simple timeline: comments + status changes
 - No filtering
 - No export

**Tech Stack:**

- Backend: AWS S3 SDK, activity logging middleware, file validation
- Frontend: File dropzone, image preview, timeline UI component
- Storage: AWS S3 with presigned URLs (secure downloads)
- Real-time: Polling (30s interval), WebSocket option

---

### Sprint 4: Knowledge Base + Meilisearch

**Duration:** 2 weeks (Dec 18-31, 2024)
**Status:** Planned
**Priority:** MEDIUM
**ServiceNow Module:** Knowledge Management (Professional)

**Features:**

1. **Article CRUD (Enhanced)**

 - Create article: title, body (**Tiptap rich text**), category
 - Edit article (full editor)
 - Delete article (soft delete)
 - Publish/Unpublish (status field)
 - No approval workflow (post-MVP)
 - No versioning (post-MVP)

2. **Meilisearch Integration**

 - Typo-tolerant search across all articles
 - Instant search as-you-type
 - Search highlights in title + body
 - Filter by category + status
 - Sort by: Relevance, Views, Created Date
 - Auto-index on publish

3. **Categories**

 - Simple category list (single level)
 - Assign article to one category
 - No subcategories (post-MVP)
 - No tags (post-MVP)

4. **Link to Incidents**
 - Link article to incident (many-to-many)
 - Show linked articles on incident view
 - **Smart suggestions** (Meilisearch similarity)
 - No AI suggestions (post-MVP)

**Tech Stack:**

- Backend: Prisma CRUD, **Meilisearch SDK**, Tiptap JSON storage
- Frontend: **Tiptap editor**, Meilisearch InstantSearch components

---

### Sprint 5: Advanced SLA Management

**Duration:** 1.5 weeks (Jan 1-10, 2025)
**Status:** Planned
**Priority:** HIGH
**ServiceNow Module:** SLA Management (Professional)

**Features:**

1. **Configurable SLA Policies**

 - Admin UI to create/edit SLA policies
 - Different targets per priority + category combination
 - Example defaults:
 - P1 Critical: Resolve in 4 hours
 - P2 High: Resolve in 8 hours
 - P3 Medium: Resolve in 24 hours
 - P4 Low: Resolve in 72 hours
 - **Business hours calendar** (Mon-Fri 9am-5pm)
 - **Holiday calendar** (skip non-working days)
 - Multiple policies per organization

2. **SLA Automation**

 - Auto-escalation on breach risk (80% elapsed)
 - Email notifications:
 - Warning at 80% (to agent + manager)
 - Breach notification (to agent + manager + admin)
 - Escalation workflow (reassign to senior agent)
 - SLA pause/resume (on hold status)

3. **SLA Display & Tracking**

 - Real-time countdown timer (WebSocket updates)
 - Color indicators: Green (>50%), Yellow (25-50%), Red (<25%)
 - Show "Breached" with breach time
 - SLA history log (pause/resume events)
 - Dashboard widget: Breach risk incidents
 - Reports: SLA compliance % per agent/team

**Tech Stack:**

- Backend: Complex date calculation, Prisma cron jobs, Bull queue for escalations
- Frontend: Real-time countdown, color-coded badges, admin configuration UI
- Notifications: Nodemailer for email alerts

---

### Sprint 6: Dashboard & Polish

**Duration:** 2 weeks (Jan 11-24, 2025)
**Status:** Planned
**Priority:** MEDIUM

**Features:**

1. **Professional Dashboard**

 - Total incidents (count + trend)
 - Incidents by status (pie chart)
 - Incidents by priority (bar chart)
 - SLA compliance % (gauge chart)
 - Top 10 breach risk incidents (table)
 - My open incidents (agent view)
 - Date range filters (last 7/30/90 days)
 - Auto-refresh every 5 minutes

2. **Email Notifications**

 - Email on incident assigned
 - Email on new comment
 - Email on SLA warning (80%)
 - Email on SLA breach
 - Professional HTML email template
 - Unsubscribe link
 - No customization (post-MVP)
 - No digest mode (post-MVP)

3. **Final Polish + Testing**
 - UI consistency check
 - Responsive design (mobile-friendly)
 - Loading states
 - Error handling
 - Form validation messages
 - Full accessibility (WCAG 2.1 AA)
 - Performance optimization
 - Security audit
 - Bug fixes
 - **1 week buffer** (Jan 25-31) for final adjustments

**Tech Stack:**

- Backend: Complex aggregation queries, Nodemailer, caching
- Frontend: Recharts (interactive charts), responsive CSS
- Testing: Jest unit tests + Playwright E2E tests

---

## Timeline & Milestones

```
 Sprint 0: Infrastructure (Nov 1-15, 2024) COMPLETE
 Sprint 1: Auth & Users (Nov 16-22, 2024) 85% DONE
 Sprint 2: Incident + Rich Text (Nov 23-Dec 6) NEXT
 Sprint 3: Comments & Files (Dec 7-17)
 Sprint 4: Knowledge + Search (Dec 18-31)
 Sprint 5: Advanced SLA (Jan 1-10, 2025)
 Sprint 6: Dashboard & Polish (Jan 11-31, 2025)

 MVP LAUNCH: JANUARY 31, 2025
```

**Total:** 11 weeks (77 days)

**Key Milestones:**

- Nov 15: Infrastructure complete
- Nov 22: Auth system live
- Dec 6: Incident management + Rich Text operational
- Dec 17: Comments & attachments working
- Dec 31: Knowledge base + Meilisearch ready
- Jan 10: Advanced SLA complete
- Jan 24: Dashboard + polish complete
- Jan 31: **MVP LAUNCH** 

---

## Post-MVP Roadmap (Priority Order)

> **Nota:** Rich Text, Meilisearch e Advanced SLA já incluídos no MVP (11 semanas). Features abaixo são para v1.2+.

---

### PRIORITY 1: Teams & Smart Assignment (v1.2 - 1 semana extra)

**Sprint Extra 3: Team Collaboration**
**Impact:** MEDIUM-HIGH - Essencial para equipas >10 pessoas
**Effort:** 1 semana
**Business Value:** Expande target market para 50-100 employees

**Features:**

1. **Team Management**

 - Create/manage teams (Assignment Groups)
 - Team members + roles (manager, member)
 - Team specialization (map to categories)
 - Team capacity settings

2. **Auto-Assignment Engine**

 - Category → Team mapping
 - Priority escalation rules
 - Agent workload balancing (least busy first)
 - Round-robin within team
 - Manual override always available

3. **Workload Dashboard**
 - Active incidents per agent
 - Agent capacity visualization
 - Team heatmap (busy/available)
 - Manager view

**Why First:** Torna o produto **escalável** para equipas maiores. Sem isto, limitado a <15 agents.

---

### PRIORITY 2: REST API & Integrations (v1.5 - 1 semana extra)

**Sprint Extra 4: Developer Platform**
**Impact:** MEDIUM - Abre integrações
**Effort:** 1 semana
**Business Value:** Permite integrações com Slack, Teams, Jira, etc.

**Features:**

1. **REST API (completa)**

 - Swagger documentation (auto-generated)
 - API keys management (CRUD)
 - Rate limiting (1000 req/hour)
 - Webhook support (incident.created, incident.updated)
 - Postman collection export

2. **Integration Ready**
 - Slack notifications (webhook)
 - Email ticket creation (IMAP)
 - CSV export/import (bulk operations)
 - Zapier/Make.com ready

**Why Second:** API permite **network effects** - quanto mais integrações, mais valioso o produto. Mas não é essencial para MVP validation.

---

### PRIORITY 3: CMDB / Asset Management (v1.5 - 2 semanas extra)

**Sprint Extra 5-6: Asset Tracking**
**Impact:** MEDIUM - Feature diferenciadora
**Effort:** 2 semanas
**Business Value:** Posiciona como "Full ITSM" vs "Helpdesk"

**Features:**

1. **Asset CRUD**

 - Asset types: Laptop, Desktop, Server, License
 - Fields: serial, model, cost, warranty, location
 - Status: In Use, Available, Retired
 - Assign to users

2. **Asset → Incident Linking**

 - Select affected asset on incident
 - View incident history per asset
 - Impact analysis (what breaks if asset fails)

3. **CSV Import/Export**

 - Bulk import assets
 - Template download
 - Validation: unique serial numbers

4. **Basic Reports**
 - Assets by status/type
 - Warranty expiration alerts (30 days)
 - Cost summary by department

**Why Third:** CMDB é **nice-to-have** mas não crítico para validação. Maioria dos clientes SME não usa CMDB seriamente nos primeiros meses.

---

### PRIORITY 4: Advanced Analytics (v2.0 - 2 semanas extra)

**Sprint Extra 7-8: Business Intelligence**
**Impact:** LOW-MEDIUM - Feature enterprise
**Effort:** 2 semanas
**Business Value:** Permite upsell para planos enterprise

**Features:**

1. **Custom Report Builder**

 - Drag-and-drop UI
 - Data sources: Incidents, Assets, Users
 - Filters: any field
 - Visualizations: bar, line, pie, table
 - Export: Excel, PDF

2. **Scheduled Reports**

 - Email delivery (daily, weekly, monthly)
 - Report templates library
 - Share reports (public link)

3. **Agent Performance**
 - Average resolution time per agent
 - CSAT score per agent
 - Incidents resolved vs assigned
 - Leaderboard

**Why Fourth:** Analytics avançado é **overkill para MVP**. Clientes precisam de 3-6 meses de dados antes de analytics fazer sentido.

---

### PRIORITY 5: SSO & Enterprise Auth (v2.0 - 2 semanas extra)

**Sprint Extra 9-10: Enterprise Security**
**Impact:** LOW - Apenas para enterprise (>100 users)
**Effort:** 2 semanas
**Business Value:** Requisito para Fortune 500, mas não para SME

**Features:**

1. **SAML 2.0**

 - Azure AD integration
 - Okta integration
 - OneLogin integration
 - Auto-provisioning (JIT)

2. **OAuth 2.0**

 - Google Workspace
 - Microsoft 365
 - GitHub

3. **2FA/MFA**

 - TOTP (Google Authenticator)
 - SMS (Twilio integration)
 - Backup codes

4. **LDAP/AD**
 - Active Directory sync
 - Group mapping to roles

**Why Last:** SSO é **apenas para enterprise** (>200 employees). JWT + Password é suficiente para 99% do target market inicial (10-50 employees).

---

## Summary: Development Time if Available

| Priority | Feature | Weeks | Cumulative | Target Users |
| -------- | ----------------------- | ----- | ---------- | -------------- |
| P1 | Rich Text + Search | 1 | +1 week | All users |
| P2 | Advanced SLA | 1 | +2 weeks | >10 agents |
| P3 | Teams & Auto-Assignment | 1 | +3 weeks | >20 agents |
| P4 | REST API | 1 | +4 weeks | Integrations |
| P5 | CMDB | 2 | +6 weeks | ITSM purists |
| P6 | Advanced Analytics | 2 | +8 weeks | >50 agents |
| P7 | SSO/SAML | 2 | +10 weeks | >200 employees |

**Recomendação:** Se houver tempo extra antes de Jan 10, desenvolver **P1 (Rich Text)** primeiro - tem o melhor ROI (1 semana, impacto imenso na UX).

**Estratégia de lançamento:**

- **v1.0 (Jan 10):** MVP básico - validar product-market fit
- **v1.1 (Jan 17):** +P1 se houver 1 semana extra → UX melhorado
- **v1.2 (Jan 31):** +P2+P3 se houver 3 semanas extra → Enterprise-ready
- **v1.5 (Mar):** +P4+P5 → Full ITSM platform
- **v2.0 (Abr):** +P6+P7 → Enterprise features

---

## Features Post-MVP (Antigas - Referência)

### Phase 1: Enhanced Core (v1.1 - Feb 2025)

**Sprint 6: Teams & Auto-Assignment**

- Team management
- Auto-assignment rules engine
- Workload balancing
- Escalation management

**Sprint 7: Advanced SLA**

- Configurable SLA policies
- Business hours calendar
- SLA pause/resume
- Auto-escalation
- Breach notifications

**Sprint 8: Rich Content & Search**

- Tiptap rich text editor
- Meilisearch integration
- Advanced filtering
- Saved filters

**Duration:** 3 weeks

---

### Phase 2: Enterprise Features (v1.5 - Mar 2025)

**CMDB / Asset Management**

- Asset CRUD (CI types)
- Asset relationships
- CSV import/export
- Asset lifecycle
- Incident Asset linking

**Advanced Analytics**

- Custom report builder
- Scheduled reports
- Agent performance metrics
- Trend analysis
- Export to Excel/PDF

**Duration:** 4 weeks

---

### Phase 3: Integration & Automation (v2.0 - Apr 2025)

**REST API & Webhooks**

- Full REST API
- API documentation (Swagger)
- Webhook support
- API keys management
- Rate limiting

**Workflow Automation**

- Workflow designer (code-based)
- Approval workflows
- Auto-assignments
- Email automation
- Custom scripts

**SSO & Advanced Auth**

- SAML 2.0
- OAuth 2.0
- LDAP integration
- 2FA/MFA

**Duration:** 4 weeks

---

2. **Agent Dashboard (ServiceNow My Work)**

 - Personal metrics:
 - My open incidents
 - My incidents due today
 - My SLA at risk incidents
 - My recent activity
 - Workload gauge (current capacity %)
 - Personal performance:
 - Average resolution time
 - SLA compliance rate
 - Incidents resolved this week
 - Customer feedback score
 - Quick actions: Create Incident, View My Queue

3. **Manager Dashboard**

 - Team performance comparison
 - Agent workload heatmap
 - Top performers (most resolved, best CSAT)
 - Problem areas (most breaches, slowest resolution)
 - Resource planning insights

4. **Custom Report Builder (ServiceNow-style)**

 - Drag-and-drop report builder
 - Data sources: Incidents, Assets, Users, SLAs
 - Filters: any field, any condition
 - Grouping: by category, priority, agent, team, date
 - Visualizations: table, bar, line, pie, gauge
 - Export: Excel, PDF, CSV
 - Schedule reports (daily, weekly, monthly email)
 - Share reports (public link, embed)
 - Saved report templates

5. **Analytics Features**
 - Trend analysis (compare periods)
 - Peak hours/days identification
 - Category distribution
 - Mean Time to Resolve (MTTR)
 - Mean Time to Acknowledge (MTTA)
 - First Contact Resolution Rate
 - Repeat incident tracking
 - Knowledge base effectiveness

**Tech Stack:**

- Backend: Complex aggregation queries, report generation, caching
- Frontend: Chart.js/Recharts, data tables, dashboard builder
- Export: ExcelJS for XLSX, PDFKit for PDF
- Caching: Redis for dashboard metrics (1-hour TTL)
- Scheduler: Node-cron for scheduled reports

**ServiceNow Parity:** 70% (missing: advanced analytics, predictive insights - post-MVP)

---

### Sprint 9: Notifications & Final Polish

**Duration:** 1 week (Jan 25-31, 2025)
**Status:** Planned
**Priority:** MEDIUM
**ServiceNow Module:** Notification Engine + UI Polish

**Features:**

1. **Email Notifications (ServiceNow-equivalent)**

 - Trigger events:
 - Incident assigned to me
 - Incident updated (watched incidents)
 - New comment @mention
 - SLA breach warning (80%, 100%)
 - Approval request pending
 - Asset warranty expiring
 - Scheduled report delivery
 - Email templates (customizable):
 - Professional HTML design
 - Logo + branding
 - Actionable buttons (View Incident, Reply, Approve)
 - Plain text fallback
 - Email preferences per user:
 - Enable/disable notifications
 - Notification frequency (real-time, digest)
 - Quiet hours
 - Nodemailer integration (SMTP/SendGrid)

2. **In-App Notifications (ServiceNow-style)**

 - Notification center (bell icon)
 - Real-time notifications (polling 30s)
 - Notification types:
 - Info (FYI)
 - Warning (action suggested)
 - Critical (action required)
 - Mark as read/unread
 - Mark all as read
 - Notification history (last 30 days)
 - Deep links (click → go to incident)
 - Desktop notifications (browser API)

3. **Final Polish & Testing**
 - UI/UX refinements:
 - Consistent spacing, colors, typography
 - Loading states, empty states, error states
 - Responsive mobile design (iPhone, Android)
 - Dark mode support
 - Accessibility (WCAG 2.1 AA compliance)
 - Keyboard shortcuts
 - Performance optimization:
 - Code splitting (reduce bundle size)
 - Image optimization (WebP, lazy loading)
 - API response caching
 - Database query optimization
 - CDN for static assets
 - Load testing (Artillery/K6):
 - 100 concurrent users
 - 1000 incidents
 - <200ms API response (p95)
 - Security audit:
 - OWASP Top 10 check
 - SQL injection testing
 - XSS testing
 - CSRF protection
 - Rate limiting verification
 - Bug fixes from testing
 - Documentation updates
 - Lighthouse score >90

**Tech Stack:**

- Backend: Nodemailer, notification queue (Bull/BullMQ)
- Frontend: Notification center UI, toast notifications
- Testing: Jest, Supertest, React Testing Library, Artillery
- Monitoring: Sentry for error tracking

**ServiceNow Parity:** 80% (missing: SMS notifications, custom notification rules - post-MVP)

---

## Timeline & Milestones

```
 Sprint 0: Infrastructure (Nov 1-15, 2024) COMPLETE
 Sprint 1: Auth & Users (Nov 16-22, 2024) 85% DONE
 Sprint 2: Incident Mgmt (Nov 23-Dec 6) NEXT
 Sprint 3: Comments & Files (Dec 7-13)
 Sprint 4: Teams & Assignment (Dec 14-20)
 Sprint 5: Knowledge Base (Dec 21-Jan 3)
 Sprint 6: SLA Management (Jan 4-17, 2025)
 Sprint 7: CMDB/Assets (Jan 18-24, 2025)
 Sprint 8: Dashboards (Jan 25-31, 2025)
 Sprint 9: Notifications (Jan 25-31, 2025)

 MVP LAUNCH: JANUARY 31, 2025
```

**Total:** 11 weeks (77 days)

**Key Milestones:**

- Nov 15: Infrastructure complete
- Nov 22: Auth system live + RBAC
- Dec 6: Incident management operational (Core ITSM)
- Dec 20: Team collaboration ready
- Jan 3: Knowledge management complete
- Jan 17: SLA tracking active (ServiceNow-grade)
- Jan 24: CMDB complete (Full ITSM)
- Jan 31: **MVP LAUNCH** (ServiceNow alternative ready)

---

## Features Post-MVP (Not for Initial Launch)

## MVP Exclusions (Post-MVP Features)

### Live Chat Support

**Decision:** NOT in MVP
**Reason:** High complexity, low ROI
**Post-MVP:** v2.0 (Q2 2026)

### Visual Workflow Designer

**Decision:** NOT in MVP
**Reason:** Code-based rules sufficient
**Post-MVP:** v2.0 (Q2 2026)

### Mobile Native Apps

**Decision:** NOT in MVP
**Reason:** PWA sufficient (responsive design)
**Post-MVP:** v2.0 (Q3 2026)

### SSO & Advanced Auth (SAML/OAuth)

**Decision:** NOT in MVP
**Reason:** JWT + RBAC sufficient
**Post-MVP:** v2.0 (Q2 2026)

### Advanced SLA (business hours, auto-escalation)

**Decision:** Simplified in MVP
**Reason:** Basic timers sufficient for v1
**Post-MVP:** v1.1 (Feb 2025)

### CMDB / Asset Management

**Decision:** NOT in MVP
**Reason:** Complex feature, low priority
**Post-MVP:** v1.5 (Mar 2025)

### Teams & Auto-Assignment

**Decision:** NOT in MVP
**Reason:** Manual assignment sufficient
**Post-MVP:** v1.1 (Feb 2025)

### Rich Text Editor (Tiptap)

**Decision:** NOT in MVP
**Reason:** Plain text sufficient
**Post-MVP:** v1.1 (Feb 2025)

### Meilisearch Integration

**Decision:** NOT in MVP
**Reason:** PostgreSQL LIKE sufficient
**Post-MVP:** v1.1 (Feb 2025)

---

## Tech Stack Adjustments for MVP

| Component | MVP Version | Post-MVP Upgrade |
| ----------------- | ----------- | --------------------- |
| **Text Editor** | Textarea | Tiptap WYSIWYG |
| **Search** | SQL LIKE | Meilisearch 1.25 |
| **File Storage** | Local disk | AWS S3 + CDN |
| **Charts** | Chart.js | Chart.js + Recharts |
| **Real-time** | Polling | WebSocket (Socket.io) |
| **Notifications** | Email only | Email + In-app + SMS |

---

## Summary: MVP vs ServiceNow

**OrionOne MVP (v1.0 - Jan 2025):**

- Incident Management (CRUD + basic workflow)
- Comments & Attachments (plain text + local files)
- Knowledge Base (articles + simple search)
- Basic SLA (timers + color indicators)
- Simple Dashboard (charts + email notifications)
- JWT Authentication + RBAC
- Responsive UI (shadcn/ui + Tailwind)

**ServiceNow Parity:** 50% (Functional MVP - enough to validate product-market fit)

**Competitive Position:** "Affordable ServiceNow Alternative for Small Teams"

**Target:** 10-50 employees, $15/agent/month (vs ServiceNow $150+)

**Next:** v1.1 (Feb 2025) adds Teams, Auto-Assignment, Rich Text, Advanced SLA

---

- Nov 15: Infrastructure complete
- Nov 22: Auth system live
- Dec 6: Core ticketing functional
- Dec 20: Team collaboration ready
- Jan 3: Knowledge base operational
- Jan 17: SLA tracking active
- Jan 24: Asset management complete
- Jan 31: **MVP LAUNCH**

---

## Success Metrics

### Technical Metrics

| Metric | Target | Current | Status |
| ----------------------- | ------ | ------- | ------ |
| **Test Coverage** | >80% | TBD | |
| **API Response (p95)** | <200ms | TBD | |
| **Frontend FCP** | <1.5s | TBD | |
| **Frontend LCP** | <2.5s | TBD | |
| **Lighthouse Score** | >90 | TBD | |
| **TypeScript Coverage** | 100% | 100% | |
| **Bundle Size** | <500KB | TBD | |

### Feature Completion

| Feature | Target MVP | Current Status |
| -------------------- | ---------- | -------------- |
| **Auth & RBAC** | 100% | 85% |
| **Tickets CRUD** | 100% | 0% |
| **Comments & Files** | 100% | 0% |
| **Teams** | 100% | 0% |
| **Knowledge Base** | 100% | 0% |
| **Search (AI)** | 100% | Config |
| **SLA Management** | 80% | 0% |
| **Asset Management** | 100% | 0% |
| **Dashboard** | 80% | 0% |
| **Notifications** | 100% | 0% |

### Business Goals

| Goal | Target | Status |
| ----------------------- | ------------ | ------ |
| **MVP Launch** | Jan 31, 2026 | |
| **First 10 Customers** | Feb 2026 | |
| **Product Hunt Launch** | Feb 2026 | |
| **1000 GitHub Stars** | Q2 2026 | |
| **Break-even** | Q3 2026 | |
| **Pricing** | $15/agent/mo | |

---

**Last Updated:** 13 November 2024
**MVP Launch:** 10 January 2025 (8 weeks)
**Version:** 1.0 (Minimal Viable Product)
