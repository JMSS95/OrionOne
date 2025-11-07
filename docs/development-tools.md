# Setup de Ferramentas de Desenvolvimento - OrionOne

## 📋 Checklist de Ferramentas

### ✅ Já Instaladas (Laravel 11)

-   **PHPUnit** - Testes unitários e de integração
-   **Pest** (via Laravel Pint) - Testes modernos (alternativa ao PHPUnit)
-   **Laravel Pint** - Code style fixer (baseado em PHP-CS-Fixer)
-   **Collision** - Error handler bonito para CLI

### 🔧 Recomendadas para Instalar

#### 1. **PHPStan** (Análise Estática)

#### 2. **Larastan** (PHPStan + regras Laravel)

#### 3. **Swagger/OpenAPI** (Documentação de API)

#### 4. **Laravel Telescope** (✅ já instalado - Debug)

#### 5. **Laravel Debugbar** (✅ já instalado - Debug)

---

## 1. PHPStan / Larastan

### O que é?

**PHPStan** analisa código **sem executá-lo** e encontra:

-   Type errors (variáveis com tipo errado)
-   Undefined variables/properties
-   Dead code (código nunca executado)
-   Lógica impossível (`if (true && false)`)

**Larastan** adiciona regras específicas do Laravel:

-   Valida facades
-   Entende magic methods (`User::find()`)
-   Analisa Eloquent relationships

### Instalação

```bash
# Dentro do container
docker-compose exec orionone-app composer require --dev larastan/larastan

# Criar arquivo de configuração
```

**Criar `phpstan.neon`:**

```neon
includes:
    - vendor/larastan/larastan/extension.neon

parameters:
    level: 5
    paths:
        - app
        - routes
    excludePaths:
        - app/Console/Kernel.php
    checkMissingIterableValueType: false
```

**Níveis (0-9):**

-   **Level 0:** Básico (undefined variables)
-   **Level 5:** Recomendado (balanço rigor/praticidade)
-   **Level 9:** Extremo (type hints obrigatórios)

### Uso

```bash
# Análise completa
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# Análise específica
docker-compose exec orionone-app ./vendor/bin/phpstan analyse app/Models

# Baseline (ignora erros atuais, só novos)
docker-compose exec orionone-app ./vendor/bin/phpstan analyse --generate-baseline
```

**Exemplo de Output:**

```
------ -------------------------------------------------
 Line   app/Http/Controllers/TicketController.php
------ -------------------------------------------------
 23     Parameter $id of method store() has invalid type int|string.
 45     Call to an undefined method App\Models\User::tickets().
------ -------------------------------------------------
```

### Integração CI/CD

**GitHub Actions:**

```yaml
- name: PHPStan
  run: docker-compose exec -T orionone-app ./vendor/bin/phpstan analyse --error-format=github
```

---

## 2. Swagger / OpenAPI (Documentação de API)

### O que é?

Gera **documentação interativa** da API REST:

-   Endpoints disponíveis
-   Parâmetros (query, body, headers)
-   Respostas (success, error)
-   Schema de dados
-   Interface para testar requests

**Exemplo:**
![Swagger UI](https://swagger.io/swagger/media/Images/tools/open-source/swagger-ui-screenshot.png)

### Opções para Laravel

#### Opção 1: **L5-Swagger** (Recomendado)

```bash
# Instalação
docker-compose exec orionone-app composer require darkaonline/l5-swagger

# Publicar configuração
docker-compose exec orionone-app php artisan vendor:publish --provider "L5Swagger\L5SwaggerServiceProvider"

# Gerar documentação
docker-compose exec orionone-app php artisan l5-swagger:generate
```

**Configuração (`config/l5-swagger.php`):**

```php
'documentations' => [
    'default' => [
        'api' => [
            'title' => 'OrionOne API Documentation',
            'version' => '1.0.0',
        ],
        'routes' => [
            'api' => 'api/documentation',
        ],
        'paths' => [
            'docs' => storage_path('api-docs'),
        ],
    ],
],
```

**Uso em Controllers:**

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;

/**
 * @OA\Info(
 *     version="1.0.0",
 *     title="OrionOne API",
 *     description="IT Service Management API"
 * )
 * @OA\Server(
 *     url="http://localhost:8888/api",
 *     description="Development Server"
 * )
 */
class TicketController extends Controller
{
    /**
     * @OA\Get(
     *     path="/tickets",
     *     summary="List all tickets",
     *     tags={"Tickets"},
     *     @OA\Parameter(
     *         name="status",
     *         in="query",
     *         required=false,
     *         @OA\Schema(type="string", enum={"open", "closed"})
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Successful operation",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(ref="#/components/schemas/Ticket")
     *         )
     *     )
     * )
     */
    public function index(Request $request)
    {
        // ...
    }

    /**
     * @OA\Post(
     *     path="/tickets",
     *     summary="Create new ticket",
     *     tags={"Tickets"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"title", "description"},
     *             @OA\Property(property="title", type="string", example="Laptop não liga"),
     *             @OA\Property(property="description", type="string"),
     *             @OA\Property(property="priority", type="string", enum={"low", "medium", "high"})
     *         )
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Ticket created",
     *         @OA\JsonContent(ref="#/components/schemas/Ticket")
     *     ),
     *     @OA\Response(
     *         response=422,
     *         description="Validation error"
     *     )
     * )
     */
    public function store(Request $request)
    {
        // ...
    }
}
```

**Schema em Model:**

```php
<?php

namespace App\Models;

/**
 * @OA\Schema(
 *     schema="Ticket",
 *     title="Ticket",
 *     description="Ticket model",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="title", type="string", example="Laptop não liga"),
 *     @OA\Property(property="description", type="string"),
 *     @OA\Property(property="status", type="string", enum={"open", "in_progress", "closed"}),
 *     @OA\Property(property="priority", type="string", enum={"low", "medium", "high"}),
 *     @OA\Property(property="created_at", type="string", format="date-time"),
 *     @OA\Property(property="updated_at", type="string", format="date-time")
 * )
 */
class Ticket extends Model
{
    // ...
}
```

**Acessar Documentação:**

```
http://localhost:8888/api/documentation
```

#### Opção 2: **Scramble** (Automático - Laravel 10+)

```bash
docker-compose exec orionone-app composer require dedoc/scramble
```

**Vantagens:**

-   ✅ Gera docs **automaticamente** (sem annotations)
-   ✅ Analisa FormRequests, Resources, Routes
-   ✅ Interface moderna

**Desvantagens:**

-   ❌ Menos controle sobre docs
-   ❌ Pode errar em casos complexos

**Uso:**

```
http://localhost:8888/docs/api
```

---

## 3. Outras Ferramentas Úteis

### PHP CS Fixer (✅ Laravel Pint já faz isso)

```bash
# Verificar estilo
docker-compose exec orionone-app ./vendor/bin/pint --test

# Corrigir automaticamente
docker-compose exec orionone-app ./vendor/bin/pint
```

### Pest (Alternativa ao PHPUnit)

**Já disponível no Laravel 11!**

```bash
# Rodar testes com Pest
docker-compose exec orionone-app php artisan test --pest
```

**Exemplo de Teste Pest:**

```php
<?php

use App\Models\User;
use App\Models\Ticket;

it('creates a ticket', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/api/tickets', [
        'title' => 'Test Ticket',
        'description' => 'Test Description',
    ]);

    $response->assertStatus(201);
    expect(Ticket::count())->toBe(1);
});

it('requires authentication', function () {
    $response = $this->post('/api/tickets', [
        'title' => 'Test',
    ]);

    $response->assertStatus(401);
});
```

### Laravel IDE Helper

Autocomplete para facades, models, etc.

```bash
docker-compose exec orionone-app composer require --dev barryvdh/laravel-ide-helper

# Gerar helpers
docker-compose exec orionone-app php artisan ide-helper:generate
docker-compose exec orionone-app php artisan ide-helper:models
docker-compose exec orionone-app php artisan ide-helper:meta
```

### Clockwork (Alternative ao Telescope)

Debug tool mais leve.

```bash
docker-compose exec orionone-app composer require itsgoingd/clockwork
```

Acessa via extensão do Chrome: [Clockwork](https://chromewebstore.google.com/detail/clockwork/dmggabnehkmmfmdffgajcflpdjlnoemp)

---

## 4. Estrutura de Testes Recomendada

```
tests/
├── Feature/              # Testes de integração (HTTP requests)
│   ├── Api/
│   │   ├── TicketTest.php
│   │   ├── UserTest.php
│   │   └── AuthTest.php
│   └── Web/
│       └── DashboardTest.php
├── Unit/                 # Testes unitários (classes isoladas)
│   ├── Models/
│   │   └── TicketTest.php
│   ├── Services/
│   │   └── TicketServiceTest.php
│   └── Actions/
│       └── CreateTicketActionTest.php
└── Fixtures/             # Dados de teste reutilizáveis
    └── tickets.json
```

**Exemplo Feature Test (PHPUnit):**

```php
<?php

namespace Tests\Feature\Api;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TicketTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_ticket(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/tickets', [
            'title' => 'Test Ticket',
            'description' => 'Test Description',
            'priority' => 'high',
        ]);

        $response->assertStatus(201)
            ->assertJsonStructure([
                'data' => ['id', 'title', 'status', 'created_at'],
            ]);

        $this->assertDatabaseHas('tickets', [
            'title' => 'Test Ticket',
            'user_id' => $user->id,
        ]);
    }

    public function test_ticket_requires_title(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/tickets', [
            'description' => 'Test',
        ]);

        $response->assertStatus(422)
            ->assertJsonValidationErrors(['title']);
    }
}
```

**Exemplo Unit Test:**

```php
<?php

namespace Tests\Unit\Models;

use App\Models\Ticket;
use App\Models\User;
use Tests\TestCase;

class TicketTest extends TestCase
{
    public function test_ticket_belongs_to_user(): void
    {
        $ticket = new Ticket();

        $this->assertInstanceOf(
            \Illuminate\Database\Eloquent\Relations\BelongsTo::class,
            $ticket->user()
        );
    }

    public function test_ticket_can_be_closed(): void
    {
        $ticket = Ticket::factory()->create(['status' => 'open']);

        $ticket->close();

        $this->assertEquals('closed', $ticket->status);
    }
}
```

---

## 5. GitHub Actions (CI/CD)

**`.github/workflows/tests.yml`:**

```yaml
name: Tests

on: [push, pull_request]

jobs:
    tests:
        runs-on: ubuntu-latest

        steps:
            - uses: actions/checkout@v3

            - name: Start Docker Compose
              run: docker-compose up -d

            - name: Install Dependencies
              run: docker-compose exec -T orionone-app composer install

            - name: Run PHPStan
              run: docker-compose exec -T orionone-app ./vendor/bin/phpstan analyse

            - name: Run Pint
              run: docker-compose exec -T orionone-app ./vendor/bin/pint --test

            - name: Run Tests
              run: docker-compose exec -T orionone-app php artisan test --coverage

            - name: Shutdown
              run: docker-compose down
```

---

## 6. Recomendação para OrionOne

### Setup Inicial

```bash
# 1. Larastan (análise estática)
docker-compose exec orionone-app composer require --dev larastan/larastan

# 2. L5-Swagger (documentação API)
docker-compose exec orionone-app composer require darkaonline/l5-swagger

# 3. IDE Helper (autocomplete)
docker-compose exec orionone-app composer require --dev barryvdh/laravel-ide-helper
```

### Configurar

```bash
# PHPStan
cat > phpstan.neon << 'EOF'
includes:
    - vendor/larastan/larastan/extension.neon
parameters:
    level: 5
    paths:
        - app
EOF

# Swagger
docker-compose exec orionone-app php artisan vendor:publish --provider "L5Swagger\L5SwaggerServiceProvider"

# IDE Helper
docker-compose exec orionone-app php artisan ide-helper:generate
```

### Workflow Diário

```bash
# Antes de commitar:

# 1. Code style
docker-compose exec orionone-app ./vendor/bin/pint

# 2. Análise estática
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# 3. Testes
docker-compose exec orionone-app php artisan test

# 4. Gerar docs Swagger (se mudou API)
docker-compose exec orionone-app php artisan l5-swagger:generate
```

---

## 7. Scripts Helper

**Criar `scripts/dev.sh`:**

```bash
#!/bin/bash

case $1 in
  test)
    docker-compose exec orionone-app php artisan test
    ;;
  stan)
    docker-compose exec orionone-app ./vendor/bin/phpstan analyse
    ;;
  fix)
    docker-compose exec orionone-app ./vendor/bin/pint
    ;;
  docs)
    docker-compose exec orionone-app php artisan l5-swagger:generate
    echo "Docs: http://localhost:8888/api/documentation"
    ;;
  check)
    echo "Running all checks..."
    docker-compose exec orionone-app ./vendor/bin/pint --test
    docker-compose exec orionone-app ./vendor/bin/phpstan analyse
    docker-compose exec orionone-app php artisan test
    ;;
  *)
    echo "Usage: ./scripts/dev.sh {test|stan|fix|docs|check}"
    ;;
esac
```

**Uso:**

```bash
chmod +x scripts/dev.sh
./scripts/dev.sh check  # Roda todos os checks
```

---

## Resumo

### ✅ Instalar Agora

1. **Larastan** - Previne bugs antes de rodar código
2. **L5-Swagger** - Documenta API para frontend/testes
3. **IDE Helper** - Melhora autocomplete no VS Code

### ⏳ Considerar Depois

-   **Pest** - Se preferir sintaxe moderna de testes
-   **Clockwork** - Se Telescope ficar pesado
-   **Dusk** - Para testes E2E (browser)

### ❌ Não Precisa

-   **PHP CS Fixer** - Laravel Pint já faz isso
-   **PHPUnit** - Já vem no Laravel
-   **Xdebug** - Telescope + Debugbar são suficientes para desenvolvimento

---

**Próximo Passo:** Quer que eu instale e configure Larastan + L5-Swagger agora?
