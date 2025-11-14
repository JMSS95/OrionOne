# MVP - Roadmap & Status - OrionOne ITSM

**Date:** 14 November 2025
**Status:** Infrastructure Complete - Ready for Development
**Target Market:** SMEs (10-200 employees) - Professional ITSM
**Target Launch:** 31 January 2026 (13 weeks)
**Positioning:** Affordable ITSM Platform - Modern Stack, Open Source

---

## Executive Summary

**OrionOne MVP (Realistic Scope):**

-   ✅ **Core ITSM**: Incident Management (CRUD + Assignment)
-   ✅ **Rich UX**: Tiptap Rich Text Editor (essential formatting)
-   ✅ **AI Search**: Meilisearch instant search (incidents + knowledge)
-   ✅ **Collaboration**: Comments (plain text) + File Attachments (basic)
-   ✅ **Knowledge**: Knowledge Base with search
-   ✅ **SLA**: Basic SLA tracking (target times, no business hours)
-   ✅ **Dashboard**: Essential metrics + Email notifications

**Moved to Post-MVP (Priority Order):**

-   🔄 **P1**: Advanced SLA (business hours, holidays, auto-escalation) - 1 week
-   🔄 **P2**: Image paste in rich text + S3 integration - 3 days
-   🔄 **P3**: Saved filters (personal + team) - 2 days
-   🔄 **P4**: Activity timeline (full audit log) - 3 days
-   🔄 **P5**: Teams & Auto-Assignment - 1 week

**Value Proposition:** Professional ITSM for growing teams ($20/agent/month)
**Differentiators:** Rich UX, AI-powered search, Modern stack, Open source

### Tech Stack - 9.5/10 (ServiceNow-Grade)

| Component          | Version | Status     | Notes                          |
| ------------------ | ------- | ---------- | ------------------------------ |
| **Next.js**        | 15.5.6  | Production | App Router + Server Components |
| **Nest.js**        | 11.1.8  | Production | Enterprise backend framework   |
| **React**          | 19.2.0  | Production | Latest framework               |
| **Prisma**         | 6.4.0   | Production | Type-safe ORM                  |
| **PostgreSQL**     | 18.0    | Production | Advanced RDBMS + full-text     |
| **Redis**          | 8.2     | Production | Cache + sessions               |
| **Meilisearch**    | 1.25    | Production | AI-ready search engine         |
| **TypeScript**     | 5.6     | Production | Strict mode enabled            |
| **Jest**           | 29.x    | Production | Testing framework              |
| **shadcn/ui**      | Latest  | Configured | Accessible component library   |
| **Tailwind CSS**   | v4      | Production | Utility-first CSS              |
| **Zod**            | 4.x     | Production | Schema validation              |
| **TanStack Query** | 5.x     | Production | Server state management        |
| **Docker**         | Latest  | Production | Containerized development      |

**Conclusion:** Stack is PRODUCTION-READY for MVP. **ITSM Score: 9.5/10** (ServiceNow-grade platform at 10% the cost).

### MVP Feature Scope (13 weeks - Nov 1, 2025 → Jan 31, 2026)

| Feature                     | Status   | Sprint   | Priority | Effort    |
| --------------------------- | -------- | -------- | -------- | --------- |
| **Authentication & RBAC**   | MVP      | Sprint 1 | CRITICAL | 1.5 weeks |
| **Incident Management**     | MVP      | Sprint 2 | CRITICAL | 2 weeks   |
| **Tiptap Rich Text**        | MVP      | Sprint 2 | HIGH     | 2 weeks   |
| **Comments & Attachments**  | MVP      | Sprint 3 | HIGH     | 1.5 weeks |
| **Knowledge Base**          | MVP      | Sprint 4 | MEDIUM   | 2 weeks   |
| **Meilisearch Search**      | MVP      | Sprint 4 | HIGH     | 2 weeks   |
| **Basic SLA (24/7)**        | MVP      | Sprint 5 | MEDIUM   | 1.5 weeks |
| **Dashboard & Email**       | MVP      | Sprint 6 | MEDIUM   | 2 weeks   |
| **Advanced SLA**            | Post-MVP | P1       | HIGH     | 1 week    |
| **Image Paste + S3**        | Post-MVP | P2       | MEDIUM   | 3 days    |
| **Saved Filters**           | Post-MVP | P3       | MEDIUM   | 2 days    |
| **Activity Timeline**       | Post-MVP | P4       | MEDIUM   | 3 days    |
| **Teams & Auto-Assignment** | Post-MVP | P5       | HIGH     | 1 week    |
| **REST API & Webhooks**     | Post-MVP | P6       | MEDIUM   | 1 week    |
| **Advanced Analytics**      | Post-MVP | P7       | LOW      | 2 weeks   |
| **CMDB / Assets**           | Post-MVP | P8       | LOW      | 2 weeks   |
| **SSO / SAML**              | Post-MVP | P9       | VERY LOW | 2 weeks   |

### Current Status

**Sprint 0:** Infrastructure Setup (Complete)
**Sprint 1:** Authentication & User Management (In Progress - 85%)

**Next Steps:**

1. Complete Sprint 1 (Auth + RBAC)
2. Deploy staging environment
3. Begin Sprint 2 (Tickets CRUD)

---

## Sprint Roadmap (0-6) - 13 Weeks Total

**Timeline:** November 1, 2025 → January 31, 2026
**Methodology:** Agile Scrum, TDD, Feature-Driven Development
**Goal:** Launch professional ITSM platform with rich UX
**Focus:** Incident management + AI search + Basic SLA (24/7)

### Sprint 0: Infrastructure Setup (COMPLETE)

**Duration:** 2 weeks (Nov 1-15, 2025)
**Status:** 100% Complete

**Deliverables:**

-   Docker environment: PostgreSQL 18, Redis 8.2, Meilisearch 1.25
-   Nest.js 11.1.8 backend with Prisma 6.4.0 ORM
-   Next.js 15.5.6 frontend with shadcn/ui + Tailwind v4
-   JWT authentication foundation + RBAC structure
-   API documentation with Swagger (auto-generated)
-   CI/CD pipeline with GitHub Actions

**ServiceNow Equivalent:** Platform installation + basic configuration

---

### Sprint 1: Authentication & User Management (IN PROGRESS)

**Duration:** 1.5 weeks (Nov 16-27, 2025)
**Status:** 70% Complete (started Nov 16)
**Priority:** CRITICAL
**ServiceNow Module:** User Administration + Security

**Features:**

1. **Enterprise Authentication**

-   JWT access tokens (15min) + refresh tokens (7 days)
-   Multi-factor authentication ready (hooks for post-MVP)
-   Password policies (complexity, expiration, history)
-   Bcrypt v6 password hashing (12 rounds)
-   Session management with Redis
-   Account lockout after failed attempts

2. **User Management (ServiceNow-style)**

-   User CRUD with audit logging
-   Profile management + avatar upload (S3)
-   Department/location assignment
-   User preferences (timezone, language, notifications)
-   Bulk user import/export (CSV)

3. **RBAC (ServiceNow-equivalent)**

-   Roles: ADMIN, ITIL_ADMIN, AGENT, END_USER
-   Granular permissions: 32 permissions across 8 resources
-   Role inheritance support
-   Dynamic permission checking
-   Row-level security (users see only their tickets/dept)

4. **Security Features**

-   Rate limiting (100 req/min per IP)
-   CORS configuration (whitelist domains)
-   Helmet security headers (CSP, HSTS, etc.)
-   Input validation + sanitization
-   SQL injection prevention (Prisma ORM)
-   XSS protection

**Tech Stack:**

-   Backend: Nest.js Guards, Prisma middleware, JWT strategy
-   Frontend: Next.js middleware, React Context, protected routes
-   Security: @nestjs/throttler, Helmet, Zod validation

---

### Sprint 2: Incident Management + Rich Text (CRITICAL)

**Duration:** 2 weeks (Nov 28 - Dec 11, 2025)
**Status:** Planned
**Priority:** CRITICAL
**Focus:** Core ITSM functionality with essential rich text

**Features:**

1. **Incident CRUD (Core)**

-   Create, Read, Update, Delete incidents
-   Auto-generate number: INC-YYYYMMDD-NNNN
-   Fields:
    -   Title (text, required, 10-255 chars)
    -   Description (**Tiptap rich text** - essential formatting only)
    -   Status: New, In Progress, Resolved, Closed
    -   Priority: P1 (Critical), P2 (High), P3 (Medium), P4 (Low)
    -   Category (dropdown: Hardware, Software, Network, Access)
    -   Assigned To (user dropdown - agents only)
-   Validation: Zod schemas on backend + frontend
-   Auto-save drafts (localStorage)

2. **Tiptap Rich Text Editor (Essential)**

-   **INCLUDED:**
    -   Formatting: **bold**, _italic_, ~~strikethrough~~
    -   Lists: bullet lists, numbered lists
    -   Links: insert/edit hyperlinks
    -   Code blocks: inline code + code blocks
    -   Headings: H2, H3 (H1 reserved for title)
    -   Markdown shortcuts: `**`, `##`, `-`, etc.
    -   Character counter
    -   Placeholder text
    -   Mobile-responsive
-   **EXCLUDED (Post-MVP P2):**
    -   ❌ Image paste/upload (use attachments instead)
    -   ❌ Tables
    -   ❌ Embeds (YouTube, etc.)
    -   ❌ Mentions (@user)

3. **Basic Filtering & Search**

-   **Quick Filters** (sidebar buttons):
    -   All Incidents
    -   My Incidents (assigned to me)
    -   Unassigned
    -   Open (New + In Progress)
    -   Closed (Resolved + Closed)
-   **Simple Search**: Search by incident number or title (PostgreSQL ILIKE)
-   **Filter by**: Status, Priority, Assigned To (single select)
-   **Sort by**: Created (desc), Updated (desc), Priority (P1→P4)
-   **Pagination**: Offset-based, 25 per page
-   **EXCLUDED (Post-MVP P3):**
    -   ❌ Saved filters (personal + team)
    -   ❌ Advanced filter builder (multiple conditions)
    -   ❌ Full-text search with Meilisearch (Sprint 4)

4. **Assignment (Manual)**

-   Assign incident to agent (dropdown)
-   Reassign to different agent
-   Unassign incident
-   Show assignee name + avatar on incident card
-   **EXCLUDED (Post-MVP P5):**
    -   ❌ Teams/groups
    -   ❌ Auto-assignment rules
    -   ❌ Workload balancing

**Tech Stack:**

-   Backend: Prisma complex queries, DTOs with validation, Guards, Meilisearch SDK
-   Frontend: TanStack Query (caching), React Hook Form, shadcn/ui tables, **Tiptap editor**
-   Search: **Meilisearch 1.25** (primary), PostgreSQL full-text (fallback)
-   Validation: Zod schemas (backend + frontend)
-   Storage: AWS S3 for pasted images

---

### Sprint 3: Comments & Attachments

**Duration:** 1.5 weeks (Dec 12-22, 2025)
**Status:** Planned
**Priority:** HIGH
**Focus:** Essential collaboration tools

**Features:**

1. **Comments (Plain Text)**

-   Add comment to incident (textarea, 10-2000 chars)
-   List all comments (chronological, newest first)
-   Auto-linkify URLs (detect http/https)
-   Show: author name + avatar, timestamp (relative: "2 hours ago"), comment text
-   Character counter
-   No edit/delete (append-only for audit)
-   Email notification to assignee on new comment
-   **EXCLUDED:**
    -   ❌ Rich text formatting
    -   ❌ @mentions
    -   ❌ Internal vs public comments
    -   ❌ Comment reactions/likes

2. **File Attachments (Basic)**

-   Upload files: **max 2 files per comment**, **5MB each**
-   Allowed formats: jpg, jpeg, png, pdf, txt, log, zip
-   Local storage: `nest-backend/uploads/` folder
-   File validation: check MIME type + file extension
-   Display: filename, size (KB/MB), upload timestamp
-   Download: serve via `/api/attachments/:id/download`
-   Delete: only by file owner or admin
-   Simple file input (no drag & drop)
-   **EXCLUDED:**
    -   ❌ Image preview/thumbnails (just icon + filename)
    -   ❌ Drag & drop upload
    -   ❌ Multiple file selection UI
    -   ❌ S3/cloud storage (local files for MVP)
    -   ❌ Virus scanning

3. **Simple Activity Feed**

-   Show on incident detail page
-   Events tracked:
    -   Incident created
    -   Status changed (with old → new value)
    -   Priority changed
    -   Assignee changed
    -   Comment added
    -   File attached
-   Display: icon + text + timestamp + author
-   No filtering (show all)
-   **EXCLUDED (Post-MVP P4):**
    -   ❌ Full audit log with filtering
    -   ❌ Export to CSV
    -   ❌ Field-level change tracking

**Tech Stack:**

-   Backend: AWS S3 SDK, activity logging middleware, file validation
-   Frontend: File dropzone, image preview, timeline UI component
-   Storage: AWS S3 with presigned URLs (secure downloads)
-   Real-time: Polling (30s interval), WebSocket option

---

### Sprint 4: Knowledge Base + Meilisearch (CONSOLIDATED)

**Duration:** 2 weeks (Dec 23, 2025 - Jan 5, 2026)
**Status:** Planned
**Priority:** MEDIUM
**Focus:** Unified search for incidents + knowledge articles

**🔍 Meilisearch Integration (Unified Setup)**

-   Configure Meilisearch indexes:
    -   `incidents` index (title, description, incident number)
    -   `articles` index (title, body, tags)
-   Searchable attributes: title (weight: 3), description/body (weight: 1)
-   Filterable: status, priority, categoryId, authorId
-   Sortable: createdAt, updatedAt, views
-   Typo tolerance: 1-2 character errors
-   Instant search: <50ms response time
-   Search highlights in results
-   Auto-sync on create/update (Prisma middleware)
-   Global search bar (header): search both incidents + articles

**Features (Knowledge Base):**

1. **Article CRUD (Simplified)**

-   Create article: title (required, 10-200 chars), body (**Tiptap rich text**)
-   Edit article (full editor)
-   Delete article (soft delete: deleted = true)
-   Publish/Unpublish toggle (published: boolean)
-   View counter (increment on article view)
-   **EXCLUDED:**
    -   ❌ Approval workflow
    -   ❌ Version history
    -   ❌ Draft auto-save

2. **Categories (Simple)**

-   Predefined categories: Hardware, Software, Network, Access, General
-   Assign article to ONE category (required)
-   No category management UI (hardcoded for MVP)
-   **EXCLUDED:**
    -   ❌ Subcategories/nested categories
    -   ❌ Tags system
    -   ❌ Custom category creation

3. **Link to Incidents**

-   Manual link: select article from dropdown on incident page
-   Many-to-many relation (incident ↔ articles)
-   Show linked articles on incident detail
-   Basic suggestion: show top 5 articles from same category
-   **EXCLUDED:**
    -   ❌ Smart suggestions (Meilisearch similarity)
    -   ❌ AI-powered recommendations
    -   ❌ Auto-link based on keywords

**Tech Stack:**

-   Backend: Prisma CRUD, **Meilisearch SDK**, Tiptap JSON storage
-   Frontend: **Tiptap editor**, Meilisearch InstantSearch components

---

### Sprint 5: Basic SLA Tracking (SIMPLIFIED)

**Duration:** 1.5 weeks (Jan 6-15, 2026)
**Status:** Planned
**Priority:** MEDIUM
**Focus:** Essential SLA tracking without complex calculations

**Features:**

1. **Simple SLA Target Times (24/7 Clock)**

-   Fixed target times per priority (no configurable policies yet):
    -   P1 Critical: 4 hours
    -   P2 High: 8 hours
    -   P3 Medium: 24 hours
    -   P4 Low: 72 hours
-   **24/7 calculation** (no business hours/holidays)
-   Target time starts when incident created
-   Target time stops when incident closed/resolved
-   Store: `targetResolveAt` (timestamp) in incident table

2. **SLA Display (Visual Indicators)**

-   Calculate remaining time: `targetResolveAt - now`
-   Color-coded badges:
    -   🟢 Green: >50% time remaining
    -   🟡 Yellow: 25-50% time remaining
    -   🔴 Red: <25% time remaining
    -   ⚫ Breached: past target time
-   Show countdown: "2h 30m remaining" or "Breached 1h 15m ago"
-   Dashboard widget: "At Risk" incidents (red + breached)
-   No real-time updates (refresh on page load)

3. **Basic Email Notifications**

-   Email on SLA breach:
    -   To: assignee + admins
    -   Subject: "SLA Breached: INC-20251201-0042"
    -   Body: incident title, priority, target time, breach time
-   Manual email send (cron job every 15 minutes)
-   No warning emails (only breach)

**EXCLUDED (Post-MVP P1 - Advanced SLA):**

-   ❌ Business hours calendar (Mon-Fri 9-5)
-   ❌ Holiday calendar
-   ❌ Configurable SLA policies (admin UI)
-   ❌ Auto-escalation at 80%
-   ❌ SLA pause/resume
-   ❌ Warning emails at 80%
-   ❌ Real-time countdown (WebSocket)
-   ❌ SLA history/audit log

**Tech Stack:**

-   Backend: Complex date calculation, Prisma cron jobs, Bull queue for escalations
-   Frontend: Real-time countdown, color-coded badges, admin configuration UI
-   Notifications: Nodemailer for email alerts

---

### Sprint 6: Dashboard & Polish

**Duration:** 2 weeks (Jan 16-31, 2026)
**Status:** Planned
**Priority:** MEDIUM

**Features:**

1. **Professional Dashboard**

-   Total incidents (count + trend)
-   Incidents by status (pie chart)
-   Incidents by priority (bar chart)
-   SLA compliance % (gauge chart)
-   Top 10 breach risk incidents (table)
-   My open incidents (agent view)
-   Date range filters (last 7/30/90 days)
-   Auto-refresh every 5 minutes

2. **Email Notifications**

-   Email on incident assigned
-   Email on new comment
-   Email on SLA warning (80%)
-   Email on SLA breach
-   Professional HTML email template
-   Unsubscribe link
-   No customization (post-MVP)
-   No digest mode (post-MVP)

3. **Final Polish + Testing**

-   UI consistency check
-   Responsive design (mobile-friendly)
-   Loading states
-   Error handling
-   Form validation messages
-   Full accessibility (WCAG 2.1 AA)
-   Performance optimization
-   Security audit
-   Bug fixes
-   **1 week buffer** (Jan 25-31) for final adjustments

**Tech Stack:**

-   Backend: Complex aggregation queries, Nodemailer, caching
-   Frontend: Recharts (interactive charts), responsive CSS
-   Testing: Jest unit tests + Playwright E2E tests

---

## Timeline & Milestones

```
 Sprint 0: Infrastructure (Nov 1-15, 2025) ✅ COMPLETE
 Sprint 1: Auth & Users (Nov 16-27, 2025) 🔄 IN PROGRESS (70%)
 Sprint 2: Incident + Rich Text (Nov 28-Dec 11, 2025) NEXT
 Sprint 3: Comments & Files (Dec 12-22, 2025)
 Sprint 4: Knowledge + Search (Dec 23, 2025-Jan 5, 2026)
 Sprint 5: Basic SLA (24/7) (Jan 6-15, 2026)
 Sprint 6: Dashboard & Polish (Jan 16-31, 2026)

 MVP LAUNCH: JANUARY 31, 2026
```

**Total:** 13 weeks (92 days)

**Key Milestones:**

-   Nov 15, 2025: ✅ Infrastructure complete
-   Nov 27, 2025: Auth system live (Sprint 1 end)
-   Dec 11, 2025: Incident management + Rich Text operational
-   Dec 22, 2025: Comments & attachments working
-   Jan 5, 2026: Knowledge base + Meilisearch ready
-   Jan 15, 2026: Basic SLA (24/7) complete
-   Jan 31, 2026: **MVP LAUNCH** (Dashboard + polish complete)

---

## Post-MVP Roadmap (Priority Order)

> **IMPORTANT:** MVP focuses on **core ITSM functionality** that works well. Advanced features below are prioritized by **business value** and **implementation effort**. Add them incrementally after MVP launch based on user feedback.

---

## 🔥 PRIORITY 1: Advanced SLA Management (v1.1 - 1 week)

**Effort:** 5-7 days
**Business Value:** HIGH - Essential for enterprise customers (>50 agents)
**User Demand:** HIGH - Top feature request from ITSM users
**Technical Complexity:** HIGH

**Features:**

1. **Business Hours Calendar**

    - Configure work schedule: Mon-Fri 9am-5pm (configurable)
    - Timezone support (organization-level)
    - SLA calculation excludes non-working hours
    - Example: P1 4-hour SLA created Friday 4pm → due Monday 11am

2. **Holiday Calendar**

    - Admin UI to add holidays (date + name)
    - Import standard calendars (US, UK, PT, etc.)
    - SLA calculation skips holidays

3. **Auto-Escalation**

    - Warning email at 80% SLA elapsed (to agent + manager)
    - Breach notification (to agent + manager + admin)
    - Optional: reassign to senior agent on 80% warning

4. **SLA Pause/Resume**

    - Pause SLA when status = "Waiting on Customer"
    - Resume when status changes back
    - Track pause events in SLA history

5. **Real-time Countdown**
    - WebSocket updates every 60 seconds
    - Live countdown on incident detail page

**API Endpoints:**

-   `POST /api/sla-policies` (admin create policy)
-   `GET /api/sla-policies`
-   `POST /api/holidays` (admin add holiday)
-   `GET /api/holidays`

**Tech Stack:**

-   Backend: date-fns for complex date calculations, Bull queue for background jobs
-   Frontend: WebSocket connection, live countdown component

---

## 📸 PRIORITY 2: Image Paste in Rich Text (v1.1 - 3 days)

**Effort:** 2-3 days
**Business Value:** MEDIUM-HIGH - Great UX improvement
**User Demand:** MEDIUM - Nice to have, not critical
**Technical Complexity:** LOW

**Features:**

-   Paste images directly into Tiptap editor (Ctrl+V)
-   Auto-upload to S3 or local storage
-   Show upload progress bar
-   Insert image at cursor position
-   Resize image (max width: 800px)
-   Image lazy loading

**Tech Stack:**

-   Tiptap Image extension
-   Multer for file upload
-   AWS S3 SDK (or local uploads/)

---

## 💾 PRIORITY 3: Saved Filters (v1.1 - 2 days)

**Effort:** 2 days
**Business Value:** MEDIUM - Power user feature
**User Demand:** MEDIUM
**Technical Complexity:** LOW

**Features:**

-   Save current filter combination (name + filters JSON)
-   Personal filters (user-level)
-   Team filters (shared with team)
-   Filter dropdown in incidents page
-   Edit/delete saved filters

**Database:**

```prisma
model SavedFilter {
  id        String   @id @default(cuid())
  name      String
  filters   Json     // {status: ['OPEN'], priority: ['P1']}
  userId    String
  teamId    String?  // null = personal, value = team shared
}
```

---

## 📊 PRIORITY 4: Full Activity Timeline (v1.2 - 3 days)

**Effort:** 3 days
**Business Value:** MEDIUM - Audit/compliance feature
**User Demand:** LOW-MEDIUM
**Technical Complexity:** LOW

**Features:**

-   Track ALL field changes (before → after)
-   Filter activity by: type (comments, status, assignments), user, date range
-   Export activity log to CSV
-   Show IP address + user agent for compliance

**Database:**

```prisma
model ActivityLog {
  id            String   @id @default(cuid())
  incidentId    String
  userId        String
  action        String   // "STATUS_CHANGED", "ASSIGNED", "COMMENTED"
  fieldName     String?  // "status", "priority"
  oldValue      String?
  newValue      String?
  ipAddress     String?
  userAgent     String?
  createdAt     DateTime @default(now())
}
```

---

## 👥 PRIORITY 5: Teams & Auto-Assignment (v1.2 - 1 week)

**Effort:** 5-7 days
**Business Value:** MEDIUM-HIGH - Essential for teams >10 agents
**User Demand:** MEDIUM - Requested by 30% of enterprise users
**Technical Complexity:** MEDIUM

**Features:**

1. **Team Management**

    - Create/edit/delete teams (admin only)
    - Assign users to teams (one user, multiple teams)
    - Team lead designation
    - Team specialization: assign categories to team

2. **Auto-Assignment Rules**

    - Round-robin: distribute evenly across team members
    - Workload-based: assign to agent with fewest open incidents
    - Category-based: auto-assign based on incident category → team mapping
    - Priority rules: P1 incidents → senior agents

3. **Team Dashboard**
    - Team performance metrics
    - Workload distribution chart
    - Team open incidents count

**Database:**

```prisma
model Team {
  id          String   @id @default(cuid())
  name        String
  members     TeamMember[]
  categories  String[]  // ["HARDWARE", "SOFTWARE"]
}

model TeamMember {
  id       String   @id @default(cuid())
  teamId   String
  userId   String
  role     String   // "MEMBER", "LEAD"
}
```

---

## 🔌 PRIORITY 6: REST API & Webhooks (v1.3 - 1 week)

**Effort:** 5-7 days
**Business Value:** MEDIUM - Enables integrations
**User Demand:** LOW-MEDIUM - Requested by 15% of users
**Technical Complexity:** LOW

**Features:**

-   Full REST API for all CRUD operations
-   API key authentication
-   Rate limiting (100 req/min per key)
-   Swagger/OpenAPI documentation (already 90% done)
-   Webhook support for events: incident created, status changed, commented
-   Webhook retry logic (3 attempts)

---

## 📊 PRIORITY 7: Advanced Analytics (v1.4 - 2 weeks)

**Effort:** 10-12 days
**Business Value:** MEDIUM - Business intelligence
**User Demand:** LOW - Power user feature
**Technical Complexity:** HIGH

**Features:**

-   Custom report builder (drag & drop)
-   Scheduled reports (daily/weekly/monthly email)
-   Agent performance metrics (avg resolution time, SLA compliance %)
-   Trend analysis (incidents over time by category/priority)
-   Export to Excel/PDF

---

## 📦 PRIORITY 8: CMDB / Asset Management (v1.5 - 2 weeks)

**Effort:** 10-14 days
**Business Value:** LOW-MEDIUM - Full ITSM feature
**User Demand:** LOW - Requested by <10% of users
**Technical Complexity:** MEDIUM

**Features:**

-   Asset CRUD (computers, servers, licenses)
-   Asset relationships (computer → user)
-   Link asset to incident
-   Warranty tracking
-   CSV import/export

---

## 🔐 PRIORITY 9: SSO & SAML (v2.0 - 2 weeks)

**Effort:** 10-14 days
**Business Value:** LOW - Enterprise-only feature
**User Demand:** VERY LOW - Requested by <5% of users
**Technical Complexity:** HIGH

**Features:**

-   SAML 2.0 (Azure AD, Okta)
-   OAuth 2.0 (Google, Microsoft)
-   LDAP integration
-   JIT (Just-In-Time) provisioning

---

---

## 📋 MVP RISK ANALYSIS

### ✅ LOW RISK (Confidence: 90%+)

| Sprint   | Feature        | Why Low Risk                           |
| -------- | -------------- | -------------------------------------- |
| Sprint 1 | Authentication | Standard JWT + Prisma, well-documented |
| Sprint 2 | Incident CRUD  | Basic CRUD, no complex business logic  |
| Sprint 3 | Comments       | Simple append-only data, no edge cases |
| Sprint 3 | File Upload    | Standard Multer, local storage simple  |

### ⚠️ MEDIUM RISK (Confidence: 70-80%)

| Sprint   | Feature            | Risk                             | Mitigation                                 |
| -------- | ------------------ | -------------------------------- | ------------------------------------------ |
| Sprint 2 | Tiptap Integration | Learning curve, JSON storage     | Allocate 3 days for R&D, use official docs |
| Sprint 4 | Meilisearch Setup  | First-time setup, indexing logic | Start early, test with small dataset first |
| Sprint 5 | SLA Calculation    | Date math complexity             | Use date-fns library, extensive unit tests |
| Sprint 6 | Dashboard Charts   | Aggregation queries performance  | Add database indexes, use Redis caching    |

### 🔴 HIGH RISK (Confidence: 50-60%)

| Item                     | Risk                      | Impact             | Mitigation                                           |
| ------------------------ | ------------------------- | ------------------ | ---------------------------------------------------- |
| **Timeline Pressure**    | 13 weeks is tight         | Could delay launch | 2-week buffer in Sprint 6, cut P4 features if needed |
| **Scope Creep**          | Users requesting features | Distraction        | Strict "post-MVP" policy, document requests for v1.1 |
| **Testing Time**         | Need 80% coverage         | Quality issues     | Write tests during development (TDD), not after      |
| **Meilisearch Learning** | New technology            | Integration delays | Spike task in week 1 of Sprint 4 (2 days R&D)        |

### 🛡️ RISK MITIGATION STRATEGIES

1. **Weekly Sprint Reviews** (every Friday 4pm)

    - Demo completed features
    - Identify blockers early
    - Adjust next week's scope if needed

2. **Feature Freeze** (Jan 20, 2026)

    - No new features after this date
    - Focus 100% on: bug fixes, testing, polish
    - Allocate 11 days for stabilization

3. **Fallback Plan** (if behind schedule)

    - **Option A**: Cut Sprint 5 (SLA) → Post-MVP P1
    - **Option B**: Cut Sprint 4 (Knowledge Base) → Post-MVP P6
    - **Option C**: Extend launch to Feb 14 (2 extra weeks)

4. **Technical Spikes** (R&D tasks)
    - Sprint 2 Week 1: Tiptap POC (1 day)
    - Sprint 4 Week 1: Meilisearch POC (2 days)
    - Budget 10% of each sprint for unexpected complexity

---

## 📊 MVP vs Post-MVP SUMMARY

### ✅ IN MVP (13 weeks)

-   Core Incident Management (CRUD, assignment, filters)
-   Tiptap Rich Text (essential formatting)
-   Plain Text Comments + Basic File Attachments
-   Knowledge Base (articles with search)
-   Meilisearch (incidents + articles)
-   Basic SLA (24/7 tracking, breach alerts)
-   Dashboard (essential metrics)
-   Email Notifications

### 🔄 POST-MVP (Prioritized)

**Week 14-15 (v1.1):**

-   P1: Advanced SLA (business hours, holidays)
-   P2: Image paste in rich text
-   P3: Saved filters

**Week 16-17 (v1.2):**

-   P4: Full activity timeline
-   P5: Teams & auto-assignment

**Week 18+ (v1.3+):**

-   P6: REST API & Webhooks
-   P7: Advanced Analytics
-   P8: CMDB / Assets
-   P9: SSO / SAML

---

## 📊 QUICK REFERENCE TABLES

### MVP Timeline Overview

| Sprint    | Duration     | Dates              | Focus Area                   | Status  |
| --------- | ------------ | ------------------ | ---------------------------- | ------- |
| Sprint 0  | 2 weeks      | Nov 1-15, 2025     | Infrastructure               | ✅ Done |
| Sprint 1  | 1.5 weeks    | Nov 16-27, 2025    | Auth & RBAC                  | 🔄 70%  |
| Sprint 2  | 2 weeks      | Nov 28-Dec 11      | Incident + Rich Text         | ⏳ Next |
| Sprint 3  | 1.5 weeks    | Dec 12-22          | Comments & Files             | ⏳      |
| Sprint 4  | 2 weeks      | Dec 23-Jan 5, 2026 | Knowledge Base + Search      | ⏳      |
| Sprint 5  | 1.5 weeks    | Jan 6-15, 2026     | Basic SLA                    | ⏳      |
| Sprint 6  | 2 weeks      | Jan 16-31, 2026    | Dashboard & Polish           | ⏳      |
| **TOTAL** | **13 weeks** | **92 days**        | **MVP LAUNCH: Jan 31, 2026** |         |

### Post-MVP Roadmap Summary

| Version | Timeline   | Features                                   | Target Users      |
| ------- | ---------- | ------------------------------------------ | ----------------- |
| v1.1    | Week 14-15 | Advanced SLA, Image Paste, Saved Filters   | All users         |
| v1.2    | Week 16-17 | Activity Timeline, Teams & Auto-Assignment | Teams >10 agents  |
| v1.3    | Week 18-19 | REST API & Webhooks                        | Integration needs |
| v1.4    | Week 20-21 | Advanced Analytics                         | Teams >50 agents  |
| v1.5    | Week 22-23 | CMDB / Asset Management                    | ITSM purists      |
| v2.0    | Week 24-25 | SSO & SAML                                 | Enterprise >200   |

### Business Goals

| Metric                     | Target           | Status     |
| -------------------------- | ---------------- | ---------- |
| **MVP Launch**             | Jan 31, 2026     | On track   |
| **First 10 Customers**     | Feb 2026         | -          |
| **Product Hunt Launch**    | Feb 2026         | -          |
| **1000 GitHub Stars**      | Q2 2026          | -          |
| **Break-even**             | Q3 2026          | -          |
| **Pricing**                | $20/agent/mo     | Fixed      |
| **Target Market**          | 10-200 employees | Defined    |
| **ServiceNow Alternative** | 10% cost         | Positioned |

---

**Last Updated:** 14 November 2025
**Next Review:** Every Friday 4pm (Sprint Reviews)
**Documentation:** See DEVELOPMENT-PLAN.md for detailed sprint breakdowns
