# Arquitetura do OrionOne

## Visão Geral

OrionOne seguirá uma arquitetura **MVC com Service Layer**, equilibrando simplicidade com boas práticas de Engenharia de Software. Esta decisão arquitetural foi tomada considerando:

- Prazo de desenvolvimento (2.5 meses para MVP)
- Manutenibilidade e testabilidade
- Aproveitamento das convenções do Laravel
- Escalabilidade para funcionalidades futuras

## Padrão Arquitetural

### MVC + Service Layer + Actions

```
┌─────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER │
│ - Controllers: Request handling (5-15 linhas) │
│ - Requests: Form validation │
│ - Resources: API responses (futuro) │
└────────────────────────┬────────────────────────────────────┘
 │
┌────────────────────────▼────────────────────────────────────┐
│ BUSINESS LOGIC LAYER │
│ - Services: Lógica de negócio complexa e orquestração │
│ - Actions: Operações atómicas (single responsibility) │
│ - Policies: Regras de autorização │
│ - Events/Listeners: Domain events │
└────────────────────────┬────────────────────────────────────┘
 │
┌────────────────────────▼────────────────────────────────────┐
│ DATA LAYER │
│ - Models: Eloquent ORM │
│ - Observers: Hooks automáticos de modelos │
│ - Repositories: Abstração de queries (opcional) │
└────────────────────────┬────────────────────────────────────┘
 │
┌────────────────────────▼────────────────────────────────────┐
│ INFRASTRUCTURE │
│ - Database: PostgreSQL 16 │
│ - Cache: Redis (sessions, queries, queues) │
│ - Storage: Local filesystem / S3 (produção) │
└─────────────────────────────────────────────────────────────┘
```

---

## Camadas Detalhadas

### 1. Presentation Layer

**Responsabilidade**: Interface entre o utilizador e a aplicação.

#### Controllers

Os controllers serão **thin controllers** - apenas coordenação, sem lógica de negócio:

**Princípios:**

- Controllers NÃO contêm lógica de negócio
- Máximo 15 linhas por método
- Apenas: validação, chamada de service, redirect/response
- Dependency injection de Services no constructor

#### Form Requests

Toda a validação de input será isolada em Form Request classes:

**Vantagens:**

- Validação isolada e reutilizável
- Controllers mais limpos
- Fácil de testar
- Autorização integrada (`authorize()` method)

---

### 2. Business Logic Layer

#### Services

Os Services orquestram lógica de negócio complexa que envolve múltiplas entidades.

**Quando usar Services:**

- Operações que envolvem múltiplos models
- Lógica de negócio complexa
- Orquestração de Actions
- Transações de base de dados
- Coordenação de notificações e events

**Exemplo de responsabilidades:**

- `TicketService`: criação de tickets, atribuição, resolução
- `AssignmentService`: lógica de auto-assignment (round-robin, skills-based)
- `SLAService`: cálculo de deadlines, verificação de violações
- `NotificationService`: envio de emails, notificações in-app

#### Actions

Actions encapsulam operações atómicas com single responsibility.

**Quando usar Actions:**

- Operações simples mas importantes
- Lógica reutilizável entre Services
- Single Responsibility Principle
- Fácil de testar isoladamente

**Exemplos planeados:**

- `AssignTicketAction`: atribuir ticket a um agent
- `ResolveTicketAction`: marcar ticket como resolvido
- `EscalateTicketAction`: escalar ticket para manager

#### Policies

Toda a autorização será centralizada em Policy classes:

**Vantagens:**

- Autorização centralizada e auditável
- Reutilizável em controllers, views, API
- Integração automática com Laravel Gates

---

### 3. Data Layer

#### Eloquent Models

Os models Eloquent terão responsabilidades bem definidas:

**Responsabilidades:**

- Definir relacionamentos (hasMany, belongsTo, etc)
- Casts e accessors/mutators
- Query scopes para queries reutilizáveis
- **NÃO** conter lógica de negócio complexa

**Boas práticas:**

- Usar `$fillable` para mass assignment protection
- Definir `$casts` para automatic type conversion
- Criar scopes para queries comuns (`scopeOpen`, `scopeOverdue`)
- Usar attributes para computed properties

#### Observers

Observers implementarão hooks automáticos de lifecycle:

**Exemplos planeados:**

- Auto-geração de `ticket_number` ao criar ticket
- Auto-atualização de `resolved_at` quando status muda para "resolved"
- Logging automático de alterações críticas

---

## Fluxo de Dados

### Exemplo: Criar Ticket

```
┌─────────┐
│ User │ submete formulário
└────┬────┘
 │ POST /tickets
 │
┌────▼────────────────┐
│ TicketController │ → valida com StoreTicketRequest
└────┬────────────────┘
 │ createTicket()
┌────▼────────────────┐
│ TicketService │ → orquestra operação
└────┬────────────────┘
 │
 ├──→ Ticket::create() [Data Layer]
 ├──→ AssignmentService [determina equipa/agent]
 ├──→ SLAService [calcula deadlines]
 ├──→ NotificationService [envia emails]
 └──→ event(TicketCreated) [dispara event]
 │
 └──→ Listeners
 - LogTicketActivity
 - UpdateStatistics
```

---

## Decisões Arquiteturais

### Porquê NÃO Modular Monolith?

**Considerado mas rejeitado porque:**

- Overkill para MVP de 2.5 meses
- Complexidade sem benefício real no contexto académico
- Laravel não tem suporte nativo (requer packages third-party)
- Overhead de setup vs. benefícios em projeto com 1 developer

**Quando seria apropriado:**

- Equipas com 5+ developers a trabalhar em paralelo
- Domínios muito distintos (10+ bounded contexts)
- Necessidade de deploy independente de módulos

### Porquê NÃO Hexagonal/Clean Architecture?

**Considerado mas rejeitado porque:**

- Tempo de desenvolvimento duplicado para abstrações
- Luta contra convenções idiomáticas do Laravel
- Abstração excessiva para o domínio do problema
- Curva de aprendizagem alta sem ganhos claros no prazo

**Quando seria apropriado:**

- Aplicações enterprise de longa duração (10+ anos)
- Múltiplos frontends (web, mobile, desktop, third-party APIs)
- Necessidade de trocar framework no futuro
- Domínios extremamente complexos

### Porquê Services + Actions?

**Escolhido porque:**

- Equilibra simplicidade com boas práticas
- Testável e manutenível
- Idiomático ao Laravel (community best practices)
- Escalável para crescimento futuro
- Fácil de explicar ao júri e documentar

---

## Estrutura de Pastas Planeada

```
app/
├── Http/
│ ├── Controllers/ # Thin controllers
│ │ ├── TicketController.php
│ │ ├── CommentController.php
│ │ ├── DashboardController.php
│ │ └── KnowledgeBaseController.php
│ │
│ ├── Requests/ # Form validation
│ │ ├── StoreTicketRequest.php
│ │ ├── UpdateTicketRequest.php
│ │ └── StoreCommentRequest.php
│ │
│ └── Middleware/
│ └── CheckTicketAccess.php
│
├── Services/ # Business logic orchestration
│ ├── TicketService.php
│ ├── AssignmentService.php
│ ├── SLAService.php
│ ├── NotificationService.php
│ └── ReportingService.php
│
├── Actions/ # Atomic operations
│ ├── Tickets/
│ │ ├── CreateTicketAction.php
│ │ ├── AssignTicketAction.php
│ │ ├── ResolveTicketAction.php
│ │ ├── CloseTicketAction.php
│ │ └── EscalateTicketAction.php
│ │
│ └── Comments/
│ └── AddCommentAction.php
│
├── Models/ # Eloquent models
│ ├── Ticket.php
│ ├── Comment.php
│ ├── Team.php
│ ├── Article.php
│ └── Category.php
│
├── Policies/ # Authorization
│ ├── TicketPolicy.php
│ ├── CommentPolicy.php
│ └── ArticlePolicy.php
│
├── Observers/ # Model hooks
│ ├── TicketObserver.php
│ └── CommentObserver.php
│
├── Notifications/ # Email/Slack/Database
│ ├── TicketCreated.php
│ ├── TicketAssigned.php
│ ├── CommentAdded.php
│ └── SLAViolation.php
│
├── Events/ # Domain events
│ ├── TicketCreated.php
│ ├── TicketStatusChanged.php
│ └── SLAViolated.php
│
├── Listeners/ # Event handlers
│ ├── LogTicketActivity.php
│ ├── UpdateStatistics.php
│ └── SendNotifications.php
│
└── Jobs/ # Async tasks
 ├── CheckSLAViolations.php
 ├── GenerateDailyReport.php
 └── SendBulkNotifications.php
```

---

## Padrões de Design a Utilizar

### 1. Service Layer Pattern

Centraliza lógica de negócio complexa, mantendo controllers finos e focados.

### 2. Action Pattern (Command Pattern)

Encapsula operações atómicas com single responsibility.

### 3. Observer Pattern

Para hooks automáticos de models (auto-generate ticket_number, timestamps, etc).

### 4. Event-Driven Architecture

Para comunicação desacoplada entre componentes do sistema.

### 5. Repository Pattern (Opcional)

Considerado apenas se surgir necessidade de abstrair queries muito complexas.

---

## Princípios SOLID

### Single Responsibility Principle

Cada classe terá UMA razão para mudar:

- `TicketController`: coordena HTTP requests
- `TicketService`: orquestra criação de tickets
- `AssignTicketAction`: apenas atribui tickets
- `SLAService`: apenas calcula SLAs

### Open/Closed Principle

Extensível sem modificar código existente:

- Novos tipos de notificação podem ser adicionados sem alterar `NotificationService`
- Novas estratégias de assignment podem ser injetadas via interface

### Liskov Substitution Principle

Interfaces bem definidas permitem substituição:

- `AssignmentStrategyInterface` pode ter múltiplas implementações
- Mocks podem substituir Services em testes

### Interface Segregation Principle

Classes pequenas e focadas, sem métodos não utilizados.

- Preferir várias interfaces específicas a uma genérica

### Dependency Inversion Principle

Dependency injection em todos os Services:

- Controllers dependem de abstrações (Services)
- Services dependem de interfaces, não implementações concretas
- Facilita testing e mocking

---

## Estratégia de Testes

### Unit Tests (Services & Actions)

**Objetivo:** Testar lógica de negócio isoladamente

**Abordagem:**

- Mock de dependências externas
- Testes rápidos (< 100ms cada)
- Coverage mínimo de 80% em Services críticos

**Exemplos de testes:**

- `TicketService::createTicket()` atribui equipa correta
- `SLAService::calculateDeadlines()` calcula prazos conforme prioridade
- `AssignTicketAction` atualiza status e notifica agent

### Feature Tests (Controllers)

**Objetivo:** Testar fluxo completo HTTP → Response

**Abordagem:**

- Database transactions (rollback após cada teste)
- Autenticação real com factory users
- Assertions em database, session, redirects

**Exemplos de testes:**

- User pode criar ticket e é redirecionado corretamente
- Agent pode ver apenas tickets da sua equipa
- Manager pode ver todos os tickets

### Browser Tests (Dusk - Opcional)

**Objetivo:** Testar interface Vue/Inertia em browser real

**Quando usar:**

- Fluxos críticos de UI (criar ticket, comentar)
- Interações JavaScript complexas
- Antes de releases

---

## Performance Considerations

### Caching Strategy

| Tipo de Dados | TTL | Storage |
| ----------------------- | -------- | ------- |
| Query results | 5-15 min | Redis |
| Session data | 120 min | Redis |
| Dashboard stats | 60 min | Redis |
| Knowledge base articles | 24 horas | Redis |
| User permissions | 60 min | Redis |

### Database Optimization

- **Indexes:** em todas as foreign keys + composite indexes para queries comuns
- **Eager loading:** evitar N+1 queries com `with()`
- **Query scopes:** reutilizáveis e otimizados
- **Soft deletes:** para auditoria sem perda de dados

### Queue Jobs

| Operação | Fila | Prioridade |
| --------------- | --------------- | ---------- |
| Envio de emails | `notifications` | Normal |
| SLA checks | `monitoring` | High |
| Relatórios | `reports` | Low |
| Exports | `exports` | Low |

---

## Segurança

### Authentication

- **Laravel Sanctum:** SPA authentication com cookies httpOnly
- **Session-based:** para web tradicional
- **CSRF protection:** automático em formulários

### Authorization

- **Policies:** para todos os recursos (Ticket, Comment, Article)
- **Gates:** para permissões globais (view-dashboard, manage-users)
- **Spatie Permission:** para roles & permissions granulares

### Data Protection

- **Password hashing:** bcrypt (default Laravel)
- **SQL injection prevention:** Eloquent ORM (prepared statements)
- **XSS protection:** Blade/Vue automatic escaping
- **Rate limiting:** por IP e por user
- **Validation:** todos os inputs sanitizados

---

## Escalabilidade Futura

### Possíveis Evoluções

1. **API RESTful**

 - Services já prontos para serem reutilizados
 - Laravel Resources para serialização

2. **Microservices** (se necessário)

 - Domínios bem definidos facilitam separação
 - Event-driven já implementado

3. **Event Sourcing**

 - Events já implementados
 - Facilita audit trail completo

4. **CQRS**
 - Separação read/write se necessário
 - Services já separam commands de queries

### Limitações Conhecidas

- **Multi-tenancy:** requer refactoring de queries (global scopes)
- **Real-time features:** precisam de WebSocket layer (Laravel Reverb/Pusher)
- **File storage:** precisa migrar para S3 em produção
- **Horizontal scaling:** sessões Redis já preparadas

---

## Conclusão

A arquitetura escolhida para OrionOne equilibra:

- **Pragmatismo:** MVP entregue no prazo de 2.5 meses
- **Qualidade:** Código testável, manutenível e profissional
- **Aprendizagem:** Demonstra conhecimento sólido de Engenharia de Software
- **Escalabilidade:** Preparado para crescimento futuro sem rewrite

Esta arquitetura não é a mais complexa possível, mas é **apropriada para o contexto e objetivos** do projeto académico OrionOne, demonstrando maturidade técnica ao escolher a solução adequada ao problema, não a mais "fancy".
