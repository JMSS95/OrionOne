# Tech Stack - OrionOne ITSM

**Data:** 10 Novembro 2025
**Status:** ✅ STACK COMPLETO E MODERNIZADO (Score: 8.7/10)

---

## Stack Essencial Instalado

### **Backend** (Composer)

#### Arquitetura Moderna

| Package                        | Versão | Status | Propósito                                                           |
| ------------------------------ | ------ | ------ | ------------------------------------------------------------------- |
| `spatie/laravel-data`          | 4.18   | ✅     | **DTOs type-safe** + validação automática                           |
| `lorisleiva/laravel-actions`   | 2.9    | ✅     | **Actions reutilizáveis** (Controller/Job/Command/Listener)         |
| `spatie/laravel-query-builder` | 6.3    | ✅     | **Filtros URL automáticos** (?filter[status]=open&sort=-created_at) |

#### Autenticação & Segurança

| Package                     | Versão | Status | Propósito                            |
| --------------------------- | ------ | ------ | ------------------------------------ |
| `spatie/laravel-permission` | 6.23   | ✅     | Gestão de roles e permissions (RBAC) |
| `laravel/sanctum`           | 4.0    | ✅     | API authentication tokens (SPA/API)  |

#### API & Integrações

| Package/Feature        | Versão | Status | Propósito                               |
| ---------------------- | ------ | ------ | --------------------------------------- |
| **Laravel API**        | 12.x   | ✅     | RESTful API nativa (routes/api.php)     |
| `laravel/sanctum`      | 4.0    | ✅     | Token authentication para API externa   |
| **API Resources**      | 12.x   | ✅     | Transformação de dados (JsonResource)   |
| **Rate Limiting**      | 12.x   | ✅     | Throttling de requests (60/min default) |
| **CORS**               | 12.x   | ✅     | Cross-origin requests (frontend/mobile) |
| `knuckleswtf/scribe`   | 5.5    | ✅     | Documentação automática API (OpenAPI)   |
| **Swagger/L5-Swagger** | -      | ❌     | **REMOVIDO** (substituído por Scribe)   |

#### Audit & Monitoring

| Package                      | Versão | Status | Propósito                                   |
| ---------------------------- | ------ | ------ | ------------------------------------------- |
| `spatie/laravel-activitylog` | 4.10   | ✅     | Audit trail (quem fez o quê, quando)        |
| `laravel/telescope`          | 5.15   | ✅     | Debug tool (dev/staging)                    |
| `laravel/pulse`              | 1.4    | ✅     | **Real-time monitoring** (dashboard /pulse) |

#### Search & Indexing

| Package                        | Versão | Status | Propósito                     |
| ------------------------------ | ------ | ------ | ----------------------------- |
| `laravel/scout`                | 10.21  | ✅     | Search abstraction layer      |
| `meilisearch/meilisearch-php`  | 1.16   | ✅     | AI-powered search client (KB) |
| **Meilisearch Docker Service** | 1.12   | ✅     | Search engine (porta 7700)    |

#### File Processing

| Package                      | Versão | Status | Propósito                               |
| ---------------------------- | ------ | ------ | --------------------------------------- |
| `intervention/image`         | -      | ❌     | **REMOVIDO** (não usado)                |
| `league/flysystem-aws-s3-v3` | 3.30   | ⚠️     | Storage AWS S3 (manter para futuro)     |
| `barryvdh/laravel-dompdf`    | -      | ❌     | **REMOVIDO** (não usado)                |
| `maatwebsite/excel`          | 1.1    | ⚠️     | Exportação Excel (manter para Sprint 6) |

#### Testing

| Package                       | Versão | Status | Propósito                      |
| ----------------------------- | ------ | ------ | ------------------------------ |
| `pestphp/pest`                | 3.8    | ✅     | **Modern testing framework**   |
| `pestphp/pest-plugin-laravel` | 3.2    | ✅     | Laravel integration for Pest   |
| `phpunit/phpunit`             | 11.5   | ✅     | Base testing (usado pelo Pest) |

#### Developer Experience

| Package                       | Versão | Status | Propósito                                |
| ----------------------------- | ------ | ------ | ---------------------------------------- |
| `barryvdh/laravel-ide-helper` | 3.6    | ✅     | Autocomplete perfeito (PHPStorm, VSCode) |
| `barryvdh/laravel-debugbar`   | 3.16   | ✅     | Debug toolbar (dev)                      |
| `laravel/pint`                | 1.24   | ✅     | Code style fixer                         |
| `larastan/larastan`           | 3.8    | ✅     | PHPStan for Laravel (static analysis)    |

---

### **Frontend** (NPM)

#### Core Framework

| Package              | Versão | Status | Propósito                        |
| -------------------- | ------ | ------ | -------------------------------- |
| `vue`                | 3.4    | ✅     | Framework reativo                |
| `@inertiajs/vue3`    | 2.0    | ✅     | SSR simplificado (sem API REST)  |
| `vite`               | 6.4    | ✅     | Build tool (downgrade do 7.0 RC) |
| `@vitejs/plugin-vue` | 5.x    | ✅     | Plugin Vite para Vue 3           |

#### UI Components (Shadcn-vue)

| Package                    | Versão | Status | Propósito                                  |
| -------------------------- | ------ | ------ | ------------------------------------------ |
| `clsx`                     | \*     | ✅     | Utility para className condicionais        |
| `tailwind-merge`           | \*     | ✅     | Merge classes Tailwind sem conflitos       |
| `tailwindcss-animate`      | \*     | ✅     | Animações Tailwind CSS                     |
| `class-variance-authority` | \*     | ✅     | Variantes de componentes type-safe (CVA)   |
| `lucide-vue-next`          | \*     | ✅     | Ícones Lucide (600+ ícones modernos)       |
| `radix-vue`                | \*     | ✅     | Componentes acessíveis Radix UI para Vue 3 |

#### Ícones

| Package           | Versão | Status | Propósito                             |
| ----------------- | ------ | ------ | ------------------------------------- |
| `lucide-vue-next` | \*     | ✅     | Ícones principais (600+ modernos)     |
| `@iconify/vue`    | -      | ❌     | **REMOVIDO** (não usado)              |
| `@heroicons/vue`  | -      | ❌     | **REMOVIDO** (substituído por Lucide) |

#### Forms & Validation

| Package        | Versão | Status | Propósito                     |
| -------------- | ------ | ------ | ----------------------------- |
| `vee-validate` | \*     | ✅     | Forms complexos com validação |
| `zod`          | \*     | ✅     | Schema validation (frontend)  |

#### Utilities

| Package               | Versão | Status | Propósito                                 |
| --------------------- | ------ | ------ | ----------------------------------------- |
| `@vueuse/core`        | 11.3   | ✅     | 200+ composables úteis (versão corrigida) |
| `@headlessui/vue`     | -      | ❌     | **REMOVIDO** (usando Radix-vue)           |
| `@inertiajs/progress` | \*     | ✅     | Loading bar automático entre páginas      |

#### Charts & Rich Text

| Package            | Versão | Status | Propósito                       |
| ------------------ | ------ | ------ | ------------------------------- |
| `chart.js`         | \*     | ✅     | Gráficos para dashboard         |
| `vue-chartjs`      | \*     | ✅     | Wrapper Vue para Chart.js       |
| `@vueup/vue-quill` | \*     | ✅     | Editor WYSIWYG (comentários KB) |
| `marked`           | \*     | ✅     | Parser Markdown → HTML          |
| `dompurify`        | \*     | ✅     | Sanitização XSS                 |

---

## Infraestrutura (Docker)

### Serviços Docker Configurados

| Serviço                | Imagem             | Porta | Status | Propósito                     |
| ---------------------- | ------------------ | ----- | ------ | ----------------------------- |
| `orionone-app`         | php:8.4-fpm-alpine | -     | ✅     | Laravel application (PHP 8.4) |
| `orionone-frontend`    | node:20-alpine     | -     | ✅     | Vite dev server (HMR)         |
| `orionone-db`          | postgres:16-alpine | 5432  | ✅     | PostgreSQL database           |
| `orionone-redis`       | redis:7-alpine     | 6379  | ✅     | Cache + Queue backend         |
| `orionone-meilisearch` | meilisearch:1.12   | 7700  | ✅     | AI-powered search engine      |
| `orionone-nginx`       | nginx:alpine       | 80    | ✅     | Web server + reverse proxy    |

### Volumes Persistentes

-   `orionone_pgdata` - Dados PostgreSQL
-   `orionone_redisdata` - Dados Redis
-   `orionone_meilisearch` - Índices Meilisearch

---

## O Que NÃO Instalámos (e Porquê)

### ❌ Removido da Stack Inicial

#### Intervention/Image

**Porquê:** Não estava sendo usado no projeto. Adicionar apenas quando implementar upload de avatares/anexos.

#### Barryvdh/Laravel-DomPDF

**Porquê:** Não estava sendo usado. Adicionar apenas quando necessário gerar PDFs.

#### @iconify/vue & @heroicons/vue

**Porquê:** Redundante. Lucide-vue-next fornece todos os ícones necessários.

#### @headlessui/vue

**Porquê:** Substituído por Radix-vue (melhor integração com Shadcn-vue).

#### L5-Swagger (darkaonline/l5-swagger)

**Porquê:** Substituído por Scribe 5.5 (melhor DX, auto-discovery, OpenAPI 3.0).

---

### ⚠️ Mantido Mas Não Usado Ainda

#### league/flysystem-aws-s3-v3

**Status:** Mantido para implementação futura de storage S3.
**Quando usar:** Sprint 5-6 (upload de attachments para produção).

#### maatwebsite/excel

**Status:** Mantido para exportação de relatórios.
**Quando usar:** Sprint 6 (feature de exportar tickets/analytics para Excel).

---

### 🔴 Decidimos NÃO Usar

### Zod (no Backend)

**Porquê:** Laravel já tem validação nativa (FormRequest + Rules). Zod seria duplicação desnecessária.

**Alternativa:**

-   Backend: `spatie/laravel-data` + Laravel FormRequests
-   Frontend: Zod + Vee-Validate (já instalado)

### Pest PHP (Inicialmente)

**Status Anterior:** Não instalado (requer PHP 8.3+, projeto usava PHP 8.2)

**Status Atual:** ✅ **INSTALADO** (Pest 3.8 + PHP 8.4 upgrade completo)

**Quando:** Stack Analysis 2025 - upgrade completo de PHP 8.2 → 8.4

### @formkit/auto-animate

**Porquê:** Luxo desnecessário para MVP. Tailwind + CSS transitions são suficientes.

**Reavaliar:** Post-MVP se necessário para UX premium.

### @tanstack/vue-query

**Porquê:** Útil para cache de dados, mas Inertia.js já gerencia estado entre páginas.

**Quando adicionar:** Sprint 5-6 se necessário para otimizações de performance.

### Laravel Horizon

**Porquê:** Requer ext-pcntl (Linux only), não funciona no Windows.

**Alternativa:** Laravel Queue + Laravel Pulse (monitoring real-time já instalado).

**Reavaliar:** Apenas para deploy em produção Linux/Docker.

---

## Stack Score Final

Após implementação completa das melhorias do Stack Analysis 2025:

| Categoria         | Score      | Status                       |
| ----------------- | ---------- | ---------------------------- |
| Backend Core      | 9/10       | ✅ Excelente (PHP 8.4)       |
| Backend Packages  | 9/10       | ✅ Excelente (Scribe+Pulse)  |
| Frontend Core     | 9/10       | ✅ Excelente (Vite 6 stable) |
| Frontend Packages | 8.5/10     | ✅ Muito Bom                 |
| Infrastructure    | 9/10       | ✅ Excelente (+Meilisearch)  |
| Testing           | 9/10       | ✅ Excelente (Pest PHP)      |
| Monitoring        | 9/10       | ✅ Excelente (Pulse)         |
| Security          | 8/10       | ✅ Bom                       |
| Performance       | 9/10       | ✅ Excelente (PHP 8.4)       |
| DX (Dev Exp)      | 9/10       | ✅ Excelente                 |
| **MÉDIA GERAL**   | **8.7/10** | ✅ **EXCELENTE**             |

---

## Stack Melhorias Implementadas

### ✅ Completado (Stack Analysis 2025)

1. **PHP 8.4 Upgrade** - Performance boost + property hooks
2. **Pest PHP 3.8** - Modern BDD-style testing
3. **Scribe 5.5** - Substituiu L5-Swagger (melhor DX)
4. **Laravel Pulse 1.4** - Real-time monitoring dashboard
5. **Meilisearch + Scout** - AI-powered search para KB
6. **Vite 6.4** - Downgrade do RC 7.0 para stable
7. **VueUse 11.3** - Fix de versão incompatível
8. **Removido 20 pacotes** - Projeto mais limpo e rápido

### 🟡 Opcional (Post-MVP)

-   **Laravel Horizon** - Queue monitoring (apenas produção Linux)
-   **Spatie Backup** - Backups automáticos
-   **Laravel Socialite** - SSO (Google, Microsoft)
-   **Intervention/Image** - Quando adicionar uploads
-   **DomPDF** - Quando necessário gerar PDFs

---

## Próximos Passos

### Essenciais (Sprint 1-2)

-   ✅ `Button.vue` - Botões (primary, secondary, outline, ghost)
-   ✅ `Input.vue` - Text inputs
-   ✅ `Card.vue` - Containers
-   ✅ `Badge.vue` - Status tags
-   ✅ `Avatar.vue` - User avatars
-   ⏳ `Dropdown.vue` - Menus (criar em Sprint 2)

### Sprint 2-3 (Tickets)

-   `Dialog.vue` - Modals
-   `Table.vue` - DataTable tickets
-   `Select.vue` - Dropdowns
-   `Textarea.vue` - Descrições
-   `Toast.vue` - Notifications

### Sprint 4-5 (Colaboração)

-   `Tabs.vue` - Navigation tabs
-   `Accordion.vue` - FAQ/KB
-   `Command.vue` - Search palette (Cmd+K)

---

## Configurações Pendentes (Sprint 2)

### 1. Setup Vee-Validate

Criar composable global para forms.

### 2. Configurar Spatie Packages

Publicar configs e executar migrations.

Ver [Commands Reference](COMMANDS-REFERENCE.md#laravel-artisan-commands) para comandos.

### 3. Criar Seeder

Roles, permissions, utilizadores teste.

Ver [Implementation Checklist](implementation-checklist.md) para instruções TDD.

### 4. Configurar Meilisearch

```bash
# Iniciar serviço Docker
docker-compose up -d orionone-meilisearch

# Configurar índice para Articles (KB)
php artisan scout:import "App\Models\Article"
```

---

## Referências

-   [Stack Analysis 2025](STACK-ANALYSIS-2025.md) - Análise completa e score 8.7/10
-   [ITSM Stack Analysis](ITSM-STACK-ANALYSIS.md) - Validação para mercado ITSM (8.5/10)
-   [Implementation Checklist](implementation-checklist.md) - Roadmap detalhado Sprint 1-6
-   [Commands Reference](COMMANDS-REFERENCE.md) - Comandos úteis do projeto

---

**Última Atualização:** 10 Novembro 2025, 04:15
**Status:** ✅ **STACK 100% MODERNIZADO E PRONTO PARA MVP**

---

## Próximos Passos (Sprint 2)

### Componentes Shadcn-vue a Criar Manualmente

Como o CLI não funciona com Vite 6, vamos criar estes componentes:

### Essenciais (Sprint 1)

Criar estrutura em `resources/js/components/ui/` e `resources/js/lib/`.

Ver [Commands Reference](COMMANDS-REFERENCE.md) para comandos específicos.

### 2. Setup Vee-Validate

Criar composable global para forms.

### 3. Configurar Spatie Packages

Publicar configs e executar migrations.

Ver [Commands Reference](COMMANDS-REFERENCE.md#laravel-artisan-commands) para comandos.

### 4. Criar Seeder

Roles, permissions, utilizadores teste.

Ver [Implementation Checklist](implementation-checklist.md) para instruções TDD.

---

## Stack Fases Futuras

### FASE 2 (Sprint 3-4) - Otimizações

-   @tanstack/vue-query (se necessário)
-   Laravel Pulse (monitoring)

### FASE 3 (Sprint 6) - Produção

-   spatie/laravel-backup
-   Laravel Horizon (queues)
-   GitHub Actions CI/CD

---

**Última Atualização:** 07 Novembro 2025, 23:50
