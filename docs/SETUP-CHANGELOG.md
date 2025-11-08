# Setup Changelog - OrionOne

**Data:** 08 Novembro 2025
**Sessão:** Finalização do Setup Inicial

---

## Resumo

## Esta sessão completou a configuração inicial do projeto OrionOne, preparando todas as ferramentas necessárias para iniciar o desenvolvimento do Sprint 1.

## Alterações Realizadas

### 1. Pacotes Backend Instalados (Composer)

#### Arquitetura Moderna

-   `spatie/laravel-data` (4.18) - DTOs type-safe com validação automática
-   `lorisleiva/laravel-actions` (2.9) - Actions reutilizáveis (Controller/Job/Command/Listener)
-   `spatie/laravel-query-builder` (6.3) - Filtros automáticos via URL (?filter[status]=open)

#### Developer Experience

-   `barryvdh/laravel-ide-helper` (3.6) - Autocomplete para IDE (PHPStorm, VSCode)

**Comando usado:**

```bash
docker-compose exec orionone-app composer require spatie/laravel-data lorisleiva/laravel-actions spatie/laravel-query-builder barryvdh/laravel-ide-helper --dev
```

---

### 2. Pacotes Frontend Instalados (NPM)

#### Shadcn-vue Ecosystem

-   `clsx` - Utility para className condicionais
-   `tailwind-merge` - Merge classes Tailwind sem conflitos
-   `tailwindcss-animate` - Animações Tailwind CSS
-   `class-variance-authority` - Variantes de componentes type-safe
-   `lucide-vue-next` - Ícones Lucide (600+ ícones modernos)
-   `radix-vue` - Componentes acessíveis Radix UI
-   `reka-ui` - Primitives UI unstyled

#### Ícones

-   `@iconify/vue` - Acesso a 150k+ ícones

#### Forms & Validation

-   `vee-validate` - Forms complexos com validação

#### Progress Bar

-   `nprogress` - Loading bar customizável (alternativa ao @inertiajs/progress depreciado)

**Comandos usados:**

```bash
npm install clsx tailwind-merge class-variance-authority --legacy-peer-deps
npm install lucide-vue-next --legacy-peer-deps
npm install radix-vue reka-ui --legacy-peer-deps
npm install tailwindcss-animate --legacy-peer-deps
npm install @iconify/vue --legacy-peer-deps
npm install vee-validate --legacy-peer-deps
npm install nprogress --legacy-peer-deps
```

**Nota:** `--legacy-peer-deps` necessário devido a conflitos do Vite 7 com Shadcn-vue CLI.

---

### 3. IDE Helper Configurado

**Ficheiros gerados:**

-   `_ide_helper.php` - Autocomplete para facades Laravel
-   `.phpstorm.meta.php` - Meta info para PhpStorm

**Comandos executados:**

```bash
php artisan ide-helper:generate
php artisan ide-helper:meta
```

**Adicionado ao `.gitignore`:**

```
_ide_helper.php
_ide_helper_models.php
.phpstorm.meta.php
```

---

### 4. NProgress Configurado

**Ficheiro:** `resources/js/app.js`

**Alterações:**

-   Importado NProgress e CSS
-   Configurado `showSpinner: false`
-   Adicionados event listeners para Inertia router
-   Desabilitado progress bar default do Inertia (`progress: false`)

```js
import NProgress from "nprogress";
import "nprogress/nprogress.css";

NProgress.configure({ showSpinner: false });

router.on("start", () => NProgress.start());
router.on("finish", () => NProgress.done());
```

---

### 5. Tailwind CSS Configurado para Shadcn-vue

**Ficheiro:** `tailwind.config.js`

**Adicionado:**

-   Dark mode class-based
-   CSS variables para cores do theme
-   Border radius customizável
-   Plugin `tailwindcss-animate`

**Ficheiro:** `resources/css/app.css`

**Adicionado:**

-   CSS variables (light + dark mode)
-   65 linhas de configuração de tema

---

### 6. Estrutura de Diretórios Criada

```
app/
  Data/           # DTOs (Laravel Data)

resources/js/
  components/
    ui/           # Componentes Shadcn-vue (a criar manualmente)
  lib/
    utils.js      # Utilities (cn() para merge classes)
```

**Ficheiro:** `resources/js/lib/utils.js`

```js
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
    return twMerge(clsx(inputs));
}
```

---

### 7. Components.json Criado

**Ficheiro:** `components.json`

Configuração do Shadcn-vue (style, paths, aliases). Usado como referência para criar componentes manualmente.

---

### 8. Spatie Packages Configurados

**Configs publicados:**

-   `config/permission.php` (já existia)
-   `config/activitylog.php` (já existia)

**Migrations publicadas:**

-   Spatie Permission: `create_permission_tables`
-   Spatie Activity Log: `create_activity_log_table` + 2 adições

**Migrations executadas:**

```bash
php artisan migrate:fresh
```

**Resultado:**

-   9 migrations executadas com sucesso
-   Base de dados pronta para seeders

---

### 9. Documentação Atualizada

#### Ficheiros Modificados

**`docs/implementation-checklist.md`**

-   Completamente reescrito (1510 linhas)
-   Estrutura TDD: Planning → Tests First → Implementation → Frontend
-   Cada feature mostra ciclo RED-GREEN-REFACTOR
-   Removidos todos os emojis

**`docs/tech-stack.md`**

-   Atualizado com packages instalados
-   Removidos emojis
-   Adicionada explicação de porquê não usar Zod e Pest

**`README.md`**

-   Removidos emojis das secções de documentação

**`SETUP.md`**

-   Removidos emojis
-   Mantidos marcadores "NOVO"

#### Ficheiros Criados

**`docs/business-model.md`** (NOVO)

-   Business Model Canvas completo
-   Análise SWOT
-   Go-to-Market Strategy
-   Projeções financeiras 3 anos
-   25.631 linhas

**`docs/development-planning.md`** (NOVO)

-   Cronograma detalhado (Nov 2025 - Jan 2026)
-   6 sprints com user stories
-   KPIs técnicos e de projeto
-   Análise de riscos
-   24.670 linhas

---

## O Que NÃO Foi Feito (Deliberado)

### Seeders

**Status:** Revertidos para que o utilizador aprenda fazendo.

**Ficheiros que foram criados e depois revertidos:**

-   `database/seeders/RolePermissionSeeder.php`
-   `database/seeders/UserSeeder.php`
-   Alterações em `database/seeders/DatabaseSeeder.php`
-   Trait `HasRoles` em `app/Models/User.php`

**Para fazer manualmente:**
Seguir `docs/implementation-checklist.md` - Sprint 1, Feature 1: Role & Permission Setup.

### Componentes Shadcn-vue

**Status:** Estrutura criada, componentes a criar manualmente.

**Razão:** Shadcn-vue CLI não funciona com Vite 7 (peer dependency conflicts).

**Para fazer:**
Criar componentes manualmente em `resources/js/components/ui/` seguindo a documentação oficial.

### IDE Helper Models

**Status:** Não executado.

**Comando:** `php artisan ide-helper:models`

**Razão:** Requer conexão à base de dados com dados. PostgreSQL driver disponível apenas no Docker.

**Para fazer:**
Executar após criar seeders e popular base de dados.

---

## Próximos Passos Recomendados

### 1. Criar Seeders (Sprint 1, Feature 1)

Seguir TDD workflow em `implementation-checklist.md`:

1. Planning (30 min)
2. Tests First - criar `RolePermissionTest.php` (vai falhar - RED)
3. Implementation - criar `RolePermissionSeeder.php` (testes passam - GREEN)
4. Criar `UserSeeder.php` com utilizadores teste

### 2. Executar Seeders

```bash
php artisan db:seed
```

### 3. Gerar IDE Helper Models

```bash
docker-compose exec orionone-app php artisan ide-helper:models --write
```

### 4. Criar Componentes Shadcn-vue Base

Criar manualmente em `resources/js/components/ui/`:

-   Button.vue
-   Input.vue
-   Card.vue
-   Badge.vue
-   Avatar.vue

### 5. Testar Login

Credenciais dos utilizadores teste (após seeder):

-   **Admin:** admin@orionone.test / password
-   **Agent:** agent@orionone.test / password
-   **User:** user@orionone.test / password

---

## Comandos Úteis Docker

### Executar comandos Laravel

```bash
docker-compose exec orionone-app php artisan [comando]
```

### Executar testes

```bash
docker-compose exec orionone-app php artisan test
```

### Entrar no container

```bash
docker-compose exec orionone-app bash
```

### Ver logs

```bash
docker-compose logs -f orionone-app
```

---

## Verificação Final

### Backend

-   [x] Composer packages instalados
-   [x] IDE Helper configurado
-   [x] Spatie configs publicados
-   [x] Migrations executadas
-   [ ] Seeders (para fazer)

### Frontend

-   [x] NPM packages instalados
-   [x] NProgress configurado
-   [x] Tailwind CSS com variáveis
-   [x] Estrutura de diretórios
-   [x] Utils helper criado
-   [ ] Componentes UI (para fazer)

### Documentação

-   [x] Implementation checklist TDD
-   [x] Tech stack atualizado
-   [x] Business model criado
-   [x] Development planning criado
-   [x] Emojis removidos
-   [x] Setup profissional

---

## Estado do Projeto

**Setup:** 95% Completo

**Pronto para:** Sprint 1 - Auth & Users

**Próxima Sessão:** Criar seeders seguindo TDD workflow

---

**Última Atualização:** 08 Novembro 2025, 00:35
