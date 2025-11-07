# Setup Completo - OrionOne

## Instalado e Configurado

### 1. Docker (5 containers rodando)

- `orionone-app` - Laravel + PHP 8.2-FPM
- `orionone-frontend` - Vite dev server (porta 5173)
- `orionone-nginx` - Nginx (porta 8888)
- `orionone-postgres` - PostgreSQL 16
- `orionone-redis` - Redis 7

**Acesso:**

- Laravel: http://localhost:8888
- Vite HMR: http://localhost:5173

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
 Actions/
 Tickets/ # Operações atómicas de tickets
 Comments/ # Operações atómicas de comments
 Services/ # Lógica de negócio e orquestração
 Policies/ # Autorização (Gates)
 Observers/ # Hooks de lifecycle de models
 Notifications/ # Email, Slack, Database notifications
 Events/ # Domain events
 Listeners/ # Event handlers
```

### 4. Base de Dados

Migrations executadas:

- `users` table
- `cache` table
- `jobs` table
- `telescope_entries` table

### 5. Documentação Criada

- `docs/docker-deep-dive.md` - Explicação completa de Docker
- `docs/development-tools.md` - Ferramentas e boas práticas
- `docs/scripts.md` - Comandos úteis do dia-a-dia

## Próximos Passos

### 1. Começar Desenvolvimento (Prioridade Alta)

#### A. Criar Models Base

```bash
# Ticket
php artisan make:model Ticket -mfs

# Comment
php artisan make:model Comment -mfs

# Team
php artisan make:model Team -mfs

# Category
php artisan make:model Category -mfs

# Article (Knowledge Base)
php artisan make:model Article -mfs
```

**Flags:**

- `-m` = migration
- `-f` = factory
- `-s` = seeder

#### B. Implementar Authentication

```bash
# Já tem Laravel Breeze instalado, criar views/controllers personalizados
php artisan breeze:install vue

# Configurar roles e permissions (Spatie)
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"
php artisan migrate
```

#### C. Criar Controllers

```bash
php artisan make:controller TicketController --resource
php artisan make:controller CommentController --resource
php artisan make:controller DashboardController
```

#### D. Criar Form Requests

```bash
php artisan make:request StoreTicketRequest
php artisan make:request UpdateTicketRequest
php artisan make:request StoreCommentRequest
```

### 2. Implementar Funcionalidades Core

#### Ordem Sugerida (seguir requirements.md):

1. **RF01 - Authentication** (1-2 dias)

 - Login/Logout
 - Roles (Admin, Manager, Agent, User)
 - Password reset

2. **RF02 - Ticket Creation** (2-3 dias)

 - Form com validação
 - Upload de anexos
 - Auto-assignment básico

3. **RF03 - Comments** (1 dia)

 - Adicionar comentários
 - Notificações

4. **RF04 - Teams** (1-2 dias)

 - CRUD de equipas
 - Atribuir agents a equipas

5. **RF05 - Assignment** (2 dias)

 - Manual assignment
 - Auto-assignment (round-robin)

6. **RF06 - SLA** (2-3 dias)

 - Cálculo de deadlines
 - Alertas de violação

7. **RF07 - Knowledge Base** (2-3 dias)

 - CRUD de artigos
 - Categorização
 - Busca

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

- **Feature Test** (teste de integração HTTP)
- **Unit Test** (lógica isolada)

**Exemplo:**

```bash
php artisan make:test TicketTest # Feature
php artisan make:test TicketServiceTest --unit # Unit
```

### 4. Frontend (Inertia.js + Vue 3)

#### Componentes a Criar:

```
resources/js/
 Components/
 Tickets/
 TicketCard.vue
 TicketForm.vue
 TicketList.vue
 Dashboard/
 StatsCard.vue
 RecentTickets.vue
 Shared/
 Sidebar.vue
 Navbar.vue
 Modal.vue
 Pages/
 Tickets/
 Index.vue
 Show.vue
 Create.vue
 Dashboard.vue
 Auth/
 Login.vue
 Register.vue
 Layouts/
 AppLayout.vue
 GuestLayout.vue
```

## Timeline Sugerida (2.5 meses)

### Semana 1-2: Setup + Authentication + Tickets

- Docker e ambiente (concluído)
- Models base + migrations
- Authentication (Breeze + roles)
- CRUD de tickets básico

### Semana 3-4: Core Features

- Comments
- Teams
- Assignment (manual + auto)
- SLA básico

### Semana 5-6: Knowledge Base + Dashboard

- CRUD de artigos
- Categorização e busca
- Dashboard com estatísticas
- Gráficos

### Semana 7-8: Polimento + Testes

- Notificações
- Activity log
- Testes unitários e de integração
- Code coverage >70%

### Semana 9-10: Documentação + Deploy

- Swagger API docs completa
- README atualizado
- Deploy (VPS/Cloud)
- Apresentação final

## Comandos Rápidos

### Desenvolvimento

```bash
# Iniciar tudo
docker-compose up -d

# Ver logs
docker-compose logs -f orionone-app

# Artisan
docker-compose exec orionone-app php artisan [comando]

# Testes
docker-compose exec orionone-app php artisan test

# Code quality
docker-compose exec orionone-app ./vendor/bin/pint
docker-compose exec orionone-app ./vendor/bin/phpstan analyse
```

### Quando Trocar de PC

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

- `docs/requirements.md` - Requisitos funcionais e não-funcionais
- `docs/architecture.md` - Arquitetura e decisões técnicas
- `docs/database-schema.md` - Schema completo do PostgreSQL
- `docs/docker-deep-dive.md` - Explicação completa de Docker
- `docs/development-tools.md` - Ferramentas e workflow
- `docs/scripts.md` - Comandos úteis

## Checklist Atual

- [x] Docker configurado (5 containers)
- [x] Migrations executadas
- [x] Larastan instalado
- [x] L5-Swagger instalado
- [x] Estrutura de pastas criada
- [x] Documentação completa
- [ ] Models com relationships
- [ ] Authentication completo
- [ ] CRUD de Tickets
- [ ] CRUD de Comments
- [ ] Sistema de Teams
- [ ] Assignment logic
- [ ] SLA calculation
- [ ] Knowledge Base
- [ ] Dashboard
- [ ] Notifications
- [ ] Activity Log
- [ ] Testes (>70% coverage)
- [ ] API documentation (Swagger)
- [ ] Deploy

---

**Status:** Ambiente 100% configurado, pronto para desenvolvimento! 
