<div align="center">

<img src="logo/OrionOne.png" alt="OrionOne Logo" width="200"/>

**Modern IT Service Management Platform**

[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat)](https://github.com/JMSS95/OrionOne)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Nest.js](https://img.shields.io/badge/Nest.js-11-E0234E?style=flat&logo=nestjs&logoColor=white)](https://nestjs.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](CONTRIBUTING.md)

</div>

---

## About

**OrionOne** is a modern **ITSM (IT Service Management) platform** built with Next.js 15, Nest.js 11, and TypeScript. Designed for enterprise-grade IT operations with features inspired by ServiceNow and Jira Service Desk.

### Key Features

-   **90% cost savings** compared to market leaders ($20/agent vs $200+)
-   **Rich Text Editor** with Tiptap for professional ticket descriptions
-   **AI-powered Search** with Meilisearch (typo-tolerant, instant results)
-   **Advanced SLA Management** with configurable policies
-   **Modern Stack** with Next.js 15 + Nest.js 11 + Prisma 6 + PostgreSQL 18

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

| Layer        | Technology   | Version | Purpose            |
| ------------ | ------------ | ------- | ------------------ |
| **Backend**  | Nest.js      | 11.1.8  | RESTful API        |
|              | Prisma       | 6.4.0   | Type-safe ORM      |
|              | PostgreSQL   | 18.0    | Primary database   |
|              | Redis        | 8.2     | Cache & sessions   |
|              | Meilisearch  | 1.25    | Full-text search   |
| **Frontend** | Next.js      | 15.5.6  | React 19 framework |
|              | shadcn/ui    | latest  | Component library  |
|              | Tailwind CSS | v4      | Utility-first CSS  |
| **DevOps**   | Docker       | latest  | Containerization   |
|              | Nginx        | 1.24+   | Reverse proxy      |

**Detailed documentation:** [TECH-STACK.md](TECH-STACK.md)

---

## Quick Start

```bash
# Clone and setup (10 minutes)
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne
docker compose up -d

# Backend setup
cd nest-backend && npm install && npm run prisma:migrate:dev && npm run start:dev

# Frontend setup (new terminal)
cd next-frontend && npm install && npm run dev
```

** Full setup guide:** [SETUP.md](SETUP.md)

**Access:**

-   Frontend: http://localhost:3000
-   Backend API: http://localhost:3001/api
-   Login: `admin@orionone.com` / `Admin123!`

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
 nest-backend/ # Nest.js 11 API
 prisma/ # Database schema + migrations
 schema.prisma # 15 models (User, Ticket, Article, etc.)
 migrations/ # Database migrations
 seed.ts # Seed data (5 users, 8 categories, etc.)
 src/ # Source code
 modules/ # Feature modules (auth, users, tickets, etc.)
 prisma/ # Prisma service
 main.ts # Application entry point
 test/ # E2E tests
 next-frontend/ # Next.js 15 SPA
 app/ # Pages (App Router)
 layout.tsx # Root layout
 page.tsx # Home page
 components/ # React components (shadcn/ui)
 lib/ # Utilities
 public/ # Static assets
 docs/ # Documentation
 DEVELOPMENT-PLAN.md # 6-sprint roadmap
 MVP.md # MVP features & status
 TECH-STACK.md # Technology stack details
 SPRINT-0-SETUP.md # Sprint 0 setup guide
 guides/ # Implementation guides
 docker/ # Docker configuration
 logo/ # OrionOne branding
 OrionOne.png # Logo image
 scripts/ # Utility scripts
 docker-compose.yml # 7-service orchestration
 nginx.conf # Reverse proxy configuration
 .env.example # Environment variables template
 SETUP.md # Quick setup guide
```

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
