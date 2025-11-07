# Rotina de Desenvolvimento - OrionOne

## Filosofia: Feature-Driven + TDD

Desenvolver **por feature completa** (vertical slice), não por camadas (DB → API → Frontend).

### Evitar (Waterfall por camadas)

```
1. Criar TODA a DB
2. Criar TODO o backend/API
3. Criar TODO o frontend
4. Testar TUDO no final
```

**Problemas:**

-   Descobres erros tarde demais
-   Difícil integrar tudo
-   Não tens nada funcional até o fim

### Seguir (Iterativo por Feature)

```
Feature 1 (Tickets) → Feature 2 (Comments) → Feature 3 (Teams) → ...
```

Cada feature passa por **TODAS as camadas** antes de passar para a próxima.

---

## Ciclo de Desenvolvimento por Feature

### Fase 1: Planeamento (30 min)

```
📋 Definir feature
   ├─ Requisito funcional (do requirements.md)
   ├─ User story
   └─ Critérios de aceitação
```

**Exemplo - RF02: Criar Ticket**

```markdown
**User Story:**
Como utilizador autenticado, quero criar um ticket para reportar um problema.

**Critérios de Aceitação:**

-   [ ] Form com campos: título, descrição, prioridade
-   [ ] Validação: título obrigatório, max 255 chars
-   [ ] Upload de anexos (opcional)
-   [ ] Auto-assignment a equipa correta
-   [ ] Email enviado ao agent responsável
-   [ ] Redirect para página do ticket criado
```

---

### Fase 2: Base de Dados (30-45 min)

#### 2.1. Migration

```bash
php artisan make:migration create_tickets_table
```

#### 2.2. Model + Relationships

```bash
php artisan make:model Ticket
```

#### 2.3. Factory (Dados de Teste)

```bash
php artisan make:factory TicketFactory
```

#### 2.4. Seeder (Dados Iniciais)

```bash
php artisan make:seeder TicketSeeder
```

**Checkpoint:**

```bash
php artisan migrate:fresh --seed
php artisan tinker
>>> Ticket::count()  # Deve retornar > 0
```

---

### Fase 3: Backend (TDD) (2-3h)

#### 3.1. **PRIMEIRO: Escrever Testes**

```bash
# Feature Test (HTTP)
php artisan make:test TicketTest

# Unit Test (Lógica)
php artisan make:test TicketServiceTest --unit
```

**Exemplo (Feature Test):**

```php
public function test_user_can_create_ticket(): void
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/tickets', [
        'title' => 'Laptop não liga',
        'description' => 'Tentei ligar mas não funciona',
        'priority' => 'high',
    ]);

    $response->assertStatus(201);
    $this->assertDatabaseHas('tickets', [
        'title' => 'Laptop não liga',
        'user_id' => $user->id,
    ]);
}
```

**Rodar teste (vai falhar - esperado!):**

```bash
docker-compose exec orionone-app php artisan test --filter=TicketTest
# RED: Route not found
```

#### 3.2. Implementar até Testes Passarem (RED → GREEN)

**a) Route:**

```php
Route::post('/tickets', [TicketController::class, 'store']);
```

**b) Form Request:**

```bash
php artisan make:request StoreTicketRequest
```

**c) Controller:**

```bash
php artisan make:controller TicketController --resource
```

**d) Service (se lógica complexa):**

```bash
# Criar manualmente em app/Services/TicketService.php
```

**e) Action (operações atómicas):**

```bash
# Criar manualmente em app/Actions/Tickets/CreateTicketAction.php
```

**Rodar teste novamente:**

```bash
docker-compose exec orionone-app php artisan test --filter=TicketTest
# GREEN: Teste passa!
```

#### 3.3. Refactor (GREEN → REFACTOR)

Melhorar código sem quebrar testes:

-   Extrair lógica para Service
-   Adicionar validações extras
-   Melhorar nomenclatura

**Rodar testes após cada mudança:**

```bash
docker-compose exec orionone-app php artisan test
```

#### 3.4. Code Quality

```bash
# Code style
docker-compose exec orionone-app ./vendor/bin/pint

# Análise estática
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# Testes com coverage
docker-compose exec orionone-app php artisan test --coverage
```

**Checkpoint:**

-   [ ] Todos os testes passam
-   [ ] Pint sem erros
-   [ ] PHPStan sem erros
-   [ ] Coverage >80% na feature

---

### Fase 4: Frontend (1-2h)

#### 4.1. Componentes Vue

```bash
# Criar componentes
resources/js/Components/Tickets/TicketForm.vue
resources/js/Components/Tickets/TicketCard.vue
```

#### 4.2. Página Inertia

```bash
resources/js/Pages/Tickets/Create.vue
resources/js/Pages/Tickets/Index.vue
resources/js/Pages/Tickets/Show.vue
```

#### 4.3. Controller (Inertia)

```php
public function create()
{
    return Inertia::render('Tickets/Create', [
        'priorities' => ['low', 'medium', 'high'],
        'categories' => Category::all(),
    ]);
}
```

#### 4.4. Teste Manual no Browser

```bash
# Vite já está rodando em localhost:5173
# Aceder: http://localhost:8888/tickets/create
```

**Checkpoint:**

-   [ ] Form renderiza corretamente
-   [ ] Validações funcionam (frontend + backend)
-   [ ] Submit cria ticket
-   [ ] Redirect funciona
-   [ ] Erros são exibidos

---

### Fase 5: API (REST) (1h) - **Opcional**

Se precisar de API REST (para mobile/third-party):

#### 5.1. API Controller

```bash
php artisan make:controller Api/TicketController --api
```

#### 5.2. API Resource

```bash
php artisan make:resource TicketResource
```

#### 5.3. Swagger Annotations

```php
/**
 * @OA\Post(
 *     path="/api/tickets",
 *     summary="Create new ticket",
 *     tags={"Tickets"},
 *     @OA\RequestBody(...)
 * )
 */
public function store(StoreTicketRequest $request) { }
```

#### 5.4. API Tests

```bash
php artisan make:test Api/TicketApiTest
```

**Checkpoint:**

-   [ ] API testes passam
-   [ ] Swagger docs geradas
-   [ ] Postman/Insomnia testado

---

### Fase 6: Commit & Deploy (15 min)

```bash
# 1. Última verificação
docker-compose exec orionone-app php artisan test
docker-compose exec orionone-app ./vendor/bin/pint
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# 2. Commit
git add .
git commit -m "feat(tickets): implementar criação de tickets

- Migration e Model de Ticket
- Form Request com validações
- TicketService com lógica de assignment
- Vue components (TicketForm, TicketCard)
- Testes unitários e de integração (coverage 85%)
- API REST com Swagger docs"

# 3. Push
git push origin main
```

---

## 📅 Exemplo de Sprint (1 Semana)

### Segunda-feira: RF02 - Criar Tickets

```
09:00-09:30  Planeamento (user story, critérios)
09:30-10:30  DB (migration, model, factory, seeder)
10:30-13:00  Backend TDD (testes → implementação → refactor)
14:00-15:30  Frontend (Vue components, Inertia pages)
15:30-16:00  Code quality (Pint, PHPStan)
16:00-16:30  Commit & review
```

### Terça-feira: RF03 - Adicionar Comentários

```
09:00-09:30  Planeamento
09:30-10:30  DB (comments table)
10:30-13:00  Backend TDD
14:00-15:30  Frontend (CommentList, CommentForm)
15:30-16:00  Code quality
16:00-16:30  Commit
```

### Quarta-feira: RF04 - Gestão de Equipas

```
(Mesmo ciclo)
```

### Quinta-feira: RF05 - Assignment Logic

```
(Mesmo ciclo)
```

### Sexta-feira: Polimento + Integração

```
09:00-11:00  Testes de integração entre features
11:00-13:00  Bug fixes
14:00-15:00  Refactoring
15:00-16:00  Documentação (README, Swagger)
16:00-17:00  Code review (PHPStan, coverage report)
```

---

## Scripts Helper

### Criar `scripts/feature.sh`

```bash
#!/bin/bash
# Scaffolding rápido de feature

FEATURE=$1

if [ -z "$FEATURE" ]; then
    echo "Usage: ./scripts/feature.sh FeatureName"
    exit 1
fi

# Lowercase
feature_lower=$(echo $FEATURE | tr '[:upper:]' '[:lower:]')

# Migration
docker-compose exec orionone-app php artisan make:migration create_${feature_lower}_table

# Model + Factory + Seeder
docker-compose exec orionone-app php artisan make:model $FEATURE -fs

# Controller
docker-compose exec orionone-app php artisan make:controller ${FEATURE}Controller --resource

# Form Request
docker-compose exec orionone-app php artisan make:request Store${FEATURE}Request
docker-compose exec orionone-app php artisan make:request Update${FEATURE}Request

# Tests
docker-compose exec orionone-app php artisan make:test ${FEATURE}Test
docker-compose exec orionone-app php artisan make:test ${FEATURE}ServiceTest --unit

# Policy
docker-compose exec orionone-app php artisan make:policy ${FEATURE}Policy

echo "✅ Feature scaffold criado: $FEATURE"
echo "📝 Próximos passos:"
echo "   1. Escrever migration em database/migrations/"
echo "   2. Escrever testes em tests/"
echo "   3. Implementar lógica até testes passarem"
```

**Uso:**

```bash
chmod +x scripts/feature.sh
./scripts/feature.sh Ticket
```

---

## Checklist por Feature

```markdown
### Feature: [Nome]

**DB:**

-   [ ] Migration criada e testada
-   [ ] Model com relationships
-   [ ] Factory funcional
-   [ ] Seeder com dados realistas

**Backend:**

-   [ ] Feature tests escritos (RED)
-   [ ] Controller implementado
-   [ ] Form Request com validações
-   [ ] Service/Action (se necessário)
-   [ ] Policy de autorização
-   [ ] Testes passam (GREEN)
-   [ ] Code refactorado (REFACTOR)
-   [ ] Pint sem erros
-   [ ] PHPStan sem erros
-   [ ] Coverage >80%

**Frontend:**

-   [ ] Componentes Vue criados
-   [ ] Páginas Inertia funcionais
-   [ ] Validação frontend + backend
-   [ ] UX testada no browser
-   [ ] Responsivo (mobile/desktop)

**API (opcional):**

-   [ ] API Controller
-   [ ] Resources (JSON)
-   [ ] Swagger docs
-   [ ] API tests

**Git:**

-   [ ] Commit com mensagem descritiva
-   [ ] Push para repositório
```

---

## Prioridades por Fase do Projeto

### Fase 1: MVP (Semanas 1-4)

**Foco:** Funcionalidades core funcionais, código limpo.

```
Ciclo: Planeamento → DB → Backend TDD → Frontend → Commit
Tempo por feature: 1-2 dias
Features: RF01-RF06 (Auth, Tickets, Comments, Teams, Assignment, SLA básico)
```

### Fase 2: Extensão (Semanas 5-6)

**Foco:** Features extras, polimento UX.

```
Ciclo: (igual Fase 1)
Features: RF07-RF10 (Knowledge Base, Dashboard, Notifications, Activity Log)
```

### Fase 3: Qualidade (Semanas 7-8)

**Foco:** Testes, refactoring, performance.

```
- Aumentar coverage para >90%
- Refactoring guiado por PHPStan
- Performance tuning (N+1 queries, caching)
- Accessibility (WCAG 2.1)
```

### Fase 4: Documentação + Deploy (Semanas 9-10)

**Foco:** Docs, deploy, apresentação.

```
- Swagger completo
- README.md atualizado
- Deploy em VPS/Cloud
- Vídeo demo
- Slides apresentação
```

---

## Métricas de Qualidade

### Por Feature

```bash
# Coverage
php artisan test --coverage --min=80

# Complexidade ciclomática (PHPStan)
./vendor/bin/phpstan analyse --level=max

# Code style
./vendor/bin/pint --test
```

### Por Sprint (Semanal)

```
- Features completadas: X/Y
- Testes passando: 100%
- Coverage médio: >80%
- PHPStan errors: 0
- Bugs abertos: <5
```

---

## Próximo Passo Imediato

Quer começar com **RF02 - Criar Tickets** seguindo esta rotina?

```bash
# 1. Scaffold
./scripts/feature.sh Ticket

# 2. Planear
# (criar user story + critérios de aceitação)

# 3. DB
# (migration + model + factory + seeder)

# 4. Backend TDD
# (escrever testes → implementar → refactor)

# 5. Frontend
# (Vue components + Inertia pages)

# 6. Commit
git commit -m "feat(tickets): criar tickets"
```

Devo criar o script `feature.sh` e começar com RF02?


---

# Estratégia de Testes

## Visão Geral

Este documento define a estratégia de testes do OrionOne, estabelecendo guidelines, métricas de qualidade e padrões para garantir confiabilidade e manutenibilidade do código.

---

## Pirâmide de Testes

```
         ╱╲
        ╱E2E╲          <- 5-10% (Selenium, Cypress)
       ╱──────╲
      ╱ Feature╲       <- 30-40% (HTTP tests, Inertia)
     ╱──────────╲
    ╱    Unit    ╲     <- 50-60% (Services, Actions, Models)
   ╱──────────────╲
```

### Distribuição Recomendada

| Tipo              | %      | Quantidade Esperada | Tempo de Execução |
| ----------------- | ------ | ------------------- | ----------------- |
| **Unit Tests**    | 50-60% | ~80-100 testes      | <5s               |
| **Feature Tests** | 30-40% | ~50-60 testes       | <15s              |
| **E2E Tests**     | 5-10%  | ~10-15 testes       | <2min             |

---

## Tipos de Testes

### 1. Unit Tests

**O quê testar:**

-   Services (lógica de negócio)
-   Actions (operações atómicas)
-   Models (métodos customizados)
-   Helpers/Utilities

**Características:**

-   Rápidos (<1ms cada)
-   Isolados (sem DB, sem HTTP)
-   Focados em lógica pura
-   Uso de mocks/stubs se necessário

**Exemplos de cenários:**

-   Cálculo de tempo restante de SLA
-   Deteção de violações de SLA
-   Lógica de atribuição automática
-   Validações de negócio customizadas

### 2. Feature Tests (HTTP)

**O quê testar:**

-   Controllers (endpoints HTTP)
-   Autorização (Policies)
-   Validação (Form Requests)
-   Workflows completos

**Características:**

-   Usa `RefreshDatabase`
-   Testa HTTP responses (200, 403, 422)
-   Valida database state
-   Testa autorização via Policies

**Exemplos de cenários:**

-   User pode criar ticket
-   Agent pode atribuir ticket a equipa
-   User não pode apagar ticket de outro user
-   Validação de campos obrigatórios

### 3. Integration Tests

**O quê testar:**

-   Eventos + Listeners
-   Observers
-   Jobs (queues)
-   Notificações

**Exemplos de cenários:**

-   Notificação enviada quando ticket atribuído
-   Activity log criado quando ticket modificado
-   Job de email adicionado à queue
-   Evento disparado após criação de comentário

### 4. E2E Tests (Futuro)

**Ferramentas:** Laravel Dusk ou Cypress

**O quê testar:**

-   Fluxos críticos completos
-   Interações Vue 3 complexas
-   Multi-step workflows

**Exemplos de cenários:**

-   Fluxo completo: Login → Criar Ticket → Adicionar Comentário → Resolver
-   Upload de anexos via drag-and-drop
-   Filtros e pesquisa em tempo real

---

## Métricas de Qualidade

### Coverage Mínimo

| Layer           | Coverage Alvo | Obrigatório    |
| --------------- | ------------- | -------------- |
| **Services**    | 90-100%       | ✅ Sim         |
| **Actions**     | 90-100%       | ✅ Sim         |
| **Controllers** | 80-90%        | ✅ Sim         |
| **Models**      | 70-80%        | ⚠️ Recomendado |
| **Policies**    | 100%          | ✅ Sim         |
| **Observers**   | 80-90%        | ✅ Sim         |
| **Geral**       | >80%          | ✅ Sim         |

### Comandos

```bash
# Coverage geral
docker-compose exec orionone-app php artisan test --coverage

# Coverage com threshold mínimo (CI/CD)
docker-compose exec orionone-app php artisan test --coverage --min=80

# Coverage de path específico
docker-compose exec orionone-app php artisan test --coverage --path=app/Services
```

---

## Factories & Seeders

### Factories

**Usar para:** Criar dados fake nos testes

**Estados customizados recomendados:**

-   `urgent()` - Ticket com prioridade urgent
-   `resolved()` - Ticket já resolvido
-   `admin()` - User com role admin
-   `agent()` - User com role agent

### Seeders

**Usar para:** Popular DB em desenvolvimento (não em testes)

**Seeders recomendados:**

-   `DevelopmentSeeder` - Dados completos para desenvolvimento local
-   `DemoSeeder` - Dados para demonstração/apresentação
-   `TestSeeder` - Dataset pequeno para testes manuais

---

## Estrutura de Testes

```
tests/
├── Feature/
│   ├── Auth/
│   │   ├── LoginTest.php
│   │   ├── RegisterTest.php
│   │   └── PasswordResetTest.php
│   ├── Tickets/
│   │   ├── TicketCrudTest.php
│   │   ├── TicketAssignmentTest.php
│   │   └── TicketNotificationTest.php
│   ├── Comments/
│   │   └── CommentTest.php
│   └── Teams/
│       └── TeamTest.php
│
├── Unit/
│   ├── Services/
│   │   ├── TicketServiceTest.php
│   │   ├── SLAServiceTest.php
│   │   └── AssignmentServiceTest.php
│   ├── Actions/
│   │   ├── CreateTicketActionTest.php
│   │   └── AssignTicketActionTest.php
│   └── Models/
│       ├── TicketTest.php
│       └── UserTest.php
│
└── Browser/ (futuro)
    └── TicketCreationTest.php
```

---

## AAA Pattern

**Arrange → Act → Assert**

Estrutura padrão para todos os testes:

1. **Arrange** - Preparar dados e estado inicial
2. **Act** - Executar ação a ser testada
3. **Assert** - Verificar resultado esperado

---

## Assertions Comuns

### HTTP Responses

```php
$response->assertStatus(200);           // OK
$response->assertStatus(201);           // Created
$response->assertStatus(403);           // Forbidden
$response->assertStatus(404);           // Not Found
$response->assertStatus(422);           // Validation Error
```

### Database

```php
$this->assertDatabaseHas('tickets', ['title' => 'Test']);
$this->assertDatabaseMissing('tickets', ['id' => 999]);
$this->assertDatabaseCount('tickets', 10);
$this->assertSoftDeleted('tickets', ['id' => 1]);
```

### Notifications/Events

```php
Notification::assertSentTo($user, TicketAssignedNotification::class);
Event::assertDispatched(TicketCreated::class);
Queue::assertPushed(SendTicketNotification::class);
```

---

## CI/CD Pipeline (Futuro)

Pipeline GitHub Actions para executar testes automaticamente em cada push:

**Etapas:**

1. Setup PHP 8.2 + PostgreSQL 16
2. Install dependencies (`composer install`)
3. Run tests com coverage mínima 80%
4. PHPStan analysis (level 5)
5. Laravel Pint code style check

---

## Boas Práticas

### DO

-   Escrever testes **antes** do código (TDD)
-   Usar factories em vez de criar dados manualmente
-   Testar **comportamento**, não implementação
-   Manter testes **isolados** (sem dependências entre testes)
-   Nomear testes de forma descritiva (`test_user_can_create_ticket`)
-   Usar `RefreshDatabase` em Feature Tests
-   Asserções específicas (`assertEquals`, não `assertTrue`)

### DON'T

-   Testar código de framework (Laravel já testa)
-   Testar getters/setters simples
-   Testes com lógica complexa (if/loops)
-   Testes dependentes de ordem de execução
-   Hardcode de IDs ou timestamps
-   Deixar `dd()` ou `dump()` em testes

---

## Debugging de Testes

```bash
# Executar teste específico
php artisan test --filter=test_user_can_create_ticket

# Ver queries SQL
php artisan test --filter=TicketTest --log-events-verbose-text

# Parar no primeiro erro
php artisan test --stop-on-failure
```

---

## Timeline de Implementação

### Semana 1-2 (Setup)

-   [x] Configurar PHPUnit
-   [ ] Criar primeiras factories
-   [ ] Feature tests de Auth

### Semana 3-4 (Core)

-   [ ] Unit tests de Services
-   [ ] Feature tests de Tickets
-   [ ] Coverage >70%

### Semana 5-6 (Extended)

-   [ ] Tests de Comments, Teams, SLA
-   [ ] Coverage >80%

### Semana 7-8 (Quality)

-   [ ] Refactoring tests
-   [ ] Coverage >90%
-   [ ] E2E tests (opcional)

---

## Recursos

-   [Laravel Testing Docs](https://laravel.com/docs/11.x/testing)
-   [PHPUnit Documentation](https://phpunit.de/documentation.html)
-   [Test Driven Laravel](https://course.testdrivenlaravel.com/)

**Regra de Ouro:**

> "Código sem testes é código legado."

---

## Métricas de Qualidade

### Coverage Mínimo

| Layer           | Coverage Alvo | Obrigatório    |
| --------------- | ------------- | -------------- |
| **Services**    | 90-100%       | ✅ Sim         |
| **Actions**     | 90-100%       | ✅ Sim         |
| **Controllers** | 80-90%        | ✅ Sim         |
| **Models**      | 70-80%        | ⚠️ Recomendado |
| **Policies**    | 100%          | ✅ Sim         |
| **Observers**   | 80-90%        | ✅ Sim         |
| **Geral**       | >80%          | ✅ Sim         |

### Comandos

```bash
# Coverage geral
docker-compose exec orionone-app php artisan test --coverage

# Coverage com threshold mínimo (CI/CD)
docker-compose exec orionone-app php artisan test --coverage --min=80

# Coverage de path específico
docker-compose exec orionone-app php artisan test --coverage --path=app/Services
```

---

## Factories & Seeders

### Factories

**Usar para:** Criar dados fake nos testes

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class TicketFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(),
            'description' => fake()->paragraph(),
            'status' => 'open',
            'priority' => fake()->randomElement(['low', 'medium', 'high', 'urgent']),
            'user_id' => User::factory(),
        ];
    }

    public function urgent(): static
    {
        return $this->state(fn (array $attributes) => [
            'priority' => 'urgent',
        ]);
    }

    public function resolved(): static
    {
        return $this->state(fn (array $attributes) => [
            'status' => 'resolved',
            'resolved_at' => now(),
        ]);
    }
}
```

**Uso nos testes:**

```php
// Ticket básico
$ticket = Ticket::factory()->create();

// Ticket urgente
$ticket = Ticket::factory()->urgent()->create();

// 10 tickets para teste
$tickets = Ticket::factory()->count(10)->create();

// Ticket com relações
$ticket = Ticket::factory()
    ->for(User::factory()->agent())
    ->has(Comment::factory()->count(3))
    ->create();
```

### Seeders

**Usar para:** Popular DB em desenvolvimento (não em testes)

```php
<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Team;
use App\Models\Ticket;
use Illuminate\Database\Seeder;

class DevelopmentSeeder extends Seeder
{
    public function run(): void
    {
        // Admin
        $admin = User::factory()->admin()->create([
            'name' => 'Admin User',
            'email' => 'admin@orionone.test',
        ]);

        // 5 Agents
        $agents = User::factory()->agent()->count(5)->create();

        // 2 Teams
        $supportTeam = Team::factory()->create(['name' => 'Suporte Técnico']);
        $networkTeam = Team::factory()->create(['name' => 'Redes']);

        // 50 Tickets
        Ticket::factory()->count(50)->create();
    }
}
```

---

## Estrutura de Testes

```
tests/
├── Feature/
│   ├── Auth/
│   │   ├── LoginTest.php
│   │   ├── RegisterTest.php
│   │   └── PasswordResetTest.php
│   ├── Tickets/
│   │   ├── TicketCrudTest.php
│   │   ├── TicketAssignmentTest.php
│   │   └── TicketNotificationTest.php
│   ├── Comments/
│   │   └── CommentTest.php
│   └── Teams/
│       └── TeamTest.php
│
├── Unit/
│   ├── Services/
│   │   ├── TicketServiceTest.php
│   │   ├── SLAServiceTest.php
│   │   └── AssignmentServiceTest.php
│   ├── Actions/
│   │   ├── CreateTicketActionTest.php
│   │   └── AssignTicketActionTest.php
│   └── Models/
│       ├── TicketTest.php
│       └── UserTest.php
│
└── Browser/ (futuro)
    └── TicketCreationTest.php
```

---

## AAA Pattern

**Arrange → Act → Assert**

```php
/** @test */
public function assigns_ticket_to_least_busy_agent(): void
{
    // Arrange
    $busyAgent = User::factory()->agent()->create();
    $freeAgent = User::factory()->agent()->create();

    Ticket::factory()->for($busyAgent, 'assignedTo')->count(5)->create();
    Ticket::factory()->for($freeAgent, 'assignedTo')->count(1)->create();

    $service = new AssignmentService();
    $newTicket = Ticket::factory()->create();

    // Act
    $assignedAgent = $service->assignToLeastBusy($newTicket);

    // Assert
    $this->assertEquals($freeAgent->id, $assignedAgent->id);
    $this->assertEquals($freeAgent->id, $newTicket->fresh()->assigned_to);
}
```

---

## Assertions Comuns

### HTTP Responses

```php
$response->assertStatus(200);           // OK
$response->assertStatus(201);           // Created
$response->assertStatus(204);           // No Content
$response->assertStatus(403);           // Forbidden
$response->assertStatus(404);           // Not Found
$response->assertStatus(422);           // Validation Error

$response->assertJson(['status' => 'success']);
$response->assertJsonStructure(['data' => ['id', 'title']]);
$response->assertRedirect('/tickets');
```

### Database

```php
$this->assertDatabaseHas('tickets', ['title' => 'Test']);
$this->assertDatabaseMissing('tickets', ['id' => 999]);
$this->assertDatabaseCount('tickets', 10);
$this->assertSoftDeleted('tickets', ['id' => 1]);
```

### Notifications/Events

```php
Notification::assertSentTo($user, TicketAssignedNotification::class);
Event::assertDispatched(TicketCreated::class);
Queue::assertPushed(SendTicketNotification::class);
```

---

## CI/CD Pipeline (Futuro)

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
    test:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3

            - name: Setup PHP
              uses: shivammathur/setup-php@v2
              with:
                  php-version: 8.2
                  extensions: pdo_pgsql, redis

            - name: Install Dependencies
              run: composer install --no-interaction

            - name: Run Tests
              run: php artisan test --coverage --min=80

            - name: PHPStan
              run: ./vendor/bin/phpstan analyse

            - name: Pint
              run: ./vendor/bin/pint --test
```

---

## Boas Práticas

### DO

-   Escrever testes **antes** do código (TDD)
-   Usar factories em vez de criar dados manualmente
-   Testar **comportamento**, não implementação
-   Manter testes **isolados** (sem dependências entre testes)
-   Nomear testes de forma descritiva (`test_user_can_create_ticket`)
-   Usar `RefreshDatabase` em Feature Tests
-   Asserções específicas (`assertEquals`, não `assertTrue`)

### DON'T

-   Testar código de framework (Laravel já testa)
-   Testar getters/setters simples
-   Testes com lógica complexa (if/loops)
-   Testes dependentes de ordem de execução
-   Hardcode de IDs ou timestamps
-   Deixar `dd()` ou `dump()` em testes

---

## Debugging de Testes

```bash
# Executar teste específico
php artisan test --filter=test_user_can_create_ticket

# Ver queries SQL
php artisan test --filter=TicketTest --log-events-verbose-text

# Parar no primeiro erro
php artisan test --stop-on-failure

# Com dd() para debug
// Dentro do teste
dd($response->json());
dd($ticket->fresh());
```

---

## Timeline de Implementação

### Semana 1-2 (Setup)

-   [x] Configurar PHPUnit
-   [ ] Criar primeiras factories
-   [ ] Feature tests de Auth

### Semana 3-4 (Core)

-   [ ] Unit tests de Services
-   [ ] Feature tests de Tickets
-   [ ] Coverage >70%

### Semana 5-6 (Extended)

-   [ ] Tests de Comments, Teams, SLA
-   [ ] Coverage >80%

### Semana 7-8 (Quality)

-   [ ] Refactoring tests
-   [ ] Coverage >90%
-   [ ] E2E tests (opcional)

---

## Recursos

-   [Laravel Testing Docs](https://laravel.com/docs/11.x/testing)
-   [PHPUnit Documentation](https://phpunit.de/documentation.html)
-   [Test Driven Laravel](https://course.testdrivenlaravel.com/)
-   [Laracasts: Testing](https://laracasts.com/topics/testing)

**Regra de Ouro:**

> "Código sem testes é código legado."

