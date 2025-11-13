# PARTE 5: Limpeza & Arquivamento (Week 2 End)

> **⚠️ TIMING ATUALIZADO:** > **Execução**: **Week 2 End (29 Nov 2024) → Weekend (30 Nov - 1 Dec)** > **Timing Original**: Week 10+ (27-31 Jan 2025) ❌
> **Duração**: 2-3 horas
> **Pré-requisitos**: Week 2 completo (Tickets Module backend), Week 3 CSS migration ainda pendente

---

## 🔄 Justificativa da Antecipação

### Por Que Antecipar de Week 10 para Week 2?

**Bloqueio Identificado:**

-   **Week 3 Day 1:** Tarefa "Copiar Tailwind CSS do Laravel"
-   **Ficheiros Necessários:**
    -   `resources/css/app.css` (30+ CSS variables)
    -   `tailwind.config.js` (colors, borderRadius, fonts)
-   **Window de Execução:** Após Week 2 Friday (29 Nov), antes de Week 3 Monday (2 Dec)

**Benefícios:**

-   ✅ Libera ~350 MB de espaço (vendor/ + node_modules/ Laravel)
-   ✅ Reduz confusão no workspace (sem 2 stacks paralelas)
-   ✅ Acelera Git operations (200+ ficheiros a menos)
-   ✅ Foco 100% no Next.js/Nest.js

**Sem Riscos:**

-   Git tag `v0.1.0-laravel` permanece (backup sempre disponível)
-   Docker Compose já não usa Laravel (migrado para Nest.js)
-   CSS será copiado do arquivo antes de continuar Week 3

---

## 📅 Plano de Execução (29 Nov - 1 Dec)

1. **Week 2 Friday (29 Nov):** Completar Tickets Module backend
2. **Weekend (30 Nov - 1 Dec):** Executar cleanup → `archive-laravel-vue/`
3. **Week 3 Monday (2 Dec):** Copiar CSS do arquivo → Continuar frontend

---

## 📋 Visão Geral

Após a migração completa para **Next.js 15 + Nest.js 10**, todos os ficheiros Laravel/PHP/Vue devem ser:

1. ✅ **Arquivados** em `archive-laravel-vue/` com backup Git tag `v0.1.0-laravel`
2. 🗑️ **Removidos** da raiz do projeto (cleanup completo)
3. 📝 **Documentados** com README explicativo no arquivo

**Objetivo**: Deixar apenas código Next.js/Nest.js na raiz, mantendo backup seguro do Laravel/Vue.

---

## 🎯 Checklist de Limpeza

### ✅ Antes de Começar

**CRITICAL**: Verificar se migração está 100% completa

```bash
# 1. Verificar MVP funcional
- [ ] Login/Register funcionando (Next.js → Nest.js)
- [ ] Dashboard carregando dados (PostgreSQL via Prisma)
- [ ] Tickets CRUD completo (criar, listar, editar, deletar)
- [ ] Comments funcionando
- [ ] File uploads (avatares, anexos)
- [ ] Permissions/Roles (CASL)
- [ ] Notificações
- [ ] Knowledge Base
- [ ] Assets Management

# 2. Verificar Docker
- [ ] 8 containers rodando: postgres, redis, meilisearch, mailpit, backend, frontend, nginx
- [ ] Health checks: http://localhost/api/health → {"status":"ok"}
- [ ] Frontend: http://localhost → Next.js app
- [ ] Backend: http://localhost/api → Nest.js API
- [ ] Swagger: http://localhost/api/docs

# 3. Verificar testes
cd nest-backend && npm run test        # Unit tests passando
cd nest-backend && npm run test:e2e    # E2E tests passando
cd next-frontend && npm run test       # Component tests passando

# 4. Verificar Git backup
git tag                                 # Confirmar tag v0.1.0-laravel existe
git show v0.1.0-laravel                 # Verificar conteúdo do backup

# 5. Criar segundo backup (pré-cleanup)
git add .
git commit -m "feat: complete Next.js + Nest.js migration (Week 10)"
git tag v1.0.0-nextjs-nestjs
git push origin v1.0.0-nextjs-nestjs
```

**⚠️ STOP**: Se qualquer item acima falhar, NÃO prosseguir com cleanup!

---

## 📦 Estrutura de Arquivamento

```
c:\laragon\www\orionone\
├── archive-laravel-vue/           # ← Novo: Arquivo completo Laravel/Vue
│   ├── README.md                   # ← Index do arquivo
│   │
│   ├── app/                        # ← Backend Laravel
│   │   ├── Http/
│   │   │   ├── Controllers/        # 8 controllers
│   │   │   ├── Middleware/
│   │   │   └── Requests/           # Form validations
│   │   ├── Models/                 # 12 Eloquent models
│   │   ├── Services/               # 5 services
│   │   ├── Actions/                # 3 actions
│   │   ├── Policies/               # Authorization
│   │   ├── Observers/              # Model hooks
│   │   ├── Providers/
│   │   └── Notifications/
│   │
│   ├── resources/                  # ← Frontend Vue
│   │   ├── js/
│   │   │   ├── Pages/              # 12 Inertia pages
│   │   │   ├── Components/         # 26 Vue components
│   │   │   ├── Layouts/            # 3 layouts
│   │   │   └── Stores/             # 4 Pinia stores
│   │   ├── css/
│   │   │   └── app.css             # Tailwind + CSS variables
│   │   └── views/
│   │       ├── app.blade.php       # Inertia root
│   │       └── scribe/             # API docs
│   │
│   ├── database/                   # ← Database
│   │   ├── migrations/             # 15 migrations
│   │   ├── seeders/                # Seed data
│   │   └── factories/              # Factories
│   │
│   ├── routes/                     # ← Routes
│   │   ├── web.php                 # Web routes
│   │   ├── auth.php                # Auth routes
│   │   └── console.php             # Artisan commands
│   │
│   ├── tests/                      # ← Tests
│   │   ├── Feature/                # Feature tests
│   │   └── Unit/                   # Unit tests
│   │
│   ├── config/                     # ← Laravel config
│   │   ├── app.php
│   │   ├── database.php
│   │   ├── auth.php
│   │   └── ... (18 config files)
│   │
│   ├── bootstrap/                  # ← Bootstrap
│   │   ├── app.php
│   │   └── cache/
│   │
│   ├── public/                     # ← Public assets
│   │   ├── index.php               # Laravel entry point
│   │   └── vendor/
│   │
│   ├── storage/                    # ← Storage
│   │   ├── app/
│   │   ├── framework/
│   │   └── logs/
│   │
│   ├── docker/                     # ← Docker configs Laravel
│   │   ├── 8.3/
│   │   └── nginx/
│   │
│   ├── docs/                       # ← Documentação técnica
│   │   ├── architecture-laravel.md
│   │   ├── tech-stack-laravel-vue.md
│   │   ├── TECH-DEEP-DIVE-BACKEND-LARAVEL.md
│   │   ├── TECH-DEEP-DIVE-FRONTEND-VUE.md
│   │   ├── TECH-DEEP-DIVE-DATABASE-LARAVEL.md
│   │   └── TECH-DEEP-DIVE-DEVOPS-LARAVEL.md
│   │
│   ├── vendor/                     # ← Composer dependencies
│   ├── node_modules/               # ← npm dependencies (Vite, Vue)
│   │
│   ├── artisan                     # ← Artisan CLI
│   ├── composer.json
│   ├── composer.lock
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── phpunit.xml
│   ├── phpstan.neon
│   ├── .env.example
│   ├── .scribe/                    # ← Scribe API docs
│   ├── sail                        # ← Laravel Sail
│   ├── docker-compose.yml          # ← Docker Compose Laravel
│   ├── Dockerfile                  # ← Dockerfile Laravel
│   ├── _ide_helper.php
│   └── _ide_helper_models.php
│
├── nest-backend/                   # ✅ Backend Next.js (MANTÉM)
├── next-frontend/                  # ✅ Frontend Nest.js (MANTÉM)
├── docs/                           # ✅ Documentação migração (MANTÉM)
│   ├── MIGRATION-PART-1-SETUP.md
│   ├── MIGRATION-PART-2-BACKEND.md
│   ├── MIGRATION-PART-3-FRONTEND.md
│   ├── MIGRATION-PART-4-TIMELINE.md
│   ├── MIGRATION-PART-5-CLEANUP.md  # ← ESTE DOCUMENTO
│   ├── MIGRATION-REVIEW-GAPS.md
│   ├── MIGRATION-READY.md
│   ├── architecture.md             # ← Arquitetura Next.js/Nest.js
│   ├── business-model.md
│   ├── database-schema.md
│   └── ...
│
├── .github/                        # ✅ GitHub configs (MANTÉM)
├── .vscode/                        # ✅ VS Code configs (MANTÉM)
├── scripts/                        # ✅ Scripts Python (MANTÉM)
├── README.md                       # ✅ ATUALIZAR (Next.js/Nest.js)
├── LICENSE
├── CONTRIBUTING.md
├── SETUP.md                        # ✅ ATUALIZAR (novo setup)
└── DEPLOYMENT.md                   # ✅ ATUALIZAR (novo deploy)
```

---

## 🗂️ Ficheiros a Arquivar

### 1. Backend Laravel (PHP)

```bash
# Mover para archive-laravel-vue/
app/                      # TODOS os controllers, models, services, actions, policies
bootstrap/                # Laravel bootstrap
config/                   # 18 ficheiros de configuração Laravel
database/                 # Migrations, seeders, factories
routes/                   # web.php, auth.php, console.php
vendor/                   # Composer dependencies (pode deletar, está no backup Git)
artisan                   # CLI Laravel
composer.json
composer.lock
phpunit.xml               # PHPUnit config
phpstan.neon              # PHPStan config
sail                      # Laravel Sail script
_ide_helper.php
_ide_helper_models.php
.phpunit.result.cache
prepareBindings($bindings)  # Ficheiro temporário
```

**Total**: ~3,500 linhas PHP, 12 models, 8 controllers, 5 services, 15 migrations

### 2. Frontend Vue (JavaScript)

```bash
# Mover para archive-laravel-vue/
resources/js/             # Pages, Components, Layouts, Stores (Vue 3 + Inertia)
resources/css/            # app.css (Tailwind + CSS variables)
resources/views/          # Blade templates (app.blade.php, scribe/, vendor/)
node_modules/             # npm dependencies (pode deletar, está no backup Git)
vite.config.js            # Vite bundler
tailwind.config.js        # Tailwind config (tem CSS variables!)
postcss.config.js         # PostCSS config
jsconfig.json             # JavaScript config
package.json              # npm dependencies (Vite, Vue, Inertia)
package-lock.json
components.json           # Shadcn-vue config
```

**Total**: ~2,800 linhas Vue, 12 pages, 26 componentes, 4 stores

### 3. Docker Laravel/PHP

```bash
# Mover para archive-laravel-vue/
docker/                   # Docker configs (8.0/, 8.1/, 8.2/, 8.3/, mariadb/, mysql/, nginx/, pgsql/)
docker-compose.yml        # Docker Compose Laravel (6 containers)
Dockerfile                # Dockerfile Laravel (PHP 8.3)
.dockerignore
.env.docker
```

**Nota**: Next.js/Nest.js terão novos docker-compose.yml + Dockerfiles na raiz

### 4. Tests Laravel/PHP

```bash
# Mover para archive-laravel-vue/
tests/                    # Feature tests (12), Unit tests (1)
  Feature/
    Auth/                 # AuthenticationTest, RegistrationTest, etc.
    ProfileTest.php
    RolePermissionTest.php
    UpdateProfileTest.php
  Unit/
    ExampleTest.php
  Pest.php                # Pest config
  TestCase.php
```

**Total**: 13 test files

### 5. Public Laravel

```bash
# Mover para archive-laravel-vue/
public/
  index.php               # Laravel entry point
  robots.txt              # Robots (copiar para next-frontend/public/)
  hot                     # Vite HMR
  images/                 # Imagens (migrar para next-frontend/public/)
  vendor/                 # Vendor assets
```

### 6. Storage Laravel

```bash
# Mover para archive-laravel-vue/
storage/
  app/                    # Uploaded files
    public/               # Public uploads (avatares, etc.)
  framework/              # Cache, sessions, views
    cache/
    sessions/
    views/
  logs/                   # Laravel logs
  debugbar/               # Debugbar cache
```

**Nota**: Uploads devem ser migrados para storage Next.js/Nest.js

### 7. Scribe API Docs

```bash
# Mover para archive-laravel-vue/
.scribe/                  # Scribe generated docs
resources/views/scribe/   # Scribe templates
```

**Substituir por**: Swagger no Nest.js (http://localhost/api/docs)

### 8. Laravel Vendor

```bash
# DELETAR (não arquivar, já está no backup Git)
vendor/                   # 150+ MB de Composer dependencies

# Se quiser manter no arquivo (opcional)
# Mas recomendado deletar e usar composer install no backup Git
```

### 9. Node Modules Vue

```bash
# DELETAR (não arquivar, já está no backup Git)
node_modules/             # 200+ MB de npm dependencies (Vite, Vue, etc.)

# Se quiser manter no arquivo (opcional)
# Mas recomendado deletar e usar npm install no backup Git
```

### 10. Configurações de Ambiente

```bash
# Mover para archive-laravel-vue/
.env                      # CRITICAL: Contém secrets Laravel
.env.example              # Template
.env.docker               # Docker env
.env.testing              # Testing env
```

**⚠️ SECURITY**: `.env` tem DATABASE_PASSWORD, APP_KEY, etc. Manter no arquivo privado.

### 11. Configurações Editor

```bash
# MANTÉM na raiz (serve para Next.js/Nest.js também)
.editorconfig             # ✅ Mantém
.gitignore                # ✅ Mantém (atualizar para Next.js/Nest.js)
.gitattributes            # ✅ Mantém
.phpstorm.meta.php        # ❌ Mover para archive (PHP-specific)
```

---

## 🔧 Comandos de Arquivamento

### Script Completo (PowerShell)

```powershell
# ===========================
# SCRIPT DE ARQUIVAMENTO
# OrionOne - Laravel → Next.js/Nest.js
# ===========================

# 1. VERIFICAÇÕES PRÉ-ARQUIVAMENTO
Write-Host "🔍 Verificando migração completa..." -ForegroundColor Cyan

# Verificar tag backup
git tag | Select-String "v0.1.0-laravel"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERRO: Tag v0.1.0-laravel não encontrada!" -ForegroundColor Red
    Write-Host "Execute: git tag v0.1.0-laravel" -ForegroundColor Yellow
    exit 1
}

# Verificar projetos Next.js/Nest.js
if (!(Test-Path "nest-backend") -or !(Test-Path "next-frontend")) {
    Write-Host "❌ ERRO: nest-backend/ ou next-frontend/ não encontrados!" -ForegroundColor Red
    exit 1
}

# Verificar Docker rodando
docker ps | Select-String "orionone"
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ WARNING: Docker não está rodando. Deseja continuar? (S/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -ne "S") { exit 1 }
}

Write-Host "✅ Verificações passaram!" -ForegroundColor Green

# 2. CRIAR SEGUNDO BACKUP (PRÉ-CLEANUP)
Write-Host "`n📦 Criando backup pré-cleanup..." -ForegroundColor Cyan
git add .
git commit -m "feat: complete Next.js + Nest.js migration (Week 10)"
git tag v1.0.0-nextjs-nestjs
git push origin v1.0.0-nextjs-nestjs

Write-Host "✅ Backup v1.0.0-nextjs-nestjs criado!" -ForegroundColor Green

# 3. CRIAR ESTRUTURA DE ARQUIVAMENTO
Write-Host "`n📁 Criando estrutura de arquivamento..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "archive-laravel-vue"

# 4. MOVER BACKEND LARAVEL (PHP)
Write-Host "`n🔄 Movendo backend Laravel..." -ForegroundColor Cyan
Move-Item -Path "app" -Destination "archive-laravel-vue/app"
Move-Item -Path "bootstrap" -Destination "archive-laravel-vue/bootstrap"
Move-Item -Path "config" -Destination "archive-laravel-vue/config"
Move-Item -Path "database" -Destination "archive-laravel-vue/database"
Move-Item -Path "routes" -Destination "archive-laravel-vue/routes"
Move-Item -Path "artisan" -Destination "archive-laravel-vue/artisan"
Move-Item -Path "composer.json" -Destination "archive-laravel-vue/composer.json"
Move-Item -Path "composer.lock" -Destination "archive-laravel-vue/composer.lock"
Move-Item -Path "phpunit.xml" -Destination "archive-laravel-vue/phpunit.xml"
Move-Item -Path "phpstan.neon" -Destination "archive-laravel-vue/phpstan.neon"
Move-Item -Path "sail" -Destination "archive-laravel-vue/sail"
Move-Item -Path "_ide_helper.php" -Destination "archive-laravel-vue/_ide_helper.php"
Move-Item -Path "_ide_helper_models.php" -Destination "archive-laravel-vue/_ide_helper_models.php"
if (Test-Path ".phpunit.result.cache") {
    Move-Item -Path ".phpunit.result.cache" -Destination "archive-laravel-vue/.phpunit.result.cache"
}
if (Test-Path "prepareBindings(`$bindings)") {
    Move-Item -Path "prepareBindings(`$bindings)" -Destination "archive-laravel-vue/prepareBindings(`$bindings)"
}
Move-Item -Path ".phpstorm.meta.php" -Destination "archive-laravel-vue/.phpstorm.meta.php"

Write-Host "✅ Backend Laravel arquivado!" -ForegroundColor Green

# 5. MOVER FRONTEND VUE (JAVASCRIPT)
Write-Host "`n🔄 Movendo frontend Vue..." -ForegroundColor Cyan
Move-Item -Path "resources" -Destination "archive-laravel-vue/resources"
Move-Item -Path "vite.config.js" -Destination "archive-laravel-vue/vite.config.js"
Move-Item -Path "postcss.config.js" -Destination "archive-laravel-vue/postcss.config.js"
Move-Item -Path "jsconfig.json" -Destination "archive-laravel-vue/jsconfig.json"
Move-Item -Path "components.json" -Destination "archive-laravel-vue/components.json"

# Copiar tailwind.config.js (pode ser útil para referência de CSS variables)
Copy-Item -Path "tailwind.config.js" -Destination "archive-laravel-vue/tailwind.config.js"
Remove-Item -Path "tailwind.config.js"

# Mover package.json Laravel/Vue
Move-Item -Path "package.json" -Destination "archive-laravel-vue/package.json"
Move-Item -Path "package-lock.json" -Destination "archive-laravel-vue/package-lock.json"

Write-Host "✅ Frontend Vue arquivado!" -ForegroundColor Green

# 6. MOVER DOCKER LARAVEL
Write-Host "`n🔄 Movendo Docker configs Laravel..." -ForegroundColor Cyan
Move-Item -Path "docker" -Destination "archive-laravel-vue/docker"
Move-Item -Path "docker-compose.yml" -Destination "archive-laravel-vue/docker-compose.yml"
Move-Item -Path "Dockerfile" -Destination "archive-laravel-vue/Dockerfile"
Move-Item -Path ".dockerignore" -Destination "archive-laravel-vue/.dockerignore"
if (Test-Path ".env.docker") {
    Move-Item -Path ".env.docker" -Destination "archive-laravel-vue/.env.docker"
}

Write-Host "✅ Docker Laravel arquivado!" -ForegroundColor Green

# 7. MOVER TESTS LARAVEL
Write-Host "`n🔄 Movendo tests Laravel..." -ForegroundColor Cyan
Move-Item -Path "tests" -Destination "archive-laravel-vue/tests"

Write-Host "✅ Tests Laravel arquivados!" -ForegroundColor Green

# 8. MOVER PUBLIC LARAVEL
Write-Host "`n🔄 Movendo public Laravel..." -ForegroundColor Cyan

# Copiar robots.txt e images/ para next-frontend/public/ antes de mover
if (Test-Path "public/robots.txt") {
    Copy-Item -Path "public/robots.txt" -Destination "next-frontend/public/robots.txt"
}
if (Test-Path "public/images") {
    Copy-Item -Path "public/images" -Destination "next-frontend/public/images" -Recurse
}

# Mover public/ completo para arquivo
Move-Item -Path "public" -Destination "archive-laravel-vue/public"

Write-Host "✅ Public Laravel arquivado!" -ForegroundColor Green

# 9. MOVER STORAGE LARAVEL
Write-Host "`n🔄 Movendo storage Laravel..." -ForegroundColor Cyan

# CRITICAL: Migrar uploads antes de mover
if (Test-Path "storage/app/public") {
    Write-Host "⚠️ Migrando uploads para Next.js/Nest.js..." -ForegroundColor Yellow
    # TODO: Copiar para nest-backend/uploads/ ou S3
    # Por enquanto, manter no arquivo
}

Move-Item -Path "storage" -Destination "archive-laravel-vue/storage"

Write-Host "✅ Storage Laravel arquivado!" -ForegroundColor Green

# 10. MOVER SCRIBE API DOCS
Write-Host "`n🔄 Movendo Scribe API docs..." -ForegroundColor Cyan
if (Test-Path ".scribe") {
    Move-Item -Path ".scribe" -Destination "archive-laravel-vue/.scribe"
}

Write-Host "✅ Scribe arquivado!" -ForegroundColor Green

# 11. MOVER CONFIGURAÇÕES DE AMBIENTE
Write-Host "`n🔄 Movendo .env Laravel..." -ForegroundColor Cyan
if (Test-Path ".env") {
    Move-Item -Path ".env" -Destination "archive-laravel-vue/.env"
}
if (Test-Path ".env.example") {
    Move-Item -Path ".env.example" -Destination "archive-laravel-vue/.env.example"
}
if (Test-Path ".env.testing") {
    Move-Item -Path ".env.testing" -Destination "archive-laravel-vue/.env.testing"
}

Write-Host "✅ .env arquivados!" -ForegroundColor Green

# 12. DELETAR VENDOR E NODE_MODULES (OPCIONAL)
Write-Host "`n🗑️ Deletando vendor/ e node_modules/..." -ForegroundColor Cyan
Write-Host "⚠️ Deseja deletar vendor/ e node_modules/? (S/N)" -ForegroundColor Yellow
Write-Host "   (Estão no backup Git, pode recuperar com composer/npm install)" -ForegroundColor Gray
$response = Read-Host

if ($response -eq "S") {
    if (Test-Path "vendor") {
        Remove-Item -Path "vendor" -Recurse -Force
        Write-Host "✅ vendor/ deletado!" -ForegroundColor Green
    }
    if (Test-Path "node_modules") {
        Remove-Item -Path "node_modules" -Recurse -Force
        Write-Host "✅ node_modules/ deletado!" -ForegroundColor Green
    }
} else {
    if (Test-Path "vendor") {
        Move-Item -Path "vendor" -Destination "archive-laravel-vue/vendor"
    }
    if (Test-Path "node_modules") {
        Move-Item -Path "node_modules" -Destination "archive-laravel-vue/node_modules"
    }
    Write-Host "✅ vendor/ e node_modules/ movidos para arquivo!" -ForegroundColor Green
}

# 13. COMMIT ARQUIVAMENTO
Write-Host "`n📝 Commitando arquivamento..." -ForegroundColor Cyan
git add .
git commit -m "refactor: archive Laravel/Vue code to archive-laravel-vue/

- Moved all PHP/Laravel backend code
- Moved all Vue/Inertia frontend code
- Moved Laravel tests, configs, routes
- Moved Docker configs (Laravel)
- Moved Scribe API docs
- Moved storage and public assets
- Clean root: only Next.js + Nest.js remain

Tag backups:
- v0.1.0-laravel: Original Laravel/Vue (Sprint 1)
- v1.0.0-nextjs-nestjs: Complete migration (Week 10)

See: docs/MIGRATION-PART-5-CLEANUP.md"

git push origin feat/migrate-nextjs-nestjs

Write-Host "`n✅ ARQUIVAMENTO COMPLETO!" -ForegroundColor Green
Write-Host "`n📊 Estrutura final:" -ForegroundColor Cyan
Get-ChildItem -Directory | Select-Object Name

Write-Host "`n📦 Backups disponíveis:" -ForegroundColor Cyan
git tag | Select-String "laravel|nextjs"

Write-Host "`n🎉 Migração 100% completa! Projeto limpo e organizado." -ForegroundColor Green
```

### Uso do Script

```powershell
# Salvar script
New-Item -Path "scripts/archive-laravel.ps1" -ItemType File

# Copiar conteúdo acima para scripts/archive-laravel.ps1

# Executar (Week 10+, após migração completa)
cd c:\laragon\www\orionone
.\scripts\archive-laravel.ps1
```

---

## 📝 Atualizar Documentação na Raiz

### 1. README.md

````markdown
# OrionOne - ITSM Platform

> **Stack**: Next.js 15 + Nest.js 10 + PostgreSQL + TypeScript
> **Versão**: v1.0.0
> **Status**: ✅ Production Ready

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# Start Docker containers (8 services)
docker-compose up -d

# Backend: http://localhost/api
# Frontend: http://localhost
# Swagger: http://localhost/api/docs
```
````

## 📦 Stack

-   **Frontend**: Next.js 15 (App Router), React 19, Tailwind CSS v4, Shadcn-ui
-   **Backend**: Nest.js 10, Prisma ORM, JWT Auth, CASL Permissions
-   **Database**: PostgreSQL 16, Redis 7.2, Meilisearch 1.9
-   **Infrastructure**: Docker Compose, Nginx, Mailpit

## 📚 Documentação

-   [`docs/architecture.md`](docs/architecture.md) - Arquitetura completa
-   [`docs/SETUP.md`](SETUP.md) - Setup desenvolvimento
-   [`docs/MIGRATION-PART-*.md`](docs/) - Migração Laravel → Next.js/Nest.js
-   [`nest-backend/README.md`](nest-backend/README.md) - Backend docs
-   [`next-frontend/README.md`](next-frontend/README.md) - Frontend docs

## 🗃️ Versão Anterior (Laravel/Vue)

Esta aplicação foi migrada de **Laravel 12 + Vue 3** para **Next.js 15 + Nest.js 10**.

-   **Backup Git**: Tag `v0.1.0-laravel`
-   **Arquivo**: `archive-laravel-vue/` (código Laravel/Vue completo)
-   **Documentação**: `archive-laravel-vue/README.md`

```bash
# Recuperar código Laravel/Vue
git checkout v0.1.0-laravel
```

## 🧪 Tests

```bash
# Backend (Nest.js)
cd nest-backend
npm run test        # Unit tests
npm run test:e2e    # E2E tests

# Frontend (Next.js)
cd next-frontend
npm run test        # Component tests
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

````

### 2. SETUP.md

Atualizar com instruções Next.js/Nest.js:

```markdown
# Setup - OrionOne (Next.js + Nest.js)

## Pré-requisitos

- Node.js 20+
- Docker & Docker Compose
- Git

## Instalação

1. Clone o repositório
2. Configure environment variables:
   - `nest-backend/.env` (DATABASE_URL, JWT_SECRET)
   - `next-frontend/.env.local` (NEXT_PUBLIC_API_URL)
3. Start Docker: `docker-compose up -d`
4. Run migrations: `cd nest-backend && npx prisma migrate dev`
5. Seed database: `cd nest-backend && npx prisma db seed`
6. Access: http://localhost

Veja documentação completa em `docs/MIGRATION-PART-1-SETUP.md`
````

### 3. DEPLOYMENT.md

Atualizar com deploy Next.js/Nest.js:

```markdown
# Deployment - OrionOne

## Production

-   **Frontend**: Vercel ou Docker (Next.js standalone)
-   **Backend**: AWS ECS, Heroku ou Docker
-   **Database**: AWS RDS PostgreSQL
-   **Storage**: AWS S3
-   **Email**: SendGrid ou AWS SES

Veja guia completo em `docs/MIGRATION-PART-1-SETUP.md` (Deploy section)
```

---

## 🎯 Estrutura Final (Pós-Cleanup)

```
c:\laragon\www\orionone\
├── archive-laravel-vue/         # ✅ Arquivo completo Laravel/Vue
│   ├── README.md                #    - Documentação do arquivo
│   ├── app/                     #    - Backend Laravel (PHP)
│   ├── resources/               #    - Frontend Vue
│   ├── database/                #    - Migrations, seeders
│   ├── routes/                  #    - Routes Laravel
│   ├── tests/                   #    - Tests Laravel
│   ├── config/                  #    - Config Laravel
│   ├── public/                  #    - Public Laravel
│   ├── storage/                 #    - Storage Laravel
│   ├── docker/                  #    - Docker Laravel
│   ├── docs/                    #    - Docs técnicos Laravel/Vue
│   ├── composer.json            #    - Composer
│   ├── package.json             #    - npm (Vite, Vue)
│   └── ...                      #    - Outros ficheiros Laravel
│
├── nest-backend/                # ✅ Backend Nest.js (ATIVO)
│   ├── src/
│   ├── prisma/
│   ├── test/
│   ├── package.json
│   └── ...
│
├── next-frontend/               # ✅ Frontend Next.js (ATIVO)
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── docs/                        # ✅ Documentação (ATIVO)
│   ├── architecture.md          #    - Arquitetura Next.js/Nest.js
│   ├── MIGRATION-PART-1-SETUP.md
│   ├── MIGRATION-PART-2-BACKEND.md
│   ├── MIGRATION-PART-3-FRONTEND.md
│   ├── MIGRATION-PART-4-TIMELINE.md
│   ├── MIGRATION-PART-5-CLEANUP.md  # ← ESTE DOCUMENTO
│   ├── MIGRATION-REVIEW-GAPS.md
│   ├── MIGRATION-READY.md
│   └── ...
│
├── .github/                     # ✅ GitHub configs
├── .vscode/                     # ✅ VS Code configs
├── scripts/                     # ✅ Scripts Python + PowerShell
│   ├── archive-laravel.ps1      #    - Script de arquivamento
│   └── ...
│
├── docker-compose.yml           # ✅ Docker Compose (8 containers)
├── README.md                    # ✅ ATUALIZADO (Next.js/Nest.js)
├── SETUP.md                     # ✅ ATUALIZADO
├── DEPLOYMENT.md                # ✅ ATUALIZADO
├── CONTRIBUTING.md              # ✅ Mantém
├── LICENSE                      # ✅ Mantém
└── .gitignore                   # ✅ ATUALIZADO
```

**Raiz**: Apenas Next.js + Nest.js + documentação migração
**Arquivo**: Todo código Laravel/Vue em `archive-laravel-vue/`
**Backup Git**: Tags `v0.1.0-laravel` e `v1.0.0-nextjs-nestjs`

---

## ✅ Checklist Final

### Após Executar Script de Arquivamento

-   [ ] Verificar estrutura: `Get-ChildItem -Recurse -Depth 1`
-   [ ] Confirmar raiz limpa (apenas nest-backend/, next-frontend/, docs/)
-   [ ] Verificar arquivo completo: `Get-ChildItem archive-laravel-vue/ -Recurse`
-   [ ] Testar Docker: `docker-compose up -d` (8 containers)
-   [ ] Testar frontend: http://localhost → Next.js app
-   [ ] Testar backend: http://localhost/api/health → {"status":"ok"}
-   [ ] Testar login completo (Next.js → Nest.js → PostgreSQL)
-   [ ] Verificar Git tags: `git tag` → v0.1.0-laravel, v1.0.0-nextjs-nestjs
-   [ ] Push final: `git push origin feat/migrate-nextjs-nestjs`
-   [ ] Criar Pull Request: feat/migrate-nextjs-nestjs → main
-   [ ] Merge to main após aprovação
-   [ ] Tag production: `git tag v1.0.0 && git push --tags`

### Documentação Atualizada

-   [ ] README.md → Next.js/Nest.js stack
-   [ ] SETUP.md → Novo setup instructions
-   [ ] DEPLOYMENT.md → Novo deployment guide
-   [ ] .gitignore → Excluir node_modules dos 2 projetos
-   [ ] docs/architecture.md → Arquitetura Next.js/Nest.js
-   [ ] nest-backend/README.md → Backend docs
-   [ ] next-frontend/README.md → Frontend docs

### Backup & Recovery

-   [ ] Backup Git completo no GitHub
-   [ ] Tag v0.1.0-laravel testado: `git checkout v0.1.0-laravel`
-   [ ] Tag v1.0.0-nextjs-nestjs testado: `git checkout v1.0.0-nextjs-nestjs`
-   [ ] Arquivo `archive-laravel-vue/` commitado e pushed
-   [ ] README no arquivo com instruções de recovery

---

## 🔄 Recuperar Código Laravel/Vue

### Opção 1: Git Tag (Recomendado)

```bash
# Ver tags disponíveis
git tag

# Checkout tag Laravel/Vue
git checkout v0.1.0-laravel

# Criar branch de desenvolvimento (se necessário)
git checkout -b laravel-maintenance

# Voltar para main Next.js/Nest.js
git checkout main
```

### Opção 2: Arquivo Local

```bash
# Código está em archive-laravel-vue/
cd archive-laravel-vue/

# Instalar dependencies
composer install    # Backend Laravel
npm install         # Frontend Vue

# Configurar .env
cp .env.example .env
php artisan key:generate

# Rodar Laravel/Vue
php artisan serve   # Backend: http://localhost:8000
npm run dev         # Frontend: http://localhost:5173
```

---

## 📊 Estatísticas de Arquivamento

### Ficheiros Movidos

```
Backend Laravel (PHP):
- app/: 45 ficheiros (~3,500 linhas)
- config/: 18 ficheiros
- database/: 15 migrations + 3 seeders
- routes/: 3 ficheiros
- Total: ~80 ficheiros PHP

Frontend Vue (JavaScript):
- resources/js/: 38 componentes (~2,800 linhas)
- resources/css/: 1 ficheiro (Tailwind)
- resources/views/: 20+ Blade templates
- Total: ~60 ficheiros Vue/JS

Tests:
- tests/Feature/: 12 ficheiros
- tests/Unit/: 1 ficheiro
- Total: 13 test files

Configs & Docker:
- docker/: 8 pastas (PHP versions)
- docker-compose.yml: 1 ficheiro
- Dockerfile: 1 ficheiro
- Total: ~50 ficheiros config

TOTAL ARQUIVADO: ~200 ficheiros Laravel/Vue (~6,300 linhas código)
```

### Tamanho

```
vendor/: ~150 MB (Composer dependencies)
node_modules/: ~200 MB (npm dependencies Vite + Vue)
storage/: ~50 MB (uploads, logs, cache)
Total Laravel/Vue: ~400 MB

Após cleanup:
Raiz (sem archive): ~100 MB (nest-backend + next-frontend)
```

---

## 🎉 Conclusão

Após executar este processo:

1. ✅ **Raiz limpa**: Apenas Next.js + Nest.js
2. ✅ **Backup seguro**: 2 tags Git (v0.1.0-laravel, v1.0.0-nextjs-nestjs)
3. ✅ **Arquivo organizado**: `archive-laravel-vue/` com README
4. ✅ **Documentação atualizada**: README, SETUP, DEPLOYMENT
5. ✅ **Migração completa**: 100% funcional em Next.js/Nest.js

**Próximos passos**:

-   Merge Pull Request → main
-   Deploy production (Vercel + AWS)
-   Monitor logs & performance
-   Celebrar! 🎉

---

**Última atualização**: 13 Nov 2024
**Autor**: [@JMSS95](https://github.com/JMSS95)
**Executar em**: Week 10+ (27-31 Jan 2025)
