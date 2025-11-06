# OrionOne

**Modern IT Service Management Platform**

Uma plataforma completa de gestão de tickets de suporte técnico, desenvolvida com Laravel 11 e Vue 3, focada em simplicidade, performance e experiência do utilizador.

---

## Sobre o Projeto

OrionOne é um sistema ITSM (IT Service Management) desenvolvido como projeto final do CET - Técnico especialista em tecnologias e programação de sistemas de informação. inspirado em soluções enterprise como ServiceNow e Jira Service Desk, o OrionOne oferece uma alternativa moderna, ágil e intuitiva para gestão de suporte técnico.

### Principais Características

**Gestão de Tickets**

-   Sistema completo de criação, atribuição e acompanhamento de tickets
-   Estados configuráveis (Open, In Progress, Resolved, Closed)
-   Priorização automática e manual
-   SLA tracking com alertas de violação

**Equipas & Colaboração**

-   Organização por equipas especializadas
-   Sistema de comentários públicos e internos
-   Atribuição automática baseada em regras
-   Notificações por email em tempo real

**Knowledge Base**

-   Base de conhecimento para self-service
-   Sistema de categorias e pesquisa
-   Métricas de utilidade dos artigos
-   Interface de criação simples para agents

**Dashboard & Métricas**

-   Visão geral de tickets por estado
-   Análise de performance de SLA
-   Estatísticas por equipa e agent
-   Tracking de tendências

---

## Stack Tecnológica

### Backend

-   **Laravel 11** - Framework PHP moderno
-   **PostgreSQL 16** - Base de dados relacional
-   **Redis 7** - Cache e queue management
-   **Eloquent ORM** - Object-Relational Mapping

### Frontend

-   **Vue 3** - Progressive JavaScript framework
-   **Inertia.js** - Monolith SPA approach
-   **Tailwind CSS** - Utility-first CSS framework
-   **Vite** - Next generation frontend tooling

### Packages Principais

```
spatie/laravel-permission     # Role & Permission management
spatie/laravel-activitylog    # Audit trail
laravel/breeze               # Authentication scaffolding
laravel/sanctum              # API authentication
```

---

## Requisitos

-   PHP 8.2 ou superior
-   Composer 2.x
-   Node.js 20 LTS
-   PostgreSQL 16
-   Redis 7.x

---

## Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne
```

### 2. Backend Setup

```bash
# Instalar dependências
composer install

# Configurar ambiente
cp .env.example .env
php artisan key:generate

# Configurar base de dados no .env
# DB_CONNECTION=pgsql
# DB_DATABASE=orionone
# DB_USERNAME=laravel
# DB_PASSWORD=secret

# Executar migrations
php artisan migrate

# Popular com dados de teste
php artisan db:seed
```

### 3. Frontend Setup

```bash
# Instalar dependências
npm install

# Build para desenvolvimento
npm run dev
```

### 4. Iniciar Aplicação

```bash
# Terminal 1: Laravel
php artisan serve

# Terminal 2: Vite
npm run dev

# Aceder em: http://orionone.test:8888/
```

---

## Docker Setup (Alternativa)

```bash
# Iniciar containers
docker-compose up -d

# Setup inicial
docker-compose exec app composer install
docker-compose exec app cp .env.example .env
docker-compose exec app php artisan key:generate
docker-compose exec app php artisan migrate --seed

# Aceder em: http://orionone.test:8888/
```

---

## Utilizadores de Teste

Após executar `php artisan db:seed`:

| Role  | Email               | Password |
| ----- | ------------------- | -------- |
| Admin | admin@orionone.test | password |
| Agent | john@orionone.test  | password |
| Agent | jane@orionone.test  | password |
| User  | user1@orionone.test | password |

---

## Estrutura do Projeto

```
OrionOne/
├── app/
│   │
│   ├── Http/
│   │   ├── Controllers/           # Request handling (5-20 linhas cada)
│   │   │   ├── TicketController.php
│   │   │   ├── CommentController.php
│   │   │   ├── TeamController.php
│   │   │   ├── ArticleController.php
│   │   │   └── DashboardController.php
│   │   │
│   │   ├── Requests/              # Validation isolada
│   │   │   ├── StoreTicketRequest.php
│   │   │   ├── UpdateTicketRequest.php
│   │   │   ├── StoreCommentRequest.php
│   │   │   └── StoreArticleRequest.php
│   │   │
│   │   └── Middleware/
│   │       └── EnsureUserHasTeam.php
│   │
│   ├── Services/                  # Business Logic Layer
│   │   ├── TicketService.php      # CRUD + regras de negócio
│   │   ├── AssignmentService.php  # Lógica de atribuição
│   │   ├── SLAService.php         # Cálculo de SLA
│   │   ├── NotificationService.php # Orquestração de notificações
│   │   └── SearchService.php      # Lógica de pesquisa
│   │
│   ├── Actions/                   # Single Responsibility Operations
│   │   ├── Tickets/
│   │   │   ├── CreateTicketAction.php
│   │   │   ├── AssignTicketAction.php
│   │   │   ├── ResolveTicketAction.php
│   │   │   ├── CloseTicketAction.php
│   │   │   └── EscalateTicketAction.php
│   │   │
│   │   ├── Comments/
│   │   │   └── AddCommentAction.php
│   │   │
│   │   └── Articles/
│   │       ├── PublishArticleAction.php
│   │       └── IncrementViewsAction.php
│   │
│   ├── Models/                    # Eloquent Models
│   │   ├── Ticket.php
│   │   ├── Comment.php
│   │   ├── Team.php
│   │   ├── User.php
│   │   ├── Article.php
│   │   └── Category.php
│   │
│   ├── Policies/                  # Authorization
│   │   ├── TicketPolicy.php
│   │   ├── CommentPolicy.php
│   │   └── ArticlePolicy.php
│   │
│   ├── Observers/                 # Model Hooks
│   │   ├── TicketObserver.php     # Auto-generate ticket_number, etc
│   │   └── CommentObserver.php
│   │
│   ├── Notifications/             # Email/Slack/Database
│   │   ├── TicketCreated.php
│   │   ├── TicketAssigned.php
│   │   ├── TicketResolved.php
│   │   ├── CommentAdded.php
│   │   └── SLABreachWarning.php
│   │
│   ├── Events/                    # Domain Events
│   │   ├── TicketCreated.php
│   │   ├── TicketResolved.php
│   │   └── SLABreached.php
│   │
│   ├── Listeners/                 # Event Handlers
│   │   ├── SendTicketCreatedNotification.php
│   │   ├── LogTicketActivity.php
│   │   └── UpdateTeamStatistics.php
│   │
│   └── Jobs/                      # Async Tasks
│       ├── CheckSLADeadlines.php
│       ├── SendDailyReport.php
│       └── CleanupOldTickets.php
│
├── database/
│   ├── migrations/
│   ├── seeders/
│   └── factories/
│
├── resources/
│   ├── js/
│   │   ├── Pages/                 # Inertia Pages
│   │   │   ├── Dashboard.vue
│   │   │   ├── Tickets/
│   │   │   │   ├── Index.vue
│   │   │   │   ├── Show.vue
│   │   │   │   ├── Create.vue
│   │   │   │   └── Edit.vue
│   │   │   ├── Teams/
│   │   │   ├── Articles/
│   │   │   └── Reports/
│   │   │
│   │   ├── Components/            # Reusable Vue Components
│   │   │   ├── Layout/
│   │   │   │   ├── AppLayout.vue
│   │   │   │   ├── Sidebar.vue
│   │   │   │   └── Navbar.vue
│   │   │   ├── Tickets/
│   │   │   │   ├── TicketCard.vue
│   │   │   │   ├── TicketList.vue
│   │   │   │   ├── StatusBadge.vue
│   │   │   │   └── PriorityBadge.vue
│   │   │   ├── Comments/
│   │   │   │   ├── CommentList.vue
│   │   │   │   └── CommentForm.vue
│   │   │   └── Shared/
│   │   │       ├── Button.vue
│   │   │       ├── Modal.vue
│   │   │       ├── Dropdown.vue
│   │   │       └── SearchBar.vue
│   │   │
│   │   ├── Composables/           # Vue 3 Composables
│   │   │   ├── useTickets.js
│   │   │   ├── usePermissions.js
│   │   │   └── useFilters.js
│   │   │
│   │   └── Utils/
│   │       ├── helpers.js
│   │       └── formatters.js
│   │
│   └── css/
│       └── app.css
│
└── tests/
    ├── Feature/
    │   ├── TicketManagementTest.php
    │   ├── CommentSystemTest.php
    │   └── SLATrackingTest.php
    │
    └── Unit/
        ├── Services/
        │   ├── TicketServiceTest.php
        │   └── AssignmentServiceTest.php
        │
        └── Actions/
            └── CreateTicketActionTest.php
```

---

## Funcionalidades Implementadas

### MVP (Fase 1)

-   [x] Autenticação e autorização multi-role
-   [x] CRUD completo de tickets
-   [x] Sistema de comentários
-   [x] Gestão de equipas
-   [x] Atribuição automática de tickets
-   [x] SLA tracking básico
-   [x] Knowledge base com pesquisa
-   [x] Dashboard com métricas
-   [x] Notificações por email
-   [x] Activity log (auditoria)

### Em Desenvolvimento

-   [ ] Real-time updates via WebSockets
-   [ ] Anexos de ficheiros
-   [ ] Relatórios avançados
-   [ ] Search engine (Meilisearch)
-   [ ] API RESTful

### Roadmap Futuro

-   [ ] Multi-tenancy
-   [ ] Workflows configuráveis
-   [ ] Integração com email
-   [ ] Mobile app
-   [ ] Sistema de aprovações

---

## Modelo de Dados

### Entidades Principais

**Users**
Utilizadores do sistema com roles (Admin, Agent, User)

**Tickets**
Pedidos de suporte com estados, prioridades e SLA tracking

**Comments**
Comunicação sobre tickets (pública ou interna)

**Teams**
Grupos de agents especializados

**Articles**
Conteúdo da knowledge base

**Categories**
Organização de artigos

Para diagrama detalhado: [docs/database-schema.md](docs/database-schema.md)

---

## Testes

```bash
# Executar suite de testes
php artisan test

# Com cobertura
php artisan test --coverage

# Testes específicos
php artisan test --filter TicketTest
```

---

## Deployment

### Produção

```bash
# Build assets
npm run build

# Optimize Laravel
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Migrations em produção
php artisan migrate --force
```

### Ambiente Recomendado

-   PHP 8.2 FPM
-   Nginx
-   PostgreSQL 16
-   Redis
-   Supervisor (para queues)

---

## Segurança

-   Autenticação via Laravel Sanctum
-   CSRF protection em todos os forms
-   Password hashing com Bcrypt
-   SQL injection protection via Eloquent
-   XSS protection automático
-   Rate limiting por IP
-   Autorização granular via Policies

---

## Contribuir

```bash
# Fork o repositório
git checkout -b feature/nova-funcionalidade
git commit -m "feat: adiciona funcionalidade X"
git push origin feature/nova-funcionalidade
# Abrir Pull Request
```

### Convenções

**Commits**: Conventional Commits

```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
refactor: refatoração
test: testes
```

**Code Style**: PSR-12 (PHP), ESLint (JavaScript)

---

## Documentação

-   [Requisitos](docs/requirements.md)
-   [Arquitetura](docs/architecture.md)
-   [Database Schema](docs/database-schema.md)
-   [API Reference](docs/api.md) (em desenvolvimento)

---

## Licença

Projeto académico desenvolvido para o CET - Técnico especialista em tecnologias e programação de sistemas de informação.

**Instituição**: Centro de Formação Profissional de Évora
**Ano Letivo**: 2024/2026

---

## Autor

**João Santos**
[Email](JMSS1995@hotmail.com) • [GitHub](https://github.com/JMSS95)

---

## Agradecimentos

Desenvolvido com Laravel, Vue.js, e ❤️

Stack construída sobre os ombros de gigantes:

-   Laravel Framework
-   Vue.js Team
-   Spatie packages
-   Tailwind Labs
-   Open Source Community

---

**OrionOne** • Modern ITSM Platform • 2025
