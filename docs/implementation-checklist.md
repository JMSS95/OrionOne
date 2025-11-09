# Implementation Checklist - OrionOne

**Sprint-by-Sprint Implementation Guide**

> Segue a filosofia **TDD + Feature-Driven Development** do [development-guide.md](./development-guide.md)
> Cada feature passa por: **Planning → Tests First → Implementation → Frontend**

---

## Sprint 1: Auth & Users (11-17 Nov)

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

**Checkpoint:** Rodar todos os testes de Sprint 2:

```bash
docker-compose exec orionone-app php artisan test
# Todos os testes devem passar
```

---

## Checklist Resumo

### Sprint 1

-   Instalar Laravel IDE Helper
-   Instalar Inertia Progress
-   Publicar configs Spatie (Permission + Activity Log)
-   Criar RolePermissionSeeder (3 roles: admin, agent, user)
-   Seed utilizadores teste
-   Adicionar campo avatar à tabela users
-   Criar UpdateProfileAction
-   Atualizar profile page com avatar upload

### Sprint 2

-   Migration tickets
-   Model Ticket com relationships
-   TicketData DTO
-   CreateTicketAction
-   TicketController com Query Builder
-   Página Tickets/Index (lista + filtros)
-   Página Tickets/Create (form)
-   Testes (>90% coverage)

---

**Continua nos próximos sprints...**

**Última Atualização:** 07 Novembro 2025, 23:45
