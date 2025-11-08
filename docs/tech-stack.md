# Tech Stack - FASE 1 (Sprint 1-2)

**Data:** 07 Novembro 2025
**Status:** INSTALADO E PRONTO

---

## Stack Essencial Instalado

### **Backend** (Composer)

#### Arquitetura Moderna

| Package                        | Versão | Propósito                                                           |
| ------------------------------ | ------ | ------------------------------------------------------------------- |
| `spatie/laravel-data`          | 4.18   | **DTOs type-safe** + validação automática                           |
| `lorisleiva/laravel-actions`   | 2.9    | **Actions reutilizáveis** (Controller/Job/Command/Listener)         |
| `spatie/laravel-query-builder` | 6.3    | **Filtros URL automáticos** (?filter[status]=open&sort=-created_at) |

#### Autenticação & Segurança

| Package                     | Versão | Propósito                            |
| --------------------------- | ------ | ------------------------------------ |
| `spatie/laravel-permission` | 6.23   | Gestão de roles e permissions (RBAC) |
| `laravel/sanctum`           | 4.0    | API authentication tokens (SPA/API)  |

#### API & Integrações

| Package/Feature     | Versão | Propósito                                      |
| ------------------- | ------ | ---------------------------------------------- |
| **Laravel API**     | 11.x   | RESTful API nativa (routes/api.php)            |
| `laravel/sanctum`   | 4.0    | Token authentication para API externa          |
| **API Resources**   | 11.x   | Transformação de dados (JsonResource)          |
| **Rate Limiting**   | 11.x   | Throttling de requests (60/min default)        |
| **CORS**            | 11.x   | Cross-origin requests (frontend/mobile)        |
| **Swagger/OpenAPI** | -      | Documentação automática API (adicionar Fase 2) |

#### Audit & Monitoring

| Package                      | Versão | Propósito                            |
| ---------------------------- | ------ | ------------------------------------ |
| `spatie/laravel-activitylog` | 4.10   | Audit trail (quem fez o quê, quando) |
| `laravel/telescope`          | 5.15   | Debug tool (dev/staging)             |

#### File Processing

| Package                      | Versão | Propósito                                       |
| ---------------------------- | ------ | ----------------------------------------------- |
| `intervention/image`         | 3.11   | Processamento de imagens (avatars, attachments) |
| `league/flysystem-aws-s3-v3` | 3.30   | Storage em AWS S3                               |
| `barryvdh/laravel-dompdf`    | 3.1    | Geração de PDFs (relatórios tickets)            |
| `maatwebsite/excel`          | 1.1    | Exportação Excel (relatórios, analytics)        |

#### Developer Experience

| Package                       | Versão | Propósito                                |
| ----------------------------- | ------ | ---------------------------------------- |
| `barryvdh/laravel-ide-helper` | 3.6    | Autocomplete perfeito (PHPStorm, VSCode) |

---

### **Frontend** (NPM)

#### UI Components (Shadcn-vue)

| Package                    | Versão | Propósito                                   |
| -------------------------- | ------ | ------------------------------------------- |
| `clsx`                     | \*     | Utility para className condicionais         |
| `tailwind-merge`           | \*     | Merge classes Tailwind sem conflitos        |
| `tailwindcss-animate`      | \*     | Animações Tailwind CSS                      |
| `class-variance-authority` | \*     | Variantes de componentes type-safe (CVA)    |
| `lucide-vue-next`          | \*     | Ícones Lucide (600+ ícones modernos)        |
| `reka-ui`                  | \*     | Primitives UI unstyled (base do Shadcn-vue) |
| `radix-vue`                | \*     | Componentes acessíveis Radix UI para Vue 3  |

**NOTA:** Shadcn-vue CLI não funciona com Vite 7. Componentes serão criados manualmente.

#### Ícones

| Package          | Versão | Propósito                             |
| ---------------- | ------ | ------------------------------------- |
| `@iconify/vue`   | \*     | 150k+ ícones (acesso a TODAS as libs) |
| `@heroicons/vue` | \*     | Ícones Heroicons (Tailwind oficial)   |

#### Forms & Validation

| Package        | Versão | Propósito                     |
| -------------- | ------ | ----------------------------- |
| `vee-validate` | \*     | Forms complexos com validação |

#### Utilities

| Package               | Versão | Propósito                                |
| --------------------- | ------ | ---------------------------------------- |
| `@vueuse/core`        | \*     | 200+ composables úteis                   |
| `@headlessui/vue`     | \*     | Componentes acessíveis (Modal, Dropdown) |
| `@inertiajs/progress` | \*     | Loading bar automático entre páginas     |

#### Charts & Rich Text

| Package            | Versão | Propósito                       |
| ------------------ | ------ | ------------------------------- |
| `chart.js`         | \*     | Gráficos para dashboard         |
| `vue-chartjs`      | \*     | Wrapper Vue para Chart.js       |
| `@vueup/vue-quill` | \*     | Editor WYSIWYG (comentários KB) |
| `marked`           | \*     | Parser Markdown → HTML          |
| `dompurify`        | \*     | Sanitização XSS                 |

---

## O Que NÃO Instalámos (e Porquê)

### Zod

**Porquê:** Laravel já tem validação nativa (FormRequest + Rules). Zod seria duplicação desnecessária e adiciona complexidade de sincronizar schemas frontend/backend.

**Alternativa:** Usar `spatie/laravel-data` no backend + Vee-Validate no frontend.

### Pest PHP

**Porquê:** Requer PHP 8.3+ mas projeto usa PHP 8.2. Conflitos de versão com PHPUnit 11.

**Alternativa:** Manter PHPUnit (já funciona bem, 100% compatível).

### @formkit/auto-animate

**Porquê:** Luxo desnecessário para MVP. Tailwind + CSS transitions são suficientes.

### @tanstack/vue-query

**Porquê:** Útil para cache de dados, mas Inertia.js já gerencia estado entre páginas. Adicionar depois (Fase 2) se necessário para otimizações.

---

## Componentes Shadcn-vue a Criar Manualmente

Como o CLI não funciona com Vite 7, vamos criar estes componentes:

### Essenciais (Sprint 1)

-   `Button.vue` - Botões (primary, secondary, outline, ghost)
-   `Input.vue` - Text inputs
-   `Card.vue` - Containers
-   `Badge.vue` - Status tags
-   `Avatar.vue` - User avatars
-   `Dropdown.vue` - Menus

### Sprint 2 (Tickets)

-   `Dialog.vue` - Modals
-   `Table.vue` - DataTable tickets
-   `Select.vue` - Dropdowns
-   `Textarea.vue` - Descrições
-   `Toast.vue` - Notifications

### Sprint 3+ (Colaboração)

-   `Tabs.vue` - Navigation tabs
-   `Accordion.vue` - FAQ/KB
-   `Command.vue` - Search palette (Cmd+K)

---

## Próximos Passos

### 1. Criar Componentes Base

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
