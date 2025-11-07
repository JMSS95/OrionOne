# Database Schema - OrionOne# Database Schema - OrionOne

## Visão Geral## Diagrama ER

OrionOne utilizará **PostgreSQL 16** como base de dados relacional, aproveitando features avançadas como JSONB para custom fields, full-text search para knowledge base, e indexes otimizados para performance.```

┌─────────┐ ┌──────────┐ ┌─────────┐

**Características principais:**│ users │──────<│ tickets │>──────│ teams │

-   Normalização até 3NF (evitar redundância)└────┬────┘ └────┬─────┘ └─────────┘

-   Soft deletes em tabelas críticas (auditoria) │ │

-   Timestamps automáticos (created_at, updated_at) │ ┌────▼─────┐

-   Foreign keys com ON DELETE CASCADE/SET NULL apropriados │ │ comments │

-   Indexes estratégicos para queries comuns │ └──────────┘

    │

--- │ ┌──────────┐ ┌────────────┐

     └───────────<│ articles │>──────│ categories │

## Diagrama ER Completo └──────────┘ └────────────┘

```

```

                    ┌──────────────┐## Tabelas Principais

                    │    users     │

                    │──────────────│### users

                    │ id  PK       │

                    │ name         │| Campo    | Tipo         | Descrição          |

                    │ email  UQ    │| -------- | ------------ | ------------------ |

                    │ password     │| id       | BIGSERIAL    | Primary key        |

                    └───────┬──────┘| name     | VARCHAR(255) | Nome do utilizador |

                            │| email    | VARCHAR(255) | Email (único)      |

        ┌───────────────────┼───────────────────┐| password | VARCHAR(255) | Password hash      |

        │ 1                 │ N                 │ N

        │                   │                   │### tickets

┌────▼─────┐ ┌────▼─────────┐ ┌────▼────────┐

│ roles │ │ tickets │ │ comments │| Campo | Tipo | Descrição |

│──────────│ │──────────────│ │─────────────│| ------------- | ------------ | ----------------------------------- |

│ id PK │◄───┐ │ id PK │ │ id PK │| id | BIGSERIAL | Primary key |

│ name UQ │ │ │ number UQ │ │ content │| ticket_number | VARCHAR(20) | Número único (TKT-000001) |

└──────────┘ │ │ title │ │ ticket_id FK│──┐| title | VARCHAR(255) | Título do ticket |

                   │   │ description  │   │ user_id FK  │  │| description   | TEXT         | Descrição detalhada                 |

                   │   │ status       │   │ is_internal │  │| status        | VARCHAR(50)  | open, in_progress, resolved, closed |

        ┌──────────┼───│ priority     │   └─────────────┘  │| priority      | VARCHAR(50)  | low, medium, high, urgent           |

        │          │   │ requester FK │                    │| requester_id  | BIGINT FK    | Quem criou (users.id)               |

        │          │   │ assigned FK  │                    │| assigned_to   | BIGINT FK    | Agent atribuído (users.id)          |

        │ N        │   │ team_id FK   │                    │ N| team_id       | BIGINT FK    | Equipa responsável (teams.id)       |

┌────▼─────┐ │ │ sla_fields │ │

│ teams │ │ │ custom_fields│ │ 1### comments

│──────────│ │ └──────────────┘ ┌─────▼────────┐

│ id PK │ │ │ tickets │| Campo | Tipo | Descrição |

│ name │ │ └──────────────┘| ----------- | --------- | ----------------------- |

│ slug UQ │ │| id | BIGSERIAL | Primary key |

└────┬─────┘ │| ticket_id | BIGINT FK | Ticket relacionado |

        │         │| user_id     | BIGINT FK | Autor do comentário     |

        │ N       │| content     | TEXT      | Conteúdo                |

┌────▼──────────▼──┐| is_internal | BOOLEAN | Visível só para agents? |

│ team_user │ ← PIVOT TABLE

│──────────────────│## Indexes

│ team_id FK │

│ user_id FK │```sql

│ role (member/lead)│-- Performance indexes

│ joined_at │CREATE INDEX idx_tickets_status ON tickets(status);

└──────────────────┘CREATE INDEX idx_tickets_priority ON tickets(priority);

CREATE INDEX idx_tickets_requester ON tickets(requester_id);

CREATE INDEX idx_tickets_assigned ON tickets(assigned_to);

┌──────────────┐ ┌───────────────┐ ┌──────────────┐CREATE INDEX idx_comments_ticket ON comments(ticket_id);

│ categories │ 1 │ articles │ N │ users │```

│──────────────│◄───────│───────────────│────────►│ (author_id) │
│ id PK │ │ id PK │ └──────────────┘
│ name │ │ title │
│ slug UQ │ │ slug UQ │
│ icon │ │ content │
│ parent_id FK │ │ category_id FK│
└──────────────┘ │ author_id FK │
│ is_published │
│ views │
│ helpful_count │
└───────────────┘

┌───────────────────┐ ┌──────────────┐
│ model_has_roles │◄───────│ permissions │
│───────────────────│ │──────────────│
│ role_id FK │ │ id PK │
│ model_type │ │ name UQ │
│ model_id FK │ └──────────────┘
└───────────────────┘ ▲
│ N
┌───────────────────┐ │
│ role_has_perms │◄──────────────┘
│───────────────────│
│ permission_id FK │
│ role_id FK │
└───────────────────┘

````

---

## Tabelas Principais

### 1. users

**Descrição:** Utilizadores do sistema (Admin, Agent, Requester)

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | BIGSERIAL | PRIMARY KEY | Identificador único |
| `name` | VARCHAR(255) | NOT NULL | Nome completo |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Email (login) |
| `email_verified_at` | TIMESTAMP | NULLABLE | Data de verificação |
| `password` | VARCHAR(255) | NOT NULL | Hash bcrypt |
| `remember_token` | VARCHAR(100) | NULLABLE | Token "remember me" |
| `avatar` | VARCHAR(255) | NULLABLE | URL do avatar |
| `is_active` | BOOLEAN | DEFAULT true | Conta ativa? |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |
| `deleted_at` | TIMESTAMP | NULLABLE | Soft delete |

**Indexes:**
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_active ON users(is_active) WHERE deleted_at IS NULL;
````

**Relacionamentos:**

-   `hasMany`: tickets (como requester)
-   `hasMany`: tickets (como assigned agent)
-   `hasMany`: comments
-   `hasMany`: articles (como author)
-   `belongsToMany`: teams (pivot: team_user)
-   `belongsToMany`: roles (via Spatie Permission)

---

### 2. teams

**Descrição:** Equipas de suporte especializadas (Hardware, Software, Network, etc.)

| Campo         | Tipo         | Constraints      | Descrição                         |
| ------------- | ------------ | ---------------- | --------------------------------- |
| `id`          | BIGSERIAL    | PRIMARY KEY      | Identificador único               |
| `name`        | VARCHAR(255) | NOT NULL         | Nome da equipa                    |
| `slug`        | VARCHAR(255) | UNIQUE, NOT NULL | URL-friendly (hardware, software) |
| `description` | TEXT         | NULLABLE         | Descrição da equipa               |
| `email`       | VARCHAR(255) | NULLABLE         | Email da equipa                   |
| `is_active`   | BOOLEAN      | DEFAULT true     | Equipa ativa?                     |
| `created_at`  | TIMESTAMP    | NOT NULL         |                                   |
| `updated_at`  | TIMESTAMP    | NOT NULL         |                                   |

**Indexes:**

```sql
CREATE UNIQUE INDEX idx_teams_slug ON teams(slug);
CREATE INDEX idx_teams_active ON teams(is_active);
```

**Relacionamentos:**

-   `hasMany`: tickets
-   `belongsToMany`: users (pivot: team_user)

---

### 3. team_user (Pivot Table)

**Descrição:** Relacionamento muitos-para-muitos entre users e teams

| Campo       | Tipo        | Constraints      | Descrição    |
| ----------- | ----------- | ---------------- | ------------ |
| `id`        | BIGSERIAL   | PRIMARY KEY      |              |
| `team_id`   | BIGINT      | FK → teams(id)   |              |
| `user_id`   | BIGINT      | FK → users(id)   |              |
| `role`      | VARCHAR(50) | DEFAULT 'member' | member, lead |
| `joined_at` | TIMESTAMP   | NOT NULL         |              |

**Indexes:**

```sql
CREATE UNIQUE INDEX idx_team_user_unique ON team_user(team_id, user_id);
CREATE INDEX idx_team_user_team ON team_user(team_id);
CREATE INDEX idx_team_user_user ON team_user(user_id);
```

---

### 4. tickets

**Descrição:** Tickets de suporte criados por utilizadores

| Campo                     | Tipo         | Constraints          | Descrição                           |
| ------------------------- | ------------ | -------------------- | ----------------------------------- |
| `id`                      | BIGSERIAL    | PRIMARY KEY          |                                     |
| `ticket_number`           | VARCHAR(20)  | UNIQUE, NOT NULL     | TKT-000001 (auto-gerado)            |
| `title`                   | VARCHAR(255) | NOT NULL             | Título do ticket                    |
| `description`             | TEXT         | NOT NULL             | Descrição detalhada                 |
| `status`                  | VARCHAR(50)  | NOT NULL             | open, in_progress, resolved, closed |
| `priority`                | VARCHAR(50)  | NOT NULL             | low, medium, high, urgent           |
| `requester_id`            | BIGINT       | FK → users(id)       | Quem criou                          |
| `assigned_to`             | BIGINT       | FK → users(id), NULL | Agent atribuído                     |
| `team_id`                 | BIGINT       | FK → teams(id), NULL | Equipa responsável                  |
| `category`                | VARCHAR(100) | NULLABLE             | Categoria do problema               |
| `first_response_at`       | TIMESTAMP    | NULLABLE             | Primeira resposta do agent          |
| `first_response_deadline` | TIMESTAMP    | NULLABLE             | SLA: deadline 1ª resposta           |
| `resolution_deadline`     | TIMESTAMP    | NULLABLE             | SLA: deadline resolução             |
| `resolved_at`             | TIMESTAMP    | NULLABLE             | Data de resolução                   |
| `closed_at`               | TIMESTAMP    | NULLABLE             | Data de fecho                       |
| `is_escalated`            | BOOLEAN      | DEFAULT false        | Escalado para manager?              |
| `custom_fields`           | JSONB        | NULLABLE             | Campos customizáveis                |
| `created_at`              | TIMESTAMP    | NOT NULL             |                                     |
| `updated_at`              | TIMESTAMP    | NOT NULL             |                                     |
| `deleted_at`              | TIMESTAMP    | NULLABLE             | Soft delete                         |

**Indexes:**

```sql
CREATE UNIQUE INDEX idx_tickets_number ON tickets(ticket_number);
CREATE INDEX idx_tickets_status ON tickets(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_requester ON tickets(requester_id);
CREATE INDEX idx_tickets_assigned ON tickets(assigned_to);
CREATE INDEX idx_tickets_team ON tickets(team_id);
CREATE INDEX idx_tickets_created ON tickets(created_at);
CREATE INDEX idx_tickets_sla_deadline ON tickets(resolution_deadline) WHERE status IN ('open', 'in_progress');
CREATE INDEX idx_tickets_custom_fields ON tickets USING GIN(custom_fields);
```

**Relacionamentos:**

-   `belongsTo`: user (requester)
-   `belongsTo`: user (assigned agent)
-   `belongsTo`: team
-   `hasMany`: comments
-   `morphMany`: activity_log (via Spatie Activity Log)

**Enums (implementados via validation):**

-   **status:** `open`, `in_progress`, `on_hold`, `resolved`, `closed`
-   **priority:** `low`, `medium`, `high`, `urgent`

---

### 5. comments

**Descrição:** Comentários em tickets (públicos ou internos)

| Campo         | Tipo      | Constraints              | Descrição               |
| ------------- | --------- | ------------------------ | ----------------------- |
| `id`          | BIGSERIAL | PRIMARY KEY              |                         |
| `ticket_id`   | BIGINT    | FK → tickets(id) CASCADE | Ticket relacionado      |
| `user_id`     | BIGINT    | FK → users(id)           | Autor do comentário     |
| `content`     | TEXT      | NOT NULL                 | Conteúdo do comentário  |
| `is_internal` | BOOLEAN   | DEFAULT false            | Visível só para agents? |
| `created_at`  | TIMESTAMP | NOT NULL                 |                         |
| `updated_at`  | TIMESTAMP | NOT NULL                 |                         |
| `deleted_at`  | TIMESTAMP | NULLABLE                 | Soft delete             |

**Indexes:**

```sql
CREATE INDEX idx_comments_ticket ON comments(ticket_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_comments_created ON comments(created_at);
CREATE INDEX idx_comments_internal ON comments(is_internal);
```

**Relacionamentos:**

-   `belongsTo`: ticket
-   `belongsTo`: user (author)

---

### 6. categories

**Descrição:** Categorias para Knowledge Base (pode ser hierárquico)

| Campo         | Tipo         | Constraints               | Descrição                  |
| ------------- | ------------ | ------------------------- | -------------------------- |
| `id`          | BIGSERIAL    | PRIMARY KEY               |                            |
| `name`        | VARCHAR(255) | NOT NULL                  | Nome da categoria          |
| `slug`        | VARCHAR(255) | UNIQUE, NOT NULL          | URL-friendly               |
| `description` | TEXT         | NULLABLE                  | Descrição                  |
| `icon`        | VARCHAR(100) | NULLABLE                  | Nome do ícone (Heroicons)  |
| `parent_id`   | BIGINT       | FK → categories(id), NULL | Categoria pai (hierarquia) |
| `order`       | INTEGER      | DEFAULT 0                 | Ordem de exibição          |
| `is_visible`  | BOOLEAN      | DEFAULT true              | Visível no frontend?       |
| `created_at`  | TIMESTAMP    | NOT NULL                  |                            |
| `updated_at`  | TIMESTAMP    | NOT NULL                  |                            |

**Indexes:**

```sql
CREATE UNIQUE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_visible ON categories(is_visible);
```

**Relacionamentos:**

-   `hasMany`: articles
-   `belongsTo`: category (parent) - self-referencing
-   `hasMany`: categories (children)

---

### 7. articles

**Descrição:** Artigos da Knowledge Base

| Campo               | Tipo         | Constraints         | Descrição                 |
| ------------------- | ------------ | ------------------- | ------------------------- |
| `id`                | BIGSERIAL    | PRIMARY KEY         |                           |
| `title`             | VARCHAR(255) | NOT NULL            | Título do artigo          |
| `slug`              | VARCHAR(255) | UNIQUE, NOT NULL    | URL-friendly              |
| `content`           | TEXT         | NOT NULL            | Conteúdo (Markdown/HTML)  |
| `excerpt`           | TEXT         | NULLABLE            | Resumo curto              |
| `category_id`       | BIGINT       | FK → categories(id) | Categoria                 |
| `author_id`         | BIGINT       | FK → users(id)      | Quem criou                |
| `is_published`      | BOOLEAN      | DEFAULT false       | Publicado?                |
| `published_at`      | TIMESTAMP    | NULLABLE            | Data de publicação        |
| `views`             | INTEGER      | DEFAULT 0           | Contador de visualizações |
| `helpful_count`     | INTEGER      | DEFAULT 0           | "Foi útil?" - Sim         |
| `not_helpful_count` | INTEGER      | DEFAULT 0           | "Foi útil?" - Não         |
| `featured`          | BOOLEAN      | DEFAULT false       | Destacado no homepage?    |
| `meta_description`  | VARCHAR(160) | NULLABLE            | SEO                       |
| `created_at`        | TIMESTAMP    | NOT NULL            |                           |
| `updated_at`        | TIMESTAMP    | NOT NULL            |                           |
| `deleted_at`        | TIMESTAMP    | NULLABLE            | Soft delete               |

**Indexes:**

```sql
CREATE UNIQUE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_category ON articles(category_id);
CREATE INDEX idx_articles_author ON articles(author_id);
CREATE INDEX idx_articles_published ON articles(is_published, published_at);
CREATE INDEX idx_articles_featured ON articles(featured) WHERE is_published = true;
-- Full-text search (PostgreSQL)
CREATE INDEX idx_articles_fulltext ON articles USING GIN(to_tsvector('portuguese', title || ' ' || content));
```

**Relacionamentos:**

-   `belongsTo`: category
-   `belongsTo`: user (author)

---

## Tabelas de Spatie Permission

### 8. roles

| Campo        | Tipo         | Descrição          |
| ------------ | ------------ | ------------------ |
| `id`         | BIGSERIAL    | PRIMARY KEY        |
| `name`       | VARCHAR(255) | admin, agent, user |
| `guard_name` | VARCHAR(255) | web                |
| `created_at` | TIMESTAMP    |                    |
| `updated_at` | TIMESTAMP    |                    |

**Roles planeados:**

-   **admin:** acesso total ao sistema
-   **agent:** gestão de tickets, KB
-   **user:** criar tickets, ver KB

---

### 9. permissions

| Campo        | Tipo         | Descrição                         |
| ------------ | ------------ | --------------------------------- |
| `id`         | BIGSERIAL    | PRIMARY KEY                       |
| `name`       | VARCHAR(255) | view-tickets, create-tickets, etc |
| `guard_name` | VARCHAR(255) | web                               |
| `created_at` | TIMESTAMP    |                                   |
| `updated_at` | TIMESTAMP    |                                   |

**Permissions planeados:**

-   `view-all-tickets`, `create-ticket`, `update-ticket`, `delete-ticket`
-   `assign-ticket`, `close-ticket`, `escalate-ticket`
-   `view-kb`, `create-article`, `publish-article`
-   `manage-users`, `manage-teams`, `view-dashboard`

---

### 10. model_has_roles (Pivot)

| Campo        | Tipo         | Descrição       |
| ------------ | ------------ | --------------- |
| `role_id`    | BIGINT       | FK → roles(id)  |
| `model_type` | VARCHAR(255) | App\Models\User |
| `model_id`   | BIGINT       | FK → users(id)  |

---

### 11. role_has_permissions (Pivot)

| Campo           | Tipo   | Descrição            |
| --------------- | ------ | -------------------- |
| `permission_id` | BIGINT | FK → permissions(id) |
| `role_id`       | BIGINT | FK → roles(id)       |

---

## Tabelas de Sistema (Laravel)

### 12. cache

Laravel cache (sessions, query cache, etc.)

---

### 13. jobs

Laravel queue jobs (emails, SLA checks, reports)

---

### 14. failed_jobs

Jobs que falharam (retry mechanism)

---

### 15. activity_log (Spatie Activity Log)

**Descrição:** Auditoria de ações no sistema

| Campo          | Tipo         | Descrição                 |
| -------------- | ------------ | ------------------------- |
| `id`           | BIGSERIAL    | PRIMARY KEY               |
| `log_name`     | VARCHAR(255) | ticket, user, article     |
| `description`  | TEXT         | created, updated, deleted |
| `subject_type` | VARCHAR(255) | Modelo afetado            |
| `subject_id`   | BIGINT       | ID do modelo              |
| `causer_type`  | VARCHAR(255) | Quem fez (User)           |
| `causer_id`    | BIGINT       | User ID                   |
| `properties`   | JSON         | Dados antes/depois        |
| `created_at`   | TIMESTAMP    |                           |

---

## Estratégia de Migrations

### Ordem de Execução

```
1. users
2. teams
3. team_user
4. categories
5. articles
6. tickets
7. comments
8. roles & permissions (Spatie)
9. activity_log (Spatie)
```

### Boas Práticas

-   Foreign keys com constraints apropriados
-   Indexes em colunas frequentemente consultadas
-   Soft deletes em tabelas críticas
-   Timestamps automáticos
-   Default values sensatos

---

## Queries Comuns Otimizadas

### Dashboard: Tickets por Status

```sql
SELECT status, COUNT(*) as total
FROM tickets
WHERE deleted_at IS NULL
  AND team_id = ?
GROUP BY status;
-- Usa: idx_tickets_status
```

### Tickets Overdue (SLA)

```sql
SELECT *
FROM tickets
WHERE status IN ('open', 'in_progress')
  AND resolution_deadline < NOW()
  AND resolved_at IS NULL;
-- Usa: idx_tickets_sla_deadline
```

### Knowledge Base Search

```sql
SELECT *
FROM articles
WHERE is_published = true
  AND to_tsvector('portuguese', title || ' ' || content) @@ plainto_tsquery('portuguese', ?);
-- Usa: idx_articles_fulltext
```

---

## Considerações de Performance

### Indexes Estratégicos

-   **Foreign keys:** sempre indexadas
-   **Status/Priority:** queries de filtro comuns
-   **Timestamps:** ordenação cronológica
-   **JSONB fields:** GIN index para custom_fields
-   **Full-text:** GIN index para search

### Soft Deletes

-   Tickets, Comments, Articles: mantém histórico
-   Indexes com `WHERE deleted_at IS NULL` para performance

### Partitioning (Futuro)

Se o volume crescer:

-   Particionar `tickets` por data (`created_at`)
-   Particionar `activity_log` por mês

---

## Conclusão

Este schema foi desenhado para:

-   **Performance:** indexes estratégicos, queries otimizadas
-   **Escalabilidade:** estrutura normalizada, suporta growth
-   **Auditoria:** soft deletes, activity log completo
-   **Flexibilidade:** JSONB para campos customizáveis
-   **Best Practices:** convenções Laravel, Spatie packages

O schema suporta todos os requisitos funcionais do OrionOne enquanto mantém performance e manutenibilidade.
