<div align="center">

<img src="logo/OrionOne.png" alt="OrionOne Logo"/>

**Modern IT Service Management Platform**

[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat)](https://github.com/JMSS95/OrionOne)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Nest.js](https://img.shields.io/badge/Nest.js-11-E0234E?style=flat&logo=nestjs&logoColor=white)](https://nestjs.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-8.2-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Meilisearch](https://img.shields.io/badge/Meilisearch-1.25-FF5CAA?style=flat&logo=meilisearch&logoColor=white)](https://www.meilisearch.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#tech-stack) • [Documentation](#-documentation) • [Contributing](CONTRIBUTING.md)

</div>

---

## About

**OrionOne** is a modern **ITSM (IT Service Management) platform** built with Next.js 15, Nest.js 11, and TypeScript. Designed for enterprise-grade IT operations with features inspired by ServiceNow and Jira Service Desk.

### Key Features

-   **Multi-Role Authentication** - JWT-based auth with Admin, Agent, and User roles
-   **Incident Management** - Complete CRUD with priorities, SLA tracking, and status workflow
-   **Rich Text Editor** - Tiptap editor for professional ticket descriptions with formatting
-   **AI-Powered Search** - Meilisearch with typo-tolerance and instant results
-   **Real-Time Collaboration** - Comments and file attachments on incidents
-   **Knowledge Base** - Searchable articles with full-text search
-   **SLA Management** - Configurable policies with automated tracking (24/7)
-   **Dashboard & Analytics** - Real-time metrics and performance insights
-   **Email Notifications** - Automated alerts for assignments and updates
-   **Docker Ready** - Complete containerized setup with Redis, PostgreSQL, and Meilisearch
-   **90% Cost Savings** - Enterprise features at $20/agent vs $200+ (ServiceNow, Zendesk)

---

## Features

| Feature                 | Description                                        | Status   |
| ----------------------- | -------------------------------------------------- | -------- |
| Authentication          | Multi-role (Admin, Agent, User) with JWT + refresh | Sprint 1 |
| User & Team Management  | RBAC with granular permissions                     | Sprint 1 |
| Incident Management     | CRUD, priorities, status, SLA tracking             | Sprint 2 |
| Rich Text Editor        | Tiptap editor for professional descriptions        | Sprint 2 |
| AI-Powered Search       | Meilisearch with typo-tolerance                    | Sprint 2 |
| Comments & Attachments  | Real-time collaboration with file uploads          | Sprint 3 |
| Knowledge Base          | Full-text search powered by Meilisearch            | Sprint 4 |
| Advanced SLA Management | Configurable SLA policies with escalation          | Sprint 5 |
| Dashboard & Analytics   | Real-time metrics and team performance stats       | Sprint 6 |

**MVP Target:** January 31, 2026 (13 weeks) • [Complete Roadmap →](docs/DEVELOPMENT-PLAN.md)

---

## Tech Stack

### Backend

| Technology      | Version | Purpose                                          |
| --------------- | ------- | ------------------------------------------------ |
| **Nest.js**     | 11.1.8  | Enterprise-grade Node.js framework for REST APIs |
| **Prisma**      | 6.4.0   | Type-safe ORM with migrations                    |
| **PostgreSQL**  | 18.0    | Primary relational database (pgcrypto, pg_trgm)  |
| **Redis**       | 8.2     | Session storage, caching, and job queues         |
| **Meilisearch** | 1.25    | Lightning-fast full-text search engine           |
| **Jest**        | 30.0.0  | Testing framework with ts-jest                   |
| **Passport**    | 0.7.0   | Authentication middleware (JWT strategy)         |

### Frontend

| Technology          | Version | Purpose                                 |
| ------------------- | ------- | --------------------------------------- |
| **Next.js**         | 15.5.6  | React framework with App Router & SSR   |
| **React**           | 19.2.0  | UI library with Server Components       |
| **TypeScript**      | 5.6+    | Type-safe JavaScript with strict mode   |
| **shadcn/ui**       | latest  | Accessible component library (Radix UI) |
| **Tailwind CSS**    | v4      | Utility-first CSS framework             |
| **TanStack Query**  | 5.x     | Server state management with caching    |
| **Zod**             | 4.x     | TypeScript-first schema validation      |
| **Tiptap**          | 2.x     | Rich text editor (headless)             |
| **React Hook Form** | 7.x     | Performant form library                 |
| **Axios**           | 1.13.2  | HTTP client with interceptors           |

### DevOps & Infrastructure

| Technology         | Version | Purpose                                    |
| ------------------ | ------- | ------------------------------------------ |
| **Docker**         | latest  | Container platform for all services        |
| **Docker Compose** | v2      | Multi-container orchestration (7 services) |
| **Nginx**          | 1.24+   | Reverse proxy and load balancer            |
| **Playwright**     | 1.x     | End-to-end testing framework               |

### Development Tools

| Tool                | Purpose                                     |
| ------------------- | ------------------------------------------- |
| **ESLint**          | Code linting and style enforcement          |
| **Prettier**        | Code formatting                             |
| **Husky**           | Git hooks for pre-commit checks             |
| **Winston**         | Logging framework (configured)              |
| **Swagger/OpenAPI** | API documentation (configured at /api/docs) |

**Detailed documentation:** [TECH-STACK.md](docs/TECH-STACK.md)

---

## Quick Start

### Prerequisites

-   **Docker** & **Docker Compose** installed
-   **Node.js** 20+ (for local development)
-   **Git** for version control

### Setup with Docker (Recommended - 5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# 2. Copy environment files
cp nest-backend/.env.example nest-backend/.env
cp next-frontend/.env.example next-frontend/.env

# 3. Start all services with Docker Compose
docker compose up -d

# This will start:
# - PostgreSQL 18.0 (port 5432)
# - Redis 8.2 (port 6379)
# - Meilisearch 1.25 (port 7700)
# - Nest.js Backend (port 3001)
# - Next.js Frontend (port 3000)
# - Nginx Reverse Proxy (port 80)

# 4. Run database migrations
cd nest-backend
npm install
npm run prisma:migrate:dev
npm run prisma:seed # Optional: seed with sample data

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:3001/api
# API Docs: http://localhost:3001/api/docs
# Meilisearch: http://localhost:7700
```

### Manual Setup (Alternative - 10 minutes)

```bash
# 1. Start infrastructure services only
docker compose up -d postgres redis meilisearch

# 2. Backend setup
cd nest-backend
npm install
npm run prisma:migrate:dev
npm run start:dev # Runs on http://localhost:3001

# 3. Frontend setup (new terminal)
cd next-frontend
npm install
npm run dev # Runs on http://localhost:3000
```

**Full setup guide with troubleshooting:** [SETUP.md](SETUP.md)

### Default Access Credentials

After running the seed script (development only):

| Role  | Email             | Password       |
| ----- | ----------------- | -------------- |
| Admin | admin@orionone.io | See .env file |
| Agent | agent@orionone.io | See .env file |
| User  | user@orionone.io  | See .env file |

> **Note:** Change these credentials in production. Default passwords are defined in `nest-backend/prisma/seed.ts`

---

## Documentation

| Document                                                 | Description                                |
| -------------------------------------------------------- | ------------------------------------------ |
| [SETUP.md](SETUP.md)                                     | Complete setup guide (10 minutes)          |
| [TECH-STACK.md](TECH-STACK.md)                           | Complete technology stack details          |
| [docs/DEVELOPMENT-PLAN.md](docs/DEVELOPMENT-PLAN.md)     | 6-sprint roadmap (13 weeks)                |
| [docs/SPRINT-0-SETUP.md](docs/SPRINT-0-SETUP.md)         | Sprint 0 infrastructure setup              |
| [CONTRIBUTING.md](CONTRIBUTING.md)                       | How to contribute (workflow + conventions) |
| [DEPLOYMENT.md](DEPLOYMENT.md)                           | Production deployment guide                |
| [docs/COMMANDS-REFERENCE.md](docs/COMMANDS-REFERENCE.md) | All CLI commands                           |
| [docs/COMPONENTS-GUIDE.md](docs/COMPONENTS-GUIDE.md)     | shadcn/ui components catalog               |

---

## Development

### Common Commands

```bash
# Backend (nest-backend/)
npm run start:dev # Dev server with watch mode
npm run test # Run all tests
npm run prisma:studio # Database GUI

# Frontend (next-frontend/)
npm run dev # Dev server
npm run test # Run all tests
npm run lint # Check code quality

# Infrastructure
docker compose up -d # Start services
docker compose logs -f # View logs
docker compose down # Stop services
```

### Project Structure

```
orionone/
 nest-backend/ # Nest.js 11 REST API
 prisma/
 schema.prisma # Database schema (15+ models)
 migrations/ # Database version control
 seed.ts # Sample data seeding
 src/
 auth/ # Authentication module (JWT + Passport)
 users/ # User management
 incidents/ # Incident CRUD + SLA
 comments/ # Comment system
 attachments/ # File upload handling
 articles/ # Knowledge Base
 search/ # Meilisearch integration
 slapolicies/ # SLA policy management
 dashboard/ # Metrics & analytics
 email/ # Email notifications
 prisma/ # Prisma service
 main.ts # Bootstrap application
 test/ # E2E tests (Jest + Supertest)
 uploads/ # File storage directory
 package.json

 next-frontend/ # Next.js 15 with App Router
 app/
 (auth)/ # Authentication pages
 dashboard/ # Dashboard & metrics
 incidents/ # Incident management UI
 knowledge/ # Knowledge Base UI
 layout.tsx # Root layout
 page.tsx # Home page
 globals.css # Global styles
 components/
 ui/ # shadcn/ui components
 dashboard/ # Dashboard components
 incidents/ # Incident components
 tiptap/ # Rich text editor
 search/ # Search components
 lib/
 hooks/ # React custom hooks
 dto/ # TypeScript interfaces
 utils.ts # Utility functions
 public/
 images/ # Static assets
 tests/e2e/ # Playwright E2E tests
 package.json

 docker/ # Docker configuration
 nginx/
 nginx.conf # Nginx reverse proxy config

 docs/ # Comprehensive documentation
 DEVELOPMENT-PLAN.md # 6-sprint roadmap (13 weeks)
 MVP.md # MVP features & status
 TECH-STACK.md # Technology stack deep dive
 database-schema.md # Database architecture
 architecture.md # System architecture
 guides/ # Sprint implementation guides
 Sprint-1-guide.md # Auth & User Management
 Sprint-2-guide.md # Incidents & Rich Text
 Sprint-3-guide.md # Comments & Attachments
 Sprint-4-guide.md # Knowledge Base & Meilisearch
 Sprint-5-guide.md # SLA Tracking
 Sprint-6-guide.md # Dashboard & Notifications
 COMMANDS-REFERENCE.md # CLI commands reference

 scripts/ # Utility scripts
 remove_ai_emojis.py # Code cleanup scripts

 logo/ # Branding assets
 OrionOne.png

 docker-compose.yml # 7-service orchestration
 nginx.conf # Root nginx configuration
 .env.example # Environment template
 SETUP.md # Complete setup guide
 DEPLOYMENT.md # Production deployment
 CONTRIBUTING.md # Contribution guidelines
 LICENSE # MIT License
 README.md # This file
```

### Docker Services Architecture

The `docker-compose.yml` orchestrates 7 services:

| Service         | Port | Purpose                                  |
| --------------- | ---- | ---------------------------------------- |
| **postgres**    | 5432 | PostgreSQL 18.0 database                 |
| **redis**       | 6379 | Redis 8.2 for sessions & caching         |
| **meilisearch** | 7700 | Meilisearch 1.25 search engine           |
| **backend**     | 3001 | Nest.js API (depends on postgres, redis) |
| **frontend**    | 3000 | Next.js UI (depends on backend)          |
| **nginx**       | 80   | Reverse proxy (routes traffic)           |
| **pgadmin**     | 5050 | PostgreSQL GUI (optional, dev only)      |

---

## Roadmap

| Sprint       | Duration       | Focus Area                         | Status   |
| ------------ | -------------- | ---------------------------------- | -------- |
| **Sprint 0** | Nov 1-15       | Infrastructure Setup               | Complete |
| **Sprint 1** | Nov 16-27 (2w) | Authentication & User Management   | 70% Done |
| **Sprint 2** | Nov 28-Dec 6   | Incident + Rich Text + Meilisearch | Planned  |
| **Sprint 3** | Dec 7-17       | Comments & Attachments             | Planned  |
| **Sprint 4** | Dec 18-31      | Knowledge Base + Search            | Planned  |
| **Sprint 5** | Jan 1-10       | Advanced SLA Management            | Planned  |
| **Sprint 6** | Jan 11-31      | Dashboard + Polish + Buffer        | Planned  |

**MVP Target:** January 31, 2026 (13 weeks) • [Full Development Plan →](docs/DEVELOPMENT-PLAN.md)

---

## Contributing

We follow professional industry standards with TDD (Test-Driven Development) workflow:

1. **Fork & Clone** the repository
2. **Create feature branch**: `git checkout -b feat/your-feature`
3. **Follow TDD cycle**: RED → GREEN → REFACTOR
4. **Write tests first** (Jest + Supertest for backend, React Testing Library for frontend)
5. **Commit** with [Conventional Commits](https://www.conventionalcommits.org/)
6. **Push & Create PR**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file.

---

## Author

**João Santos**

-   GitHub: [@JMSS95](https://github.com/JMSS95)
-   Project: [OrionOne](https://github.com/JMSS95/OrionOne)

> **Academic Project** • CET - Specialist Technician in Information Systems Technologies and Programming
> Professional Training Center of Évora • 2024/2026

---

<div align="center">

**OrionOne ITSM Platform**
Built with for academic excellence

[ Back to Top](#orionone-itsm)

</div>
