# Tech Deep Dive - Backend (Laravel/PHP)

Guia Completo e Detalhado: O que cada biblioteca faz, como funciona, e porque usamos no OrionOne

---

## 1. LARAVEL FRAMEWORK (Nucleo do Backend)

### O que é?

**Laravel** é o framework PHP mais popular do mundo. Pensa nele como uma "caixa de ferramentas" gigante que já tem tudo o que precisas para construir aplicações web modernas.

### Porque usamos Laravel 12?

-   **Routing automático**: Define rotas URL → Controller numa linha
-   **Eloquent ORM**: Trabalhar com BD usando objetos (não SQL puro)
-   **Migrations**: Versionamento da estrutura da BD
-   **Blade Templates**: (não usamos, preferimos Inertia.js)
-   **Authentication**: Sistema de login pronto
-   **Queue Jobs**: Tarefas assíncronas (emails, processamento)
-   **Validation**: Validação de dados integrada
-   **Cache**: Redis/Memcached out-of-the-box

### Como funciona? (Ciclo de Vida de um Request)

```
1. Request chega (http://orionone.test/tickets)
   ↓
2. routes/web.php define: Route::get('/tickets', TicketController@index)
   ↓
3. Middleware executa (auth, CSRF, etc)
   ↓
4. Controller processa: TicketController::index()
   ↓
5. Service Layer: TicketService::getAll()
   ↓
6. Model: Ticket::query()->with('user')->paginate(20)
   ↓
7. Response: return Inertia::render('Tickets/Index', ['tickets' => $tickets])
   ↓
8. Inertia.js envia JSON para Vue.js renderizar
```

### Componentes Laravel que Usamos

#### **Eloquent ORM** (Base de Dados)

**O que é ORM?**
ORM significa "Object-Relational Mapping" - ou seja, permite trabalhar com a base de dados usando **objetos PHP** em vez de escrever SQL diretamente. Cada tabela da BD vira uma "classe" (Model), e cada linha vira um "objeto".

**Comparação: SQL Puro vs Eloquent**

```php
// SEM LARAVEL (SQL Puro - verboso e propenso a erros)
// Tens que escrever SQL manualmente, cuidar de SQL injection, fazer bind de parâmetros...
$pdo = new PDO('pgsql:host=localhost;dbname=orionone', 'user', 'pass');
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => 'test@email.com']);
$users = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Para acessar dados:
echo $users[0]['name']; // Array associativo

// COM ELOQUENT (elegante e seguro!)
// Laravel cuida de tudo: conexão, SQL injection protection, bind de parâmetros
$users = User::where('email', 'test@email.com')->get();

// Para acessar dados:
echo $users[0]->name; // Objeto com propriedades
```

**Relacionamentos Automáticos: A Magia do Eloquent**

Imagine que tens 2 tabelas:

-   `tickets` (id, title, user_id)
-   `users` (id, name, email)

```php
// SEM ELOQUENT: Tens que fazer JOINs manualmente
$ticket = DB::select('SELECT * FROM tickets WHERE id = ?', [1])[0];
$user = DB::select('SELECT * FROM users WHERE id = ?', [$ticket['user_id']])[0];

echo "Ticket criado por: " . $user['name'];

// COM ELOQUENT: Relacionamentos automáticos!
// No Model Ticket.php definiste uma vez:
// public function user() { return $this->belongsTo(User::class); }

$ticket = Ticket::find(1);
echo "Ticket criado por: " . $ticket->user->name;
// O Laravel faz o JOIN automaticamente quando acedes a $ticket->user!

// Relacionamento inverso (1 user tem muitos tickets)
$user = User::find(1);
foreach ($user->tickets as $ticket) {
    echo $ticket->title; // Laravel busca automaticamente todos os tickets deste user
}
```

**Eager Loading: Evitar o Problema N+1**

```php
// PROBLEMA N+1 (Muito lento! Faz 101 queries)
$tickets = Ticket::all(); // 1 query: SELECT * FROM tickets

foreach ($tickets as $ticket) {
    echo $ticket->user->name; // 100 queries: SELECT * FROM users WHERE id = X
}
// Total: 1 + 100 = 101 queries para buscar 100 tickets!

// SOLUÇÃO: Eager Loading (Faz apenas 2 queries)
$tickets = Ticket::with('user')->get();
// Query 1: SELECT * FROM tickets
// Query 2: SELECT * FROM users WHERE id IN (1, 2, 3, ..., 100)

foreach ($tickets as $ticket) {
    echo $ticket->user->name; // Já está carregado! Sem query adicional!
}
// Total: 2 queries!
```

**Soft Deletes: "Apagar" sem Apagar**

```php
// No Model Ticket.php:
use SoftDeletes;

// Na migration:
$table->softDeletes(); // Adiciona coluna "deleted_at"

// Quando "apagares":
$ticket->delete(); // NÃO apaga da BD, apenas marca deleted_at = now()

// Queries normais ignoram tickets apagados:
Ticket::all(); // Apenas tickets com deleted_at = NULL

// Para incluir apagados:
Ticket::withTrashed()->get(); // Inclui apagados
Ticket::onlyTrashed()->get(); // Apenas apagados

// Para restaurar:
$ticket->restore(); // deleted_at = NULL

// Para apagar definitivamente:
$ticket->forceDelete(); // DELETE FROM tickets WHERE id = X
```

**Scopes: Queries Reutilizáveis**

```php
// No Model Ticket.php:
public function scopeOpen($query)
{
    return $query->where('status', 'open');
}

public function scopeUrgent($query)
{
    return $query->where('priority', 'urgent');
}

public function scopeAssignedTo($query, User $user)
{
    return $query->where('assigned_to', $user->id);
}

// Uso (queries encadeáveis!):
Ticket::open()->urgent()->get(); // Tickets abertos E urgentes
Ticket::assignedTo($user)->get(); // Tickets atribuídos a um user específico
Ticket::open()->assignedTo($user)->oldest()->get(); // Tickets abertos do user, ordenados por mais antigos
```

**Porque Eloquent é Poderoso?**

1. **Produtividade**: Menos código, mais legível
2. **Segurança**: Protection contra SQL injection automática
3. **Manutenibilidade**: Mudanças na BD refletem nos Models
4. **Relacionamentos**: JOINs complexos viram `$ticket->user->team->name`
5. **Eventos**: Hooks automáticos (creating, created, updating, updated, deleting, deleted)
6. **Casting**: `'status' => 'array'` converte JSON automaticamente

#### **Migrations** (Versionamento de Base de Dados)

**O que são Migrations?**
Migrations são como "commits do Git" mas para a estrutura da base de dados. Em vez de escrever SQL manualmente no servidor, defines a estrutura em **código PHP** que pode ser versionado, revertido, e executado em qualquer ambiente.

**Problema que Resolve:**

```
SEM MIGRATIONS (Caótico):
1. Dev A cria tabela `tickets` manualmente no phpMyAdmin
2. Dev B não sabe e tenta usar a tabela → ERRO
3. Em produção, tabela não existe → APLICAÇÃO QUEBRA
4. Ninguém sabe qual foi a última estrutura
5. Impossível reverter mudanças

COM MIGRATIONS (Organizado):
1. Dev A cria migration: CreateTicketsTable.php
2. Commit no Git
3. Dev B faz pull → php artisan migrate (tabela criada automaticamente)
4. Em produção: php artisan migrate (estrutura sincronizada)
5. Rollback fácil: php artisan migrate:rollback
```

**Anatomia de uma Migration:**

```php
// database/migrations/2025_11_11_000001_create_tickets_table.php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * Este método é executado quando fazes:
     * php artisan migrate
     *
     * Define COMO criar a estrutura da tabela.
     */
    public function up(): void
    {
        Schema::create('tickets', function (Blueprint $table) {
            // Primary Key (auto-increment)
            // SQL: id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
            $table->id();

            // Ticket Number (único, indexado)
            // SQL: ticket_number VARCHAR(255) UNIQUE
            // Exemplo: "TKT-000001", "TKT-000002"
            $table->string('ticket_number')->unique();

            // Foreign Key para tabela users
            // SQL: user_id BIGINT UNSIGNED, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            // ON DELETE CASCADE = se user é apagado, tickets dele também são
            $table->foreignId('user_id')
                  ->constrained()           // Cria FK automaticamente
                  ->onDelete('cascade');    // Apaga tickets se user for apagado

            // Campos de texto
            // SQL: title VARCHAR(255), description TEXT
            $table->string('title');              // Até 255 caracteres
            $table->text('description');          // Texto longo (sem limite prático)

            // Enum: Apenas valores específicos permitidos
            // SQL: status ENUM('open', 'in_progress', 'resolved', 'closed')
            $table->enum('status', ['open', 'in_progress', 'resolved', 'closed'])
                  ->default('open');        // Valor padrão quando criar ticket

            // Outro Enum para prioridade
            $table->enum('priority', ['low', 'medium', 'high', 'urgent'])
                  ->default('medium');

            // Foreign Key opcional (pode ser NULL)
            // SQL: assigned_to BIGINT UNSIGNED NULL, FOREIGN KEY...
            $table->foreignId('assigned_to')
                  ->nullable()              // Pode ser NULL (ticket não atribuído)
                  ->constrained('users')    // FK para tabela users
                  ->nullOnDelete();         // Se user for apagado, assigned_to = NULL

            // Metadata em JSONB (PostgreSQL)
            // SQL: metadata JSONB NULL
            // Permite armazenar dados flexíveis: {"ip": "192.168.1.1", "device": "mobile"}
            $table->jsonb('metadata')->nullable();

            // Timestamps automáticos (created_at, updated_at)
            // Laravel preenche automaticamente
            $table->timestamps();

            // Soft Deletes (deleted_at)
            // Permite "apagar" sem realmente apagar
            $table->softDeletes();

            // Índices para performance
            // SQL: CREATE INDEX tickets_status_priority_index ON tickets(status, priority)
            $table->index(['status', 'priority']); // Queries por status+priority ficam rápidas
            $table->index('created_at');            // Ordenar por data fica rápido
        });
    }

    /**
     * Reverse the migrations.
     *
     * Este método é executado quando fazes:
     * php artisan migrate:rollback
     *
     * Define COMO desfazer a migration (voltar atrás).
     * Normalmente é só DROP TABLE.
     */
    public function down(): void
    {
        Schema::dropIfExists('tickets');
    }
};
```

**Comandos de Migration:**

```bash
# Criar nova migration
php artisan make:migration create_tickets_table
php artisan make:migration add_priority_to_tickets_table

# Executar migrations pendentes
php artisan migrate
# Output:
# Migrating: 2025_11_11_000001_create_tickets_table
# Migrated:  2025_11_11_000001_create_tickets_table (45.23ms)

# Ver status (quais já foram executadas)
php artisan migrate:status
# Output:
# ┌─────────────────────────────────────────────────────┬─────────┐
# │ Migration                                           │ Ran?    │
# ├─────────────────────────────────────────────────────┼─────────┤
# │ 2014_10_12_000000_create_users_table              │ Yes     │
# │ 2025_11_11_000001_create_tickets_table            │ Yes     │
# │ 2025_11_11_000002_add_priority_to_tickets_table   │ No      │
# └─────────────────────────────────────────────────────┴─────────┘

# Rollback última migration
php artisan migrate:rollback
# Output: Dropped table 'tickets'

# Rollback TUDO (cuidado em produção!)
php artisan migrate:reset

# Fresh: DROP tudo e recria do zero
php artisan migrate:fresh
# Útil em desenvolvimento, NUNCA em produção!

# Fresh + Seeds (com dados de teste)
php artisan migrate:fresh --seed
```

**Modificar Tabelas Existentes:**

```php
// database/migrations/2025_11_12_add_priority_to_tickets.php
public function up(): void
{
    Schema::table('tickets', function (Blueprint $table) {
        // Adicionar coluna nova
        $table->enum('priority', ['low', 'medium', 'high', 'urgent'])
              ->default('medium')
              ->after('status'); // Adiciona DEPOIS da coluna 'status'

        // Adicionar índice
        $table->index('priority');
    });
}

public function down(): void
{
    Schema::table('tickets', function (Blueprint $table) {
        // Remover índice primeiro (sempre antes de remover coluna)
        $table->dropIndex(['priority']);

        // Remover coluna
        $table->dropColumn('priority');
    });
}
```

**Modificar Colunas Existentes (requer doctrine/dbal):**

```bash
# Instalar package necessário
composer require doctrine/dbal
```

```php
public function up(): void
{
    Schema::table('tickets', function (Blueprint $table) {
        // Mudar tipo de coluna
        $table->text('title')->change(); // VARCHAR(255) → TEXT

        // Tornar coluna nullable
        $table->string('assigned_to')->nullable()->change();

        // Renomear coluna
        $table->renameColumn('description', 'body');
    });
}
```

**Migrations com Dados (Seeders):**

```php
// database/seeders/DatabaseSeeder.php
public function run(): void
{
    // Criar users
    User::factory(10)->create();

    // Criar admin
    User::create([
        'name' => 'Admin',
        'email' => 'admin@orionone.test',
        'password' => bcrypt('password'),
    ]);

    // Criar tickets
    Ticket::factory(50)->create();
}
```

```bash
# Executar seeders
php artisan db:seed

# Ou tudo junto (migrations + seeds)
php artisan migrate:fresh --seed
```

**Vantagens das Migrations:**

1. **Versionamento**: Estrutura da BD no Git
2. **Reprodutibilidade**: Qualquer dev pode recriar BD localmente
3. **Rollback**: Voltar atrás se algo correr mal
4. **Documentação**: Código mostra evolução da BD
5. **CI/CD**: Automated deployment atualiza BD automaticamente
6. **Zero-downtime**: Migrations podem ser escritas para não quebrar app em produção

#### **Validation** (Validação de Dados de Entrada)

**O que é Validation?**
Validação é o processo de **verificar se os dados que o utilizador enviou são válidos** antes de os processar. Por exemplo: email tem formato correto? Password tem 8+ caracteres? Ficheiro é uma imagem?

**Problema que Resolve:**

```php
// SEM VALIDAÇÃO (Perigoso e verboso):
public function store(Request $request)
{
    // Tens que validar TUDO manualmente
    if (empty($request->input('title'))) {
        return back()->with('error', 'Título é obrigatório');
    }

    if (strlen($request->input('title')) < 5) {
        return back()->with('error', 'Título deve ter 5+ caracteres');
    }

    if (strlen($request->input('title')) > 255) {
        return back()->with('error', 'Título não pode ter mais de 255 caracteres');
    }

    $email = $request->input('email');
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return back()->with('error', 'Email inválido');
    }

    // ... dezenas de linhas de validação

    // Se chegou aqui, dados são válidos
    Ticket::create($request->all());
}

// COM LARAVEL VALIDATION (Limpo e seguro):
public function store(StoreTicketRequest $request)
{
    // Laravel já validou TUDO! Se chegou aqui, dados são 100% válidos
    Ticket::create($request->validated());
}
```

**Form Request: Validação Organizada**

```php
// app/Http/Requests/StoreTicketRequest.php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreTicketRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * Este método verifica se o utilizador TEM PERMISSÃO para fazer este request.
     * Retorna TRUE = autorizado, FALSE = HTTP 403 Forbidden
     */
    public function authorize(): bool
    {
        // Qualquer utilizador autenticado pode criar ticket
        return $this->user() !== null;

        // Exemplos de autorização mais complexa:
        // return $this->user()->can('create-ticket'); // Via Policy
        // return $this->user()->hasRole('agent'); // Via Spatie Permission
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * Define as REGRAS de validação. Laravel valida automaticamente!
     * Se falhar → HTTP 422 com erros em JSON
     * Se passar → continua para o Controller
     */
    public function rules(): array
    {
        return [
            // Campo obrigatório, tipo string, entre 5 e 255 caracteres
            'title' => [
                'required',      // Não pode estar vazio
                'string',        // Tem que ser texto (não array, não number)
                'min:5',         // Mínimo 5 caracteres
                'max:255',       // Máximo 255 caracteres
            ],

            // Descrição: obrigatória, string, mínimo 20 caracteres
            'description' => 'required|string|min:20',

            // Prioridade: obrigatória, tem que ser um destes valores
            'priority' => [
                'required',
                'in:low,medium,high,urgent', // Apenas estes valores são aceites
            ],

            // Categoria: obrigatória, tem que existir na tabela categories
            'category_id' => [
                'required',
                'exists:categories,id', // Verifica se ID existe na BD
            ],

            // Attachments: opcional, array, cada item é ficheiro imagem
            'attachments' => 'nullable|array|max:5', // Máximo 5 ficheiros
            'attachments.*' => [
                'file',                              // Tem que ser ficheiro
                'image',                             // Tem que ser imagem
                'mimes:jpg,png,gif,webp',           // Formatos aceites
                'max:2048',                          // Máximo 2MB por ficheiro
            ],

            // Email: opcional, mas se enviado tem que ser válido e único
            'email' => [
                'nullable',                          // Pode estar vazio
                'email',                             // Formato de email válido
                'unique:users,email,' . $this->user()->id, // Único, exceto o próprio user
            ],

            // Password: apenas quando está a criar (POST)
            // Confirmação: password e password_confirmation têm que ser iguais
            'password' => [
                'required_if:' . ($this->isMethod('POST')), // Obrigatório apenas em POST
                'confirmed',                         // Verifica password_confirmation
                'min:8',                             // Mínimo 8 caracteres
                'regex:/[a-z]/',                     // Pelo menos 1 letra minúscula
                'regex:/[A-Z]/',                     // Pelo menos 1 letra maiúscula
                'regex:/[0-9]/',                     // Pelo menos 1 número
                'regex:/[@$!%*#?&]/',               // Pelo menos 1 caractere especial
            ],

            // Datas
            'start_date' => 'required|date|after:today', // Depois de hoje
            'end_date' => 'required|date|after:start_date', // Depois de start_date

            // Arrays com validação de elementos
            'tags' => 'array|min:1|max:10',          // Entre 1 e 10 tags
            'tags.*' => 'string|max:50',             // Cada tag: string, max 50 chars
        ];
    }

    /**
     * Get custom messages for validator errors.
     *
     * Define MENSAGENS PERSONALIZADAS para cada erro de validação.
     * Por padrão Laravel usa mensagens em inglês.
     * Aqui podemos traduzir para português e personalizar.
     */
    public function messages(): array
    {
        return [
            // Formato: 'campo.regra' => 'Mensagem personalizada'

            'title.required' => 'O título do ticket é obrigatório.',
            'title.min' => 'O título deve ter pelo menos :min caracteres.',
            'title.max' => 'O título não pode ter mais de :max caracteres.',

            'description.required' => 'A descrição é obrigatória.',
            'description.min' => 'Descreve o problema com mais detalhe (mínimo :min caracteres).',

            'priority.required' => 'Seleciona uma prioridade.',
            'priority.in' => 'Prioridade inválida. Escolhe: low, medium, high ou urgent.',

            'category_id.exists' => 'A categoria selecionada não existe.',

            'attachments.max' => 'Máximo de :max ficheiros permitidos.',
            'attachments.*.image' => 'Todos os ficheiros devem ser imagens.',
            'attachments.*.max' => 'Cada imagem deve ter no máximo :max KB.',

            'email.unique' => 'Este email já está a ser usado por outro utilizador.',

            'password.confirmed' => 'As passwords não coincidem.',
            'password.min' => 'A password deve ter pelo menos :min caracteres.',
            'password.regex' => 'A password deve conter maiúsculas, minúsculas, números e caracteres especiais.',
        ];
    }

    /**
     * Get custom attributes for validator errors.
     *
     * Define NOMES personalizados para os campos.
     * Usado nas mensagens de erro padrão.
     */
    public function attributes(): array
    {
        return [
            'title' => 'título',
            'description' => 'descrição',
            'priority' => 'prioridade',
            'category_id' => 'categoria',
            'attachments.*' => 'anexo',
        ];
    }

    /**
     * Prepare the data for validation.
     *
     * Modifica os dados ANTES de validar.
     * Útil para normalizar inputs (trim, lowercase, etc).
     */
    protected function prepareForValidation(): void
    {
        $this->merge([
            // Remove espaços em branco do título
            'title' => trim($this->title),

            // Converte email para lowercase
            'email' => strtolower($this->email),

            // Remove caracteres especiais do telefone
            'phone' => preg_replace('/[^0-9]/', '', $this->phone),
        ]);
    }
}
```

**Uso no Controller:**

```php
// app/Http/Controllers/TicketController.php
use App\Http\Requests\StoreTicketRequest;

class TicketController extends Controller
{
    public function store(StoreTicketRequest $request)
    {
        // Se chegou aqui, Laravel JÁ VALIDOU tudo!
        // $request->validated() retorna apenas campos validados (mais seguro)

        $ticket = Ticket::create($request->validated());

        return redirect()
            ->route('tickets.show', $ticket)
            ->with('success', 'Ticket criado com sucesso!');
    }
}
```

**O que acontece por trás?**

```
1. Request chega → POST /tickets
   ↓
2. Laravel injeta StoreTicketRequest no Controller
   ↓
3. Executa authorize() → Verifica permissões
   ↓ Se FALSE → HTTP 403 Forbidden
   ↓ Se TRUE → Continua
   ↓
4. Executa prepareForValidation() → Normaliza dados
   ↓
5. Executa rules() → Valida cada campo
   ↓ Se FALHA → HTTP 422 + JSON com erros
   ↓ Se PASSA → Continua
   ↓
6. Controller recebe Request validado
   ↓
7. $request->validated() retorna dados limpos
```

**Validação no Frontend (Inertia + Vue):**

```vue
<!-- resources/js/Pages/Tickets/Create.vue -->
<template>
    <form @submit.prevent="submit">
        <!-- Campo Título -->
        <div>
            <label for="title">Título</label>
            <input
                id="title"
                v-model="form.title"
                type="text"
                :class="{ 'border-red-500': form.errors.title }"
            />
            <!-- Mostrar erro de validação (vem do Laravel) -->
            <p v-if="form.errors.title" class="text-red-500 text-sm">
                {{ form.errors.title }}
            </p>
        </div>

        <button type="submit" :disabled="form.processing">Criar Ticket</button>
    </form>
</template>

<script setup>
import { useForm } from "@inertiajs/vue3";

const form = useForm({
    title: "",
    description: "",
    priority: "medium",
    category_id: null,
});

function submit() {
    form.post("/tickets", {
        onSuccess: () => {
            // Sucesso! Ticket criado
            form.reset();
        },
        onError: (errors) => {
            // Erros de validação do Laravel
            // form.errors.title, form.errors.description, etc.
            console.log(errors);
        },
    });
}
</script>
```

**Regras de Validação Mais Usadas:**

```php
// Obrigatoriedade
'required'              // Campo obrigatório
'required_if:outro_campo,valor' // Obrigatório se outro campo = valor
'required_with:outro_campo'     // Obrigatório se outro campo presente
'nullable'              // Pode ser NULL/vazio

// Tipos
'string'                // Texto
'integer'               // Número inteiro
'numeric'               // Número (int ou float)
'boolean'               // true/false
'array'                 // Array
'file'                  // Ficheiro
'image'                 // Imagem

// Tamanhos
'min:5'                 // Mínimo (string: chars, number: valor, file: KB)
'max:255'               // Máximo
'between:5,255'         // Entre 5 e 255
'size:10'               // Exatamente 10

// Formatos
'email'                 // Email válido
'url'                   // URL válida
'ip'                    // IP válido
'date'                  // Data válida
'regex:/[a-z]/'         // Regex personalizado

// Base de Dados
'exists:tabela,coluna'  // Verifica se existe
'unique:tabela,coluna'  // Verifica se é único

// Ficheiros
'mimes:jpg,png'         // Formatos permitidos
'dimensions:min_width=100,min_height=100' // Dimensões mínimas

// Comparações
'same:outro_campo'      // Igual a outro campo
'different:outro_campo' // Diferente de outro campo
'confirmed'             // Verifica campo_confirmation
'in:foo,bar,baz'        // Valor tem que ser um destes
'not_in:foo,bar'        // Valor NÃO pode ser um destes

// Datas
'before:tomorrow'       // Antes de amanhã
'after:yesterday'       // Depois de ontem
'after_or_equal:start_date' // Depois ou igual a start_date
```

**Vantagens da Validação Laravel:**

1. **Segurança**: Protege contra dados inválidos/maliciosos
2. **UX**: Mensagens claras para o utilizador
3. **Organização**: Validação separada do Controller
4. **Reuso**: Mesma validação em API e Web
5. **Type-Safety**: Com Spatie Data fica ainda melhor
6. **Internacionalização**: Mensagens em qualquer língua

#### **Queue Jobs** (Tarefas Assíncronas em Background)

**O que são Queue Jobs?**
Queue Jobs são tarefas que **NÃO precisam ser executadas imediatamente** durante o request HTTP. Em vez de bloquear o utilizador, a tarefa é adicionada a uma "fila" (queue) e processada em background por um worker.

**Problema que Resolve:**

```php
// SEM QUEUES (Utilizador espera... e espera... e espera...)
public function store(StoreTicketRequest $request)
{
    // 1. Criar ticket na BD (50ms)
    $ticket = Ticket::create($request->validated());

    // 2. Enviar email ao utilizador (2 segundos!)
    Mail::to($ticket->user)->send(new TicketCreatedMail($ticket));

    // 3. Enviar notificação ao agente (1 segundo)
    Mail::to($ticket->assigned_agent)->send(new TicketAssignedMail($ticket));

    // 4. Gerar PDF do ticket (3 segundos!)
    $pdf = PDF::loadView('tickets.pdf', compact('ticket'))->save();

    // 5. Upload para S3 (2 segundos)
    Storage::disk('s3')->put("tickets/{$ticket->id}.pdf", $pdf);

    // TOTAL: 8+ segundos de espera! Utilizador pensa que app crashou
    return redirect()->route('tickets.show', $ticket);
}

// COM QUEUES (Resposta INSTANTÂNEA!)
public function store(StoreTicketRequest $request)
{
    // 1. Criar ticket na BD (50ms)
    $ticket = Ticket::create($request->validated());

    // 2. Adicionar jobs à queue (1ms cada!)
    SendTicketCreatedEmail::dispatch($ticket);          // Envia email em background
    SendTicketAssignedEmail::dispatch($ticket);         // Envia notificação em background
    GenerateTicketPDF::dispatch($ticket);               // Gera PDF em background

    // TOTAL: 50ms! Utilizador recebe resposta IMEDIATAMENTE
    // Workers processam os emails/PDF em background enquanto utilizador já está a ver o ticket
    return redirect()->route('tickets.show', $ticket);
}
```

**Anatomia de um Job:**

```php
// app/Jobs/SendTicketCreatedEmail.php
<?php

namespace App\Jobs;

use App\Mail\TicketCreatedMail;
use App\Models\Ticket;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Mail;

/**
 * Job para enviar email quando ticket é criado.
 *
 * ShouldQueue = Interface que indica ao Laravel: "Execute este job em background"
 */
class SendTicketCreatedEmail implements ShouldQueue
{
    use Dispatchable,          // Permite fazer: Job::dispatch()
        InteractsWithQueue,    // Permite interagir com a queue (retry, delete, etc)
        Queueable,             // Permite definir queue, delay, etc
        SerializesModels;      // Serializa Models automaticamente (guarda ID, não objeto inteiro)

    /**
     * Número de tentativas se o job falhar.
     *
     * Se falhar 3 vezes → Job vai para "failed_jobs" table
     */
    public int $tries = 3;

    /**
     * Tempo máximo de execução (segundos).
     *
     * Se demorar mais de 60s → Laravel mata o job
     */
    public int $timeout = 60;

    /**
     * Tempo de espera entre tentativas (segundos).
     *
     * backoff = [60, 120, 300] significa:
     * - 1ª tentativa falha → espera 60s
     * - 2ª tentativa falha → espera 120s
     * - 3ª tentativa falha → espera 300s
     * - Depois disso → failed_jobs
     */
    public array $backoff = [60, 120, 300];

    /**
     * Create a new job instance.
     *
     * Laravel serializa o $ticket automaticamente:
     * - Guarda apenas o ID do ticket
     * - Quando o worker executar, busca o ticket pela ID
     *
     * Isto poupa memória! Em vez de guardar objeto inteiro na queue,
     * guarda apenas: {"ticket_id": 123}
     */
    public function __construct(
        public Ticket $ticket // SerializesModels transforma isto em ID automaticamente
    ) {}

    /**
     * Execute the job.
     *
     * Este método é executado pelo WORKER em background.
     * NÃO é executado durante o request HTTP!
     *
     * Fluxo:
     * 1. Controller faz: SendTicketCreatedEmail::dispatch($ticket)
     * 2. Laravel adiciona job à queue (Redis)
     * 3. Worker em background pega o job
     * 4. Worker executa handle()
     * 5. Se handle() completar sem exceções → Job apagado da queue
     * 6. Se handle() lançar exceção → Job reentra na queue para retry
     */
    public function handle(): void
    {
        // Enviar email
        // Se isto falhar (SMTP down, etc), Laravel automaticamente:
        // 1. Marca job como falhado
        // 2. Reenvia para queue depois de backoff[0] segundos
        // 3. Tenta novamente (até $tries vezes)
        Mail::to($this->ticket->user)
            ->send(new TicketCreatedMail($this->ticket));

        // Opcional: Log de sucesso
        \Log::info("Email enviado para ticket #{$this->ticket->ticket_number}");
    }

    /**
     * Handle a job failure.
     *
     * Executado quando job falha DEFINITIVAMENTE (depois de $tries tentativas).
     * Útil para:
     * - Logging
     * - Notificar admins
     * - Criar ticket manual
     */
    public function failed(\Throwable $exception): void
    {
        // Log o erro
        \Log::error("Falha ao enviar email do ticket #{$this->ticket->ticket_number}: " . $exception->getMessage());

        // Notificar admin via Slack
        \Notification::route('slack', config('services.slack.webhook'))
            ->notify(new JobFailedNotification($this->ticket, $exception));
    }
}
```

**Dispatch (Adicionar Job à Queue):**

```php
// 1. Dispatch simples (executa AGORA em background)
SendTicketCreatedEmail::dispatch($ticket);

// 2. Dispatch com delay (executa DEPOIS de 5 minutos)
SendTicketCreatedEmail::dispatch($ticket)
    ->delay(now()->addMinutes(5));

// 3. Dispatch em queue específica
SendTicketCreatedEmail::dispatch($ticket)
    ->onQueue('emails'); // Queue "emails" (pode ter worker dedicado)

// 4. Dispatch condicional
SendTicketCreatedEmail::dispatchIf($ticket->user->wants_emails, $ticket);
SendTicketCreatedEmail::dispatchUnless($ticket->is_spam, $ticket);

// 5. Dispatch em chain (sequencial)
SendTicketCreatedEmail::withChain([
    new SendTicketAssignedEmail($ticket),
    new GenerateTicketPDF($ticket),
])->dispatch($ticket);
// Executa em ordem: Created → Assigned → PDF
// Se algum falhar, resto não executa

// 6. Dispatch em batch (paralelo com rastreamento)
Bus::batch([
    new SendTicketCreatedEmail($ticket),
    new SendTicketAssignedEmail($ticket),
    new GenerateTicketPDF($ticket),
])->then(function (Batch $batch) {
    // Executado quando TODOS os jobs completarem
    \Log::info("Batch completo!");
})->catch(function (Batch $batch, \Throwable $e) {
    // Executado se algum job falhar
    \Log::error("Batch falhou: " . $e->getMessage());
})->finally(function (Batch $batch) {
    // Executado sempre (sucesso ou falha)
})->dispatch();
```

**Configuração de Queues:**

```php
// config/queue.php
return [
    // Driver padrão (redis = recomendado para produção)
    'default' => env('QUEUE_CONNECTION', 'redis'),

    'connections' => [
        // Sync: Executa imediatamente (sem queue) - útil para testes
        'sync' => [
            'driver' => 'sync',
        ],

        // Redis: Produção (rápido, confiável)
        'redis' => [
            'driver' => 'redis',
            'connection' => 'default',
            'queue' => env('REDIS_QUEUE', 'default'),
            'retry_after' => 90, // Retry job após 90s se worker crashar
            'block_for' => null,
        ],

        // Database: Alternativa ao Redis (mais lento)
        'database' => [
            'driver' => 'database',
            'table' => 'jobs',
            'queue' => 'default',
            'retry_after' => 90,
        ],
    ],

    // Failed jobs (jobs que falharam definitivamente)
    'failed' => [
        'driver' => 'database-uuids',
        'database' => env('DB_CONNECTION', 'pgsql'),
        'table' => 'failed_jobs',
    ],
];
```

**Workers (Processar Queue):**

```bash
# Worker simples (processa queue "default")
php artisan queue:work

# Worker para queue específica
php artisan queue:work redis --queue=emails

# Worker com timeout e memory limit
php artisan queue:work redis \
    --timeout=60 \          # Mata job após 60s
    --memory=256 \          # Restart worker se usar 256MB RAM
    --sleep=3 \             # Espera 3s entre jobs (reduz CPU)
    --tries=3 \             # Tenta 3 vezes antes de falhar
    --max-jobs=1000 \       # Processa 1000 jobs e restart (evita memory leaks)
    --max-time=3600         # Restart após 1 hora

# Worker para múltiplas queues (prioridade)
php artisan queue:work redis --queue=high,default,low
# Processa "high" primeiro, depois "default", depois "low"

# Ver jobs na queue
php artisan queue:monitor redis:default,redis:emails
# Alerta se queue tem > 100 jobs

# Ver failed jobs
php artisan queue:failed

# Retry failed job
php artisan queue:retry 1 # Retry job ID 1
php artisan queue:retry all # Retry TODOS

# Limpar failed jobs
php artisan queue:flush # Apaga TODOS os failed jobs
```

**Supervisor (Production - Workers Always Running):**

```ini
# /etc/supervisor/conf.d/orionone-worker.conf
[program:orionone-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/orionone/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=www-data
numprocs=4                     # 4 workers em paralelo
redirect_stderr=true
stdout_logfile=/var/www/orionone/storage/logs/worker.log
stopwaitsecs=3600              # Espera 1h antes de matar worker
```

```bash
# Iniciar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start orionone-worker:*

# Ver status
sudo supervisorctl status orionone-worker:*
```

**Job Events (Monitoring):**

```php
// app/Providers/EventServiceProvider.php
use Illuminate\Queue\Events\JobFailed;
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobProcessing;

Queue::before(function (JobProcessing $event) {
    // Antes de processar job
    \Log::info("Processing job: {$event->job->getName()}");
});

Queue::after(function (JobProcessed $event) {
    // Depois de processar job (sucesso)
    \Log::info("Job completed: {$event->job->getName()}");
});

Queue::failing(function (JobFailed $event) {
    // Quando job falha
    \Log::error("Job failed: {$event->job->getName()}");

    // Notificar Slack
    \Notification::route('slack', config('services.slack.webhook'))
        ->notify(new JobFailedNotification($event));
});
```

**Quando Usar Queues?**

**USE para:**

-   Enviar emails/notificações
-   Gerar relatórios PDF/Excel
-   Processar uploads (resize imagens, etc)
-   Imports/Exports grandes
-   API calls externas (Stripe, AWS, etc)
-   Limpeza de dados antigos
-   Backups

**NÃO USE para:**

-   Buscar dados da BD (use cache)
-   Operações críticas que devem ser imediatas
-   Dados que utilizador precisa VER agora

**Vantagens das Queues:**

1. **Performance**: Resposta HTTP rápida (não bloqueia utilizador)
2. **Resiliência**: Retry automático se falhar
3. **Escalabilidade**: Múltiplos workers em paralelo
4. **Priorização**: Queues diferentes para tarefas urgentes
5. **Monitoring**: Laravel Horizon (dashboard bonito)
6. **Throttling**: Rate limiting (não sobrecarregar APIs externas)

---

## 🔐 2. ILLUMINATE (Componentes Core do Laravel)

### O que é?

**Illuminate** é o nome dos pacotes internos do Laravel. Cada componente é independente e pode ser usado fora do Laravel.

### Componentes Principais que Usamos

#### **Illuminate\Http** (Requests & Responses)

```php
// Request: Aceder a dados do HTTP
$request->input('name');        // POST/GET/PUT
$request->file('avatar');       // Upload de ficheiro
$request->user();               // Utilizador autenticado
$request->ip();                 // IP do cliente
$request->header('User-Agent'); // Headers HTTP

// Response: Respostas HTTP
return response()->json(['status' => 'success']);
return response()->download($path);
return redirect()->route('tickets.index');
```

#### **Illuminate\Support** (Helpers & Collections)

```php
// Collections: Arrays com superpoderes
$tickets = Ticket::all(); // Retorna Collection

$tickets->filter(fn($t) => $t->priority === 'high')
        ->map(fn($t) => $t->title)
        ->take(5);

// Helpers úteis
Str::slug('Olá Mundo!'); // ola-mundo
Arr::get($array, 'key.nested', 'default');
now()->addDays(7)->format('Y-m-d');
```

#### **Illuminate\Database** (Query Builder)

```php
// Query Builder: SQL programático
DB::table('tickets')
    ->join('users', 'tickets.user_id', '=', 'users.id')
    ->where('status', 'open')
    ->whereDate('created_at', '>', now()->subDays(7))
    ->orderBy('priority', 'desc')
    ->select('tickets.*', 'users.name')
    ->paginate(20);
```

#### **Illuminate\Auth** (Autenticação)

```php
// Login
Auth::attempt(['email' => $email, 'password' => $password]);

// Verificar autenticação
if (Auth::check()) { /* utilizador está logado */ }

// Obter utilizador
$user = Auth::user();
$userId = Auth::id();

// Logout
Auth::logout();
```

#### **Illuminate\Cache** (Caching com Redis)

```php
// Guardar em cache (expira em 1 hora)
Cache::put('user_' . $id, $user, now()->addHour());

// Obter de cache
$user = Cache::get('user_' . $id);

// Cache com fallback (se não existir, executa query)
$stats = Cache::remember('dashboard_stats', 3600, function() {
    return Ticket::selectRaw('status, COUNT(*) as count')
                 ->groupBy('status')
                 ->get();
});
```

---

## 3. SPATIE PACKAGES (Produtividade Profissional)

### Porque Spatie?

**Spatie** é uma empresa belga que cria os MELHORES packages Laravel do mercado. São usados por empresas como NASA, Disney, e milhares de startups.

---

### 3.1 **spatie/laravel-permission** (Roles & Permissions)

#### O que faz?

Sistema RBAC (Role-Based Access Control) profissional. Controla QUEM pode fazer O QUÊ.

#### Como funciona?

```php
// Criar roles
Role::create(['name' => 'admin']);
Role::create(['name' => 'agent']);
Role::create(['name' => 'user']);

// Criar permissões
Permission::create(['name' => 'tickets.create']);
Permission::create(['name' => 'tickets.delete']);
Permission::create(['name' => 'users.manage']);

// Atribuir permissões a roles
$admin = Role::findByName('admin');
$admin->givePermissionTo('tickets.delete', 'users.manage');

$agent = Role::findByName('agent');
$agent->givePermissionTo('tickets.create', 'comments.create');

// Atribuir role a utilizador
$user->assignRole('agent');

// Verificar permissões
if ($user->hasPermissionTo('tickets.delete')) {
    // Pode apagar tickets
}

// Middleware em rotas
Route::middleware(['permission:tickets.delete'])->group(function() {
    Route::delete('/tickets/{ticket}', [TicketController::class, 'destroy']);
});
```

#### Porque usamos?

-   **Escalável**: 100+ permissões sem problemas
-   **Cache integrado**: Performance excelente
-   **Middleware pronto**: Proteção de rotas automática
-   **Blade directives**: `@can('tickets.delete')` nos templates

**Tabelas criadas:**

-   `roles` - Papéis (admin, agent, user)
-   `permissions` - Permissões granulares
-   `role_has_permissions` - Relacionamento
-   `model_has_roles` - Utilizadores têm roles
-   `model_has_permissions` - Permissões diretas (override)

---

### 3.2 **spatie/laravel-data** (DTOs + Validation)

#### O que faz?

**Data Transfer Objects** type-safe. Substitui arrays associativos por objetos tipados.

#### Exemplo SEM Laravel Data (problema)

```php
// Controller retorna array (não sabemos a estrutura!)
public function store(Request $request)
{
    $data = $request->all(); // Array genérico 😱

    // Que campos tem? Que tipos? Não sabemos!
    $ticket = Ticket::create($data);
}
```

#### Exemplo COM Laravel Data (solução)

```php
// app/Data/TicketData.php
use Spatie\LaravelData\Data;

class TicketData extends Data
{
    public function __construct(
        public string $title,
        public string $description,
        public Priority $priority,      // Enum type-safe
        public int $category_id,
        public ?int $assigned_to = null,
    ) {}

    // Validação automática
    public static function rules(): array
    {
        return [
            'title' => 'required|string|min:5|max:255',
            'description' => 'required|string|min:20',
            'priority' => ['required', 'enum:' . Priority::class],
            'category_id' => 'required|exists:categories,id',
        ];
    }
}

// Uso no Controller
public function store(TicketData $data)
{
    // $data é 100% type-safe!
    // IDE autocomplete funciona perfeitamente
    $ticket = Ticket::create([
        'title' => $data->title,           // String garantido
        'priority' => $data->priority->value, // Enum
    ]);
}
```

#### Vantagens:

- **Type safety**: IDE sabe os tipos
- **Validação integrada**: Rules no próprio DTO
- **Documentação viva**: A classe É a documentação
- **Refactoring seguro**: Rename funciona
- **Testes mais fáceis**: `TicketData::from(['title' => 'Test'])`

---

### 3.3 **spatie/laravel-activitylog** (Audit Trail)

#### O que faz?

Regista TODAS as ações importantes: quem criou, editou, apagou, quando, que mudanças.

#### Como funciona?

```php
// app/Models/Ticket.php
use Spatie\Activitylog\Traits\LogsActivity;

class Ticket extends Model
{
    use LogsActivity;

    protected static $logAttributes = ['*']; // Loga todos os campos
    protected static $logOnlyDirty = true;   // Só mudanças reais

    // Descrição do log
    public function getDescriptionForEvent(string $eventName): string
    {
        return "Ticket {$eventName}";
    }
}

// Uso automático (Laravel faz tudo!)
$ticket = Ticket::create(['title' => 'Bug crítico']);
// Activity log criado: "Ticket created by User #5"

$ticket->update(['status' => 'in_progress']);
// Activity log: "Ticket updated: status changed from 'open' to 'in_progress'"

// Logs manuais (ações customizadas)
activity()
    ->performedOn($ticket)
    ->causedBy($user)
    ->withProperties(['ip' => request()->ip()])
    ->log('Ticket foi escalado para a equipa de segurança');

// Obter histórico
$ticket->activities; // Collection de Activity models

// Ver mudanças
foreach ($ticket->activities as $activity) {
    echo $activity->description;
    echo $activity->created_at;
    echo $activity->causer->name; // Quem fez

    // Mudanças (antes → depois)
    $changes = $activity->properties;
    $changes['attributes']; // Valores novos
    $changes['old'];        // Valores antigos
}
```

#### Porque é essencial?

-   **Compliance**: GDPR, ISO 27001 exigem audit logs
-   **Debug**: "Quem mudou este ticket para closed?"
-   **Histórico**: Timeline completa de mudanças
-   **Rollback**: Reverter mudanças indesejadas

**Tabela criada:**

-   `activity_log` - Todos os eventos (JSON)

---

### 3.4 **spatie/laravel-query-builder** (Filtros URL)

#### O que faz?

Filtros, ordenação e pesquisa através da URL. Transforma URLs em queries Eloquent.

#### Exemplo Prático

```php
// GET /tickets?filter[status]=open&filter[priority]=high&sort=-created_at&include=user,comments

// app/Http/Controllers/TicketController.php
use Spatie\QueryBuilder\QueryBuilder;

public function index()
{
    $tickets = QueryBuilder::for(Ticket::class)
        ->allowedFilters(['status', 'priority', 'assigned_to'])
        ->allowedSorts('created_at', 'priority', 'title')
        ->allowedIncludes('user', 'comments', 'team')
        ->defaultSort('-created_at')
        ->paginate(20);

    return Inertia::render('Tickets/Index', [
        'tickets' => $tickets
    ]);
}
```

#### URLs que Funcionam:

```
# Filtrar por status
/tickets?filter[status]=open

# Múltiplos filtros
/tickets?filter[status]=open&filter[priority]=high

# Ordenar
/tickets?sort=priority           # ASC
/tickets?sort=-created_at        # DESC

# Eager load relacionamentos
/tickets?include=user,comments

# Combinar tudo
/tickets?filter[status]=open&sort=-priority&include=user&page=2
```

#### Vantagens:

✅ **Frontend-friendly**: Vue.js constrói URLs facilmente
✅ **Performance**: Só carrega o necessário
✅ **Consistência**: Mesma sintaxe em todas as APIs
✅ **Documentação automática**: Scribe documenta filtros

---

## 🛠️ 4. LORISLEIVA LARAVEL ACTIONS

### O que faz?

**Actions Pattern**: Uma classe = Uma ação. Pode ser usada como Controller, Job, Command, Listener.

### Problema que Resolve

#### Sem Actions (código duplicado)

```php
// Controller
class TicketController {
    public function store(Request $request) {
        $ticket = Ticket::create($request->validated());
        Mail::to($ticket->user)->send(new TicketCreated($ticket));
        return redirect()->route('tickets.show', $ticket);
    }
}

// API Controller (DUPLICADO!)
class ApiTicketController {
    public function store(Request $request) {
        $ticket = Ticket::create($request->validated());
        Mail::to($ticket->user)->send(new TicketCreated($ticket));
        return response()->json($ticket);
    }
}

// Queue Job (DUPLICADO!)
class ProcessBulkTicketsJob {
    public function handle() {
        foreach ($this->tickets as $data) {
            $ticket = Ticket::create($data);
            Mail::to($ticket->user)->send(new TicketCreated($ticket));
        }
    }
}
```

#### Com Actions (DRY - Don't Repeat Yourself)

```php
// app/Actions/Tickets/CreateTicketAction.php
use Lorisleiva\Actions\Concerns\AsAction;

class CreateTicketAction
{
    use AsAction;

    // Lógica de negócio (uma vez!)
    public function handle(TicketData $data): Ticket
    {
        $ticket = Ticket::create($data->toArray());

        Mail::to($ticket->user)->send(new TicketCreated($ticket));

        activity()
            ->performedOn($ticket)
            ->log('Ticket created');

        return $ticket;
    }

    // Como Controller
    public function asController(Request $request)
    {
        $data = TicketData::from($request);
        $ticket = $this->handle($data);

        return redirect()->route('tickets.show', $ticket)
            ->with('success', 'Ticket criado com sucesso!');
    }

    // Como Job (queue)
    public function asJob(TicketData $data): void
    {
        $this->handle($data);
    }

    // Como Command (CLI)
    public function asCommand(Command $command): void
    {
        $data = TicketData::from([
            'title' => $command->ask('Title?'),
            'description' => $command->ask('Description?'),
        ]);

        $ticket = $this->handle($data);
        $command->info("Ticket #{$ticket->id} created!");
    }
}

// Uso em múltiplos contextos
Route::post('/tickets', CreateTicketAction::class);        // Controller
CreateTicketAction::dispatch($data);                        // Job
Artisan::command('ticket:create', CreateTicketAction::class); // CLI
```

### Vantagens:

✅ **DRY**: Lógica escrita uma vez
✅ **Testável**: Testes unitários simples
✅ **Reusável**: Controller, Job, Command, Listener
✅ **Organizado**: Cada ação num ficheiro

---

## 5. LARAVEL SANCTUM (API Authentication)

### O que faz?

Sistema de autenticação para **SPAs** (Single Page Applications) e **APIs**.

### Como Funciona?

#### 1. **Cookie-based (SPA)** - Usado no OrionOne

```php
// Frontend (Vue.js) faz login
axios.post('/login', {
    email: 'user@test.com',
    password: 'secret'
});

// Laravel retorna cookie httpOnly (seguro!)
// Proximos requests incluem cookie automaticamente
axios.get('/api/user'); // ✅ Autenticado automaticamente
```

#### 2. **Token-based (API Externa)**

```php
// Gerar token para app externa
$token = $user->createToken('mobile-app')->plainTextToken;
// "1|laravel_sanctum_abcdef123456..."

// Cliente usa token no header
curl -H "Authorization: Bearer 1|laravel_sanctum..." \
     https://api.orionone.test/tickets
```

### Configuração no OrionOne

```php
// config/sanctum.php
'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', 'localhost,orionone.test')),

// Proteger rotas
Route::middleware('auth:sanctum')->group(function() {
    Route::get('/api/user', fn() => request()->user());
    Route::apiResource('/api/tickets', ApiTicketController::class);
});
```

---

## 📝 6. LARAVEL TELESCOPE (Debug & Monitoring)

### O que faz?

Dashboard de **debugging profissional**. Vê TUDO o que acontece na aplicação.

### Features:

-   **Requests**: Todas as HTTP requests (URL, payload, response)
-   **Queries**: Todas as SQL queries (com timing!)
-   **Jobs**: Queue jobs (pendentes, executados, falhados)
-   **Mails**: Emails enviados (preview HTML)
-   **Notifications**: Notificações enviadas
-   **Cache**: Hits/misses do cache
-   **Exceptions**: Erros capturados
-   **Logs**: Todos os logs (`Log::info()`)

### Acesso:

```
http://orionone.test:8888/telescope
```

### Uso Real:

```php
// Desenvolves uma feature...
$ticket = Ticket::create($data);

// Vai ao Telescope:
// → Queries: Ver SQL executado
// → Logs: Ver `Log::info()` que escreveste
// → Mails: Preview do email enviado
```

**⚠️ IMPORTANTE:** Desativar em produção!

```php
// .env
TELESCOPE_ENABLED=false
```

---

## 7. BARRYVDH IDE HELPER (Autocomplete)

### O que faz?

Gera ficheiros que dão **autocomplete** no PHPStorm/VSCode.

### Problema:

```php
$user = User::find(1);
$user->name; // ❌ IDE não sabe que 'name' existe (User é dinâmico)
```

### Solução:

```bash
php artisan ide-helper:models --write
```

**Resultado:** Ficheiro `_ide_helper_models.php` criado:

```php
/**
 * App\Models\User
 *
 * @property int $id
 * @property string $name
 * @property string $email
 * @method static \Illuminate\Database\Eloquent\Builder|User find($id)
 * @method static \Illuminate\Database\Eloquent\Builder|User where($column, $value)
 */
class User extends Model { }
```

Agora IDE tem **autocomplete perfeito**! 🎉

---

## 🧪 8. PESTPHP (Testing Framework)

### O que faz?

Framework de testes **moderno e elegante**. Alternativa ao PHPUnit (mais bonito!).

### Sintaxe:

```php
// ❌ PHPUnit (antigo)
class TicketTest extends TestCase
{
    public function test_user_can_create_ticket(): void
    {
        $this->actingAs($user)
             ->post('/tickets', $data)
             ->assertRedirect('/tickets');
    }
}

// ✅ Pest (moderno)
test('user can create ticket', function() {
    actingAs($user)
        ->post('/tickets', $data)
        ->assertRedirect('/tickets');
});

// ✅ Ainda melhor (it() syntax)
it('allows authenticated users to create tickets', function() {
    $user = User::factory()->create();
    $data = ['title' => 'Bug', 'description' => 'Critical bug'];

    actingAs($user)
        ->post('/tickets', $data)
        ->assertRedirect()
        ->assertSessionHas('success');

    expect(Ticket::count())->toBe(1);
    expect(Ticket::first()->title)->toBe('Bug');
});
```

### Vantagens:

✅ **Legível**: Parece inglês normal
✅ **Rápido**: Executa em paralelo
✅ **Expect API**: Assertions modernas
✅ **Snapshot testing**: `expect($html)->toMatchSnapshot()`

### Executar Testes:

```bash
php artisan test                    # Todos
php artisan test --filter=Ticket    # Específico
php artisan test --parallel         # Paralelo (4x mais rápido!)
```

---

## 9. INTERVENTION IMAGE (Processamento de Imagens)

### O que faz?

Redimensionar, cortar, converter imagens. Usado para **avatares** e **anexos**.

### Exemplo no OrionOne:

```php
use Intervention\Image\ImageManager;
use Intervention\Image\Drivers\Gd\Driver;

public function handle(User $user, array $data): User
{
    if (isset($data['avatar'])) {
        // Apagar avatar antigo
        if ($user->avatar) {
            Storage::disk('public')->delete($user->avatar);
        }

        // Processar nova imagem
        $manager = new ImageManager(new Driver());
        $image = $manager->read($data['avatar']);

        // Redimensionar para 200x200 (quadrado)
        $image->cover(200, 200);

        // Guardar
        $path = 'avatars/' . $user->id . '_' . time() . '.jpg';
        Storage::disk('public')->put($path, (string) $image->toJpeg());

        $data['avatar'] = $path;
    }

    $user->update($data);
    return $user->fresh();
}
```

### Operações Comuns:

```php
$image->resize(800, 600);         // Redimensionar
$image->cover(200, 200);          // Crop para quadrado
$image->fit(300, 300);            // Fit dentro de caixa
$image->rotate(90);               // Rodar
$image->grayscale();              // Preto e branco
$image->blur(15);                 // Blur
$image->toJpeg(quality: 85);     // Converter para JPG
$image->toPng();                  // Converter para PNG
```

---

## 📧 10. LARAVEL NOTIFICATIONS (Multi-Channel)

### O que faz?

Enviar notificações via **Email, SMS, Slack, Database**.

### Exemplo:

```php
// app/Notifications/TicketAssignedNotification.php
class TicketAssignedNotification extends Notification
{
    public function __construct(public Ticket $ticket) {}

    // Canais de envio
    public function via($notifiable): array
    {
        return ['mail', 'database'];
    }

    // Email
    public function toMail($notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject('Ticket Atribuído: ' . $this->ticket->title)
            ->line('Foi-te atribuído um novo ticket.')
            ->action('Ver Ticket', route('tickets.show', $this->ticket))
            ->line('Prioridade: ' . $this->ticket->priority);
    }

    // Database (notificações in-app)
    public function toDatabase($notifiable): array
    {
        return [
            'ticket_id' => $this->ticket->id,
            'ticket_title' => $this->ticket->title,
            'message' => 'Novo ticket atribuído',
        ];
    }
}

// Enviar notificação
$agent->notify(new TicketAssignedNotification($ticket));

// Obter notificações in-app
$notifications = $user->notifications;
$user->unreadNotifications;
```

---

## RESUMO: Quando Usar Cada Biblioteca?

| Biblioteca                | Usa Quando...                                |
| ------------------------- | -------------------------------------------- |
| **Laravel Eloquent**      | Qualquer interação com BD                    |
| **Spatie Permission**     | Controlar acessos (roles/permissions)        |
| **Spatie Data**           | Passar dados entre camadas (type-safe)       |
| **Spatie Activity Log**   | Registar ações dos utilizadores              |
| **Spatie Query Builder**  | APIs com filtros/ordenação                   |
| **Laravel Actions**       | Lógica reutilizável (Controller+Job+Command) |
| **Laravel Sanctum**       | Autenticação SPA ou API tokens               |
| **Laravel Telescope**     | Debug em desenvolvimento                     |
| **Intervention Image**    | Upload e processamento de imagens            |
| **Pest PHP**              | Escrever testes (TDD)                        |
| **Laravel Notifications** | Enviar emails/notificações                   |

---

## Próximos Passos

Agora que sabes o que cada biblioteca faz, vê:

-   **[TECH-DEEP-DIVE-FRONTEND.md](./TECH-DEEP-DIVE-FRONTEND.md)** - Vue.js, Inertia, Tailwind
-   **[TECH-DEEP-DIVE-DATABASE.md](./TECH-DEEP-DIVE-DATABASE.md)** - PostgreSQL, Redis
-   **[TECH-DEEP-DIVE-DEVOPS.md](./TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx

---

**Dúvidas?** Abre issue ou lê a documentação oficial:

-   [Laravel Docs](https://laravel.com/docs)
-   [Spatie Docs](https://spatie.be/docs)
-   [Laravel Actions](https://laravelactions.com)
