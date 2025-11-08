# Documentação OrionOne

**Sistema completo de documentação do projeto OrionOne ITSM Platform.**

---

## Índice de Documentação

### Setup & Getting Started

1. **[Commands Reference](COMMANDS-REFERENCE.md)** - Guia completo de todos os comandos (Git, Docker, Laravel, etc)
2. **[Docker Guide](DOCKER-GUIDE.md)** - Guia Docker para iniciantes
3. **[Setup Changelog](SETUP-CHANGELOG.md)** - Histórico completo de configuração do projeto

### Arquitetura & Design

4. **[Architecture](architecture.md)** - Arquitetura do sistema (Clean Architecture, CQRS, DDD)
5. **[Tech Stack](tech-stack.md)** - Stack tecnológica completa (Backend, Frontend, DevOps)
6. **[Database Schema](database-schema.md)** - Esquema completo da base de dados

### Desenvolvimento

7. **[Development Guide](development-guide.md)** - Guia de desenvolvimento (TDD, patterns, conventions)
8. **[Development Planning](development-planning.md)** - Planeamento de desenvolvimento (sprints, cronograma)
9. **[Implementation Checklist](implementation-checklist.md)** - Checklist TDD sprint-by-sprint

### Componentes UI

10. **[Components Guide](COMPONENTS-GUIDE.md)** - Guia de uso dos componentes Shadcn-vue
11. **[Components Summary](COMPONENTS-SUMMARY.md)** - Resumo da implementação dos componentes

### Business & Requirements

12. **[Business Model](business-model.md)** - Modelo de negócio, value proposition, análise SWOT
13. **[Requirements](requirements.md)** - Requisitos funcionais e não-funcionais

---

## Estrutura de Ficheiros

```
docs/
├── README.md                      # Este ficheiro (índice)
├── COMMANDS-REFERENCE.md          # Comandos completos
├── DOCKER-GUIDE.md                # Docker para iniciantes
├── SETUP-CHANGELOG.md             # Histórico de setup
├── architecture.md                # Arquitetura do sistema
├── tech-stack.md                  # Stack tecnológica
├── database-schema.md             # Schema da BD
├── development-guide.md           # Guia de desenvolvimento
├── development-planning.md        # Planeamento e sprints
├── implementation-checklist.md    # Checklist TDD
├── COMPONENTS-GUIDE.md            # Componentes UI (guia de uso)
├── COMPONENTS-SUMMARY.md          # Componentes UI (resumo)
├── business-model.md              # Modelo de negócio
└── requirements.md                # Requisitos do projeto
```

---

## Quick Start

### 1. Setup Inicial

Consultar **[Commands Reference](COMMANDS-REFERENCE.md)** para comandos completos.

```bash
# Clone do repositório
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# Iniciar containers Docker
docker-compose up -d

# Instalar dependências
docker-compose exec orionone-app composer install
docker-compose exec orionone-frontend npm install

# Configurar ambiente
cp .env.example .env
php artisan key:generate

# Executar migrations e seeders
php artisan migrate:fresh --seed

# Aceder à aplicação
http://localhost:8888
```

### 2. Desenvolvimento

Seguir **[Development Guide](development-guide.md)** para:
- Filosofia TDD (Red-Green-Refactor)
- Padrões de código
- Convenções de nomenclatura
- Git workflow

### 3. Implementar Features

Usar **[Implementation Checklist](implementation-checklist.md)** para:
- Sprint 1: Auth & Users
- Sprint 2: Tickets Core
- Sprint 3: Colaboração
- Sprint 4: Knowledge Base
- Sprint 5: Dashboard & Reports
- Sprint 6: Polish & Deploy

---

## Guias por Público

### Para Developers

**Começar aqui:**
1. [Commands Reference](COMMANDS-REFERENCE.md) - Memorizar comandos essenciais
2. [Development Guide](development-guide.md) - Entender workflow TDD
3. [Architecture](architecture.md) - Compreender estrutura do código
4. [Components Guide](COMPONENTS-GUIDE.md) - Usar componentes UI

**Workflow diário:**
```bash
# 1. Pull latest changes
git pull origin main

# 2. Criar feature branch
git checkout -b feature/ticket-filters

# 3. Escrever teste (RED)
php artisan make:test TicketFilterTest

# 4. Implementar (GREEN)
# ... código ...

# 5. Refatorar
# ... melhorias ...

# 6. Commit
git add .
git commit -m "feat: add ticket filters"
git push origin feature/ticket-filters

# 7. Criar PR no GitHub
```

### Para DevOps

**Focar em:**
1. [Docker Guide](DOCKER-GUIDE.md) - Gestão de containers
2. [Commands Reference](COMMANDS-REFERENCE.md) - Secção Docker e deployment
3. [Tech Stack](tech-stack.md) - Infraestrutura completa

### Para Product Owners / Stakeholders

**Ler primeiro:**
1. [Business Model](business-model.md) - Value proposition, mercado
2. [Requirements](requirements.md) - Features e requisitos
3. [Development Planning](development-planning.md) - Cronograma e sprints

---

## Convenções de Documentação

### Formato

- **Markdown** (`.md`)
- UTF-8 encoding
- Line breaks: Unix (LF)
- Max line length: 120 caracteres (soft limit)

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
# Shell commands
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

- [ ] Documento segue estrutura padrão
- [ ] Links internos funcionam
- [ ] Code blocks têm linguagem especificada
- [ ] Sem erros ortográficos
- [ ] Adicionado ao índice (`docs/README.md`)
- [ ] Data de atualização presente

---

## Manutenção

### Review Periódico

**Mensalmente:**
- Atualizar `SETUP-CHANGELOG.md` com mudanças
- Verificar links quebrados
- Atualizar versões de packages em `tech-stack.md`

**Trimestralmente:**
- Atualizar `business-model.md` com métricas reais
- Revisar `requirements.md` com feedback de users
- Atualizar `development-planning.md` com roadmap

---

## Contactos

**Desenvolvedor Principal:** João Santos (@JMSS95)
**Repositório:** https://github.com/JMSS95/OrionOne
**Documentação Online:** (TBD)

---

**Última Atualização:** 08 Novembro 2025
**Versão:** 1.0
