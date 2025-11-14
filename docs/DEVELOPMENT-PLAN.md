# Development Plan - OrionOne ITSM

**Project:** OrionOne ITSM Platform
**Stack:** Next.js 15.5.6 + Nest.js 11.1.8 + Prisma 6.4.0 + PostgreSQL 18.0
**Methodology:** Agile Scrum with mixed sprint durations
**Target:** Professional ITSM platform with Rich UX
**Timeline:** 11 weeks (6 sprints)
**Start Date:** November 16, 2024
**Target Launch:** January 31, 2025

---

## Project Overview

### Vision Statement

Build a modern, cloud-native ITSM platform that competes with ServiceNow and Zendesk, offering:

- **90% cost savings** compared to market leaders ($20/agent vs $200+)
- **Superior UX** with Rich Text (Tiptap) + AI Search (Meilisearch)
- **Professional features** with Advanced SLA Management
- **Modern stack** with Next.js 15 + Nest.js 11
- **Target market:** 10-200 employees

### Success Metrics

| Metric | Target | Status |
| ------------------------ | -------------- | ------ |
| **Code Coverage** | >80% | TBD |
| **API Response Time** | <200ms (p95) | TBD |
| **Frontend Performance** | Lighthouse >90 | TBD |
| **Uptime** | 99.9% | TBD |
| **User Satisfaction** | NPS >50 | TBD |

---

## Sprint Overview

| Sprint | Duration | Focus Area | Status |
| ------------ | -------------- | ----------------------------------- | -------------- |
| **Sprint 0** | Nov 1-15 | Infrastructure Setup | Complete |
| **Sprint 1** | Nov 16-22 (1w) | Authentication & User Management | In Progress |
| **Sprint 2** | Nov 23-Dec 6 | Incident + Rich Text + Meilisearch | Planned |
| **Sprint 3** | Dec 7-17 | Comments & Attachments | Planned |
| **Sprint 4** | Dec 18-31 | Knowledge Base + Meilisearch Search | Planned |
| **Sprint 5** | Jan 1-10 | Advanced SLA Management | Planned |
| **Sprint 6** | Jan 11-31 | Dashboard + Polish + Buffer | Planned |

---

## Sprint 0: Infrastructure Setup (COMPLETE)

**Status:** 100% Complete
**Duration:** 2 weeks
**Team:** DevOps + Backend Lead

### Objectives

- [x] Setup Docker development environment
- [x] Configure PostgreSQL 18.0 with extensions
- [x] Setup Redis 8.2 for caching/sessions
- [x] Configure Meilisearch 1.25 for search
- [x] Initialize Nest.js backend project
- [x] Initialize Next.js frontend project
- [x] Setup Prisma ORM with PostgreSQL
- [x] Configure environment variables
- [x] Setup Git repository and branching strategy

### Deliverables

 **Infrastructure:**

- Docker Compose with 5 services (app, postgres, redis, meilisearch, nginx)
- PostgreSQL 18.0 with pgcrypto, pg_trgm, pg_stat_statements extensions
- Redis 8.2 configured for sessions + queues
- Meilisearch 1.25 with master key

 **Backend (Nest.js):**

- Project structure with modules (auth, users, tickets, etc.)
- Prisma 6.4.0 configured with PostgreSQL
- JWT authentication setup
- Swagger API documentation
- Winston logging
- Jest testing framework

 **Frontend (Next.js):**

- Next.js 15.5.6 with App Router
- React 19.2.0
- Tailwind CSS v4
- shadcn/ui configuration
- Axios 1.13.2 for API calls
- React Hook Form + Zod validation

 **Documentation:**

- SETUP.md - Quick start guide
- COMMANDS-REFERENCE.md - All commands documented
- TECHNOLOGY-AUDIT-2025.md - Tech stack analysis
- database-schema.md - Database design
- architecture.md - System architecture

### Technical Debt

None - Infrastructure is production-ready.

---

## Sprint 1: Authentication & User Management (IN PROGRESS)

**Status:** 70% Complete
**Duration:** 2 weeks (Nov 13 - Nov 27)
**Team:** Backend (2) + Frontend (1) + QA (1)

### User Stories

#### US1.1: User Registration

**As a** new user
**I want to** register an account
**So that** I can access the ITSM platform

**Acceptance Criteria:**

- [ ] Registration form with email, password, name
- [ ] Email validation (format + unique)
- [ ] Password strength requirements (min 8 chars, uppercase, lowercase, number)
- [ ] Email verification link sent
- [ ] Account activated after email verification
- [ ] Success toast + redirect to login

**API Endpoints:**

- `POST /api/auth/register`
- `POST /api/auth/verify-email/:token`

**Tests:**

- [ ] Unit: Password hashing
- [ ] Integration: Registration flow
- [ ] E2E: Full registration + verification

---

#### US1.2: User Login

**As a** registered user
**I want to** login with email/password
**So that** I can access my account

**Acceptance Criteria:**

- [ ] Login form with email + password
- [ ] JWT token returned on success
- [ ] Token stored in httpOnly cookie
- [ ] Invalid credentials show error message
- [ ] Redirect to dashboard after login
- [ ] Remember me option (30-day token)

**API Endpoints:**

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`

**Tests:**

- [ ] Unit: JWT token generation
- [ ] Integration: Login/logout flow
- [ ] E2E: Login + access protected route

---

#### US1.3: Password Reset

**As a** user who forgot password
**I want to** reset my password via email
**So that** I can regain access to my account

**Acceptance Criteria:**

- [ ] Forgot password form with email
- [ ] Reset link sent to email (expires in 1 hour)
- [ ] Reset password form with new password
- [ ] Password updated + confirmation email
- [ ] Old tokens invalidated

**API Endpoints:**

- `POST /api/auth/forgot-password`
- `POST /api/auth/reset-password/:token`

---

#### US1.4: User Profile Management

**As a** logged-in user
**I want to** manage my profile
**So that** I can keep my information up-to-date

**Acceptance Criteria:**

- [ ] View profile page with avatar, name, email, role
- [ ] Edit profile form (name, avatar, timezone, language)
- [ ] Change password form
- [ ] Upload avatar (max 2MB, jpg/png)
- [ ] Success notification on update

**API Endpoints:**

- `GET /api/users/me`
- `PATCH /api/users/me`
- `POST /api/users/me/avatar`
- `PATCH /api/users/me/password`

---

#### US1.5: Role-Based Access Control (RBAC)

**As an** administrator
**I want to** assign roles to users
**So that** I can control access to features

**Acceptance Criteria:**

- [ ] Roles: ADMIN, AGENT, USER (defined in Prisma)
- [ ] Permissions: VIEW_TICKETS, CREATE_TICKETS, ASSIGN_TICKETS, etc.
- [ ] Guards on API routes (check roles)
- [ ] Frontend shows/hides UI based on permissions
- [ ] Unauthorized access returns 403

**API Endpoints:**

- `GET /api/roles`
- `GET /api/permissions`
- `POST /api/users/:id/roles`

---

### Technical Tasks

#### Backend (Nest.js)

- [x] Auth module with JWT strategy
- [x] Users module with CRUD operations
- [ ] Password hashing with bcrypt v6
- [ ] Email service with Nodemailer
- [ ] Guards: JwtAuthGuard, RolesGuard
- [ ] Decorators: @CurrentUser(), @Roles()
- [ ] DTOs: RegisterDto, LoginDto, UpdateProfileDto
- [ ] Unit tests for AuthService, UsersService
- [ ] E2E tests for auth endpoints

#### Frontend (Next.js)

- [ ] Auth context provider
- [ ] Login page (/login)
- [ ] Register page (/register)
- [ ] Forgot password page (/forgot-password)
- [ ] Reset password page (/reset-password/:token)
- [ ] Profile page (/profile)
- [ ] Protected route wrapper (RequireAuth)
- [ ] API client with token refresh
- [ ] Form validation with Zod
- [ ] Tests with React Testing Library

#### Database (Prisma)

- [x] User model with fields: id, email, password, name, avatar, role
- [x] Role enum: ADMIN, AGENT, USER
- [x] Sessions table for refresh tokens
- [x] Password reset tokens table
- [ ] Seed admin user + test users

---

### Sprint 1 Deliverables

**Backend:**

- JWT authentication working
- User CRUD endpoints
- Email verification
- Password reset flow
- RBAC implementation
- 80%+ test coverage

**Frontend:**

- Authentication pages (login, register, reset)
- Profile management page
- Protected routes
- Auth context + token management

**Documentation:**

- API docs updated (Swagger)
- User guide for authentication

---

## Sprint 2: Incident Management + Rich Text + Meilisearch (PLANNED)

**Status:** Planned
**Duration:** 2 weeks (Nov 23 - Dec 6, 2024)
**Team:** Backend (2) + Frontend (2) + QA (1)

### User Stories

#### US2.1: Create Incident with Rich Text

**As a** user
**I want to** create an incident with formatted description
**So that** I can clearly explain the issue

**Acceptance Criteria:**

- [ ] Create incident form with: title, description (rich text), priority, category
- [ ] **Tiptap rich text editor** with formatting (bold, italic, lists, code, links)
- [ ] Markdown shortcuts support (##, \*\*, --)
- [ ] Image paste support (auto-upload to S3)
- [ ] Auto-generate incident number (INC-YYYYMMDD-NNNN)
- [ ] Manual assignment to agent (dropdown)
- [ ] Success toast + redirect to incident detail

**API Endpoints:**

- `POST /api/incidents`
- `GET /api/categories`
- `GET /api/users?role=AGENT`

---

#### US2.2: Search Incidents with Meilisearch

**As a** user
**I want to** search incidents instantly with typo tolerance
**So that** I can quickly find relevant incidents

**Acceptance Criteria:**

- [ ] Search bar with as-you-type instant search (<50ms)
- [ ] **Typo-tolerant search** (1-2 character errors)
- [ ] Search across: title, description, incident number
- [ ] **Search highlights** in results
- [ ] Relevance ranking (title > description)
- [ ] Fallback to PostgreSQL if Meilisearch unavailable

**API Endpoints:**

- `GET /api/incidents/search?q=query`

---

#### US2.3: View Incidents List with Advanced Filters

**As a** user
**I want to** view and filter incidents
**So that** I can track their status

**Acceptance Criteria:**

- [ ] Table with columns: incident#, title, status, priority, assignee, created date
- [ ] **Filter builder UI** (multiple conditions)
- [ ] **Quick filters**: My Incidents, Unassigned, Overdue
- [ ] **Saved filters** (personal + shared)
- [ ] Filter by: status, priority, assignee, category, date range
- [ ] Sort by: created, updated, priority, SLA breach risk
- [ ] Pagination: cursor-based (50 per page)
- [ ] Click row to view details

**API Endpoints:**

- `GET /api/incidents?filters=...&sort=...&cursor=...`
- `POST /api/incidents/filters` (save filter)
- `GET /api/incidents/filters` (list saved filters)

---

#### US2.4: Update Incident

**As an** agent
**I want to** update incident details
**So that** I can manage incidents effectively

**Acceptance Criteria:**

- [ ] Edit form for title, description (rich text), status, priority, assignee
- [ ] Status workflow: New → In Progress → Resolved → Closed
- [ ] Activity log records all changes
- [ ] Email notification on status change
- [ ] Optimistic UI updates

**API Endpoints:**

- `PATCH /api/incidents/:id`

---

### Technical Tasks

#### Backend (Nest.js)

- [ ] Incidents module with full CRUD
- [ ] **Meilisearch service** (index, search, sync)
- [ ] Background job: sync incidents to Meilisearch on create/update
- [ ] DTO validation (create, update, filters)
- [ ] Auto-generate incident number function
- [ ] Advanced filtering logic (query builder)
- [ ] Saved filters CRUD
- [ ] Activity logging integration
- [ ] Email notifications service
- [ ] Unit tests (>80% coverage)
- [ ] E2E tests for all endpoints

#### Frontend (Next.js)

- [ ] Incidents list page (/incidents)
- [ ] Create incident page (/incidents/create)
- [ ] Incident detail page (/incidents/:id)
- [ ] Edit incident page (/incidents/:id/edit)
- [ ] **Tiptap rich text editor component**
- [ ] **Meilisearch instant search component**
- [ ] Filter builder UI component
- [ ] Quick filters sidebar
- [ ] Saved filters dropdown
- [ ] Components: IncidentCard, IncidentTable, IncidentForm
- [ ] Status/priority badge components
- [ ] Tests for all components

#### Database (Prisma)

- [ ] Incident model with all fields (description as JSON for Tiptap)
- [ ] SavedFilter model (user, name, filters JSON)
- [ ] Category model (Hardware, Software, Network, etc.)
- [ ] IncidentStatus enum (NEW, IN_PROGRESS, RESOLVED, CLOSED)
- [ ] IncidentPriority enum (P1, P2, P3, P4)
- [ ] Indexes on status, priority, assigneeId, createdAt
- [ ] Seed 50+ test incidents

#### Meilisearch

- [ ] Configure Meilisearch index: incidents
- [ ] Searchable attributes: [title, description, incidentNumber]
- [ ] Filterable attributes: [status, priority, categoryId, assigneeId]
- [ ] Sortable attributes: [createdAt, updatedAt, priority]
- [ ] Typo tolerance: 1-2 characters
- [ ] Ranking rules: [words, typo, proximity, attribute, sort, exactness]

---

### Sprint 2 Deliverables

- [ ] Full incident CRUD with **rich text editor**
- [ ] **Meilisearch** instant search with typo tolerance
- [ ] Advanced filters + saved filters
- [ ] Quick filters (My Incidents, Unassigned)
- [ ] Activity logging
- [ ] Email notifications
- [ ] 80%+ test coverage
- [ ] Swagger API docs updated

---

## Sprint 3: Comments & Attachments (PLANNED)

**Status:** Planned
**Duration:** 1.5 weeks (Dec 7-17, 2024)
**Team:** Backend (1) + Frontend (2) + QA (1)

### User Stories

#### US3.1: Add Comment to Ticket

**As a** user
**I want to** comment on tickets
**So that** I can provide updates or ask questions

**Acceptance Criteria:**

- [ ] Comment form on ticket detail page
- [ ] Rich text editor (Tiptap)
- [ ] @mentions with autocomplete
- [ ] Internal notes (visible to agents only)
- [ ] Email notification on new comment
- [ ] Real-time comment updates (optional)

---

#### US3.2: Upload Attachments

**As a** user
**I want to** upload files to tickets
**So that** I can provide evidence (screenshots, logs)

**Acceptance Criteria:**

- [ ] Drag & drop file upload
- [ ] Multiple files (max 5 per upload)
- [ ] File size limit (10MB per file)
- [ ] Allowed formats: jpg, png, pdf, txt, log, zip
- [ ] Preview images inline
- [ ] Download button for files
- [ ] Delete attachment (with confirmation)

---

### Technical Tasks

- [ ] Comments model (Prisma)
- [ ] Attachments model (Prisma)
- [ ] File upload service (local storage)
- [ ] Activity log for comments
- [ ] Tests for comments/attachments

---

## Sprint 4: Knowledge Base + Meilisearch (PLANNED)

**Status:** Planned
**Duration:** 2 weeks (Dec 18-31, 2024)
**Team:** Backend (2) + Frontend (2) + QA (1)

### User Stories

- Create knowledge articles with **Tiptap rich text**
- **Meilisearch** typo-tolerant search
- Link articles to incidents
- Smart article suggestions (Meilisearch similarity)
- Category organization
- Draft/Published status

### Technical Tasks

- [ ] Articles model (Prisma) with body as JSON
- [ ] **Meilisearch integration** for articles
- [ ] Background job: sync articles to Meilisearch
- [ ] Similarity search for suggestions
- [ ] Article-Incident linking (many-to-many)
- [ ] **Tiptap editor** frontend component
- [ ] Tests

---

## Sprint 5: Advanced SLA Management (PLANNED)

**Status:** Planned
**Duration:** 1.5 weeks (Jan 1-10, 2025)
**Team:** Backend (2) + Frontend (1) + QA (1)

### User Stories

- Configure SLA policies (admin UI)
- **Business hours calendar** (Mon-Fri 9-5)
- **Holiday calendar** (skip non-working days)
- **Auto-escalation** at 80% breach risk
- **Email notifications** (warning at 80%, breach alert)
- **SLA pause/resume** (e.g., "Waiting on Customer")
- Real-time countdown timer (WebSocket)
- SLA dashboard (compliance %, breach risk list)

### Technical Tasks

- [ ] SLA policies CRUD
- [ ] **Bull queue** for SLA background jobs
- [ ] Complex date calculation (business hours)
- [ ] Escalation logic service
- [ ] Email notification templates
- [ ] SLA dashboard aggregations
- [ ] Real-time countdown component
- [ ] Tests

---

## Sprint 6: Dashboard + Polish + Buffer (PLANNED)

**Status:** Planned
**Duration:** 2 weeks (Jan 11-31, 2025)
**Team:** Full Team

### Week 1: Professional Dashboard (Jan 11-17)

#### User Stories

- Dashboard with: total incidents, by status (pie), by priority (bar), SLA compliance (gauge)
- Top 10 breach risk incidents (table)
- Date range filters (last 7/30/90 days)
- Auto-refresh every 5 minutes
- Email notifications: incident assigned, new comment, SLA warning, SLA breach

#### Technical Tasks

- [ ] Dashboard aggregation queries
- [ ] **Recharts** interactive charts
- [ ] Email notification templates
- [ ] Auto-refresh logic
- [ ] Tests

---

### Week 2: Polish + Testing + Buffer (Jan 18-31)

#### Focus Areas

**Quality:**

- [ ] Increase test coverage to >90%
- [ ] **Playwright E2E tests** for critical paths
- [ ] Security audit (OWASP Top 10)
- [ ] **Accessibility (WCAG 2.1 AA)**: keyboard navigation, screen readers, color contrast
- [ ] Browser testing (Chrome, Firefox, Safari, Edge)

**UI/UX:**

- [ ] Responsive design check (mobile, tablet, desktop)
- [ ] Loading states everywhere
- [ ] Error handling improvements
- [ ] Form validation UX
- [ ] Empty states
- [ ] Toast notifications consistency

**Performance:**

- [ ] Lighthouse score >90
- [ ] Bundle size optimization
- [ ] API response time <200ms (p95)
- [ ] Database query optimization
- [ ] Meilisearch response time <50ms

**DevOps:**

- [ ] Production Docker images
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Database backups
- [ ] Monitoring (Grafana + Prometheus)
- [ ] Error tracking (Sentry)

**Documentation:**

- [ ] User manual (how to create incident, search, etc.)
- [ ] Admin guide (how to configure SLA policies)
- [ ] API documentation complete (Swagger)
- [ ] Deployment guide
- [ ] README.md updated

---

### MVP LAUNCH: JANUARY 31, 2025

**Final Buffer Week (Jan 25-31):**

- Bug fixes from testing
- Final adjustments based on feedback
- Production deployment preparation
- Team training/onboarding materials

---

## Post-MVP Roadmap (v1.2+)

Features moved to post-MVP (not included in 11-week timeline):

### Priority 1: Teams & Auto-Assignment (v1.2 - 1 week)

- Create/manage teams (Assignment Groups)
- Team specialization (category mapping)
- Auto-assignment engine (workload balancing, round-robin)
- Workload dashboard

### Priority 2: REST API & Integrations (v1.5 - 1 week)

- Full REST API with Swagger docs
- API keys management
- Rate limiting
- Webhook support
- Slack/Email integrations

### Priority 3: CMDB / Asset Management (v1.5 - 2 weeks)

- Asset CRUD (laptops, servers, licenses)
- Asset → Incident linking
- Warranty tracking
- CSV import/export

### Priority 4: Advanced Analytics (v2.0 - 2 weeks)

- Custom report builder
- Scheduled reports (email delivery)
- Agent performance metrics
- CSAT surveys

### Priority 5: SSO & Enterprise Auth (v2.0 - 2 weeks)

- SAML 2.0 (Azure AD, Okta)
- OAuth 2.0 (Google, Microsoft)
- LDAP integration

---

## Project Metrics Tracking

- Real-time notifications (WebSocket)
- Email notifications (templated)
- Push notifications (optional)
- Notification preferences
- Mark as read/unread

### Technical Tasks

- [ ] WebSocket gateway (Nest.js)
- [ ] Notifications model (Prisma)
- [ ] Email templates
- [ ] Real-time updates on frontend
- [ ] Tests for notifications

---

## Sprint 8: Polish, Testing & Deployment (PLANNED)

**Status:** Planned
**Duration:** 2 weeks (Feb 19 - Mar 5)

### Focus Areas

**Quality:**

- [ ] Increase test coverage to >90%
- [ ] Performance testing (load tests)
- [ ] Security audit
- [ ] Accessibility (WCAG 2.1 AA)
- [ ] Browser testing (Chrome, Firefox, Safari)

**UI/UX:**

- [ ] Dark mode implementation
- [ ] Mobile responsiveness
- [ ] Loading states everywhere
- [ ] Error handling improvements
- [ ] Onboarding tutorial

**DevOps:**

- [ ] Production Docker images
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Database backups
- [ ] Monitoring (Grafana + Prometheus)
- [ ] Error tracking (Sentry)

**Documentation:**

- [ ] User manual
- [ ] Admin guide
- [ ] API documentation complete
- [ ] Deployment guide
- [ ] Video tutorials

---

## Project Metrics Tracking

### Code Quality

| Metric | Target | Current | Status |
| ------------------------ | ------ | ------- | ------ |
| Backend Test Coverage | >80% | TBD | |
| Frontend Test Coverage | >70% | TBD | |
| ESLint Errors | 0 | 0 | |
| TypeScript Errors | 0 | 0 | |
| Security Vulnerabilities | 0 | 0 | |

### Performance

| Metric | Target | Current | Status |
| ----------------------- | ------ | ------- | ------ |
| API Response Time (p95) | <200ms | TBD | |
| Frontend FCP | <1.5s | TBD | |
| Frontend LCP | <2.5s | TBD | |
| Lighthouse Score | >90 | TBD | |
| Bundle Size | <500KB | TBD | |

### Business

| Metric | Target | Current | Status |
| ----------------- | ------ | ------- | ------ |
| Features Complete | 100% | 15% | |
| Bugs (Critical) | 0 | 0 | |
| Bugs (High) | <5 | TBD | |
| Documentation | 100% | 60% | |
| User Acceptance | >90% | TBD | |

---

## Definition of Done (DoD)

### For Each User Story

- [ ] Code implemented and peer-reviewed
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] E2E tests passing (critical paths)
- [ ] Code linted and formatted
- [ ] TypeScript strict mode passing
- [ ] API documented in Swagger
- [ ] Manual testing completed
- [ ] Accessibility checked
- [ ] Responsive design verified
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Deployed to staging environment
- [ ] Product owner approval

### For Each Sprint

- [ ] All user stories meet DoD
- [ ] Sprint demo completed
- [ ] Retrospective conducted
- [ ] Backlog refined for next sprint
- [ ] Bugs triaged and prioritized
- [ ] Technical debt documented

---

## Risk Management

### High Risks

| Risk | Impact | Probability | Mitigation |
| ----------------------------- | ------ | ----------- | -------------------------------------- |
| **Scope Creep** | HIGH | MEDIUM | Strict sprint planning, prioritization |
| **Tech Stack Learning Curve** | MEDIUM | LOW | Pair programming, documentation |
| **Third-party Dependencies** | MEDIUM | LOW | Vendor lock-in analysis, alternatives |
| **Performance Issues** | HIGH | MEDIUM | Early load testing, optimization |
| **Security Vulnerabilities** | HIGH | LOW | Security audits, penetration testing |

### Medium Risks

| Risk | Impact | Probability | Mitigation |
| ------------------------- | ------ | ----------- | --------------------------------- |
| **API Rate Limits** | MEDIUM | LOW | Caching, rate limiting |
| **Database Scaling** | MEDIUM | MEDIUM | Connection pooling, read replicas |
| **Browser Compatibility** | MEDIUM | LOW | Progressive enhancement |

---

## Resources & References

### Team Structure

| Role | Count | Responsibility |
| ---------------------- | ----- | ------------------------------------ |
| **Product Owner** | 1 | Requirements, priorities, acceptance |
| **Scrum Master** | 1 | Facilitate sprints, remove blockers |
| **Tech Lead** | 1 | Architecture, code review, mentoring |
| **Backend Developer** | 2 | Nest.js, Prisma, API development |
| **Frontend Developer** | 2 | Next.js, React, UI/UX |
| **QA Engineer** | 1 | Testing, quality assurance |
| **DevOps Engineer** | 1 | Infrastructure, CI/CD, monitoring |

### Communication

- **Daily Standup:** 9:00 AM (15 min)
- **Sprint Planning:** First Monday (2 hours)
- **Sprint Review:** Last Friday (1 hour)
- **Sprint Retrospective:** Last Friday (30 min)
- **Backlog Refinement:** Mid-sprint Wednesday (1 hour)

### Tools

- **Project Management:** Jira / Linear
- **Code Repository:** GitHub
- **CI/CD:** GitHub Actions
- **Communication:** Slack / Discord
- **Documentation:** Notion / Confluence
- **Design:** Figma

---

## Change Log

| Date | Sprint | Change | Reason |
| ---------- | ------ | ---------------- | ------------------- |
| 2025-11-13 | 0 | Project kickoff | Initial planning |
| 2025-11-13 | 1 | Auth in progress | Started development |

---

**Last Updated:** 13 November 2025
**Maintained by:** OrionOne Product Team
**Next Review:** End of Sprint 1 (Nov 27, 2025)
