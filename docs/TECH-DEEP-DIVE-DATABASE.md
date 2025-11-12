# Tech Deep Dive - Base de Dados (PostgreSQL/Redis)

> **Guia Completo**: Como funciona a camada de dados do OrionOne - PostgreSQL 16, Redis 7, Queues, Cache

---

## 1. POSTGRESQL 16 (Base de Dados Relacional)

### O que é?

**PostgreSQL** é uma base de dados relacional open-source. É como MySQL, mas com **mais features avançadas**.

### Porque PostgreSQL (não MySQL)?

| Feature | PostgreSQL ✅ | MySQL ❌ |
| -------------------- | ----------------- | ---------------- |
| **JSONB** | Nativo, indexável | JSON simples |
| **Full-Text Search** | Built-in (pt-PT!) | Precisa extensão |
| **Arrays** | `tags TEXT[]` | Não suporta |
| **Window Functions** | Completo | Limitado |
| **CTEs Recursivos** | Sim | Sim (desde 8.0) |
| **Transações ACID** | Muito robusto | Bom |
| **Extensões** | PostGIS, pg_trgm | Menos opções |

### PostgreSQL no OrionOne:

```php
// config/database.php
'pgsql' => [
 'driver' => 'pgsql',
 'host' => env('DB_HOST', '127.0.0.1'),
 'port' => env('DB_PORT', '5432'),
 'database' => env('DB_DATABASE', 'orionone'),
 'username' => env('DB_USERNAME', 'postgres'),
 'password' => env('DB_PASSWORD', ''),
 'charset' => 'utf8',
 'prefix' => '',
 'schema' => 'public',
 'sslmode' => 'prefer',
],
```

---

## 2. FEATURES POSTGRESQL USADAS NO ORIONONE

### 1. **JSONB (Binary JSON)**

#### O que é?

Tipo de dados que armazena JSON de forma **binária** (mais rápido que texto).

#### Porque usar?

- **Flexível**: Esquema dinâmico (sem ALTER TABLE)
- **Indexável**: Queries rápidas em JSON
- **Binário**: 20-30% mais rápido que JSON texto

#### Exemplo Real: Metadata em Tickets

```php
// Migration
Schema::create('tickets', function (Blueprint $table) {
 $table->id();
 $table->string('title');
 $table->text('description');
 $table->jsonb('metadata')->nullable(); // ← JSONB!
 $table->timestamps();
});
```

```php
// Criar ticket com metadata
Ticket::create([
 'title' => 'Problema de rede',
 'description' => 'Sem internet',
 'metadata' => [
 'ip_address' => '192.168.1.100',
 'device_type' => 'laptop',
 'os' => 'Windows 11',
 'tags' => ['network', 'urgent'],
 ],
]);
```

```php
// Queries em JSONB
// 1. Buscar por campo específico
$tickets = Ticket::whereRaw("metadata->>'device_type' = ?", ['laptop'])->get();

// 2. Buscar array dentro de JSONB
$urgents = Ticket::whereRaw("metadata @> ?", ['{"tags":["urgent"]}']})->get();

// 3. Index para performance
Schema::table('tickets', function (Blueprint $table) {
 $table->index('metadata', 'tickets_metadata_gin', 'gin'); // GIN index
});
```

---

### 2. **Full-Text Search (Pesquisa de Texto)**

#### O que é?

Pesquisa inteligente que entende **palavras similares**, **stemming** (palavras raiz), e **ranking**.

#### Exemplo: Pesquisar tickets

```sql
-- Criar índice de texto completo
CREATE INDEX tickets_fulltext_idx ON tickets
USING GIN (to_tsvector('portuguese', title || ' ' || description));
```

```php
// Migration Laravel
Schema::table('tickets', function (Blueprint $table) {
 DB::statement("
 CREATE INDEX tickets_fulltext_idx ON tickets
 USING GIN (to_tsvector('portuguese', title || ' ' || description))
 ");
});
```

```php
// Query Laravel
$results = Ticket::whereRaw("
 to_tsvector('portuguese', title || ' ' || description) @@
 plainto_tsquery('portuguese', ?)",
 [$searchQuery]
)
->orderByRaw("
 ts_rank(
 to_tsvector('portuguese', title || ' ' || description),
 plainto_tsquery('portuguese', ?)
 ) DESC",
 [$searchQuery]
)
->get();
```

**Exemplo:**

```php
$search = "problemas impressoras";
// Encontra: "problema com impressora", "impressoras não funcionam", etc
// Não precisa match exato!
```

---

### 3. **Arrays Nativos**

#### O que é?

PostgreSQL suporta arrays como tipo de dados nativo.

#### Exemplo: Tags em Artigos

```php
// Migration
Schema::create('knowledge_base_articles', function (Blueprint $table) {
 $table->id();
 $table->string('title');
 $table->text('content');
 $table->text('tags', 'text[]')->nullable(); // ← Array!
 $table->timestamps();
});
```

```php
// Criar artigo
KnowledgeBaseArticle::create([
 'title' => 'Como resetar password',
 'content' => '...',
 'tags' => ['password', 'authentication', 'security'], // Array direto!
]);
```

```php
// Queries com arrays
// 1. Contém tag específica
$articles = KnowledgeBaseArticle::whereRaw("'password' = ANY(tags)")->get();

// 2. Contém qualquer tag de uma lista
$articles = KnowledgeBaseArticle::whereRaw("tags && ARRAY['password', 'security']")->get();

// 3. Adicionar tag
DB::statement("
 UPDATE knowledge_base_articles
 SET tags = array_append(tags, ?)
 WHERE id = ?",
 ['new-tag', $articleId]
);
```

---

### 4. **Window Functions (Análises Avançadas)**

#### O que é?

Funções que calculam valores sobre "janelas" de dados, sem GROUP BY.

#### Exemplo 1: Ranking de Agentes (quem resolve mais tickets)

```php
$rankings = DB::select("
 SELECT
 users.name,
 COUNT(tickets.id) AS total_resolved,
 RANK() OVER (ORDER BY COUNT(tickets.id) DESC) AS ranking
 FROM users
 LEFT JOIN tickets ON tickets.assigned_to = users.id
 AND tickets.status = 'resolved'
 GROUP BY users.id, users.name
");
```

**Resultado:**

```
name | total_resolved | ranking
---------------|----------------|--------
João Silva | 142 | 1
Maria Santos | 138 | 2
Pedro Costa | 105 | 3
```

#### Exemplo 2: Comparar com Média

```php
$comparisons = DB::select("
 SELECT
 teams.name AS team_name,
 COUNT(tickets.id) AS tickets_count,
 AVG(COUNT(tickets.id)) OVER () AS avg_tickets, -- ← Window!
 COUNT(tickets.id) - AVG(COUNT(tickets.id)) OVER () AS diff
 FROM teams
 LEFT JOIN tickets ON tickets.team_id = teams.id
 GROUP BY teams.id, teams.name
");
```

**Resultado:**

```
team_name | tickets_count | avg_tickets | diff
-----------|---------------|-------------|------
Suporte | 450 | 300 | +150
Dev | 250 | 300 | -50
Infra | 200 | 300 | -100
```

---

### 5. **CTEs (Common Table Expressions) - Queries Complexas**

#### O que são?

"Subqueries com nome" para queries mais legíveis.

#### Exemplo: Hierarquia de Tickets (Ticket Parent → Children)

```php
$hierarchy = DB::select("
 WITH RECURSIVE ticket_tree AS (
 -- Base: tickets pai (sem parent)
 SELECT id, title, parent_ticket_id, 1 AS level
 FROM tickets
 WHERE parent_ticket_id IS NULL

 UNION ALL

 -- Recursivo: tickets filhos
 SELECT t.id, t.title, t.parent_ticket_id, tt.level + 1
 FROM tickets t
 INNER JOIN ticket_tree tt ON t.parent_ticket_id = tt.id
 )
 SELECT * FROM ticket_tree ORDER BY level, id
");
```

**Resultado:**

```
id | title | level
----|----------------------------|------
1 | Problema com servidor | 1 (pai)
2 | ├─ Investigar logs | 2 (filho)
3 | ├─ Verificar disco | 2 (filho)
4 | └─ Substituir HD | 3 (neto)
```

---

### 6. **Partitioning (Tabelas Grandes)**

#### O que é?

Dividir tabela grande em "partições" menores (por data, range, etc).

#### Exemplo: Logs por Mês

```sql
-- Criar tabela principal (particionada por data)
CREATE TABLE activity_logs (
 id BIGSERIAL,
 user_id INT,
 action VARCHAR(255),
 created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- Criar partições (1 por mês)
CREATE TABLE activity_logs_2024_01 PARTITION OF activity_logs
 FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE activity_logs_2024_02 PARTITION OF activity_logs
 FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

**Vantagens:**
✅ **Performance**: Queries só leem partição relevante
✅ **Manutenção**: Apagar logs antigos = DROP PARTITION (rápido)
✅ **Escalabilidade**: Cada partição pode ter índices próprios

---

### 7. **Extensões PostgreSQL**

#### pg_trgm (Trigram Similarity)

Pesquisa fuzzy (palavras parecidas).

```sql
-- Ativar extensão
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Pesquisa "parecida"
SELECT * FROM tickets
WHERE title % 'impresora'; -- Encontra "impressora" (typo!)
```

#### uuid-ossp (UUIDs)

Gerar IDs universalmente únicos.

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Usar UUID como PK
CREATE TABLE sessions (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 data TEXT
);
```

---

## 3. REDIS 7 (Cache + Queues)

### O que é?

**Redis** é uma base de dados **em memória** (RAM). Super rápido para cache e queues.

### Redis no OrionOne:

```php
// config/database.php
'redis' => [
 'client' => env('REDIS_CLIENT', 'phpredis'),
 'default' => [
 'host' => env('REDIS_HOST', '127.0.0.1'),
 'password' => env('REDIS_PASSWORD'),
 'port' => env('REDIS_PORT', '6379'),
 'database' => env('REDIS_DB', '0'),
 ],
 'cache' => [
 'host' => env('REDIS_HOST', '127.0.0.1'),
 'database' => '1', // DB separada para cache
 ],
 'queue' => [
 'host' => env('REDIS_HOST', '127.0.0.1'),
 'database' => '2', // DB separada para queues
 ],
],
```

---

### USO 1: CACHE (Performance)

#### Problema:

Queries pesadas que demoram muito:

```php
// Query lenta (JOIN + GROUP BY)
$stats = DB::table('tickets')
 ->join('users', 'tickets.assigned_to', '=', 'users.id')
 ->select(DB::raw('COUNT(*) as total, users.name'))
 ->groupBy('users.id', 'users.name')
 ->get();
// ⏱️ 500ms
```

#### Solução: Cache com Redis

```php
use Illuminate\Support\Facades\Cache;

$stats = Cache::remember('dashboard-stats', now()->addMinutes(10), function () {
 return DB::table('tickets')
 ->join('users', 'tickets.assigned_to', '=', 'users.id')
 ->select(DB::raw('COUNT(*) as total, users.name'))
 ->groupBy('users.id', 'users.name')
 ->get();
});
// ⏱️ 2ms (cached!)
```

#### Cache Patterns no OrionOne:

**1. Cache de Modelo (Model Caching)**

```php
class Team extends Model
{
 public static function findCached($id)
 {
 return Cache::remember("team.{$id}", 3600, function () use ($id) {
 return static::with('members')->find($id);
 });
 }
}
```

**2. Cache de Queries Complexas**

```php
public function getDashboardStats()
{
 return Cache::remember('dashboard-stats', now()->addHour(), function () {
 return [
 'open_tickets' => Ticket::where('status', 'open')->count(),
 'in_progress' => Ticket::where('status', 'in_progress')->count(),
 'resolved_today' => Ticket::where('status', 'resolved')
 ->whereDate('resolved_at', today())
 ->count(),
 ];
 });
}
```

**3. Invalidar Cache Automaticamente**

```php
class Ticket extends Model
{
 protected static function booted()
 {
 // Quando ticket muda, limpa cache
 static::saved(function () {
 Cache::forget('dashboard-stats');
 });
 }
}
```

---

### USO 2: QUEUES (Jobs Assíncronos)

#### Problema:

Ações lentas bloqueiam request:

```php
public function store(Request $request)
{
 $ticket = Ticket::create($request->validated());

 // Envia email (3 segundos!) ⏱️
 Mail::to($ticket->user)->send(new TicketCreated($ticket));

 return redirect()->back(); // Utilizador espera 3s!
}
```

#### Solução: Queue com Redis

```php
public function store(Request $request)
{
 $ticket = Ticket::create($request->validated());

 // Adiciona email à queue (1ms!)
 Mail::to($ticket->user)->queue(new TicketCreated($ticket));

 return redirect()->back(); // Resposta instantânea!
}
```

#### Como Funciona?

```
1. Request chega
 ↓
2. Ticket criado no PostgreSQL
 ↓
3. Job "SendEmail" adicionado à queue Redis
 ↓
4. Response enviada (rápido!)
 ↓
5. Worker processa job em background
 ↓
6. Email enviado (utilizador já recebeu response)
```

#### Processar Queue:

```bash
# Worker para processar jobs
php artisan queue:work redis --queue=emails,notifications
```

#### Jobs no OrionOne:

**1. SendTicketNotification**

```php
// app/Jobs/SendTicketNotification.php
class SendTicketNotification implements ShouldQueue
{
 use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

 public function __construct(
 public Ticket $ticket,
 public User $recipient,
 ) {}

 public function handle()
 {
 Mail::to($this->recipient)->send(
 new TicketCreated($this->ticket)
 );
 }
}
```

**Dispatch:**

```php
SendTicketNotification::dispatch($ticket, $user);
```

**2. ProcessBulkTicketUpdate**

```php
class ProcessBulkTicketUpdate implements ShouldQueue
{
 public function __construct(public array $ticketIds, public array $updates) {}

 public function handle()
 {
 foreach ($this->ticketIds as $id) {
 Ticket::find($id)->update($this->updates);

 // Pausa para não sobrecarregar DB
 usleep(100000); // 0.1s
 }
 }
}
```

**3. Failed Jobs (Retry)**

```php
// config/queue.php
'connections' => [
 'redis' => [
 'retry_after' => 90, // Retry após 90s
 'tries' => 3, // 3 tentativas
 ],
],
```

```php
// Job com retry custom
class SendTicketNotification implements ShouldQueue
{
 public $tries = 5; // 5 tentativas
 public $backoff = [60, 120, 300]; // Espera 1min, 2min, 5min

 public function failed(Throwable $exception)
 {
 // Log erro
 Log::error("Failed to send notification: {$exception->getMessage()}");
 }
}
```

---

### USO 3: RATE LIMITING

#### Problema:

Utilizador abusa da API (spam requests).

#### Solução: Rate Limit com Redis

```php
// routes/web.php
Route::middleware(['throttle:api'])->group(function () {
 Route::post('/tickets', [TicketController::class, 'store']);
});

// config/cache.php
'limiter' => 'redis', // Rate limiting via Redis

// app/Providers/RouteServiceProvider.php
RateLimiter::for('api', function (Request $request) {
 return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});
```

**Resultado:**

- ✅ 60 requests por minuto permitidos
- ❌ 61º request → HTTP 429 Too Many Requests

---

### USO 4: SESSION STORAGE

#### Porque Redis para sessões?

✅ **Performance**: Mais rápido que file/database
✅ **Escalabilidade**: Multi-server (load balancer)
✅ **Auto-expiring**: TTL automático

```php
// config/session.php
'driver' => env('SESSION_DRIVER', 'redis'),
'connection' => 'default',
'lifetime' => 120, // 2 horas
```

---

## 4. QUERY OPTIMIZATION (Performance)

### 1. **Indexes**

#### Quando criar index?

- Colunas em WHERE, JOIN, ORDER BY
- Foreign keys
- Colunas pesquisadas frequentemente

#### Exemplo:

```php
Schema::table('tickets', function (Blueprint $table) {
 // Index simples
 $table->index('status'); // WHERE status = 'open'

 // Index composto
 $table->index(['team_id', 'status']); // WHERE team_id = X AND status = Y

 // Unique index
 $table->unique('ticket_number'); // Garante unicidade

 // Foreign key index (Laravel cria automaticamente)
 $table->foreign('user_id')->references('id')->on('users');
});
```

#### Verificar uso de index:

```sql
EXPLAIN ANALYZE SELECT * FROM tickets WHERE status = 'open';
```

---

### 2. **Eager Loading (N+1 Problem)**

#### Problema: N+1 Queries

```php
$tickets = Ticket::all(); // 1 query

foreach ($tickets as $ticket) {
 echo $ticket->user->name; // N queries (1 por ticket!)
}
// Total: 1 + 100 = 101 queries!
```

#### Solução: Eager Loading

```php
$tickets = Ticket::with('user')->get(); // 2 queries

foreach ($tickets as $ticket) {
 echo $ticket->user->name; // Já carregado!
}
// Total: 2 queries!
```

#### Nested Relations:

```php
$tickets = Ticket::with([
 'user',
 'team.members',
 'comments.author',
])->get();
// 4 queries (tickets, users, teams, comments)
```

---

### 3. **Select Only Needed Columns**

#### Buscar tudo

```php
$tickets = Ticket::all(); // SELECT * (todos os campos)
```

#### Buscar só o necessário

```php
$tickets = Ticket::select('id', 'title', 'status')->get();
// Mais rápido, menos memória
```

---

### 4. **Chunk Large Datasets**

#### Carregar tudo na memória

```php
$tickets = Ticket::all(); // 100.000 tickets → Out of memory!
foreach ($tickets as $ticket) {
 // ...
}
```

#### Processar em chunks

```php
Ticket::chunk(1000, function ($tickets) {
 foreach ($tickets as $ticket) {
 // Processa 1000 de cada vez
 }
});
// Memória constante!
```

---

## 6. DATABASE VIEWS (Queries Pré-Computadas)

### O que são Views?

**Database Views** são queries SQL guardadas como "tabelas virtuais". São como **atalhos para queries complexas**.

### Porque usar Views?

- **Performance**: Query complexa executada uma vez, reutilizada sempre
- **DRY**: Não repetir SQL complexo em múltiplos lugares
- **Segurança**: Expor apenas colunas necessárias
- **Simplicidade**: Query de 50 linhas viram `SELECT * FROM v_dashboard`

### VIEW 1: v_ticket_dashboard (Dashboard Principal)

**Problema:** Dashboard precisa de dados de 4 tabelas (tickets, users, teams, comments).

**Solução:** View que JOINa tudo automaticamente.

```sql
CREATE OR REPLACE VIEW v_ticket_dashboard AS
SELECT
 t.id,
 t.ticket_number,
 t.title,
 t.status,
 t.priority,
 u_req.name AS requester_name,
 u_ag.name AS assigned_agent_name,
 tm.name AS team_name,
 CASE
 WHEN t.resolution_deadline < NOW() AND t.status IN ('open', 'in_progress')
 THEN true
 ELSE false
 END AS is_overdue,
 (SELECT COUNT(*) FROM comments WHERE ticket_id = t.id) AS comment_count
FROM tickets t
LEFT JOIN users u_req ON t.requester_id = u_req.id
LEFT JOIN users u_ag ON t.assigned_to = u_ag.id
LEFT JOIN teams tm ON t.team_id = tm.id
WHERE t.deleted_at IS NULL;
```

**Uso em Laravel:**

```php
// Antes (query complexa em Controller)
$tickets = Ticket::with(['requester', 'assignedAgent', 'team'])
 ->withCount('comments')
 ->where('team_id', $teamId)
 ->get()
 ->map(function($ticket) {
 $ticket->is_overdue = $ticket->resolution_deadline < now()
 && in_array($ticket->status, ['open', 'in_progress']);
 return $ticket;
 });

// Depois (simples com View!)
$tickets = DB::table('v_ticket_dashboard')
 ->where('team_id', $teamId)
 ->orderBy('is_overdue', 'desc')
 ->get();
// ✅ Mais simples, mais rápido!
```

### VIEW 2: v_sla_compliance (Relatório SLA)

**Problema:** Calcular SLA compliance requer lógica complexa (deadlines, timestamps).

**Solução:** View com CASE statements pré-calculados.

```sql
CREATE OR REPLACE VIEW v_sla_compliance AS
SELECT
 t.id,
 t.ticket_number,
 t.priority,
 CASE
 WHEN t.first_response_at <= t.first_response_deadline THEN 'MET'
 WHEN t.first_response_at > t.first_response_deadline THEN 'BREACHED'
 WHEN t.first_response_at IS NULL AND NOW() > t.first_response_deadline THEN 'BREACHED'
 ELSE 'PENDING'
 END AS first_response_sla_status,
 CASE
 WHEN t.resolved_at <= t.resolution_deadline THEN 'MET'
 WHEN t.resolved_at > t.resolution_deadline THEN 'BREACHED'
 WHEN t.resolved_at IS NULL AND NOW() > t.resolution_deadline THEN 'BREACHED'
 ELSE 'PENDING'
 END AS resolution_sla_status
FROM tickets t
WHERE t.deleted_at IS NULL;
```

**Uso em Laravel:**

```php
// Relatório mensal SLA por priority
$slaReport = DB::table('v_sla_compliance')
 ->selectRaw('
 priority,
 COUNT(*) as total,
 SUM(CASE WHEN resolution_sla_status = "MET" THEN 1 ELSE 0 END) as met,
 SUM(CASE WHEN resolution_sla_status = "BREACHED" THEN 1 ELSE 0 END) as breached
 ')
 ->whereMonth('created_at', now()->month)
 ->groupBy('priority')
 ->get();

// Resultado:
// [
// {priority: 'urgent', total: 45, met: 40, breached: 5},
// {priority: 'high', total: 120, met: 110, breached: 10},
// ]
```

### VIEW 3: v_agent_performance (Métricas de Agent)

**Problema:** Calcular performance de agents requer agregações complexas.

**Solução:** View com AVG, COUNT, GROUP BY pré-calculados.

```sql
CREATE OR REPLACE VIEW v_agent_performance AS
SELECT
 u.id AS agent_id,
 u.name AS agent_name,
 COUNT(DISTINCT t.id) AS total_tickets,
 COUNT(DISTINCT CASE WHEN t.status = 'resolved' THEN t.id END) AS resolved_tickets,
 AVG(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600) AS avg_resolution_hours,
 COUNT(DISTINCT CASE WHEN t.resolved_at <= t.resolution_deadline THEN t.id END) AS sla_met_count
FROM users u
LEFT JOIN tickets t ON u.id = t.assigned_to
WHERE u.deleted_at IS NULL
GROUP BY u.id, u.name;
```

**Uso em Laravel:**

```php
// Ranking de top 10 agents
$topAgents = DB::table('v_agent_performance')
 ->where('total_tickets', '>', 10) // Mínimo 10 tickets
 ->orderBy('avg_resolution_hours', 'asc') // Mais rápidos primeiro
 ->limit(10)
 ->get();
```

**Performance Tip:**

- Views são queries "ao vivo" (sempre dados atuais)
- Se View demorar >2s, considerar **Materialized View** (cache pré-computado)

---

## 7. DATABASE TRIGGERS (Automação)

### O que são Triggers?

**Triggers** são código SQL que executa **automaticamente** quando algo acontece (INSERT, UPDATE, DELETE).

É como "event listeners" no Laravel, mas **no banco de dados**!

### Porque usar Triggers?

- **Automação**: Zero código PHP para lógica repetitiva
- **Performance**: Executa no DB (sem round-trip PHP ↔ PostgreSQL)
- **Data Integrity**: Garantir regras mesmo se bypass Laravel
- **Auditoria**: Log automático de mudanças

### TRIGGER 1: Auto-gerar ticket_number

**Problema:** Todo ticket precisa de número único no formato `TKT-20251111-0001`.

**Sem Trigger (código PHP):**

```php
// Controller
$date = now()->format('Ymd');
$count = Ticket::whereDate('created_at', today())->count() + 1;
$ticketNumber = "TKT-{$date}-" . str_pad($count, 4, '0', STR_PAD_LEFT);

Ticket::create([
 'ticket_number' => $ticketNumber,
 'title' => $request->title,
 // ...
]);
// ❌ Código repetido, race condition possível
```

**Com Trigger (automático!):**

```sql
CREATE OR REPLACE FUNCTION generate_ticket_number()
RETURNS TRIGGER AS $$
DECLARE
 date_prefix TEXT;
 seq_num INTEGER;
BEGIN
 IF NEW.ticket_number IS NOT NULL THEN
 RETURN NEW; -- Já definido
 END IF;

 date_prefix := TO_CHAR(NOW(), 'YYYYMMDD');

 SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_number FROM 13) AS INTEGER)), 0) + 1
 INTO seq_num
 FROM tickets
 WHERE ticket_number LIKE 'TKT-' || date_prefix || '-%';

 NEW.ticket_number := 'TKT-' || date_prefix || '-' || LPAD(seq_num::TEXT, 4, '0');
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_generate_ticket_number
BEFORE INSERT ON tickets
FOR EACH ROW
WHEN (NEW.ticket_number IS NULL)
EXECUTE FUNCTION generate_ticket_number();
```

**Uso em Laravel (simplificado):**

```php
// Controller - Zero lógica de ticket_number!
Ticket::create([
 'title' => $request->title,
 'description' => $request->description,
 // ticket_number gerado automaticamente pelo trigger!
]);

// Resultado: TKT-20251111-0001, TKT-20251111-0002, ...
```

### TRIGGER 2: Auto-calcular SLA deadlines

**Problema:** Cada priority tem SLA diferente (urgent=2h, high=4h, etc).

**Sem Trigger:**

```php
// Service
$firstResponseDeadline = match($priority) {
 'urgent' => now()->addHours(2),
 'high' => now()->addHours(4),
 'medium' => now()->addHours(8),
 'low' => now()->addHours(24),
};

$resolutionDeadline = match($priority) {
 'urgent' => now()->addHours(8),
 'high' => now()->addDays(2),
 'medium' => now()->addDays(5),
 'low' => now()->addDays(10),
};
// ❌ Lógica repetida, precisa testar tudo
```

**Com Trigger:**

```sql
CREATE OR REPLACE FUNCTION set_sla_deadlines()
RETURNS TRIGGER AS $$
BEGIN
 NEW.first_response_deadline := NEW.created_at +
 CASE NEW.priority
 WHEN 'urgent' THEN INTERVAL '2 hours'
 WHEN 'high' THEN INTERVAL '4 hours'
 WHEN 'medium' THEN INTERVAL '8 hours'
 WHEN 'low' THEN INTERVAL '24 hours'
 END;

 NEW.resolution_deadline := NEW.created_at +
 CASE NEW.priority
 WHEN 'urgent' THEN INTERVAL '8 hours'
 WHEN 'high' THEN INTERVAL '2 days'
 WHEN 'medium' THEN INTERVAL '5 days'
 WHEN 'low' THEN INTERVAL '10 days'
 END;

 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_sla_deadlines
BEFORE INSERT ON tickets
FOR EACH ROW
EXECUTE FUNCTION set_sla_deadlines();
```

**Uso em Laravel:**

```php
// Simples - SLA calculado automaticamente!
$ticket = Ticket::create([
 'title' => 'Server down',
 'priority' => 'urgent',
]);

// Resultado automático:
// first_response_deadline = created_at + 2 hours
// resolution_deadline = created_at + 8 hours
// ✅ Zero cálculos em PHP!
```

### TRIGGER 3: Validar agent assignment

**Problema:** Agent deve pertencer ao Team do ticket.

**Sem Trigger:**

```php
// Form Request
public function rules() {
 return [
 'assigned_to' => [
 'required',
 'exists:users,id',
 function ($attribute, $value, $fail) {
 $teamId = $this->input('team_id');
 $exists = DB::table('team_user')
 ->where('user_id', $value)
 ->where('team_id', $teamId)
 ->exists();
 if (!$exists) {
 $fail('Agent não pertence ao team.');
 }
 },
 ],
 ];
}
// ❌ Validação complexa, pode ser bypass em console/seed
```

**Com Trigger (garantido sempre!):**

```sql
CREATE OR REPLACE FUNCTION validate_ticket_assignment()
RETURNS TRIGGER AS $$
BEGIN
 IF NEW.assigned_to IS NULL THEN
 RETURN NEW;
 END IF;

 IF NOT EXISTS (
 SELECT 1 FROM team_user
 WHERE user_id = NEW.assigned_to AND team_id = NEW.team_id
 ) THEN
 RAISE EXCEPTION 'User % não pertence ao Team %', NEW.assigned_to, NEW.team_id;
 END IF;

 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_ticket_assignment
BEFORE INSERT OR UPDATE OF assigned_to, team_id ON tickets
FOR EACH ROW
WHEN (NEW.assigned_to IS NOT NULL)
EXECUTE FUNCTION validate_ticket_assignment();
```

**Benefício:**

- Data integrity **GARANTIDA** mesmo em:
 - Tinker/Console
 - Seeds
 - Direct SQL
 - APIs sem validation

### TRIGGER 4: Log automático de status changes

**Problema:** Toda mudança de status deve ser registada em `activity_log`.

**Sem Trigger:**

```php
// Controller
$oldStatus = $ticket->status;
$ticket->update(['status' => 'resolved']);

activity()
 ->performedOn($ticket)
 ->withProperties(['old_status' => $oldStatus, 'new_status' => 'resolved'])
 ->log('status_changed');
// ❌ Código repetido em vários lugares, fácil esquecer
```

**Com Trigger:**

```sql
CREATE OR REPLACE FUNCTION log_ticket_status_change()
RETURNS TRIGGER AS $$
BEGIN
 IF OLD.status IS DISTINCT FROM NEW.status THEN
 INSERT INTO activity_log (
 log_name, description, subject_type, subject_id,
 properties, created_at, updated_at
 ) VALUES (
 'ticket',
 'status_changed',
 'App\Models\Ticket',
 NEW.id,
 jsonb_build_object('old_status', OLD.status, 'new_status', NEW.status),
 NOW(), NOW()
 );
 END IF;
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_ticket_status_change
AFTER UPDATE ON tickets
FOR EACH ROW
EXECUTE FUNCTION log_ticket_status_change();
```

**Uso em Laravel:**

```php
// Simples - log automático!
$ticket->update(['status' => 'resolved']);
// ✅ activity_log atualizado automaticamente pelo trigger!

// Consultar histórico
$statusHistory = Activity::forSubject($ticket)
 ->where('description', 'status_changed')
 ->get();
```

**Performance:** Triggers executam em **microsegundos** (não milissegundos).

---

## 8. STORED PROCEDURES (Lógica Complexa)

### O que são Stored Procedures?

**Stored Procedures** são **funções SQL** guardadas no banco de dados. Como "methods" PHP, mas no PostgreSQL!

### Porque usar Stored Procedures?

- **Performance**: Lógica executada no DB (menos round-trips)
- **Reutilização**: Chamado de Laravel, Python, Java, etc.
- **Transações**: ACID garantido
- **Segurança**: Expor apenas procedures (não tabelas diretas)

### PROCEDURE 1: assign_ticket_auto()

**Problema:** Atribuir ticket ao agent menos ocupado de um team.

**Sem Procedure:**

```php
// Service
$agent = User::role('agent')
 ->whereHas('teams', fn($q) => $q->where('teams.id', $teamId))
 ->withCount(['assignedTickets' => fn($q) =>
 $q->whereIn('status', ['open', 'in_progress'])
 ])
 ->orderBy('assigned_tickets_count')
 ->first();

if ($agent) {
 $ticket->update(['assigned_to' => $agent->id, 'team_id' => $teamId]);
}
// ❌ Query complexa, múltiplas round-trips
```

**Com Stored Procedure:**

```sql
CREATE OR REPLACE FUNCTION assign_ticket_auto(
 p_ticket_id BIGINT,
 p_team_id BIGINT
) RETURNS BIGINT AS $$
DECLARE
 v_agent_id BIGINT;
BEGIN
 SELECT u.id INTO v_agent_id
 FROM users u
 JOIN team_user tu ON u.id = tu.user_id
 LEFT JOIN tickets t ON t.assigned_to = u.id
 AND t.status IN ('open', 'in_progress')
 WHERE tu.team_id = p_team_id
 AND u.is_active = true
 GROUP BY u.id
 ORDER BY COUNT(t.id) ASC, RANDOM()
 LIMIT 1;

 IF v_agent_id IS NOT NULL THEN
 UPDATE tickets
 SET assigned_to = v_agent_id, team_id = p_team_id
 WHERE id = p_ticket_id;
 END IF;

 RETURN v_agent_id;
END;
$$ LANGUAGE plpgsql;
```

**Uso em Laravel:**

```php
// Service
$agentId = DB::selectOne('SELECT assign_ticket_auto(?, ?)', [$ticketId, $teamId])->assign_ticket_auto;

activity()->log("Auto-assigned to agent {$agentId}");
// ✅ 1 chamada DB vs 3-4 queries
```

### PROCEDURE 2: generate_sla_report()

**Problema:** Gerar relatório SLA agregado (por priority, team, período).

**Sem Procedure:**

```php
// Controller - query gigante
$report = Ticket::selectRaw('
 priority,
 COUNT(*) as total,
 SUM(CASE WHEN first_response_at <= first_response_deadline THEN 1 ELSE 0 END) as fr_met,
 SUM(CASE WHEN resolved_at <= resolution_deadline THEN 1 ELSE 0 END) as res_met
')
 ->whereBetween('created_at', [$startDate, $endDate])
 ->where('team_id', $teamId)
 ->groupBy('priority')
 ->get();
// ❌ SQL complexo misturado com PHP
```

**Com Stored Procedure:**

```sql
CREATE OR REPLACE FUNCTION generate_sla_report(
 p_start_date TIMESTAMP,
 p_end_date TIMESTAMP,
 p_team_id BIGINT DEFAULT NULL
)
RETURNS TABLE (
 priority VARCHAR,
 total_tickets BIGINT,
 first_response_met BIGINT,
 resolution_met BIGINT,
 avg_resolution_hours NUMERIC
) AS $$
BEGIN
 RETURN QUERY
 SELECT
 t.priority,
 COUNT(*)::BIGINT,
 COUNT(CASE WHEN t.first_response_at <= t.first_response_deadline THEN 1 END)::BIGINT,
 COUNT(CASE WHEN t.resolved_at <= t.resolution_deadline THEN 1 END)::BIGINT,
 ROUND(AVG(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600), 2)::NUMERIC
 FROM tickets t
 WHERE t.created_at BETWEEN p_start_date AND p_end_date
 AND (p_team_id IS NULL OR t.team_id = p_team_id)
 GROUP BY t.priority;
END;
$$ LANGUAGE plpgsql STABLE;
```

**Uso em Laravel:**

```php
// Controller - super simples!
$slaReport = DB::select('SELECT * FROM generate_sla_report(?, ?, ?)', [
 now()->startOfMonth(),
 now()->endOfMonth(),
 $teamId // ou NULL para todos
]);

return view('reports.sla', compact('slaReport'));
// ✅ SQL limpo, reutilizável, testável isoladamente
```

**Benefício:** Procedure pode ser testada diretamente no PostgreSQL (sem Laravel).

---

## 9. CHECK CONSTRAINTS (Validação em DB)

### O que são Check Constraints?

**Check Constraints** são **regras de validação** no banco de dados. Como "validation rules" do Laravel, mas **no PostgreSQL**!

### Porque usar Check Constraints?

- **Dupla proteção**: Laravel valida + PostgreSQL valida
- **Data integrity**: Impossível inserir dados inválidos (mesmo via SQL direto)
- **Performance**: Validação no DB é instantânea
- **Documentação**: Schema autodocumentado (constraints explícitos)

### Exemplo 1: Validar ENUM values

```sql
-- Status deve ser um dos valores permitidos
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_status
 CHECK (status IN ('open', 'in_progress', 'on_hold', 'resolved', 'closed'));

-- Priority deve ser válido
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_priority
 CHECK (priority IN ('low', 'medium', 'high', 'urgent'));
```

**Benefício:**

```php
// Tentativa de inserir status inválido
Ticket::create([
 'status' => 'invalid_status', // ❌
]);
// PostgreSQL EXCEPTION: new row for relation "tickets" violates check constraint "chk_tickets_status"
// ✅ Impossível burlar validation!
```

### Exemplo 2: Validar datas lógicas

```sql
-- resolved_at deve ser posterior a created_at
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_resolved_date
 CHECK (resolved_at IS NULL OR resolved_at >= created_at);

-- closed_at deve ser posterior a resolved_at
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_closed_date
 CHECK (closed_at IS NULL OR closed_at >= resolved_at);
```

### Exemplo 3: Validar contadores não negativos

```sql
-- Views, helpful_count não podem ser negativos
ALTER TABLE articles ADD CONSTRAINT chk_articles_views
 CHECK (views >= 0);

ALTER TABLE articles ADD CONSTRAINT chk_articles_helpful
 CHECK (helpful_count >= 0 AND not_helpful_count >= 0);
```

### Exemplo 4: Validar formato de email

```sql
-- Email deve ter formato válido
ALTER TABLE users ADD CONSTRAINT chk_users_email_format
 CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
```

**Comparação:**

| Validação | Laravel Form Request | PostgreSQL Check Constraint |
| --------------- | ---------------------- | --------------------------- |
| **Quando** | HTTP requests | INSERT/UPDATE sempre |
| **Bypass?** | Console, Tinker, Seeds | ❌ NUNCA |
| **Performance** | ~5ms | ~0.01ms (instantâneo) |
| **Mensagens** | Customizáveis | Generic SQL error |

**Best Practice:** Usar **AMBOS**!

- Laravel: User-friendly error messages
- PostgreSQL: Ultimate protection

---

## 10. INDEXES AVANÇADOS

### Partial Indexes (Conditional)

**O que são:** Indexes apenas para subset de rows (com WHERE clause).

**Problema:** Index em `tickets.status` indexa TODOS os tickets (incluindo fechados).

**Solução:** Index apenas tickets ATIVOS!

```sql
-- Index apenas tickets ativos (não fechados)
CREATE INDEX idx_tickets_active_status ON tickets(status, priority)
 WHERE deleted_at IS NULL AND status NOT IN ('closed');
```

**Benefício:**

- Index 50% mais pequeno (tickets fechados excluídos)
- Queries em tickets ativos 2x mais rápidas

### Composite Indexes (Multi-Column)

**O que são:** Indexes em múltiplas colunas (para queries JOIN/WHERE complexas).

```sql
-- Dashboard: Filtrar por team + status + ordenar por created_at
CREATE INDEX idx_tickets_team_status_created ON tickets(team_id, status, created_at DESC)
 WHERE deleted_at IS NULL;
```

**Query otimizada:**

```sql
SELECT * FROM tickets
WHERE team_id = 5 AND status = 'open' AND deleted_at IS NULL
ORDER BY created_at DESC;
-- ✅ Usa idx_tickets_team_status_created (super rápido!)
```

### Expression Indexes (Calculated Columns)

**O que são:** Indexes em expressões SQL (não apenas colunas).

```sql
-- Buscar artigos por helpfulness percentage (calculado)
CREATE INDEX idx_articles_helpfulness ON articles((
 CASE
 WHEN (helpful_count + not_helpful_count) > 0
 THEN helpful_count::NUMERIC / (helpful_count + not_helpful_count)
 ELSE 0
 END
)) WHERE is_published = true;
```

**Query otimizada:**

```sql
SELECT * FROM articles
WHERE (helpful_count::NUMERIC / (helpful_count + not_helpful_count)) > 0.8
 AND is_published = true;
-- ✅ Usa idx_articles_helpfulness
```

---

## 5. BACKUP & RESTORE

### Backup PostgreSQL:

```bash
# Backup completo
pg_dump -U postgres -d orionone -F c -f backup.dump

# Backup apenas schema
pg_dump -U postgres -d orionone --schema-only -f schema.sql

# Backup apenas dados
pg_dump -U postgres -d orionone --data-only -f data.sql
```

### Restore:

```bash
pg_restore -U postgres -d orionone_new backup.dump
```

### Backup Redis:

```bash
# Redis faz snapshots automáticos (RDB)
# config/redis.conf
save 900 1 # Salva se 1 key mudou em 15min
save 300 10 # Salva se 10 keys mudaram em 5min
save 60 10000 # Salva se 10k keys mudaram em 1min
```

---

---

## RESUMO: Stack Base de Dados (Enterprise-Grade)

| Tecnologia | Propósito | Exemplo de Uso |
| ---------------------- | ------------------------------ | ----------------------------------------- |
| **PostgreSQL 16** | Base de dados relacional | Tickets, Users, Teams |
| **JSONB** | Dados flexíveis indexáveis | Metadata, Custom Fields |
| **Full-Text Search** | Pesquisa inteligente | Buscar tickets/artigos (português) |
| **Arrays** | Listas nativas | Tags, Permissions |
| **Window Functions** | Analytics avançadas | Rankings, Comparações |
| **Database Views** | Queries pré-computadas | Dashboard, SLA Reports, Agent Performance |
| **Triggers** | Automação (ticket_number, SLA) | Auto-gerar, Auto-calcular, Auto-validar |
| **Stored Procedures** | Lógica complexa reutilizável | assign_ticket_auto(), SLA reports |
| **Check Constraints** | Validação em DB | Status enum, datas lógicas, email format |
| **Partial Indexes** | Indexes condicionais | Apenas tickets ativos (performance) |
| **Composite Indexes** | Multi-column indexes | team_id + status + created_at |
| **Expression Indexes** | Indexes em cálculos | Helpfulness percentage |
| **Redis 7** | Cache + Queues | Cache de queries, Jobs assíncronos |
| **Laravel Cache** | Abstração Redis | Cache::remember() |
| **Laravel Queue** | Jobs assíncronos | Emails, Notifications |

---

## Stack Levels (Arquitetura)

```
┌─────────────────────────────────────────────────┐
│ LARAVEL (PHP 8.3) │
│ ├─ Eloquent Models │
│ ├─ Query Builder │
│ └─ Cache Facade (Redis) │
└─────────────────┬───────────────────────────────┘
 │
┌─────────────────▼───────────────────────────────┐
│ DATABASE LAYER (PostgreSQL 16) │
│ ├─ Tables (10 principais + Spatie + Sistema) │
│ ├─ Views (Dashboard, SLA, Performance, KB) │
│ ├─ Triggers (ticket_number, SLA, validation) │
│ ├─ Stored Procedures (auto-assign, reports) │
│ ├─ Check Constraints (enums, dates, format) │
│ └─ Indexes (Partial, Composite, Expression) │
└──────────────────────────────────────────────────┘
```

---

## Performance Checklist (Sempre Seguir!)

✅ **Indexes:**

1. Foreign keys sempre indexadas
2. Status/Priority (queries frequentes)
3. Timestamps (ordenação)
4. JSONB fields (GIN index)
5. Full-text search (GIN index português)
6. Partial indexes (WHERE clauses específicos)
7. Composite indexes (múltiplas colunas em WHERE/JOIN)

✅ **Queries:**

1. Eager load relationships (`with()`) - evita N+1
2. Select apenas colunas necessárias (não `SELECT *`)
3. Cache queries lentas (`Cache::remember()`)
4. Chunk datasets grandes (`chunk(1000)`)
5. Use Views para queries complexas repetidas

✅ **Automação:**

1. Triggers para lógica repetitiva (ticket_number, SLA)
2. Stored Procedures para lógica complexa reutilizável
3. Check Constraints para validação crítica

✅ **Cache:**

1. Redis para cache de queries (`ttl: 3600`)
2. Tags para invalidação seletiva
3. Queues para operações assíncronas (emails)

✅ **Monitoring:**

1. `DB::enableQueryLog()` em desenvolvimento
2. Laravel Telescope para queries lentas
3. PostgreSQL `EXPLAIN ANALYZE` para optimization

---

## Próximo Guia

- **[TECH-DEEP-DIVE-DEVOPS.md](./TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx, Deploy

---

**Performance Tips:**

1. Sempre usa indexes em foreign keys
2. Eager load relationships (evita N+1)
3. Cache queries lentas (Redis)
4. Usa queues para emails/notificações
5. Chunk datasets grandes
6. Full-text search para pesquisas
7. JSONB para dados flexíveis
