# Arquitetura do OrionOne - Next.js 15 + Nest.js 10

> **Stack**: Next.js 15 (App Router) + Nest.js 10 + Prisma + TypeScript
> **Versão**: v1.0.0 (em desenvolvimento)
> **Última atualização**: 13 Nov 2024

---

## 📋 Visão Geral

OrionOne utiliza uma arquitetura **moderna full-stack TypeScript** com separação clara entre frontend e backend, otimizada para:

-   **Type-Safety End-to-End**: TypeScript em toda a stack
-   **Prazo de desenvolvimento**: 10 semanas para MVP (13 Nov - 31 Jan 2025)
-   **Manutenibilidade**: Código modular, testável e documentado
-   **Performance**: React Server Components, API otimizada, caching estratégico
-   **Escalabilidade**: Arquitetura preparada para crescimento

---

## 🏗️ Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                    │
│                      Next.js 15 Frontend                     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  App Router (RSC)                                    │   │
│  │  - app/(auth)/: Login, Register, Password Reset     │   │
│  │  - app/(dashboard)/: Protected routes              │   │
│  │  - app/api/: Edge API routes (opcional)            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Componentes React                                   │   │
│  │  - Shadcn-ui (new-york style, zinc base)           │   │
│  │  - Client Components: Forms, Modals, Interações    │   │
│  │  - Server Components: Data fetching, Layout        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  State Management                                    │   │
│  │  - Zustand: Auth, Theme, UI state                  │   │
│  │  - React Query: Server state, caching              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
                        (Axios Client)
┌─────────────────────────────────────────────────────────────┐
│                      CAMADA DE API                           │
│                     Nest.js 10 Backend                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Controllers (API Endpoints)                        │   │
│  │  - @Controller(): Routing                          │   │
│  │  - @Get/@Post/@Put/@Delete: HTTP methods          │   │
│  │  - @UseGuards(JwtAuthGuard): Auth protection       │   │
│  │  - Swagger decorators: API documentation           │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Services (Business Logic)                          │   │
│  │  - @Injectable(): Dependency injection             │   │
│  │  - Business rules & validations                    │   │
│  │  - Orchestration de múltiplos recursos            │   │
│  └─────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Repositories (Data Access)                         │   │
│  │  - Prisma Client: Type-safe ORM                    │   │
│  │  - CRUD operations                                  │   │
│  │  - Complex queries & relations                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Middleware & Guards                                │   │
│  │  - JwtAuthGuard: JWT token validation             │   │
│  │  - CaslAbilityGuard: Permission checking           │   │
│  │  - AllExceptionsFilter: Global error handling      │   │
│  │  - LoggingInterceptor: Request/Response logging    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      (Prisma ORM)
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE DADOS                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ PostgreSQL 16│  │  Redis 7.2   │  │ Meilisearch  │     │
│  │              │  │              │  │   1.9        │     │
│  │ - 15 Tables  │  │ - Sessions   │  │ - Full-text  │     │
│  │ - Relations  │  │ - Cache      │  │   search     │     │
│  │ - Triggers   │  │ - Queues     │  │ - Tickets    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Storage    │  │   Mailpit    │  │    Nginx     │     │
│  │              │  │              │  │              │     │
│  │ - Local/S3   │  │ - Email test │  │ - Reverse    │     │
│  │ - Avatars    │  │   (dev)      │  │   proxy      │     │
│  │ - Uploads    │  │ - SMTP       │  │ - / → frontend│    │
│  └──────────────┘  └──────────────┘  │ - /api → back│     │
│                                       └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Padrões Arquiteturais

### Backend: Nest.js Modular Architecture

```typescript
// app.module.ts - Root Module
@Module({
    imports: [
        ConfigModule.forRoot(),
        PrismaModule, // Database
        AuthModule, // Authentication
        UsersModule, // User management
        TicketsModule, // Tickets CRUD
        CommentsModule, // Comments
        ArticlesModule, // Knowledge base
        AssetsModule, // Asset tracking
        NotificationsModule, // Real-time notifications
        UploadModule, // File uploads
        LoggerModule, // Winston logging
    ],
})
export class AppModule {}
```

**Princípios**:

-   **Single Responsibility**: Cada module tem uma responsabilidade clara
-   **Dependency Injection**: @Injectable() para loose coupling
-   **Guards & Interceptors**: Cross-cutting concerns (auth, logging, errors)
-   **DTO Validation**: class-validator + class-transformer
-   **Swagger Documentation**: @ApiTags, @ApiResponse decorators

### Frontend: Next.js App Router + Component Patterns

```typescript
// app/(dashboard)/tickets/page.tsx - Server Component
export default async function TicketsPage() {
    // Server-side data fetching (RSC)
    const initialTickets = await fetchTickets();

    return <TicketsClientList initialData={initialTickets} />;
}

// components/tickets/tickets-client-list.tsx - Client Component
("use client");
export function TicketsClientList({ initialData }) {
    // React Query para client-side caching
    const { data } = useTickets({ initialData });

    return <DataTable data={data} columns={ticketColumns} />;
}
```

**Princípios**:

-   **Server First**: RSC para data fetching quando possível
-   **Client quando necessário**: 'use client' apenas para interatividade
-   **Zustand para UI State**: Auth, theme, sidebar, modals
-   **React Query para Server State**: API data, caching, mutations
-   **Composition over Inheritance**: Shadcn-ui composable components

---

## 📦 Estrutura de Pastas

### Backend: nest-backend/

```
nest-backend/
├── src/
│   ├── main.ts                    # Bootstrap application
│   ├── app.module.ts              # Root module
│   │
│   ├── auth/                      # Authentication module
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts     # Login, register endpoints
│   │   ├── auth.service.ts        # JWT generation, password hashing
│   │   ├── jwt.strategy.ts        # Passport JWT strategy
│   │   └── dto/
│   │       ├── login.dto.ts
│   │       └── register.dto.ts
│   │
│   ├── users/                     # User management
│   │   ├── users.module.ts
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   └── dto/
│   │
│   ├── tickets/                   # Tickets CRUD
│   │   ├── tickets.module.ts
│   │   ├── tickets.controller.ts
│   │   ├── tickets.service.ts     # SLA calculation, ticketNumber
│   │   └── dto/
│   │
│   ├── upload/                    # File uploads
│   │   ├── upload.module.ts
│   │   ├── upload.controller.ts
│   │   ├── upload.service.ts      # Sharp processing, WebP
│   │   └── dto/
│   │
│   ├── casl/                      # Authorization
│   │   ├── casl.module.ts
│   │   ├── ability.factory.ts     # Define permissions
│   │   └── casl.guard.ts          # Permission checking
│   │
│   ├── prisma/                    # Database
│   │   ├── prisma.module.ts
│   │   ├── prisma.service.ts      # PrismaClient wrapper
│   │   └── schema.prisma          # 15 models, 6 enums
│   │
│   ├── common/                    # Shared code
│   │   ├── filters/
│   │   │   └── all-exceptions.filter.ts  # Global error handler
│   │   ├── interceptors/
│   │   │   └── logging.interceptor.ts    # Request logging
│   │   ├── guards/
│   │   │   └── jwt-auth.guard.ts
│   │   └── decorators/
│   │       └── current-user.decorator.ts
│   │
│   └── config/                    # Configuration
│       ├── database.config.ts
│       └── jwt.config.ts
│
├── prisma/
│   ├── schema.prisma              # Prisma schema (15 models)
│   ├── migrations/                # Database migrations
│   └── seed.ts                    # Seed data (32 permissions)
│
├── test/                          # E2E tests
├── .env                           # Environment variables
├── tsconfig.json                  # TypeScript strict mode
└── nest-cli.json
```

### Frontend: next-frontend/

```
next-frontend/
├── app/
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Home page
│   ├── globals.css                # Tailwind + CSS variables
│   │
│   ├── (auth)/                    # Auth group (centered layout)
│   │   ├── layout.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── forgot-password/
│   │       └── page.tsx
│   │
│   ├── (dashboard)/               # Dashboard group (sidebar layout)
│   │   ├── layout.tsx             # Sidebar + header
│   │   ├── dashboard/
│   │   │   └── page.tsx           # Overview cards
│   │   ├── tickets/
│   │   │   ├── page.tsx           # Tickets list
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx       # Ticket detail
│   │   │   └── new/
│   │   │       └── page.tsx       # Create ticket
│   │   ├── knowledge-base/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   ├── assets/
│   │   ├── users/
│   │   └── settings/
│   │
│   └── api/                       # Edge API routes (opcional)
│       └── health/
│           └── route.ts
│
├── components/
│   ├── ui/                        # Shadcn-ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   │
│   ├── layout/                    # Layout components
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── footer.tsx
│   │
│   ├── tickets/                   # Feature components
│   │   ├── ticket-form.tsx
│   │   ├── ticket-card.tsx
│   │   ├── ticket-status-badge.tsx
│   │   └── tickets-client-list.tsx
│   │
│   └── forms/                     # Reusable forms
│       ├── login-form.tsx
│       ├── register-form.tsx
│       └── ticket-form.tsx
│
├── lib/
│   ├── utils.ts                   # cn() utility
│   ├── api.ts                     # Axios instance
│   │
│   ├── hooks/                     # React Query hooks
│   │   ├── use-tickets.ts         # useTickets(), useCreateTicket()
│   │   ├── use-auth.ts            # useLogin(), useRegister()
│   │   └── use-notifications.ts
│   │
│   └── stores/                    # Zustand stores
│       ├── auth-store.ts          # user, token, logout()
│       ├── theme-store.ts         # theme, toggleTheme()
│       └── sidebar-store.ts       # isOpen, toggle()
│
├── types/                         # TypeScript types
│   ├── ticket.ts
│   ├── user.ts
│   └── api.ts
│
├── public/                        # Static files
├── .env.local                     # Environment variables
├── components.json                # Shadcn-ui config
├── tsconfig.json                  # TypeScript config
└── next.config.ts                 # Next.js config
```

---

## 🔐 Camada de Segurança

### Authentication Flow (JWT)

```typescript
// 1. Login Request (Next.js → Nest.js)
POST /api/auth/login
Body: { email, password }

// 2. Backend valida credenciais (Nest.js)
AuthService:
  - findUserByEmail()
  - bcrypt.compare(password, hash)
  - generateJwtToken() → { access_token, user }

// 3. Frontend armazena token (Zustand)
useAuthStore.setState({
  user,
  token: access_token,
  isAuthenticated: true
})

// 4. Requests subsequentes incluem token (Axios)
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

// 5. Backend valida JWT (JwtAuthGuard)
@UseGuards(JwtAuthGuard)
async getProfile(@CurrentUser() user: User) {
  return user;
}
```

### Authorization (CASL)

```typescript
// ability.factory.ts - Define permissions
export class AbilityFactory {
    createForUser(user: User) {
        const { can, build } = new AbilityBuilder(Ability);

        if (user.role === "ADMIN") {
            can("manage", "all"); // Tudo
        } else if (user.role === "AGENT") {
            can("read", "Ticket");
            can("update", "Ticket", { assigneeId: user.id }); // Apenas tickets assignados
            can("create", "Comment");
        } else {
            can("read", "Ticket", { createdById: user.id }); // Apenas seus tickets
            can("create", "Ticket");
        }

        return build();
    }
}

// Uso em componente (Next.js)
const ability = useAbility();
{
    ability.can("update", ticket) && <EditButton />;
}
```

---

## 📊 Camada de Dados - Prisma Schema

Ver documentação completa em: `docs/MIGRATION-PART-2-BACKEND.md`

**15 Models**: User, Role, Permission, RoleHasPermissions, Team, Ticket, Comment, Category, Article, Asset, Media, Notification, ActivityLog, Announcement

**6 Enums**: Role, TicketStatus, TicketPriority, AssetStatus, NotificationType, ActivityAction

**Highlights**:

-   UUID Primary Keys (segurança)
-   Timestamps automáticos (createdAt, updatedAt)
-   Indexes para performance (status, priority, createdById)
-   Fulltext Search (@fulltext para Meilisearch)
-   Polymorphic Media (avatares, anexos)

---

## 🚀 Performance & Caching

### Backend Caching (Redis)

```typescript
// tickets.service.ts
async findAll() {
  const cacheKey = 'tickets:all';

  // Try cache first
  const cached = await this.redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Query database
  const tickets = await this.prisma.ticket.findMany({
    include: { createdBy: true, assignee: true }
  });

  // Cache for 5 minutes
  await this.redis.setex(cacheKey, 300, JSON.stringify(tickets));

  return tickets;
}
```

### Frontend Caching (React Query)

```typescript
// lib/hooks/use-tickets.ts
export function useTickets() {
    return useQuery({
        queryKey: ["tickets"],
        queryFn: fetchTickets,
        staleTime: 5 * 60 * 1000, // 5 minutes
        cacheTime: 10 * 60 * 1000, // 10 minutes
    });
}

// Optimistic updates on mutations
export function useUpdateTicket() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: updateTicket,
        onMutate: async (newTicket) => {
            await queryClient.cancelQueries(["tickets"]);
            const previous = queryClient.getQueryData(["tickets"]);
            queryClient.setQueryData(["tickets"], (old) =>
                old.map((t) => (t.id === newTicket.id ? newTicket : t))
            );
            return { previous };
        },
        onError: (err, variables, context) => {
            queryClient.setQueryData(["tickets"], context.previous);
        },
        onSuccess: () => {
            queryClient.invalidateQueries(["tickets"]);
        },
    });
}
```

---

## 🐳 Docker & DevOps

### Containers (8 services)

```yaml
# docker-compose.yml
services:
    postgres: # PostgreSQL 16 database
    redis: # Redis 7.2 cache/sessions
    meilisearch: # Meilisearch 1.9 search
    mailpit: # Email testing (dev)
    backend: # Nest.js API (port 3001)
    frontend: # Next.js app (port 3000)
    nginx: # Reverse proxy (port 80)
```

**Network**: `orionone_network` (bridge)

### Reverse Proxy (Nginx)

```nginx
# nginx.conf
upstream frontend {
  server frontend:3000;
}

upstream backend {
  server backend:3001;
}

server {
  listen 80;

  # Frontend
  location / {
    proxy_pass http://frontend;
  }

  # Backend API
  location /api {
    proxy_pass http://backend;
  }
}
```

**Access**:

-   Frontend: http://localhost
-   Backend API: http://localhost/api
-   Swagger Docs: http://localhost/api/docs
-   Mailpit: http://localhost:8025

---

## 🧪 Estratégia de Testes

### Backend (Nest.js)

```typescript
// tickets.service.spec.ts - Unit Tests
describe("TicketsService", () => {
    it("should create ticket with SLA", async () => {
        const ticket = await service.create({
            title: "Test",
            priority: "HIGH",
        });

        expect(ticket.ticketNumber).toMatch(/^TKT-\d{8}-\d{4}$/);
        expect(ticket.slaDeadline).toBeDefined();
    });
});

// tickets.e2e-spec.ts - E2E Tests
describe("Tickets API (e2e)", () => {
    it("/tickets (GET) returns all tickets", () => {
        return request(app.getHttpServer())
            .get("/tickets")
            .set("Authorization", `Bearer ${token}`)
            .expect(200);
    });
});
```

### Frontend (Next.js)

```typescript
// components/tickets/ticket-form.test.tsx
describe("TicketForm", () => {
    it("submits valid ticket", async () => {
        const onSubmit = jest.fn();
        render(<TicketForm onSubmit={onSubmit} />);

        await userEvent.type(screen.getByLabelText("Title"), "Test Ticket");
        await userEvent.click(screen.getByText("Submit"));

        await waitFor(() => {
            expect(onSubmit).toHaveBeenCalled();
        });
    });
});
```

---

## 📚 Documentação & Ferramentas

### API Documentation (Swagger)

```typescript
// main.ts - Swagger setup
const config = new DocumentBuilder()
    .setTitle("OrionOne API")
    .setDescription("ITSM Platform API")
    .setVersion("1.0")
    .addBearerAuth()
    .build();

const document = SwaggerModule.createDocument(app, config);
SwaggerModule.setup("api/docs", app, document);
```

**Acesso**: http://localhost:3001/api/docs

### Logging (Winston)

```typescript
// logger.module.ts
WinstonModule.forRoot({
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.colorize()
            ),
        }),
        new winston.transports.File({
            filename: "logs/error.log",
            level: "error",
        }),
        new winston.transports.File({
            filename: "logs/combined.log",
        }),
    ],
});
```

---

## 🔄 Próximos Passos

### Semana 0 (13-17 Nov) - Foundation

-   [x] Projetos criados (Nest.js + Next.js)
-   [x] .env configurados
-   [ ] Docker + Nginx (Week 0 Day 3)
-   [ ] Prisma schema + migrations (Week 0 Day 4)
-   [ ] Health check + CORS (Week 0 Day 4)

### Semana 1 (18-22 Nov) - Auth

-   [ ] Seed data (32 permissions)
-   [ ] AuthModule (JWT)
-   [ ] CASL AbilityFactory
-   [ ] UsersModule CRUD
-   [ ] UploadModule (Sharp)

### Semana 2-3 (25 Nov - 6 Dec) - Tickets

-   [ ] TicketsModule backend
-   [ ] Tailwind CSS migration
-   [ ] Tickets frontend (list, create, detail)
-   [ ] Tiptap editor

---

## 📖 Referências

### Documentação Oficial

-   [Next.js 15 Docs](https://nextjs.org/docs)
-   [Nest.js Docs](https://docs.nestjs.com)
-   [Prisma Docs](https://www.prisma.io/docs)
-   [Shadcn-ui](https://ui.shadcn.com)

### Migração

-   `MIGRATION-PART-1-SETUP.md` - Infrastructure
-   `MIGRATION-PART-2-BACKEND.md` - Nest.js + Prisma
-   `MIGRATION-PART-3-FRONTEND.md` - Next.js + React
-   `MIGRATION-PART-4-TIMELINE.md` - 10-week plan
-   `MIGRATION-PART-5-CLEANUP.md` - Cleanup & archive

### Backup Laravel/Vue

-   `docs/archive-laravel-vue/` - Documentação arquivada
-   Git tag: `v0.1.0-laravel`

---

**Última atualização**: 13 Nov 2024
**Mantido por**: [@JMSS95](https://github.com/JMSS95)
