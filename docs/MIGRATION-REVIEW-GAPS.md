# 🔍 Revisão de Migração - Gaps Identificados

**Data:** 13 Novembro 2025
**Status:** PRÉ-MIGRAÇÃO - Análise Completa

---

## ✅ PONTOS FORTES DO PLANO

### 1. **Documentação Completa**

-   ✅ Part 1: Setup & Infrastructure (877 linhas) - Package mapping, Docker analysis
-   ✅ Part 2: Backend Migration (1108 linhas) - Prisma schema, Nest.js code
-   ✅ Part 3: Frontend Migration (840 linhas) - Next.js structure, React components
-   ✅ Part 4: Timeline (844 linhas) - 10 weeks detailed plan

### 2. **Stack Analysis Completo**

-   ✅ 17 Laravel production packages mapeados
-   ✅ 13 Vue frontend packages mapeados
-   ✅ 14 database migrations catalogadas
-   ✅ Docker Compose com 6 containers analisado

### 3. **Código Production-Ready**

-   ✅ Prisma schema completo (15 models, 6 enums)
-   ✅ Auth JWT + CASL (código pronto)
-   ✅ TicketsService com SLA calculation
-   ✅ UploadService com Sharp processing

---

## ⚠️ GAPS CRÍTICOS IDENTIFICADOS

### **GAP 1: Environment Variables Migration**

**Problema:** Plano não detalha como migrar variáveis de ambiente Laravel → Nest.js/Next.js

**Laravel .env atual:**

```env
APP_NAME=Laravel
DB_CONNECTION=pgsql
DB_HOST=orionone-db
DB_PORT=5432
DB_DATABASE=orionone
DB_USERNAME=laravel
DB_PASSWORD=secret
REDIS_HOST=orionone-redis
MEILISEARCH_HOST=http://orionone-meilisearch:7700
MEILISEARCH_KEY=masterKey
```

**Nest.js .env necessário:**

```env
# Database
DATABASE_URL="postgresql://laravel:secret@orionone-db:5432/orionone?schema=public"

# JWT
JWT_SECRET=<generate-with-openssl>
JWT_EXPIRATION=7d

# Redis
REDIS_HOST=orionone-redis
REDIS_PORT=6379

# Meilisearch
MEILISEARCH_HOST=http://orionone-meilisearch:7700
MEILISEARCH_API_KEY=masterKey

# App
NODE_ENV=development
PORT=3001
```

**Next.js .env.local necessário:**

```env
NEXT_PUBLIC_API_URL=http://localhost:3001
```

**Solução:** Adicionar à Week 0 Day 2:

-   [ ] Criar `nest-backend/.env` com DATABASE_URL e configs
-   [ ] Gerar JWT_SECRET: `openssl rand -base64 32`
-   [ ] Criar `next-frontend/.env.local` com API_URL

---

### **GAP 2: Database Triggers e Views**

**Problema:** Laravel tem 2 triggers e 3 views que não foram convertidos para Prisma

**Triggers Atuais (PostgreSQL):**

1. **auto_generate_ticket_number** - Gera TKT-YYYYMMDD-0001 automaticamente
2. **auto_calculate_sla_deadlines** - Calcula deadlines baseado em priority

**Views Atuais:**

1. **dashboard_metrics_view** - Métricas agregadas (tickets por status)
2. **sla_compliance_view** - Taxa de compliance SLA
3. **agent_performance_view** - Performance média dos agentes

**Conversão para Nest.js:**

**OPÇÃO A (Recomendada): Mover lógica para Application Layer**

```typescript
// Em vez de trigger, usar no TicketsService.create():
async create(dto: CreateTicketDto) {
  const ticketNumber = await this.generateTicketNumber(); // Lógica no código
  const slaDeadlines = this.calculateSLA(dto.priority); // Lógica no código

  return this.prisma.ticket.create({
    data: { ...dto, ticketNumber, ...slaDeadlines }
  });
}
```

✅ **Vantagem:** Mais fácil de testar, debug, e manter
❌ **Desvantagem:** Se alguém inserir direto no DB, triggers não executam

**OPÇÃO B: Manter Triggers no PostgreSQL**

```typescript
// Week 1: Criar migration raw SQL
await prisma.$executeRaw`
  CREATE OR REPLACE FUNCTION auto_generate_ticket_number()
  RETURNS trigger AS $$
  -- código do trigger aqui
  $$ LANGUAGE plpgsql;
`;
```

✅ **Vantagem:** Garante consistência mesmo com inserts diretos
❌ **Desvantagem:** Mais complexo, dificulta testes

**OPÇÃO C: Híbrido (RECOMENDAÇÃO FINAL)**

-   Triggers → Mover para Application Layer (TicketsService)
-   Views → Manter no DB (performance em queries complexas)

```typescript
// DashboardService (usa views existentes)
async getMetrics() {
  return this.prisma.$queryRaw`SELECT * FROM dashboard_metrics_view`;
}
```

**Solução:** Adicionar à Week 1 Day 1:

-   [ ] Decidir estratégia: Application Layer vs DB Triggers
-   [ ] Se Application Layer: Implementar em Services
-   [ ] Se DB Triggers: Criar Prisma migrations com raw SQL
-   [ ] Manter Views no DB para queries de reports

---

### **GAP 3: Seed Data - Permissions Detalhadas**

**Problema:** Prisma seed mencionado mas sem lista completa de 50+ permissions

**Laravel Permissions (implementação-checklist.md):**

```php
// Tickets
tickets.create, tickets.view, tickets.update, tickets.delete
tickets.assign, tickets.close, tickets.reopen
tickets.view_all, tickets.view_assigned, tickets.view_own

// Comments
comments.create, comments.view, comments.update, comments.delete
comments.view_internal

// Articles
articles.create, articles.view, articles.update, articles.delete
articles.publish, articles.view_draft

// Assets
assets.create, assets.view, assets.update, assets.delete
assets.assign, assets.import

// Users
users.create, users.view, users.update, users.delete
users.manage_roles

// Teams
teams.create, teams.view, teams.update, teams.delete
teams.manage_members

// Reports
reports.view, reports.export
```

**Prisma Seed Completo:**

```typescript
// prisma/seed.ts
async function main() {
    // 1. Create Permissions (32 total)
    const permissions = [
        // Tickets (9)
        {
            name: "tickets.create",
            guardName: "api",
            description: "Create tickets",
        },
        { name: "tickets.view", guardName: "api", description: "View tickets" },
        {
            name: "tickets.update",
            guardName: "api",
            description: "Update tickets",
        },
        {
            name: "tickets.delete",
            guardName: "api",
            description: "Delete tickets",
        },
        {
            name: "tickets.assign",
            guardName: "api",
            description: "Assign tickets",
        },
        {
            name: "tickets.close",
            guardName: "api",
            description: "Close tickets",
        },
        {
            name: "tickets.view_all",
            guardName: "api",
            description: "View all tickets",
        },
        {
            name: "tickets.view_assigned",
            guardName: "api",
            description: "View assigned tickets",
        },
        {
            name: "tickets.view_own",
            guardName: "api",
            description: "View own tickets",
        },
        // Comments (4)
        {
            name: "comments.create",
            guardName: "api",
            description: "Create comments",
        },
        {
            name: "comments.view",
            guardName: "api",
            description: "View comments",
        },
        {
            name: "comments.update",
            guardName: "api",
            description: "Update comments",
        },
        {
            name: "comments.view_internal",
            guardName: "api",
            description: "View internal comments",
        },
        // Articles (6)
        {
            name: "articles.create",
            guardName: "api",
            description: "Create articles",
        },
        {
            name: "articles.view",
            guardName: "api",
            description: "View articles",
        },
        {
            name: "articles.update",
            guardName: "api",
            description: "Update articles",
        },
        {
            name: "articles.delete",
            guardName: "api",
            description: "Delete articles",
        },
        {
            name: "articles.publish",
            guardName: "api",
            description: "Publish articles",
        },
        {
            name: "articles.view_draft",
            guardName: "api",
            description: "View draft articles",
        },
        // Assets (5)
        {
            name: "assets.create",
            guardName: "api",
            description: "Create assets",
        },
        { name: "assets.view", guardName: "api", description: "View assets" },
        {
            name: "assets.update",
            guardName: "api",
            description: "Update assets",
        },
        {
            name: "assets.delete",
            guardName: "api",
            description: "Delete assets",
        },
        {
            name: "assets.import",
            guardName: "api",
            description: "Import assets from CSV",
        },
        // Users (4)
        { name: "users.view", guardName: "api", description: "View users" },
        { name: "users.update", guardName: "api", description: "Update users" },
        { name: "users.delete", guardName: "api", description: "Delete users" },
        {
            name: "users.manage_roles",
            guardName: "api",
            description: "Manage user roles",
        },
        // Teams (4)
        { name: "teams.create", guardName: "api", description: "Create teams" },
        { name: "teams.view", guardName: "api", description: "View teams" },
        { name: "teams.update", guardName: "api", description: "Update teams" },
        {
            name: "teams.manage_members",
            guardName: "api",
            description: "Manage team members",
        },
    ];

    for (const perm of permissions) {
        await prisma.permission.upsert({
            where: { name: perm.name },
            update: {},
            create: perm,
        });
    }

    // 2. Assign Permissions to Roles
    const adminPerms = permissions.map((p) => p.name); // All permissions
    const agentPerms = [
        "tickets.create",
        "tickets.view",
        "tickets.update",
        "tickets.assign",
        "tickets.close",
        "tickets.view_all",
        "tickets.view_assigned",
        "comments.create",
        "comments.view",
        "comments.update",
        "comments.view_internal",
        "articles.view",
        "teams.view",
        "assets.view",
    ];
    const userPerms = [
        "tickets.create",
        "tickets.view",
        "tickets.view_own",
        "comments.create",
        "comments.view",
        "articles.view",
    ];

    // 3. Create RoleHasPermissions
    for (const permName of adminPerms) {
        const perm = await prisma.permission.findUnique({
            where: { name: permName },
        });
        await prisma.roleHasPermission.create({
            data: { roleName: "ADMIN", permissionId: perm.id },
        });
    }
    // Repetir para AGENT e USER...

    // 4. Create Test Users
    const users = [
        { name: "Admin User", email: "admin@orionone.com", role: "ADMIN" },
        { name: "Agent User", email: "agent@orionone.com", role: "AGENT" },
        { name: "Normal User", email: "user@orionone.com", role: "USER" },
    ];

    for (const user of users) {
        await prisma.user.create({
            data: {
                ...user,
                password: await bcrypt.hash("password", 10),
                emailVerifiedAt: new Date(),
            },
        });
    }
}
```

**Solução:** Adicionar à Week 1 Day 1:

-   [ ] Criar `prisma/seed.ts` completo com 32 permissions
-   [ ] Mapear permissions para 3 roles (ADMIN, AGENT, USER)
-   [ ] Criar 3 test users (1 por role)
-   [ ] Executar `npx prisma db seed`

---

### **GAP 4: File Uploads - Storage Strategy**

**Problema:** Sharp processa imagens, mas onde armazenar? Local? S3?

**Laravel Atual:**

-   Storage: `storage/app/public/avatars/`
-   Symlink: `public/storage → storage/app/public`
-   URL: `http://localhost/storage/avatars/user.jpg`

**Nest.js Opções:**

**OPÇÃO A: Local Storage (Desenvolvimento)**

```typescript
// nest-backend/src/upload/upload.service.ts
async processAvatar(file: Express.Multer.File) {
  const filename = `${uuidv4()}.webp`;
  const filepath = path.join(process.cwd(), 'uploads', 'avatars', filename);

  await sharp(file.buffer)
    .resize(300, 300)
    .webp({ quality: 80 })
    .toFile(filepath);

  return { url: `/uploads/avatars/${filename}` };
}

// main.ts - Servir arquivos estáticos
app.useStaticAssets(path.join(__dirname, '..', 'uploads'), {
  prefix: '/uploads/',
});
```

✅ **Vantagem:** Simples, zero config
❌ **Desvantagem:** Não escala (1 servidor), perde files em redeploy

**OPÇÃO B: S3/MinIO (Produção)**

```typescript
// AWS S3 ou MinIO (S3-compatible, self-hosted)
npm install @aws-sdk/client-s3

async processAvatar(file: Express.Multer.File) {
  const buffer = await sharp(file.buffer)
    .resize(300, 300)
    .webp({ quality: 80 })
    .toBuffer();

  const key = `avatars/${uuidv4()}.webp`;
  await this.s3.putObject({
    Bucket: 'orionone',
    Key: key,
    Body: buffer,
    ContentType: 'image/webp',
  });

  return { url: `https://s3.amazonaws.com/orionone/${key}` };
}
```

✅ **Vantagem:** Escalável, durável, CDN-ready
❌ **Desvantagem:** Precisa AWS account ou MinIO container

**RECOMENDAÇÃO: Híbrido**

-   **Week 1-8:** Local Storage (desenvolvimento rápido)
-   **Week 9:** Migrar para MinIO container (add no docker-compose)
-   **Produção:** S3 ou DigitalOcean Spaces

**Solução:** Adicionar à Week 1 Day 5:

-   [ ] Implementar Local Storage (uploads/ folder)
-   [ ] Servir static files em main.ts
-   [ ] Adicionar à Week 9: Setup MinIO container
-   [ ] Documentar S3 migration para produção

---

### **GAP 5: Email Notifications - Configuração**

**Problema:** Queue jobs enviam emails, mas sem config SMTP

**Laravel Atual (.env):**

```env
MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${APP_NAME}"
```

**Nest.js Solução:**

```bash
npm install @nestjs-modules/mailer nodemailer
npm install -D @types/nodemailer
```

```typescript
// nest-backend/src/mail/mail.module.ts
import { MailerModule } from "@nestjs-modules/mailer";

@Module({
    imports: [
        MailerModule.forRoot({
            transport: {
                host: process.env.MAIL_HOST || "mailpit",
                port: parseInt(process.env.MAIL_PORT) || 1025,
                secure: false,
                auth: {
                    user: process.env.MAIL_USERNAME,
                    pass: process.env.MAIL_PASSWORD,
                },
            },
            defaults: {
                from: '"OrionOne" <noreply@orionone.com>',
            },
        }),
    ],
})
export class MailModule {}
```

**Docker Compose - Adicionar Mailpit:**

```yaml
# Adicionar service
mailpit:
    image: axllent/mailpit
    container_name: orionone_mailpit
    ports:
        - "1025:1025" # SMTP
        - "8025:8025" # Web UI
    networks:
        - orionone_network
```

**Solução:** Adicionar à Week 8 Day 2:

-   [ ] Instalar @nestjs-modules/mailer
-   [ ] Configurar MailModule com Mailpit
-   [ ] Adicionar Mailpit ao docker-compose.yml
-   [ ] Testar email: http://localhost:8025 (UI)

---

### **GAP 6: Testing Strategy - Missing Details**

**Problema:** Timeline menciona 80% coverage, mas sem detalhes de COMO

**Estrutura de Testes Necessária:**

```
nest-backend/
├── test/
│   ├── unit/              # Jest unit tests
│   │   ├── auth.service.spec.ts
│   │   ├── tickets.service.spec.ts
│   │   └── ...
│   │
│   ├── integration/       # API tests (Supertest)
│   │   ├── auth.e2e-spec.ts
│   │   ├── tickets.e2e-spec.ts
│   │   └── ...
│   │
│   └── fixtures/          # Test data
│       ├── users.fixture.ts
│       ├── tickets.fixture.ts
│       └── ...
│
next-frontend/
├── __tests__/
│   ├── components/        # React Testing Library
│   │   ├── TicketCard.test.tsx
│   │   └── ...
│   │
│   └── e2e/               # Playwright
│       ├── auth.spec.ts
│       ├── tickets.spec.ts
│       └── ...
```

**Jest Config (nest-backend):**

```json
// package.json
{
    "jest": {
        "coverageThreshold": {
            "global": {
                "branches": 80,
                "functions": 80,
                "lines": 80,
                "statements": 80
            }
        },
        "collectCoverageFrom": [
            "src/**/*.ts",
            "!src/main.ts",
            "!src/**/*.module.ts"
        ]
    }
}
```

**Playwright Config (next-frontend):**

```typescript
// playwright.config.ts
export default defineConfig({
    testDir: "./__tests__/e2e",
    use: {
        baseURL: "http://localhost:3000",
        screenshot: "only-on-failure",
        video: "retain-on-failure",
    },
    projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
```

**Solução:** Adicionar à Week 9:

-   [ ] Day 1: Criar estrutura de pastas test/
-   [ ] Day 1: Configurar Jest coverage threshold
-   [ ] Day 2: Configurar Supertest (API tests)
-   [ ] Day 3: Configurar Playwright + devices
-   [ ] Day 4: Criar fixtures reutilizáveis (users, tickets)

---

### **GAP 7: CI/CD - GitHub Actions Missing Steps**

**Problema:** Week 10 menciona CI/CD, mas sem workflow file

**GitHub Actions Completo:**

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
    push:
        branches: [main, feat/migrate-nextjs-nestjs]
    pull_request:
        branches: [main]

jobs:
    backend-tests:
        runs-on: ubuntu-latest

        services:
            postgres:
                image: postgres:16
                env:
                    POSTGRES_PASSWORD: secret
                options: >-
                    --health-cmd pg_isready
                    --health-interval 10s
                    --health-timeout 5s
                    --health-retries 5

        steps:
            - uses: actions/checkout@v4

            - name: Setup Node.js
              uses: actions/setup-node@v4
              with:
                  node-version: "20"
                  cache: "npm"
                  cache-dependency-path: nest-backend/package-lock.json

            - name: Install dependencies
              working-directory: nest-backend
              run: npm ci

            - name: Run Prisma migrations
              working-directory: nest-backend
              run: npx prisma migrate deploy
              env:
                  DATABASE_URL: postgresql://postgres:secret@localhost:5432/test

            - name: Run unit tests
              working-directory: nest-backend
              run: npm test -- --coverage

            - name: Run E2E tests
              working-directory: nest-backend
              run: npm run test:e2e

            - name: Upload coverage
              uses: codecov/codecov-action@v4
              with:
                  files: nest-backend/coverage/lcov.info

    frontend-tests:
        runs-on: ubuntu-latest

        steps:
            - uses: actions/checkout@v4

            - name: Setup Node.js
              uses: actions/setup-node@v4
              with:
                  node-version: "20"
                  cache: "npm"
                  cache-dependency-path: next-frontend/package-lock.json

            - name: Install dependencies
              working-directory: next-frontend
              run: npm ci

            - name: Run Playwright tests
              working-directory: next-frontend
              run: npx playwright test

            - name: Upload Playwright report
              if: failure()
              uses: actions/upload-artifact@v4
              with:
                  name: playwright-report
                  path: next-frontend/playwright-report/

    build-images:
        needs: [backend-tests, frontend-tests]
        runs-on: ubuntu-latest
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'

        steps:
            - uses: actions/checkout@v4

            - name: Login to Docker Hub
              uses: docker/login-action@v3
              with:
                  username: ${{ secrets.DOCKERHUB_USERNAME }}
                  password: ${{ secrets.DOCKERHUB_TOKEN }}

            - name: Build and push backend
              uses: docker/build-push-action@v5
              with:
                  context: nest-backend
                  push: true
                  tags: orionone/backend:latest

            - name: Build and push frontend
              uses: docker/build-push-action@v5
              with:
                  context: next-frontend
                  push: true
                  tags: orionone/frontend:latest
```

**Solução:** Adicionar à Week 10 Day 2:

-   [ ] Criar `.github/workflows/ci.yml`
-   [ ] Adicionar secrets no GitHub: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN
-   [ ] Testar pipeline: commit → push → verificar Actions tab
-   [ ] Adicionar badge no README: [![CI](badge-url)](link)

---

### **GAP 8: Docker Production - Multi-Stage Builds**

**Problema:** Dockerfile mencionado, mas sem exemplo de multi-stage build

**Nest.js Dockerfile.prod:**

```dockerfile
# nest-backend/Dockerfile.prod
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
COPY prisma ./prisma/

RUN npm ci

COPY . .

RUN npx prisma generate
RUN npm run build

# Stage 2: Production
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/prisma ./prisma
COPY package*.json ./

EXPOSE 3001

CMD ["node", "dist/main"]
```

**Next.js Dockerfile.prod:**

```dockerfile
# next-frontend/Dockerfile.prod
# Stage 1: Dependencies
FROM node:20-alpine AS deps

WORKDIR /app

COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# Stage 3: Production
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/next.config.mjs ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

**docker-compose.prod.yml:**

```yaml
services:
    backend:
        build:
            context: ./nest-backend
            dockerfile: Dockerfile.prod
        environment:
            DATABASE_URL: postgresql://laravel:secret@postgres:5432/orionone
            NODE_ENV: production
        depends_on:
            - postgres
            - redis
            - meilisearch

    frontend:
        build:
            context: ./next-frontend
            dockerfile: Dockerfile.prod
        environment:
            NEXT_PUBLIC_API_URL: http://backend:3001
        depends_on:
            - backend

    postgres:
        # ... (mesmo do dev)

    redis:
        # ... (mesmo do dev)

    meilisearch:
        # ... (mesmo do dev)

    nginx:
        image: nginx:alpine
        ports:
            - "80:80"
        volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf:ro
        depends_on:
            - frontend
            - backend
```

**Solução:** Adicionar à Week 10 Day 1:

-   [ ] Criar Dockerfile.prod para backend (multi-stage)
-   [ ] Criar Dockerfile.prod para frontend (multi-stage)
-   [ ] Criar docker-compose.prod.yml
-   [ ] Criar nginx.conf (reverse proxy)
-   [ ] Testar build: `docker-compose -f docker-compose.prod.yml up`

---

### **GAP 9: Tailwind CSS Variables Migration**

**Problema:** Laravel tem CSS variables customizadas (--radius, --chart-1 a --chart-5) que precisam ser migradas

**Laravel app.css atual:**

```css
:root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --radius: 0.5rem;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
}

.dark {
    --background: 240 10% 3.9%;
    --chart-1: 220 70% 50%;
    /* ... */
}
```

**Next.js Migration:**

**OPÇÃO A (Recomendada): Copy-Paste CSS Variables**

```css
// next-frontend/app/globals.css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
    :root {
        /* COPIAR EXATAMENTE do Laravel app.css */
        --background: 0 0% 100%;
        --foreground: 240 10% 3.9%;
        /* ... todas as 30+ variables */
    }

    .dark {
        /* COPIAR dark mode variables */
    }
}

@layer base {
    * {
        @apply border-border;
    }
    body {
        @apply bg-background text-foreground;
    }
}
```

✅ **Vantagem:** 100% compatível, mesma aparência
✅ **Vantagem:** Shadcn-ui funcionará sem alterações

**OPÇÃO B: Usar tema Shadcn-ui padrão**

```bash
npx shadcn@latest init
# Escolher: new-york style, zinc base color
```

❌ **Desvantagem:** Aparência diferente do Laravel (precisa redesign)

**RECOMENDAÇÃO: OPÇÃO A** - Manter CSS variables existentes

**tailwind.config.ts (Next.js):**

```typescript
// COPIAR EXATAMENTE do Laravel tailwind.config.js
export default {
    darkMode: ["class"],
    content: [
        "./pages/**/*.{ts,tsx}",
        "./components/**/*.{ts,tsx}",
        "./app/**/*.{ts,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ["Figtree", ...defaultTheme.fontFamily.sans],
            },
            borderRadius: {
                lg: "var(--radius)",
                md: "calc(var(--radius) - 2px)",
                sm: "calc(var(--radius) - 4px)",
            },
            colors: {
                // COPIAR TODOS os colors do Laravel config
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                // ... 20+ colors
            },
        },
    },
    plugins: [require("tailwindcss-animate")],
};
```

**Solução:** Adicionar à Week 3 Day 1 (Next.js Setup):

-   [ ] Copiar `app.css` completo do Laravel → `globals.css`
-   [ ] Copiar `tailwind.config.js` → `tailwind.config.ts`
-   [ ] Verificar: Dark mode toggle funciona
-   [ ] Verificar: Chart colors idênticos (--chart-1 a --chart-5)

---

### **GAP 10: Shadcn Component Aliases - Path Mapping**

**Problema:** Laravel usa aliases `@/components`, `@/lib` que precisam ser configurados no Next.js

**Laravel jsconfig.json:**

```json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "@/*": ["resources/js/*"]
        }
    }
}
```

**Laravel components.json (Shadcn-vue):**

```json
{
    "aliases": {
        "components": "@/components",
        "utils": "@/lib/utils",
        "ui": "@/components/ui"
    }
}
```

**Next.js tsconfig.json:**

```json
{
    "compilerOptions": {
        "target": "ES2017",
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": true,
        "skipLibCheck": true,
        "strict": true,
        "noEmit": true,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "preserve",
        "incremental": true,
        "plugins": [
            {
                "name": "next"
            }
        ],
        "baseUrl": ".",
        "paths": {
            "@/*": ["./"],
            "@/components/*": ["./components/*"],
            "@/lib/*": ["./lib/*"],
            "@/hooks/*": ["./hooks/*"],
            "@/types/*": ["./types/*"]
        }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
}
```

**components.json (Next.js Shadcn-ui):**

```json
{
    "$schema": "https://ui.shadcn.com/schema.json",
    "style": "new-york",
    "rsc": true,
    "tsx": true,
    "tailwind": {
        "config": "tailwind.config.ts",
        "css": "app/globals.css",
        "baseColor": "zinc",
        "cssVariables": true
    },
    "aliases": {
        "components": "@/components",
        "utils": "@/lib/utils",
        "ui": "@/components/ui",
        "lib": "@/lib",
        "hooks": "@/hooks"
    }
}
```

**Solução:** Adicionar à Week 3 Day 1:

-   [ ] Configurar tsconfig.json com paths aliases
-   [ ] Criar components.json (npx shadcn@latest init)
-   [ ] Testar imports: `import { Button } from '@/components/ui/button'`

---

### **GAP 11: Docker Networking - Container Communication**

**Problema:** Next.js frontend precisa se comunicar com Nest.js backend via Docker network

**Laravel docker-compose.yml atual:**

-   `orionone-app` (PHP) → comunica com `orionone-db` via hostname
-   `orionone-frontend` (Vite) → apenas dev server, não faz API calls

**Nest.js + Next.js networking:**

**docker-compose.yml (adaptado):**

```yaml
services:
    # Nest.js Backend API
    backend:
        build:
            context: ./nest-backend
            dockerfile: Dockerfile
        container_name: orionone_backend
        restart: unless-stopped
        ports:
            - "3001:3001"
        environment:
            DATABASE_URL: postgresql://laravel:secret@postgres:5432/orionone
            REDIS_HOST: redis
            MEILISEARCH_HOST: http://meilisearch:7700
            JWT_SECRET: ${JWT_SECRET}
            NODE_ENV: development
        depends_on:
            postgres:
                condition: service_healthy
            redis:
                condition: service_started
        networks:
            - orionone_network
        healthcheck:
            test: ["CMD", "wget", "--spider", "http://localhost:3001/health"]
            interval: 30s
            timeout: 10s
            retries: 3

    # Next.js Frontend
    frontend:
        build:
            context: ./next-frontend
            dockerfile: Dockerfile.dev
        container_name: orionone_frontend
        restart: unless-stopped
        ports:
            - "3000:3000"
        environment:
            # CRITICAL: Use container hostname, not localhost!
            NEXT_PUBLIC_API_URL: http://backend:3001
            # For browser requests: use host machine URL
            NEXT_PUBLIC_API_URL_BROWSER: http://localhost:3001
        depends_on:
            backend:
                condition: service_healthy
        networks:
            - orionone_network
        volumes:
            - ./next-frontend:/app
            - /app/node_modules
            - /app/.next

    # PostgreSQL (MANTER IGUAL)
    postgres:
        image: postgres:16-alpine
        container_name: orionone_postgres
        # ... (sem alterações)

    # Redis (MANTER IGUAL)
    redis:
        image: redis:7-alpine
        # ...

    # Meilisearch (MANTER IGUAL)
    meilisearch:
        image: getmeili/meilisearch:v1.12
        # ...

    # Nginx (NOVO - Reverse Proxy)
    nginx:
        image: nginx:alpine
        container_name: orionone_nginx
        restart: unless-stopped
        ports:
            - "80:80"
        volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf:ro
        depends_on:
            - frontend
            - backend
        networks:
            - orionone_network

networks:
    orionone_network:
        driver: bridge

volumes:
    orionone_pgdata:
    orionone_redisdata:
    orionone_meilisearch:
```

**nginx.conf (Reverse Proxy):**

```nginx
events {
  worker_connections 1024;
}

http {
  upstream backend {
    server backend:3001;
  }

  upstream frontend {
    server frontend:3000;
  }

  server {
    listen 80;
    server_name localhost;

    # Frontend (Next.js)
    location / {
      proxy_pass http://frontend;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      proxy_set_header Host $host;
      proxy_cache_bypass $http_upgrade;
    }

    # Backend API (Nest.js)
    location /api {
      rewrite ^/api/(.*) /$1 break;
      proxy_pass http://backend;
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
}
```

**Solução:** Adicionar à Week 0 Day 3:

-   [ ] Adaptar docker-compose.yml (backend + frontend services)
-   [ ] Criar nginx.conf (reverse proxy)
-   [ ] Testar networking: frontend → http://backend:3001
-   [ ] Testar browser: http://localhost/api → backend

---

### **GAP 12: Nest.js Health Check Endpoint**

**Problema:** Docker healthcheck precisa de endpoint `/health`

**Solução:**

```typescript
// nest-backend/src/health/health.controller.ts
import { Controller, Get } from "@nestjs/common";
import { ApiTags } from "@nestjs/swagger";

@ApiTags("health")
@Controller("health")
export class HealthController {
    @Get()
    check() {
        return {
            status: "ok",
            timestamp: new Date().toISOString(),
            uptime: process.uptime(),
        };
    }
}
```

**Adicionar ao AppModule:**

```typescript
@Module({
    imports: [
        /* ... */
    ],
    controllers: [HealthController],
})
export class AppModule {}
```

**Solução:** Adicionar à Week 0 Day 4:

-   [ ] Criar HealthController
-   [ ] Testar: curl http://localhost:3001/health
-   [ ] Verificar Docker healthcheck: `docker inspect orionone_backend`

---

### **GAP 13: TypeScript Strict Mode Configuration**

**Problema:** Part 4 menciona `--strict` mas sem explicar impacto

**Nest.js tsconfig.json (strict):**

```json
{
    "compilerOptions": {
        "module": "commonjs",
        "declaration": true,
        "removeComments": true,
        "emitDecoratorMetadata": true,
        "experimentalDecorators": true,
        "allowSyntheticDefaultImports": true,
        "target": "ES2021",
        "sourceMap": true,
        "outDir": "./dist",
        "baseUrl": "./",
        "incremental": true,
        "skipLibCheck": true,
        "strictNullChecks": true,
        "noImplicitAny": true,
        "strictBindCallApply": true,
        "forceConsistentCasingInFileNames": true,
        "noFallthroughCasesInSwitch": true,
        "strict": true
    }
}
```

**Impacto do Strict Mode:**

-   ❌ `let user;` → ❌ ERROR: Variable implicitly has 'any' type
-   ✅ `let user: User;` → ✅ OK
-   ❌ `if (user.name)` → ❌ ERROR: Object is possibly 'null'
-   ✅ `if (user?.name)` → ✅ OK (optional chaining)

**Solução:** Adicionar à Week 0 Day 2:

-   [ ] Criar tsconfig.json com strict: true
-   [ ] Aprender TypeScript strict patterns:
    -   Optional chaining: `user?.name`
    -   Nullish coalescing: `name ?? 'Unknown'`
    -   Type guards: `if (typeof x === 'string')`
    -   Non-null assertion: `user!.name` (usar com cuidado!)

---

### **GAP 14: Error Handling Strategy**

**Problema:** Plano não define estratégia de error handling global

**Nest.js Exception Filters:**

```typescript
// nest-backend/src/common/filters/http-exception.filter.ts
import {
    ExceptionFilter,
    Catch,
    ArgumentsHost,
    HttpException,
    HttpStatus,
} from "@nestjs/common";
import { Request, Response } from "express";

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
    catch(exception: unknown, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const request = ctx.getRequest<Request>();

        const status =
            exception instanceof HttpException
                ? exception.getStatus()
                : HttpStatus.INTERNAL_SERVER_ERROR;

        const message =
            exception instanceof HttpException
                ? exception.getResponse()
                : "Internal server error";

        // Log error
        console.error({
            timestamp: new Date().toISOString(),
            path: request.url,
            method: request.method,
            status,
            message,
            stack: exception instanceof Error ? exception.stack : undefined,
        });

        response.status(status).json({
            statusCode: status,
            timestamp: new Date().toISOString(),
            path: request.url,
            message:
                typeof message === "string"
                    ? message
                    : (message as any).message,
        });
    }
}
```

**Registrar globalmente:**

```typescript
// main.ts
import { AllExceptionsFilter } from "./common/filters/http-exception.filter";

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    app.useGlobalFilters(new AllExceptionsFilter());

    await app.listen(3001);
}
```

**Next.js Error Boundary:**

```typescript
// next-frontend/app/error.tsx
"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        console.error(error);
    }, [error]);

    return (
        <div className="flex min-h-screen flex-col items-center justify-center">
            <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
            <p className="text-muted-foreground mb-6">{error.message}</p>
            <Button onClick={reset}>Try again</Button>
        </div>
    );
}
```

**Solução:** Adicionar à Week 1 Day 2:

-   [ ] Criar AllExceptionsFilter (Nest.js)
-   [ ] Registrar em main.ts
-   [ ] Criar error.tsx (Next.js)
-   [ ] Testar: throw new Error('test') → ver error UI

---

### **GAP 15: Logging Strategy - Winston Configuration**

**Problema:** Timeline menciona Winston, mas sem configuração

**Nest.js Winston Setup:**

```bash
npm install nest-winston winston
```

```typescript
// nest-backend/src/logger/logger.module.ts
import { Module } from "@nestjs/common";
import { WinstonModule } from "nest-winston";
import * as winston from "winston";

@Module({
    imports: [
        WinstonModule.forRoot({
            transports: [
                new winston.transports.Console({
                    format: winston.format.combine(
                        winston.format.timestamp(),
                        winston.format.colorize(),
                        winston.format.printf(
                            ({ timestamp, level, message, context }) => {
                                return `${timestamp} [${context}] ${level}: ${message}`;
                            }
                        )
                    ),
                }),
                new winston.transports.File({
                    filename: "logs/error.log",
                    level: "error",
                    format: winston.format.json(),
                }),
                new winston.transports.File({
                    filename: "logs/combined.log",
                    format: winston.format.json(),
                }),
            ],
        }),
    ],
})
export class LoggerModule {}
```

**Usar em Services:**

```typescript
import { Inject, Injectable } from "@nestjs/common";
import { WINSTON_MODULE_PROVIDER } from "nest-winston";
import { Logger } from "winston";

@Injectable()
export class TicketsService {
    constructor(
        @Inject(WINSTON_MODULE_PROVIDER)
        private readonly logger: Logger
    ) {}

    async create(dto: CreateTicketDto) {
        this.logger.info("Creating ticket", { context: "TicketsService", dto });
        // ...
    }
}
```

**Solução:** Adicionar à Week 8 Day 4:

-   [ ] Instalar nest-winston
-   [ ] Criar LoggerModule
-   [ ] Configurar transports (console + file)
-   [ ] Adicionar logging em Services críticos

---

### **GAP 16: CORS Configuration - Cross-Origin Requests**

**Problema:** Next.js (localhost:3000) precisa fazer requests para Nest.js (localhost:3001)

**Nest.js CORS:**

```typescript
// main.ts
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    // Enable CORS
    app.enableCors({
        origin: [
            "http://localhost:3000", // Next.js dev
            "http://localhost", // Nginx
            "http://frontend:3000", // Docker
        ],
        credentials: true,
        methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allowedHeaders: ["Content-Type", "Authorization"],
    });

    await app.listen(3001);
}
bootstrap();
```

**Solução:** Adicionar à Week 0 Day 4:

-   [ ] Configurar CORS em main.ts
-   [ ] Testar cross-origin: http://localhost:3000 → http://localhost:3001
-   [ ] Verificar credentials: cookies/JWT funcionam

---

### **GAP 17: WebSocket Real-Time (Optional but Recommended)**

**Problema:** Notifications mencionadas mas sem estratégia de real-time

**Laravel Atual:** Polling (fetch notificações a cada 30s)

**Nest.js WebSocket (RECOMENDADO):**

```bash
npm install @nestjs/websockets @nestjs/platform-socket.io
npm install socket.io
```

```typescript
// nest-backend/src/notifications/notifications.gateway.ts
import {
    WebSocketGateway,
    WebSocketServer,
    SubscribeMessage,
    OnGatewayConnection,
} from "@nestjs/websockets";
import { Server, Socket } from "socket.io";

@WebSocketGateway({
    cors: {
        origin: "http://localhost:3000",
        credentials: true,
    },
})
export class NotificationsGateway implements OnGatewayConnection {
    @WebSocketServer()
    server: Server;

    handleConnection(client: Socket) {
        console.log(`Client connected: ${client.id}`);
    }

    // Emit notification to specific user
    sendNotification(userId: string, notification: any) {
        this.server.to(userId).emit("notification", notification);
    }

    @SubscribeMessage("join")
    handleJoin(client: Socket, userId: string) {
        client.join(userId);
        return { event: "joined", data: userId };
    }
}
```

**Next.js Client:**

```typescript
// next-frontend/hooks/use-notifications.ts
import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

export function useNotifications(userId: string) {
    const [socket, setSocket] = useState<Socket | null>(null);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        const newSocket = io("http://localhost:3001");

        newSocket.on("connect", () => {
            newSocket.emit("join", userId);
        });

        newSocket.on("notification", (notification) => {
            setNotifications((prev) => [notification, ...prev]);
        });

        setSocket(newSocket);

        return () => {
            newSocket.close();
        };
    }, [userId]);

    return { notifications };
}
```

**Solução (OPCIONAL):** Adicionar à Week 8 Day 3:

-   [ ] Instalar @nestjs/websockets + socket.io
-   [ ] Criar NotificationsGateway
-   [ ] Criar useNotifications hook (Next.js)
-   [ ] Testar: criar ticket → assignee recebe notificação em real-time

**Alternativa:** Manter polling (mais simples, Week 8 original)

---

## 📋 CHECKLIST DE CORREÇÕES

### **Immediate Fixes (Adicionar aos Docs):**

**Part 1: MIGRATION-PART-1-SETUP.md**

-   [ ] Adicionar seção: "Environment Variables Migration"
-   [ ] Adicionar seção: "Storage Strategy (Local vs S3)"
-   [ ] Adicionar seção: "Email Configuration (Mailpit)"

**Part 2: MIGRATION-PART-2-BACKEND.md**

-   [ ] Adicionar: Decisão sobre Triggers (Application vs DB)
-   [ ] Adicionar: Prisma seed completo (32 permissions)
-   [ ] Adicionar: Views migration strategy

**Part 3: MIGRATION-PART-3-FRONTEND.md**

-   [ ] Adicionar: Static file serving (uploads)
-   [ ] Adicionar: Environment variables (.env.local)

**Part 4: MIGRATION-PART-4-TIMELINE.md**

-   [ ] Week 0 Day 2: Adicionar step "Create .env files"
-   [ ] Week 0 Day 3: Adicionar step "Configure Docker networking + Nginx"
-   [ ] Week 0 Day 4: Adicionar step "Create health check endpoint"
-   [ ] Week 0 Day 4: Adicionar step "Configure CORS"
-   [ ] Week 1 Day 1: Adicionar step "Decide Triggers strategy"
-   [ ] Week 1 Day 1: Adicionar step "Create complete seed.ts (32 permissions)"
-   [ ] Week 1 Day 2: Adicionar step "Create AllExceptionsFilter"
-   [ ] Week 1 Day 5: Adicionar step "Setup local storage"
-   [ ] Week 3 Day 1: Adicionar step "Copy Tailwind CSS variables"
-   [ ] Week 3 Day 1: Adicionar step "Configure TypeScript path aliases"
-   [ ] Week 8 Day 2: Adicionar step "Configure Mailpit + @nestjs-modules/mailer"
-   [ ] Week 8 Day 3: Adicionar step "(Optional) WebSocket notifications"
-   [ ] Week 8 Day 4: Adicionar step "Configure Winston logging"
-   [ ] Week 9: Adicionar detalhes de estrutura de testes
-   [ ] Week 10 Day 1: Adicionar multi-stage Dockerfiles
-   [ ] Week 10 Day 2: Adicionar GitHub Actions workflow completo

---

## 🎯 RECOMENDAÇÕES FINAIS

### **1. Prioridade CRÍTICA (Week 0 - Setup):**

-   ✅ Criar .env files (DATABASE_URL, JWT_SECRET, API URLs)
-   ✅ Configurar Docker networking + Nginx reverse proxy
-   ✅ Copiar Tailwind CSS variables (app.css → globals.css)
-   ✅ Configurar TypeScript path aliases (@/components, @/lib)
-   ✅ Criar health check endpoint (/health)
-   ✅ Configurar CORS (Next.js → Nest.js)

### **2. Prioridade Alta (Week 1-2):**

-   ✅ Decidir estratégia de Triggers (recomendação: Application Layer)
-   ✅ Criar seed.ts completo com 32 permissions
-   ✅ Criar AllExceptionsFilter (error handling global)
-   ✅ Configurar local storage para uploads
-   ✅ Documentar estratégia de Views (manter no DB)

### **3. Prioridade Média (Week 3-8):**

-   ⚠️ Adicionar Mailpit ao docker-compose (Week 8)
-   ⚠️ Configurar Winston logging (Week 8)
-   ⚠️ Criar estrutura de testes (Week 9)
-   ⚠️ WebSocket notifications (OPCIONAL - Week 8)

### **4. Prioridade Baixa (Week 9-10):**

-   💡 Multi-stage Dockerfiles (production)
-   💡 GitHub Actions workflow completo
-   💡 MinIO/S3 migration (produção)
-   💡 Codecov integration

---

## ✅ CONCLUSÃO

**Plano Original:** SÓLIDO - 90% completo
**Gaps Identificados:** 17 total (8 originais + 9 novos)
**Gaps Críticos:** 6 (Week 0 setup)
**Impact:** MÉDIO - 6 gaps críticos devem ser resolvidos na Week 0
**Ação:** Atualizar Migration Parts 1-4 com todos os gaps + iniciar Week 0

**Novos Gaps Encontrados:**

-   GAP 9: Tailwind CSS variables migration ⚠️ CRÍTICO
-   GAP 10: TypeScript path aliases ⚠️ CRÍTICO
-   GAP 11: Docker networking + Nginx ⚠️ CRÍTICO
-   GAP 12: Health check endpoint ⚠️ CRÍTICO
-   GAP 13: TypeScript strict mode 📚 EDUCACIONAL
-   GAP 14: Error handling strategy ⚠️ IMPORTANTE
-   GAP 15: Winston logging configuration ⚠️ IMPORTANTE
-   GAP 16: CORS configuration ⚠️ CRÍTICO
-   GAP 17: WebSocket real-time 💡 OPCIONAL

**Status:** ✅ PRONTO PARA MIGRAÇÃO após atualizar docs com 17 gaps
