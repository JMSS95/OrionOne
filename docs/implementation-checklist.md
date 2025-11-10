# Implementation Checklist - OrionOne

**Sprint-by-Sprint Implementation Guide**

> Segue a filosofia **TDD + Feature-Driven Development** do [development-guide.md](./development-guide.md)
> Cada feature passa por: **Planning → Tests First (RED) → Implementation (GREEN) → Frontend**

---

## Sprint 1: Auth & Users (11-17 Nov)

**Nota Importante:** O sistema de autenticação (Laravel Breeze) já foi instalado e configurado durante a **Fase 0: Setup Inicial** (ver [SETUP.md](./SETUP.md)). Esta fase inclui:

-   Autenticação completa (login, register, password reset)
-   Proteção de rotas via middleware `auth`
-   Sistema de sessões
-   Profile page básica

**Sprint 1 foca-se em:** Adicionar Roles & Permissions (via Spatie) e expandir funcionalidades do Profile (avatar upload).

---

### Configuração Inicial

#### 1. Laravel IDE Helper

**Já instalado via Composer.** Gerar helpers para melhor autocomplete:

```bash
docker-compose exec orionone-app php artisan ide-helper:generate
docker-compose exec orionone-app php artisan ide-helper:models --write
docker-compose exec orionone-app php artisan ide-helper:meta
```

Adicionar ao `.gitignore`:

```
_ide_helper.php
_ide_helper_models.php
.phpstorm.meta.php
```

#### 2. Inertia Progress Bar

**Já instalado via NPM.** Configurar em `resources/js/app.js`:

```js
import { router } from "@inertiajs/vue3";
import NProgress from "@inertiajs/progress";

NProgress.configure({ showSpinner: false });

router.on("start", () => NProgress.start());
router.on("finish", () => NProgress.done());
```

#### 3. Publicar Configs Spatie

```bash
# Permission
docker-compose exec orionone-app php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"

# Activity Log
docker-compose exec orionone-app php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider" --tag="activitylog-migrations"
docker-compose exec orionone-app php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider" --tag="activitylog-config"

docker-compose exec orionone-app php artisan migrate
```

---

### Feature 1: Role & Permission Setup

#### Phase 1: Planning (30 min)

**User Story:**
Como administrador do sistema, preciso de roles e permissões para controlar acessos.

**Critérios de Aceitação:**

-   Sistema deve ter 3 roles: admin, agent, user
-   Admin tem todas as permissões
-   Agent pode gerir tickets e comentários
-   User apenas cria tickets e vê os próprios

**Permissões necessárias:**

-   tickets: create, view, update, delete, assign, close
-   comments: create, delete
-   users: view, manage (admin only)

#### Phase 2: Tests First (RED)

```bash
docker-compose exec orionone-app php artisan make:test RolePermissionTest
```

**Ficheiro:** `tests/Feature/RolePermissionTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;
use Illuminate\Foundation\Testing\RefreshDatabase;

class RolePermissionTest extends TestCase
{
    use RefreshDatabase;

    public function test_system_has_required_roles(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $this->assertDatabaseHas('roles', ['name' => 'admin']);
        $this->assertDatabaseHas('roles', ['name' => 'agent']);
        $this->assertDatabaseHas('roles', ['name' => 'user']);
    }

    public function test_admin_has_all_permissions(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $admin = Role::findByName('admin');

        $this->assertTrue($admin->hasPermissionTo('tickets.create'));
        $this->assertTrue($admin->hasPermissionTo('tickets.delete'));
        $this->assertTrue($admin->hasPermissionTo('users.manage'));
    }

    public function test_agent_can_manage_tickets_only(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $agent = Role::findByName('agent');

        $this->assertTrue($agent->hasPermissionTo('tickets.create'));
        $this->assertTrue($agent->hasPermissionTo('comments.create'));
        $this->assertFalse($agent->hasPermissionTo('users.manage'));
    }

    public function test_user_can_only_create_tickets(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $user = Role::findByName('user');

        $this->assertTrue($user->hasPermissionTo('tickets.create'));
        $this->assertFalse($user->hasPermissionTo('tickets.delete'));
        $this->assertFalse($user->hasPermissionTo('users.view'));
    }
}
```

**Rodar testes:**

```bash
docker-compose exec orionone-app php artisan test --filter=CreateTicketTest
# RED: Tickets table doesn't exist
```

#### Phase 3: Implementation (GREEN)

Agora implementar até os testes passarem:

```bash
docker-compose exec orionone-app php artisan make:seeder RolePermissionSeeder
```

**Ficheiro:** `database/seeders/RolePermissionSeeder.php`

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;

class RolePermissionSeeder extends Seeder
{
    public function run(): void
    {
        // Reset cache
        app()[\Spatie\Permission\PermissionRegistrar::class]->forgetCachedPermissions();

        // Criar permissões
        $permissions = [
            'tickets.create',
            'tickets.view',
            'tickets.update',
            'tickets.delete',
            'tickets.assign',
            'tickets.close',
            'comments.create',
            'comments.delete',
            'users.view',
            'users.manage',
        ];

        foreach ($permissions as $permission) {
            Permission::create(['name' => $permission]);
        }

        // Admin - todas as permissões
        $admin = Role::create(['name' => 'admin']);
        $admin->givePermissionTo(Permission::all());

        // Agent - gestão de tickets
        $agent = Role::create(['name' => 'agent']);
        $agent->givePermissionTo([
            'tickets.create',
            'tickets.view',
            'tickets.update',
            'tickets.assign',
            'tickets.close',
            'comments.create',
            'comments.delete',
        ]);

        // User - apenas criar tickets
        $user = Role::create(['name' => 'user']);
        $user->givePermissionTo([
            'tickets.create',
            'tickets.view',
            'comments.create',
        ]);
    }
}
```

**Adicionar ao DatabaseSeeder:**

```php
public function run(): void
{
    $this->call([
        RolePermissionSeeder::class,
    ]);
}
```

**Rodar testes novamente:**

```bash
docker-compose exec orionone-app php artisan test --filter=RolePermissionTest
# GREEN: Testes passam!
```

#### Phase 4: Seed Users de Teste

Criar utilizadores para desenvolvimento:

```bash
docker-compose exec orionone-app php artisan make:seeder UserSeeder
```

**Ficheiro:** `database/seeders/UserSeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        // Admin
        $admin = User::create([
            'name' => 'Admin User',
            'email' => 'admin@orionone.test',
            'password' => Hash::make('password'),
            'email_verified_at' => now(),
        ]);
        $admin->assignRole('admin');

        // Agent
        $agent = User::create([
            'name' => 'Agent User',
            'email' => 'agent@orionone.test',
            'password' => Hash::make('password'),
            'email_verified_at' => now(),
        ]);
        $agent->assignRole('agent');

        // Regular User
        $user = User::create([
            'name' => 'Regular User',
            'email' => 'user@orionone.test',
            'password' => Hash::make('password'),
            'email_verified_at' => now(),
        ]);
        $user->assignRole('user');
    }
}
```

**Adicionar ao DatabaseSeeder:**

```php
public function run(): void
{
    $this->call([
        RolePermissionSeeder::class,
        UserSeeder::class, // Adicionar esta linha
    ]);
}
```

**Seed da base de dados:**

```bash
docker-compose exec orionone-app php artisan migrate:fresh --seed
```

---

### Feature 2: Profile Avatar Upload

#### Phase 1: Planning (30 min)

**User Story:**
Como utilizador autenticado, quero adicionar uma foto de perfil para personalizar a minha conta.

**Critérios de Aceitação:**

-   Campo avatar na tabela users
-   Upload de imagem com validação (jpeg, png, max 2MB)
-   Redimensionamento automático para 200x200px
-   Apagar avatar antigo ao fazer upload de novo
-   Usar Laravel Actions para lógica reutilizável

#### Phase 2: Tests First (RED)

```bash
docker-compose exec orionone-app php artisan make:test UpdateProfileTest
```

**Ficheiro:** `tests/Feature/UpdateProfileTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Illuminate\Foundation\Testing\RefreshDatabase;

class UpdateProfileTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_update_profile_with_avatar(): void
    {
        Storage::fake('public');
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post(route('profile.update'), [
            'name' => 'Updated Name',
            'avatar' => UploadedFile::fake()->image('avatar.jpg'),
        ]);

        $response->assertRedirect(route('profile.edit'));

        $this->assertEquals('Updated Name', $user->fresh()->name);
        $this->assertNotNull($user->fresh()->avatar);

        Storage::disk('public')->assertExists($user->fresh()->avatar);
    }

    public function test_avatar_must_be_image(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post(route('profile.update'), [
            'name' => 'Test',
            'avatar' => UploadedFile::fake()->create('document.pdf'),
        ]);

        $response->assertSessionHasErrors(['avatar']);
    }

    public function test_old_avatar_is_deleted_on_new_upload(): void
    {
        Storage::fake('public');
        $user = User::factory()->create([
            'avatar' => 'avatars/old-avatar.jpg',
        ]);

        Storage::disk('public')->put('avatars/old-avatar.jpg', 'old content');

        $this->actingAs($user)->post(route('profile.update'), [
            'name' => $user->name,
            'avatar' => UploadedFile::fake()->image('new-avatar.jpg'),
        ]);

        Storage::disk('public')->assertMissing('avatars/old-avatar.jpg');
        Storage::disk('public')->assertExists($user->fresh()->avatar);
    }
}
```

**Rodar testes (vai falhar - esperado!):**

```bash
docker-compose exec orionone-app php artisan test --filter=UpdateProfileTest
# RED: Column 'avatar' not found
```

#### Phase 3: Implementation (GREEN)

**a) Migration:**

```bash
docker-compose exec orionone-app php artisan make:migration add_avatar_to_users_table
```

```php
public function up(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->string('avatar')->nullable()->after('email');
    });
}
```

```bash
docker-compose exec orionone-app php artisan migrate
```

**b) Criar UpdateProfileAction (Laravel Actions):**

```bash
docker-compose exec orionone-app php artisan make:action UpdateProfileAction
```

**Ficheiro:** `app/Actions/Users/UpdateProfileAction.php`

```php
<?php

namespace App\Actions\Users;

use App\Models\User;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Intervention\Image\Laravel\Facades\Image;
use Lorisleiva\Actions\Concerns\AsAction;

class UpdateProfileAction
{
    use AsAction;

    public function handle(User $user, array $data): User
    {
        // Avatar upload
        if (isset($data['avatar']) && $data['avatar'] instanceof UploadedFile) {
            // Apagar avatar antigo
            if ($user->avatar) {
                Storage::disk('public')->delete($user->avatar);
            }

            // Processar nova imagem
            $image = Image::read($data['avatar']);
            $image->cover(200, 200);

            $path = 'avatars/' . $user->id . '_' . time() . '.jpg';
            Storage::disk('public')->put($path, $image->encode());

            $data['avatar'] = $path;
        }

        // Atualizar dados
        $user->update([
            'name' => $data['name'],
            'avatar' => $data['avatar'] ?? $user->avatar,
        ]);

        return $user->fresh();
    }

    public function asController(): \Illuminate\Http\RedirectResponse
    {
        $validated = request()->validate([
            'name' => ['required', 'string', 'max:255'],
            'avatar' => ['nullable', 'image', 'mimes:jpeg,png,jpg', 'max:2048'],
        ]);

        $this->handle(auth()->user(), $validated);

        return redirect()->route('profile.edit')
            ->with('success', 'Perfil atualizado com sucesso!');
    }
}
```

**c) Registar Route:**

```php
// routes/web.php
use App\Actions\Users\UpdateProfileAction;

Route::post('/profile', UpdateProfileAction::class)->name('profile.update');
```

**Rodar testes novamente:**

```bash
docker-compose exec orionone-app php artisan test --filter=UpdateProfileTest
# GREEN: Testes passam!
```

#### Phase 4: Frontend (Vue + Shadcn-vue)

Atualizar `resources/js/Pages/Profile/Edit.vue` (já existe do Breeze):

```vue
<script setup>
import { ref } from "vue";
import { useForm } from "@inertiajs/vue3";
import AuthenticatedLayout from "@/Layouts/AuthenticatedLayout.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";

const props = defineProps({
    user: Object,
});

const avatarPreview = ref(
    props.user.avatar ? `/storage/${props.user.avatar}` : null
);

const form = useForm({
    name: props.user.name,
    avatar: null,
});

const handleAvatarChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        form.avatar = file;
        avatarPreview.value = URL.createObjectURL(file);
    }
};

const submit = () => {
    form.post(route("profile.update"));
};
</script>

<template>
    <AuthenticatedLayout>
        <div class="max-w-2xl mx-auto p-6">
            <h1 class="text-2xl font-bold mb-6">Editar Perfil</h1>

            <form @submit.prevent="submit" class="space-y-6">
                <!-- Avatar -->
                <div>
                    <label class="block text-sm font-medium mb-2">
                        Foto de Perfil
                    </label>

                    <div class="flex items-center space-x-4">
                        <img
                            v-if="avatarPreview"
                            :src="avatarPreview"
                            alt="Avatar"
                            class="w-24 h-24 rounded-full object-cover"
                        />
                        <div
                            v-else
                            class="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center"
                        >
                            <span class="text-gray-500 text-2xl">
                                {{ user.name.charAt(0).toUpperCase() }}
                            </span>
                        </div>

                        <Input
                            type="file"
                            @change="handleAvatarChange"
                            accept="image/jpeg,image/png,image/jpg"
                        />
                    </div>

                    <p
                        v-if="form.errors.avatar"
                        class="mt-2 text-sm text-red-600"
                    >
                        {{ form.errors.avatar }}
                    </p>
                </div>

                <!-- Name -->
                <div>
                    <label class="block text-sm font-medium mb-2">Nome</label>
                    <Input v-model="form.name" required />
                    <p
                        v-if="form.errors.name"
                        class="mt-2 text-sm text-red-600"
                    >
                        {{ form.errors.name }}
                    </p>
                </div>

                <!-- Submit -->
                <Button type="submit" :disabled="form.processing">
                    Guardar Alterações
                </Button>
            </form>
        </div>
    </AuthenticatedLayout>
</template>
```

**Checkpoint:** Rodar todos os testes de Sprint 1:

```bash
docker-compose exec orionone-app php artisan test
# Todos os testes devem passar
```

---

## Sprint 2: Tickets Core (18 Nov - 01 Dez)

### Feature 3: Create Ticket

#### Phase 1: Planning (30 min)

**User Story:**
Como utilizador autenticado, quero criar um ticket para reportar um problema ou solicitar suporte.

**Critérios de Aceitação:**

-   Form com campos: título, descrição, prioridade
-   Validação: título obrigatório (max 255), descrição obrigatória
-   Gerar número único do ticket (TK-20251101-0001)
-   Auto-assignment a equipa baseado em carga de trabalho
-   Status inicial: "open"
-   Activity log do evento

#### Phase 2: Tests First (RED)

```bash
docker-compose exec orionone-app php artisan make:test CreateTicketTest
```

**Ficheiro:** `tests/Feature/CreateTicketTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use App\Models\Ticket;
use Illuminate\Foundation\Testing\RefreshDatabase;

class CreateTicketTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_ticket(): void
    {
        $user = User::factory()->create();
        $user->assignRole('user');

        $response = $this->actingAs($user)->post(route('tickets.store'), [
            'title' => 'Laptop não liga',
            'description' => 'Tentei ligar o laptop mas não funciona.',
            'priority' => 'high',
        ]);

        $response->assertRedirect();

        $this->assertDatabaseHas('tickets', [
            'title' => 'Laptop não liga',
            'requester_id' => $user->id,
            'status' => 'open',
            'priority' => 'high',
        ]);
    }

    public function test_ticket_number_is_auto_generated(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)->post(route('tickets.store'), [
            'title' => 'Test Ticket',
            'description' => 'Test description',
            'priority' => 'medium',
        ]);

        $ticket = Ticket::first();

        $this->assertMatchesRegularExpression(
            '/^TK-\d{8}-\d{4}$/',
            $ticket->ticket_number
        );
    }

    public function test_title_is_required(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post(route('tickets.store'), [
            'description' => 'Test',
            'priority' => 'medium',
        ]);

        $response->assertSessionHasErrors(['title']);
    }

    public function test_activity_is_logged_on_creation(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)->post(route('tickets.store'), [
            'title' => 'Test',
            'description' => 'Test',
            'priority' => 'medium',
        ]);

        $ticket = Ticket::first();

        $this->assertDatabaseHas('activity_log', [
            'subject_type' => Ticket::class,
            'subject_id' => $ticket->id,
            'description' => 'Ticket criado',
        ]);
    }
}
```

**Rodar testes (vai falhar - esperado!):**

```bash
docker-compose exec orionone-app php artisan test --filter=CreateTicketTest
# RED: Table 'tickets' doesn't exist
```

#### Phase 3: Implementation (GREEN)

**a) Migration:**

```bash
docker-compose exec orionone-app php artisan make:migration create_tickets_table
```

```php
public function up(): void
{
    Schema::create('tickets', function (Blueprint $table) {
        $table->id();
        $table->string('ticket_number')->unique();
        $table->string('title');
        $table->text('description');
        $table->enum('status', ['open', 'in_progress', 'resolved', 'closed'])->default('open');
        $table->enum('priority', ['low', 'medium', 'high', 'urgent'])->default('medium');
        $table->foreignId('requester_id')->constrained('users')->onDelete('cascade');
        $table->foreignId('assigned_to')->nullable()->constrained('users')->onDelete('set null');
        $table->foreignId('team_id')->nullable()->constrained('teams')->onDelete('set null');
        $table->timestamp('resolved_at')->nullable();
        $table->timestamp('closed_at')->nullable();
        $table->timestamps();
        $table->softDeletes();

        $table->index(['status', 'priority']);
        $table->index('requester_id');
        $table->index('assigned_to');
    });
}
```

```bash
docker-compose exec orionone-app php artisan migrate
```

**b) Model:**

```bash
docker-compose exec orionone-app php artisan make:model Ticket
```

**Ficheiro:** `app/Models/Ticket.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\SoftDeletes;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class Ticket extends Model
{
    use SoftDeletes, LogsActivity;

    protected $fillable = [
        'ticket_number',
        'title',
        'description',
        'status',
        'priority',
        'requester_id',
        'assigned_to',
        'team_id',
        'resolved_at',
        'closed_at',
    ];

    protected $casts = [
        'resolved_at' => 'datetime',
        'closed_at' => 'datetime',
    ];

    public function requester(): BelongsTo
    {
        return $this->belongsTo(User::class, 'requester_id');
    }

    public function assignee(): BelongsTo
    {
        return $this->belongsTo(User::class, 'assigned_to');
    }

    public function team(): BelongsTo
    {
        return $this->belongsTo(Team::class);
    }

    public function getActivitylogOptions(): LogOptions
    {
        return LogOptions::defaults()
            ->logOnly(['status', 'priority', 'assigned_to'])
            ->logOnlyDirty();
    }
}
```

**c) TicketData (Laravel Data DTO):**

```bash
docker-compose exec orionone-app php artisan make:data TicketData
```

**Ficheiro:** `app/Data/TicketData.php`

```php
<?php

namespace App\Data;

use Spatie\LaravelData\Data;
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Attributes\Validation\Max;
use Spatie\LaravelData\Attributes\Validation\In;

class TicketData extends Data
{
    public function __construct(
        #[Required, Max(255)]
        public string $title,

        #[Required]
        public string $description,

        #[In(['low', 'medium', 'high', 'urgent'])]
        public string $priority = 'medium',

        public ?int $team_id = null,
    ) {}
}
```

**d) CreateTicketAction (Laravel Actions):**

```bash
docker-compose exec orionone-app php artisan make:action CreateTicketAction
```

**Ficheiro:** `app/Actions/Tickets/CreateTicketAction.php`

```php
<?php

namespace App\Actions\Tickets;

use App\Data\TicketData;
use App\Models\Ticket;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Lorisleiva\Actions\Concerns\AsAction;

class CreateTicketAction
{
    use AsAction;

    public function handle(TicketData $data, User $requester): Ticket
    {
        return DB::transaction(function () use ($data, $requester) {
            $ticket = Ticket::create([
                'ticket_number' => $this->generateTicketNumber(),
                'title' => $data->title,
                'description' => $data->description,
                'priority' => $data->priority,
                'requester_id' => $requester->id,
                'team_id' => $data->team_id,
                'assigned_to' => $data->team_id
                    ? $this->findAvailableAgent($data->team_id)?->id
                    : null,
            ]);

            activity()
                ->performedOn($ticket)
                ->causedBy($requester)
                ->log('Ticket criado');

            return $ticket->fresh();
        });
    }

    protected function generateTicketNumber(): string
    {
        $prefix = 'TK';
        $date = now()->format('Ymd');
        $count = Ticket::whereDate('created_at', today())->count() + 1;

        return sprintf('%s-%s-%04d', $prefix, $date, $count);
    }

    protected function findAvailableAgent(int $teamId): ?User
    {
        return User::role('agent')
            ->whereHas('teams', fn($q) => $q->where('teams.id', $teamId))
            ->withCount(['assignedTickets' => fn($q) => $q->whereIn('status', ['open', 'in_progress'])])
            ->orderBy('assigned_tickets_count')
            ->first();
    }

    public function asController(): \Illuminate\Http\RedirectResponse
    {
        $data = TicketData::from(request());

        $ticket = $this->handle($data, auth()->user());

        return redirect()->route('tickets.show', $ticket)
            ->with('success', 'Ticket criado com sucesso!');
    }
}
```

**e) Registar Route:**

```php
// routes/web.php
use App\Actions\Tickets\CreateTicketAction;

Route::post('/tickets', CreateTicketAction::class)->name('tickets.store');
```

**f) Adicionar relationship no User Model:**

```php
// app/Models/User.php
public function assignedTickets(): HasMany
{
    return $this->hasMany(Ticket::class, 'assigned_to');
}
```

**Rodar testes novamente:**

```bash
docker-compose exec orionone-app php artisan test --filter=CreateTicketTest
# GREEN: Testes passam!
```

#### Phase 4: Frontend (Vue + Shadcn-vue)

**Criar:** `resources/js/Pages/Tickets/Create.vue`

```vue
<script setup>
import { useForm } from "@inertiajs/vue3";
import AuthenticatedLayout from "@/Layouts/AuthenticatedLayout.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Textarea from "@/components/ui/Textarea.vue";
import Select from "@/components/ui/Select.vue";

const props = defineProps({
    teams: Array,
});

const form = useForm({
    title: "",
    description: "",
    priority: "medium",
    team_id: null,
});

const submit = () => {
    form.post(route("tickets.store"));
};
</script>

<template>
    <AuthenticatedLayout>
        <div class="max-w-2xl mx-auto p-6">
            <h1 class="text-2xl font-bold mb-6">Criar Novo Ticket</h1>

            <form @submit.prevent="submit" class="space-y-6">
                <!-- Title -->
                <div>
                    <label class="block text-sm font-medium mb-2">
                        Título *
                    </label>
                    <Input
                        v-model="form.title"
                        placeholder="Descreva brevemente o problema"
                        required
                    />
                    <p
                        v-if="form.errors.title"
                        class="mt-2 text-sm text-red-600"
                    >
                        {{ form.errors.title }}
                    </p>
                </div>

                <!-- Description -->
                <div>
                    <label class="block text-sm font-medium mb-2">
                        Descrição *
                    </label>
                    <Textarea
                        v-model="form.description"
                        rows="6"
                        placeholder="Explique o problema em detalhe"
                        required
                    />
                    <p
                        v-if="form.errors.description"
                        class="mt-2 text-sm text-red-600"
                    >
                        {{ form.errors.description }}
                    </p>
                </div>

                <!-- Priority -->
                <div>
                    <label class="block text-sm font-medium mb-2">
                        Prioridade
                    </label>
                    <Select v-model="form.priority">
                        <option value="low">Baixa</option>
                        <option value="medium">Média</option>
                        <option value="high">Alta</option>
                        <option value="urgent">Urgente</option>
                    </Select>
                </div>

                <!-- Team (optional) -->
                <div v-if="teams?.length">
                    <label class="block text-sm font-medium mb-2">
                        Equipa (Opcional)
                    </label>
                    <Select v-model="form.team_id">
                        <option :value="null">Atribuir automaticamente</option>
                        <option
                            v-for="team in teams"
                            :key="team.id"
                            :value="team.id"
                        >
                            {{ team.name }}
                        </option>
                    </Select>
                </div>

                <!-- Submit -->
                <div class="flex space-x-4">
                    <Button type="submit" :disabled="form.processing">
                        Criar Ticket
                    </Button>
                    <Button
                        type="button"
                        variant="outline"
                        @click="$inertia.visit(route('tickets.index'))"
                    >
                        Cancelar
                    </Button>
                </div>
            </form>
        </div>
    </AuthenticatedLayout>
</template>
```

---

### Feature 4: List Tickets with Filtering

#### Phase 1: Planning (30 min)

**User Story:**
Como utilizador, quero ver lista de tickets com filtros de status e prioridade.

**Critérios de Aceitação:**

-   Lista paginada (12 por página)
-   Filtro por status via URL: `?filter[status]=open`
-   Filtro por prioridade: `?filter[priority]=high`
-   Search por título: `?filter[search]=laptop`
-   Ordenação: `?sort=-created_at`
-   Usar Spatie Query Builder

#### Phase 2: Tests First (RED)

```bash
docker-compose exec orionone-app php artisan make:test ListTicketsTest
```

**Ficheiro:** `tests/Feature/ListTicketsTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use App\Models\Ticket;
use Illuminate\Foundation\Testing\RefreshDatabase;

class ListTicketsTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_view_tickets_list(): void
    {
        $user = User::factory()->create();
        Ticket::factory()->count(5)->create(['requester_id' => $user->id]);

        $response = $this->actingAs($user)->get(route('tickets.index'));

        $response->assertOk();
        $response->assertInertia(fn ($page) =>
            $page->component('Tickets/Index')
                 ->has('tickets.data', 5)
        );
    }

    public function test_can_filter_tickets_by_status(): void
    {
        $user = User::factory()->create();

        Ticket::factory()->count(3)->create([
            'requester_id' => $user->id,
            'status' => 'open',
        ]);

        Ticket::factory()->count(2)->create([
            'requester_id' => $user->id,
            'status' => 'closed',
        ]);

        $response = $this->actingAs($user)->get(route('tickets.index', [
            'filter' => ['status' => 'open'],
        ]));

        $response->assertOk();
        $response->assertInertia(fn ($page) =>
            $page->has('tickets.data', 3)
        );
    }

    public function test_can_search_tickets_by_title(): void
    {
        $user = User::factory()->create();

        Ticket::factory()->create([
            'requester_id' => $user->id,
            'title' => 'Laptop não liga',
        ]);

        Ticket::factory()->create([
            'requester_id' => $user->id,
            'title' => 'Impressora com erro',
        ]);

        $response = $this->actingAs($user)->get(route('tickets.index', [
            'filter' => ['search' => 'laptop'],
        ]));

        $response->assertOk();
        $response->assertInertia(fn ($page) =>
            $page->has('tickets.data', 1)
        );
    }

    public function test_can_sort_tickets_by_created_at(): void
    {
        $user = User::factory()->create();

        $old = Ticket::factory()->create([
            'requester_id' => $user->id,
            'created_at' => now()->subDays(5),
        ]);

        $new = Ticket::factory()->create([
            'requester_id' => $user->id,
            'created_at' => now(),
        ]);

        $response = $this->actingAs($user)->get(route('tickets.index', [
            'sort' => '-created_at',
        ]));

        $response->assertOk();
        $response->assertInertia(fn ($page) =>
            $page->where('tickets.data.0.id', $new->id)
        );
    }
}
```

**Rodar testes (vai falhar - esperado!):**

```bash
docker-compose exec orionone-app php artisan test --filter=ListTicketsTest
# RED: Route tickets.index not defined
```

#### Phase 3: Implementation (GREEN)

**a) TicketController:**

```bash
docker-compose exec orionone-app php artisan make:controller TicketController
```

**Ficheiro:** `app/Http/Controllers/TicketController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Ticket;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Spatie\QueryBuilder\QueryBuilder;
use Spatie\QueryBuilder\AllowedFilter;

class TicketController extends Controller
{
    public function index()
    {
        $tickets = QueryBuilder::for(Ticket::class)
            ->allowedFilters([
                AllowedFilter::partial('search', 'title'),
                AllowedFilter::exact('status'),
                AllowedFilter::exact('priority'),
            ])
            ->allowedSorts(['created_at', 'priority', 'status'])
            ->defaultSort('-created_at')
            ->with(['requester', 'assignee'])
            ->paginate(12)
            ->withQueryString();

        return Inertia::render('Tickets/Index', [
            'tickets' => $tickets,
            'filters' => request()->only(['filter', 'sort']),
        ]);
    }
}
```

**b) Registar Route:**

```php
// routes/web.php
Route::get('/tickets', [TicketController::class, 'index'])->name('tickets.index');
```

**c) Factory para testes:**

```bash
docker-compose exec orionone-app php artisan make:factory TicketFactory
```

**Ficheiro:** `database/factories/TicketFactory.php`

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
            'ticket_number' => 'TK-' . now()->format('Ymd') . '-' . rand(1000, 9999),
            'title' => fake()->sentence(),
            'description' => fake()->paragraph(),
            'status' => fake()->randomElement(['open', 'in_progress', 'resolved', 'closed']),
            'priority' => fake()->randomElement(['low', 'medium', 'high', 'urgent']),
            'requester_id' => User::factory(),
        ];
    }
}
```

**Rodar testes novamente:**

```bash
docker-compose exec orionone-app php artisan test --filter=ListTicketsTest
# GREEN: Testes passam!
```

#### Phase 4: Frontend (Vue + Shadcn-vue)

**Criar:** `resources/js/Pages/Tickets/Index.vue`

```vue
<script setup>
import { ref, watch } from "vue";
import { router } from "@inertiajs/vue3";
import AuthenticatedLayout from "@/Layouts/AuthenticatedLayout.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Select from "@/components/ui/Select.vue";
import Card from "@/components/ui/Card.vue";
import { Icon } from "@iconify/vue";

const props = defineProps({
    tickets: Object,
    filters: Object,
});

const search = ref(props.filters?.filter?.search || "");
const status = ref(props.filters?.filter?.status || "");
const priority = ref(props.filters?.filter?.priority || "");

const applyFilters = () => {
    router.get(
        route("tickets.index"),
        {
            filter: {
                search: search.value || undefined,
                status: status.value || undefined,
                priority: priority.value || undefined,
            },
        },
        { preserveState: true }
    );
};

const clearFilters = () => {
    search.value = "";
    status.value = "";
    priority.value = "";
    router.get(route("tickets.index"));
};

const statusColors = {
    open: "bg-blue-100 text-blue-800",
    in_progress: "bg-yellow-100 text-yellow-800",
    resolved: "bg-green-100 text-green-800",
    closed: "bg-gray-100 text-gray-800",
};
</script>

<template>
    <AuthenticatedLayout>
        <div class="p-6">
            <div class="flex items-center justify-between mb-6">
                <h1 class="text-2xl font-bold">Tickets</h1>
                <Button @click="router.visit(route('tickets.create'))">
                    <Icon icon="mdi:plus" class="w-5 h-5 mr-2" />
                    Novo Ticket
                </Button>
            </div>

            <!-- Filters -->
            <Card class="mb-6 p-4">
                <div class="grid gap-4 md:grid-cols-4">
                    <Input
                        v-model="search"
                        placeholder="Pesquisar..."
                        @keyup.enter="applyFilters"
                    />

                    <Select v-model="status" @change="applyFilters">
                        <option value="">Todos os status</option>
                        <option value="open">Aberto</option>
                        <option value="in_progress">Em progresso</option>
                        <option value="resolved">Resolvido</option>
                        <option value="closed">Fechado</option>
                    </Select>

                    <Select v-model="priority" @change="applyFilters">
                        <option value="">Todas prioridades</option>
                        <option value="low">Baixa</option>
                        <option value="medium">Média</option>
                        <option value="high">Alta</option>
                        <option value="urgent">Urgente</option>
                    </Select>

                    <Button variant="outline" @click="clearFilters">
                        Limpar Filtros
                    </Button>
                </div>
            </Card>

            <!-- Tickets Grid -->
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card
                    v-for="ticket in tickets.data"
                    :key="ticket.id"
                    class="cursor-pointer hover:shadow-lg transition p-4"
                    @click="router.visit(route('tickets.show', ticket.id))"
                >
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-500 font-mono">
                                {{ ticket.ticket_number }}
                            </span>
                            <span
                                :class="statusColors[ticket.status]"
                                class="px-2 py-1 text-xs font-medium rounded-full"
                            >
                                {{ ticket.status }}
                            </span>
                        </div>

                        <h3 class="font-medium text-gray-900 line-clamp-1">
                            {{ ticket.title }}
                        </h3>

                        <p class="text-sm text-gray-500 line-clamp-2">
                            {{ ticket.description }}
                        </p>

                        <div
                            class="flex items-center justify-between text-xs text-gray-500"
                        >
                            <span>{{ ticket.requester.name }}</span>
                            <span>{{ ticket.created_at_human }}</span>
                        </div>
                    </div>
                </Card>
            </div>

            <!-- Empty State -->
            <div
                v-if="tickets.data.length === 0"
                class="text-center py-12 text-gray-500"
            >
                Nenhum ticket encontrado.
            </div>

            <!-- Pagination -->
            <div
                v-if="tickets.links.length > 3"
                class="mt-6 flex justify-center space-x-2"
            >
                <Button
                    v-for="(link, index) in tickets.links"
                    :key="index"
                    variant="outline"
                    size="sm"
                    :disabled="!link.url || link.active"
                    @click="router.visit(link.url)"
                    v-html="link.label"
                />
            </div>
        </div>
    </AuthenticatedLayout>
</template>
```

---

### Feature 5: API Documentation Setup (Swagger)

#### Phase 1: Planning (20 min)

**Objetivo:**
Configurar L5-Swagger para documentar automaticamente a API REST do OrionOne.

**Critérios de Aceitação:**

-   Instalação e configuração L5-Swagger
-   Annotations básicas nos Controllers existentes
-   Route `/api/documentation` acessível
-   Documentação auto-gerada para Tickets API

#### Phase 2: Installation & Configuration

**a) Instalar L5-Swagger:**

```bash
docker-compose exec orionone-app composer require "darkaonline/l5-swagger"
docker-compose exec orionone-app php artisan vendor:publish --provider="L5Swagger\L5SwaggerServiceProvider"
```

**b) Configurar em `config/l5-swagger.php`:**

```php
'defaults' => [
    'api' => [
        'title' => 'OrionOne Helpdesk API',
        'description' => 'API documentation for OrionOne ticket management system',
        'version' => '1.0.0',
    ],
    'routes' => [
        'api' => 'api/documentation',
    ],
],
```

**c) Adicionar annotations básicas em `app/Http/Controllers/Controller.php`:**

```php
/**
 * @OA\Info(
 *     title="OrionOne Helpdesk API",
 *     version="1.0.0",
 *     description="API REST para sistema de gestão de tickets",
 *     @OA\Contact(
 *         email="support@orionone.com"
 *     )
 * )
 *
 * @OA\Server(
 *     url="http://localhost:8888",
 *     description="Development Server"
 * )
 *
 * @OA\SecurityScheme(
 *     securityScheme="sanctum",
 *     type="http",
 *     scheme="bearer",
 *     bearerFormat="JWT"
 * )
 */
abstract class Controller
{
    //
}
```

#### Phase 3: Document Tickets API

**Adicionar annotations em `TicketController`:**

```php
/**
 * @OA\Get(
 *     path="/api/tickets",
 *     summary="List all tickets",
 *     description="Retrieve paginated list of tickets with optional filters",
 *     operationId="getTickets",
 *     tags={"Tickets"},
 *     security={{"sanctum":{}}},
 *     @OA\Parameter(
 *         name="filter[status]",
 *         in="query",
 *         description="Filter by status",
 *         required=false,
 *         @OA\Schema(type="string", enum={"open","in_progress","resolved","closed"})
 *     ),
 *     @OA\Parameter(
 *         name="filter[priority]",
 *         in="query",
 *         description="Filter by priority",
 *         required=false,
 *         @OA\Schema(type="string", enum={"low","medium","high","urgent"})
 *     ),
 *     @OA\Parameter(
 *         name="sort",
 *         in="query",
 *         description="Sort by field (use - for descending)",
 *         required=false,
 *         @OA\Schema(type="string", example="-created_at")
 *     ),
 *     @OA\Response(
 *         response=200,
 *         description="Successful operation",
 *         @OA\JsonContent(
 *             type="object",
 *             @OA\Property(property="data", type="array", @OA\Items(ref="#/components/schemas/Ticket")),
 *             @OA\Property(property="links", type="object"),
 *             @OA\Property(property="meta", type="object")
 *         )
 *     ),
 *     @OA\Response(response=401, description="Unauthenticated")
 * )
 */
public function index(Request $request)
{
    // ...
}

/**
 * @OA\Post(
 *     path="/api/tickets",
 *     summary="Create a new ticket",
 *     description="Create a new support ticket",
 *     operationId="createTicket",
 *     tags={"Tickets"},
 *     security={{"sanctum":{}}},
 *     @OA\RequestBody(
 *         required=true,
 *         @OA\JsonContent(
 *             required={"title","description"},
 *             @OA\Property(property="title", type="string", maxLength=255, example="Laptop não liga"),
 *             @OA\Property(property="description", type="string", example="Detalhes do problema..."),
 *             @OA\Property(property="priority", type="string", enum={"low","medium","high","urgent"}, example="high"),
 *             @OA\Property(property="category_id", type="integer", example=1)
 *         )
 *     ),
 *     @OA\Response(
 *         response=201,
 *         description="Ticket created successfully",
 *         @OA\JsonContent(ref="#/components/schemas/Ticket")
 *     ),
 *     @OA\Response(response=422, description="Validation error")
 * )
 */
public function store(Request $request)
{
    // ...
}
```

**Definir schema de Ticket (adicionar no topo de `Ticket` model):**

```php
/**
 * @OA\Schema(
 *     schema="Ticket",
 *     type="object",
 *     title="Ticket",
 *     description="Ticket model",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="title", type="string", example="Problema com impressora"),
 *     @OA\Property(property="description", type="string"),
 *     @OA\Property(property="status", type="string", enum={"open","in_progress","resolved","closed"}),
 *     @OA\Property(property="priority", type="string", enum={"low","medium","high","urgent"}),
 *     @OA\Property(property="requester_id", type="integer"),
 *     @OA\Property(property="assigned_to", type="integer", nullable=true),
 *     @OA\Property(property="created_at", type="string", format="date-time"),
 *     @OA\Property(property="updated_at", type="string", format="date-time")
 * )
 */
class Ticket extends Model
{
    // ...
}
```

#### Phase 4: Generate & Test Documentation

**a) Gerar documentação:**

```bash
docker-compose exec orionone-app php artisan l5-swagger:generate
```

**b) Aceder à documentação:**

Abrir browser: `http://localhost:8888/api/documentation`

**c) Testar endpoints:**

-   Clicar em "Authorize" → Inserir token Sanctum
-   Testar GET `/api/tickets`
-   Testar POST `/api/tickets`
-   Verificar responses

#### Checklist Feature 5 (Swagger)

-   [ ] Pacote L5-Swagger instalado
-   [ ] Configuração publicada e editada
-   [ ] Annotations básicas em Controller.php
-   [ ] Annotations em TicketController (GET + POST)
-   [ ] Schema do Ticket definido
-   [ ] Documentação gerada com sucesso
-   [ ] Route `/api/documentation` acessível
-   [ ] Endpoints testados via Swagger UI
-   [ ] Adicionado ao `.gitignore`: `storage/api-docs/`

**Nota:** Em Sprint 6, expandiremos a documentação para cobrir todos os endpoints (Comments, Teams, KB, etc).

---

**Checkpoint:** Rodar todos os testes de Sprint 2:

```bash
docker-compose exec orionone-app php artisan test
# Todos os testes devem passar
```

---

## Sprint 3: Colaboração (02-15 Dez)

### Feature 5: Comments System

#### Phase 1: Planning (30 min)

**User Story:**
Como utilizador, quero comentar em tickets para colaborar na resolução.

**Critérios de Aceitação:**

-   Comentários públicos (visíveis para todos) e internos (só agents/admins)
-   Rich text editor para formatação
-   Menção de utilizadores (@username)
-   Upload de anexos nos comentários
-   Notificação por email quando mencionado
-   Activity log de comentários

#### Phase 2: Tests First (RED)

```bash
docker-compose exec orionone-app php artisan make:test CommentTest
```

**Ficheiro:** `tests/Feature/CommentTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use App\Models\Ticket;
use App\Models\Comment;
use Illuminate\Foundation\Testing\RefreshDatabase;

class CommentTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_public_comment(): void
    {
        $user = User::factory()->create();
        $ticket = Ticket::factory()->create();

        $response = $this->actingAs($user)->post(route('tickets.comments.store', $ticket), [
            'body' => 'Este é um comentário público',
            'is_internal' => false,
        ]);

        $response->assertRedirect();
        $this->assertDatabaseHas('comments', [
            'ticket_id' => $ticket->id,
            'user_id' => $user->id,
            'body' => 'Este é um comentário público',
            'is_internal' => false,
        ]);
    }

    public function test_agent_can_create_internal_comment(): void
    {
        $agent = User::factory()->create();
        $agent->assignRole('agent');
        $ticket = Ticket::factory()->create();

        $response = $this->actingAs($agent)->post(route('tickets.comments.store', $ticket), [
            'body' => 'Nota interna',
            'is_internal' => true,
        ]);

        $response->assertRedirect();
        $this->assertDatabaseHas('comments', [
            'is_internal' => true,
        ]);
    }

    public function test_regular_user_cannot_see_internal_comments(): void
    {
        $user = User::factory()->create();
        $user->assignRole('user');

        $ticket = Ticket::factory()->create(['requester_id' => $user->id]);
        Comment::factory()->create([
            'ticket_id' => $ticket->id,
            'is_internal' => true,
            'body' => 'Internal note',
        ]);

        $response = $this->actingAs($user)->get(route('tickets.show', $ticket));

        $response->assertDontSee('Internal note');
    }

    public function test_comment_body_is_required(): void
    {
        $user = User::factory()->create();
        $ticket = Ticket::factory()->create();

        $response = $this->actingAs($user)->post(route('tickets.comments.store', $ticket), [
            'body' => '',
        ]);

        $response->assertSessionHasErrors(['body']);
    }
}
```

**Rodar testes:**

```bash
docker-compose exec orionone-app php artisan test --filter=CommentTest
# RED: Table 'comments' doesn't exist
```

#### Phase 3: Implementation (GREEN)

**a) Migration:**

```bash
docker-compose exec orionone-app php artisan make:migration create_comments_table
```

```php
public function up(): void
{
    Schema::create('comments', function (Blueprint $table) {
        $table->id();
        $table->foreignId('ticket_id')->constrained()->onDelete('cascade');
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->text('body');
        $table->boolean('is_internal')->default(false);
        $table->timestamps();
        $table->softDeletes();

        $table->index(['ticket_id', 'created_at']);
    });
}
```

**b) Model:**

```bash
docker-compose exec orionone-app php artisan make:model Comment
```

**c) CommentData + CreateCommentAction:**

```bash
docker-compose exec orionone-app php artisan make:data CommentData
docker-compose exec orionone-app php artisan make:action CreateCommentAction
```

**d) Atualizar Ticket Model:**

```php
public function comments(): HasMany
{
    return $this->hasMany(Comment::class)->orderBy('created_at');
}

public function publicComments(): HasMany
{
    return $this->comments()->where('is_internal', false);
}
```

**e) Controller:**

```php
// app/Http/Controllers/CommentController.php
public function store(Request $request, Ticket $ticket)
{
    $validated = $request->validate([
        'body' => 'required|string|min:3',
        'is_internal' => 'boolean',
    ]);

    // Só agents/admins podem criar notas internas
    if ($validated['is_internal'] && !auth()->user()->hasAnyRole(['agent', 'admin'])) {
        abort(403);
    }

    $comment = $ticket->comments()->create([
        'user_id' => auth()->id(),
        'body' => $validated['body'],
        'is_internal' => $validated['is_internal'] ?? false,
    ]);

    activity()
        ->performedOn($ticket)
        ->causedBy(auth()->user())
        ->log('Comentário adicionado');

    return back()->with('success', 'Comentário adicionado!');
}
```

**Rodar testes novamente:**

```bash
docker-compose exec orionone-app php artisan test --filter=CommentTest
# GREEN: Testes passam!
```

#### Phase 4: Frontend

Adicionar secção de comentários em `Tickets/Show.vue` com editor rich text (Tiptap).

---

### Feature 6: Teams Management

#### Phase 1: Planning (30 min)

**User Story:**
Como admin, quero organizar agents em equipas para distribuir tickets.

**Critérios de Aceitação:**

-   CRUD de equipas
-   Atribuir agents a equipas
-   Auto-assignment baseado em equipa
-   Dashboard por equipa

#### Phase 2-4: Implementação

Similar ao padrão anterior:

-   Migration `teams` + pivot `team_user`
-   Model Team com relationships
-   TeamController (Query Builder)
-   Testes de assignments
-   Interface de gestão

---

### Feature 7: Email Notifications

#### Phase 1: Planning (30 min)

**User Story:**
Como utilizador, quero receber emails quando há updates nos meus tickets.

**Critérios de Aceitação:**

-   Email quando ticket atribuído
-   Email quando comentário adicionado
-   Email quando status muda
-   Email quando mencionado
-   Unsubscribe link

#### Phase 2-4: Implementação

```bash
docker-compose exec orionone-app php artisan make:notification TicketAssignedNotification
docker-compose exec orionone-app php artisan make:notification CommentAddedNotification
docker-compose exec orionone-app php artisan make:notification TicketStatusChangedNotification
```

Usar **Laravel Queues** para envio assíncrono.

---

## Sprint 4: Knowledge Base (16-29 Dez)

### Feature 8: Articles CRUD

#### Phase 1: Planning (30 min)

**User Story:**
Como agent, quero criar artigos de knowledge base para reduzir tickets repetitivos.

**Critérios de Aceitação:**

-   Editor rich text (Tiptap)
-   Categorias hierárquicas
-   Tags para categorização
-   Busca full-text
-   Métricas de utilidade (upvote/downvote)
-   Histórico de versões

#### Phase 2: Tests First (RED)

```bash
docker-compose exec orionone-app php artisan make:test ArticleTest
```

Testes para:

-   Criar artigo
-   Publicar/despublicar
-   Pesquisa
-   Votação útil/não útil

#### Phase 3: Implementation (GREEN)

**Migrations:**

```bash
docker-compose exec orionone-app php artisan make:migration create_articles_table
docker-compose exec orionone-app php artisan make:migration create_categories_table
docker-compose exec orionone-app php artisan make:migration create_article_votes_table
```

**Models:**

-   Article (title, slug, body, status, views, helpful_votes)
-   Category (name, slug, parent_id)
-   ArticleVote (user_id, article_id, is_helpful)

**Full-text Search:**

```php
// Usar Scout + Meilisearch ou PostgreSQL Full-Text Search
$articles = Article::search($query)
    ->where('status', 'published')
    ->paginate(20);
```

#### Phase 4: Frontend

-   Lista de categorias com contador
-   Página de artigo com TOC (table of contents)
-   Botões de feedback (útil/não útil)
-   Editor Tiptap para criação

---

### Feature 9: KB Search & Browse

Interface de pesquisa com:

-   Autocomplete
-   Filtros por categoria
-   Artigos relacionados
-   Artigos mais vistos

---

## Sprint 5: Dashboard & Reports (30 Dez - 12 Jan)

### Feature 10: Admin Dashboard

#### Phase 1: Planning (30 min)

**User Story:**
Como admin, quero ver métricas do sistema para tomar decisões.

**Critérios de Aceitação:**

-   Total de tickets (open, closed, in progress)
-   Gráfico de tickets por dia (últimos 30 dias)
-   SLA compliance rate
-   Tickets por prioridade
-   Performance por agent
-   Tempo médio de resolução

#### Phase 2-4: Implementação

**Controller:**

```php
public function index()
{
    $stats = [
        'total_tickets' => Ticket::count(),
        'open_tickets' => Ticket::where('status', 'open')->count(),
        'avg_resolution_time' => Ticket::whereNotNull('resolved_at')
            ->selectRaw('AVG(TIMESTAMPDIFF(HOUR, created_at, resolved_at)) as avg')
            ->value('avg'),
        'tickets_by_priority' => Ticket::groupBy('priority')
            ->selectRaw('priority, count(*) as total')
            ->pluck('total', 'priority'),
        'tickets_chart' => Ticket::whereBetween('created_at', [now()->subDays(30), now()])
            ->groupBy(DB::raw('DATE(created_at)'))
            ->selectRaw('DATE(created_at) as date, count(*) as total')
            ->get(),
    ];

    return Inertia::render('Dashboard', $stats);
}
```

**Frontend:**

Usar **Chart.js** ou **ApexCharts** para gráficos.

---

### Feature 11: Reports & Export

-   Exportar relatórios para PDF (DomPDF)
-   Exportar para Excel (Laravel Excel)
-   Relatórios agendados (Laravel Scheduler)

---

## Sprint 6: Polish & Deploy (13-26 Jan)

### Feature 12: API Documentation (Swagger)

#### Configuração L5-Swagger

```bash
docker-compose exec orionone-app composer require "darkaonline/l5-swagger"
docker-compose exec orionone-app php artisan vendor:publish --provider="L5Swagger\L5SwaggerServiceProvider"
```

**Configurar annotations nos Controllers:**

```php
/**
 * @OA\Post(
 *     path="/api/tickets",
 *     summary="Create a new ticket",
 *     tags={"Tickets"},
 *     @OA\RequestBody(
 *         required=true,
 *         @OA\JsonContent(
 *             required={"title","description"},
 *             @OA\Property(property="title", type="string", example="Laptop issue"),
 *             @OA\Property(property="description", type="string"),
 *             @OA\Property(property="priority", type="string", enum={"low","medium","high","urgent"})
 *         )
 *     ),
 *     @OA\Response(response=201, description="Ticket created successfully")
 * )
 */
public function store(Request $request) { }
```

**Gerar documentação:**

```bash
docker-compose exec orionone-app php artisan l5-swagger:generate
```

**Aceder:** http://localhost:8888/api/documentation

---

### Feature 13: Performance Optimization

-   **Caching:** Redis para queries pesadas
-   **Eager Loading:** Evitar N+1 queries
-   **Image Optimization:** Intervention Image
-   **CDN:** Para assets estáticos
-   **Database Indexing:** Revisar indexes

**Exemplo caching:**

```php
$stats = Cache::remember('dashboard.stats', 300, function () {
    return [
        'total_tickets' => Ticket::count(),
        // ...
    ];
});
```

---

### Feature 14: Testing & QA

**a) Testes E2E (Laravel Dusk):**

```bash
docker-compose exec orionone-app composer require --dev laravel/dusk
docker-compose exec orionone-app php artisan dusk:install
```

**Exemplo teste:**

```php
public function testUserCanCreateTicket()
{
    $this->browse(function (Browser $browser) {
        $browser->loginAs(User::find(1))
                ->visit('/tickets/create')
                ->type('title', 'Test Ticket')
                ->type('description', 'Test Description')
                ->press('Criar Ticket')
                ->assertPathIs('/tickets/1');
    });
}
```

**b) Load Testing (Apache Bench):**

```bash
ab -n 1000 -c 10 http://localhost:8888/tickets
```

**c) Security Audit:**

```bash
docker-compose exec orionone-app composer audit
```

---

### Feature 15: Deployment

**a) Setup Production Environment:**

-   VPS (DigitalOcean, AWS, Azure)
-   Domain + SSL (Let's Encrypt)
-   GitHub Actions CI/CD
-   Monitoring (Laravel Telescope + Sentry)

**b) GitHub Actions Workflow:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
    push:
        branches: [main]

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3
            - name: Setup PHP
              uses: shivammathur/setup-php@v2
              with:
                  php-version: "8.4"
            - name: Install Dependencies
              run: composer install --no-dev --optimize-autoloader
            - name: Run Tests
              run: php artisan test
            - name: Deploy
              run: |
                  ssh user@server 'cd /var/www/orionone && git pull && php artisan migrate --force'
```

**c) Monitoring Setup:**

```bash
# Install Sentry SDK
docker-compose exec orionone-app composer require sentry/sentry-laravel

# Configure
SENTRY_LARAVEL_DSN=your-sentry-dsn
```

---

### Checklist Final Sprint 6

-   [ ] API Documentation (Swagger) completa
-   [ ] Testes E2E com Dusk
-   [ ] Load testing executado
-   [ ] Security audit sem vulnerabilidades
-   [ ] Caching implementado
-   [ ] Performance: todas páginas < 500ms
-   [ ] Deploy production funcional
-   [ ] Monitoring (Sentry) configurado
-   [ ] Backup strategy definida
-   [ ] Documentation: README, User Manual, Deployment Guide
-   [ ] Video demo gravado
-   [ ] Apresentação preparada

---

## Checklist Resumo Completo

### Sprint 1: Auth & Users

-   [x] Laravel IDE Helper
-   [x] Inertia Progress
-   [x] Publicar configs Spatie
-   [x] RolePermissionSeeder (3 roles)
-   [x] UserSeeder (3 test users)
-   [x] Profile Avatar Upload

### Sprint 2: Tickets Core

-   [x] Migration tickets
-   [x] Model Ticket + relationships
-   [x] TicketData DTO
-   [x] CreateTicketAction
-   [x] TicketController + Query Builder
-   [x] Frontend: Index + Create
-   [ ] Factory + Seeders

### Sprint 3: Colaboração

-   [ ] Comments system (public + internal)
-   [ ] Teams management
-   [ ] Email notifications (queued)
-   [ ] Mention system (@username)

### Sprint 4: Knowledge Base

-   [ ] Articles CRUD
-   [ ] Categories hierarchy
-   [ ] Full-text search
-   [ ] Article voting (helpful/not)
-   [ ] Version history

### Sprint 5: Dashboard & Reports

-   [ ] Admin dashboard (metrics)
-   [ ] Charts (tickets por dia, SLA)
-   [ ] Agent performance reports
-   [ ] Export PDF/Excel
-   [ ] Scheduled reports

### Sprint 6: Polish & Deploy

-   [ ] API Documentation (L5-Swagger)
-   [ ] Performance optimization
-   [ ] E2E tests (Dusk)
-   [ ] Load testing
-   [ ] Security audit
-   [ ] Production deployment
-   [ ] Monitoring (Sentry)
-   [ ] Documentation completa
-   [ ] Video demo

---

## Features Opcionais (Nice-to-Have)

Se houver tempo extra após completar todos os 6 sprints:

### Tier 1 (Rápido - 1-2 dias cada)

-   [ ] Dark mode toggle
-   [ ] Multi-language support (i18n)
-   [ ] Advanced search com filtros
-   [ ] Ticket templates
-   [ ] Quick replies (canned responses)

### Tier 2 (Médio - 3-5 dias cada)

-   [ ] SLA automation (auto-escalate)
-   [ ] Mobile responsive optimization
-   [ ] Ticket merge functionality
-   [ ] Customer satisfaction survey
-   [ ] File versioning

### Tier 3 (Complexo - 1 semana cada)

-   [ ] Live chat integration
-   [ ] Webhook system para integrações
-   [ ] Custom fields por ticket type
-   [ ] API pública (OAuth 2.0)
-   [ ] Multi-tenancy support

---

## Estado Atual da Implementação

**Progresso Geral:** 15% (6 de 40 features completas)

### Sprint 1: Auth & Users - COMPLETO

-   [x] Laravel IDE Helper instalado
-   [x] Inertia Progress Bar configurado
-   [x] Publicar configs Spatie (Permission + Activity Log)
-   [x] RolePermissionSeeder criado (3 roles: admin, agent, user)
-   [x] UserSeeder criado (3 test users)
-   [x] RolePermissionTest passando (4/4 testes OK)
-   [ ] Profile Avatar Upload (planeado, não implementado)

**Código Implementado:**

-   OK `database/seeders/RolePermissionSeeder.php`
-   OK `database/seeders/UserSeeder.php`
-   OK `tests/Feature/RolePermissionTest.php`
-   OK Migrations: permissions, roles, activity_log
-   FALTA Avatar migration (não existe)
-   FALTA UpdateProfileAction (não existe)
-   FALTA UpdateProfileTest (não existe)

---

### Sprint 2: Tickets Core - NÃO INICIADO

-   [ ] Migration tickets (não existe)
-   [ ] Model Ticket (não existe)
-   [ ] TicketData DTO (não existe)
-   [ ] CreateTicketAction (pasta vazia)
-   [ ] TicketController (não existe)
-   [ ] Frontend: Tickets/Index.vue (não existe)
-   [ ] Frontend: Tickets/Create.vue (não existe)
-   [ ] CreateTicketTest (não existe)
-   [ ] ListTicketsTest (não existe)
-   [ ] TicketFactory (não existe)
-   [ ] Swagger L5 Setup (não instalado)

**Código Implementado:**

-   FALTA Nenhum código de tickets implementado
-   AVISO Pasta `app/Actions/Tickets/` existe mas está vazia

---

### Sprint 3: Colaboração - NÃO INICIADO

-   [ ] Comments system (público + interno)
-   [ ] Teams management
-   [ ] Email notifications (queued)
-   [ ] Mention system (@username)

---

### Sprint 4: Knowledge Base - NÃO INICIADO

-   [ ] Articles CRUD
-   [ ] Categories hierarchy
-   [ ] Full-text search
-   [ ] Article voting (helpful/not)
-   [ ] Version history

---

### Sprint 5: Dashboard & Reports - NÃO INICIADO

-   [ ] Admin dashboard (metrics)
-   [ ] Charts (tickets por dia, SLA)
-   [ ] Agent performance reports
-   [ ] Export PDF/Excel
-   [ ] Scheduled reports

---

### Sprint 6: Polish & Deploy - NÃO INICIADO

-   [ ] API Documentation (L5-Swagger)
-   [ ] Performance optimization
-   [ ] E2E tests (Dusk)
-   [ ] Load testing
-   [ ] Security audit
-   [ ] Production deployment
-   [ ] Monitoring (Sentry)
-   [ ] Documentation completa
-   [ ] Video demo

---

## Features Opcionais (Nice-to-Have)

Se houver tempo extra após completar todos os 6 sprints:

### Tier 1 (Rápido - 1-2 dias cada)

-   [ ] Dark mode toggle
-   [ ] Multi-language support (i18n)
-   [ ] Advanced search com filtros
-   [ ] Ticket templates
-   [ ] Quick replies (canned responses)

### Tier 2 (Médio - 3-5 dias cada)

-   [ ] SLA automation (auto-escalate)
-   [ ] Mobile responsive optimization
-   [ ] Ticket merge functionality
-   [ ] Customer satisfaction survey
-   [ ] File versioning

### Tier 3 (Complexo - 1 semana cada)

-   [ ] Live chat integration
-   [ ] Webhook system para integrações
-   [ ] Custom fields por ticket type
-   [ ] API pública (OAuth 2.0)
-   [ ] Multi-tenancy support

---

## Status Resumo

| Sprint    | Features | Completas | Em Progresso | Não Iniciadas | Status |
| --------- | -------- | --------- | ------------ | ------------- | ------ |
| Sprint 1  | 7        | 6         | 0            | 1             | 85%    |
| Sprint 2  | 5        | 0         | 0            | 5             | 0%     |
| Sprint 3  | 4        | 0         | 0            | 4             | 0%     |
| Sprint 4  | 5        | 0         | 0            | 5             | 0%     |
| Sprint 5  | 5        | 0         | 0            | 5             | 0%     |
| Sprint 6  | 9        | 0         | 0            | 9             | 0%     |
| **TOTAL** | **35**   | **6**     | **0**        | **29**        | **17%** |

---

**Próximos Passos Recomendados:**

1. **Completar Sprint 1** - Implementar Avatar Upload (Feature 2)
2. **Iniciar Sprint 2** - Criar sistema de Tickets (Feature 3 e 4)
3. **Setup Swagger** - Adicionar documentação API (Feature 5)

**Última Atualização:** 10 Novembro 2025, 02:20
**Última Verificação Automática:** 10 Novembro 2025, 02:20
