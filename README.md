<div align="center">

**Modern IT Service Management Platform**

[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat)](https://github.com/JMSS95/OrionOne)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Nest.js](https://img.shields.io/badge/Nest.js-10-E0234E?style=flat&logo=nestjs&logoColor=white)](https://nestjs.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Prisma](https://img.shields.io/badge/Prisma-6-2D3748?style=flat&logo=prisma&logoColor=white)](https://www.prisma.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](CONTRIBUTING.md)

</div>

---

## Table of Contents

-   [About](#about)
-   [Features](#features)
-   [Tech Stack](#tech-stack)
-   [Quick Start](#quick-start)
-   [Development](#development)
-   [Documentation](#documentation)
-   [Roadmap](#roadmap)
-   [Contributing](#contributing)
-   [License](#license)

---

## About

**OrionOne** é uma **plataforma ITSM (IT Service Management) completa** desenvolvida como projeto final CET - Técnico Especialista em Tecnologias e Programação de Sistemas de Informação. Inspirado em soluções enterprise como ServiceNow e Jira Service Desk, OrionOne oferece gestão profissional de IT Service Management para empresas.

> **Stack**: Next.js 15 + Nest.js 10 + PostgreSQL 16 + TypeScript
> **Projeto Académico** • CET - Técnico Especialista em Tecnologias e Programação de Sistemas de Informação
> Centro de Formação Profissional de Évora • 2024/2026

### 🔄 Migração Laravel → Next.js/Nest.js

Este projeto foi inicialmente desenvolvido em **Laravel 12 + Vue 3** (Sprint 1 - 18% MVP completo) e está em migração para **Next.js 15 + Nest.js 10** para:

-   ✅ **TypeScript Full-Stack**: Type-safety end-to-end
-   ✅ **Modern Stack**: Next.js App Router, Nest.js modular architecture
-   ✅ **Performance**: React Server Components, API otimizada
-   ✅ **Ecosystem**: npm packages mais recentes, melhor DX

**Backup Laravel/Vue**: Git tag `v0.1.0-laravel` + `docs/archive-laravel-vue/`

---

## Features

### MVP (Week 10 - 31 Jan 2025)

#### 🔐 Authentication & Authorization

-   Multi-role authentication (Admin, Agent, User)
-   JWT token-based auth with refresh tokens
-   Password reset with email verification
-   Role-Based Access Control (RBAC) + CASL permissions

#### 🎫 Ticket Management

-   Complete CRUD (Create, Read, Update, Delete)
-   Auto-generated ticket numbers (TKT-YYYYMMDD-0001)
-   Priority levels (Low, Medium, High, Urgent)
-   Status tracking (Open, In Progress, Resolved, Closed)
-   SLA calculation and tracking
-   Rich text editor (Tiptap) for descriptions

#### 💬 Comments & Collaboration

-   Public and internal comments
-   File attachments (images, documents)
-   Real-time notifications (polling 30s)
-   Activity log tracking

#### 📚 Knowledge Base

-   Articles with categories
-   Full-text search (Meilisearch)
-   Markdown editor
-   View counter

#### 💼 Asset Management (CMDB)

-   Assets CRUD (6 types: Laptop, Desktop, Server, License, Mobile, Network)
-   Asset-Ticket linking
-   Status tracking (Available, Assigned, Maintenance, Retired)
-   Asset reports

#### 👥 User & Team Management

-   User profiles with avatars
-   Team assignment
-   Permission management (32 permissions)
-   Activity log per user

#### 📊 Dashboard & Analytics

-   Ticket metrics by status
-   Priority distribution
-   Team statistics
-   Recent activity feed

**[Complete Roadmap →](docs/MVP.md)**

---

## Tech Stack

### Backend - Nest.js 10

-   **Nest.js 10** - Progressive Node.js framework
-   **Prisma 6** - Type-safe ORM with migrations
-   **PostgreSQL 16** - Enterprise-grade database
-   **Redis 7** - Cache, sessions, and queues
-   **JWT + Passport** - Authentication strategy
-   **CASL** - Permission-based authorization
-   **Sharp** - Image processing (WebP conversion)
-   **Winston** - Structured logging
-   **Swagger** - API documentation

### Frontend - Next.js 15

-   **Next.js 15** - React framework with App Router
-   **React 19** - Latest React with Server Components
-   **TypeScript 5.3** - Type-safe JavaScript
-   **Tailwind CSS v4** - Utility-first CSS
-   **Shadcn-ui** - High-quality UI components
-   **Zustand** - Lightweight state management
-   **React Query** - Server state management
-   **React Hook Form + Zod** - Form validation
-   **Tiptap** - Rich text editor
-   **date-fns** - Date utilities for SLA

### Infrastructure

-   **Docker Compose** - 8 containers (backend, frontend, postgres, redis, meilisearch, mailpit, nginx)
-   **Nginx** - Reverse proxy (/ → frontend, /api → backend)
-   **Meilisearch 1.9** - Full-text search engine
-   **Mailpit** - Email testing (dev)
-   **GitHub Actions** - CI/CD pipeline

### Developer Experience

-   **TypeScript Strict Mode** - Maximum type safety
-   **Prisma Studio** - Database GUI
-   **Jest + Supertest** - Backend testing (Nest.js)
-   **React Testing Library** - Frontend testing (Next.js)
-   **ESLint + Prettier** - Code formatting
-   **Swagger UI** - Interactive API docs

**[Complete Architecture →](docs/architecture.md)**

---

## Quick Start

### Prerequisites

**Required:**

-   [Git](https://git-scm.com/) (2.40+)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (4.25+)
-   [Node.js](https://nodejs.org/) (20.x LTS)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# 2. Start Docker containers (8 services)
docker-compose up -d

# 3. Install backend dependencies
cd nest-backend
npm install

# 4. Run database migrations
npx prisma migrate dev

# 5. Seed database
npx prisma db seed

# 6. Install frontend dependencies
cd ../next-frontend
npm install

# 7. Access application
# Frontend: http://localhost
# Backend API: http://localhost/api
# Swagger Docs: http://localhost/api/docs
# Mailpit: http://localhost:8025
```

### Default Credentials

```
Admin:
Email: admin@orionone.com
Password: admin123

Agent:
Email: agent@orionone.com
Password: agent123

User:
Email: user@orionone.com
Password: user123
```

---

## Development

### Development Workflow

OrionOne follows **Feature-Driven Development**:

**Workflow per Feature:**

1. **Planning** (30min) - User stories and acceptance criteria
2. **Database** (1h) - Prisma schema, migrations
3. **Backend** (3-4h) - Nest.js modules, services, controllers
4. **Frontend** (2-3h) - Next.js pages, React components
5. **Testing** (1-2h) - Unit + E2E tests
6. **Commit** (15min) - Conventional commits

**Code Quality:**

-   TypeScript Strict Mode
-   ESLint + Prettier
-   Jest + Supertest (backend)
-   React Testing Library (frontend)
-   > 80% test coverage

### Architecture

```
Next.js Frontend (React Server Components)
    ↓ HTTP/REST (Axios)
Nest.js Backend (Controllers)
    ↓
Services (Business Logic)
    ↓
Prisma (ORM)
    ↓
PostgreSQL Database
```

**Layers:**

-   **Presentation:** Next.js pages, React components, Shadcn-ui
-   **API:** Nest.js controllers, DTOs, Swagger docs
-   **Business Logic:** Services, Guards, Interceptors
-   **Data:** Prisma models, migrations, seeders
-   **Infrastructure:** Docker, Nginx, Redis, PostgreSQL

**[Complete Architecture →](docs/architecture.md)**

### Project Structure

```
OrionOne/
├─ nest-backend/         # Backend Nest.js
│  ├─ src/
│  │  ├─ auth/           # Authentication module
│  │  ├─ users/          # User management
│  │  ├─ tickets/        # Tickets CRUD
│  │  ├─ upload/         # File uploads
│  │  ├─ casl/           # Authorization
│  │  ├─ prisma/         # Database
│  │  └─ common/         # Shared code
│  ├─ prisma/
│  │  ├─ schema.prisma   # 15 models, 6 enums
│  │  ├─ migrations/     # Database migrations
│  │  └─ seed.ts         # Seed data
│  └─ test/              # E2E tests
├─ next-frontend/        # Frontend Next.js
│  ├─ app/
│  │  ├─ (auth)/         # Auth pages
│  │  ├─ (dashboard)/    # Protected pages
│  │  └─ api/            # Edge API routes
│  ├─ components/
│  │  ├─ ui/             # Shadcn-ui components
│  │  ├─ layout/         # Layout components
│  │  └─ tickets/        # Feature components
│  ├─ lib/
│  │  ├─ hooks/          # React Query hooks
│  │  └─ stores/         # Zustand stores
│  └─ types/             # TypeScript types
└─ docs/                 # Technical documentation
   ├─ architecture.md    # Architecture guide
   ├─ MIGRATION-*.md     # Migration docs
   └─ archive-laravel-vue/ # Laravel/Vue backup
```

### Testing

**Test Strategy:**

```bash
# Backend (Nest.js)
cd nest-backend
npm run test        # Unit tests
npm run test:e2e    # E2E tests
npm run test:cov    # Coverage report

# Frontend (Next.js)
cd next-frontend
npm run test        # Component tests
npm run test:watch  # Watch mode
```

---

## Documentation

### Essential

-   **[Quick Start](SETUP.md)** - Complete setup guide
-   **[Architecture](docs/architecture.md)** - Next.js + Nest.js architecture
-   **[Database Schema](docs/database-schema.md)** - Prisma schema with 15 models
-   **[MVP Roadmap](docs/MVP.md)** - Complete roadmap and timeline

### Migration

-   **[Migration Part 1: Setup](docs/MIGRATION-PART-1-SETUP.md)** - Infrastructure & packages (1042 lines)
-   **[Migration Part 2: Backend](docs/MIGRATION-PART-2-BACKEND.md)** - Nest.js + Prisma (1108 lines)
-   **[Migration Part 3: Frontend](docs/MIGRATION-PART-3-FRONTEND.md)** - Next.js + React (840 lines)
-   **[Migration Part 4: Timeline](docs/MIGRATION-PART-4-TIMELINE.md)** - 10-week plan (1005 lines)
-   **[Migration Part 5: Cleanup](docs/MIGRATION-PART-5-CLEANUP.md)** - Archive Laravel/Vue (1870 lines)
-   **[Migration Gaps Review](docs/MIGRATION-REVIEW-GAPS.md)** - 17 gaps analysis (1797 lines)
-   **[Migration Ready](docs/MIGRATION-READY.md)** - Executive summary (259 lines)

### Laravel/Vue Archive

-   **[Archive README](docs/archive-laravel-vue/README.md)** - Laravel 12 + Vue 3 documentation
-   **Backup Git Tag:** `v0.1.0-laravel` - Original Sprint 1 code

### Business

-   **[Requirements](docs/requirements.md)** - Functional and non-functional requirements
-   **[Business Model](docs/business-model.md)** - Business model and SWOT analysis
-   **[ITSM Stack Analysis](docs/ITSM-STACK-ANALYSIS.md)** - Comparison with ServiceNow

---

## Roadmap

### Week 0 (13-17 Nov) - Foundation

**Completed:**

-   [x] Migration decision (Laravel → Next.js/Nest.js)
-   [x] Migration documentation (5992 lines)
-   [x] Git backup (tag v0.1.0-laravel)
-   [x] Projects created (nest-backend + next-frontend)
-   [x] Environment configured (.env files, JWT_SECRET)

**In Progress:**

-   [ ] Docker + Nginx (8 containers)
-   [ ] Prisma schema + migrations (15 models)
-   [ ] Health check + CORS

### Week 1 (18-22 Nov) - Authentication

-   [ ] Seed data (32 permissions)
-   [ ] AuthModule (JWT + Passport)
-   [ ] CASL AbilityFactory
-   [ ] UsersModule CRUD
-   [ ] UploadModule (Sharp, WebP)

### Week 2-3 (25 Nov - 6 Dec) - Tickets

-   [ ] TicketsModule backend
-   [ ] Tailwind CSS migration (30+ variables)
-   [ ] Tickets frontend (list, create, detail, edit)
-   [ ] Tiptap rich text editor

### Week 4-10 (9 Dec - 31 Jan) - MVP Complete

-   [ ] Comments + Notifications
-   [ ] Knowledge Base + Meilisearch
-   [ ] Assets Management (CMDB)
-   [ ] Dashboard + Analytics
-   [ ] Teams + Announcements
-   [ ] Email (Mailpit → SMTP)
-   [ ] Logging (Winston)
-   [ ] Production deploy

**Target:** 31 Jan 2025 (39 features, 100% MVP)

**[Complete Timeline →](docs/MIGRATION-PART-4-TIMELINE.md)**

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Commit Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: new feature
fix: bug fix
docs: documentation
refactor: code refactoring
test: adding tests
chore: maintenance
```

## Security

OrionOne implements enterprise-grade security:

-   Authentication via Laravel Sanctum
-   CSRF protection on all forms
-   Password hashing with Bcrypt (cost 12)
-   SQL injection protection via Eloquent
-   XSS protection (automatic escaping)
-   Rate limiting per IP
-   Granular authorization via Policies
-   Activity logging (audit trail)
-   Soft deletes for data recovery

---

## License

This is an academic project developed for CET - Técnico Especialista em Tecnologias e Programação de Sistemas de Informação.

**Institution:** Centro de Formação Profissional de Évora
**Academic Year:** 2024/2026
**License:** MIT

See [LICENSE](LICENSE) for more information.

---

## Author

**João Santos**
[GitHub](https://github.com/JMSS95) • [Email](mailto:JMSS1995@hotmail.com)

---

## Acknowledgments

Built with amazing open-source technologies:

-   [Laravel](https://laravel.com) - PHP Framework
-   [Vue.js](https://vuejs.org) - Progressive JavaScript Framework
-   [Inertia.js](https://inertiajs.com) - Modern Monolith Approach
-   [Spatie](https://spatie.be/open-source) - Laravel Packages
-   [Tailwind CSS](https://tailwindcss.com) - Utility-First CSS
-   [Shadcn](https://ui.shadcn.com) - UI Components
-   [PostgreSQL](https://www.postgresql.org) - Advanced Database
-   Open Source Community

---

<div align="center">

**OrionOne** • Modern ITSM Platform • 2025

[Documentation](docs/README.md) • [Report Bug](https://github.com/JMSS95/OrionOne/issues) • [Request Feature](https://github.com/JMSS95/OrionOne/issues)

</div>
