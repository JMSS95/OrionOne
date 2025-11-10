# Documentação OrionOne

**Sistema completo de documentação do projeto OrionOne ITSM Platform.**

---

## Índice de Documentação

### 🚀 Setup & Getting Started

1. **[Quick Start](QUICK-START.md)** - Setup completo em 10 minutos (Docker-first)
2. **[Commands Reference](COMMANDS-REFERENCE.md)** - Guia completo de todos os comandos (Git, Docker, Laravel, etc)
3. **[Docker Guide](DOCKER-GUIDE.md)** - Guia Docker para iniciantes
4. **[Documentation Cleanup](DOCUMENTATION-CLEANUP.md)** - Análise e remoção de documentação redundante

### 🏗️ Arquitetura & Design

5. **[Architecture](architecture.md)** - Arquitetura do sistema (MVC + Services + Actions + Observers + Events)
6. **[Tech Stack](tech-stack.md)** - Stack tecnológica completa (Backend, Frontend, **API REST**, DevOps)
7. **[Database Schema](database-schema.md)** - Esquema completo da base de dados

### 💻 Desenvolvimento

8. **[Development Guide](development-guide.md)** - Guia de desenvolvimento (TDD, patterns, conventions)
9. **[Implementation Checklist](implementation-checklist.md)** - Checklist TDD sprint-by-sprint (**Sprints 1-2 completos: Auth, Tickets, API REST, Observers, Events**)
10. **[Components Guide](COMPONENTS-GUIDE.md)** - Guia completo dos componentes Shadcn-vue (uso + implementação)

### 📊 Análises & Planeamento

11. **[Stack Analysis 2025](STACK-ANALYSIS-2025.md)** - Análise completa da stack (Score: 8.7/10)
12. **[ITSM Stack Analysis](ITSM-STACK-ANALYSIS.md)** - Análise do mercado ITSM (Score: 7.2/10)
13. **[MVP Priorities](MVP-PRIORITIES.md)** - Roadmap Sprint 2-6 e prioridades MVP
14. **[MVP Readiness Checklist](MVP-READINESS-CHECKLIST.md)** - Estado MVP (95% pronto)

### 📝 Business & Requirements

15. **[Business Model](business-model.md)** - Modelo de negócio, value proposition, análise SWOT
16. **[Requirements](requirements.md)** - Requisitos funcionais e não-funcionais

---

## Estrutura de Ficheiros

```
docs/
├── README.md                           # Este ficheiro (índice)
├── QUICK-START.md                      # ⭐ Setup em 10 minutos
├── COMMANDS-REFERENCE.md               # Comandos completos
├── DOCKER-GUIDE.md                     # Docker para iniciantes
├── DOCUMENTATION-CLEANUP.md            # Análise de redundâncias
├── architecture.md                     # Arquitetura do sistema
├── tech-stack.md                       # Stack tecnológica
├── database-schema.md                  # Schema da BD
├── development-guide.md                # Guia de desenvolvimento
├── implementation-checklist.md         # Checklist TDD
├── COMPONENTS-GUIDE.md                 # Componentes UI (completo)
├── STACK-ANALYSIS-2025.md              # Análise stack (8.7/10)
├── ITSM-STACK-ANALYSIS.md              # Análise ITSM (7.2/10)
├── MVP-PRIORITIES.md                   # Roadmap Sprint 2-6
├── MVP-READINESS-CHECKLIST.md          # Estado MVP (95%)
├── business-model.md                   # Modelo de negócio
└── requirements.md                     # Requisitos do projeto
```

---

## Quick Start

### 1. Setup Inicial (10 minutos)

**👉 Consultar [QUICK-START.md](QUICK-START.md) para guia completo.**

```bash
# Clone do repositório
git clone https://github.com/JMSS/OrionOne.git
cd OrionOne

# Copiar .env
cp .env.example .env

# Iniciar containers Docker (6 containers)
docker-compose up -d

# Instalar dependências
docker-compose exec orionone-app composer install
docker-compose exec orionone-frontend npm install --legacy-peer-deps

# Configurar Laravel
docker-compose exec orionone-app php artisan key:generate
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan db:seed --class=RolePermissionSeeder

# Dev mode
docker-compose exec orionone-frontend npm run dev
```

**Acesso:**
- 🌐 Frontend: http://localhost
- 📊 Pulse: http://localhost/pulse
- 📚 API Docs: http://localhost/docs
- 🔍 Meilisearch: http://localhost:7700

### 2. Desenvolvimento

Seguir **[Development Guide](development-guide.md)** para:

-   Filosofia TDD (Red-Green-Refactor)
-   Padrões de código
-   Convenções de nomenclatura
-   Git workflow

### 3. Implementar Features

Usar **[Implementation Checklist](implementation-checklist.md)** para:

-   **Sprint 1: Auth & Users** (Completo - Roles, Permissions, Avatar Upload)
-   **Sprint 2: Tickets Core** (Próximo - CRUD, Filtros, API REST, Observers, Events)
-   Sprint 3: Colaboração (Comments, Mentions, Notifications)
-   Sprint 4: Knowledge Base (Articles, Categories, Search)
-   Sprint 5: Dashboard & Reports (Analytics, KPIs)
-   Sprint 6: Polish & Deploy (CI/CD, Performance)

**Roadmap MVP:** Ver [MVP-PRIORITIES.md](MVP-PRIORITIES.md) para prioridades Sprint 2-6.

---

## Guias por Público

### Para Developers

**Começar aqui:**

1. [QUICK-START.md](QUICK-START.md) - Setup em 10 minutos
2. [Development Guide](development-guide.md) - Entender workflow TDD
3. [Architecture](architecture.md) - Compreender estrutura do código
4. [COMPONENTS-GUIDE.md](COMPONENTS-GUIDE.md) - Usar componentes UI

**Workflow diário:**

```bash
# 1. Pull latest changes
git pull origin main

# 2. Criar feature branch
git checkout -b feature/ticket-filters

# 3. Escrever teste (RED)
docker-compose exec orionone-app php artisan make:test TicketFilterTest

# 4. Implementar (GREEN)
# ... código ...

# 5. Refatorar
# ... melhorias ...

# ... melhorias ...

# 6. Rodar testes (Pest PHP)
docker-compose exec orionone-app php artisan test

# 7. Commit
git add .
git commit -m "feat: add ticket filters"
git push origin feature/ticket-filters
```

### Para DevOps

**Focar em:**

1. [DOCKER-GUIDE.md](DOCKER-GUIDE.md) - Gestão de containers
2. [COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md) - Secção Docker e deployment
3. [tech-stack.md](tech-stack.md) - Infraestrutura completa

### Para Product Owners / Stakeholders

**Ler primeiro:**

1. [business-model.md](business-model.md) - Value proposition, mercado
2. [requirements.md](requirements.md) - Features e requisitos
3. [MVP-PRIORITIES.md](MVP-PRIORITIES.md) - Roadmap Sprint 2-6
4. [MVP-READINESS-CHECKLIST.md](MVP-READINESS-CHECKLIST.md) - Estado atual (95%)

---

## Stack Técnica (8.7/10)

| Componente      | Versão       | Status      |
| --------------- | ------------ | ----------- |
| **PHP**         | 8.4          | ✅ Produção |
| **Laravel**     | 12.x         | ✅ Produção |
| **Vue**         | 3.4          | ✅ Produção |
| **Vite**        | 6.4          | ✅ Produção |
| **PostgreSQL**  | 16           | ✅ Produção |
| **Redis**       | 7            | ✅ Produção |
| **Meilisearch** | 1.12         | ✅ Produção |
| **Pest PHP**    | 3.8          | ✅ Produção |

**Análise completa:** [STACK-ANALYSIS-2025.md](STACK-ANALYSIS-2025.md)

---

## Convenções de Documentação

### Formato

-   **Markdown** (`.md`)
-   UTF-8 encoding
-   Line breaks: Unix (LF)
-   Max line length: 120 caracteres (soft limit)

### Estrutura de Documento

```markdown
# Título Principal

**Resumo breve do documento.**

---

## Secção 1
````

### Para DevOps

**Focar em:**

1. [Docker Guide](docker-guide.md) - Gestão de containers
2. [Commands Reference](commands-reference.md) - Secção Docker e deployment
3. [Tech Stack](tech-stack.md) - Infraestrutura completa

### Para Product Owners / Stakeholders

**Ler primeiro:**

1. [Business Model](business-model.md) - Value proposition, mercado
2. [Requirements](requirements.md) - Features e requisitos
3. [Development Planning](development-planning.md) - Cronograma e sprints

---

## Convenções de Documentação

### Formato

-   **Markdown** (`.md`)
-   UTF-8 encoding
-   Line breaks: Unix (LF)
-   Max line length: 120 caracteres (soft limit)

### Estrutura de Documento

```markdown
# Título Principal

**Resumo breve do documento.**

---

## Secção 1

Conteúdo...

### Subsecção 1.1

Conteúdo...

---

## Secção 2

...
```

### Code Blocks

Sempre especificar linguagem:

````markdown
```php
// PHP code
```

```bash
# Shell commands (Docker-first)
docker-compose exec orionone-app php artisan ...
```

```vue
<!-- Vue components -->
```
````

### Links Internos

Usar paths relativos:

```markdown
Ver [Development Guide](development-guide.md) para detalhes.
```

---

## Contribuir para Documentação

### Atualizar Documentação

```bash
# 1. Editar ficheiro
vim docs/development-guide.md

# 2. Verificar ortografia (opcional)
# Usar VS Code spell checker

# 3. Commit
git add docs/development-guide.md
git commit -m "docs: update development guide with new patterns"
```

### Criar Novo Documento

1. Criar ficheiro em `docs/`
2. Adicionar ao índice em `docs/README.md`
3. Seguir estrutura padrão
4. Commit com mensagem `docs: add [document-name]`

### Checklist para PRs de Documentação

-   [ ] Documento segue estrutura padrão
-   [ ] Links internos funcionam
-   [ ] Code blocks têm linguagem especificada
-   [ ] Sem erros ortográficos
-   [ ] Adicionado ao índice (`docs/README.md`)
-   [ ] Data de atualização presente
-   [ ] Comandos usam Docker (docker-compose exec)

---

## Manutenção

### Review Periódico

**Mensalmente:**

-   Atualizar stack versions em `tech-stack.md`
-   Verificar links quebrados
-   Remover documentação obsoleta

**Trimestralmente:**

-   Atualizar `business-model.md` com métricas reais
-   Revisar `requirements.md` com feedback de users
-   Atualizar `MVP-PRIORITIES.md` com roadmap

---

## Contactos

**Desenvolvedor Principal:** João Santos (@JMSS)
**Repositório:** https://github.com/JMSS/OrionOne
**Documentação Online:** (TBD)

---

**Última Atualização:** 10 Novembro 2025, 06:00
**Versão:** 2.0 (Docker-first, Stack 8.7/10)
