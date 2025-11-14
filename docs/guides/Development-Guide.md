# Development Guide - OrionOne ITSM

**Stack:** Next.js 15.5.6 + Nest.js 11.1.8 + Prisma 6.4.0 + PostgreSQL 18.0
**Philosophy:** Feature-Driven Development + Test-Driven Development (TDD)
**MVP Scope:** 13 weeks (6 sprints), Tiptap Rich Text + Meilisearch + Basic SLA (24/7)
**Timeline:** Nov 1, 2025 - Jan 31, 2026
**Last Updated:** 14 November 2025

---

## Development Philosophy

### Feature-Driven Development (Vertical Slices)

Develop by **complete features** (vertical slice), not by layers (DB → API → Frontend).

#### Avoid (Waterfall by Layers)

```
1. Build ALL database tables
2. Build ALL backend/API endpoints
3. Build ALL frontend pages
4. Test EVERYTHING at the end
```

**Problems:**

-   Discover errors too late
-   Difficult to integrate everything
-   Nothing functional until the end
-   High risk of rework

#### Follow (Iterative by Feature)

```
Feature 1 (Authentication) → Feature 2 (Tickets) → Feature 3 (Comments) →
```

Each feature goes through **ALL layers** before moving to the next.

**Benefits:**

-   Early feedback and validation
-   Working software at each iteration
-   Easier to test and debug
-   Continuous integration
-   Reduced risk

---

## Development Cycle per Feature

### Phase 1: Planning (30 min)

**Checklist:**

-   [ ] Define feature scope
-   [ ] Write user story
-   [ ] Define acceptance criteria
-   [ ] Identify API endpoints needed
-   [ ] Design data model (Prisma schema)

**Example - Create Incident Feature (MVP Sprint 2)**

```markdown
**User Story:**
As an authenticated user, I want to create an incident with rich text description to report an issue clearly.

**Acceptance Criteria:**

-   [ ] Form with fields: title, description (**Tiptap rich text**), priority (P1-P4), category
-   [ ] Validation: title required (5-255 chars), description required (20+ chars)
-   [ ] **Rich text formatting (essential)**: bold, italic, lists, code blocks, links, headings
-   [ ] Markdown shortcuts (##, \*\*, --)
-   [ ] Character counter + placeholder text
-   [ ] Auto-generate incident number (INC-YYYYMMDD-NNNN)
-   [ ] Manual assignment to agent (dropdown)
-   [ ] Success toast + redirect to incident detail page
-   [ ] **EXCLUDED (Post-MVP):** Image paste (P2), tables, embeds, mentions

**API Endpoints:**

-   POST /api/incidents
-   GET /api/incidents/:id
-   GET /api/categories
-   GET /api/users?role=AGENT

**NOTE:** Meilisearch indexing moved to Sprint 4 (consolidated with Knowledge Base)
```

---

### Phase 2: Database Schema (30-45 min)

#### 2.1. Prisma Schema Design

**Location:** `nest-backend/prisma/schema.prisma`

```prisma
// Add to schema.prisma
model Incident {
 id String @id @default(cuid())
 incidentNumber String @unique @map("incident_number")
 title String @db.VarChar(255)
 description Json // Tiptap JSON format for rich text
 status IncidentStatus @default(NEW)
 priority IncidentPriority @default(P3)

 // Relationships
 requesterId String @map("requester_id")
 requester User @relation("IncidentRequester", fields: [requesterId], references: [id])

 assigneeId String? @map("assignee_id")
 assignee User? @relation("IncidentAssignee", fields: [assigneeId], references: [id])

 categoryId String @map("category_id")
 category Category @relation(fields: [categoryId], references: [id])

 // Timestamps
 createdAt DateTime @default(now()) @map("created_at")
 updatedAt DateTime @updatedAt @map("updated_at")
 closedAt DateTime? @map("closed_at")

 // Relations
 comments Comment[]
 attachments Attachment[]
 activities Activity[]

 @@map("incidents")
 @@index([status, priority])
 @@index([requesterId])
 @@index([assigneeId])
 @@index([categoryId])
 @@index([createdAt])
}

enum IncidentStatus {
 NEW
 IN_PROGRESS
 RESOLVED
 CLOSED
}

enum IncidentPriority {
 P1 // Critical - 4h SLA
 P2 // High - 8h SLA
 P3 // Medium - 24h SLA
 P4 // Low - 72h SLA
}
```

**Note:** Description stored as JSON (Tiptap format) for rich text. Meilisearch will index the plain text version.

#### 2.2. Create Migration

```bash
cd nest-backend

# Generate migration
npm run prisma:migrate:dev -- --name create_incidents_table

# Review migration SQL
cat prisma/migrations/TIMESTAMP_create_incidents_table/migration.sql
```

#### 2.3. Seed Data

**Location:** `nest-backend/prisma/seed.ts`

```typescript
import { PrismaClient, IncidentStatus, IncidentPriority } from "@prisma/client";

const prisma = new PrismaClient();

async function seedIncidents() {
    const users = await prisma.user.findMany({ take: 10 });
    const categories = await prisma.category.findMany();

    const incidents = [];
    for (let i = 1; i <= 50; i++) {
        const createdAt = new Date(2024, 10, (i % 28) + 1);

        // Simple plain text description for MVP (Tiptap JSON in production)
        const description = {
            type: "doc",
            content: [
                {
                    type: "paragraph",
                    content: [
                        {
                            type: "text",
                            text: `Detailed description of the incident number ${i}. This is a test incident for development purposes.`,
                        },
                    ],
                },
            ],
        };

        incidents.push({
            incidentNumber: `INC-${createdAt
                .toISOString()
                .slice(0, 10)
                .replace(/-/g, "")}-${String(i).padStart(4, "0")}`,
            title: `Issue with ${
                ["Network", "Hardware", "Software", "Access"][i % 4]
            }`,
            description, // Tiptap JSON format
            status: ["NEW", "IN_PROGRESS", "RESOLVED", "CLOSED"][
                i % 4
            ] as IncidentStatus,
            priority: ["P1", "P2", "P3", "P4"][i % 4] as IncidentPriority,
            requesterId: users[i % users.length].id,
            assigneeId: i % 3 === 0 ? users[i % users.length].id : null,
            categoryId: categories[i % categories.length].id,
            createdAt,
            updatedAt: createdAt,
        });
    }

    await prisma.incident.createMany({ data: incidents });
    console.log(` Seeded ${incidents.length} incidents`);
}

async function main() {
    await seedIncidents();
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
```

**Note:** Description uses Tiptap JSON format for rich text storage.

**Run Seeds:**

```bash
npm run prisma:seed
```

#### 2.4. Verify Database

```bash
# Check schema
npm run prisma:studio

# Or via PostgreSQL
docker exec orionone_postgres psql -U orionone -d orionone -c "SELECT COUNT(*) FROM incidents;"
```

---

### Phase 3: Backend Development (TDD) (2-3h)

#### 3.1. Write Tests First (RED)

**Location:** `nest-backend/src/tickets/tickets.controller.spec.ts`

```typescript
import { Test, TestingModule } from "@nestjs/testing";
import { IncidentsController } from "./incidents.controller";
import { IncidentsService } from "./incidents.service";
import { PrismaService } from "../prisma/prisma.service";
import { CreateIncidentDto } from "./dto/create-incident.dto";

describe("IncidentsController", () => {
    let controller: IncidentsController;
    let service: IncidentsService;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            controllers: [IncidentsController],
            providers: [IncidentsService, PrismaService],
        }).compile();

        controller = module.get<IncidentsController>(IncidentsController);
        service = module.get<IncidentsService>(IncidentsService);
    });

    describe("create", () => {
        it("should create an incident and return 201", async () => {
            const createIncidentDto: CreateIncidentDto = {
                title: "Laptop not working",
                description: {
                    type: "doc",
                    content: [
                        {
                            type: "paragraph",
                            content: [
                                {
                                    type: "text",
                                    text: "My laptop won't turn on after the update",
                                },
                            ],
                        },
                    ],
                },
                priority: "P2",
                categoryId: "cat-123",
            };

            const result = {
                id: "incident-123",
                incidentNumber: "INC-20241113-0001",
                ...createIncidentDto,
                status: "NEW",
                requesterId: "user-123",
                createdAt: new Date(),
                updatedAt: new Date(),
            };

            jest.spyOn(service, "create").mockResolvedValue(result as any);

            expect(
                await controller.create(createIncidentDto, {
                    user: { id: "user-123" },
                })
            ).toBe(result);
        });

        it("should throw BadRequestException for invalid data", async () => {
            const createIncidentDto: CreateIncidentDto = {
                title: "AB", // Too short (min 5 chars)
                description: { type: "doc", content: [] }, // Empty
                priority: "HIGH",
                categoryId: "cat-123",
            };

            await expect(
                controller.create(createTicketDto, { user: { id: "user-123" } })
            ).rejects.toThrow();
        });
    });
});
```

**Run Tests (Will Fail - Expected!):**

```bash
npm run test -- tickets.controller.spec.ts

# Output: RED (routes/service not implemented yet)
```

#### 3.2. Implement Code (GREEN)

**a) DTO (Data Transfer Object):**

**Location:** `nest-backend/src/tickets/dto/create-ticket.dto.ts`

```typescript
import {
    IsString,
    IsEnum,
    IsOptional,
    MinLength,
    MaxLength,
    IsUUID,
} from "class-validator";
import { ApiProperty } from "@nestjs/swagger";
import { TicketPriority } from "@prisma/client";

export class CreateTicketDto {
    @ApiProperty({
        example: "Laptop not working",
        minLength: 5,
        maxLength: 255,
    })
    @IsString()
    @MinLength(5, { message: "Title must be at least 5 characters" })
    @MaxLength(255, { message: "Title must not exceed 255 characters" })
    title: string;

    @ApiProperty({ example: "My laptop won't turn on", minLength: 20 })
    @IsString()
    @MinLength(20, { message: "Description must be at least 20 characters" })
    description: string;

    @ApiProperty({ enum: TicketPriority, example: "MEDIUM" })
    @IsEnum(TicketPriority)
    priority: TicketPriority;

    @ApiProperty({ example: "cat-hardware-uuid" })
    @IsUUID()
    categoryId: string;

    @ApiProperty({ example: "team-it-uuid", required: false })
    @IsOptional()
    @IsUUID()
    teamId?: string;
}
```

**b) Service (Business Logic):**

**Location:** `nest-backend/src/tickets/tickets.service.ts`

```typescript
import { Injectable, NotFoundException } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { CreateTicketDto } from "./dto/create-ticket.dto";
import { UpdateTicketDto } from "./dto/update-ticket.dto";

@Injectable()
export class TicketsService {
    constructor(private prisma: PrismaService) {}

    async create(createTicketDto: CreateTicketDto, userId: string) {
        // Generate ticket number
        const now = new Date();
        const dateStr = now.toISOString().slice(0, 10).replace(/-/g, "");
        const count = await this.prisma.ticket.count({
            where: {
                createdAt: {
                    gte: new Date(now.setHours(0, 0, 0, 0)),
                },
            },
        });
        const ticketNumber = `TKT-${dateStr}-${String(count + 1).padStart(
            4,
            "0"
        )}`;

        // Auto-assign to team if not specified
        let teamId = createTicketDto.teamId;
        if (!teamId) {
            const category = await this.prisma.category.findUnique({
                where: { id: createTicketDto.categoryId },
                include: { defaultTeam: true },
            });
            teamId = category?.defaultTeam?.id;
        }

        // Create ticket
        return this.prisma.ticket.create({
            data: {
                ...createTicketDto,
                ticketNumber,
                requesterId: userId,
                teamId,
                status: "OPEN",
            },
            include: {
                requester: { select: { id: true, name: true, email: true } },
                category: { select: { id: true, name: true } },
                team: { select: { id: true, name: true } },
            },
        });
    }

    async findAll(filters?: {
        status?: string;
        priority?: string;
        userId?: string;
    }) {
        return this.prisma.ticket.findMany({
            where: {
                ...(filters?.status && { status: filters.status as any }),
                ...(filters?.priority && { priority: filters.priority as any }),
                ...(filters?.userId && {
                    OR: [
                        { requesterId: filters.userId },
                        { assigneeId: filters.userId },
                    ],
                }),
            },
            include: {
                requester: { select: { id: true, name: true, email: true } },
                assignee: { select: { id: true, name: true, email: true } },
                category: { select: { id: true, name: true } },
                team: { select: { id: true, name: true } },
            },
            orderBy: { createdAt: "desc" },
        });
    }

    async findOne(id: string) {
        const ticket = await this.prisma.ticket.findUnique({
            where: { id },
            include: {
                requester: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                assignee: {
                    select: { id: true, name: true, email: true, avatar: true },
                },
                category: { select: { id: true, name: true, icon: true } },
                team: { select: { id: true, name: true } },
                comments: {
                    include: {
                        author: {
                            select: { id: true, name: true, avatar: true },
                        },
                    },
                    orderBy: { createdAt: "asc" },
                },
                attachments: true,
            },
        });

        if (!ticket) {
            throw new NotFoundException(`Ticket #${id} not found`);
        }

        return ticket;
    }

    async update(id: string, updateTicketDto: UpdateTicketDto) {
        await this.findOne(id); // Verify exists

        return this.prisma.ticket.update({
            where: { id },
            data: updateTicketDto,
            include: {
                requester: { select: { id: true, name: true, email: true } },
                assignee: { select: { id: true, name: true, email: true } },
                category: { select: { id: true, name: true } },
                team: { select: { id: true, name: true } },
            },
        });
    }

    async remove(id: string) {
        await this.findOne(id); // Verify exists
        return this.prisma.ticket.delete({ where: { id } });
    }
}
```

**c) Controller (HTTP Layer):**

**Location:** `nest-backend/src/tickets/tickets.controller.ts`

```typescript
import {
    Controller,
    Get,
    Post,
    Body,
    Patch,
    Param,
    Delete,
    UseGuards,
    Req,
    Query,
} from "@nestjs/common";
import { ApiTags, ApiOperation, ApiBearerAuth } from "@nestjs/swagger";
import { TicketsService } from "./tickets.service";
import { CreateTicketDto } from "./dto/create-ticket.dto";
import { UpdateTicketDto } from "./dto/update-ticket.dto";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";

@ApiTags("tickets")
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller("tickets")
export class TicketsController {
    constructor(private readonly ticketsService: TicketsService) {}

    @Post()
    @ApiOperation({ summary: "Create a new ticket" })
    create(@Body() createTicketDto: CreateTicketDto, @Req() req) {
        return this.ticketsService.create(createTicketDto, req.user.id);
    }

    @Get()
    @ApiOperation({ summary: "Get all tickets" })
    findAll(
        @Query()
        filters: {
            status?: string;
            priority?: string;
            userId?: string;
        }
    ) {
        return this.ticketsService.findAll(filters);
    }

    @Get(":id")
    @ApiOperation({ summary: "Get ticket by ID" })
    findOne(@Param("id") id: string) {
        return this.ticketsService.findOne(id);
    }

    @Patch(":id")
    @ApiOperation({ summary: "Update ticket" })
    update(@Param("id") id: string, @Body() updateTicketDto: UpdateTicketDto) {
        return this.ticketsService.update(id, updateTicketDto);
    }

    @Delete(":id")
    @ApiOperation({ summary: "Delete ticket" })
    remove(@Param("id") id: string) {
        return this.ticketsService.remove(id);
    }
}
```

**d) Module:**

**Location:** `nest-backend/src/tickets/tickets.module.ts`

```typescript
import { Module } from "@nestjs/common";
import { TicketsService } from "./tickets.service";
import { TicketsController } from "./tickets.controller";
import { PrismaModule } from "../prisma/prisma.module";

@Module({
    imports: [PrismaModule],
    controllers: [TicketsController],
    providers: [TicketsService],
    exports: [TicketsService],
})
export class TicketsModule {}
```

**Run Tests Again (Should Pass!):**

```bash
npm run test -- tickets.controller.spec.ts

# Output: GREEN
```

#### 3.3. Integration Testing

**Location:** `nest-backend/test/tickets.e2e-spec.ts`

```typescript
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication, ValidationPipe } from "@nestjs/common";
import * as request from "supertest";
import { AppModule } from "../src/app.module";
import { PrismaService } from "../src/prisma/prisma.service";

describe("Tickets (e2e)", () => {
    let app: INestApplication;
    let prisma: PrismaService;
    let authToken: string;

    beforeAll(async () => {
        const moduleFixture: TestingModule = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        app.useGlobalPipes(
            new ValidationPipe({ whitelist: true, transform: true })
        );
        await app.init();

        prisma = app.get<PrismaService>(PrismaService);

        // Login to get auth token
        const loginResponse = await request(app.getHttpServer())
            .post("/auth/login")
            .send({ email: "admin@orionone.com", password: "password123" });

        authToken = loginResponse.body.access_token;
    });

    afterAll(async () => {
        await prisma.$disconnect();
        await app.close();
    });

    describe("/tickets (POST)", () => {
        it("should create a new ticket", () => {
            return request(app.getHttpServer())
                .post("/tickets")
                .set("Authorization", `Bearer ${authToken}`)
                .send({
                    title: "Test ticket from E2E",
                    description:
                        "This is a test ticket created during E2E testing",
                    priority: "MEDIUM",
                    categoryId: "existing-category-id",
                })
                .expect(201)
                .expect((res) => {
                    expect(res.body).toHaveProperty("id");
                    expect(res.body).toHaveProperty("ticketNumber");
                    expect(res.body.title).toBe("Test ticket from E2E");
                });
        });

        it("should return 400 for invalid data", () => {
            return request(app.getHttpServer())
                .post("/tickets")
                .set("Authorization", `Bearer ${authToken}`)
                .send({
                    title: "ABC", // Too short
                    description: "Short",
                    priority: "INVALID",
                })
                .expect(400);
        });
    });
});
```

**Run E2E Tests:**

```bash
npm run test:e2e
```

#### 3.4. Code Quality Checks

```bash
# Linting
npm run lint

# Format code
npm run format

# Type checking
npm run build
```

---

### Phase 4: Frontend Development (1-2h)

#### 4.1. API Client Setup

**Location:** `next-frontend/lib/api/tickets.ts`

```typescript
import { apiClient } from "./client";
import { z } from "zod";

// Zod schemas for validation
export const ticketSchema = z.object({
    id: z.string(),
    ticketNumber: z.string(),
    title: z.string().min(5).max(255),
    description: z.string().min(20),
    status: z.enum([
        "OPEN",
        "IN_PROGRESS",
        "PENDING",
        "RESOLVED",
        "CLOSED",
        "CANCELLED",
    ]),
    priority: z.enum(["LOW", "MEDIUM", "HIGH", "URGENT"]),
    requesterId: z.string(),
    assigneeId: z.string().nullable(),
    categoryId: z.string(),
    teamId: z.string().nullable(),
    createdAt: z.string(),
    updatedAt: z.string(),
    closedAt: z.string().nullable(),
});

export const createTicketSchema = z.object({
    title: z.string().min(5, "Title must be at least 5 characters").max(255),
    description: z
        .string()
        .min(20, "Description must be at least 20 characters"),
    priority: z.enum(["LOW", "MEDIUM", "HIGH", "URGENT"]),
    categoryId: z.string().uuid("Invalid category"),
    teamId: z.string().uuid().optional(),
});

export type Ticket = z.infer<typeof ticketSchema>;
export type CreateTicketInput = z.infer<typeof createTicketSchema>;

// API functions
export const ticketsApi = {
    getAll: async (filters?: { status?: string; priority?: string }) => {
        const response = await apiClient.get<Ticket[]>("/tickets", {
            params: filters,
        });
        return response.data;
    },

    getById: async (id: string) => {
        const response = await apiClient.get<Ticket>(`/tickets/${id}`);
        return response.data;
    },

    create: async (data: CreateTicketInput) => {
        const response = await apiClient.post<Ticket>("/tickets", data);
        return response.data;
    },

    update: async (id: string, data: Partial<CreateTicketInput>) => {
        const response = await apiClient.patch<Ticket>(`/tickets/${id}`, data);
        return response.data;
    },

    delete: async (id: string) => {
        await apiClient.delete(`/tickets/${id}`);
    },
};
```

#### 4.2. Create Ticket Form Component

**Location:** `next-frontend/app/tickets/create/page.tsx`

```tsx
"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/components/ui/use-toast";
import {
    ticketsApi,
    createTicketSchema,
    type CreateTicketInput,
} from "@/lib/api/tickets";

export default function CreateTicketPage() {
    const router = useRouter();
    const { toast } = useToast();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<CreateTicketInput>({
        resolver: zodResolver(createTicketSchema),
        defaultValues: {
            title: "",
            description: "",
            priority: "MEDIUM",
            categoryId: "",
        },
    });

    const onSubmit = async (data: CreateTicketInput) => {
        try {
            setIsSubmitting(true);
            const ticket = await ticketsApi.create(data);

            toast({
                title: "Success",
                description: `Ticket ${ticket.ticketNumber} created successfully`,
            });

            router.push(`/tickets/${ticket.id}`);
        } catch (error: any) {
            toast({
                title: "Error",
                description:
                    error.response?.data?.message || "Failed to create ticket",
                variant: "destructive",
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="container max-w-2xl py-8">
            <h1 className="text-3xl font-bold mb-6">Create New Ticket</h1>

            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-6"
                >
                    <FormField
                        control={form.control}
                        name="title"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Title</FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Brief description of the issue"
                                        {...field}
                                    />
                                </FormControl>
                                <FormDescription>
                                    A clear, concise title (5-255 characters)
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="description"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Description</FormLabel>
                                <FormControl>
                                    <Textarea
                                        placeholder="Detailed description of the issue"
                                        className="min-h-[150px]"
                                        {...field}
                                    />
                                </FormControl>
                                <FormDescription>
                                    Provide detailed information (minimum 20
                                    characters)
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="priority"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Priority</FormLabel>
                                <Select
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                >
                                    <FormControl>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select priority" />
                                        </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                        <SelectItem value="LOW">Low</SelectItem>
                                        <SelectItem value="MEDIUM">
                                            Medium
                                        </SelectItem>
                                        <SelectItem value="HIGH">
                                            High
                                        </SelectItem>
                                        <SelectItem value="URGENT">
                                            Urgent
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="categoryId"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Category</FormLabel>
                                <Select
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                >
                                    <FormControl>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select category" />
                                        </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                        <SelectItem value="cat-hardware">
                                            Hardware
                                        </SelectItem>
                                        <SelectItem value="cat-software">
                                            Software
                                        </SelectItem>
                                        <SelectItem value="cat-network">
                                            Network
                                        </SelectItem>
                                        <SelectItem value="cat-access">
                                            Access
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <div className="flex gap-4">
                        <Button type="submit" disabled={isSubmitting}>
                            {isSubmitting ? "Creating..." : "Create Ticket"}
                        </Button>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => router.push("/tickets")}
                        >
                            Cancel
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
```

#### 4.3. Tickets List Page

**Location:** `next-frontend/app/tickets/page.tsx`

```tsx
import { Suspense } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { PlusCircle } from "lucide-react";
import { TicketsTable } from "@/components/tickets/tickets-table";
import { TicketsTableSkeleton } from "@/components/tickets/tickets-table-skeleton";

export default function TicketsPage() {
    return (
        <div className="container py-8">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-3xl font-bold">Tickets</h1>
                    <p className="text-muted-foreground mt-1">
                        Manage and track support tickets
                    </p>
                </div>
                <Button asChild>
                    <Link href="/tickets/create">
                        <PlusCircle className="mr-2 h-4 w-4" />
                        Create Ticket
                    </Link>
                </Button>
            </div>

            <Suspense fallback={<TicketsTableSkeleton />}>
                <TicketsTable />
            </Suspense>
        </div>
    );
}
```

---

### Phase 5: Testing & Quality (30 min)

#### 5.1. Backend Tests

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Coverage report
npm run test:cov

# Coverage threshold (CI/CD)
npm run test:cov -- --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

#### 5.2. Frontend Tests

**Location:** `next-frontend/__tests__/tickets/create.test.tsx`

```tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CreateTicketPage from "@/app/tickets/create/page";
import { ticketsApi } from "@/lib/api/tickets";

jest.mock("@/lib/api/tickets");

describe("Create Ticket Page", () => {
    it("renders the form", () => {
        render(<CreateTicketPage />);

        expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/priority/i)).toBeInTheDocument();
    });

    it("submits form with valid data", async () => {
        const user = userEvent.setup();
        const mockCreate = jest.spyOn(ticketsApi, "create").mockResolvedValue({
            id: "ticket-123",
            ticketNumber: "TKT-20251113-0001",
            title: "Test Ticket",
            description:
                "This is a test ticket description with enough characters",
            priority: "HIGH",
            status: "OPEN",
            categoryId: "cat-123",
        } as any);

        render(<CreateTicketPage />);

        await user.type(screen.getByLabelText(/title/i), "Test Ticket");
        await user.type(
            screen.getByLabelText(/description/i),
            "This is a test ticket description with enough characters"
        );
        await user.click(
            screen.getByRole("button", { name: /create ticket/i })
        );

        await waitFor(() => {
            expect(mockCreate).toHaveBeenCalled();
        });
    });

    it("shows validation errors for invalid data", async () => {
        const user = userEvent.setup();
        render(<CreateTicketPage />);

        await user.type(screen.getByLabelText(/title/i), "ABC"); // Too short
        await user.click(
            screen.getByRole("button", { name: /create ticket/i })
        );

        await waitFor(() => {
            expect(
                screen.getByText(/title must be at least 5 characters/i)
            ).toBeInTheDocument();
        });
    });
});
```

**Run Frontend Tests:**

```bash
npm run test
```

---

### Phase 6: Code Quality & Refactoring (30 min)

#### 6.1. Linting & Formatting

```bash
# Backend
cd nest-backend
npm run lint
npm run format

# Frontend
cd next-frontend
npm run lint
npm run format
```

#### 6.2. Type Checking

```bash
# Backend
npm run build

# Frontend
npm run type-check
```

#### 6.3. Code Review Checklist

-   [ ] No console.log() statements
-   [ ] No commented code
-   [ ] No magic numbers/strings (use constants)
-   [ ] Proper error handling
-   [ ] Input validation (DTO + Zod)
-   [ ] Proper TypeScript types (no `any`)
-   [ ] Tests cover happy path and edge cases
-   [ ] API documented with Swagger decorators
-   [ ] Responsive UI (mobile + desktop)
-   [ ] Accessibility (ARIA labels, keyboard navigation)

---

### Phase 7: Git Commit (15 min)

```bash
# Stage changes
git add nest-backend/prisma/schema.prisma
git add nest-backend/src/tickets/
git add next-frontend/app/tickets/
git add next-frontend/lib/api/tickets.ts

# Commit with conventional commit format
git commit -m "feat(tickets): implement create ticket feature

- Add Ticket model to Prisma schema
- Create TicketsModule with CRUD operations
- Add DTO validation with class-validator
- Implement unit tests and e2e tests
- Create ticket creation form with React Hook Form + Zod
- Add tickets list page with shadcn/ui table

Refs: #12"

# Push to remote
git push origin feat/tickets-create
```

---

## Weekly Development Routine

### Monday: New Feature Planning

```
09:00-10:00 Sprint planning
10:00-11:00 Feature 1 - Planning & Schema design
11:00-13:00 Feature 1 - Backend TDD (tests + implementation)
14:00-16:00 Feature 1 - Frontend implementation
16:00-17:00 Feature 1 - Testing & commit
```

### Tuesday-Thursday: Feature Development

```
09:00-13:00 Feature N - Full cycle (planning → backend → frontend)
14:00-16:00 Feature N - Testing & refactoring
16:00-17:00 Feature N - Code review & commit
```

### Friday: Quality & Integration

```
09:00-11:00 Integration testing
11:00-13:00 Bug fixes
14:00-15:00 Refactoring
15:00-16:00 Documentation update
16:00-17:00 Code review & sprint retrospective
```

---

## Feature Development Checklist

```markdown
### Feature: [Name]

**Planning:**

-   [ ] User story defined
-   [ ] Acceptance criteria documented
-   [ ] API endpoints designed
-   [ ] Prisma schema designed

**Database:**

-   [ ] Prisma schema updated
-   [ ] Migration created and reviewed
-   [ ] Seed data added
-   [ ] Database tested (Prisma Studio)

**Backend:**

-   [ ] DTOs created with validation decorators
-   [ ] Service implemented with business logic
-   [ ] Controller created with proper guards
-   [ ] Unit tests written and passing
-   [ ] E2E tests written and passing
-   [ ] Swagger documentation added
-   [ ] Error handling implemented
-   [ ] Code linted and formatted

**Frontend:**

-   [ ] API client functions created
-   [ ] Zod schemas for validation
-   [ ] Forms with React Hook Form
-   [ ] Pages/components created
-   [ ] shadcn/ui components used
-   [ ] Responsive design (mobile + desktop)
-   [ ] Loading states implemented
-   [ ] Error handling with toast notifications
-   [ ] Tests written and passing

**Quality:**

-   [ ] All tests passing (backend + frontend)
-   [ ] Code coverage >80%
-   [ ] Linting passing
-   [ ] Type checking passing
-   [ ] No console.log() or commented code
-   [ ] Accessibility checked (ARIA, keyboard)

**Git:**

-   [ ] Conventional commit message
-   [ ] Changes pushed to feature branch
-   [ ] Pull request created (if applicable)
```

---

## Testing Strategy

### Backend Testing Pyramid

```
 /\
 / \ E2E Tests (10%)
 /____\ - Full API workflows
 / \ Integration Tests (30%)
 /________\ - Service + Database
 / \ Unit Tests (60%)
 /____________\- Pure functions, DTOs
```

### Test Coverage Targets

| Layer           | Coverage Target | Required |
| --------------- | --------------- | -------- |
| **Services**    | 90-100%         | Yes      |
| **Controllers** | 80-90%          | Yes      |
| **DTOs**        | 100%            | Yes      |
| **Utilities**   | 90-100%         | Yes      |
| **Overall**     | >80%            | Yes      |

### Frontend Testing

```typescript
// Component tests
- Render tests (does it render?)
- Interaction tests (user actions)
- Form validation tests
- API integration tests (mocked)

// E2E tests (Playwright - optional)
- Critical user flows
- Authentication flow
- Ticket creation flow
- Dashboard interaction
```

---

## Code Quality Metrics

### Daily Checks

```bash
# Backend
cd nest-backend
npm run lint && npm run test:cov && npm run build

# Frontend
cd next-frontend
npm run lint && npm run test && npm run build
```

### Weekly Review

```bash
# Analyze bundle size
cd next-frontend
npm run build
npm run analyze

# Check for security vulnerabilities
npm audit

# Check for outdated dependencies
npm outdated
```

---

## Development Tools

### VS Code Extensions

**Required:**

-   ESLint
-   Prettier
-   Prisma
-   TypeScript Error Translator
-   GitLens

**Recommended:**

-   Tailwind CSS IntelliSense
-   REST Client (for API testing)
-   Thunder Client (alternative to Postman)
-   Error Lens
-   Auto Rename Tag

### Browser Extensions

-   React Developer Tools
-   Redux DevTools (if using Redux)
-   Lighthouse (performance audits)

---

## Best Practices

### DO

-   **Write tests first** (TDD approach)
-   **Use TypeScript strictly** (no `any` types)
-   **Validate all inputs** (DTOs + Zod)
-   **Handle errors gracefully** (try-catch + error messages)
-   **Use Prisma transactions** for multi-step operations
-   **Implement proper logging** (Winston/Pino)
-   **Use environment variables** for config
-   **Follow naming conventions** (PascalCase for classes, camelCase for functions)
-   **Write descriptive commit messages** (conventional commits)
-   **Keep functions small** (<50 lines)
-   **Use constants** for magic numbers/strings

### DON'T

-   **Don't use `any` type** (use proper types or `unknown`)
-   **Don't skip validation** (both backend and frontend)
-   **Don't hardcode values** (use env variables or constants)
-   **Don't ignore TypeScript errors** (fix them, don't suppress)
-   **Don't commit console.log()** (use proper logging)
-   **Don't commit commented code** (delete it, Git has history)
-   **Don't skip tests** (tests are documentation)
-   **Don't mix concerns** (keep controllers thin, logic in services)
-   **Don't expose sensitive data** (use DTOs to filter)
-   **Don't ignore security** (sanitize inputs, use guards)

---

## Helper Scripts

### Create Feature Script

**Location:** `scripts/create-feature.sh`

```bash
#!/bin/bash
# Quick scaffolding for new feature

FEATURE=$1

if [ -z "$FEATURE" ]; then
 echo "Usage: ./scripts/create-feature.sh FeatureName"
 exit 1
fi

FEATURE_LOWER=$(echo $FEATURE | tr '[:upper:]' '[:lower:]')

echo " Creating feature: $FEATURE"

# Backend
cd nest-backend
nest g resource $FEATURE_LOWER --no-spec
nest g service $FEATURE_LOWER
nest g controller $FEATURE_LOWER

echo " Backend scaffolding complete"

# Create test files
cat > src/$FEATURE_LOWER/$FEATURE_LOWER.service.spec.ts << EOF
import { Test, TestingModule } from '@nestjs/testing';
import { ${FEATURE}Service } from './${FEATURE_LOWER}.service';

describe('${FEATURE}Service', () => {
 let service: ${FEATURE}Service;

 beforeEach(async () => {
 const module: TestingModule = await Test.createTestingModule({
 providers: [${FEATURE}Service],
 }).compile();

 service = module.get<${FEATURE}Service>(${FEATURE}Service);
 });

 it('should be defined', () => {
 expect(service).toBeDefined();
 });
});
EOF

echo " Test files created"

# Frontend
cd ../next-frontend

mkdir -p app/$FEATURE_LOWER
mkdir -p components/$FEATURE_LOWER
mkdir -p lib/api

cat > app/$FEATURE_LOWER/page.tsx << EOF
export default function ${FEATURE}Page() {
 return (
 <div className="container py-8">
 <h1 className="text-3xl font-bold">${FEATURE}</h1>
 </div>
 );
}
EOF

cat > lib/api/$FEATURE_LOWER.ts << EOF
import { apiClient } from './client';

export const ${FEATURE_LOWER}Api = {
 getAll: async () => {
 const response = await apiClient.get('/$FEATURE_LOWER');
 return response.data;
 },
};
EOF

echo " Frontend scaffolding complete"

echo ""
echo " Next steps:"
echo "1. Update Prisma schema (nest-backend/prisma/schema.prisma)"
echo "2. Create migration: npm run prisma:migrate:dev"
echo "3. Write tests first (TDD)"
echo "4. Implement business logic"
echo "5. Create frontend components"

cd ..
```

**Usage:**

```bash
chmod +x scripts/create-feature.sh
./scripts/create-feature.sh Tickets
```

---

## Additional Resources

### Official Documentation

-   **Nest.js**: https://docs.nestjs.com/
-   **Next.js**: https://nextjs.org/docs
-   **Prisma**: https://www.prisma.io/docs
-   **shadcn/ui**: https://ui.shadcn.com/docs
-   **React Hook Form**: https://react-hook-form.com/
-   **Zod**: https://zod.dev/

### Testing Resources

-   **Jest**: https://jestjs.io/docs/getting-started
-   **Testing Library**: https://testing-library.com/docs/react-testing-library/intro/
-   **Supertest**: https://github.com/ladjs/supertest

### Best Practices

-   **TypeScript Deep Dive**: https://basarat.gitbook.io/typescript/
-   **Clean Code JavaScript**: https://github.com/ryanmcdermott/clean-code-javascript
-   **Node.js Best Practices**: https://github.com/goldbergyoni/nodebestpractices

---

**Last Updated:** 13 November 2025
**Maintained by:** OrionOne Development Team
**Stack:** Next.js 15.5.6 + Nest.js 11.1.8 + Prisma 6.4.0 + PostgreSQL 18.0
