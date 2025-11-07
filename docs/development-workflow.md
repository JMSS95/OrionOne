# Rotina de Desenvolvimento - OrionOne

## 🎯 Filosofia: Feature-Driven + TDD

Desenvolver **por feature completa** (vertical slice), não por camadas (DB → API → Frontend).

### ❌ Evitar (Waterfall por camadas)

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

### ✅ Seguir (Iterativo por Feature)

```
Feature 1 (Tickets) → Feature 2 (Comments) → Feature 3 (Teams) → ...
```

Cada feature passa por **TODAS as camadas** antes de passar para a próxima.

---

## 🔄 Ciclo de Desenvolvimento por Feature

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

**✅ Checkpoint:**

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

**✅ Checkpoint:**

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

**✅ Checkpoint:**

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

**✅ Checkpoint:**

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

## 🛠️ Scripts Helper

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

## ✅ Checklist por Feature

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

## 🎯 Prioridades por Fase do Projeto

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

## 📊 Métricas de Qualidade

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

## 🚀 Próximo Passo Imediato

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
