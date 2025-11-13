# 🚀 Migração Next.js + Nest.js - PARTE 1: Setup & Infraestrutura

**Deadline:** Fim de Janeiro 2025 (10 semanas)
**Data:** 13 Novembro 2025
**Estado Atual:** Laravel 18% completo → Migrar para Next.js 15 + Nest.js 10

---

## 📊 ANÁLISE COMPLETA DO STACK ATUAL

### Backend Laravel 12 - Packages Instalados

#### ✅ Packages de Produção (17 total)

```json
{
    "php": "^8.2",
    "laravel/framework": "^12.0",

    // Auth & Security
    "laravel/sanctum": "^4.0", // JWT tokens
    "spatie/laravel-permission": "^6.23", // RBAC (roles/permissions)

    // Database & Search
    "laravel/scout": "^10.21", // Search abstraction
    "meilisearch/meilisearch-php": "^1.16", // Full-text search

    // File Management
    "intervention/image": "^3.11", // Image processing
    "spatie/laravel-medialibrary": "^11.17", // File uploads

    // Data & API
    "spatie/laravel-data": "^4.18", // DTOs
    "spatie/laravel-query-builder": "^6.3", // API filters
    "spatie/laravel-activitylog": "^4.10", // Audit logs
    "maatwebsite/excel": "^1.1", // Excel import/export

    // Architecture Patterns
    "lorisleiva/laravel-actions": "^2.9", // Action pattern

    // Frontend Integration
    "inertiajs/inertia-laravel": "^2.0", // SSR bridge
    "tightenco/ziggy": "^2.0", // Route helper

    // Monitoring
    "laravel/pulse": "^1.4", // Performance monitoring
    "laravel/tinker": "^2.10.1" // REPL
}
```

#### 🛠️ Dev Dependencies (13 total)

```json
{
    "laravel/breeze": "^2.3", // Auth scaffolding
    "laravel/telescope": "^5.15", // Debug dashboard
    "laravel/pail": "^1.2.2", // Log viewer
    "laravel/sail": "^1.41", // Docker wrapper
    "laravel/pint": "^1.24", // Code formatter

    // Testing
    "pestphp/pest": "^3.8", // Test framework
    "pestphp/pest-plugin-laravel": "^3.2",
    "phpunit/phpunit": "^11.5.3",
    "mockery/mockery": "^1.6",
    "fakerphp/faker": "^1.23",

    // Code Quality
    "larastan/larastan": "^3.8", // PHPStan (static analysis)
    "barryvdh/laravel-debugbar": "^3.16", // Debug bar
    "barryvdh/laravel-ide-helper": "^3.6", // IDE autocomplete

    // Documentation
    "knuckleswtf/scribe": "^5.5" // API docs generator
}
```

---

### Frontend Vue 3 - Packages Instalados

#### ✅ Production Dependencies (13 total)

```json
{
    // Core
    "vue": "^3.4.0",
    "@inertiajs/vue3": "^2.0.0",
    "@inertiajs/progress": "^0.2.7",

    // UI Framework (Shadcn-vue)
    "radix-vue": "^1.9.17", // Headless UI
    "reka-ui": "^2.6.0", // Additional components
    "lucide-vue-next": "^0.553.0", // Icons
    "class-variance-authority": "^0.7.1", // CVA utility
    "clsx": "^2.1.1", // Class merging
    "tailwind-merge": "^3.3.1", // Tailwind merger
    "tailwindcss-animate": "^1.0.7", // Animations

    // Forms & Validation
    "vee-validate": "^4.15.1", // Form validation

    // Rich Text
    "@tiptap/vue-3": "^3.10.7", // WYSIWYG editor
    "@tiptap/starter-kit": "^3.10.7",
    "@tiptap/extension-placeholder": "^3.10.7",

    // Charts
    "chart.js": "^4.5.1", // Charting library
    "vue-chartjs": "^5.3.3", // Vue wrapper

    // Utilities
    "date-fns": "^4.1.0", // Date manipulation
    "nprogress": "^0.2.0" // Progress bar
}
```

#### 🛠️ Dev Dependencies (13 total)

```json
{
    // Build Tools
    "vite": "^6.0.0", // Build tool
    "laravel-vite-plugin": "^2.0.0", // Laravel integration
    "@vitejs/plugin-vue": "^5.0.0", // Vue plugin

    // Styling
    "tailwindcss": "^3.2.1", // CSS framework
    "@tailwindcss/forms": "^0.5.3", // Form styles
    "@tailwindcss/vite": "^4.0.0", // Vite plugin
    "autoprefixer": "^10.4.12", // CSS prefixer
    "postcss": "^8.4.31", // CSS processor

    // HTTP & Utils
    "axios": "^1.11.0", // HTTP client
    "concurrently": "^9.0.1", // Run multiple commands
    "@vueuse/core": "^11.3.0", // Vue composables

    // Additional
    "@vueup/vue-quill": "^1.2.0", // Quill editor (unused?)
    "dompurify": "^3.3.0", // XSS sanitization
    "marked": "^17.0.0" // Markdown parser
}
```

---

### Docker Infrastructure (6 Containers)

```yaml
1. orionone-app (Laravel + PHP-FPM 8.2)
   - Dockerfile custom
   - Volume: ./:/var/www/html
   - Health check: php -v

2. orionone-frontend (Node 20-alpine)
   - Runs: npm run dev
   - Port: 5173
   - Hot reload enabled

3. orionone-postgres (PostgreSQL 16-alpine)
   - Port: 5432
   - Volume: orionone_pgdata
   - Health check: pg_isready

4. orionone-redis (Redis 7-alpine)
   - Port: 6379
   - Persistence: AOF enabled
   - Volume: orionone_redisdata

5. orionone-meilisearch (v1.12)
   - Port: 7700
   - Volume: orionone_meilisearch
   - API key protected

6. orionone-nginx (nginx:alpine)
   - Port: 8888 (host) → 80 (container)
   - Config: docker/nginx/default.conf
   - Proxy to PHP-FPM
```

---

## 🎯 NOVO STACK: Next.js 15 + Nest.js 10

### Estratégia: Desenvolvimento Acelerado com Ferramentas Modernas

**Objetivo:** Completar 100% do MVP até 31 Janeiro 2025 (10 semanas)

**Abordagem:**

1. **Maximizar código gerado** (Prisma, NestJS CLI, Shadcn-ui)
2. **Reutilizar bibliotecas existentes** (Tiptap, Chart.js, date-fns)
3. **Usar templates prontos** (Next.js SaaS starters)
4. **Automação de testes** (GitHub Actions CI/CD)

---

### Backend: Nest.js 10 Stack Otimizado

#### 🚀 Core Framework (Instalação Obrigatória)

```bash
# CLI global (código gerado automático)
npm i -g @nestjs/cli

# Criar projeto
nest new nest-backend --strict --package-manager npm
```

```json
{
    "@nestjs/core": "^10.4",
    "@nestjs/common": "^10.4",
    "@nestjs/platform-express": "^10.4",
    "reflect-metadata": "^0.2.2",
    "rxjs": "^7.8"
}
```

**🔥 Ganho de Velocidade:**

-   CLI gera modules/controllers/services automaticamente
-   Decorators reduzem boilerplate 70%
-   Dependency injection nativa (zero config)

---

#### 🗄️ Database: Prisma ORM (RECOMENDADO para velocidade)

**Por que Prisma > TypeORM:**

-   ✅ Schema-first (auto-migração)
-   ✅ Type-safe queries (zero erros em runtime)
-   ✅ Prisma Studio (GUI visual)
-   ✅ Migrations automáticas
-   ✅ Geração de tipos TypeScript

```bash
npm install prisma @prisma/client
npx prisma init
```

```json
{
    "@prisma/client": "^6.2",
    "prisma": "^6.2"
}
```

**Conversão de migrations Laravel → Prisma:**

```prisma
// prisma/schema.prisma (auto-gerado!)
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  name      String
  email     String   @unique
  password  String
  avatar    String?
  role      Role     @default(USER)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  deletedAt DateTime? @map("deleted_at")

  ticketsCreated  Ticket[] @relation("Requester")
  ticketsAssigned Ticket[] @relation("Assignee")
  comments        Comment[]
  activityLogs    ActivityLog[]

  @@map("users")
}

enum Role {
  ADMIN
  AGENT
  USER
}
```

**Comandos mágicos:**

```bash
# Criar migration a partir do schema
npx prisma migrate dev --name init

# Gerar tipos TypeScript automaticamente
npx prisma generate

# GUI para visualizar database
npx prisma studio
```

---

#### 🔐 Authentication & Authorization

**Substituir Laravel Sanctum + Spatie Permission:**

```bash
npm install @nestjs/passport @nestjs/jwt passport passport-jwt bcrypt
npm install @casl/ability @casl/prisma
npm install -D @types/passport-jwt @types/bcrypt
```

```json
{
    "@nestjs/passport": "^10.0",
    "@nestjs/jwt": "^10.2",
    "passport": "^0.7",
    "passport-jwt": "^4.0",
    "bcrypt": "^5.1",
    "@casl/ability": "^6.7", // Substituir Spatie Permission
    "@casl/prisma": "^1.4" // Prisma integration
}
```

**Setup em 5 minutos:**

```typescript
// nest-backend/src/auth/jwt.strategy.ts (gerado pelo CLI)
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private prisma: PrismaService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET,
    });
  }

  async validate(payload: { sub: string; email: string }) {
    return this.prisma.user.findUnique({ where: { id: payload.sub } });
  }
}

// Usar em qualquer controller
@UseGuards(JwtAuthGuard)
@Get('profile')
getProfile(@User() user: User) {
  return user;
}
```

**CASL RBAC (substituir Spatie Permission):**

```typescript
// abilities/ability.factory.ts
@Injectable()
export class AbilityFactory {
  createForUser(user: User) {
    const { can, cannot, build } = new AbilityBuilder(PrismaAbility);

    if (user.role === Role.ADMIN) {
      can('manage', 'all'); // Tudo permitido
    } else if (user.role === Role.AGENT) {
      can('read', 'Ticket');
      can('update', 'Ticket', { assignedTo: user.id });
      can('create', 'Comment');
    } else {
      can('read', 'Ticket', { requesterId: user.id });
      can('create', 'Ticket');
    }

    return build();
  }
}

// Usar em controller
@Post('tickets/:id/assign')
async assignTicket(@Param('id') id: string, @User() user: User) {
  const ability = this.abilityFactory.createForUser(user);

  if (!ability.can('update', 'Ticket')) {
    throw new ForbiddenException();
  }

  return this.ticketsService.assign(id, user.id);
}
```

---

#### 📁 File Upload & Storage

**Substituir Intervention/Image + Spatie MediaLibrary:**

```bash
npm install @nestjs/platform-express multer sharp
npm install @aws-sdk/client-s3  # Se usar S3
npm install -D @types/multer
```

```json
{
    "multer": "^1.4.5-lts.1", // File upload middleware
    "sharp": "^0.33", // Substituir Intervention/Image
    "@aws-sdk/client-s3": "^3.600" // S3 storage (opcional)
}
```

**Código 90% mais simples:**

```typescript
// upload.service.ts
@Injectable()
export class UploadService {
  async processAvatar(file: Express.Multer.File): Promise<string> {
    const filename = `${randomUUID()}.webp`;
    const outputPath = `uploads/avatars/${filename}`;

    // Sharp = Intervention/Image mas 5x mais rápido
    await sharp(file.buffer)
      .resize(300, 300, { fit: 'cover' })
      .webp({ quality: 80 })
      .toFile(outputPath);

    return outputPath;
  }
}

// Controller
@Post('profile/avatar')
@UseInterceptors(FileInterceptor('avatar'))
async uploadAvatar(
  @UploadedFile() file: Express.Multer.File,
  @User() user: User
) {
  const avatarUrl = await this.uploadService.processAvatar(file);

  return this.prisma.user.update({
    where: { id: user.id },
    data: { avatar: avatarUrl },
  });
}
```

---

#### 🔍 Search Engine

**Substituir Laravel Scout + Meilisearch:**

```bash
npm install meilisearch
```

```json
{
    "meilisearch": "^0.43" // Mesmo client JS
}
```

**REUTILIZAR container Docker existente:**

```yaml
# docker-compose.yml (sem mudanças!)
orionone-meilisearch:
    image: getmeili/meilisearch:v1.12
    ports:
        - "7700:7700"
    environment:
        MEILI_MASTER_KEY: masterKey
```

**Integração em 10 linhas:**

```typescript
// search.service.ts
import { MeiliSearch } from "meilisearch";

@Injectable()
export class SearchService {
    private client: MeiliSearch;

    constructor() {
        this.client = new MeiliSearch({
            host: process.env.MEILISEARCH_HOST,
            apiKey: process.env.MEILISEARCH_KEY,
        });
    }

    async indexTicket(ticket: Ticket) {
        const index = this.client.index("tickets");
        await index.addDocuments([
            {
                id: ticket.id,
                ticketNumber: ticket.ticketNumber,
                title: ticket.title,
                description: ticket.description,
            },
        ]);
    }

    async search(query: string) {
        const index = this.client.index("tickets");
        return index.search(query, { limit: 20 });
    }
}
```

---

#### 📊 Excel Import/Export

**Substituir Maatwebsite/Excel:**

```bash
npm install exceljs
```

```json
{
    "exceljs": "^4.4" // Mais poderoso que Maatwebsite
}
```

**Exemplo: Export de tickets:**

```typescript
// excel.service.ts
import ExcelJS from 'exceljs';

@Injectable()
export class ExcelService {
  async exportTickets(tickets: Ticket[]): Promise<Buffer> {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Tickets');

    worksheet.columns = [
      { header: 'Ticket #', key: 'ticketNumber', width: 15 },
      { header: 'Title', key: 'title', width: 30 },
      { header: 'Status', key: 'status', width: 15 },
      { header: 'Priority', key: 'priority', width: 10 },
      { header: 'Created', key: 'createdAt', width: 20 },
    ];

    worksheet.addRows(tickets);

    // Style header
    worksheet.getRow(1).font = { bold: true };
    worksheet.getRow(1).fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FF4F81BD' },
    };

    return workbook.xlsx.writeBuffer();
  }
}

// Controller
@Get('tickets/export')
async exportTickets(@Res() res: Response) {
  const tickets = await this.ticketsService.findAll();
  const buffer = await this.excelService.exportTickets(tickets);

  res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
  res.setHeader('Content-Disposition', 'attachment; filename=tickets.xlsx');
  res.send(buffer);
}
```

---

#### ✉️ Queue & Background Jobs

**Substituir Laravel Queues:**

```bash
npm install @nestjs/bull bull
npm install -D @types/bull
```

```json
{
    "@nestjs/bull": "^10.2", // Queue module
    "bull": "^4.16" // Redis-based queue
}
```

**REUTILIZAR container Redis existente:**

```typescript
// app.module.ts
@Module({
    imports: [
        BullModule.forRoot({
            redis: {
                host: process.env.REDIS_HOST,
                port: parseInt(process.env.REDIS_PORT),
            },
        }),
        BullModule.registerQueue({
            name: "emails",
        }),
    ],
})
export class AppModule {}

// emails.processor.ts
@Processor("emails")
export class EmailsProcessor {
    @Process("send-notification")
    async sendNotification(job: Job<{ to: string; subject: string }>) {
        console.log("Sending email to:", job.data.to);
        // Send email logic
    }
}

// tickets.service.ts
@Injectable()
export class TicketsService {
    constructor(@InjectQueue("emails") private emailQueue: Queue) {}

    async createTicket(dto: CreateTicketDto) {
        const ticket = await this.prisma.ticket.create({ data: dto });

        // Enviar email em background
        await this.emailQueue.add("send-notification", {
            to: ticket.requester.email,
            subject: `Ticket ${ticket.ticketNumber} criado`,
        });

        return ticket;
    }
}
```

---

#### 📝 Validation & DTOs

**Substituir Spatie Laravel Data:**

```bash
npm install class-validator class-transformer
```

```json
{
    "class-validator": "^0.14", // Decorators de validação
    "class-transformer": "^0.5" // Transformação de tipos
}
```

**Validação automática (melhor que Laravel Request):**

```typescript
// create-ticket.dto.ts
import { IsString, IsEnum, MinLength, MaxLength } from 'class-validator';

export class CreateTicketDto {
  @IsString()
  @MinLength(5)
  @MaxLength(200)
  title: string;

  @IsString()
  @MinLength(10)
  description: string;

  @IsEnum(TicketPriority)
  priority: TicketPriority;

  @IsEnum(TicketStatus)
  status: TicketStatus = TicketStatus.OPEN;
}

// Controller (validação AUTOMÁTICA!)
@Post()
create(@Body() dto: CreateTicketDto) {
  // Se chegar aqui, dto já está validado!
  return this.ticketsService.create(dto);
}
```

---

#### 📚 API Documentation

**Substituir Knuckles Scribe:**

```bash
npm install @nestjs/swagger swagger-ui-express
```

```json
{
    "@nestjs/swagger": "^8.0", // OpenAPI generator
    "swagger-ui-express": "^5.0" // UI visual
}
```

**Documentação AUTOMÁTICA (zero config manual):**

```typescript
// main.ts
const config = new DocumentBuilder()
    .setTitle("OrionOne ITSM API")
    .setDescription("ServiceNow-like ticket management system")
    .setVersion("1.0")
    .addBearerAuth()
    .build();

const document = SwaggerModule.createDocument(app, config);
SwaggerModule.setup("api/docs", app, document);

// Acesso: http://localhost:3001/api/docs
```

**Decorators para documentar endpoints:**

```typescript
@ApiTags("tickets")
@Controller("tickets")
export class TicketsController {
    @Post()
    @ApiOperation({ summary: "Create new ticket" })
    @ApiResponse({ status: 201, description: "Ticket created", type: Ticket })
    @ApiResponse({ status: 400, description: "Invalid data" })
    @ApiBearerAuth()
    create(@Body() dto: CreateTicketDto) {
        return this.ticketsService.create(dto);
    }
}
```

---

#### 🧪 Testing

**Substituir Pest PHP:**

```bash
npm install --save-dev jest @types/jest ts-jest
npm install --save-dev @nestjs/testing
npm install --save-dev supertest @types/supertest
```

```json
{
    "jest": "^29.7",
    "@nestjs/testing": "^10.4",
    "supertest": "^7.0", // API testing
    "@faker-js/faker": "^9.3" // Fake data
}
```

**Exemplo de teste (similar ao Pest):**

```typescript
// tickets.service.spec.ts
describe("TicketsService", () => {
    let service: TicketsService;
    let prisma: PrismaService;

    beforeEach(async () => {
        const module = await Test.createTestingModule({
            providers: [TicketsService, PrismaService],
        }).compile();

        service = module.get(TicketsService);
        prisma = module.get(PrismaService);
    });

    it("should create a ticket", async () => {
        const dto = {
            title: "Test ticket",
            description: "Test description",
            priority: TicketPriority.HIGH,
        };

        const result = await service.create(dto);

        expect(result.title).toBe(dto.title);
        expect(result.ticketNumber).toMatch(/TKT-\d{8}-\d{4}/);
    });
});
```

---

#### 📊 Monitoring & Logging

**Substituir Laravel Telescope + Pulse:**

```bash
npm install winston
npm install @sentry/node @sentry/profiling-node
```

```json
{
    "winston": "^3.17", // Advanced logging
    "@sentry/node": "^8.0", // Error tracking
    "@sentry/profiling-node": "^8.0" // Performance monitoring
}
```

**Logger customizado:**

```typescript
// logger.service.ts
import winston from "winston";

export const logger = winston.createLogger({
    level: "info",
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: "error.log", level: "error" }),
        new winston.transports.File({ filename: "combined.log" }),
    ],
});

// Usar em qualquer lugar
logger.info("Ticket created", { ticketId: ticket.id });
logger.error("Failed to send email", { error: err.message });
```

---

## 📦 RESUMO: Backend Package Comparison

| Laravel              | Nest.js          | Velocidade | Notas                         |
| -------------------- | ---------------- | ---------- | ----------------------------- |
| Laravel Framework    | @nestjs/core     | ⚡⚡⚡     | CLI gera código               |
| Eloquent ORM         | Prisma           | ⚡⚡⚡⚡   | Type-safe, auto-migrations    |
| Sanctum              | JWT + Passport   | ⚡⚡⚡     | Stateless, melhor para APIs   |
| Spatie Permission    | CASL Ability     | ⚡⚡⚡⚡   | Mais flexível, type-safe      |
| Intervention/Image   | Sharp            | ⚡⚡⚡⚡⚡ | 5x mais rápido                |
| Spatie MediaLibrary  | Multer + Sharp   | ⚡⚡⚡     | Menos features, mais controle |
| Spatie Data          | class-validator  | ⚡⚡⚡⚡   | Validação automática          |
| Spatie Query Builder | Prisma filters   | ⚡⚡⚡⚡   | Type-safe queries             |
| Maatwebsite/Excel    | ExcelJS          | ⚡⚡⚡⚡   | Mais features                 |
| Laravel Actions      | Services (DI)    | ⚡⚡⚡⚡   | Padrão nativo                 |
| Laravel Queues       | Bull + Redis     | ⚡⚡⚡     | Mesma arquitetura             |
| Scribe               | Swagger/OpenAPI  | ⚡⚡⚡⚡⚡ | Auto-gerado                   |
| Pest PHP             | Jest             | ⚡⚡⚡     | Sintaxe similar               |
| Telescope            | Winston + Sentry | ⚡⚡⚡     | Produção-ready                |

**Legenda:**

-   ⚡⚡⚡⚡⚡ = Muito mais rápido/fácil
-   ⚡⚡⚡⚡ = Mais rápido
-   ⚡⚡⚡ = Equivalente
-   ⚡⚡ = Mais complexo

---

## 🔧 CONFIGURAÇÕES CRÍTICAS (Week 0)

### Environment Variables Migration

**Laravel .env → Nest.js .env:**

```env
# Nest.js Backend (.env)
DATABASE_URL="postgresql://laravel:secret@orionone-db:5432/orionone?schema=public"

JWT_SECRET=<generate-with-openssl-rand-base64-32>
JWT_EXPIRATION=7d

REDIS_HOST=orionone-redis
REDIS_PORT=6379

MEILISEARCH_HOST=http://orionone-meilisearch:7700
MEILISEARCH_API_KEY=masterKey

NODE_ENV=development
PORT=3001

# Email (Mailpit for dev)
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_FROM=noreply@orionone.com
```

**Next.js Frontend (.env.local):**

```env
NEXT_PUBLIC_API_URL=http://localhost:3001
```

---

### Docker Networking & CORS

**Problema:** Next.js precisa se comunicar com Nest.js via container hostname

**docker-compose.yml (adaptado):**

```yaml
services:
    backend:
        build: ./nest-backend
        ports: ["3001:3001"]
        environment:
            DATABASE_URL: postgresql://laravel:secret@postgres:5432/orionone
        networks: [orionone_network]
        healthcheck:
            test: ["CMD", "wget", "--spider", "http://localhost:3001/health"]

    frontend:
        build: ./next-frontend
        ports: ["3000:3000"]
        environment:
            NEXT_PUBLIC_API_URL: http://backend:3001
        depends_on: [backend]
        networks: [orionone_network]

    nginx:
        image: nginx:alpine
        ports: ["80:80"]
        volumes: ["./nginx.conf:/etc/nginx/nginx.conf:ro"]
        depends_on: [frontend, backend]
        networks: [orionone_network]
```

**Nest.js CORS (main.ts):**

```typescript
app.enableCors({
    origin: [
        "http://localhost:3000",
        "http://localhost",
        "http://frontend:3000",
    ],
    credentials: true,
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization"],
});
```

---

### Tailwind CSS Variables (100% Reusable!)

**CRÍTICO:** Copiar exatamente do Laravel para manter aparência idêntica

**Laravel:** `resources/css/app.css`
**Next.js:** `app/globals.css`

```css
/* Copiar todas as 30+ CSS variables */
@layer base {
    :root {
        --background: 0 0% 100%;
        --foreground: 240 10% 3.9%;
        --primary: 240 5.9% 10%;
        --radius: 0.5rem;
        --chart-1: 12 76% 61%;
        /* ... etc */
    }
    .dark {
        /* ... */
    }
}
```

**tailwind.config.ts (Next.js):**

```typescript
// Copiar colors, borderRadius, fontFamily do Laravel
export default {
    darkMode: ["class"],
    theme: {
        extend: {
            colors: {
                background: "hsl(var(--background))",
                // ... copiar todos
            },
        },
    },
};
```

---

### TypeScript Path Aliases

**tsconfig.json (Next.js):**

```json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@/*": ["./"],
            "@/components/*": ["./components/*"],
            "@/lib/*": ["./lib/*"],
            "@/hooks/*": ["./hooks/*"],
            "@/types/*": ["./types/*"]
        }
    }
}
```

**components.json (Shadcn-ui):**

```json
{
    "aliases": {
        "components": "@/components",
        "utils": "@/lib/utils",
        "ui": "@/components/ui"
    }
}
```

---

### Storage Strategy

**Development:** Local storage
**Production:** MinIO (S3-compatible) ou AWS S3

**Nest.js Local Storage:**

```typescript
// upload.service.ts
const filepath = path.join(process.cwd(), "uploads", "avatars", filename);
await sharp(file.buffer).resize(300, 300).toFile(filepath);

// main.ts - Serve static files
app.useStaticAssets(path.join(__dirname, "..", "uploads"), {
    prefix: "/uploads/",
});
```

---

## 🚀 PRÓXIMOS PASSOS

**Hoje (13 Nov):**

1. ✅ Análise completa concluída (17 gaps identificados)
2. ✅ Criar MIGRATION-PART-2-BACKEND.md (database + código)
3. ✅ Criar MIGRATION-PART-3-FRONTEND.md (Next.js setup)
4. ✅ Criar MIGRATION-PART-4-TIMELINE.md (10 semanas detalhadas)
5. ✅ Criar MIGRATION-REVIEW-GAPS.md (análise de gaps)

**Amanhã (14 Nov):**

-   Decisão final: Aprovar migração?
-   Criar branch `feat/migrate-nextjs-nestjs`
-   Backup projeto Laravel (tag `v0.1.0-laravel`)

---

**Continua em:** `MIGRATION-PART-2-BACKEND.md`
