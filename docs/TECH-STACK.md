# Technology Stack - OrionOne ITSM

**Last Updated:** November 13, 2025
**Project:** OrionOne - IT Service Management Platform
**Architecture:** Microservices (Backend API + Frontend SPA)

---

## Overview

OrionOne is built with a modern, type-safe full-stack TypeScript architecture optimized for enterprise-grade ITSM operations.

```

 FRONTEND 
 Next.js 15.5.6 + React 19.2.0 + shadcn/ui + Tailwind v4 

 REST API (JSON)

 BACKEND 
 Nest.js 11.1.8 + Prisma 6.4.0 + TypeScript 

 PostgreSQL 18 Redis 8.2 Meilisearch AWS S3
 (Database) (Cache) (Search) (Storage)
```

---

## Core Technologies

### Backend

#### Nest.js 11.1.8

- **Type:** Node.js framework
- **License:** MIT
- **Purpose:** RESTful API server
- **Documentation:** [https://docs.nestjs.com/](https://docs.nestjs.com/)
- **Key Features:**
 - TypeScript-first architecture
 - Modular design (Controllers, Services, Guards, Interceptors)
 - Dependency Injection
 - Built-in OpenAPI/Swagger documentation
 - Robust testing utilities (Jest + Supertest)

**Configuration:**

```typescript
// nest-backend/src/main.ts
const app = await NestFactory.create(AppModule);
app.setGlobalPrefix("api/v1");
app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
app.enableCors();
await app.listen(3000);
```

#### Prisma 6.4.0

- **Type:** ORM (Object-Relational Mapping)
- **License:** Apache 2.0
- **Purpose:** Type-safe database access
- **Documentation:** [https://www.prisma.io/docs](https://www.prisma.io/docs)
- **Key Features:**
 - Declarative schema with migrations
 - Auto-generated TypeScript types
 - Query builder with IntelliSense
 - Connection pooling
 - Transaction support

#### @nestjs/config

- **Type:** Configuration module
- **License:** MIT
- **Purpose:** Environment variables management
- **Documentation:** [https://docs.nestjs.com/techniques/configuration](https://docs.nestjs.com/techniques/configuration)
- **Key Features:**
 - Load `.env` files
 - Schema validation with Joi
 - Type-safe config access
 - Multiple environment support

**Example:**

```typescript
// app.module.ts
import { ConfigModule } from "@nestjs/config";

@Module({
 imports: [
 ConfigModule.forRoot({
 isGlobal: true,
 envFilePath: ".env",
 validationSchema: Joi.object({
 NODE_ENV: Joi.string().valid(
 "development",
 "production",
 "test"
 ),
 PORT: Joi.number().default(3000),
 DATABASE_URL: Joi.string().required(),
 JWT_SECRET: Joi.string().required(),
 }),
 }),
 ],
})
export class AppModule {}
```

#### @nestjs/throttler

- **Type:** Rate limiting module
- **License:** MIT
- **Purpose:** Protect against brute-force attacks
- **Documentation:** [https://docs.nestjs.com/security/rate-limiting](https://docs.nestjs.com/security/rate-limiting)
- **Key Features:**
 - Global or per-route rate limiting
 - Customizable time windows
 - Redis storage for distributed systems

**Example:**

```typescript
import { ThrottlerModule } from "@nestjs/throttler";

@Module({
 imports: [
 ThrottlerModule.forRoot([
 {
 ttl: 60000, // 1 minute
 limit: 10, // 10 requests per minute
 },
 ]),
 ],
})
export class AppModule {}

// Apply to specific routes
@Controller("auth")
@UseGuards(ThrottlerGuard)
export class AuthController {
 @Post("login")
 @Throttle({ default: { limit: 3, ttl: 60000 } }) // 3 attempts per minute
 async login() {}
}
```

#### Helmet

- **Type:** Security middleware
- **License:** MIT
- **Purpose:** Set secure HTTP headers
- **Documentation:** [https://helmetjs.github.io/](https://helmetjs.github.io/)
- **Headers Set:**
 - Content-Security-Policy
 - X-DNS-Prefetch-Control
 - X-Frame-Options
 - X-Content-Type-Options
 - Strict-Transport-Security

**Example:**

```typescript
// main.ts
import helmet from "helmet";

async function bootstrap() {
 const app = await NestFactory.create(AppModule);
 app.use(helmet());
 await app.listen(3000);
}
```

#### Compression

- **Type:** Compression middleware
- **License:** MIT
- **Purpose:** Gzip/Deflate compression for responses
- **Documentation:** [https://github.com/expressjs/compression](https://github.com/expressjs/compression)
- **Benefits:**
 - Reduce response size (60-80%)
 - Faster page loads
 - Lower bandwidth costs

**Example:**

```typescript
// main.ts
import compression from "compression";

async function bootstrap() {
 const app = await NestFactory.create(AppModule);
 app.use(compression());
 await app.listen(3000);
}
```

#### Passport + passport-jwt

- **Type:** Authentication middleware
- **License:** MIT
- **Purpose:** JWT authentication strategy
- **Documentation:** [https://www.passportjs.org/](https://www.passportjs.org/) • [https://docs.nestjs.com/security/authentication](https://docs.nestjs.com/security/authentication)
- **Key Features:**
 - Multiple authentication strategies
 - Session management
 - Serialization/deserialization

**Example:**

```typescript
// jwt.strategy.ts
import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from "passport-jwt";

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
 constructor(private configService: ConfigService) {
 super({
 jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
 ignoreExpiration: false,
 secretOrKey: configService.get("JWT_SECRET"),
 });
 }

 async validate(payload: any) {
 return {
 userId: payload.sub,
 email: payload.email,
 roles: payload.roles,
 };
 }
}
```

#### class-transformer + class-validator

- **Type:** Validation libraries
- **License:** MIT
- **Purpose:** DTO validation and transformation
- **Documentation:** [https://github.com/typestack/class-validator](https://github.com/typestack/class-validator) • [https://github.com/typestack/class-transformer](https://github.com/typestack/class-transformer)
- **Key Features:**
 - Decorator-based validation
 - Type coercion
 - Nested validation
 - Custom validators

**Example:**

```typescript
import {
 IsString,
 IsEmail,
 IsEnum,
 MinLength,
 MaxLength,
 IsOptional,
} from "class-validator";
import { Transform } from "class-transformer";

export class CreateUserDto {
 @IsEmail()
 email: string;

 @IsString()
 @MinLength(8)
 @MaxLength(32)
 password: string;

 @IsEnum(["ADMIN", "AGENT", "USER"])
 role: string;

 @IsOptional()
 @Transform(({ value }) => value?.trim())
 name?: string;
}
```

#### @nestjs/swagger (Swagger UI)

- **Type:** API documentation tool
- **License:** MIT
- **Purpose:** Auto-generate interactive API documentation
- **Documentation:** [https://docs.nestjs.com/openapi/introduction](https://docs.nestjs.com/openapi/introduction)
- **Key Features:**
 - Automatic OpenAPI/Swagger spec generation
 - Interactive API explorer (Swagger UI)
 - Type-safe decorators (`@ApiProperty`, `@ApiOperation`)
 - JWT authentication support in UI

**Example:**

```typescript
import {
 ApiTags,
 ApiOperation,
 ApiResponse,
 ApiBearerAuth,
} from "@nestjs/swagger";

@ApiTags("tickets")
@Controller("tickets")
@ApiBearerAuth()
export class TicketsController {
 @Post()
 @ApiOperation({ summary: "Create a new ticket" })
 @ApiResponse({ status: 201, description: "Ticket created successfully" })
 @ApiResponse({ status: 400, description: "Bad request" })
 async create(@Body() dto: CreateTicketDto) {
 return this.ticketsService.create(dto);
 }
}

// Access at: http://localhost:3000/api
```

**Schema Example:**

```prisma
model Ticket {
 id String @id @default(cuid())
 ticketNo String @unique
 title String @db.VarChar(255)
 description String? @db.Text
 priority TicketPriority @default(MEDIUM)
 status TicketStatus @default(OPEN)
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 requesterId String
 requester User @relation("TicketRequester", fields: [requesterId], references: [id])

 assigneeId String?
 assignee User? @relation("TicketAssignee", fields: [assigneeId], references: [id])

 comments Comment[]

 @@index([status, priority])
 @@index([requesterId])
 @@index([assigneeId])
 @@map("tickets")
}

enum TicketPriority {
 LOW
 MEDIUM
 HIGH
 URGENT
}

enum TicketStatus {
 OPEN
 IN_PROGRESS
 RESOLVED
 CLOSED
}
```

**Commands:**

```bash
# Generate Prisma Client
npm run prisma:generate

# Create migration
npm run prisma:migrate:dev

# Deploy to production
npm run prisma:migrate:deploy

# Reset database (dev only)
npm run prisma:migrate:reset

# Open Prisma Studio
npm run prisma:studio

# Seed database
npm run prisma:seed
```

---

### Frontend

#### Next.js 15.5.6

- **Type:** React framework
- **License:** MIT
- **Purpose:** Server-side rendering + Static generation
- **Documentation:** [https://nextjs.org/docs](https://nextjs.org/docs)
- **Key Features:**
 - App Router (file-based routing)
 - React Server Components
 - Automatic code splitting
 - Image optimization
 - API routes (if needed)
 - TypeScript support

**Project Structure:**

```
next-frontend/
 app/
 (auth)/
 login/
 register/
 (dashboard)/
 tickets/
 assets/
 knowledge-base/
 layout.tsx
 page.tsx
 components/
 ui/ # shadcn/ui components
 tickets/
 assets/
 layout/
 lib/
 api/ # API clients
 hooks/
 utils/
 validations/ # Zod schemas
 public/
```

#### React 19.2.0

- **Type:** UI library
- **License:** MIT
- **Purpose:** Component-based UI
- **Documentation:** [https://react.dev/](https://react.dev/)
- **Patterns:**
 - Functional components only
 - React Hooks (useState, useEffect, useCallback, useMemo)
 - Custom hooks for reusable logic
 - Server Components (async components)
 - Client Components ('use client' directive)

#### shadcn/ui

- **Type:** Component library
- **License:** MIT
- **Purpose:** Pre-built accessible components
- **Documentation:** [https://ui.shadcn.com/](https://ui.shadcn.com/)
- **Built on:**
 - Radix UI (headless components)
 - Tailwind CSS v4 (styling)
 - class-variance-authority (variants)

**Available Components:**

- Forms: Input, Select, Checkbox, Radio, Switch, Textarea
- Data Display: Table, Card, Badge, Avatar, Separator
- Feedback: Alert, Toast, Dialog, AlertDialog
- Navigation: Tabs, DropdownMenu, NavigationMenu
- Overlays: Sheet, Popover, Tooltip, HoverCard
- Layout: Accordion, Collapsible, ScrollArea

**Installation:**

```bash
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add table
npx shadcn@latest add dialog
```

#### Tailwind CSS v4

- **Type:** Utility-first CSS framework
- **License:** MIT
- **Purpose:** Rapid UI development
- **Documentation:** [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
- **Configuration:** `tailwind.config.js`
- **Theme:** Custom OrionOne brand colors

#### React Hook Form 7.x

- **Type:** Form management library
- **License:** MIT
- **Purpose:** Performant form handling
- **Documentation:** [https://react-hook-form.com/](https://react-hook-form.com/)
- **Key Features:**
 - Uncontrolled components (better performance)
 - Built-in validation
 - TypeScript support
 - Small bundle size (9KB)

**Example:**

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const ticketSchema = z.object({
 title: z.string().min(5).max(255),
 description: z.string().optional(),
 priority: z.enum(["LOW", "MEDIUM", "HIGH", "URGENT"]),
});

type TicketFormData = z.infer<typeof ticketSchema>;

export function TicketForm() {
 const form = useForm<TicketFormData>({
 resolver: zodResolver(ticketSchema),
 });

 const onSubmit = (data: TicketFormData) => {
 console.log(data);
 };

 return <form onSubmit={form.handleSubmit(onSubmit)}>...</form>;
}
```

#### Zod 4.x

- **Type:** Schema validation library
- **License:** MIT
- **Purpose:** TypeScript-first schema validation
- **Documentation:** [https://zod.dev/](https://zod.dev/)
- **Key Features:**
 - Type inference (no need to write types separately)
 - Composable schemas
 - Rich validation rules
 - Custom error messages
 - Transform and parse data

**Example:**

```typescript
import { z } from "zod";

// Define schema
const userSchema = z.object({
 email: z.string().email("Invalid email format"),
 password: z.string().min(8, "Password must be at least 8 characters"),
 role: z.enum(["ADMIN", "AGENT", "USER"]),
 age: z.number().min(18).max(100).optional(),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;

// Validate data
const result = userSchema.safeParse({
 email: "user@example.com",
 password: "SecurePass123",
 role: "AGENT",
});

if (result.success) {
 console.log(result.data); // Typed as User
} else {
 console.error(result.error.errors);
}
```

#### TanStack Query (React Query) 5.x

- **Type:** Server state management
- **License:** MIT
- **Purpose:** Data fetching, caching, and synchronization
- **Documentation:** [https://tanstack.com/query/latest](https://tanstack.com/query/latest)
- **Key Features:**
 - Automatic caching and refetching
 - Background updates
 - Optimistic updates
 - Infinite queries
 - Devtools integration
 - TypeScript support

**Example:**

- **Type:** Server state management
- **License:** MIT
- **Purpose:** Data fetching, caching, synchronization
- **Documentation:** [https://tanstack.com/query/latest](https://tanstack.com/query/latest)
- **Documentation:** [https://tanstack.com/query/latest](https://tanstack.com/query/latest)
- **Key Features:**
 - Automatic background refetching
 - Caching and cache invalidation
 - Parallel queries
 - Mutations with optimistic updates
 - Pagination and infinite scroll support

**Example:**

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

export function TicketsList() {
 const queryClient = useQueryClient();

 // Fetch tickets
 const { data: tickets, isLoading } = useQuery({
 queryKey: ["tickets"],
 queryFn: async () => {
 const res = await fetch("/api/tickets");
 return res.json();
 },
 });

 // Create ticket mutation
 const createMutation = useMutation({
 mutationFn: (newTicket) =>
 fetch("/api/tickets", {
 method: "POST",
 body: JSON.stringify(newTicket),
 }),
 onSuccess: () => {
 queryClient.invalidateQueries({ queryKey: ["tickets"] });
 },
 });

 return <div>...</div>;
}
```

#### Axios 1.13.x

- **Type:** HTTP client
- **License:** MIT
- **Purpose:** API communication
- **Documentation:** [https://axios-http.com/docs/intro](https://axios-http.com/docs/intro)
- **Key Features:**
 - Promise-based requests
 - Request/response interceptors
 - Automatic JSON transformation
 - Request cancellation
 - TypeScript support

**Example:**

```typescript
// lib/api/client.ts
import axios from "axios";

const apiClient = axios.create({
 baseURL: process.env.NEXT_PUBLIC_API_URL,
 headers: {
 "Content-Type": "application/json",
 },
});

// Request interceptor (add auth token)
apiClient.interceptors.request.use((config) => {
 const token = localStorage.getItem("access_token");
 if (token) {
 config.headers.Authorization = `Bearer ${token}`;
 }
 return config;
});

// Response interceptor (handle errors)
apiClient.interceptors.response.use(
 (response) => response,
 (error) => {
 if (error.response?.status === 401) {
 // Redirect to login
 window.location.href = "/login";
 }
 return Promise.reject(error);
 }
);

export default apiClient;
```

#### Zustand 5.x

- **Type:** Client state management
- **License:** MIT
- **Purpose:** Lightweight global state
- **Documentation:** [https://zustand-demo.pmnd.rs/](https://zustand-demo.pmnd.rs/)
- **Key Features:**
 - Simple API (no boilerplate)
 - TypeScript support
 - Devtools integration
 - Middleware support (persist, immer)

**Example:**

```typescript
// lib/stores/auth-store.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthState {
 user: User | null;
 token: string | null;
 setAuth: (user: User, token: string) => void;
 logout: () => void;
}

export const useAuthStore = create<AuthState>()(
 persist(
 (set) => ({
 user: null,
 token: null,
 setAuth: (user, token) => set({ user, token }),
 logout: () => set({ user: null, token: null }),
 }),
 {
 name: "auth-storage",
 }
 )
);
```

#### Lucide React

- **Type:** Icon library
- **License:** MIT
- **Purpose:** High-quality SVG icons
- **Documentation:** [https://lucide.dev/](https://lucide.dev/)
- **Features:**
 - 1000+ icons
 - Fully customizable (size, color, stroke)
 - Tree-shakeable
 - TypeScript support

**Example:**

```tsx
import { Check, X, AlertCircle, User, Settings } from "lucide-react";

export function StatusIcon({ status }: { status: string }) {
 if (status === "success") return <Check className="text-green-500" />;
 if (status === "error") return <X className="text-red-500" />;
 return <AlertCircle className="text-yellow-500" />;
}
```

#### clsx + tailwind-merge

- **Type:** Utility libraries
- **License:** MIT
- **Purpose:** Conditional CSS class management
- **Documentation:** [https://github.com/lukeed/clsx](https://github.com/lukeed/clsx) • [https://github.com/dcastil/tailwind-merge](https://github.com/dcastil/tailwind-merge)
- **clsx**: Conditional class names
- **tailwind-merge**: Merge Tailwind classes without conflicts

**Example:**

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
 return twMerge(clsx(inputs));
}

// Usage in components
<button
 className={cn(
 "px-4 py-2 rounded",
 isPrimary && "bg-blue-500 text-white",
 isDisabled && "opacity-50 cursor-not-allowed"
 )}
>
 Click me
</button>;
```

---

### Database

#### PostgreSQL 18.0

- **Type:** Relational database
- **License:** PostgreSQL License
- **Purpose:** Primary data store
- **Documentation:** [https://www.postgresql.org/docs/18/](https://www.postgresql.org/docs/18/)
- **Key Features:**
 - ACID compliance
 - JSON/JSONB support
 - Full-text search
 - Advanced indexing
 - Robust transactions
 - Row-level security (RLS)

**Production Optimization:**

```conf
# postgresql.conf
shared_buffers = 256MB # 25% of RAM
effective_cache_size = 1GB # 50-75% of RAM
work_mem = 16MB # Per operation
maintenance_work_mem = 128MB # For VACUUM, indexes
max_connections = 100
wal_buffers = 16MB
checkpoint_completion_target = 0.9
random_page_cost = 1.1 # For SSD
```

**Connection String:**

```bash
DATABASE_URL="postgresql://orionone:password@localhost:5432/orionone?schema=public"
```

---

### Cache & Search

#### Redis 8.2

- **Type:** In-memory data store
- **License:** BSD
- **Purpose:** Caching + session storage
- **Documentation:** [https://redis.io/docs/](https://redis.io/docs/)
- **Use Cases:**
 - API response caching
 - Session storage
 - Rate limiting
 - Real-time data (Pub/Sub)

**Configuration:**

```conf
# redis.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1 # Persist every 15min if 1 key changed
save 300 10 # Persist every 5min if 10 keys changed
requirepass your_secure_password
```

**Usage in Nest.js:**

```typescript
import { CACHE_MANAGER } from "@nestjs/cache-manager";
import { Inject } from "@nestjs/common";
import { Cache } from "cache-manager";

@Injectable()
export class TicketsService {
 constructor(@Inject(CACHE_MANAGER) private cache: Cache) {}

 async findAll() {
 const cached = await this.cache.get("tickets:all");
 if (cached) return cached;

 const tickets = await this.prisma.ticket.findMany();
 await this.cache.set("tickets:all", tickets, 300); // 5 minutes
 return tickets;
 }
}
```

#### Meilisearch 1.25

- **Type:** Full-text search engine
- **License:** MIT
- **Purpose:** Fast, typo-tolerant search
- **Documentation:** [https://www.meilisearch.com/docs](https://www.meilisearch.com/docs)
- **Use Cases:**
 - Knowledge Base article search
 - Ticket search
 - Asset search
 - User search

**Key Features:**

- Sub-50ms search responses
- Typo tolerance (1-2 character mistakes)
- Filters and facets
- Highlighting
- Language detection
- Sorting

**Integration:**

```typescript
import { MeiliSearch } from "meilisearch";

const client = new MeiliSearch({
 host: process.env.MEILISEARCH_URL,
 apiKey: process.env.MEILISEARCH_KEY,
});

// Index documents
await client
 .index("articles")
 .addDocuments([{ id: 1, title: "How to reset password", content: "..." }]);

// Search
const results = await client.index("articles").search("reset password", {
 limit: 10,
 attributesToHighlight: ["title", "content"],
});
```

---

### File Storage

#### AWS S3

- **Type:** Object storage
- **License:** Proprietary
- **Purpose:** File uploads (attachments, avatars, documents)
- **Documentation:** [https://docs.aws.amazon.com/s3/](https://docs.aws.amazon.com/s3/)
- **Features:**
 - Scalable storage
 - CDN integration (CloudFront)
 - Versioning
 - Lifecycle policies
 - Encryption at rest

**Usage:**

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({
 region: process.env.AWS_REGION,
 credentials: {
 accessKeyId: process.env.AWS_ACCESS_KEY_ID,
 secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
 },
});

async uploadFile(file: Buffer, key: string) {
 await s3Client.send(new PutObjectCommand({
 Bucket: process.env.AWS_S3_BUCKET,
 Key: key,
 Body: file,
 ContentType: 'image/jpeg',
 }));

 return `https://${process.env.AWS_S3_BUCKET}.s3.amazonaws.com/${key}`;
}
```

---

## Development Tools

### Testing

#### Jest 29.x

- **Type:** Testing framework
- **License:** MIT
- **Purpose:** Unit + integration tests
- **Documentation:** [https://jestjs.io/](https://jestjs.io/)
- **Used For:** Backend (Nest.js) + Frontend (Next.js)

**Backend Example:**

```typescript
describe('TicketsService', () => {
 let service: TicketsService;
 let prisma: PrismaService;

 beforeEach(async () => {
 const module = await Test.createTestingModule({
 providers: [TicketsService, PrismaService],
 }).compile();

 service = module.get(TicketsService);
 prisma = module.get(PrismaService);
 });

 it('should create a ticket', async () => {
 const dto = { title: 'Test ticket', priority: 'HIGH' };
 jest.spyOn(prisma.ticket, 'create').mockResolvedValue({...});

 const ticket = await service.create(dto);
 expect(ticket.title).toBe('Test ticket');
 });
});
```

#### Supertest 7.x

- **Type:** HTTP testing library
- **License:** MIT
- **Purpose:** E2E API testing
- **Documentation:** [https://github.com/ladjs/supertest](https://github.com/ladjs/supertest)
- **Used For:** Backend (Nest.js)

**Example:**

```typescript
describe("TicketsController (e2e)", () => {
 let app: INestApplication;

 beforeAll(async () => {
 const module = await Test.createTestingModule({
 imports: [AppModule],
 }).compile();

 app = module.createNestApplication();
 await app.init();
 });

 it("/tickets (POST)", () => {
 return request(app.getHttpServer())
 .post("/tickets")
 .send({ title: "New ticket", priority: "HIGH" })
 .expect(201)
 .expect((res) => {
 expect(res.body.ticketNo).toMatch(/TKT-\d{8}-\d{4}/);
 });
 });
});
```

#### React Testing Library

- **Type:** React component testing
- **License:** MIT
- **Purpose:** Frontend component tests
- **Documentation:** [https://testing-library.com/react](https://testing-library.com/react)
- **Philosophy:** Test user behavior, not implementation

**Example:**

```tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { TicketForm } from "./TicketForm";

describe("TicketForm", () => {
 it("should submit form with valid data", async () => {
 const onSubmit = jest.fn();
 render(<TicketForm onSubmit={onSubmit} />);

 fireEvent.change(screen.getByLabelText(/title/i), {
 target: { value: "Test ticket" },
 });
 fireEvent.click(screen.getByRole("button", { name: /submit/i }));

 await waitFor(() => {
 expect(onSubmit).toHaveBeenCalledWith({
 title: "Test ticket",
 priority: "MEDIUM",
 });
 });
 });
});
```

### Code Quality

#### ESLint

- **Type:** Linter
- **License:** MIT
- **Purpose:** Code quality + consistency
- **Documentation:** [https://eslint.org/](https://eslint.org/)
- **Config:** `.eslintrc.json`
- **Rules:** TypeScript recommended + Next.js + Nest.js

#### Prettier

- **Type:** Code formatter
- **License:** MIT
- **Purpose:** Consistent code formatting
- **Documentation:** [https://prettier.io/](https://prettier.io/)
- **Config:** `.prettierrc`

#### TypeScript 5.6.x

- **Type:** Typed superset of JavaScript
- **License:** Apache 2.0
- **Purpose:** Type safety
- **Documentation:** [https://www.typescriptlang.org/](https://www.typescriptlang.org/)
- **Config:** `tsconfig.json` (strict mode enabled)

**Strict Mode Settings:**

```json
{
 "compilerOptions": {
 "strict": true,
 "noImplicitAny": true,
 "strictNullChecks": true,
 "strictFunctionTypes": true,
 "noUnusedLocals": true,
 "noUnusedParameters": true
 }
}
```

---

## Infrastructure

### Docker

- **Type:** Containerization
- **License:** Apache 2.0
- **Purpose:** Local development + production deployment
- **Documentation:** [https://docs.docker.com/](https://docs.docker.com/)
- **Services:\*\***
 - PostgreSQL 18.0
 - Redis 8.2
 - Meilisearch 1.25

**docker-compose.yml:**

```yaml
services:
 postgres:
 image: postgres:18-alpine
 container_name: orionone_postgres
 environment:
 POSTGRES_USER: orionone
 POSTGRES_PASSWORD: password
 POSTGRES_DB: orionone
 ports:
 - "5432:5432"
 volumes:
 - postgres_data:/var/lib/postgresql/data

 redis:
 image: redis:8.2-alpine
 container_name: orionone_redis
 ports:
 - "6379:6379"
 volumes:
 - redis_data:/data

 meilisearch:
 image: getmeili/meilisearch:v1.25
 container_name: orionone_meilisearch
 environment:
 MEILI_MASTER_KEY: your_master_key
 ports:
 - "7700:7700"
 volumes:
 - meilisearch_data:/meili_data

volumes:
 postgres_data:
 redis_data:
 meilisearch_data:
```

### PM2

- **Type:** Process manager
- **License:** AGPL 3.0
- **Purpose:** Production Node.js process management
- **Documentation:** [https://pm2.keymetrics.io/](https://pm2.keymetrics.io/)
- **Features:**
 - Cluster mode
 - Auto-restart
 - Log management
 - Monitoring

**ecosystem.config.js:**

```javascript
module.exports = {
 apps: [
 {
 name: "orionone-backend",
 script: "dist/main.js",
 cwd: "/var/www/orionone/nest-backend",
 instances: 2,
 exec_mode: "cluster",
 max_memory_restart: "500M",
 env: {
 NODE_ENV: "production",
 PORT: 3000,
 },
 },
 {
 name: "orionone-frontend",
 script: "node_modules/.bin/next",
 args: "start",
 cwd: "/var/www/orionone/next-frontend",
 instances: 2,
 exec_mode: "cluster",
 max_memory_restart: "1G",
 env: {
 NODE_ENV: "production",
 PORT: 3001,
 },
 },
 ],
};
```

### Nginx

- **Type:** Web server + reverse proxy
- **License:** BSD-like
- **Purpose:** Load balancing + SSL termination
- **Documentation:** [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
- **Features:**
 - HTTP/2
 - Gzip compression
 - Static file caching
 - SSL/TLS termination

---

## Authentication & Authorization

### JWT (JSON Web Tokens)

- **Type:** Token-based authentication
- **Library:** `@nestjs/jwt`
- **Purpose:** Stateless authentication
- **Tokens:**
 - Access Token (15 minutes)
 - Refresh Token (7 days)

**Implementation:**

```typescript
import { JwtService } from '@nestjs/jwt';

async login(user: User) {
 const payload = { sub: user.id, email: user.email, roles: user.roles };

 return {
 access_token: this.jwtService.sign(payload, { expiresIn: '15m' }),
 refresh_token: this.jwtService.sign(payload, { expiresIn: '7d' }),
 };
}
```

### Bcrypt

- **Type:** Password hashing
- **Library:** `bcrypt` v6
- **Purpose:** Secure password storage
- **Documentation:** [https://github.com/kelektiv/node.bcrypt.js](https://github.com/kelektiv/node.bcrypt.js)
- **Rounds:** 12

**Usage:**

```typescript
import * as bcrypt from 'bcrypt';

async hashPassword(password: string): Promise<string> {
 return bcrypt.hash(password, 12);
}

async comparePassword(password: string, hash: string): Promise<boolean> {
 return bcrypt.compare(password, hash);
}
```

### CASL

- **Type:** Authorization library
- **License:** MIT
- **Purpose:** Role-Based Access Control (RBAC)
- **Documentation:** [https://casl.js.org/](https://casl.js.org/)
- **Abilities:** 32 permissions across 8 resources

**Example:**

```typescript
import { Ability, AbilityBuilder } from "@casl/ability";

function defineAbilitiesFor(user: User) {
 const { can, cannot, build } = new AbilityBuilder(Ability);

 if (user.role === "ADMIN") {
 can("manage", "all");
 } else if (user.role === "AGENT") {
 can("read", "Ticket");
 can("update", "Ticket");
 can("create", "Comment");
 } else if (user.role === "USER") {
 can("read", "Ticket", { requesterId: user.id });
 can("create", "Ticket");
 }

 return build();
}
```

---

## Monitoring & Observability

### Sentry

- **Type:** Error tracking
- **License:** Proprietary (Free tier available)
- **Purpose:** Production error monitoring
- **Documentation:** [https://docs.sentry.io/](https://docs.sentry.io/)
- **Integrations:** Backend + Frontend

**Backend:**

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
 dsn: process.env.SENTRY_DSN,
 environment: process.env.NODE_ENV,
 tracesSampleRate: 1.0,
});
```

**Frontend:**

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
 dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
 environment: process.env.NODE_ENV,
 tracesSampleRate: 0.1,
});
```

### Winston / Pino

- **Type:** Logging
- **License:** MIT
- **Purpose:** Structured logging
- **Documentation:** [https://github.com/winstonjs/winston](https://github.com/winstonjs/winston) • [https://getpino.io/](https://getpino.io/)
- **Levels:** error, warn, info, debug

**Usage:**

```typescript
import { Logger } from "@nestjs/common";

const logger = new Logger("TicketsService");

logger.log("Ticket created", { ticketId: ticket.id });
logger.error("Failed to create ticket", { error: error.message });
```

---

## Version History

| Date | Version | Major Changes |
| -------- | ------- | ------------------------------------ |
| Nov 2025 | 2.0.0 | Migration to Next.js 15 + Nest.js 11 |
| Oct 2024 | 1.0.0 | Initial Laravel 12 + Vue 3 version |

---

## External Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Nest.js Docs](https://docs.nestjs.com/)
- [Prisma Docs](https://www.prisma.io/docs)
- [shadcn/ui Docs](https://ui.shadcn.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/18/)
- [Redis Docs](https://redis.io/docs/)
- [Meilisearch Docs](https://www.meilisearch.com/docs)

---

**OrionOne ITSM Platform** • Built with by JMSS95
