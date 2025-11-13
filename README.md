<div align="center">
 <img src="public/images/logo.png" alt="OrionOne Logo" width="300">

**Modern IT Service Management Platform**

[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat)](https://github.com/JMSS95/OrionOne)
[![PHP](https://img.shields.io/badge/PHP-8.2-777BB4?style=flat&logo=php&logoColor=white)](https://www.php.net/)
[![Laravel](https://img.shields.io/badge/Laravel-12-FF2D20?style=flat&logo=laravel&logoColor=white)](https://laravel.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Inertia](https://img.shields.io/badge/Inertia.js-2.0-9553E9?style=flat&logo=inertia&logoColor=white)](https://inertiajs.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Uma plataforma ITSM completa para gestão profissional de IT Service Management, incluindo Asset Management (CMDB), Knowledge Base com AI Search, SLA Management e reporting avançado.

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

**OrionOne** é uma **plataforma ITSM (IT Service Management) completa** desenvolvida como projeto final de Engenharia de Software (TCC). Inspirado em soluções enterprise como ServiceNow e Jira Service Desk, OrionOne oferece gestão profissional de IT Service Management para empresas de 10-500 funcionários.

**Diferenciais:**

-   Arquitetura moderna (Laravel 12 + Vue 3 + PostgreSQL 16)
-   Desenvolvimento guiado por testes (TDD, >80% coverage)
-   Asset Management (CMDB) incluído no MVP
-   Documentação técnica completa
-   Stack enterprise open-source

> **Projeto Académico** • CET - Técnico Especialista em Tecnologias e Programação de Sistemas de Informação
> Centro de Formação Profissional de Évora • 2024/2026

**ITSM Score:** 8.5/10 | **Target Market:** 10-500 funcionários | **MVP Launch:** Fevereiro 2026

---

## Features

### Implemented (Sprint 1 - Complete)

#### Authentication & Authorization

-   Multi-role authentication (Admin, Agent, User) via Laravel Breeze
-   Password reset with email verification
-   CSRF protection on all forms
-   Role-Based Access Control (RBAC) via Spatie Permission

#### User Profile Management

-   Profile updates (name, email)
-   Avatar upload with validation (JPG, PNG, GIF, WEBP)
-   Auto-resize to 300x300px (Intervention Image v3)
-   Account deletion with confirmation

#### Infrastructure

-   Docker Compose with 6 containers (app, nginx, postgres, redis, queue, scheduler)
-   PostgreSQL 16 with advanced features (Views, Triggers, Stored Procedures)
-   Redis 7 for cache and queue management
-   Vue 3 + Inertia.js frontend with HMR
-   Automated testing (Feature + Unit tests)

### In Development (Sprint 2-7)

**Sprint 2: Tickets CRUD** (6 weeks)

-   Complete ticket management (Create, Read, Update, Delete)
-   Auto-generated ticket numbers (TKT-000001, TKT-000002...)
-   Priority levels (Low, Medium, High, Urgent)
-   Status tracking (Open, In Progress, Resolved, Closed)

**Sprint 3: Comments & Collaboration** (6 weeks)

-   Public and internal comments
-   User mentions (@username)
-   Real-time notifications

**Sprint 4: Knowledge Base** (6 weeks)

-   Articles with categories
-   Full-text search (PostgreSQL + Meilisearch)
-   Voting system (helpful/not helpful)

**Sprint 5: Dashboard & SLA** (6 weeks)

-   Ticket metrics by status
-   SLA tracking with breach alerts
-   Team statistics
-   Chart.js visualizations

**Sprint 6: Teams & Automation** (4 weeks)

-   Team management
-   Auto-assignment rules
-   Scheduled reports

**Sprint 7: Asset Management (CMDB)** (4 weeks) ← **NEW**

-   Assets CRUD (6 types: Laptop, Desktop, Server, License, Mobile, Network)
-   Asset-Ticket linking (affected_asset_id)
-   CSV Import/Export (bulk operations via Maatwebsite Excel)
-   Asset reports (status, warranty alerts, cost summary)

**[Complete Roadmap →](docs/MVP.md)**

---

## Tech Stack

### Backend

-   **Laravel 12** - Modern PHP framework
-   **PostgreSQL 16** - Enterprise-grade database with Views, Triggers, Stored Procedures
-   **Redis 7** - Cache and queue management
-   **Spatie Packages** - Data DTOs, Permissions, Activity Log, Query Builder, MediaLibrary
-   **Laravel Actions** - Reusable business logic (Controller/Job/Command)
-   **Maatwebsite Excel** - CSV/Excel import/export for asset management

### Frontend

-   **Vue 3** - Progressive JavaScript framework
-   **Inertia.js 2.0** - Modern monolith SPA approach
-   **Tailwind CSS** - Utility-first CSS framework
-   **Shadcn-vue** - High-quality UI components (Radix + Tailwind)
-   **Vite 6** - Next generation frontend tooling
-   **Tiptap** - Rich text editor for ticket descriptions
-   **Chart.js** - Data visualizations and analytics
-   **date-fns** - Modern date utility library for SLA tracking

### Developer Experience

-   **Docker Compose** - Consistent development environment
-   **Laravel Telescope** - Debugging and monitoring
-   **Laravel Pulse** - Real-time performance insights
-   **Pest PHP** - Modern testing framework
-   **PHPStan** - Static analysis (Level 5)
-   **Laravel Pint** - Code style formatter

**[Complete Tech Stack →](docs/tech-stack.md)**

---

## Quick Start

### Prerequisites

This project uses **Docker exclusively**. No need to install PHP, PostgreSQL or Redis locally.

**Required:**

-   [Git](https://git-scm.com/) (2.40+)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (4.25+)
-   [Node.js](https://nodejs.org/) (20.x LTS) - Optional, for local npm

### Setup (10 minutes)

```bash
# 1. Clone repository
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# 2. Configure environment
cp .env.example .env
# Defaults work without changes

# 3. Start all Docker containers
docker-compose up -d

# 4. Verify containers are running
docker-compose ps
# Should see: orionone-app, orionone-nginx, orionone-postgres, orionone-redis

# 5. Install backend dependencies
docker-compose exec orionone-app composer install

# 6. Setup Laravel
docker-compose exec orionone-app php artisan key:generate
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan db:seed

# 7. Install frontend dependencies
docker-compose exec orionone-app npm install

# 8. Build assets (or dev mode with hot reload)
docker-compose exec orionone-app npm run build
# OR for development with HMR:
docker-compose exec orionone-app npm run dev
```

### Access Application

**URLs:**

-   **Frontend:** http://localhost
-   **Laravel Telescope:** http://localhost/telescope (debugging)
-   **Laravel Pulse:** http://localhost/pulse (monitoring)
-   **API Docs:** http://localhost/docs (Scribe)

**Test Credentials:**

```
Admin: admin@orionone.test / password
Agent: agent@orionone.test / password
User: user@orionone.test / password
```

### Common Commands

```bash
# View logs
docker-compose logs -f orionone-app

# Stop containers
docker-compose down

# Rebuild after Dockerfile changes
docker-compose up -d --build

# Run tests
docker-compose exec orionone-app php artisan test

# Clear cache
docker-compose exec orionone-app php artisan config:clear
docker-compose exec orionone-app php artisan cache:clear
```

**[Complete Setup Guide →](SETUP.md)** | **[Commands Reference →](docs/COMMANDS-REFERENCE.md)**

---

## Development

### Development Workflow

OrionOne follows **Feature-Driven Development + TDD**:

**6-Phase Workflow per Feature:**

1. **Planning** (30min) - User stories and acceptance criteria
2. **Database** (45min) - Migration, Model, Factory, Seeder
3. **Backend TDD** (2-3h) - Tests first, then implementation (RED → GREEN → REFACTOR)
4. **Frontend** (1-2h) - Vue 3 components + Inertia.js pages
5. **API** (1h) - Optional REST endpoints
6. **Commit** (15min) - Conventional commits

**Code Quality:**

-   PHPStan Level 5 (static analysis)
-   Laravel Pint (PSR-12 code style)
-   > 80% test coverage
-   Pest PHP for testing

### Architecture

```
Controllers (thin) → Services (business logic) → Models (data)
 ↓
 Actions (atomic operations)
 ↓
 Events → Listeners
 ↓
 Observers (model hooks)
```

**Layers:**

-   **Presentation:** Controllers, Form Requests, Inertia Pages (Vue)
-   **Business Logic:** Services, Actions, Policies
-   **Data:** Models, Observers, Migrations
-   **Infrastructure:** PostgreSQL, Redis, Queue Jobs

**[Complete Development Guide →](docs/development-guide.md)** | **[Architecture →](docs/architecture.md)**

### Project Structure

```
OrionOne/
├─ app/
│  ├─ Http/          # Controllers, Requests, Middleware
│  ├─ Services/      # Business logic (TicketService, SLAService)
│  ├─ Actions/       # Atomic operations (CreateTicketAction)
│  ├─ Models/        # Eloquent models
│  ├─ Policies/      # Authorization
│  ├─ Observers/     # Model hooks
│  └─ Events/        # Domain events
├─ database/
│  ├─ migrations/    # Schema definitions
│  ├─ seeders/       # Test data
│  └─ factories/     # Model factories
├─ resources/
│  └─ js/
│     ├─ Pages/      # Inertia.js pages (Vue 3)
│     ├─ Components/ # Reusable Vue components
│     └─ Composables/# Vue composables
├─ tests/
│  ├─ Feature/       # HTTP integration tests
│  └─ Unit/          # Unit tests
└─ docs/             # Technical documentation
```

### Testing

```bash
# Run all tests
docker-compose exec orionone-app php artisan test

# With coverage
docker-compose exec orionone-app php artisan test --coverage

# Specific test
docker-compose exec orionone-app php artisan test --filter=UpdateProfileTest

# Continuous testing
docker-compose exec orionone-app php artisan test --watch
```

**Test Strategy:**

-   **Unit Tests:** Services, Actions (mock dependencies)
-   **Feature Tests:** Complete HTTP requests with database
-   **Browser Tests:** Dusk (optional, for critical flows)

---

## Documentation

### Essential

-   **[Quick Start](SETUP.md)** - Complete setup guide
-   **[Implementation Checklist](docs/implementation-checklist.md)** - Feature-by-feature TDD guide
-   **[Tech Stack](docs/tech-stack.md)** - All technologies used
-   **[Commands Reference](docs/COMMANDS-REFERENCE.md)** - All useful commands

### Architecture & Design

-   **[Architecture](docs/architecture.md)** - Application architecture
-   **[Database Schema](docs/database-schema.md)** - Complete schema with relationships
-   **[Requirements](docs/requirements.md)** - Functional and non-functional requirements
-   **[MVP Roadmap](docs/MVP.md)** - Complete roadmap and timeline

### Deep Dives

-   **[Backend Deep Dive](docs/TECH-DEEP-DIVE-BACKEND.md)** - Laravel, Spatie, Actions
-   **[Frontend Deep Dive](docs/TECH-DEEP-DIVE-FRONTEND.md)** - Vue 3, Inertia, Shadcn
-   **[Database Deep Dive](docs/TECH-DEEP-DIVE-DATABASE.md)** - PostgreSQL, Redis, Views, Triggers
-   **[DevOps Deep Dive](docs/TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx, Deployment

### Development

-   **[Development Guide](docs/development-guide.md)** - TDD workflow and conventions
-   **[Components Guide](docs/COMPONENTS-GUIDE.md)** - Shadcn-vue components usage
-   **[Deployment Guide](DEPLOYMENT.md)** - Production deployment

### Business

-   **[Business Model](docs/business-model.md)** - Business model and SWOT analysis
-   **[ITSM Stack Analysis](docs/ITSM-STACK-ANALYSIS.md)** - Comparison with ServiceNow

---

## Roadmap

### Phase 1: MVP (8 months - February 2026)

**Completed:**

-   [x] Authentication & Authorization (RBAC)
-   [x] User Profile Management
-   [x] Docker Infrastructure
-   [x] Testing Setup

**In Progress:**

-   [ ] Tickets CRUD (Sprint 2)
-   [ ] Comments System (Sprint 3)
-   [ ] Knowledge Base (Sprint 4)
-   [ ] Dashboard & SLA (Sprint 5)
-   [ ] Teams & Automation (Sprint 6)
-   [ ] Asset Management (Sprint 7)

**ITSM Score:** 8.5/10 (ITSM Professional)

### Phase 2: Post-MVP

-   [ ] Real-time updates (WebSockets/Reverb)
-   [ ] File attachments
-   [ ] Advanced reports (PDF/Excel export)
-   [ ] Public REST API (OAuth 2.0)
-   [ ] Mobile PWA

### Phase 3: Enterprise

-   [ ] Change Management (ITIL)
-   [ ] Problem Management (ITIL)
-   [ ] Multi-tenancy support
-   [ ] Configurable workflows
-   [ ] Email integration (IMAP)
-   [ ] Native mobile apps

**[Complete Roadmap →](docs/MVP.md)**

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Contribution Workflow

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes following our conventions
# 4. Run tests
php artisan test

# 5. Commit using Conventional Commits
git commit -m "feat: add new feature X"

# 6. Push and create Pull Request
git push origin feature/your-feature-name
```

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

### Code Style

-   **PHP**: PSR-12 (enforced by Laravel Pint)
-   **JavaScript**: ESLint + Prettier
-   **Vue**: Vue 3 Composition API style guide

---

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

**Found a security issue?** Please email JMSS1995@hotmail.com instead of opening a public issue.

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
