# 🚀 Migração Next.js + Nest.js - PARTE 2: Backend Migration

**Deadline:** Fim de Janeiro 2025 (10 semanas)
**Foco:** Conversão completa do backend Laravel → Nest.js com máxima velocidade

---

## 📊 PRISMA SCHEMA - Conversão Automática das Migrations

### Strategy: Schema-First Development

**Laravel (atual):** 14 migrations PHP → Executar uma a uma
**Prisma (novo):** 1 schema único → Auto-migração em segundos

---

### Schema Completo Prisma

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
  previewFeatures = ["fullTextSearch", "postgresqlExtensions"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ==========================================
// AUTHENTICATION & AUTHORIZATION
// ==========================================

model User {
  id                String    @id @default(uuid())
  name              String
  email             String    @unique
  emailVerifiedAt   DateTime? @map("email_verified_at")
  password          String
  rememberToken     String?   @map("remember_token")
  avatar            String?
  isActive          Boolean   @default(true) @map("is_active")
  role              Role      @default(USER)
  createdAt         DateTime  @default(now()) @map("created_at")
  updatedAt         DateTime  @updatedAt @map("updated_at")
  deletedAt         DateTime? @map("deleted_at")

  // Relationships
  ticketsCreated    Ticket[]       @relation("TicketRequester")
  ticketsAssigned   Ticket[]       @relation("TicketAssignee")
  comments          Comment[]
  articles          Article[]
  teamMembers       TeamMember[]
  activityLogs      ActivityLog[]
  assets            Asset[]
  notifications     Notification[]

  @@index([email])
  @@index([role])
  @@index([isActive])
  @@map("users")
}

enum Role {
  ADMIN
  AGENT
  USER
}

model Permission {
  id          String   @id @default(uuid())
  name        String   @unique
  guardName   String   @map("guard_name")
  description String?
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  roles RoleHasPermission[]

  @@map("permissions")
}

model RoleHasPermission {
  id           String     @id @default(uuid())
  roleName     Role       @map("role_name")
  permissionId String     @map("permission_id")
  permission   Permission @relation(fields: [permissionId], references: [id], onDelete: Cascade)

  @@unique([roleName, permissionId])
  @@map("role_has_permissions")
}

// ==========================================
// TICKETS SYSTEM
// ==========================================

model Ticket {
  id                    String         @id @default(uuid())
  ticketNumber          String         @unique @map("ticket_number")
  title                 String
  description           String         @db.Text
  status                TicketStatus   @default(OPEN)
  priority              TicketPriority @default(MEDIUM)
  requesterId           String         @map("requester_id")
  assignedTo            String?        @map("assigned_to")
  teamId                String?        @map("team_id")
  categoryId            String?        @map("category_id")
  firstResponseAt       DateTime?      @map("first_response_at")
  firstResponseDeadline DateTime?      @map("first_response_deadline")
  resolutionDeadline    DateTime?      @map("resolution_deadline")
  resolvedAt            DateTime?      @map("resolved_at")
  closedAt              DateTime?      @map("closed_at")
  isEscalated           Boolean        @default(false) @map("is_escalated")
  customFields          Json?          @map("custom_fields")
  createdAt             DateTime       @default(now()) @map("created_at")
  updatedAt             DateTime       @updatedAt @map("updated_at")
  deletedAt             DateTime?      @map("deleted_at")

  // Relationships
  requester  User               @relation("TicketRequester", fields: [requesterId], references: [id])
  assignee   User?              @relation("TicketAssignee", fields: [assignedTo], references: [id])
  team       Team?              @relation(fields: [teamId], references: [id])
  category   Category?          @relation(fields: [categoryId], references: [id])
  comments   Comment[]
  attachments Media[]
  activities ActivityLog[]

  @@index([ticketNumber])
  @@index([status, priority])
  @@index([requesterId])
  @@index([assignedTo])
  @@index([teamId])
  @@index([createdAt])
  @@map("tickets")
}

enum TicketStatus {
  OPEN
  IN_PROGRESS
  ON_HOLD
  RESOLVED
  CLOSED
  CANCELLED
}

enum TicketPriority {
  LOW
  MEDIUM
  HIGH
  URGENT
}

model Category {
  id          String    @id @default(uuid())
  name        String
  slug        String    @unique
  description String?
  parentId    String?   @map("parent_id")
  order       Int       @default(0)
  isActive    Boolean   @default(true) @map("is_active")
  createdAt   DateTime  @default(now()) @map("created_at")
  updatedAt   DateTime  @updatedAt @map("updated_at")

  parent   Category?  @relation("CategoryHierarchy", fields: [parentId], references: [id])
  children Category[] @relation("CategoryHierarchy")
  tickets  Ticket[]
  articles Article[]

  @@index([slug])
  @@index([parentId])
  @@map("categories")
}

// ==========================================
// COLLABORATION
// ==========================================

model Comment {
  id         String    @id @default(uuid())
  ticketId   String    @map("ticket_id")
  userId     String    @map("user_id")
  content    String    @db.Text
  isInternal Boolean   @default(false) @map("is_internal")
  createdAt  DateTime  @default(now()) @map("created_at")
  updatedAt  DateTime  @updatedAt @map("updated_at")
  deletedAt  DateTime? @map("deleted_at")

  ticket      Ticket        @relation(fields: [ticketId], references: [id], onDelete: Cascade)
  user        User          @relation(fields: [userId], references: [id])
  attachments Media[]
  activities  ActivityLog[]

  @@index([ticketId])
  @@index([userId])
  @@index([createdAt])
  @@map("comments")
}

model Team {
  id          String   @id @default(uuid())
  name        String
  slug        String   @unique
  description String?
  email       String?
  isActive    Boolean  @default(true) @map("is_active")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  members TeamMember[]
  tickets Ticket[]

  @@index([slug])
  @@map("teams")
}

model TeamMember {
  id       String     @id @default(uuid())
  teamId   String     @map("team_id")
  userId   String     @map("user_id")
  role     TeamRole   @default(MEMBER)
  joinedAt DateTime   @default(now()) @map("joined_at")

  team Team @relation(fields: [teamId], references: [id], onDelete: Cascade)
  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([teamId, userId])
  @@map("team_members")
}

enum TeamRole {
  LEAD
  MEMBER
}

// ==========================================
// KNOWLEDGE BASE
// ==========================================

model Article {
  id          String    @id @default(uuid())
  title       String
  slug        String    @unique
  content     String    @db.Text
  excerpt     String?
  categoryId  String    @map("category_id")
  authorId    String    @map("author_id")
  isPublished Boolean   @default(false) @map("is_published")
  viewCount   Int       @default(0) @map("view_count")
  helpfulVotes Int      @default(0) @map("helpful_votes")
  notHelpfulVotes Int   @default(0) @map("not_helpful_votes")
  publishedAt DateTime? @map("published_at")
  createdAt   DateTime  @default(now()) @map("created_at")
  updatedAt   DateTime  @updatedAt @map("updated_at")
  deletedAt   DateTime? @map("deleted_at")

  category Category          @relation(fields: [categoryId], references: [id])
  author   User              @relation(fields: [authorId], references: [id])
  versions ArticleVersion[]

  @@index([slug])
  @@index([categoryId])
  @@index([authorId])
  @@index([isPublished])
  @@map("articles")
}

model ArticleVersion {
  id         String   @id @default(uuid())
  articleId  String   @map("article_id")
  title      String
  content    String   @db.Text
  version    Int
  createdAt  DateTime @default(now()) @map("created_at")

  article Article @relation(fields: [articleId], references: [id], onDelete: Cascade)

  @@index([articleId])
  @@map("article_versions")
}

// ==========================================
// ASSETS (CMDB)
// ==========================================

model Asset {
  id             String     @id @default(uuid())
  assetTag       String     @unique @map("asset_tag")
  name           String
  type           AssetType
  manufacturer   String?
  model          String?
  serialNumber   String?    @map("serial_number")
  purchaseDate   DateTime?  @map("purchase_date")
  purchaseCost   Decimal?   @map("purchase_cost") @db.Decimal(10, 2)
  warrantyExpiry DateTime?  @map("warranty_expiry")
  status         AssetStatus @default(AVAILABLE)
  assignedTo     String?    @map("assigned_to")
  location       String?
  notes          String?    @db.Text
  customFields   Json?      @map("custom_fields")
  createdAt      DateTime   @default(now()) @map("created_at")
  updatedAt      DateTime   @updatedAt @map("updated_at")
  deletedAt      DateTime?  @map("deleted_at")

  assignedUser User? @relation(fields: [assignedTo], references: [id])

  @@index([assetTag])
  @@index([type])
  @@index([status])
  @@index([assignedTo])
  @@map("assets")
}

enum AssetType {
  LAPTOP
  DESKTOP
  SERVER
  LICENSE
  MOBILE
  NETWORK
}

enum AssetStatus {
  AVAILABLE
  IN_USE
  MAINTENANCE
  RETIRED
}

// ==========================================
// FILE STORAGE
// ==========================================

model Media {
  id           String    @id @default(uuid())
  modelType    String    @map("model_type")
  modelId      String    @map("model_id")
  collection   String
  name         String
  fileName     String    @map("file_name")
  mimeType     String    @map("mime_type")
  disk         String    @default("public")
  size         Int
  customProperties Json? @map("custom_properties")
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")

  ticket   Ticket?  @relation(fields: [modelId], references: [id], map: "media_ticket")
  comment  Comment? @relation(fields: [modelId], references: [id], map: "media_comment")

  @@index([modelType, modelId])
  @@map("media")
}

// ==========================================
// ACTIVITY LOG (AUDIT)
// ==========================================

model ActivityLog {
  id             String    @id @default(uuid())
  logName        String?   @map("log_name")
  description    String
  subjectType    String?   @map("subject_type")
  subjectId      String?   @map("subject_id")
  causerId       String?   @map("causer_id")
  properties     Json?
  event          String?
  batchUuid      String?   @map("batch_uuid")
  createdAt      DateTime  @default(now()) @map("created_at")

  causer  User?    @relation(fields: [causerId], references: [id])
  ticket  Ticket?  @relation(fields: [subjectId], references: [id], map: "activity_ticket")
  comment Comment? @relation(fields: [subjectId], references: [id], map: "activity_comment")

  @@index([logName])
  @@index([subjectType, subjectId])
  @@index([causerId])
  @@index([createdAt])
  @@map("activity_log")
}

// ==========================================
// NOTIFICATIONS
// ==========================================

model Notification {
  id        String    @id @default(uuid())
  userId    String    @map("user_id")
  type      String
  title     String
  message   String    @db.Text
  data      Json?
  readAt    DateTime? @map("read_at")
  createdAt DateTime  @default(now()) @map("created_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([readAt])
  @@map("notifications")
}

// ==========================================
// CACHE & SESSIONS
// ==========================================

model CacheEntry {
  key        String   @id
  value      String   @db.Text
  expiration Int

  @@map("cache")
}

model CacheLock {
  key        String   @id
  owner      String
  expiration Int

  @@map("cache_locks")
}

model Job {
  id           BigInt   @id @default(autoincrement())
  queue        String
  payload      String   @db.Text
  attempts     Int      @default(0)
  reservedAt   Int?     @map("reserved_at")
  availableAt  Int      @map("available_at")
  createdAt    Int      @map("created_at")

  @@index([queue])
  @@map("jobs")
}

model FailedJob {
  id         BigInt   @id @default(autoincrement())
  uuid       String   @unique
  connection String   @db.Text
  queue      String   @db.Text
  payload    String   @db.Text
  exception  String   @db.Text
  failedAt   DateTime @default(now()) @map("failed_at")

  @@map("failed_jobs")
}
```

---

## 🏗️ NEST.JS PROJECT STRUCTURE

### Arquitetura Modular (Gerada pelo CLI)

```bash
nest-backend/
├── src/
│   ├── main.ts                    # Bootstrap
│   ├── app.module.ts              # Root module
│   │
│   ├── auth/                      # Authentication module
│   │   ├── auth.module.ts
│   │   ├── auth.service.ts
│   │   ├── auth.controller.ts
│   │   ├── strategies/
│   │   │   ├── jwt.strategy.ts
│   │   │   └── local.strategy.ts
│   │   ├── guards/
│   │   │   ├── jwt-auth.guard.ts
│   │   │   └── roles.guard.ts
│   │   └── dto/
│   │       ├── login.dto.ts
│   │       └── register.dto.ts
│   │
│   ├── users/                     # Users module
│   │   ├── users.module.ts
│   │   ├── users.service.ts
│   │   ├── users.controller.ts
│   │   └── dto/
│   │       ├── create-user.dto.ts
│   │       └── update-profile.dto.ts
│   │
│   ├── tickets/                   # Tickets module
│   │   ├── tickets.module.ts
│   │   ├── tickets.service.ts
│   │   ├── tickets.controller.ts
│   │   └── dto/
│   │       ├── create-ticket.dto.ts
│   │       ├── update-ticket.dto.ts
│   │       └── filter-ticket.dto.ts
│   │
│   ├── comments/                  # Comments module
│   │   ├── comments.module.ts
│   │   ├── comments.service.ts
│   │   ├── comments.controller.ts
│   │   └── dto/
│   │       └── create-comment.dto.ts
│   │
│   ├── teams/                     # Teams module
│   │   ├── teams.module.ts
│   │   ├── teams.service.ts
│   │   └── teams.controller.ts
│   │
│   ├── articles/                  # Knowledge Base module
│   │   ├── articles.module.ts
│   │   ├── articles.service.ts
│   │   └── articles.controller.ts
│   │
│   ├── assets/                    # Assets (CMDB) module
│   │   ├── assets.module.ts
│   │   ├── assets.service.ts
│   │   └── assets.controller.ts
│   │
│   ├── upload/                    # File upload module
│   │   ├── upload.module.ts
│   │   ├── upload.service.ts
│   │   └── upload.controller.ts
│   │
│   ├── search/                    # Meilisearch module
│   │   ├── search.module.ts
│   │   └── search.service.ts
│   │
│   ├── notifications/             # Notifications module
│   │   ├── notifications.module.ts
│   │   ├── notifications.service.ts
│   │   └── notifications.gateway.ts  # WebSocket
│   │
│   ├── excel/                     # Excel export module
│   │   ├── excel.module.ts
│   │   └── excel.service.ts
│   │
│   ├── abilities/                 # CASL permissions
│   │   ├── abilities.module.ts
│   │   ├── ability.factory.ts
│   │   └── decorators/
│   │       └── check-ability.decorator.ts
│   │
│   ├── prisma/                    # Prisma service
│   │   ├── prisma.module.ts
│   │   └── prisma.service.ts
│   │
│   ├── queue/                     # Bull queues
│   │   ├── queue.module.ts
│   │   └── processors/
│   │       ├── email.processor.ts
│   │       └── notifications.processor.ts
│   │
│   └── common/                    # Shared utilities
│       ├── decorators/
│       │   └── user.decorator.ts
│       ├── filters/
│       │   └── http-exception.filter.ts
│       ├── interceptors/
│       │   └── logging.interceptor.ts
│       └── pipes/
│           └── validation.pipe.ts
│
├── prisma/
│   ├── schema.prisma              # Database schema
│   ├── seed.ts                    # Seed data
│   └── migrations/                # Auto-generated
│
├── test/
│   ├── app.e2e-spec.ts
│   └── jest-e2e.json
│
├── .env
├── .env.example
├── nest-cli.json
├── package.json
├── tsconfig.json
└── docker-compose.yml
```

---

## 🚀 CÓDIGO-BASE ESSENCIAL (Copy-Paste Ready)

### 1. Prisma Service (Singleton)

```typescript
// src/prisma/prisma.service.ts
import { Injectable, OnModuleInit, OnModuleDestroy } from "@nestjs/common";
import { PrismaClient } from "@prisma/client";

@Injectable()
export class PrismaService
    extends PrismaClient
    implements OnModuleInit, OnModuleDestroy
{
    async onModuleInit() {
        await this.$connect();
    }

    async onModuleDestroy() {
        await this.$disconnect();
    }
}

// src/prisma/prisma.module.ts
import { Global, Module } from "@nestjs/common";
import { PrismaService } from "./prisma.service";

@Global()
@Module({
    providers: [PrismaService],
    exports: [PrismaService],
})
export class PrismaModule {}
```

---

### 2. Auth Module (JWT Complete)

```typescript
// src/auth/jwt.strategy.ts
import { Injectable, UnauthorizedException } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from "passport-jwt";
import { PrismaService } from "../prisma/prisma.service";

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
    constructor(private prisma: PrismaService) {
        super({
            jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
            ignoreExpiration: false,
            secretOrKey: process.env.JWT_SECRET,
        });
    }

    async validate(payload: { sub: string; email: string; role: string }) {
        const user = await this.prisma.user.findUnique({
            where: { id: payload.sub },
            select: {
                id: true,
                name: true,
                email: true,
                avatar: true,
                role: true,
                isActive: true,
            },
        });

        if (!user || !user.isActive) {
            throw new UnauthorizedException("Invalid token");
        }

        return user;
    }
}

// src/auth/auth.service.ts
import { Injectable, UnauthorizedException } from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import { PrismaService } from "../prisma/prisma.service";
import * as bcrypt from "bcrypt";

@Injectable()
export class AuthService {
    constructor(
        private prisma: PrismaService,
        private jwtService: JwtService
    ) {}

    async login(email: string, password: string) {
        const user = await this.prisma.user.findUnique({ where: { email } });

        if (!user || !(await bcrypt.compare(password, user.password))) {
            throw new UnauthorizedException("Invalid credentials");
        }

        const payload = { sub: user.id, email: user.email, role: user.role };

        return {
            access_token: this.jwtService.sign(payload),
            user: {
                id: user.id,
                name: user.name,
                email: user.email,
                avatar: user.avatar,
                role: user.role,
            },
        };
    }

    async register(data: { name: string; email: string; password: string }) {
        const hashedPassword = await bcrypt.hash(data.password, 10);

        const user = await this.prisma.user.create({
            data: {
                ...data,
                password: hashedPassword,
            },
            select: {
                id: true,
                name: true,
                email: true,
                role: true,
            },
        });

        return user;
    }
}

// src/auth/auth.controller.ts
import { Controller, Post, Body, HttpCode } from "@nestjs/common";
import { ApiTags, ApiOperation } from "@nestjs/swagger";
import { AuthService } from "./auth.service";
import { LoginDto, RegisterDto } from "./dto";

@ApiTags("auth")
@Controller("auth")
export class AuthController {
    constructor(private authService: AuthService) {}

    @Post("login")
    @HttpCode(200)
    @ApiOperation({ summary: "User login" })
    async login(@Body() dto: LoginDto) {
        return this.authService.login(dto.email, dto.password);
    }

    @Post("register")
    @ApiOperation({ summary: "User registration" })
    async register(@Body() dto: RegisterDto) {
        return this.authService.register(dto);
    }
}
```

---

### 3. Tickets Service (CRUD Completo)

```typescript
// src/tickets/tickets.service.ts
import {
    Injectable,
    NotFoundException,
    ForbiddenException,
} from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { CreateTicketDto, UpdateTicketDto, FilterTicketDto } from "./dto";
import { User, TicketStatus, Prisma } from "@prisma/client";

@Injectable()
export class TicketsService {
    constructor(private prisma: PrismaService) {}

    async create(dto: CreateTicketDto, user: User) {
        // Generate ticket number: TKT-20251113-0001
        const date = new Date().toISOString().split("T")[0].replace(/-/g, "");
        const count = await this.prisma.ticket.count({
            where: {
                ticketNumber: { startsWith: `TKT-${date}` },
            },
        });
        const ticketNumber = `TKT-${date}-${String(count + 1).padStart(
            4,
            "0"
        )}`;

        // Calculate SLA deadlines based on priority
        const firstResponseDeadline = this.calculateSLA(
            dto.priority,
            "response"
        );
        const resolutionDeadline = this.calculateSLA(
            dto.priority,
            "resolution"
        );

        const ticket = await this.prisma.ticket.create({
            data: {
                ticketNumber,
                title: dto.title,
                description: dto.description,
                priority: dto.priority,
                status: TicketStatus.OPEN,
                requesterId: user.id,
                categoryId: dto.categoryId,
                firstResponseDeadline,
                resolutionDeadline,
            },
            include: {
                requester: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                assignee: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                category: true,
            },
        });

        // Log activity
        await this.prisma.activityLog.create({
            data: {
                logName: "ticket",
                description: "Ticket created",
                subjectType: "Ticket",
                subjectId: ticket.id,
                causerId: user.id,
                event: "created",
                properties: { ticketNumber, title: dto.title },
            },
        });

        return ticket;
    }

    async findAll(filters: FilterTicketDto, user: User) {
        const where: Prisma.TicketWhereInput = {};

        // Apply filters
        if (filters.status) where.status = filters.status;
        if (filters.priority) where.priority = filters.priority;
        if (filters.assignedTo) where.assignedTo = filters.assignedTo;
        if (filters.search) {
            where.OR = [
                {
                    ticketNumber: {
                        contains: filters.search,
                        mode: "insensitive",
                    },
                },
                { title: { contains: filters.search, mode: "insensitive" } },
            ];
        }

        // Role-based filtering
        if (user.role === "USER") {
            where.requesterId = user.id;
        } else if (user.role === "AGENT" && !filters.all) {
            where.OR = [
                { assignedTo: user.id },
                { teamId: { in: await this.getUserTeamIds(user.id) } },
            ];
        }

        const [tickets, total] = await Promise.all([
            this.prisma.ticket.findMany({
                where,
                include: {
                    requester: {
                        select: {
                            id: true,
                            name: true,
                            email: true,
                            avatar: true,
                        },
                    },
                    assignee: {
                        select: {
                            id: true,
                            name: true,
                            email: true,
                            avatar: true,
                        },
                    },
                    category: true,
                    _count: { select: { comments: true } },
                },
                orderBy: { createdAt: "desc" },
                skip: (filters.page - 1) * filters.limit,
                take: filters.limit,
            }),
            this.prisma.ticket.count({ where }),
        ]);

        return {
            data: tickets,
            meta: {
                total,
                page: filters.page,
                limit: filters.limit,
                totalPages: Math.ceil(total / filters.limit),
            },
        };
    }

    async findOne(id: string, user: User) {
        const ticket = await this.prisma.ticket.findUnique({
            where: { id },
            include: {
                requester: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                assignee: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                team: true,
                category: true,
                comments: {
                    include: {
                        user: {
                            select: { id: true, name: true, avatar: true },
                        },
                    },
                    orderBy: { createdAt: "asc" },
                },
                attachments: true,
            },
        });

        if (!ticket) {
            throw new NotFoundException("Ticket not found");
        }

        // Check permissions
        if (user.role === "USER" && ticket.requesterId !== user.id) {
            throw new ForbiddenException("Access denied");
        }

        return ticket;
    }

    async update(id: string, dto: UpdateTicketDto, user: User) {
        const ticket = await this.findOne(id, user);

        const updated = await this.prisma.ticket.update({
            where: { id },
            data: {
                ...dto,
                ...(dto.status === TicketStatus.RESOLVED && !ticket.resolvedAt
                    ? { resolvedAt: new Date() }
                    : {}),
                ...(dto.status === TicketStatus.CLOSED && !ticket.closedAt
                    ? { closedAt: new Date() }
                    : {}),
            },
            include: {
                requester: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                assignee: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
            },
        });

        // Log activity
        await this.prisma.activityLog.create({
            data: {
                logName: "ticket",
                description: "Ticket updated",
                subjectType: "Ticket",
                subjectId: ticket.id,
                causerId: user.id,
                event: "updated",
                properties: { changes: dto },
            },
        });

        return updated;
    }

    async assign(id: string, assigneeId: string, user: User) {
        const ticket = await this.findOne(id, user);

        const updated = await this.prisma.ticket.update({
            where: { id },
            data: {
                assignedTo: assigneeId,
                ...(ticket.firstResponseAt
                    ? {}
                    : { firstResponseAt: new Date() }),
            },
            include: {
                assignee: { select: { id: true, name: true, email: true } },
            },
        });

        // Log activity
        await this.prisma.activityLog.create({
            data: {
                logName: "ticket",
                description: "Ticket assigned",
                subjectType: "Ticket",
                subjectId: ticket.id,
                causerId: user.id,
                event: "assigned",
                properties: { assigneeId },
            },
        });

        return updated;
    }

    private calculateSLA(
        priority: string,
        type: "response" | "resolution"
    ): Date {
        const hours = {
            URGENT: { response: 1, resolution: 4 },
            HIGH: { response: 4, resolution: 24 },
            MEDIUM: { response: 8, resolution: 72 },
            LOW: { response: 24, resolution: 168 },
        };

        const deadline = new Date();
        deadline.setHours(deadline.getHours() + hours[priority][type]);
        return deadline;
    }

    private async getUserTeamIds(userId: string): Promise<string[]> {
        const teams = await this.prisma.teamMember.findMany({
            where: { userId },
            select: { teamId: true },
        });
        return teams.map((t) => t.teamId);
    }
}

// src/tickets/tickets.controller.ts
import {
    Controller,
    Get,
    Post,
    Patch,
    Param,
    Body,
    Query,
    UseGuards,
} from "@nestjs/common";
import { ApiTags, ApiOperation, ApiBearerAuth } from "@nestjs/swagger";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";
import { User as UserDecorator } from "../common/decorators/user.decorator";
import { TicketsService } from "./tickets.service";
import { CreateTicketDto, UpdateTicketDto, FilterTicketDto } from "./dto";
import { User } from "@prisma/client";

@ApiTags("tickets")
@Controller("tickets")
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class TicketsController {
    constructor(private ticketsService: TicketsService) {}

    @Post()
    @ApiOperation({ summary: "Create new ticket" })
    create(@Body() dto: CreateTicketDto, @UserDecorator() user: User) {
        return this.ticketsService.create(dto, user);
    }

    @Get()
    @ApiOperation({ summary: "List tickets with filters" })
    findAll(@Query() filters: FilterTicketDto, @UserDecorator() user: User) {
        return this.ticketsService.findAll(filters, user);
    }

    @Get(":id")
    @ApiOperation({ summary: "Get ticket details" })
    findOne(@Param("id") id: string, @UserDecorator() user: User) {
        return this.ticketsService.findOne(id, user);
    }

    @Patch(":id")
    @ApiOperation({ summary: "Update ticket" })
    update(
        @Param("id") id: string,
        @Body() dto: UpdateTicketDto,
        @UserDecorator() user: User
    ) {
        return this.ticketsService.update(id, dto, user);
    }

    @Post(":id/assign")
    @ApiOperation({ summary: "Assign ticket to agent" })
    assign(
        @Param("id") id: string,
        @Body("assigneeId") assigneeId: string,
        @UserDecorator() user: User
    ) {
        return this.ticketsService.assign(id, assigneeId, user);
    }
}
```

---

### 4. Upload Service (Avatar + Attachments)

```typescript
// src/upload/upload.service.ts
import { Injectable } from "@nestjs/common";
import { randomUUID } from "crypto";
import * as sharp from "sharp";
import * as path from "path";
import * as fs from "fs/promises";
import { PrismaService } from "../prisma/prisma.service";

@Injectable()
export class UploadService {
    constructor(private prisma: PrismaService) {}

    async processAvatar(file: Express.Multer.File): Promise<string> {
        const filename = `${randomUUID()}.webp`;
        const uploadsDir = path.join(process.cwd(), "uploads", "avatars");
        await fs.mkdir(uploadsDir, { recursive: true });

        const outputPath = path.join(uploadsDir, filename);

        await sharp(file.buffer)
            .resize(300, 300, { fit: "cover" })
            .webp({ quality: 80 })
            .toFile(outputPath);

        return `/uploads/avatars/${filename}`;
    }

    async processAttachment(
        file: Express.Multer.File,
        modelType: string,
        modelId: string,
        collection: string
    ) {
        const filename = `${randomUUID()}-${file.originalname}`;
        const uploadsDir = path.join(process.cwd(), "uploads", collection);
        await fs.mkdir(uploadsDir, { recursive: true });

        const filePath = path.join(uploadsDir, filename);
        await fs.writeFile(filePath, file.buffer);

        const media = await this.prisma.media.create({
            data: {
                modelType,
                modelId,
                collection,
                name: file.originalname,
                fileName: filename,
                mimeType: file.mimetype,
                size: file.size,
            },
        });

        return media;
    }

    async deleteFile(filePath: string) {
        try {
            const fullPath = path.join(process.cwd(), filePath);
            await fs.unlink(fullPath);
        } catch (error) {
            console.error("Failed to delete file:", error);
        }
    }
}
```

---

## 📦 RESUMO BACKEND

**Arquivos a criar:** ~50 ficheiros TypeScript
**Linhas de código:** ~5000 (vs 8000 em Laravel)
**Redução:** 37% menos código devido a:

-   Decorators automáticos
-   Prisma type-safety
-   CLI code generation

**Próxima parte:** Frontend Next.js 15

---

**Continua em:** `MIGRATION-PART-3-FRONTEND.md`
