# Estratégia de Testes - OrionOne

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

### ✅ DO

-   Escrever testes **antes** do código (TDD)
-   Usar factories em vez de criar dados manualmente
-   Testar **comportamento**, não implementação
-   Manter testes **isolados** (sem dependências entre testes)
-   Nomear testes de forma descritiva (`test_user_can_create_ticket`)
-   Usar `RefreshDatabase` em Feature Tests
-   Asserções específicas (`assertEquals`, não `assertTrue`)

### ❌ DON'T

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

### ✅ DO

-   Escrever testes **antes** do código (TDD)
-   Usar factories em vez de criar dados manualmente
-   Testar **comportamento**, não implementação
-   Manter testes **isolados** (sem dependências entre testes)
-   Nomear testes de forma descritiva (`test_user_can_create_ticket`)
-   Usar `RefreshDatabase` em Feature Tests
-   Asserções específicas (`assertEquals`, não `assertTrue`)

### ❌ DON'T

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
