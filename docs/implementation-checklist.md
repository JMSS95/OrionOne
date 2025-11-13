# Implementation Checklist - OrionOne

**Sprint-by-Sprint Implementation Guide**

> Cada feature passa por: **Planning → Tests First (RED) → Implementation (GREEN) → Frontend**

---

## Sprint 1: Auth & Users (11-17 Nov)

**Nota Importante:** O sistema de autenticação (Laravel Breeze) já foi instalado e configurado durante a **Fase 0: Setup Inicial** (ver [SETUP.md](./SETUP.md)). Esta fase inclui:

-   Autenticação completa (login, register, password reset)
-   Proteção de rotas via middleware `auth`
-   Sistema de sessões
-   Profile page básica

**Sprint 1 foca-se em:**

-   Adicionar Roles & Permissions (via Spatie)
-   Expandir funcionalidades do Profile (avatar upload)
-   **Database Advanced Features** (Views, Triggers, Stored Procedures, Constraints)

**Database Enterprise Fundamentals (PostgreSQL 16):**

| Component             | Quantity      | Purpose                                                           | Status      |
| --------------------- | ------------- | ----------------------------------------------------------------- | ----------- |
| **Database Views**    | 3 views       | Dashboard, SLA, Agent Performance (queries pré-computadas)        | Documented  |
| **Triggers**          | 2 triggers    | Auto-generation (ticket_number), Auto-calculation (SLA deadlines) | Documented  |
| **Check Constraints** | 4 constraints | Data validation em DB (status, priority, email, dates)            | Documented  |
| **Advanced Indexes**  | -             | Partial, Composite, Expression (performance optimization)         | ⏳ Sprint 2 |

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

### Feature 4: Database Advanced Features (Views, Triggers, Stored Procedures)

#### IMPORTANTE: Executar APÓS Sprint 2 (tabelas tickets, teams, comments criadas)

**Estado Atual:**

-   Migrations criadas e prontas: `2025_11_12_232836_create_database_views.php`, `2025_11_12_233122_create_database_triggers.php`, `2025_11_12_233216_add_check_constraints_to_tables.php`
-   **REVERTIDAS** - Aguardam criação das tabelas necessárias
-   **Executar em:** Final do Sprint 2 (após Feature 3: Create Ticket)

#### Phase 1: Planning (20 min)

**Objetivo:**
Implementar features avançadas PostgreSQL para performance, automação e data integrity.

**Componentes Enterprise a adicionar:**

-   **3 Database Views** (queries pré-computadas para tickets, SLA, performance)
-   **2 Triggers** (automação: ticket_number, SLA deadlines)
-   **4 Check Constraints** (validation em DB: status, priority, email, dates)
-   **Advanced Indexes** (Partial, Composite, Expression)

**Dependências:**

-   Tabela `users` (já existe)
-   Tabela `tickets` (Sprint 2 - Feature 3)
-   Tabela `teams` (Sprint 6)
-   Tabela `comments` (Sprint 3)

**Referências:**

-   `docs/database-schema.md` - Documentação completa de Views, Triggers, Procedures
-   `docs/TECH-DEEP-DIVE-DATABASE.md` - Exemplos práticos com Laravel

#### Phase 2: Migrations Já Criadas (Prontas)

#### Phase 2: Migrations Já Criadas (Prontas)

**Status:** Migrations criadas mas revertidas até tabelas necessárias existirem.

**a) Migration para Views:** `database/migrations/2025_11_12_232836_create_database_views.php`

**Ficheiro já criado** com 3 views:

-   `v_ticket_dashboard` - Dashboard com JOINs de tickets, users, teams
-   `v_sla_compliance` - Status SLA (MET/BREACHED/PENDING)
-   `v_agent_performance` - Performance por agente (total, resolved, avg_hours)

**b) Migration para Triggers:** `database/migrations/2025_11_12_233122_create_database_triggers.php`

**Ficheiro já criado** com 2 triggers:

-   `trg_generate_ticket_number` - Auto-gera TKT-YYYYMMDD-NNNN
-   `trg_set_sla_deadlines` - Auto-calcula first_response_deadline e resolution_deadline

**c) Migration para Check Constraints:** `database/migrations/2025_11_12_233216_add_check_constraints_to_tables.php`

**Ficheiro já criado** com 4 constraints:

-   `chk_tickets_status` - Valida enum status
-   `chk_tickets_priority` - Valida enum priority
-   `chk_tickets_resolved_date` - Valida resolved_at >= created_at
-   `chk_users_email_format` - Valida formato email

#### Phase 3: Execute Migrations (Aguarda Sprint 2)

**Quando executar:**

1. Após criar tabela `tickets` (Sprint 2 - Feature 3: Create Ticket)
2. Após criar tabela `comments` (Sprint 3)
3. Após criar tabela `teams` (Sprint 6)

**Comando para executar:**

```bash
# Quando as tabelas tickets, teams, comments existirem
docker-compose exec orionone-app php artisan migrate
```

#### Phase 4: Test Database Features (Após Sprint 2)

**Testar Views:**

```bash
docker-compose exec orionone-app php artisan tinker
>>> DB::table('v_ticket_dashboard')->count();
>>> DB::table('v_sla_compliance')->where('first_response_sla_status', 'BREACHED')->count();
>>> DB::table('v_agent_performance')->orderBy('total_tickets', 'desc')->first();
```

**Testar Trigger (ticket_number auto-gerado):**

```bash
docker-compose exec orionone-app php artisan tinker
>>> $ticket = Ticket::create(['title' => 'Test', 'description' => 'Test', 'priority' => 'medium', 'requester_id' => 1]);
>>> $ticket->ticket_number; // Deve retornar: TKT-20251111-0001 (auto-gerado!)
```

**Testar Trigger (SLA deadlines auto-calculados):**

```bash
>>> $ticket = Ticket::create(['title' => 'Urgent', 'priority' => 'urgent', 'requester_id' => 1]);
>>> $ticket->first_response_deadline; // created_at + 2 hours
>>> $ticket->resolution_deadline; // created_at + 8 hours
```

**Testar Check Constraint:**

```bash
>>> Ticket::create(['status' => 'invalid_status']); // EXCEPTION: violates check constraint
>>> User::create(['email' => 'invalid-email']); // EXCEPTION: violates check constraint
```

#### Checklist Feature 4 (Database Advanced Features)

-   [x] Migration `create_database_views` criada (2025_11_12_232836)
-   [x] Migration `create_database_triggers` criada (2025_11_12_233122)
-   [x] Migration `add_check_constraints_to_tables` criada (2025_11_12_233216)
-   [ ] **⏳ Executar migrations após Sprint 2** (quando tabela tickets existir)
-   [ ] 3 Views funcionais (v_ticket_dashboard, v_sla_compliance, v_agent_performance)
-   [ ] Trigger `trg_generate_ticket_number` funcional (auto-gera TKT-YYYYMMDD-NNNN)
-   [ ] Trigger `trg_set_sla_deadlines` funcional (auto-calcula SLA por priority)
-   [ ] Check constraints validam enums e data logic
-   [ ] Testado em Tinker: Views retornam dados
-   [ ] Testado em Tinker: Triggers funcionam automaticamente
-   [ ] Testado em Tinker: Constraints bloqueiam dados inválidos
-   [x] Documentado em `database-schema.md` (já está)
-   [x] Documentado em `TECH-DEEP-DIVE-DATABASE.md` (já está)

**Status:** **Migrations prontas** | **Aguarda Sprint 2** (tabelas tickets, comments, teams)

**Benefícios implementados:**

**Performance:** Views pré-computam JOINs complexos (Dashboard 3x mais rápido)
**Automação:** Triggers eliminam código PHP repetitivo (ticket_number, SLA)
**Data Integrity:** Check Constraints garantem validation mesmo via SQL direto
**Enterprise-Ready:** Features PostgreSQL avançadas (nível senior/architect)

---

### Preparação Frontend: VueUse Composables (2h - 15-17 Nov)

**Objetivo:** Documentar VueUse composables para uso nos próximos Sprints.

**Contexto:** VueUse (`@vueuse/core: ^11.3.0`) **JÁ ESTÁ INSTALADO!** Apenas falta documentar uso.

#### Composables Críticos para OrionOne:

**1. useDark() - Dark Mode (Sprint 6)**

```javascript
// composables/useTheme.js
import { useDark, useToggle } from '@vueuse/core'

export function useTheme() {
 const isDark = useDark()
 const toggleDark = useToggle(isDark)

 return { isDark, toggleDark }
}

// Usar em componente:
const { isDark, toggleDark } = useTheme()

// Template:
<Button @click="toggleDark" variant="ghost" size="icon">
 <SunIcon v-if="isDark" />
 <MoonIcon v-else />
</Button>
```

**2. useStorage() - Persist Filters (Sprint 2)**

```javascript
// Persist ticket filters em localStorage
import { useStorage } from "@vueuse/core";

const filters = useStorage("ticket-filters", {
    status: "",
    priority: "",
    team_id: null,
});

// Reativo! Persiste automaticamente quando muda
filters.value.status = "open";
```

**3. useDebounceFn() - Search Performance (Sprint 2/4)**

```javascript
// Debounce search input (evita 50 API calls, faz apenas 1)
import { useDebounceFn } from "@vueuse/core";

const searchTickets = useDebounceFn((query) => {
    router.reload({
        data: { search: query },
        only: ["tickets"],
    });
}, 300); // 300ms delay
```

**4. useClipboard() - Copy Ticket Number (Sprint 2)**

```javascript
// Copy ticket number to clipboard
import { useClipboard } from "@vueuse/core";

const { copy, copied } = useClipboard();

const copyTicketNumber = (ticketNumber) => {
    copy(ticketNumber);
    toast.success("Número do ticket copiado!");
};
```

**5. useWindowSize() - Responsive Logic (Sprint 5)**

```javascript
// Responsive dashboard layout
import { useWindowSize } from '@vueuse/core'

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 768)

// Mostrar tabela simplificada no mobile
<DataTable v-if="!isMobile" />
<TicketCardList v-else />
```

#### Checklist VueUse Documentation

-   [ ] Criar `docs/VUEUSE-GUIDE.md` com exemplos práticos
-   [ ] Documentar `useDark()` para dark mode
-   [ ] Documentar `useStorage()` para persist filters
-   [ ] Documentar `useDebounceFn()` para search
-   [ ] Documentar `useClipboard()` para copy actions
-   [ ] Documentar `useWindowSize()` para responsive
-   [ ] Adicionar link em `TECH-DEEP-DIVE-FRONTEND.md` secção 7

**Referência completa:** [VueUse Docs](https://vueuse.org/) - 50+ composables disponíveis!

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

### Forms Avançadas: VeeValidate + Multi-file Upload + Shadcn Advanced (6h - 15-17 Nov)

**Objetivo:** Documentar patterns avançados para forms complexas no Create Ticket.

**Contexto:**

-   VeeValidate (`vee-validate: ^4.15.1`) **JÁ INSTALADO**
-   Shadcn-vue base (15 components) **JÁ CRIADOS**
-   ⏳ Falta adicionar: Dialog, DataTable, Toast, Combobox

---

#### 1. VeeValidate - Form Validation (1.5h)

**Setup Global (`resources/js/app.js`):**

```javascript
import { configure, defineRule } from "vee-validate";
import { required, email, min, max } from "@vee-validate/rules";
import { localize } from "@vee-validate/i18n";

// Registar regras básicas
defineRule("required", required);
defineRule("email", email);
defineRule("min", min);
defineRule("max", max);

// Custom rule: unique email (API call)
defineRule("unique_email", async (value) => {
    const response = await axios.get(`/api/check-email?email=${value}`);
    return response.data.available || "Email já existe";
});

// Mensagens em português
configure({
    generateMessage: localize("pt", {
        messages: {
            required: "Campo obrigatório",
            email: "Email inválido",
            min: "Mínimo {length} caracteres",
            max: "Máximo {length} caracteres",
        },
    }),
});
```

**Criar Field Component com VeeValidate:**

```vue
<!-- resources/js/components/ui/FormField.vue -->
<script setup>
import { Field, ErrorMessage } from "vee-validate";
import Label from "./Label.vue";

const props = defineProps({
    name: String,
    label: String,
    rules: [String, Object],
    type: { type: String, default: "text" },
    placeholder: String,
});
</script>

<template>
    <div class="space-y-2">
        <Label :for="name">{{ label }}</Label>

        <Field
            :id="name"
            :name="name"
            :rules="rules"
            :type="type"
            :placeholder="placeholder"
            v-slot="{ field, errors }"
        >
            <input
                v-bind="field"
                :class="[
                    'w-full rounded-md border px-3 py-2',
                    errors.length ? 'border-red-500' : 'border-gray-300',
                ]"
            />
        </Field>

        <ErrorMessage :name="name" class="text-sm text-red-600" />
    </div>
</template>
```

**Usar em Create Ticket Form:**

```vue
<script setup>
import { Form } from "vee-validate";
import FormField from "@/components/ui/FormField.vue";

const onSubmit = (values) => {
    router.post(route("tickets.store"), values);
};
</script>

<template>
    <Form @submit="onSubmit" class="space-y-6">
        <FormField
            name="title"
            label="Título"
            rules="required|max:255"
            placeholder="Laptop não liga"
        />

        <FormField
            name="description"
            label="Descrição"
            rules="required|min:10"
            type="textarea"
        />

        <Button type="submit">Criar Ticket</Button>
    </Form>
</template>
```

---

#### 2. Multi-file Upload with Preview (1h)

**Criar Attachment Upload Component:**

```vue
<!-- resources/js/components/ui/FileUpload.vue -->
<script setup>
import { ref } from "vue";
import { X } from "lucide-vue-next";
import Button from "./Button.vue";

const props = defineProps({
    maxFiles: { type: Number, default: 5 },
    maxSize: { type: Number, default: 10 }, // MB
    accept: {
        type: Array,
        default: () => ["pdf", "png", "jpg", "jpeg", "docx"],
    },
});

const emit = defineEmits(["update:modelValue"]);

const files = ref([]);
const error = ref("");

const handleFiles = (event) => {
    const newFiles = Array.from(event.target.files);

    // Validações
    if (files.value.length + newFiles.length > props.maxFiles) {
        error.value = `Máximo ${props.maxFiles} ficheiros`;
        return;
    }

    for (const file of newFiles) {
        // Check size
        if (file.size > props.maxSize * 1024 * 1024) {
            error.value = `Ficheiro ${file.name} excede ${props.maxSize}MB`;
            continue;
        }

        // Check type
        const ext = file.name.split(".").pop().toLowerCase();
        if (!props.accept.includes(ext)) {
            error.value = `Tipo ${ext} não permitido`;
            continue;
        }

        // Add preview
        files.value.push({
            file,
            name: file.name,
            size: (file.size / 1024).toFixed(2) + " KB",
            preview: file.type.startsWith("image/")
                ? URL.createObjectURL(file)
                : null,
        });
    }

    emit(
        "update:modelValue",
        files.value.map((f) => f.file)
    );
    error.value = "";
};

const removeFile = (index) => {
    files.value.splice(index, 1);
    emit(
        "update:modelValue",
        files.value.map((f) => f.file)
    );
};
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center gap-4">
            <input
                type="file"
                multiple
                :accept="accept.map((ext) => `.${ext}`).join(',')"
                @change="handleFiles"
                class="hidden"
                id="file-upload"
            />
            <label for="file-upload">
                <Button as="span" variant="outline" type="button">
                    Adicionar Ficheiros ({{ files.length }}/{{ maxFiles }})
                </Button>
            </label>

            <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
        </div>

        <!-- File List -->
        <div v-if="files.length" class="space-y-2">
            <div
                v-for="(file, index) in files"
                :key="index"
                class="flex items-center gap-4 p-3 border rounded-md"
            >
                <!-- Preview (se imagem) -->
                <img
                    v-if="file.preview"
                    :src="file.preview"
                    class="w-12 h-12 object-cover rounded"
                />

                <!-- Info -->
                <div class="flex-1">
                    <p class="text-sm font-medium">{{ file.name }}</p>
                    <p class="text-xs text-gray-500">{{ file.size }}</p>
                </div>

                <!-- Remove -->
                <Button
                    variant="ghost"
                    size="icon"
                    type="button"
                    @click="removeFile(index)"
                >
                    <X class="w-4 h-4" />
                </Button>
            </div>
        </div>
    </div>
</template>
```

**Integrar no Create Ticket Form:**

```vue
<script setup>
import FileUpload from "@/components/ui/FileUpload.vue";
import { useForm } from "@inertiajs/vue3";

const form = useForm({
    title: "",
    description: "",
    priority: "medium",
    attachments: [], // Array de Files
});

const submit = () => {
    // Inertia suporta multipart/form-data automaticamente!
    form.post(route("tickets.store"));
};
</script>

<template>
    <form @submit.prevent="submit">
        <!-- ... outros campos ... -->

        <FileUpload
            v-model="form.attachments"
            :max-files="5"
            :max-size="10"
            :accept="['pdf', 'png', 'jpg', 'docx']"
        />

        <Button type="submit" :disabled="form.processing">
            Criar Ticket
        </Button>
    </form>
</template>
```

**Backend - Handle Upload (CreateTicketAction):**

```php
use Illuminate\Http\UploadedFile;

public function handle(TicketData $data, User $requester, ?array $attachments = null): Ticket
{
 return DB::transaction(function () use ($data, $requester, $attachments) {
 $ticket = Ticket::create([
 'title' => $data->title,
 'description' => $data->description,
 'priority' => $data->priority,
 'requester_id' => $requester->id,
 ]);

 // Upload attachments
 if ($attachments) {
 foreach ($attachments as $file) {
 /** @var UploadedFile $file */

 // Validar mime type (prevenir spoofing)
 if (!in_array($file->getMimeType(), [
 'application/pdf',
 'image/png',
 'image/jpeg',
 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
 ])) {
 throw new \Exception("Tipo de ficheiro inválido: {$file->getMimeType()}");
 }

 // Upload com nome único
 $path = $file->store('attachments', 'public');

 // Criar registo na tabela attachments
 $ticket->attachments()->create([
 'filename' => $file->getClientOriginalName(),
 'path' => $path,
 'mime_type' => $file->getMimeType(),
 'size' => $file->getSize(),
 'uploaded_by' => $requester->id,
 ]);
 }
 }

 return $ticket->fresh(['attachments']);
 });
}
```

---

#### 3. Shadcn Advanced Components (1.5h)

**Adicionar components avançados via CLI:**

```bash
# Dialog (Modal)
npx shadcn-vue@latest add dialog

# Toast (Notifications)
npx shadcn-vue@latest add toast

# Combobox (Searchable Select)
npx shadcn-vue@latest add combobox

# DropdownMenu (Actions menu)
npx shadcn-vue@latest add dropdown-menu

# Tabs
npx shadcn-vue@latest add tabs

# Accordion
npx shadcn-vue@latest add accordion

# Command Palette (Ctrl+K)
npx shadcn-vue@latest add command
```

**3.1 Dialog - Create Ticket Modal:**

```vue
<script setup>
import { ref } from "vue";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import Button from "@/components/ui/Button.vue";
import CreateTicketForm from "./CreateTicketForm.vue";

const isOpen = ref(false);

const onSuccess = () => {
    isOpen.value = false;
    // Recarregar lista
    router.reload({ only: ["tickets"] });
};
</script>

<template>
    <div>
        <Button @click="isOpen = true">Criar Ticket</Button>

        <Dialog v-model:open="isOpen">
            <DialogContent class="max-w-2xl">
                <DialogHeader>
                    <DialogTitle>Criar Novo Ticket</DialogTitle>
                </DialogHeader>

                <CreateTicketForm @success="onSuccess" />
            </DialogContent>
        </Dialog>
    </div>
</template>
```

**3.2 Toast - Success/Error Feedback:**

```javascript
// Setup global toast (resources/js/app.js)
import { Toaster } from '@/components/ui/toast'

// Mount Toaster
createApp({ render: () => h(App) })
 .component('Toaster', Toaster)
 .mount('#app')

// Add to App.vue
<template>
 <Toaster />
 <router-view />
</template>
```

```vue
<!-- Usar em components -->
<script setup>
import { useToast } from "@/components/ui/toast";

const { toast } = useToast();

const createTicket = () => {
    form.post(route("tickets.store"), {
        onSuccess: () => {
            toast({
                title: "Sucesso!",
                description: "Ticket criado com sucesso.",
            });
        },
        onError: () => {
            toast({
                title: "Erro",
                description: "Erro ao criar ticket.",
                variant: "destructive",
            });
        },
    });
};
</script>
```

**3.3 Combobox - Assign Agent (Searchable Select):**

```vue
<script setup>
import { ref, computed } from "vue";
import {
    Combobox,
    ComboboxInput,
    ComboboxOption,
    ComboboxOptions,
} from "@/components/ui/combobox";
import { useDebounceFn } from "@vueuse/core";

const props = defineProps({
    teamId: Number,
});

const emit = defineEmits(["update:modelValue"]);

const agents = ref([]);
const search = ref("");

const searchAgents = useDebounceFn(async (query) => {
    const response = await axios.get(`/api/agents`, {
        params: { team_id: props.teamId, search: query },
    });
    agents.value = response.data;
}, 300);

const filteredAgents = computed(() => {
    if (!search.value) return agents.value;
    return agents.value.filter((agent) =>
        agent.name.toLowerCase().includes(search.value.toLowerCase())
    );
});
</script>

<template>
    <Combobox @update:modelValue="emit('update:modelValue', $event)">
        <ComboboxInput
            v-model="search"
            @input="searchAgents(search)"
            placeholder="Buscar agent..."
        />

        <ComboboxOptions>
            <ComboboxOption
                v-for="agent in filteredAgents"
                :key="agent.id"
                :value="agent.id"
            >
                {{ agent.name }} ({{ agent.open_tickets_count }} tickets
                abertos)
            </ComboboxOption>
        </ComboboxOptions>
    </Combobox>
</template>
```

**3.4 DropdownMenu - Ticket Actions:**

```vue
<script setup>
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MoreVertical, Edit, Trash, UserPlus } from "lucide-vue-next";
import Button from "./Button.vue";

const props = defineProps({
    ticket: Object,
});

const editTicket = () => {
    router.visit(route("tickets.edit", props.ticket.id));
};

const deleteTicket = () => {
    if (confirm("Tem certeza?")) {
        router.delete(route("tickets.destroy", props.ticket.id));
    }
};

const assignTicket = () => {
    // Abrir modal de assign
};
</script>

<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" size="icon">
                <MoreVertical class="w-4 h-4" />
            </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="end">
            <DropdownMenuItem @click="editTicket">
                <Edit class="w-4 h-4 mr-2" />
                Editar
            </DropdownMenuItem>

            <DropdownMenuItem @click="assignTicket">
                <UserPlus class="w-4 h-4 mr-2" />
                Atribuir
            </DropdownMenuItem>

            <DropdownMenuItem @click="deleteTicket" class="text-red-600">
                <Trash class="w-4 h-4 mr-2" />
                Apagar
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
```

#### Checklist Forms Avançadas

-   [ ] VeeValidate configurado globalmente com mensagens PT
-   [ ] FormField component criado com ErrorMessage
-   [ ] FileUpload component criado (preview, validação, remove)
-   [ ] Backend handle multi-file upload com mime validation
-   [ ] Shadcn Dialog adicionado (npx shadcn-vue add dialog)
-   [ ] Shadcn Toast adicionado e configurado globalmente
-   [ ] Shadcn Combobox adicionado (searchable select)
-   [ ] Shadcn DropdownMenu adicionado (actions menu)
-   [ ] Criar ticket form usa VeeValidate + FileUpload
-   [ ] Testado: Upload 5 ficheiros (PDF, PNG, DOCX)
-   [ ] Testado: Validação VeeValidate mostra erros
-   [ ] Testado: Toast aparece após sucesso/erro
-   [ ] Documentado em `docs/FORMS-GUIDE.md`

**Tempo estimado:** ~6h (VeeValidate 1.5h + FileUpload 1h + Shadcn 1.5h + Integration 2h)

---

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

### Feature 5: API Documentation Setup (Scribe)

#### Phase 1: Planning (20 min)

**Objetivo:**
Configurar Scribe para documentar automaticamente a API REST do OrionOne (já instalado: knuckleswtf/scribe 5.5).

**Critérios de Aceitação:**

-   Scribe já instalado e configurado
-   Annotations simples nos Controllers usando PHP DocBlock
-   Route `/docs` acessível com documentação interativa
-   OpenAPI 3.0 spec disponível em `/docs.openapi`
-   Try It Out funcional (testar endpoints no browser)
-   Documentação auto-gerada para Tickets API

#### Phase 2: Verificar Configuração Existente

**a) Verificar rotas Scribe:**

```bash
# Scribe já está instalado no projeto
docker-compose exec orionone-app php artisan route:list | grep docs
# GET /docs ............ scribe (HTML documentation)
# GET /docs.openapi ... scribe.openapi (OpenAPI 3.0 spec)
# GET /docs.postman ... scribe.postman (Postman collection)
```

**b) Configuração atual em `config/scribe.php` (já configurado):**

```php
'title' => 'OrionOne API Documentation',
'description' => 'API REST para sistema de gestão de tickets ITSM',
'base_url' => config('app.url'), // http://orionone.test:8888

'routes' => [
 [
 'match' => ['prefixes' => ['api/*']], // Apenas rotas /api/*
 ],
],

'type' => 'laravel', // Blade view com possibilidade de autenticação

'try_it_out' => [
 'enabled' => true, // Testar endpoints diretamente no browser!
],

'auth' => [
 'enabled' => false, // Mudar para true quando API Sanctum estiver pronta
 'in' => 'bearer', // Bearer token
],
```

**c) Adicionar annotations Scribe nos Controllers:**

Scribe usa **PHP DocBlock simples** (não precisa @OA\ ou bibliotecas extras):

```php
// app/Http/Controllers/Api/TicketController.php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\TicketResource;
use App\Models\Ticket;

/**
 * @group Tickets
 *
 * APIs para gerenciar tickets de suporte (CRUD completo).
 */
class TicketController extends Controller
{
 /**
 * List all tickets
 *
 * Retorna lista paginada de tickets com filtros opcionais.
 *
 * @queryParam status string Filter by status. Example: open
 * @queryParam priority string Filter by priority. Example: high
 * @queryParam sort string Sort field (prefix with - for desc). Example: -created_at
 *
 * @response 200 {
 * "data": [
 * {
 * "id": 1,
 * "ticket_number": "TK-20241110-0001",
 * "title": "Laptop não liga",
 * "status": "open",
 * "priority": "high"
 * }
 * ],
 * "links": {"first": "...", "last": "...", "next": null},
 * "meta": {"current_page": 1, "total": 15}
 * }
 */
 public function index(Request $request)
 {
 // ...
 }

 /**
 * Create a new ticket
 *
 * Cria um novo ticket de suporte.
 *
 * @bodyParam title string required The ticket title. Example: Laptop issue
 * @bodyParam description string required Detailed description.
 * @bodyParam priority string Priority level. Example: high
 * @bodyParam category_id int optional Category ID. Example: 1
 *
 * @response 201 {
 * "data": {
 * "id": 1,
 * "ticket_number": "TK-20241110-0001",
 * "title": "Laptop issue",
 * "status": "open"
 * }
 * }
 *
 * @response 422 {
 * "message": "Validation failed",
 * "errors": {"title": ["The title field is required."]}
 * }
 */
 public function store(StoreTicketRequest $request)
 {
 // ...
 }
}
```

/\*\*

-   @OA\Get(
-   path="/api/tickets",
-   summary="List all tickets",
-   description="Retrieve paginated list of tickets with optional filters",
-   operationId="getTickets",
-   tags={"Tickets"},
-   security={{"sanctum":{}}},
-   @OA\Parameter(
-   name="filter[status]",
-   in="query",
-   description="Filter by status",
-   required=false,
-   @OA\Schema(type="string", enum={"open","in_progress","resolved","closed"})
-   ),
-   @OA\Parameter(
-   name="filter[priority]",
-   in="query",
-   description="Filter by priority",
-   required=false,
-   @OA\Schema(type="string", enum={"low","medium","high","urgent"})
-   ),
-   @OA\Parameter(
-   name="sort",
-   in="query",
-   description="Sort by field (use - for descending)",
-   required=false,
-   @OA\Schema(type="string", example="-created_at")
-   ),
-   @OA\Response(
-   response=200,
-   description="Successful operation",
-   @OA\JsonContent(
-   type="object",
-   @OA\Property(property="data", type="array", @OA\Items(ref="#/components/schemas/Ticket")),
-   @OA\Property(property="links", type="object"),
-   @OA\Property(property="meta", type="object")
-   )
-   ),
-   @OA\Response(response=401, description="Unauthenticated")
-   )
    \*/
    public function index(Request $request)
    {
    // ...
    }

/\*\*

-   @OA\Post(
-   path="/api/tickets",
-   summary="Create a new ticket",
-   description="Create a new support ticket",
-   operationId="createTicket",
-   tags={"Tickets"},
-   security={{"sanctum":{}}},
-   @OA\RequestBody(
-   required=true,
-   @OA\JsonContent(
-   required={"title","description"},
-   @OA\Property(property="title", type="string", maxLength=255, example="Laptop não liga"),
-   @OA\Property(property="description", type="string", example="Detalhes do problema..."),
-   @OA\Property(property="priority", type="string", enum={"low","medium","high","urgent"}, example="high"),
-   @OA\Property(property="category_id", type="integer", example=1)
-   )
-   ),
-   @OA\Response(
-   response=201,
-   description="Ticket created successfully",
-   @OA\JsonContent(ref="#/components/schemas/Ticket")
-   ),
-   @OA\Response(response=422, description="Validation error")
-   )
    \*/
    public function store(Request $request)
    {
    // ...
    }

````

**Definir schema de Ticket (adicionar no topo de `Ticket` model):**

```php
/**
 * @OA\Schema(
 * schema="Ticket",
 * type="object",
 * title="Ticket",
 * description="Ticket model",
 * @OA\Property(property="id", type="integer", example=1),
 * @OA\Property(property="title", type="string", example="Problema com impressora"),
 * @OA\Property(property="description", type="string"),
 * @OA\Property(property="status", type="string", enum={"open","in_progress","resolved","closed"}),
 * @OA\Property(property="priority", type="string", enum={"low","medium","high","urgent"}),
 * @OA\Property(property="requester_id", type="integer"),
 * @OA\Property(property="assigned_to", type="integer", nullable=true),
 * @OA\Property(property="created_at", type="string", format="date-time"),
 * @OA\Property(property="updated_at", type="string", format="date-time")
 * )
 */
class Ticket extends Model
{
 // ...
}
````

#### Phase 3: Generate & Test Documentation

**a) Gerar documentação Scribe:**

```bash
# Gerar documentação HTML + OpenAPI spec
docker-compose exec orionone-app php artisan scribe:generate
```

**b) Aceder à documentação:**

Abrir browser: `http://localhost:8888/docs`

Documentação inclui:

-   HTML interativo com Try It Out
-   OpenAPI 3.0 spec: `http://localhost:8888/docs.openapi`
-   Postman collection: `http://localhost:8888/docs.postman`

**c) Testar endpoints com Try It Out:**

1. Clicar em qualquer endpoint (ex: POST `/api/tickets`)
2. Clicar botão "Try It Out"
3. Preencher parâmetros no formulário
4. Clicar "Execute"
5. Ver resposta JSON em tempo real

**d) Autenticação Sanctum (quando estiver pronta):**

1. Mudar `'auth' => ['enabled' => true]` em `config/scribe.php`
2. Clicar "Authorize" → Inserir Bearer token
3. Token será incluído automaticamente em todos os requests

#### Checklist Feature 5 (Scribe API Documentation)

-   [ ] Scribe instalado e verificado (knuckleswtf/scribe 5.5)
-   [ ] Configuração verificada em `config/scribe.php`
-   [ ] Annotations PHP DocBlock adicionadas em TicketController
-   [ ] Documentação gerada: `php artisan scribe:generate`
-   [ ] Rota `/docs` acessível e documentação HTML renderizada
-   [ ] OpenAPI spec disponível em `/docs.openapi`
-   [ ] Try It Out testado com sucesso nos endpoints
-   [ ] Postman collection exportada de `/docs.postman`
-   [ ] Autenticação configurada quando Sanctum estiver pronto
-   [ ] Documentação gerada com sucesso
-   [ ] Route `/api/documentation` acessível
-   [ ] Endpoints testados via Scribe Try It Out (http://localhost:8888/docs)
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

### Rich Text & Notifications Setup (5h - 1-2 Dez)

**Objetivo:** Documentar Vue Quill rich text editor e Laravel Notifications antes de implementar Comments.

**Contexto:**

-   Vue Quill (`@vueup/vue-quill: ^1.2.0`) **JÁ INSTALADO**
-   Marked (`marked: ^17.0.0`) + DOMPurify (`dompurify: ^3.3.0`) **JÁ INSTALADOS**
-   Laravel Notifications (built-in) - apenas falta documentar

---

#### 1. Vue Quill - Rich Text Editor (1h)

**Setup Global Quill (`resources/js/app.js`):**

```javascript
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css"; // Theme Snow (toolbar visível)

// Registar globalmente
app.component("QuillEditor", QuillEditor);
```

**Criar RichTextEditor Component:**

```vue
<!-- resources/js/components/ui/RichTextEditor.vue -->
<script setup>
import { ref, watch } from "vue";
import { QuillEditor } from "@vueup/vue-quill";

const props = defineProps({
    modelValue: String,
    placeholder: { type: String, default: "Escrever comentário..." },
    minHeight: { type: String, default: "150px" },
});

const emit = defineEmits(["update:modelValue"]);

const content = ref(props.modelValue);

watch(content, (value) => {
    emit("update:modelValue", value);
});

// Toolbar customizada (remover opções desnecessárias)
const toolbar = [
    [{ header: [1, 2, 3, false] }],
    ["bold", "italic", "underline", "strike"],
    [{ list: "ordered" }, { list: "bullet" }],
    ["link", "image", "code-block"],
    ["clean"], // Remove formatting
];
</script>

<template>
    <div class="quill-container">
        <QuillEditor
            v-model:content="content"
            :placeholder="placeholder"
            :toolbar="toolbar"
            theme="snow"
            content-type="html"
            :style="{ minHeight }"
        />
    </div>
</template>

<style>
.quill-container {
    @apply border rounded-md;
}

.ql-toolbar {
    @apply border-b bg-gray-50 rounded-t-md;
}

.ql-container {
    @apply rounded-b-md;
}

.ql-editor {
    @apply min-h-[150px] p-4;
}

/* Dark mode support */
.dark .ql-toolbar {
    @apply bg-gray-800 border-gray-700;
}

.dark .ql-container {
    @apply bg-gray-900 border-gray-700;
}

.dark .ql-editor {
    @apply text-gray-200;
}
</style>
```

**Usar no Comment Form:**

```vue
<script setup>
import RichTextEditor from "@/components/ui/RichTextEditor.vue";
import { useForm } from "@inertiajs/vue3";

const form = useForm({
    body: "",
    is_internal: false,
});

const submit = () => {
    form.post(route("tickets.comments.store", ticket.id), {
        onSuccess: () => {
            form.reset();
            toast.success("Comentário adicionado!");
        },
    });
};
</script>

<template>
    <form @submit.prevent="submit" class="space-y-4">
        <RichTextEditor
            v-model="form.body"
            placeholder="Adicionar comentário..."
            :min-height="'200px'"
        />

        <div class="flex items-center gap-4">
            <label class="flex items-center gap-2">
                <input type="checkbox" v-model="form.is_internal" />
                <span class="text-sm">Comentário interno (só agents)</span>
            </label>

            <Button type="submit" :disabled="form.processing">
                Adicionar Comentário
            </Button>
        </div>
    </form>
</template>
```

**Backend - Sanitize HTML:**

```php
use Illuminate\Support\Str;

// No CreateCommentAction
public function handle(CommentData $data, Ticket $ticket, User $user): Comment
{
 // Sanitize HTML (prevenir XSS)
 $cleanBody = Str::of($data->body)
 ->stripTags('<p><br><strong><em><u><ol><ul><li><a><h1><h2><h3><code><pre>')
 ->trim();

 return Comment::create([
 'ticket_id' => $ticket->id,
 'user_id' => $user->id,
 'body' => $cleanBody,
 'is_internal' => $data->is_internal,
 ]);
}
```

---

#### 2. Marked + DOMPurify - Markdown Parser (0.5h)

**Contexto:** KB Articles (Sprint 4) podem usar Markdown como alternativa ao Quill.

**Criar MarkdownRenderer Component:**

```vue
<!-- resources/js/components/ui/MarkdownRenderer.vue -->
<script setup>
import { computed } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

const props = defineProps({
    content: String,
});

// Configure marked (GitHub Flavored Markdown)
marked.setOptions({
    gfm: true,
    breaks: true,
});

const html = computed(() => {
    if (!props.content) return "";

    // Parse Markdown → HTML
    const rawHtml = marked.parse(props.content);

    // Sanitize (XSS prevention)
    return DOMPurify.sanitize(rawHtml, {
        ALLOWED_TAGS: [
            "p",
            "br",
            "strong",
            "em",
            "u",
            "h1",
            "h2",
            "h3",
            "ul",
            "ol",
            "li",
            "a",
            "code",
            "pre",
            "blockquote",
        ],
        ALLOWED_ATTR: ["href", "title"],
    });
});
</script>

<template>
    <div class="prose dark:prose-invert max-w-none" v-html="html" />
</template>

<style>
/* Tailwind Typography plugin já instalado (@tailwindcss/typography) */
.prose {
    @apply text-gray-900;
}

.prose a {
    @apply text-blue-600 hover:underline;
}

.prose code {
    @apply bg-gray-100 px-1 py-0.5 rounded text-sm;
}

.prose pre {
    @apply bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto;
}
</style>
```

**Usar para renderizar KB Articles:**

```vue
<script setup>
import MarkdownRenderer from "@/components/ui/MarkdownRenderer.vue";

const article = defineProps({
    article: Object, // KB Article com campo 'content' em Markdown
});
</script>

<template>
    <div class="max-w-4xl mx-auto p-6">
        <h1 class="text-3xl font-bold mb-4">{{ article.title }}</h1>

        <!-- Render Markdown content -->
        <MarkdownRenderer :content="article.content" />
    </div>
</template>
```

---

#### 3. Laravel Notifications Multi-Channel (1.5h)

**Criar Notification: CommentAddedNotification**

```bash
docker-compose exec orionone-app php artisan make:notification CommentAddedNotification
```

**Ficheiro:** `app/Notifications/CommentAddedNotification.php`

```php
<?php

namespace App\Notifications;

use App\Models\Comment;
use App\Models\Ticket;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

class CommentAddedNotification extends Notification implements ShouldQueue
{
 use Queueable;

 public function __construct(
 public Comment $comment,
 public Ticket $ticket,
 ) {}

 /**
 * Canais de notificação
 */
 public function via(object $notifiable): array
 {
 // Multi-channel: Email + Database (bell icon)
 return ['mail', 'database'];
 }

 /**
 * Email notification
 */
 public function toMail(object $notifiable): MailMessage
 {
 return (new MailMessage)
 ->subject("Novo comentário no ticket #{$this->ticket->ticket_number}")
 ->greeting("Olá {$notifiable->name}!")
 ->line("Foi adicionado um novo comentário ao ticket **{$this->ticket->title}**.")
 ->line("**Comentário:**")
 ->line(strip_tags($this->comment->body)) // Remove HTML do email
 ->action('Ver Ticket', url("/tickets/{$this->ticket->id}"))
 ->line('Obrigado por usar o OrionOne!');
 }

 /**
 * Database notification (bell icon)
 */
 public function toDatabase(object $notifiable): array
 {
 return [
 'ticket_id' => $this->ticket->id,
 'ticket_number' => $this->ticket->ticket_number,
 'comment_id' => $this->comment->id,
 'commenter_name' => $this->comment->user->name,
 'message' => "Novo comentário no ticket #{$this->ticket->ticket_number}",
 ];
 }
}
```

**Disparar Notification no CreateCommentAction:**

```php
use App\Notifications\CommentAddedNotification;

public function handle(CommentData $data, Ticket $ticket, User $user): Comment
{
 $comment = Comment::create([
 'ticket_id' => $ticket->id,
 'user_id' => $user->id,
 'body' => $data->body,
 'is_internal' => $data->is_internal,
 ]);

 // Notificar assigned agent (se existir)
 if ($ticket->assignee && $ticket->assignee->id !== $user->id) {
 $ticket->assignee->notify(new CommentAddedNotification($comment, $ticket));
 }

 // Notificar requester (se não for ele que comentou)
 if ($ticket->requester->id !== $user->id) {
 $ticket->requester->notify(new CommentAddedNotification($comment, $ticket));
 }

 return $comment;
}
```

**Database Notifications - Bell Icon Counter:**

```vue
<!-- resources/js/Layouts/AuthenticatedLayout.vue -->
<script setup>
import { computed } from "vue";
import { usePage } from "@inertiajs/vue3";
import { Bell } from "lucide-vue-next";

const page = usePage();

const unreadCount = computed(
    () => page.props.auth?.user?.unread_notifications_count || 0
);
</script>

<template>
    <nav class="border-b bg-white">
        <div class="flex items-center justify-between px-6 py-4">
            <!-- ... logo ... -->

            <div class="flex items-center gap-4">
                <!-- Notifications Bell -->
                <Link :href="route('notifications.index')" class="relative">
                    <Bell class="w-5 h-5" />

                    <!-- Badge (unread count) -->
                    <span
                        v-if="unreadCount > 0"
                        class="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
                    >
                        {{ unreadCount > 9 ? "9+" : unreadCount }}
                    </span>
                </Link>

                <!-- ... user menu ... -->
            </div>
        </div>
    </nav>
</template>
```

**Share unread count no Inertia (Middleware):**

```php
// app/Http/Middleware/HandleInertiaRequests.php
public function share(Request $request): array
{
 return [
 ...parent::share($request),
 'auth' => [
 'user' => $request->user() ? [
 'id' => $request->user()->id,
 'name' => $request->user()->name,
 'email' => $request->user()->email,
 'avatar' => $request->user()->avatar,
 'unread_notifications_count' => $request->user()->unreadNotifications()->count(),
 ] : null,
 ],
 ];
}
```

**Mark notification as read:**

```php
// routes/web.php
Route::post('/notifications/{notification}/read', function (DatabaseNotification $notification) {
 $notification->markAsRead();
 return back();
})->name('notifications.read');
```

**Email Configuration (local testing com Mailpit):**

```env
# .env (já configurado em SETUP.md)
MAIL_MAILER=smtp
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="no-reply@orionone.test"
MAIL_FROM_NAME="OrionOne"
```

**Testar emails localmente:**

```bash
# Abrir Mailpit (já rodando via docker-compose)
# URL: http://localhost:8025

# Disparar notificação em Tinker
docker-compose exec orionone-app php artisan tinker
>>> $user = User::first();
>>> $ticket = Ticket::first();
>>> $comment = Comment::first();
>>> $user->notify(new \App\Notifications\CommentAddedNotification($comment, $ticket));
>>> exit

# Ver email em http://localhost:8025 (Mailpit)
```

#### Checklist Rich Text & Notifications

-   [ ] Vue Quill configurado globalmente
-   [ ] RichTextEditor component criado com toolbar customizada
-   [ ] Backend sanitiza HTML (strip_tags com whitelist)
-   [ ] MarkdownRenderer component criado (Marked + DOMPurify)
-   [ ] Tailwind Typography plugin configurado (@tailwindcss/typography)
-   [ ] CommentAddedNotification criada (email + database channels)
-   [ ] Notification disparada no CreateCommentAction
-   [ ] Bell icon com badge de unread count no header
-   [ ] Middleware share unread_notifications_count
-   [ ] Route para mark notification as read
-   [ ] Testado: Email aparece no Mailpit (http://localhost:8025)
-   [ ] Testado: Database notification cria registo
-   [ ] Testado: Bell icon mostra contador correto
-   [ ] Documentado em `docs/NOTIFICATIONS-GUIDE.md`

**Tempo estimado:** ~5h (Quill 1h + Marked 0.5h + Notifications backend 1.5h + Frontend 1h + Testing 1h)

---

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

### Charts & Data Visualization Setup (2h - 29 Dez)

**Objetivo:** Documentar Chart.js integration para Dashboard analytics.

**Contexto:**

-   Chart.js (`chart.js: ^4.5.1`) + vue-chartjs (`^5.3.3`) **JÁ INSTALADOS!**
-   ⏳ Apenas falta documentar uso e criar wrapper components

---

#### 1. Chart.js Setup (30 min)

**Registar Chart.js components (`resources/js/app.js`):**

```javascript
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from "chart.js";

// Registar components necessários (tree-shaking)
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

// Configuração global
ChartJS.defaults.responsive = true;
ChartJS.defaults.maintainAspectRatio = false;
ChartJS.defaults.color = "#6b7280"; // text-gray-500
ChartJS.defaults.font.family = "'Inter', sans-serif";
```

---

#### 2. Create Chart Components (1h)

**2.1 LineChart - Tickets Trend:**

```vue
<!-- resources/js/components/charts/LineChart.vue -->
<script setup>
import { Line } from "vue-chartjs";
import { computed } from "vue";

const props = defineProps({
    data: Object, // { labels: [], datasets: [] }
    title: String,
    height: { type: Number, default: 300 },
});

const options = computed(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: !!props.title,
            text: props.title,
            font: { size: 16, weight: "bold" },
        },
        legend: {
            display: true,
            position: "bottom",
        },
        tooltip: {
            mode: "index",
            intersect: false,
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                precision: 0, // Inteiros apenas
            },
        },
    },
}));
</script>

<template>
    <div :style="{ height: `${height}px` }">
        <Line :data="data" :options="options" />
    </div>
</template>
```

**Usar no Dashboard:**

```vue
<script setup>
import LineChart from "@/components/charts/LineChart.vue";

const props = defineProps({
    ticketsTrend: Object, // Backend retorna: { labels: ['1 Nov', '2 Nov'], datasets: [{ data: [10, 15] }] }
});

// Transform backend data to Chart.js format
const chartData = {
    labels: props.ticketsTrend.labels,
    datasets: [
        {
            label: "Tickets Criados",
            data: props.ticketsTrend.data,
            borderColor: "rgb(59, 130, 246)", // blue-500
            backgroundColor: "rgba(59, 130, 246, 0.1)",
            fill: true,
            tension: 0.3, // Smooth curve
        },
    ],
};
</script>

<template>
    <Card>
        <CardHeader>
            <CardTitle>Tickets Criados (Últimos 30 Dias)</CardTitle>
        </CardHeader>
        <CardContent>
            <LineChart
                :data="chartData"
                title="Tendência de Tickets"
                :height="300"
            />
        </CardContent>
    </Card>
</template>
```

**Backend - Generate Trend Data:**

```php
// app/Http/Controllers/DashboardController.php
public function index()
{
 // Tickets criados por dia (últimos 30 dias)
 $ticketsTrend = Ticket::whereBetween('created_at', [now()->subDays(30), now()])
 ->groupBy(DB::raw('DATE(created_at)'))
 ->selectRaw('DATE(created_at) as date, count(*) as total')
 ->orderBy('date')
 ->get();

 // Format para Chart.js
 $chartData = [
 'labels' => $ticketsTrend->pluck('date')->map(fn($date) => Carbon::parse($date)->format('d M')),
 'data' => $ticketsTrend->pluck('total'),
 ];

 return Inertia::render('Dashboard', [
 'ticketsTrend' => $chartData,
 ]);
}
```

---

**2.2 PieChart - Tickets por Status:**

```vue
<!-- resources/js/components/charts/PieChart.vue -->
<script setup>
import { Pie } from "vue-chartjs";
import { computed } from "vue";

const props = defineProps({
    data: Object,
    title: String,
    height: { type: Number, default: 300 },
});

const options = computed(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: !!props.title,
            text: props.title,
            font: { size: 16, weight: "bold" },
        },
        legend: {
            position: "right",
        },
    },
}));
</script>

<template>
    <div :style="{ height: `${height}px` }">
        <Pie :data="data" :options="options" />
    </div>
</template>
```

**Usar no Dashboard:**

```vue
<script setup>
const statusData = {
    labels: ["Aberto", "Em Progresso", "Resolvido", "Fechado"],
    datasets: [
        {
            data: [45, 32, 78, 123], // Backend retorna contadores
            backgroundColor: [
                "rgb(59, 130, 246)", // blue - open
                "rgb(234, 179, 8)", // yellow - in_progress
                "rgb(34, 197, 94)", // green - resolved
                "rgb(156, 163, 175)", // gray - closed
            ],
        },
    ],
};
</script>

<template>
    <Card>
        <CardHeader>
            <CardTitle>Tickets por Status</CardTitle>
        </CardHeader>
        <CardContent>
            <PieChart :data="statusData" :height="300" />
        </CardContent>
    </Card>
</template>
```

---

**2.3 BarChart - Agent Performance:**

```vue
<!-- resources/js/components/charts/BarChart.vue -->
<script setup>
import { Bar } from "vue-chartjs";
import { computed } from "vue";

const props = defineProps({
    data: Object,
    title: String,
    height: { type: Number, default: 300 },
});

const options = computed(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: !!props.title,
            text: props.title,
            font: { size: 16, weight: "bold" },
        },
        legend: {
            display: false,
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                precision: 0,
            },
        },
    },
}));
</script>

<template>
    <div :style="{ height: `${height}px` }">
        <Bar :data="data" :options="options" />
    </div>
</template>
```

**Backend - Agent Performance Data:**

```php
// Dashboard controller
$agentPerformance = User::role('agent')
 ->withCount([
 'assignedTickets as total_tickets',
 'assignedTickets as resolved_tickets' => fn($q) => $q->where('status', 'resolved'),
 ])
 ->orderBy('resolved_tickets', 'desc')
 ->limit(10)
 ->get();

$performanceData = [
 'labels' => $agentPerformance->pluck('name'),
 'data' => $agentPerformance->pluck('resolved_tickets'),
];

return Inertia::render('Dashboard', [
 'agentPerformance' => $performanceData,
]);
```

---

#### 3. Advanced Features (30 min)

**3.1 Export Chart as PNG:**

```vue
<script setup>
import { ref } from "vue";
import Button from "@/components/ui/Button.vue";

const chartRef = ref(null);

const exportChart = () => {
    const chart = chartRef.value?.chart; // Aceder ao ChartJS instance
    if (!chart) return;

    // Gerar PNG base64
    const url = chart.toBase64Image();

    // Download
    const link = document.createElement("a");
    link.download = "tickets-trend.png";
    link.href = url;
    link.click();
};
</script>

<template>
    <div>
        <LineChart ref="chartRef" :data="data" />

        <Button @click="exportChart" variant="outline" class="mt-4">
            Exportar PNG
        </Button>
    </div>
</template>
```

**3.2 Real-time Chart Updates:**

```vue
<script setup>
import { ref, onMounted } from "vue";
import { router } from "@inertiajs/vue3";

const chartData = ref(props.ticketsTrend);

// Poll backend a cada 30 segundos
onMounted(() => {
    setInterval(() => {
        router.reload({
            only: ["ticketsTrend"],
            onSuccess: (page) => {
                chartData.value = page.props.ticketsTrend;
            },
        });
    }, 30000); // 30 seconds
});
</script>

<template>
    <LineChart :data="chartData" />
</template>
```

**3.3 Dark Mode Support:**

```javascript
// Auto-detect dark mode e ajustar cores
import { useDark } from "@vueuse/core";

const isDark = useDark();

const chartColors = computed(() => ({
    borderColor: isDark.value ? "rgb(147, 197, 253)" : "rgb(59, 130, 246)",
    backgroundColor: isDark.value
        ? "rgba(147, 197, 253, 0.1)"
        : "rgba(59, 130, 246, 0.1)",
    gridColor: isDark.value ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)",
}));
```

---

#### Checklist Chart.js Integration

-   [ ] Chart.js components registados globalmente (tree-shaking)
-   [ ] LineChart component criado (tickets trend)
-   [ ] PieChart component criado (tickets por status)
-   [ ] BarChart component criado (agent performance)
-   [ ] DoughnutChart component criado (tickets por prioridade)
-   [ ] Backend gera dados no formato Chart.js (labels + datasets)
-   [ ] Export PNG funcional (toBase64Image)
-   [ ] Real-time updates (polling a cada 30s)
-   [ ] Dark mode support (cores adaptativas)
-   [ ] Responsive (funciona em mobile)
-   [ ] Testado: Charts renderizam corretamente
-   [ ] Testado: Tooltips mostram dados corretos
-   [ ] Testado: Legend funcional (hide/show datasets)
-   [ ] Documentado em `docs/CHARTS-GUIDE.md`

**Tempo estimado:** ~2h (Setup 30min + Components 1h + Advanced 30min)

**Referência:** [Chart.js Docs](https://www.chartjs.org/docs/latest/) | [Vue-ChartJS Docs](https://vue-chartjs.org/)

---

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

### Feature 12: API Documentation (Scribe) - Final Review

#### Completar Documentação de Todas as APIs

**a) Documentar Comments API:**

```php
// app/Http/Controllers/Api/CommentController.php

/**
 * @group Comments
 *
 * Gerenciar comentários em tickets.
 */
class CommentController extends Controller
{
 /**
 * List comments for a ticket
 *
 * @urlParam ticket_id int required Ticket ID. Example: 1
 *
 * @response 200 {
 * "data": [
 * {"id": 1, "body": "Comentário exemplo", "user": {"name": "João"}}
 * ]
 * }
 */
 public function index(Ticket $ticket) { }

 /**
 * Add comment to ticket
 *
 * @urlParam ticket_id int required Ticket ID. Example: 1
 * @bodyParam body string required Comment text. Example: Problema resolvido
 *
 * @response 201 {"data": {"id": 2, "body": "Problema resolvido"}}
 */
 public function store(Request $request, Ticket $ticket) { }
}
```

**b) Documentar Knowledge Base API:**

```php
// app/Http/Controllers/Api/KnowledgeBaseController.php

/**
 * @group Knowledge Base
 *
 * Artigos da base de conhecimento.
 */
class KnowledgeBaseController extends Controller
{
 /**
 * Search knowledge base articles
 *
 * @queryParam q string Search query. Example: reset password
 * @queryParam category_id int Filter by category. Example: 2
 *
 * @response 200 {
 * "data": [
 * {"id": 1, "title": "Como resetar senha", "slug": "como-resetar-senha"}
 * ]
 * }
 */
 public function search(Request $request) { }
}
```

**c) Ativar autenticação Sanctum:**

```php
// config/scribe.php
'auth' => [
 'enabled' => true, // Ativar autenticação
 'in' => 'bearer',
 'name' => 'Authorization',
 'placeholder' => 'YOUR_SANCTUM_TOKEN_HERE',
 'extra_info' => 'Obtenha seu token via POST /api/login com email e password.',
],
```

**d) Regenerar documentação final:**

```bash
# Gerar documentação com todas as APIs documentadas
docker-compose exec orionone-app php artisan scribe:generate

# Verificar:
# - /docs → HTML completo
# - /docs.openapi → OpenAPI 3.0 spec
# - /docs.postman → Postman collection
```

**e) Adicionar exemplo de autenticação:**

```bash
# Criar token Sanctum para testes
docker-compose exec orionone-app php artisan tinker
>>> $user = User::first();
>>> $token = $user->createToken('api-docs-test')->plainTextToken;
>>> echo $token; // Copiar token para testar no /docs
```

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

-   [ ] API Documentation (Scribe) completa
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

## Sprint 7: Asset Management (CMDB) (27 Jan - 23 Fev)

### Feature 13: Assets CRUD (6 Asset Types)

#### Phase 1: Planning (30 min)

**User Story:** Como administrador, quero gerir assets (laptops, servers, licenças) para rastrear inventário e relacionar com tickets.

**Asset Types:**

-   Laptop, Desktop, Server, Software License, Mobile Device, Network Equipment

**Asset Fields:**

-   `name`, `serial_number`, `model`, `manufacturer`, `purchase_date`, `warranty_end`, `cost`
-   `status`: In Use, Available, Under Repair, Retired, Lost/Stolen
-   `assigned_to` (user_id), `location` (office, remote, storage)

**Acceptance Criteria:**

-   Admin pode criar/editar/deletar assets
-   Assets listados com filtros (type, status, assigned_to)
-   Asset show page exibe histórico completo (Spatie Activity Log)
-   CSV import para bulk create

---

#### Phase 2: Tests First (RED)

**a) Create AssetTest.php:**

```php
<?php

namespace Tests\Feature;

use App\Models\Asset;
use App\Models\User;
use Tests\TestCase;

class AssetTest extends TestCase
{
 /** @test */
 public function admin_can_create_asset()
 {
 $admin = User::factory()->admin()->create();

 $this->actingAs($admin)
 ->post('/api/v1/assets', [
 'name' => 'Dell Latitude 5520',
 'serial_number' => 'SN123456',
 'asset_type' => 'laptop',
 'model' => 'Latitude 5520',
 'manufacturer' => 'Dell',
 'status' => 'available',
 'purchase_date' => '2024-01-15',
 'warranty_end' => '2027-01-15',
 'cost' => 1200.00,
 ])
 ->assertCreated()
 ->assertJsonStructure(['data' => ['id', 'name', 'serial_number']]);

 $this->assertDatabaseHas('assets', ['serial_number' => 'SN123456']);
 }

 /** @test */
 public function serial_number_must_be_unique()
 {
 Asset::factory()->create(['serial_number' => 'SN123456']);

 $admin = User::factory()->admin()->create();

 $this->actingAs($admin)
 ->post('/api/v1/assets', [
 'name' => 'Another Laptop',
 'serial_number' => 'SN123456', // Duplicate
 'asset_type' => 'laptop',
 ])
 ->assertStatus(422)
 ->assertJsonValidationErrors('serial_number');
 }

 /** @test */
 public function asset_can_be_assigned_to_user()
 {
 $asset = Asset::factory()->create(['status' => 'available']);
 $user = User::factory()->create();
 $admin = User::factory()->admin()->create();

 $this->actingAs($admin)
 ->patch("/api/v1/assets/{$asset->id}", [
 'assigned_to' => $user->id,
 'status' => 'in_use',
 ])
 ->assertOk();

 $this->assertEquals($user->id, $asset->fresh()->assigned_to);
 }

 /** @test */
 public function asset_shows_history_timeline()
 {
 $asset = Asset::factory()->create();
 activity()->performedOn($asset)->log('Asset created');

 $admin = User::factory()->admin()->create();

 $response = $this->actingAs($admin)
 ->get("/api/v1/assets/{$asset->id}")
 ->assertOk();

 $this->assertArrayHasKey('history', $response->json('data'));
 }
}
```

**b) Create AssetFactory.php:**

```php
<?php

namespace Database\Factories;

use App\Models\Asset;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class AssetFactory extends Factory
{
 protected $model = Asset::class;

 public function definition(): array
 {
 return [
 'name' => $this->faker->words(3, true),
 'serial_number' => strtoupper($this->faker->unique()->bothify('SN######')),
 'asset_type' => $this->faker->randomElement(['laptop', 'desktop', 'server', 'software_license', 'mobile_device', 'network_equipment']),
 'model' => $this->faker->words(2, true),
 'manufacturer' => $this->faker->randomElement(['Dell', 'HP', 'Lenovo', 'Apple', 'Cisco']),
 'status' => $this->faker->randomElement(['in_use', 'available', 'under_repair', 'retired', 'lost']),
 'purchase_date' => $this->faker->dateTimeBetween('-3 years', 'now'),
 'warranty_end' => $this->faker->dateTimeBetween('now', '+3 years'),
 'cost' => $this->faker->randomFloat(2, 500, 5000),
 'location' => $this->faker->randomElement(['office', 'remote', 'storage']),
 'assigned_to' => $this->faker->boolean(60) ? User::factory() : null,
 ];
 }

 public function laptop(): static
 {
 return $this->state(fn (array $attributes) => [
 'asset_type' => 'laptop',
 'manufacturer' => 'Dell',
 'model' => 'Latitude 5520',
 ]);
 }

 public function available(): static
 {
 return $this->state(fn (array $attributes) => [
 'status' => 'available',
 'assigned_to' => null,
 ]);
 }

 public function inUse(): static
 {
 return $this->state(fn (array $attributes) => [
 'status' => 'in_use',
 'assigned_to' => User::factory(),
 ]);
 }
}
```

**Run tests (should FAIL - RED):**

```bash
docker-compose exec orionone-app php artisan test --filter=AssetTest
```

---

#### Phase 3: Implementation (GREEN)

**a) Create Migration:**

```bash
docker-compose exec orionone-app php artisan make:migration create_assets_table
```

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
 public function up(): void
 {
 Schema::create('assets', function (Blueprint $table) {
 $table->id();
 $table->string('name');
 $table->string('serial_number')->unique();
 $table->enum('asset_type', ['laptop', 'desktop', 'server', 'software_license', 'mobile_device', 'network_equipment']);
 $table->string('model')->nullable();
 $table->string('manufacturer')->nullable();
 $table->enum('status', ['in_use', 'available', 'under_repair', 'retired', 'lost'])->default('available');
 $table->date('purchase_date')->nullable();
 $table->date('warranty_end')->nullable();
 $table->decimal('cost', 10, 2)->nullable();
 $table->string('location')->nullable(); // office, remote, storage
 $table->text('notes')->nullable();

 // Relationships
 $table->foreignId('assigned_to')->nullable()->constrained('users')->nullOnDelete();
 $table->foreignId('parent_id')->nullable()->constrained('assets')->nullOnDelete(); // For components (e.g., RAM → Laptop)

 $table->timestamps();
 $table->softDeletes();

 // Indexes
 $table->index('serial_number');
 $table->index('asset_type');
 $table->index('status');
 $table->index('assigned_to');
 });
 }

 public function down(): void
 {
 Schema::dropIfExists('assets');
 }
};
```

**Run migration:**

```bash
docker-compose exec orionone-app php artisan migrate
```

**b) Create Asset Model:**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;
use Spatie\Activitylog\LogOptions;
use Spatie\Activitylog\Traits\LogsActivity;

class Asset extends Model
{
 use HasFactory, SoftDeletes, LogsActivity;

 protected $fillable = [
 'name',
 'serial_number',
 'asset_type',
 'model',
 'manufacturer',
 'status',
 'purchase_date',
 'warranty_end',
 'cost',
 'location',
 'notes',
 'assigned_to',
 'parent_id',
 ];

 protected $casts = [
 'purchase_date' => 'date',
 'warranty_end' => 'date',
 'cost' => 'decimal:2',
 ];

 // Activity Log Configuration
 public function getActivitylogOptions(): LogOptions
 {
 return LogOptions::defaults()
 ->logOnly(['name', 'status', 'assigned_to', 'location'])
 ->logOnlyDirty()
 ->dontSubmitEmptyLogs();
 }

 // Relationships
 public function assignedUser(): BelongsTo
 {
 return $this->belongsTo(User::class, 'assigned_to');
 }

 public function tickets(): HasMany
 {
 return $this->hasMany(Ticket::class, 'affected_asset_id');
 }

 public function parent(): BelongsTo
 {
 return $this->belongsTo(Asset::class, 'parent_id');
 }

 public function components(): HasMany
 {
 return $this->hasMany(Asset::class, 'parent_id');
 }

 // Scopes
 public function scopeAvailable($query)
 {
 return $query->where('status', 'available');
 }

 public function scopeInUse($query)
 {
 return $query->where('status', 'in_use');
 }

 public function scopeWarrantyExpiring($query, int $days = 30)
 {
 return $query->where('warranty_end', '<=', now()->addDays($days))
 ->where('warranty_end', '>=', now());
 }
}
```

**c) Create AssetController:**

```bash
docker-compose exec orionone-app php artisan make:controller Api/AssetController --resource
```

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Asset;
use Illuminate\Http\Request;
use Spatie\QueryBuilder\QueryBuilder;

/**
 * @group Assets
 *
 * Gerenciar assets (CMDB).
 */
class AssetController extends Controller
{
 /**
 * List all assets
 *
 * @queryParam filter[asset_type] Filter by type. Example: laptop
 * @queryParam filter[status] Filter by status. Example: available
 * @queryParam filter[assigned_to] Filter by assigned user ID. Example: 5
 * @queryParam sort Sort by field. Example: -created_at
 *
 * @response 200 {
 * "data": [
 * {"id": 1, "name": "Dell Latitude 5520", "serial_number": "SN123456", "status": "in_use"}
 * ],
 * "meta": {"total": 45}
 * }
 */
 public function index(Request $request)
 {
 $assets = QueryBuilder::for(Asset::class)
 ->allowedFilters(['asset_type', 'status', 'assigned_to'])
 ->allowedSorts(['name', 'created_at', 'purchase_date'])
 ->with(['assignedUser:id,name,email'])
 ->paginate($request->per_page ?? 20);

 return response()->json($assets);
 }

 /**
 * Create new asset
 *
 * @bodyParam name string required Asset name. Example: Dell Latitude 5520
 * @bodyParam serial_number string required Unique serial number. Example: SN123456
 * @bodyParam asset_type string required Type. Example: laptop
 * @bodyParam status string Status. Example: available
 *
 * @response 201 {"data": {"id": 1, "name": "Dell Latitude 5520"}}
 */
 public function store(Request $request)
 {
 $validated = $request->validate([
 'name' => 'required|string|max:255',
 'serial_number' => 'required|string|unique:assets,serial_number|max:255',
 'asset_type' => 'required|in:laptop,desktop,server,software_license,mobile_device,network_equipment',
 'model' => 'nullable|string|max:255',
 'manufacturer' => 'nullable|string|max:255',
 'status' => 'required|in:in_use,available,under_repair,retired,lost',
 'purchase_date' => 'nullable|date',
 'warranty_end' => 'nullable|date|after:purchase_date',
 'cost' => 'nullable|numeric|min:0',
 'location' => 'nullable|string|max:255',
 'notes' => 'nullable|string',
 'assigned_to' => 'nullable|exists:users,id',
 'parent_id' => 'nullable|exists:assets,id',
 ]);

 $asset = Asset::create($validated);

 activity()
 ->performedOn($asset)
 ->causedBy(auth()->user())
 ->log('Asset created');

 return response()->json(['data' => $asset], 201);
 }

 /**
 * Show asset details
 *
 * @urlParam id int required Asset ID. Example: 1
 *
 * @response 200 {
 * "data": {
 * "id": 1,
 * "name": "Dell Latitude 5520",
 * "serial_number": "SN123456",
 * "assigned_user": {"id": 5, "name": "João Silva"},
 * "tickets": [{"id": 10, "title": "Teclado não funciona"}],
 * "history": [{"description": "Asset created", "created_at": "2024-11-10"}]
 * }
 * }
 */
 public function show(Asset $asset)
 {
 $asset->load([
 'assignedUser:id,name,email',
 'tickets:id,title,status,created_at',
 'components:id,name,asset_type',
 ]);

 // Get activity history
 $history = $asset->activities()
 ->with('causer:id,name')
 ->latest()
 ->get();

 return response()->json([
 'data' => array_merge($asset->toArray(), [
 'history' => $history,
 ]),
 ]);
 }

 /**
 * Update asset
 *
 * @urlParam id int required Asset ID. Example: 1
 * @bodyParam status string Status. Example: in_use
 * @bodyParam assigned_to int Assigned user ID. Example: 5
 *
 * @response 200 {"data": {"id": 1, "status": "in_use"}}
 */
 public function update(Request $request, Asset $asset)
 {
 $validated = $request->validate([
 'name' => 'sometimes|string|max:255',
 'serial_number' => "sometimes|string|unique:assets,serial_number,{$asset->id}|max:255",
 'asset_type' => 'sometimes|in:laptop,desktop,server,software_license,mobile_device,network_equipment',
 'model' => 'nullable|string|max:255',
 'manufacturer' => 'nullable|string|max:255',
 'status' => 'sometimes|in:in_use,available,under_repair,retired,lost',
 'purchase_date' => 'nullable|date',
 'warranty_end' => 'nullable|date',
 'cost' => 'nullable|numeric|min:0',
 'location' => 'nullable|string|max:255',
 'notes' => 'nullable|string',
 'assigned_to' => 'nullable|exists:users,id',
 'parent_id' => 'nullable|exists:assets,id',
 ]);

 $asset->update($validated);

 activity()
 ->performedOn($asset)
 ->causedBy(auth()->user())
 ->log('Asset updated');

 return response()->json(['data' => $asset->fresh()]);
 }

 /**
 * Delete asset
 *
 * @urlParam id int required Asset ID. Example: 1
 *
 * @response 204
 */
 public function destroy(Asset $asset)
 {
 $asset->delete();

 activity()
 ->performedOn($asset)
 ->causedBy(auth()->user())
 ->log('Asset deleted');

 return response()->noContent();
 }

 /**
 * Get warranty expiring soon
 *
 * @queryParam days int Days threshold. Example: 30
 *
 * @response 200 {
 * "data": [
 * {"id": 1, "name": "Dell Laptop", "warranty_end": "2024-12-10"}
 * ]
 * }
 */
 public function warrantyExpiring(Request $request)
 {
 $days = $request->query('days', 30);

 $assets = Asset::warrantyExpiring($days)
 ->with('assignedUser:id,name,email')
 ->get();

 return response()->json(['data' => $assets]);
 }
}
```

**d) Add Routes:**

```php
// routes/api.php

Route::middleware('auth:sanctum')->prefix('v1')->group(function () {
 // Assets
 Route::apiResource('assets', AssetController::class);
 Route::get('assets/warranty/expiring', [AssetController::class, 'warrantyExpiring']);
});
```

**Run tests again (should PASS - GREEN):**

```bash
docker-compose exec orionone-app php artisan test --filter=AssetTest
```

---

#### Phase 4: Frontend (Vue + Shadcn)

**a) Create Assets/Index.vue:**

```vue
<script setup lang="ts">
import { ref, computed } from "vue";
import { router } from "@inertiajs/vue3";
import AppLayout from "@/Layouts/AppLayout.vue";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/Components/ui/table";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/Components/ui/select";
import { Badge } from "@/Components/ui/badge";
import {
    Laptop,
    Server,
    Smartphone,
    HardDrive,
    Package,
} from "lucide-vue-next";

interface Asset {
    id: number;
    name: string;
    serial_number: string;
    asset_type: string;
    status: string;
    assigned_user?: { name: string; email: string };
    warranty_end: string;
}

interface Props {
    assets: {
        data: Asset[];
        meta: { total: number; current_page: number };
    };
}

const props = defineProps<Props>();

const filters = ref({
    asset_type: "",
    status: "",
    search: "",
});

const assetTypeIcons = {
    laptop: Laptop,
    desktop: Laptop,
    server: Server,
    mobile_device: Smartphone,
    network_equipment: HardDrive,
    software_license: Package,
};

const statusColors = {
    in_use: "default",
    available: "success",
    under_repair: "warning",
    retired: "secondary",
    lost: "destructive",
};

function applyFilters() {
    router.get(
        "/assets",
        { ...filters.value },
        { preserveState: true, preserveScroll: true }
    );
}

function clearFilters() {
    filters.value = { asset_type: "", status: "", search: "" };
    applyFilters();
}
</script>

<template>
    <AppLayout title="Assets">
        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                    <div class="p-6">
                        <!-- Header -->
                        <div class="flex justify-between items-center mb-6">
                            <div>
                                <h2
                                    class="text-2xl font-semibold text-gray-900"
                                >
                                    Assets ({{ assets.meta.total }})
                                </h2>
                                <p class="text-sm text-gray-600 mt-1">
                                    Gerir inventário de assets
                                </p>
                            </div>
                            <Button @click="router.visit('/assets/create')">
                                + Novo Asset
                            </Button>
                        </div>

                        <!-- Filters -->
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <Input
                                v-model="filters.search"
                                placeholder="Pesquisar..."
                                @input="applyFilters"
                            />

                            <Select
                                v-model="filters.asset_type"
                                @update:modelValue="applyFilters"
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Tipo" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="">Todos</SelectItem>
                                    <SelectItem value="laptop"
                                        >Laptop</SelectItem
                                    >
                                    <SelectItem value="desktop"
                                        >Desktop</SelectItem
                                    >
                                    <SelectItem value="server"
                                        >Server</SelectItem
                                    >
                                    <SelectItem value="software_license"
                                        >Software License</SelectItem
                                    >
                                    <SelectItem value="mobile_device"
                                        >Mobile Device</SelectItem
                                    >
                                    <SelectItem value="network_equipment"
                                        >Network Equipment</SelectItem
                                    >
                                </SelectContent>
                            </Select>

                            <Select
                                v-model="filters.status"
                                @update:modelValue="applyFilters"
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Status" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="">Todos</SelectItem>
                                    <SelectItem value="in_use"
                                        >In Use</SelectItem
                                    >
                                    <SelectItem value="available"
                                        >Available</SelectItem
                                    >
                                    <SelectItem value="under_repair"
                                        >Under Repair</SelectItem
                                    >
                                    <SelectItem value="retired"
                                        >Retired</SelectItem
                                    >
                                    <SelectItem value="lost"
                                        >Lost/Stolen</SelectItem
                                    >
                                </SelectContent>
                            </Select>

                            <Button variant="outline" @click="clearFilters">
                                Limpar Filtros
                            </Button>
                        </div>

                        <!-- Table -->
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Asset</TableHead>
                                    <TableHead>Serial Number</TableHead>
                                    <TableHead>Type</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Assigned To</TableHead>
                                    <TableHead>Warranty</TableHead>
                                    <TableHead>Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow
                                    v-for="asset in assets.data"
                                    :key="asset.id"
                                >
                                    <TableCell>
                                        <div class="flex items-center gap-2">
                                            <component
                                                :is="
                                                    assetTypeIcons[
                                                        asset.asset_type
                                                    ]
                                                "
                                                class="h-4 w-4 text-gray-500"
                                            />
                                            <span class="font-medium">{{
                                                asset.name
                                            }}</span>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <code
                                            class="text-xs bg-gray-100 px-2 py-1 rounded"
                                        >
                                            {{ asset.serial_number }}
                                        </code>
                                    </TableCell>
                                    <TableCell>{{
                                        asset.asset_type
                                    }}</TableCell>
                                    <TableCell>
                                        <Badge
                                            :variant="
                                                statusColors[asset.status]
                                            "
                                        >
                                            {{ asset.status }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <span v-if="asset.assigned_user">
                                            {{ asset.assigned_user.name }}
                                        </span>
                                        <span v-else class="text-gray-400"
                                            >Unassigned</span
                                        >
                                    </TableCell>
                                    <TableCell>
                                        <span
                                            v-if="asset.warranty_end"
                                            :class="{
                                                'text-red-600':
                                                    new Date(
                                                        asset.warranty_end
                                                    ) < new Date(),
                                            }"
                                        >
                                            {{ asset.warranty_end }}
                                        </span>
                                        <span v-else class="text-gray-400"
                                            >N/A</span
                                        >
                                    </TableCell>
                                    <TableCell>
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            @click="
                                                router.visit(
                                                    `/assets/${asset.id}`
                                                )
                                            "
                                        >
                                            Ver
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
```

**b) Create Assets/Create.vue:**

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useForm } from "@inertiajs/vue3";
import AppLayout from "@/Layouts/AppLayout.vue";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Label } from "@/Components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/Components/ui/select";
import { Textarea } from "@/Components/ui/textarea";

interface Props {
    users: { id: number; name: string }[];
}

const props = defineProps<Props>();

const form = useForm({
    name: "",
    serial_number: "",
    asset_type: "laptop",
    model: "",
    manufacturer: "",
    status: "available",
    purchase_date: "",
    warranty_end: "",
    cost: "",
    location: "",
    notes: "",
    assigned_to: null,
});

function submit() {
    form.post("/api/v1/assets", {
        onSuccess: () => {
            // Redirect to assets list
            router.visit("/assets");
        },
    });
}
</script>

<template>
    <AppLayout title="Novo Asset">
        <div class="py-12">
            <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                    <div class="p-6">
                        <h2 class="text-2xl font-semibold mb-6">
                            Criar Novo Asset
                        </h2>

                        <form @submit.prevent="submit" class="space-y-6">
                            <!-- Name -->
                            <div>
                                <Label for="name">Nome *</Label>
                                <Input
                                    id="name"
                                    v-model="form.name"
                                    type="text"
                                    placeholder="Dell Latitude 5520"
                                    required
                                />
                                <span
                                    v-if="form.errors.name"
                                    class="text-sm text-red-600"
                                >
                                    {{ form.errors.name }}
                                </span>
                            </div>

                            <!-- Serial Number -->
                            <div>
                                <Label for="serial_number"
                                    >Serial Number *</Label
                                >
                                <Input
                                    id="serial_number"
                                    v-model="form.serial_number"
                                    type="text"
                                    placeholder="SN123456"
                                    required
                                />
                                <span
                                    v-if="form.errors.serial_number"
                                    class="text-sm text-red-600"
                                >
                                    {{ form.errors.serial_number }}
                                </span>
                            </div>

                            <!-- Asset Type -->
                            <div>
                                <Label for="asset_type">Tipo *</Label>
                                <Select v-model="form.asset_type">
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="laptop"
                                            >Laptop</SelectItem
                                        >
                                        <SelectItem value="desktop"
                                            >Desktop</SelectItem
                                        >
                                        <SelectItem value="server"
                                            >Server</SelectItem
                                        >
                                        <SelectItem value="software_license"
                                            >Software License</SelectItem
                                        >
                                        <SelectItem value="mobile_device"
                                            >Mobile Device</SelectItem
                                        >
                                        <SelectItem value="network_equipment"
                                            >Network Equipment</SelectItem
                                        >
                                    </SelectContent>
                                </Select>
                            </div>

                            <!-- Model & Manufacturer -->
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <Label for="model">Modelo</Label>
                                    <Input
                                        id="model"
                                        v-model="form.model"
                                        type="text"
                                        placeholder="Latitude 5520"
                                    />
                                </div>
                                <div>
                                    <Label for="manufacturer">Fabricante</Label>
                                    <Input
                                        id="manufacturer"
                                        v-model="form.manufacturer"
                                        type="text"
                                        placeholder="Dell"
                                    />
                                </div>
                            </div>

                            <!-- Status -->
                            <div>
                                <Label for="status">Status *</Label>
                                <Select v-model="form.status">
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="available"
                                            >Available</SelectItem
                                        >
                                        <SelectItem value="in_use"
                                            >In Use</SelectItem
                                        >
                                        <SelectItem value="under_repair"
                                            >Under Repair</SelectItem
                                        >
                                        <SelectItem value="retired"
                                            >Retired</SelectItem
                                        >
                                        <SelectItem value="lost"
                                            >Lost/Stolen</SelectItem
                                        >
                                    </SelectContent>
                                </Select>
                            </div>

                            <!-- Purchase Date & Warranty End -->
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <Label for="purchase_date"
                                        >Data de Compra</Label
                                    >
                                    <Input
                                        id="purchase_date"
                                        v-model="form.purchase_date"
                                        type="date"
                                    />
                                </div>
                                <div>
                                    <Label for="warranty_end"
                                        >Fim Garantia</Label
                                    >
                                    <Input
                                        id="warranty_end"
                                        v-model="form.warranty_end"
                                        type="date"
                                    />
                                </div>
                            </div>

                            <!-- Cost & Location -->
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <Label for="cost">Custo (€)</Label>
                                    <Input
                                        id="cost"
                                        v-model="form.cost"
                                        type="number"
                                        step="0.01"
                                        placeholder="1200.00"
                                    />
                                </div>
                                <div>
                                    <Label for="location">Localização</Label>
                                    <Input
                                        id="location"
                                        v-model="form.location"
                                        type="text"
                                        placeholder="Office"
                                    />
                                </div>
                            </div>

                            <!-- Assigned To -->
                            <div>
                                <Label for="assigned_to">Atribuído a</Label>
                                <Select v-model="form.assigned_to">
                                    <SelectTrigger>
                                        <SelectValue
                                            placeholder="Selecionar utilizador"
                                        />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem :value="null"
                                            >Nenhum</SelectItem
                                        >
                                        <SelectItem
                                            v-for="user in users"
                                            :key="user.id"
                                            :value="user.id"
                                        >
                                            {{ user.name }}
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <!-- Notes -->
                            <div>
                                <Label for="notes">Notas</Label>
                                <Textarea
                                    id="notes"
                                    v-model="form.notes"
                                    placeholder="Informações adicionais..."
                                />
                            </div>

                            <!-- Buttons -->
                            <div class="flex justify-end gap-4">
                                <Button
                                    type="button"
                                    variant="outline"
                                    @click="router.visit('/assets')"
                                >
                                    Cancelar
                                </Button>
                                <Button
                                    type="submit"
                                    :disabled="form.processing"
                                >
                                    Criar Asset
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
```

---

### Feature 14: Asset→Ticket Linking

#### Add affected_asset_id to Tickets

**a) Migration to add affected_asset_id:**

```bash
docker-compose exec orionone-app php artisan make:migration add_affected_asset_id_to_tickets_table
```

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
 public function up(): void
 {
 Schema::table('tickets', function (Blueprint $table) {
 $table->foreignId('affected_asset_id')
 ->nullable()
 ->after('assigned_to')
 ->constrained('assets')
 ->nullOnDelete();

 $table->index('affected_asset_id');
 });
 }

 public function down(): void
 {
 Schema::table('tickets', function (Blueprint $table) {
 $table->dropForeign(['affected_asset_id']);
 $table->dropColumn('affected_asset_id');
 });
 }
};
```

**b) Update Ticket Model:**

```php
// app/Models/Ticket.php

public function affectedAsset(): BelongsTo
{
 return $this->belongsTo(Asset::class, 'affected_asset_id');
}
```

**c) Update TicketController validation:**

```php
// app/Http/Controllers/Api/TicketController.php

$validated = $request->validate([
 // ... existing fields
 'affected_asset_id' => 'nullable|exists:assets,id',
]);
```

**d) Update Tickets/Create.vue (add Asset select):**

```vue
<!-- Add Asset Select in Tickets/Create.vue -->
<div>
 <Label for="affected_asset_id">Asset Afetado</Label>
 <Select v-model="form.affected_asset_id">
 <SelectTrigger>
 <SelectValue placeholder="Selecionar asset" />
 </SelectTrigger>
 <SelectContent>
 <SelectItem :value="null">Nenhum</SelectItem>
 <SelectItem v-for="asset in assets" :key="asset.id" :value="asset.id">
 {{ asset.name }} ({{ asset.serial_number }})
 </SelectItem>
 </SelectContent>
 </Select>
</div>
```

---

### Feature 15: CSV Import/Export (Maatwebsite Excel)

#### Bulk Asset Import

**a) Create AssetImport class:**

```bash
docker-compose exec orionone-app php artisan make:import AssetsImport --model=Asset
```

```php
<?php

namespace App\Imports;

use App\Models\Asset;
use Maatwebsite\Excel\Concerns\ToModel;
use Maatwebsite\Excel\Concerns\WithHeadingRow;
use Maatwebsite\Excel\Concerns\WithValidation;

class AssetsImport implements ToModel, WithHeadingRow, WithValidation
{
 public function model(array $row)
 {
 return new Asset([
 'name' => $row['name'],
 'serial_number' => $row['serial_number'],
 'asset_type' => $row['asset_type'],
 'model' => $row['model'] ?? null,
 'manufacturer' => $row['manufacturer'] ?? null,
 'status' => $row['status'] ?? 'available',
 'purchase_date' => $row['purchase_date'] ?? null,
 'warranty_end' => $row['warranty_end'] ?? null,
 'cost' => $row['cost'] ?? null,
 'location' => $row['location'] ?? null,
 ]);
 }

 public function rules(): array
 {
 return [
 'name' => 'required|string|max:255',
 'serial_number' => 'required|string|unique:assets,serial_number',
 'asset_type' => 'required|in:laptop,desktop,server,software_license,mobile_device,network_equipment',
 'status' => 'nullable|in:in_use,available,under_repair,retired,lost',
 ];
 }
}
```

**b) Add Import endpoint in AssetController:**

```php
// app/Http/Controllers/Api/AssetController.php

use App\Imports\AssetsImport;
use Maatwebsite\Excel\Facades\Excel;

/**
 * Import assets from CSV
 *
 * @bodyParam file file required CSV file with assets
 *
 * @response 200 {"message": "45 assets imported successfully"}
 */
public function import(Request $request)
{
 $request->validate([
 'file' => 'required|file|mimes:csv,xlsx|max:2048',
 ]);

 Excel::import(new AssetsImport, $request->file('file'));

 return response()->json([
 'message' => 'Assets imported successfully',
 ]);
}
```

**c) Add route:**

```php
// routes/api.php

Route::post('assets/import', [AssetController::class, 'import']);
```

**d) Create AssetImport.vue:**

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useForm } from "@inertiajs/vue3";
import AppLayout from "@/Layouts/AppLayout.vue";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Label } from "@/Components/ui/label";
import { Alert, AlertDescription } from "@/Components/ui/alert";
import { Upload, Download } from "lucide-vue-next";

const form = useForm({
    file: null,
});

const fileInput = ref<HTMLInputElement | null>(null);

function handleFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        form.file = target.files[0];
    }
}

function submit() {
    form.post("/api/v1/assets/import", {
        onSuccess: () => {
            alert("Assets imported successfully!");
            router.visit("/assets");
        },
    });
}

function downloadTemplate() {
    // Generate CSV template
    const headers =
        "name,serial_number,asset_type,model,manufacturer,status,purchase_date,warranty_end,cost,location\n";
    const example =
        "Dell Latitude 5520,SN123456,laptop,Latitude 5520,Dell,available,2024-01-15,2027-01-15,1200.00,Office\n";
    const csvContent = headers + example;

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "assets_template.csv";
    link.click();
}
</script>

<template>
    <AppLayout title="Importar Assets">
        <div class="py-12">
            <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                    <div class="p-6">
                        <h2 class="text-2xl font-semibold mb-6">
                            Importar Assets (CSV)
                        </h2>

                        <Alert class="mb-6">
                            <AlertDescription>
                                <p class="mb-2">
                                    <strong>Formato CSV esperado:</strong>
                                </p>
                                <p class="text-sm">
                                    name, serial_number, asset_type, model,
                                    manufacturer, status, purchase_date,
                                    warranty_end, cost, location
                                </p>
                            </AlertDescription>
                        </Alert>

                        <div class="mb-6">
                            <Button variant="outline" @click="downloadTemplate">
                                <Download class="mr-2 h-4 w-4" />
                                Download Template CSV
                            </Button>
                        </div>

                        <form @submit.prevent="submit" class="space-y-6">
                            <div>
                                <Label for="file"
                                    >Selecionar Ficheiro CSV *</Label
                                >
                                <Input
                                    id="file"
                                    ref="fileInput"
                                    type="file"
                                    accept=".csv,.xlsx"
                                    @change="handleFileChange"
                                    required
                                />
                                <span
                                    v-if="form.errors.file"
                                    class="text-sm text-red-600"
                                >
                                    {{ form.errors.file }}
                                </span>
                            </div>

                            <div class="flex justify-end gap-4">
                                <Button
                                    type="button"
                                    variant="outline"
                                    @click="router.visit('/assets')"
                                >
                                    Cancelar
                                </Button>
                                <Button
                                    type="submit"
                                    :disabled="form.processing"
                                >
                                    <Upload class="mr-2 h-4 w-4" />
                                    Importar Assets
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
```

---

### Feature 16: Asset Reports (Chart.js)

#### Asset Analytics Dashboard

**a) Create AssetReportController:**

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Asset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

/**
 * @group Asset Reports
 */
class AssetReportController extends Controller
{
 /**
 * Get asset statistics
 *
 * @response 200 {
 * "data": {
 * "by_status": {"in_use": 25, "available": 10},
 * "by_type": {"laptop": 20, "desktop": 15},
 * "warranty_expiring_30_days": 5,
 * "total_cost": 125000.00
 * }
 * }
 */
 public function statistics()
 {
 $byStatus = Asset::select('status', DB::raw('count(*) as count'))
 ->groupBy('status')
 ->pluck('count', 'status');

 $byType = Asset::select('asset_type', DB::raw('count(*) as count'))
 ->groupBy('asset_type')
 ->pluck('count', 'asset_type');

 $warrantyExpiring = Asset::warrantyExpiring(30)->count();

 $totalCost = Asset::sum('cost');

 return response()->json([
 'data' => [
 'by_status' => $byStatus,
 'by_type' => $byType,
 'warranty_expiring_30_days' => $warrantyExpiring,
 'total_cost' => $totalCost,
 ],
 ]);
 }

 /**
 * Get cost summary by location
 *
 * @response 200 {
 * "data": [
 * {"location": "Office", "total_cost": 75000, "count": 30},
 * {"location": "Remote", "total_cost": 50000, "count": 15}
 * ]
 * }
 */
 public function costByLocation()
 {
 $data = Asset::select('location', DB::raw('SUM(cost) as total_cost'), DB::raw('COUNT(*) as count'))
 ->groupBy('location')
 ->orderByDesc('total_cost')
 ->get();

 return response()->json(['data' => $data]);
 }
}
```

**b) Add routes:**

```php
// routes/api.php

Route::get('assets/reports/statistics', [AssetReportController::class, 'statistics']);
Route::get('assets/reports/cost-by-location', [AssetReportController::class, 'costByLocation']);
```

**c) Create AssetDashboard.vue (Chart.js):**

```vue
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";
import AppLayout from "@/Layouts/AppLayout.vue";

Chart.register(...registerables);

const chartByStatus = ref<HTMLCanvasElement | null>(null);
const chartByType = ref<HTMLCanvasElement | null>(null);

onMounted(async () => {
    const response = await fetch("/api/v1/assets/reports/statistics");
    const { data } = await response.json();

    // Chart: Assets by Status
    if (chartByStatus.value) {
        new Chart(chartByStatus.value, {
            type: "doughnut",
            data: {
                labels: Object.keys(data.by_status),
                datasets: [
                    {
                        data: Object.values(data.by_status),
                        backgroundColor: [
                            "#10b981",
                            "#3b82f6",
                            "#f59e0b",
                            "#6b7280",
                            "#ef4444",
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Assets por Status",
                    },
                },
            },
        });
    }

    // Chart: Assets by Type
    if (chartByType.value) {
        new Chart(chartByType.value, {
            type: "bar",
            data: {
                labels: Object.keys(data.by_type),
                datasets: [
                    {
                        label: "Quantidade",
                        data: Object.values(data.by_type),
                        backgroundColor: "#3b82f6",
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Assets por Tipo",
                    },
                },
            },
        });
    }
});
</script>

<template>
    <AppLayout title="Asset Dashboard">
        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Chart: Assets by Status -->
                    <div class="bg-white p-6 rounded-lg shadow-sm">
                        <canvas ref="chartByStatus"></canvas>
                    </div>

                    <!-- Chart: Assets by Type -->
                    <div class="bg-white p-6 rounded-lg shadow-sm">
                        <canvas ref="chartByType"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
```

---

### Checklist Sprint 7

-   [ ] Assets migration (6 types, status, relationships)
-   [ ] Asset Model (Eloquent relationships, scopes, activity log)
-   [ ] AssetFactory (generate test data)
-   [ ] AssetTest (CRUD, uniqueness, relationships, history)
-   [ ] AssetController (CRUD, warranty expiring API)
-   [ ] Asset→Ticket linking (affected_asset_id migration)
-   [ ] CSV Import (AssetsImport class + Maatwebsite Excel)
-   [ ] CSV Export template download
-   [ ] Assets/Index.vue (DataTable with filters, Shadcn components)
-   [ ] Assets/Create.vue (Form with Asset type select)
-   [ ] Assets/Edit.vue
-   [ ] AssetImport.vue (CSV upload + template download)
-   [ ] Asset Reports (AssetReportController statistics API)
-   [ ] AssetDashboard.vue (Chart.js charts - by status, by type)
-   [ ] API Documentation (Scribe annotations)
-   [ ] Tests passing (pest --filter=AssetTest)

---

### Sprint 1: Auth & Users (100% Completo) ✅

-   [x] Laravel IDE Helper
-   [x] Inertia Progress
-   [x] Publicar configs Spatie
-   [x] RolePermissionSeeder (3 roles)
-   [x] UserSeeder (3 test users)
-   [x] Profile Avatar Upload (COMPLETO - UpdateProfileAction.php, Edit.vue, UpdateProfileTest.php)

### Sprint 2: Tickets Core (0% Completo)

-   [ ] Migration tickets (não existe)
-   [ ] Model Ticket + relationships (não existe)
-   [ ] TicketData DTO (não existe)
-   [ ] CreateTicketAction (não existe)
-   [ ] TicketController + Query Builder (não existe)
-   [ ] Frontend: Index + Create (não existe)
-   [ ] Factory + Seeders (não existe)

### Sprint 3: Colaboração (0% Completo)

-   [ ] Comments system (public + internal)
-   [ ] Teams management
-   [ ] Email notifications (queued)
-   [ ] Mention system (@username)

### Sprint 4: Knowledge Base (0% Completo)

-   [ ] Articles CRUD
-   [ ] Categories hierarchy
-   [ ] Full-text search
-   [ ] Article voting (helpful/not)
-   [ ] Version history

### Sprint 5: Dashboard & Reports (0% Completo)

-   [ ] Admin dashboard (metrics)
-   [ ] Charts (tickets por dia, SLA)
-   [ ] Agent performance reports
-   [ ] Export PDF/Excel
-   [ ] Scheduled reports

### Sprint 6: Polish & Deploy

-   [ ] API Documentation (Scribe 5.5) - Final review
-   [ ] Performance optimization
-   [ ] E2E tests (Dusk)
-   [ ] Load testing
-   [ ] Security audit
-   [ ] Production deployment
-   [ ] Monitoring (Sentry)
-   [ ] Documentation completa
-   [ ] Video demo

### Sprint 7: Asset Management (CMDB)

-   [ ] Assets CRUD (6 types: Laptop, Desktop, Server, License, Mobile, Network)
-   [ ] Asset→Ticket linking (affected_asset_id foreign key)
-   [ ] CSV Import/Export (Maatwebsite Excel)
-   [ ] Basic relationships (Asset→User, Asset→Ticket, Asset→Asset)
-   [ ] Asset reports (status, type, warranty alerts, cost summary)

---

## Progresso Resumo por Sprint

| Sprint    | Features | Completas | Progresso |
| --------- | -------- | --------- | --------- |
| Sprint 1  | 6        | 5         | 85%       |
| Sprint 2  | 7        | 0         | 0%        |
| Sprint 3  | 4        | 0         | 0%        |
| Sprint 4  | 5        | 0         | 0%        |
| Sprint 5  | 5        | 0         | 0%        |
| Sprint 6  | 9        | 0         | 0%        |
| **TOTAL** | **36**   | **5**     | **14%**   |

**Próximo Objetivo:** Completar Feature 2 (Avatar Upload) para finalizar Sprint 1 a 100%

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

**Progresso Geral:** 18% (7 de 39 features completas)

### Sprint 1: Auth & Users - 100% COMPLETO ✅

-   [x] Laravel IDE Helper instalado
-   [x] Inertia Progress Bar configurado
-   [x] Publicar configs Spatie (Permission + Activity Log)
-   [x] RolePermissionSeeder criado (3 roles: admin, agent, user)
-   [x] UserSeeder criado (3 test users)
-   [x] RolePermissionTest passando (4/4 testes OK)
-   [x] Profile Avatar Upload (COMPLETO - 13 Nov 2025)

**Código Implementado:**

-   ✅ `database/seeders/RolePermissionSeeder.php`
-   ✅ `database/seeders/UserSeeder.php`
-   ✅ `tests/Feature/RolePermissionTest.php`
-   ✅ `tests/Feature/UpdateProfileTest.php` (3 test cases)
-   ✅ Migrations: permissions, roles, activity_log, add_avatar_to_users
-   ✅ `app/Actions/Users/UpdateProfileAction.php` (129 lines, fully documented)
-   ✅ `resources/js/Pages/Profile/Edit.vue` (avatar preview, upload, validation)
-   ✅ Route: `POST /profile` → UpdateProfileAction

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
-   [ ] Scribe 5.5 configurado (knuckleswtf/scribe já instalado)

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

-   [ ] API Documentation (Scribe 5.5) - Final review
-   [ ] Performance optimization
-   [ ] E2E tests (Dusk)
-   [ ] Load testing
-   [ ] Security audit
-   [ ] Production deployment
-   [ ] Monitoring (Sentry)
-   [ ] Documentation completa
-   [ ] Video demo

---

### Sprint 7: Asset Management (CMDB) - NÃO INICIADO

-   [ ] Assets migration (6 types, status, relationships)
-   [ ] Asset Model (Eloquent relationships, scopes, activity log)
-   [ ] AssetFactory (generate test data)
-   [ ] AssetTest (CRUD, uniqueness, relationships, history)
-   [ ] AssetController (CRUD, warranty expiring API)
-   [ ] Asset→Ticket linking (affected_asset_id migration)
-   [ ] CSV Import (AssetsImport class + Maatwebsite Excel)
-   [ ] CSV Export template download
-   [ ] Assets/Index.vue (DataTable with filters)
-   [ ] Assets/Create.vue (Form with Asset type select)
-   [ ] Assets/Edit.vue
-   [ ] AssetImport.vue (CSV upload + template download)
-   [ ] Asset Reports (AssetReportController statistics API)
-   [ ] AssetDashboard.vue (Chart.js charts)
-   [ ] API Documentation (Scribe annotations)
-   [ ] Tests passing

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

| Sprint    | Features | Completas | Em Progresso | Não Iniciadas | Status  |
| --------- | -------- | --------- | ------------ | ------------- | ------- |
| Sprint 1  | 7        | 7         | 0            | 0             | 100% ✅ |
| Sprint 2  | 5        | 0         | 0            | 5             | 0%      |
| Sprint 3  | 4        | 0         | 0            | 4             | 0%      |
| Sprint 4  | 5        | 0         | 0            | 5             | 0%      |
| Sprint 5  | 5        | 0         | 0            | 5             | 0%      |
| Sprint 6  | 9        | 0         | 0            | 9             | 0%      |
| Sprint 7  | 4        | 0         | 0            | 4             | 0%      |
| **TOTAL** | **39**   | **7**     | **0**        | **32**        | **18%** |

---

**Próximos Passos Recomendados:**

1. ✅ ~~Completar Sprint 1~~ - **CONCLUÍDO** (Avatar Upload implementado)
2. **🎯 PRÓXIMO: Iniciar Sprint 2** - Criar sistema de Tickets (Migrations, Models, Actions, Controllers, Views)
3. **Instalar pacotes críticos** - Tiptap (rich text), Chart.js (dashboard), MediaLibrary migrations

**Última Atualização:** 13 Novembro 2025, 12:00 ← **Sprint 1 COMPLETO (100%) + Pacotes instalados**
**Última Verificação Automática:** 13 Novembro 2025, 12:00
