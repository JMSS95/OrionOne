# Documentação OrionOne

**Sistema completo de documentação do projeto OrionOne ITSM Platform.**

---

## Índice de Documentação

### Setup & Getting Started

1. **[Setup Guide](../SETUP.md)** - Setup completo em 10 minutos (Docker-first)
2. **[Commands Reference](COMMANDS-REFERENCE.md)** - Guia completo de todos os comandos (Git, Docker, Laravel, etc)

### Arquitetura & Design

3. **[Architecture](architecture.md)** - Arquitetura do sistema (MVC + Services + Actions + Observers + Events)
4. **[Tech Stack](tech-stack.md)** - Stack tecnológica completa (Backend, Frontend, API REST, DevOps)
5. **[Database Schema](database-schema.md)** - Esquema completo da base de dados

### Desenvolvimento

6. **[Development Guide](development-guide.md)** - Guia de desenvolvimento (TDD, patterns, conventions)
7. **[Implementation Checklist](implementation-checklist.md)** - Checklist TDD sprint-by-sprint (Sprint 1 completo, Sprints 2-7 detalhados)
8. **[Components Guide](COMPONENTS-GUIDE.md)** - Guia completo dos componentes Shadcn-vue (uso + implementação)

### Tech Deep Dives

9. **[Backend Deep Dive](TECH-DEEP-DIVE-BACKEND.md)** - Laravel 12, Spatie, Actions, API REST (1,538 linhas)
10. **[Frontend Deep Dive](TECH-DEEP-DIVE-FRONTEND.md)** - Vue 3, Inertia 2.0, Shadcn-vue, VueUse (944 linhas)
11. **[Database Deep Dive](TECH-DEEP-DIVE-DATABASE.md)** - PostgreSQL 16, Views, Triggers, Redis (1,253 linhas)
12. **[DevOps Deep Dive](TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx, CI/CD, Monitoring (718 linhas)

### Análises & Planeamento

13. **[Stack Analysis 2025](STACK-ANALYSIS-2025.md)** - Análise completa da stack (Score: 8.7/10)
14. **[ITSM Stack Analysis](ITSM-STACK-ANALYSIS.md)** - Análise do mercado ITSM (Score: 8.5/10 com Sprint 7)
15. **[MVP Roadmap & Status](MVP.md)** - Roadmap completo Sprints 1-7, cronograma 32 semanas

### Business & Requirements

16. **[Business Model](business-model.md)** - Modelo de negócio, value proposition, análise SWOT
17. **[Requirements](requirements.md)** - Requisitos funcionais e não-funcionais

---

## Estrutura de Ficheiros

```
docs/
├── README.md                           # Este ficheiro (índice)
├── COMMANDS-REFERENCE.md               # Comandos completos (Git, Docker, Laravel)
├── architecture.md                     # Arquitetura do sistema
├── tech-stack.md                       # Stack tecnológica
├── database-schema.md                  # Schema completo da BD
├── development-guide.md                # Guia de desenvolvimento TDD
├── implementation-checklist.md         # Checklist sprint-by-sprint (4,965 linhas)
├── COMPONENTS-GUIDE.md                 # Componentes Shadcn-vue
├── TECH-DEEP-DIVE-BACKEND.md           # Deep dive Backend (1,538 linhas)
├── TECH-DEEP-DIVE-FRONTEND.md          # Deep dive Frontend (944 linhas)
├── TECH-DEEP-DIVE-DATABASE.md          # Deep dive Database (1,253 linhas)
├── TECH-DEEP-DIVE-DEVOPS.md            # Deep dive DevOps (718 linhas)
├── STACK-ANALYSIS-2025.md              # Análise stack (8.7/10)
├── ITSM-STACK-ANALYSIS.md              # Análise ITSM (8.5/10)
├── MVP.md                              # Roadmap completo Sprint 1-7
├── business-model.md                   # Modelo de negócio
└── requirements.md                     # Requisitos do projeto

Raiz do projeto:
├── README.md                           # README GitHub-standard
├── SETUP.md                            # Setup rápido + Docker guide
├── DEPLOYMENT.md                       # Deploy produção
└── CONTRIBUTING.md                     # Guidelines contribuição
```

---

## Quick Start

### 1. Setup Inicial (10 minutos)

Consultar **[SETUP.md](../SETUP.md)** na raiz do projeto para guia completo.

```bash
# Clone do repositório
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# Copiar .env
cp .env.example .env

# Iniciar containers Docker (6 containers)
docker-compose up -d

# Instalar dependências
docker-compose exec orionone-app composer install
docker-compose exec orionone-app npm install

# Configurar Laravel
docker-compose exec orionone-app php artisan key:generate
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan db:seed

# Dev mode (com hot reload)
docker-compose exec orionone-app npm run dev
```

**Acesso:**

-   Frontend: http://localhost:8888
-   Laravel Telescope: http://localhost:8888/telescope
-   Laravel Pulse: http://localhost:8888/pulse
-   API Docs (Scribe): http://localhost:8888/docs
-   Meilisearch: http://localhost:7700

**Credenciais de teste:**

-   Admin: admin@orionone.test / password
-   Agent: agent@orionone.test / password
-   User: user@orionone.test / password

### 2. Desenvolvimento

Seguir **[Development Guide](development-guide.md)** para:

-   Filosofia TDD (Red-Green-Refactor)
-   Padrões de código (Services, Actions, Observers)
-   Convenções de nomenclatura
-   Git workflow (Conventional Commits)

### 3. Implementar Features

Usar **[Implementation Checklist](implementation-checklist.md)** para:

-   **Sprint 1: Auth & Users** (Completo - Roles, Permissions, Profile, Avatar, Database Views/Triggers/Constraints)
-   **Sprint 2: Tickets Core** (Próximo - CRUD, Filtros, Search, API REST, Observers, Events)
-   **Sprint 3: Comments** (Colaboração, Mentions, Notifications)
-   **Sprint 4: Knowledge Base** (Articles, Categories, Full-text Search)
-   **Sprint 5: Dashboard & SLA** (Analytics, SLA tracking, Charts)
-   **Sprint 6: Teams & Automation** (Team management, Auto-assignment)
-   **Sprint 7: Asset Management** (CMDB, CSV Import/Export, Asset reports)

**Roadmap MVP:** Ver **[MVP.md](MVP.md)** para cronograma completo (32 semanas, 8.5/10 ITSM score).

---

## Guias por Público

### Para Developers

**Começar aqui:**

1. **[SETUP.md](../SETUP.md)** - Setup completo em 10 minutos
2. **[Development Guide](development-guide.md)** - Entender workflow TDD
3. **[Architecture](architecture.md)** - Compreender estrutura do código (MVC + Services + Actions)
4. **[COMPONENTS-GUIDE.md](COMPONENTS-GUIDE.md)** - Usar componentes Shadcn-vue

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

1. **[SETUP.md](../SETUP.md)** - Docker setup completo (6 containers)
2. **[DEPLOYMENT.md](../DEPLOYMENT.md)** - Deploy produção (Nginx, SSL, Supervisor, Backups)
3. **[COMMANDS-REFERENCE.md](COMMANDS-REFERENCE.md)** - Todos os comandos Docker, Laravel, Git
4. **[TECH-DEEP-DIVE-DEVOPS.md](TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx, CI/CD, Monitoring (718 linhas)

### Para Product Owners / Stakeholders

**Ler primeiro:**

1. **[Business Model](business-model.md)** - Value proposition, mercado, SWOT analysis
2. **[Requirements](requirements.md)** - Features e requisitos funcionais/não-funcionais
3. **[MVP.md](MVP.md)** - Roadmap completo Sprint 1-7, cronograma 32 semanas, ITSM score 8.5/10
4. **[ITSM Stack Analysis](ITSM-STACK-ANALYSIS.md)** - Comparativo mercado, competitive analysis

---

## Stack Técnica (8.7/10)

| Componente      | Versão | Status   |
| --------------- | ------ | -------- |
| **PHP**         | 8.4    | Produção |
| **Laravel**     | 12.x   | Produção |
| **Vue**         | 3.4    | Produção |
| **Vite**        | 6.4    | Produção |
| **PostgreSQL**  | 16     | Produção |
| **Redis**       | 7      | Produção |
| **Meilisearch** | 1.12   | Produção |
| **Pest PHP**    | 3.8    | Produção |

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
```

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

**Desenvolvedor Principal:** João Santos
**Email:** JMSS1995@hotmail.com
**GitHub:** https://github.com/JMSS95
**Repositório:** https://github.com/JMSS95/OrionOne

---

**Última Atualização:** 13 Novembro 2025
**Versão:** 2.0 (Docker-first, Stack 8.7/10)
