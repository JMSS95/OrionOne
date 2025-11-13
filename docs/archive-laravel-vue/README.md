# 📦 Archive - Laravel 12 + Vue 3 Documentation

> **Status**: Arquivado em 13 Nov 2024
> **Versão**: v0.1.0-laravel (Sprint 1 - 18% MVP)
> **Motivo**: Migração para Next.js 15 + Nest.js 10

---

## 📚 Documentos Arquivados

Esta pasta contém a documentação técnica da implementação inicial em **Laravel 12 + Vue 3 + Inertia.js**, desenvolvida durante o Sprint 1.

### Arquitetura & Stack

-   **`architecture-laravel.md`** (513 linhas)

    -   Arquitetura MVC + Service Layer + Actions
    -   Controllers, Services, Actions, Policies pattern
    -   Eloquent ORM + Observers + Repositories (opcional)
    -   Laravel best practices

-   **`tech-stack-laravel-vue.md`**
    -   Stack completa: Laravel 12, Vue 3.4, Inertia.js 2.0
    -   Dependências: Tailwind CSS, Shadcn-vue, Vite
    -   Infrastructure: PostgreSQL, Redis, Meilisearch

### Deep Dives Técnicos

-   **`TECH-DEEP-DIVE-BACKEND-LARAVEL.md`**

    -   Controllers, Services, Actions, Policies
    -   Eloquent Models, Observers, Migrations
    -   Authentication: Laravel Sanctum
    -   File uploads com Storage facade

-   **`TECH-DEEP-DIVE-FRONTEND-VUE.md`**

    -   Vue 3 Composition API
    -   Inertia.js + Server-Side Rendering
    -   Shadcn-vue components (15 componentes)
    -   Pinia stores (state management)

-   **`TECH-DEEP-DIVE-DATABASE-LARAVEL.md`**

    -   Eloquent ORM patterns
    -   Migrations & Seeders
    -   Polymorphic relationships (Media)
    -   Database triggers (opcional)

-   **`TECH-DEEP-DIVE-DEVOPS-LARAVEL.md`**
    -   Docker Compose (6 containers)
    -   Laravel Sail configuration
    -   Nginx reverse proxy
    -   Deployment strategy

### Guias de Desenvolvimento

-   **`development-guide-laravel.md`** (1410 linhas)

    -   Rotina de desenvolvimento Feature-Driven + TDD
    -   Ciclo: Planeamento → DB → Backend → Frontend → Testes
    -   Convenções Laravel (Controllers, Models, Services)
    -   Git workflow e commit messages

-   **`COMMANDS-REFERENCE-LARAVEL.md`** (1129 linhas)

    -   Git commands (branch, commit, rebase, cherry-pick)
    -   Laravel Artisan commands (make:\*, migrate, seed, queue)
    -   Composer commands (install, update, require)
    -   npm commands (install, build, dev)
    -   Docker commands (up, down, logs, exec)
    -   Testing commands (PHPUnit, Pest)

-   **`COMPONENTS-GUIDE-VUE.md`** (729 linhas)
    -   14 Shadcn-vue components (Button, Card, Input, Select, Badge, Alert, Avatar)
    -   Props e variantes de cada componente
    -   Exemplos de uso em Vue 3
    -   Tailwind CSS customizations

---

## 🔄 Migração para Next.js + Nest.js

A decisão de migrar foi tomada para:

1. **TypeScript Full-Stack**: Type-safety end-to-end
2. **Modern Stack**: Next.js 15 App Router, Nest.js 10
3. **Performance**: React Server Components, API otimizada
4. **Ecosystem**: npm packages mais recentes, melhor DX

### Documentos de Migração (docs/)

-   `MIGRATION-PART-1-SETUP.md` - Infrastructure & packages
-   `MIGRATION-PART-2-BACKEND.md` - Nest.js + Prisma
-   `MIGRATION-PART-3-FRONTEND.md` - Next.js + React
-   `MIGRATION-PART-4-TIMELINE.md` - 10-week plan
-   `MIGRATION-REVIEW-GAPS.md` - 17 gaps analysis
-   `MIGRATION-READY.md` - Executive summary

---

## 💾 Backup Git

```bash
# Tag de backup criado
git tag v0.1.0-laravel

# Para recuperar este código Laravel/Vue
git checkout v0.1.0-laravel
```

---

## 📊 Sprint 1 - Estado Final

**Progresso**: 18% do MVP
**Features completas**: 7 de 39
**Commit**: aed9b08 (13 Nov 2024)

### Features Implementadas (Laravel/Vue)

1. ✅ Authentication (Sanctum) - Login, Register, Password Reset
2. ✅ User Management - CRUD básico
3. ✅ Roles & Permissions - CASL integration
4. ✅ Dashboard - Overview cards
5. ✅ Teams - Basic structure
6. ✅ Settings - User profile
7. ✅ File Uploads - Avatar + polymorphic Media

### Código Base

-   **Backend**: 45 arquivos PHP (~3,500 linhas)

    -   Controllers: 8 arquivos
    -   Services: 5 arquivos
    -   Actions: 3 arquivos
    -   Models: 12 arquivos
    -   Migrations: 15 arquivos

-   **Frontend**: 38 componentes Vue (~2,800 linhas)
    -   Pages: 12 arquivos
    -   Components: 15 Shadcn-vue + 11 custom
    -   Composables: 4 arquivos

---

## 🎯 Lições Aprendidas

### O Que Funcionou Bem

-   **Laravel Conventions**: Scaffolding rápido
-   **Inertia.js**: SPA sem API REST complexity
-   **Shadcn-vue**: UI components prontos
-   **Docker**: Ambiente consistente

### Desafios Encontrados

-   **TypeScript**: Vue 3 + TS ainda não ideal
-   **SSR**: Inertia.js SSR experimental
-   **Ecosystem**: Alguns packages desatualizados
-   **Performance**: Hydration issues em produção

### Por Isso Migramos para Next.js + Nest.js

✅ TypeScript First-Class
✅ React Ecosystem Maduro
✅ Next.js 15 App Router (RSC)
✅ Nest.js Modular Architecture
✅ Prisma Type-Safe ORM
✅ Better DX & Tooling

---

## 📝 Notas de Desenvolvimento

-   Esta documentação deve ser consultada apenas como **referência histórica**
-   O código Laravel/Vue está **congelado** no tag v0.1.0-laravel
-   **Não fazer** novos desenvolvimentos nesta stack
-   Para features futuras, usar a **nova stack Next.js + Nest.js**

---

**Última atualização**: 13 Nov 2024
**Mantido por**: [@JMSS95](https://github.com/JMSS95)
