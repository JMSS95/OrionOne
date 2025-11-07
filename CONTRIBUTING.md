# Guia de Contribuição - OrionOne

## Visão Geral

Este documento descreve as convenções e boas práticas para contribuir com o projeto OrionOne. Como projeto académico, seguimos standards profissionais da indústria.

---

## Workflow de Desenvolvimento

### 1. Criar uma Nova Feature

```powershell
# Use o script de scaffolding
.\scripts\feature.ps1 NomeDaFeature

# Exemplo: Para criar feature de Tickets
.\scripts\feature.ps1 Ticket
```

Isto irá gerar:

- Migration (`create_tickets_table`)
- Model + Factory + Seeder (`Ticket.php`)
- Controller (`TicketController.php`)
- Form Requests (`StoreTicketRequest`, `UpdateTicketRequest`)
- Tests (`TicketTest.php`, `TicketServiceTest.php`)
- Policy (`TicketPolicy.php`)
- Observer (`TicketObserver.php`)

### 2. Seguir o Ciclo TDD

**RED → GREEN → REFACTOR**

1. **RED**: Escrever teste que falha
2. **GREEN**: Implementar código mínimo para passar
3. **REFACTOR**: Melhorar código mantendo testes verdes

Ver detalhes completos em [`docs/development-workflow.md`](docs/development-workflow.md)

### 3. Garantir Qualidade

```powershell
# Executar todos os testes
docker-compose exec orionone-app php artisan test

# PHPStan (static analysis)
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# Laravel Pint (code style)
docker-compose exec orionone-app ./vendor/bin/pint

# Coverage (opcional)
docker-compose exec orionone-app php artisan test --coverage
```

### 4. Commit

```bash
# Seguir Conventional Commits
git add .
git commit -m "feat(tickets): adiciona CRUD completo de tickets

- Migration com campos title, description, status, priority
- TicketController com resource methods
- Tests com >90% coverage
- Policy para autorização
- Observer para audit log"

git push origin main
```

---

## Convenções de Código

### PHP (Laravel)

**PSR-12** + Laravel Best Practices

**Regras principais:**

- Type hints obrigatórios (params e return types)
- DocBlocks apenas quando adiciona valor
- Constructor property promotion (PHP 8.2+)
- Readonly properties quando possível
- Maximum 120 caracteres por linha
- 1 classe por ficheiro

### JavaScript/Vue 3

**ESLint** + Vue 3 Composition API

**Regras principais:**

- Composition API (não Options API)
- `<script setup>` syntax
- Prefer `const` sobre `let`
- 2 espaços de indentação
- Single quotes para strings
- No semicolons (;)

### Database Migrations

**Regras principais:**

- UUIDs para primary keys (não auto-increment)
- Foreign keys com `constrained()`
- Indexes em colunas frequentemente filtradas
- `softDeletes()` para tabelas principais
- Sempre implementar `down()`

---

---

## Conventional Commits

Formato: `<type>(<scope>): <subject>`

### Types

| Type | Uso |
| ---------- | ---------------------------------- |
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (sem mudança de lógica) |
| `refactor` | Refatoração |
| `test` | Adicionar/corrigir testes |
| `chore` | Tarefas de manutenção |
| `perf` | Performance |

### Scopes (opcional)

- `tickets` - Funcionalidade de tickets
- `comments` - Comentários
- `teams` - Equipas
- `auth` - Autenticação
- `sla` - SLA tracking
- `kb` - Knowledge base
- `dashboard` - Dashboard

### Exemplos

```bash
# Feature completa
feat(tickets): adiciona CRUD completo de tickets

# Bug fix
fix(auth): corrige validação de email duplicado

# Documentação
docs(readme): atualiza instruções de setup

# Refactoring
refactor(tickets): move lógica para TicketService

# Tests
test(tickets): adiciona testes para criação de tickets

# Performance
perf(dashboard): otimiza query de estatísticas com eager loading
```

---

## Estrutura de Branches (Opcional)

Para projetos maiores com múltiplos colaboradores:

```
main # Production-ready code
 feature/tickets # Nova feature
 fix/auth-bug # Bug fix
 refactor/services # Refactoring
```

**Para este projeto académico (solo):**

- Trabalhar diretamente em `main`
- Commits frequentes e pequenos
- Push regular para backup

---

## Testes

### Feature Tests (HTTP)

Testam endpoints HTTP completos, incluindo validação e autorização.

### Unit Tests (Lógica)

Testam lógica de negócio isolada (Services, Actions, Models).

### Executar Testes

```powershell
# Todos os testes
docker-compose exec orionone-app php artisan test

# Teste específico
docker-compose exec orionone-app php artisan test --filter=TicketTest

# Com coverage
docker-compose exec orionone-app php artisan test --coverage --min=80
```

Ver mais detalhes em [`docs/testing-strategy.md`](docs/testing-strategy.md)

---

## Checklist de Qualidade

Antes de cada commit:

- [ ] Testes passam (`php artisan test`)
- [ ] PHPStan sem erros (`./vendor/bin/phpstan analyse`)
- [ ] Pint sem warnings (`./vendor/bin/pint --test`)
- [ ] Coverage >80% (feature) ou >90% (service/action)
- [ ] Commit message segue Conventional Commits
- [ ] Código documentado onde necessário
- [ ] Sem `dd()`, `dump()`, `console.log()` no código

---

## Comandos Úteis

### Workflow Diário

```bash
# Iniciar containers
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Parar containers (mantém dados)
docker-compose stop

# Parar e remover containers (mantém volumes)
docker-compose down
```

### Antes de Commit

```bash
# 1. Code style
docker-compose exec orionone-app ./vendor/bin/pint

# 2. Análise estática
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# 3. Testes
docker-compose exec orionone-app php artisan test
```

### Artisan Commands

```bash
# Migrations
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan migrate:fresh --seed

# Cache
docker-compose exec orionone-app php artisan config:clear
docker-compose exec orionone-app php artisan cache:clear

# Tinker (REPL)
docker-compose exec orionone-app php artisan tinker
```

### Composer

```bash
# Instalar dependências
docker-compose exec orionone-app composer install

# Adicionar package
docker-compose exec orionone-app composer require package/name
```

### NPM (Frontend)

```bash
# Instalar dependências (Linux-compatible)
docker-compose run --rm orionone-frontend npm install

# Build para produção
docker-compose run --rm orionone-frontend npm run build
```

---

## Dúvidas?

Consultar:

- [`docs/development-workflow.md`](docs/development-workflow.md) - Workflow completo
- [`docs/testing-strategy.md`](docs/testing-strategy.md) - Estratégia de testes
- [`docs/architecture.md`](docs/architecture.md) - Decisões arquiteturais
- [`SETUP.md`](SETUP.md) - Setup do ambiente

**Regra de Ouro:**

> "Se não está testado, não está feito."
