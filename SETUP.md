# Setup Rápido - OrionOne

## Instalado e Configurado

### 1. Docker (5 containers rodando)

-   `orionone-app` - Laravel + PHP 8.2-FPM
-   `orionone-frontend` - Vite dev server (porta 5173)
-   `orionone-nginx` - Nginx (porta 8888)
-   `orionone-postgres` - PostgreSQL 16
-   `orionone-redis` - Redis 7

**Acesso:**

-   Laravel: http://localhost:8888
-   Vite HMR: http://localhost:5173

### 2. Ferramentas de Desenvolvimento

#### Larastan (PHPStan + Laravel)

```bash
docker-compose exec orionone-app ./vendor/bin/phpstan analyse
```

#### Laravel Pint (Code Style)

```bash
docker-compose exec orionone-app ./vendor/bin/pint
```

#### PHPUnit (Testes)

```bash
docker-compose exec orionone-app php artisan test
```

#### L5-Swagger (API Docs)

Instalado, aguardando configuração quando criar controllers de API.

### 3. Estrutura de Pastas Criada

```
app/
├── Actions/
│   ├── Tickets/        # Operações atómicas de tickets
│   └── Comments/       # Operações atómicas de comments
├── Services/           # Lógica de negócio e orquestração
├── Policies/           # Autorização (Gates)
├── Observers/          # Hooks de lifecycle de models
├── Notifications/      # Email, Slack, Database notifications
├── Events/             # Domain events
└── Listeners/          # Event handlers
```

### 4. Base de Dados

Migrations executadas:

-   `users` table
-   `cache` table
-   `jobs` table
-   `telescope_entries` table

### 5. Documentação Criada

-   `docs/architecture.md` - Arquitetura da aplicação (MVC + Services + Actions)
-   `docs/database-schema.md` - Schema completo da base de dados
-   `docs/requirements.md` - Requisitos funcionais e não-funcionais
-   `docs/development-guide.md` - Workflow TDD e ciclo de desenvolvimento
-   `docs/development-planning.md` - Roadmap, sprints e metas **NOVO**
-   `docs/business-model.md` - Modelo de negócio, SWOT, financials **NOVO**
-   `docs/tech-stack.md` - Stack completo de tecnologias (FASE 1) **ATUALIZADO**
-   `docs/implementation-checklist.md` - Guia passo a passo com código **NOVO**

### 6. Bibliotecas Instaladas - FASE 1 COMPLETO

#### Backend (Composer)

**Arquitetura Moderna:**

-   **Laravel 12** - Framework PHP
-   **Spatie Laravel Data** - DTOs type-safe + validação automática **NOVO**
-   **Laravel Actions** - Lógica reutilizável (Controller/Job/Command) **NOVO**
-   **Query Builder** - Filtros automáticos via URL **NOVO**

**Segurança & Audit:**

-   **Spatie Permission** - Roles & permissions (RBAC)
-   **Spatie Activity Log** - Audit trail
-   **Laravel Sanctum** - API authentication

**File Processing:**

-   **Intervention Image** - Processamento de imagens (avatars)
-   **Laravel DomPDF** - Geração de PDFs (relatórios)
-   **Maatwebsite Excel** - Exportação Excel/CSV
-   **AWS S3 Flysystem** - Storage cloud (produção)

**Developer Experience:**

-   **Laravel IDE Helper** - Autocomplete perfeito (VSCode, PHPStorm) **NOVO**
-   **Laravel Telescope** - Debugging & monitoring
-   **L5-Swagger** - API documentation
-   **PHPStan/Larastan** - Static analysis
-   **Laravel Pint** - Code formatter

#### Frontend (NPM)

**Core:**

-   **Vue 3** - Framework JavaScript
-   **Inertia.js** - SPA without API
-   **Tailwind CSS** - Utility-first CSS
-   **Vite 7** - Build tool

**UI Components (Shadcn-vue):** **NOVO**

-   **Radix Vue** - Primitives acessíveis
-   **Lucide Icons** - 600+ ícones modernos
-   **CVA** - Variantes de componentes type-safe
-   **Tailwind Merge** - Merge classes sem conflitos

**Utilities:**

-   **@iconify/vue** - 150k+ ícones universais **NOVO**
-   **@vueuse/core** - 200+ composables úteis
-   **@headlessui/vue** - Componentes acessíveis
-   **@inertiajs/progress** - Loading bar automático **NOVO**
-   **Vee-Validate** - Forms complexos **NOVO**

**Charts & Rich Text:**

-   **Heroicons** - Ícones SVG oficiais
-   **Chart.js + Vue-ChartJS** - Gráficos para dashboards
-   **Quill Editor** - WYSIWYG editor
-   **Marked** - Parser Markdown
-   **DOMPurify** - Sanitização XSS

**[Stack Completo →](docs/tech-stack.md)**

---

## Próximos Passos

### 1. Configuração Inicial de Packages  **IMPORTANTE**

```bash
# Publicar configs dos packages instalados
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"
php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider"
php artisan vendor:publish --provider="Barryvdh\DomPDF\ServiceProvider"
php artisan vendor:publish --provider="L5Swagger\L5SwaggerServiceProvider"

# Rodar migrations adicionais
php artisan migrate
```

### 2. Criar Seeder de Roles & Permissions

Criar `database/seeders/RolePermissionSeeder.php`:

```php
public function run()
{
    // Roles
    Role::create(['name' => 'admin']);
    Role::create(['name' => 'agent']);
    Role::create(['name' => 'user']);

    // Permissions
    Permission::create(['name' => 'view-all-tickets']);
    Permission::create(['name' => 'create-ticket']);
    Permission::create(['name' => 'update-ticket']);
    Permission::create(['name' => 'delete-ticket']);
    Permission::create(['name' => 'assign-ticket']);
    Permission::create(['name' => 'manage-teams']);

    // Assign to roles...
}
```

### 3. Começar Desenvolvimento (Sprint 1: Auth & Users)

#### A. Melhorar Profile & Avatar Upload

```bash
# UserController já existe (Breeze), adicionar avatar upload
php artisan make:request UpdateProfileRequest
```

#### B. Criar Tests

```bash
php artisan make:test UserTest
php artisan make:test UserPolicyTest
```

### 4. Próximos Sprints (Ver development-planning.md)

-   **Sprint 2 (18 Nov):** Tickets Core
-   **Sprint 3 (02 Dez):** Colaboração (Comments, Teams, Notifications)
-   **Sprint 4 (16 Dez):** Knowledge Base
-   **Sprint 5 (30 Dez):** Dashboard & Reports
-   **Sprint 6 (13 Jan):** Polish & Deploy

8. **RF08 - Dashboard** (2 dias)

    - Estatísticas
    - Gráficos (Chart.js)

9. **RF09 - Notifications** (1-2 dias)

    - Email (Mailtrap para dev)
    - In-app notifications

10. **RF10 - Activity Log** (1 dia)
    - Spatie Activity Log
    - Audit trail

### 3. Testes (Contínuo)

Para cada feature, criar:

-   **Feature Test** (teste de integração HTTP)
-   **Unit Test** (lógica isolada)

**Exemplo:**

```bash
php artisan make:test TicketTest          # Feature
php artisan make:test TicketServiceTest --unit  # Unit
```

# Instalar dependências
docker-compose exec orionone-app composer install
docker-compose exec orionone-frontend npm install --legacy-peer-deps

# Configurar ambiente
docker-compose exec orionone-app cp .env.example .env
docker-compose exec orionone-app php artisan key:generate

# Base de dados
docker-compose exec orionone-app php artisan migrate --seed
```
resources/js/
├── Components/
│   ├── Tickets/
│   │   ├── TicketCard.vue
│   │   ├── TicketForm.vue
│   │   └── TicketList.vue
│   ├── Dashboard/
│   │   ├── StatsCard.vue
│   │   └── RecentTickets.vue
│   └── Shared/
│       ├── Sidebar.vue
│       ├── Navbar.vue
│       └── Modal.vue
├── Pages/
│   ├── Tickets/
│   │   ├── Index.vue
│   │   ├── Show.vue
│   │   └── Create.vue
│   ├── Dashboard.vue
│   └── Auth/
│       ├── Login.vue
│       └── Register.vue
└── Layouts/
    ├── AppLayout.vue
    └── GuestLayout.vue
```

## Timeline Sugerida (2.5 meses)

### Semana 1-2: Setup + Authentication + Tickets

-   Docker e ambiente (concluído)
-   Models base + migrations
-   Authentication (Breeze + roles)
-   CRUD de tickets básico

### Semana 3-4: Core Features

-   Comments
-   Teams
-   Assignment (manual + auto)
-   SLA básico

### Semana 5-6: Knowledge Base + Dashboard

-   CRUD de artigos
-   Categorização e busca
-   Dashboard com estatísticas
-   Gráficos

### Semana 7-8: Polimento + Testes

-   Notificações
-   Activity log
-   Testes unitários e de integração
-   Code coverage >70%

### Semana 9-10: Documentação + Deploy

-   Swagger API docs completa
-   README atualizado
-   Deploy (VPS/Cloud)
-   Apresentação final

## Comandos Rápidos

**Aceder:**

-   Laravel: http://localhost:8888
-   Vite HMR: http://localhost:5173

---

## Documentação Completa

Para informação detalhada sobre o setup, consultar:

-   **[Setup Changelog](docs/setup-changelog.md)** - Histórico completo de instalação, pacotes, configurações
-   **[Commands Reference](docs/commands-reference.md)** - Todos os comandos (Git, Docker, Laravel, NPM)
-   **[Docker Guide](docs/docker-guide.md)** - Guia Docker para iniciantes
-   **[Tech Stack](docs/tech-stack.md)** - Stack tecnológica completa

```bash
# PC novo
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne
docker-compose up -d
docker-compose exec orionone-app composer install
docker-compose run --rm orionone-frontend npm install --legacy-peer-deps
docker-compose exec orionone-app php artisan migrate
```

## Documentação de Referência

## Próximos Passos

## Checklist Atual

1. **Sprint 1:** Auth & Users (Roles, Permissions, Seeders)
2. **Sprint 2:** Tickets Core (CRUD, Status, Priority)
3. **Sprint 3:** Colaboração (Comments, Teams, Notifications)
4. **Sprint 4:** Knowledge Base
5. **Sprint 5:** Dashboard & Reports
6. **Sprint 6:** Polish & Deploy

---

**Status:** Ambiente 100% configurado, pronto para desenvolvimento!
