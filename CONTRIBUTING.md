# Contributing Guide - OrionOne ITSM

**Last Updated:** November 13, 2025

Welcome! This guide will help you contribute to OrionOne following professional standards.

---

## Overview

OrionOne follows **Feature-Driven Development** with **Test-Driven Development (TDD)** practices. We prioritize code quality, type safety, and maintainability.

**Stack:** Next.js 15 + Nest.js 11 + Prisma 6 + PostgreSQL 18

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feat/feature-name
# Example: git checkout -b feat/ticket-comments
```

### 2. Follow TDD Cycle

**RED → GREEN → REFACTOR**

1. **RED**: Write failing test
2. **GREEN**: Implement minimum code to pass
3. **REFACTOR**: Improve code while keeping tests green

See detailed methodology: [`docs/guides/Development-Guide.md`](docs/guides/Development-Guide.md)

### 3. Run Quality Checks

**Backend:**

```bash
cd nest-backend
npm run test # All tests
npm run lint # Code quality
npm run build # Type checking
```

**Frontend:**

```bash
cd next-frontend
npm run test # All tests
npm run lint # Code quality
npm run type-check # TypeScript
```

### 4. Commit Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat(tickets): add comment functionality

- Add Comment model to Prisma schema
- Implement CommentsService with CRUD
- Add validation with class-validator
- Create comment form with React Hook Form
- Add unit and E2E tests

Refs: #42"
```

**Types:**

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Add tests
- `chore:` Maintenance

**Scopes:** `auth`, `tickets`, `assets`, `users`, `kb`, `api`, `ui`

### 5. Push & Create PR

```bash
git push origin feat/feature-name
```

Create Pull Request on GitHub with:

- Clear description
- Screenshots (if UI changes)
- Related issue number

---

## Code Conventions

### TypeScript

- **Strict mode** enabled (`tsconfig.json`)
- **ESLint + Prettier** for formatting
- **No `any` types** - use proper typing
- **Functional components** (React)
- **Descriptive variable names** (no abbreviations)

### Backend (Nest.js)

- **DTOs**: Use `class-validator` decorators (`@IsString`, `@IsEmail`, `@MinLength`)
- **Services**: Business logic layer, inject PrismaService
- **Controllers**: Route handlers with `@ApiOperation` for Swagger docs
- **Error handling**: Use built-in HTTP exceptions (`NotFoundException`, `BadRequestException`)

### Frontend (Next.js)

- **Components**: Functional components with TypeScript
- **Forms**: React Hook Form + Zod validation
- **State**: Local state with `useState`, server state with TanStack Query
- **Styling**: Tailwind CSS utility classes + shadcn/ui components

### Database (Prisma)

- **Models**: `PascalCase` (singular) - `User`, `Ticket`, `Asset`
- **Fields**: `camelCase` - `userId`, `createdAt`, `ticketNo`
- **Relations**: Descriptive names - `@relation("TicketRequester")`
- **Enums**: `PascalCase` with `UPPERCASE` values - `TicketStatus { OPEN, CLOSED }`
- **Indexes**: Add `@@index()` for foreign keys and frequently queried fields

 **Code examples:** See [TECH-STACK.md](../TECH-STACK.md) for detailed implementation patterns

---

## Testing Strategy

### Backend Tests (Jest + Supertest)

- **Unit Tests**: Test services in isolation with mocked dependencies
- **Integration Tests**: Test controllers with real database (test DB)
- **E2E Tests**: Test complete flows from HTTP request to database

### Frontend Tests (Jest + React Testing Library)

- **Component Tests**: Test user interactions and rendering
- **Hook Tests**: Test custom hooks in isolation
- **Integration Tests**: Test forms with validation and API calls

### Coverage Requirements

- **Minimum 80%** test coverage for all modules
- **All services** must have unit tests
- **Critical user flows** must have E2E tests

### Running Tests

```bash
# Backend
cd nest-backend
npm run test # Unit tests
npm run test:e2e # E2E tests
npm run test:cov # Coverage report

# Frontend
cd next-frontend
npm run test # All tests
npm run test:watch # Watch mode
```

- **Critical paths** must have E2E tests

---

## Common Commands

**Backend:**

```bash
npm run start:dev # Dev server
npm run test # Run tests
npm run test:cov # Coverage
npm run lint # Lint code
npm run prisma:studio # Database GUI
```

**Frontend:**

```bash
npm run dev # Dev server
npm run test # Run tests
npm run lint # Lint code
npm run build # Production build
```

**Database:**

```bash
npm run prisma:generate # Generate client
npm run prisma:migrate:dev # Create migration
npm run prisma:seed # Seed data
npm run prisma:studio # Database GUI
```

**Docker:**

```bash
docker compose up -d # Start services
docker compose logs -f # View logs
docker exec -it orionone_postgres psql -U orionone # PostgreSQL shell
```

---

## Quality Checklist

Before submitting PR, ensure:

- [ ] All tests passing (`npm run test`)
- [ ] Code coverage >80%
- [ ] No linting errors (`npm run lint`)
- [ ] TypeScript strict mode passes
- [ ] Prisma schema validated
- [ ] API documented in Swagger
- [ ] Conventional commit format
- [ ] PR description clear and complete

---

## Need Help?

- **Commands:** See [`docs/COMMANDS-REFERENCE.md`](docs/COMMANDS-REFERENCE.md)
- **Components:** See [`docs/COMPONENTS-GUIDE.md`](docs/COMPONENTS-GUIDE.md)
- **TDD Workflow:** See [`docs/guides/Development-Guide.md`](docs/guides/Development-Guide.md)
- **Roadmap:** See [`docs/DEVELOPMENT-PLAN.md`](docs/DEVELOPMENT-PLAN.md)
- **Tech Stack:** See [`TECH-STACK.md`](TECH-STACK.md)

---

**Thank you for contributing to OrionOne!** 
