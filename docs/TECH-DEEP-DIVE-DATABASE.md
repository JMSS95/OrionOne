# 🗄️ Tech Deep Dive - Base de Dados (PostgreSQL/Redis)

> **Guia Completo**: Como funciona a camada de dados do OrionOne - PostgreSQL 16, Redis 7, Queues, Cache

---

## 🐘 1. POSTGRESQL 16 (Base de Dados Relacional)

### O que é?

**PostgreSQL** é uma base de dados relacional open-source. É como MySQL, mas com **mais features avançadas**.

### Porque PostgreSQL (não MySQL)?

| Feature              | PostgreSQL ✅     | MySQL ❌         |
| -------------------- | ----------------- | ---------------- |
| **JSONB**            | Nativo, indexável | JSON simples     |
| **Full-Text Search** | Built-in (pt-PT!) | Precisa extensão |
| **Arrays**           | `tags TEXT[]`     | Não suporta      |
| **Window Functions** | Completo          | Limitado         |
| **CTEs Recursivos**  | Sim               | Sim (desde 8.0)  |
| **Transações ACID**  | Muito robusto     | Bom              |
| **Extensões**        | PostGIS, pg_trgm  | Menos opções     |

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

-   **Flexível**: Esquema dinâmico (sem ALTER TABLE)
-   **Indexável**: Queries rápidas em JSON
-   **Binário**: 20-30% mais rápido que JSON texto

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
name           | total_resolved | ranking
---------------|----------------|--------
João Silva     | 142            | 1
Maria Santos   | 138            | 2
Pedro Costa    | 105            | 3
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
team_name  | tickets_count | avg_tickets | diff
-----------|---------------|-------------|------
Suporte    | 450           | 300         | +150
Dev        | 250           | 300         | -50
Infra      | 200           | 300         | -100
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
id  | title                      | level
----|----------------------------|------
1   | Problema com servidor      | 1 (pai)
2   | ├─ Investigar logs         | 2 (filho)
3   | ├─ Verificar disco         | 2 (filho)
4   |    └─ Substituir HD        | 3 (neto)
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

-   ✅ 60 requests por minuto permitidos
-   ❌ 61º request → HTTP 429 Too Many Requests

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

-   Colunas em WHERE, JOIN, ORDER BY
-   Foreign keys
-   Colunas pesquisadas frequentemente

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
save 900 1      # Salva se 1 key mudou em 15min
save 300 10     # Salva se 10 keys mudaram em 5min
save 60 10000   # Salva se 10k keys mudaram em 1min
```

---

---

## RESUMO: Stack Base de Dados

| Tecnologia           | Propósito                |
| -------------------- | ------------------------ | ----------------------- |
| **PostgreSQL 16**    | Base de dados relacional | Tickets, Users, Teams   |
| **JSONB**            | Dados flexíveis          | Metadata, Custom Fields |
| **Full-Text Search** | Pesquisa inteligente     | Buscar tickets/artigos  |
| **Arrays**           | Listas nativas           | Tags, Permissions       |
| **Window Functions** | Analytics avançadas      | Rankings, Comparações   |
| **Redis 7**          | Cache + Queues           | Cache de queries, Jobs  |
| **Laravel Cache**    | Abstração Redis          | Cache::remember()       |
| **Laravel Queue**    | Jobs assíncronos         | Emails, Notifications   |

---

## Próximo Guia

-   **[TECH-DEEP-DIVE-DEVOPS.md](./TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx, Deploy

---

**Performance Tips:**

1. Sempre usa indexes em foreign keys
2. Eager load relationships (evita N+1)
3. Cache queries lentas (Redis)
4. Usa queues para emails/notificações
5. Chunk datasets grandes
6. Full-text search para pesquisas
7. JSONB para dados flexíveis
