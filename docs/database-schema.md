# Database Schema - OrionOne

## Visão Geral

OrionOne utilizará **PostgreSQL 16** como base de dados relacional, aproveitando features avançadas como JSONB para custom fields, full-text search para knowledge base, e indexes otimizados para performance.

**Características principais:**

-   Normalização até 3NF (evitar redundância)
-   Soft deletes em tabelas críticas (auditoria)
-   Timestamps automáticos (created_at, updated_at)
-   Foreign keys com ON DELETE CASCADE/SET NULL apropriados
-   Indexes estratégicos para queries comuns

---

## Tabelas Principais

### 1. users

**Descrição:** Utilizadores do sistema (Admin, Agent, Requester)

| Campo               | Tipo         | Constraints      | Descrição           |
| ------------------- | ------------ | ---------------- | ------------------- |
| `id`                | BIGSERIAL    | PRIMARY KEY      | Identificador único |
| `name`              | VARCHAR(255) | NOT NULL         | Nome completo       |
| `email`             | VARCHAR(255) | UNIQUE, NOT NULL | Email (login)       |
| `email_verified_at` | TIMESTAMP    | NULLABLE         | Data de verificação |
| `password`          | VARCHAR(255) | NOT NULL         | Hash bcrypt         |
| `remember_token`    | VARCHAR(100) | NULLABLE         | Token "remember me" |
| `avatar`            | VARCHAR(255) | NULLABLE         | URL do avatar       |
| `is_active`         | BOOLEAN      | DEFAULT true     | Conta ativa?        |
| `created_at`        | TIMESTAMP    | NOT NULL         |                     |
| `updated_at`        | TIMESTAMP    | NOT NULL         |                     |
| `deleted_at`        | TIMESTAMP    | NULLABLE         | Soft delete         |

**Indexes:**

```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_active ON users(is_active) WHERE deleted_at IS NULL;
```

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

## Database Views (Queries Pré-Computadas)

### VIEW 1: v_ticket_dashboard

**Propósito:** Dashboard principal com todos os dados de tickets (performance crítica).

```sql
CREATE OR REPLACE VIEW v_ticket_dashboard AS
SELECT
    t.id,
    t.ticket_number,
    t.title,
    t.status,
    t.priority,
    t.created_at,
    t.resolution_deadline,
    u_req.name AS requester_name,
    u_req.email AS requester_email,
    u_ag.name AS assigned_agent_name,
    u_ag.id AS assigned_agent_id,
    tm.name AS team_name,
    tm.id AS team_id,
    CASE
        WHEN t.resolution_deadline < NOW()
             AND t.status IN ('open', 'in_progress')
             AND t.resolved_at IS NULL
        THEN true
        ELSE false
    END AS is_overdue,
    EXTRACT(EPOCH FROM (NOW() - t.created_at))/3600 AS age_hours,
    EXTRACT(EPOCH FROM (t.first_response_at - t.created_at))/3600 AS first_response_hours,
    (SELECT COUNT(*) FROM comments WHERE ticket_id = t.id AND deleted_at IS NULL) AS comment_count
FROM tickets t
LEFT JOIN users u_req ON t.requester_id = u_req.id
LEFT JOIN users u_ag ON t.assigned_to = u_ag.id
LEFT JOIN teams tm ON t.team_id = tm.id
WHERE t.deleted_at IS NULL;
```

**Uso em Laravel:**

```php
// Controller
$tickets = DB::table('v_ticket_dashboard')
    ->where('team_id', auth()->user()->team_id)
    ->where('status', 'open')
    ->orderBy('is_overdue', 'desc')
    ->get();
```

---

### VIEW 2: v_sla_compliance

**Propósito:** Relatório de compliance SLA por ticket.

```sql
CREATE OR REPLACE VIEW v_sla_compliance AS
SELECT
    t.id,
    t.ticket_number,
    t.priority,
    t.team_id,
    t.created_at,
    t.first_response_deadline,
    t.resolution_deadline,
    t.first_response_at,
    t.resolved_at,
    CASE
        WHEN t.first_response_at IS NULL AND t.first_response_deadline < NOW()
        THEN 'BREACHED'
        WHEN t.first_response_at IS NOT NULL AND t.first_response_at <= t.first_response_deadline
        THEN 'MET'
        WHEN t.first_response_at IS NULL AND t.first_response_deadline >= NOW()
        THEN 'PENDING'
        ELSE 'BREACHED'
    END AS first_response_sla_status,
    CASE
        WHEN t.resolved_at IS NULL AND t.resolution_deadline < NOW()
        THEN 'BREACHED'
        WHEN t.resolved_at IS NOT NULL AND t.resolved_at <= t.resolution_deadline
        THEN 'MET'
        WHEN t.resolved_at IS NULL AND t.resolution_deadline >= NOW()
        THEN 'PENDING'
        ELSE 'BREACHED'
    END AS resolution_sla_status,
    ROUND(EXTRACT(EPOCH FROM (t.first_response_at - t.created_at))/3600, 2) AS first_response_hours,
    ROUND(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600, 2) AS resolution_hours
FROM tickets t
WHERE t.deleted_at IS NULL;
```

**Uso em Laravel:**

```php
// Relatório mensal SLA
$slaReport = DB::table('v_sla_compliance')
    ->selectRaw('
        priority,
        COUNT(*) as total,
        SUM(CASE WHEN resolution_sla_status = "MET" THEN 1 ELSE 0 END) as met,
        SUM(CASE WHEN resolution_sla_status = "BREACHED" THEN 1 ELSE 0 END) as breached
    ')
    ->whereMonth('created_at', now()->month)
    ->groupBy('priority')
    ->get();
```

---

### VIEW 3: v_agent_performance

**Propósito:** Métricas de performance por agent (workload, resolution time, SLA compliance).

```sql
CREATE OR REPLACE VIEW v_agent_performance AS
SELECT
    u.id AS agent_id,
    u.name AS agent_name,
    u.email AS agent_email,
    COUNT(DISTINCT t.id) AS total_tickets_assigned,
    COUNT(DISTINCT CASE WHEN t.status = 'resolved' THEN t.id END) AS resolved_tickets,
    COUNT(DISTINCT CASE WHEN t.status = 'closed' THEN t.id END) AS closed_tickets,
    COUNT(DISTINCT CASE WHEN t.status IN ('open', 'in_progress') THEN t.id END) AS active_tickets,
    COUNT(DISTINCT CASE WHEN t.priority = 'urgent' THEN t.id END) AS urgent_tickets_handled,
    ROUND(AVG(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600), 2) AS avg_resolution_hours,
    ROUND(AVG(EXTRACT(EPOCH FROM (t.first_response_at - t.created_at))/3600), 2) AS avg_first_response_hours,
    COUNT(DISTINCT CASE WHEN t.resolved_at <= t.resolution_deadline THEN t.id END) AS sla_met_count,
    ROUND(
        COUNT(DISTINCT CASE WHEN t.resolved_at <= t.resolution_deadline THEN t.id END)::NUMERIC
        / NULLIF(COUNT(DISTINCT CASE WHEN t.resolved_at IS NOT NULL THEN t.id END), 0) * 100,
        2
    ) AS sla_compliance_percentage
FROM users u
LEFT JOIN tickets t ON u.id = t.assigned_to AND t.deleted_at IS NULL
WHERE u.deleted_at IS NULL
  AND EXISTS (
      SELECT 1 FROM model_has_roles
      WHERE model_id = u.id
        AND role_id = (SELECT id FROM roles WHERE name = 'agent')
  )
GROUP BY u.id, u.name, u.email;
```

**Uso em Laravel:**

```php
// Ranking de agents por SLA compliance
$topAgents = DB::table('v_agent_performance')
    ->where('total_tickets_assigned', '>', 10)
    ->orderBy('sla_compliance_percentage', 'desc')
    ->limit(10)
    ->get();
```

---

### VIEW 4: v_kb_popular_articles

**Propósito:** Artigos da KB ordenados por popularidade e helpfulness.

```sql
CREATE OR REPLACE VIEW v_kb_popular_articles AS
SELECT
    a.id,
    a.title,
    a.slug,
    a.excerpt,
    a.views,
    a.helpful_count,
    a.not_helpful_count,
    CASE
        WHEN (a.helpful_count + a.not_helpful_count) > 0
        THEN ROUND((a.helpful_count::NUMERIC / (a.helpful_count + a.not_helpful_count) * 100), 2)
        ELSE 0
    END AS helpfulness_percentage,
    c.name AS category_name,
    c.slug AS category_slug,
    u.name AS author_name,
    a.published_at,
    a.updated_at
FROM articles a
JOIN categories c ON a.category_id = c.id
JOIN users u ON a.author_id = u.id
WHERE a.is_published = true
  AND a.deleted_at IS NULL
ORDER BY a.views DESC, a.helpful_count DESC;
```

**Uso em Laravel:**

```php
// Top 10 artigos mais úteis
$topArticles = DB::table('v_kb_popular_articles')
    ->where('views', '>', 50)
    ->orderBy('helpfulness_percentage', 'desc')
    ->limit(10)
    ->get();
```

---

## Database Triggers (Automação & Validação)

### TRIGGER 1: Auto-gerar ticket_number

**Propósito:** Gerar ticket_number único automaticamente no formato `TKT-YYYYMMDD-NNNN`.

```sql
CREATE OR REPLACE FUNCTION generate_ticket_number()
RETURNS TRIGGER AS $$
DECLARE
    date_prefix TEXT;
    seq_num INTEGER;
BEGIN
    IF NEW.ticket_number IS NOT NULL THEN
        RETURN NEW; -- Já foi definido manualmente
    END IF;

    date_prefix := TO_CHAR(NOW(), 'YYYYMMDD');

    -- Obter próximo número sequencial do dia
    SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_number FROM 13) AS INTEGER)), 0) + 1
    INTO seq_num
    FROM tickets
    WHERE ticket_number LIKE 'TKT-' || date_prefix || '-%'
      AND deleted_at IS NULL;

    NEW.ticket_number := 'TKT-' || date_prefix || '-' || LPAD(seq_num::TEXT, 4, '0');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_generate_ticket_number
BEFORE INSERT ON tickets
FOR EACH ROW
WHEN (NEW.ticket_number IS NULL)
EXECUTE FUNCTION generate_ticket_number();
```

**Resultado:**

```
TKT-20251111-0001
TKT-20251111-0002
...
TKT-20251112-0001 (novo dia, reset counter)
```

---

### TRIGGER 2: Auto-calcular SLA deadlines

**Propósito:** Calcular `first_response_deadline` e `resolution_deadline` baseado em `priority`.

```sql
CREATE OR REPLACE FUNCTION set_sla_deadlines()
RETURNS TRIGGER AS $$
BEGIN
    -- First Response SLA (baseado em priority)
    NEW.first_response_deadline := NEW.created_at +
        CASE NEW.priority
            WHEN 'urgent' THEN INTERVAL '2 hours'
            WHEN 'high' THEN INTERVAL '4 hours'
            WHEN 'medium' THEN INTERVAL '8 hours'
            WHEN 'low' THEN INTERVAL '24 hours'
            ELSE INTERVAL '24 hours' -- default
        END;

    -- Resolution SLA (baseado em priority)
    NEW.resolution_deadline := NEW.created_at +
        CASE NEW.priority
            WHEN 'urgent' THEN INTERVAL '8 hours'
            WHEN 'high' THEN INTERVAL '2 days'
            WHEN 'medium' THEN INTERVAL '5 days'
            WHEN 'low' THEN INTERVAL '10 days'
            ELSE INTERVAL '5 days' -- default
        END;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_sla_deadlines
BEFORE INSERT ON tickets
FOR EACH ROW
EXECUTE FUNCTION set_sla_deadlines();
```

**Benefício:** Zero código PHP para SLA calculation - tudo automático no DB!

---

### TRIGGER 3: Validar agent assignment

**Propósito:** Garantir que `assigned_to` pertence ao `team_id` do ticket.

```sql
CREATE OR REPLACE FUNCTION validate_ticket_assignment()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.assigned_to IS NULL THEN
        RETURN NEW; -- OK: não atribuído
    END IF;

    IF NEW.team_id IS NULL THEN
        RAISE EXCEPTION 'Ticket % deve ter team_id antes de assigned_to', NEW.id;
    END IF;

    -- Verificar se agent pertence ao team
    IF NOT EXISTS (
        SELECT 1 FROM team_user
        WHERE user_id = NEW.assigned_to
          AND team_id = NEW.team_id
    ) THEN
        RAISE EXCEPTION 'User % não pertence ao Team %', NEW.assigned_to, NEW.team_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_ticket_assignment
BEFORE INSERT OR UPDATE OF assigned_to, team_id ON tickets
FOR EACH ROW
WHEN (NEW.assigned_to IS NOT NULL)
EXECUTE FUNCTION validate_ticket_assignment();
```

**Benefício:** Data integrity garantida no DB (mesmo se bypass Laravel validation).

---

### TRIGGER 4: Log status changes automaticamente

**Propósito:** Registar mudanças de status em `activity_log` automaticamente.

```sql
CREATE OR REPLACE FUNCTION log_ticket_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO activity_log (
            log_name,
            description,
            subject_type,
            subject_id,
            properties,
            created_at,
            updated_at
        ) VALUES (
            'ticket',
            'status_changed',
            'App\Models\Ticket',
            NEW.id,
            jsonb_build_object(
                'old_status', OLD.status,
                'new_status', NEW.status,
                'changed_at', NOW()
            ),
            NOW(),
            NOW()
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_ticket_status_change
AFTER UPDATE ON tickets
FOR EACH ROW
EXECUTE FUNCTION log_ticket_status_change();
```

**Benefício:** Auditoria completa de mudanças de status - zero código PHP!

---

## Stored Procedures (Lógica Complexa)

### PROCEDURE 1: assign_ticket_auto()

**Propósito:** Atribuir ticket ao agent menos ocupado de um team.

```sql
CREATE OR REPLACE FUNCTION assign_ticket_auto(
    p_ticket_id BIGINT,
    p_team_id BIGINT
) RETURNS BIGINT AS $$
DECLARE
    v_agent_id BIGINT;
BEGIN
    -- Encontrar agent com menos tickets ativos no team
    SELECT u.id INTO v_agent_id
    FROM users u
    JOIN team_user tu ON u.id = tu.user_id
    LEFT JOIN tickets t ON t.assigned_to = u.id
                        AND t.status IN ('open', 'in_progress')
                        AND t.deleted_at IS NULL
    WHERE tu.team_id = p_team_id
      AND u.is_active = true
      AND u.deleted_at IS NULL
      AND EXISTS (
          SELECT 1 FROM model_has_roles mhr
          JOIN roles r ON mhr.role_id = r.id
          WHERE mhr.model_id = u.id AND r.name = 'agent'
      )
    GROUP BY u.id
    ORDER BY COUNT(t.id) ASC, RANDOM() -- Menos ocupado + random tie-break
    LIMIT 1;

    IF v_agent_id IS NULL THEN
        RAISE EXCEPTION 'Nenhum agent disponível no Team %', p_team_id;
    END IF;

    -- Atribuir ticket
    UPDATE tickets
    SET assigned_to = v_agent_id,
        team_id = p_team_id,
        updated_at = NOW()
    WHERE id = p_ticket_id;

    RETURN v_agent_id;
END;
$$ LANGUAGE plpgsql;
```

**Uso em Laravel:**

```php
// Controller
$agentId = DB::select('SELECT assign_ticket_auto(?, ?)', [$ticketId, $teamId])[0]->assign_ticket_auto;

activity()
    ->performedOn($ticket)
    ->log("Auto-assigned to agent {$agentId}");
```

---

### PROCEDURE 2: close_ticket()

**Propósito:** Fechar ticket com validações de negócio.

```sql
CREATE OR REPLACE FUNCTION close_ticket(
    p_ticket_id BIGINT,
    p_user_id BIGINT
) RETURNS BOOLEAN AS $$
DECLARE
    v_current_status VARCHAR(50);
BEGIN
    -- Validar ticket exists e está em status válido
    SELECT status INTO v_current_status
    FROM tickets
    WHERE id = p_ticket_id AND deleted_at IS NULL;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Ticket % não encontrado', p_ticket_id;
    END IF;

    IF v_current_status != 'resolved' THEN
        RAISE EXCEPTION 'Ticket % não está em status "resolved" (atual: %)', p_ticket_id, v_current_status;
    END IF;

    -- Fechar ticket
    UPDATE tickets
    SET status = 'closed',
        closed_at = NOW(),
        updated_at = NOW()
    WHERE id = p_ticket_id;

    -- Log activity
    INSERT INTO activity_log (
        log_name, description, subject_type, subject_id,
        causer_type, causer_id, created_at, updated_at
    ) VALUES (
        'ticket', 'closed', 'App\Models\Ticket', p_ticket_id,
        'App\Models\User', p_user_id, NOW(), NOW()
    );

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

**Uso em Laravel:**

```php
try {
    DB::select('SELECT close_ticket(?, ?)', [$ticketId, auth()->id()]);
    return redirect()->back()->with('success', 'Ticket fechado!');
} catch (\Exception $e) {
    return redirect()->back()->withErrors($e->getMessage());
}
```

---

### PROCEDURE 3: generate_sla_report()

**Propósito:** Gerar relatório de SLA compliance por período e team.

```sql
CREATE OR REPLACE FUNCTION generate_sla_report(
    p_start_date TIMESTAMP,
    p_end_date TIMESTAMP,
    p_team_id BIGINT DEFAULT NULL
)
RETURNS TABLE (
    priority VARCHAR,
    total_tickets BIGINT,
    first_response_met BIGINT,
    first_response_breached BIGINT,
    first_response_pending BIGINT,
    resolution_met BIGINT,
    resolution_breached BIGINT,
    resolution_pending BIGINT,
    avg_resolution_hours NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.priority,
        COUNT(*)::BIGINT AS total_tickets,
        COUNT(CASE WHEN t.first_response_at <= t.first_response_deadline THEN 1 END)::BIGINT AS first_response_met,
        COUNT(CASE WHEN (t.first_response_at > t.first_response_deadline)
                     OR (t.first_response_at IS NULL AND NOW() > t.first_response_deadline)
                   THEN 1 END)::BIGINT AS first_response_breached,
        COUNT(CASE WHEN t.first_response_at IS NULL AND NOW() <= t.first_response_deadline
                   THEN 1 END)::BIGINT AS first_response_pending,
        COUNT(CASE WHEN t.resolved_at <= t.resolution_deadline THEN 1 END)::BIGINT AS resolution_met,
        COUNT(CASE WHEN (t.resolved_at > t.resolution_deadline)
                     OR (t.resolved_at IS NULL AND NOW() > t.resolution_deadline)
                   THEN 1 END)::BIGINT AS resolution_breached,
        COUNT(CASE WHEN t.resolved_at IS NULL AND NOW() <= t.resolution_deadline
                   THEN 1 END)::BIGINT AS resolution_pending,
        ROUND(AVG(EXTRACT(EPOCH FROM (t.resolved_at - t.created_at))/3600), 2)::NUMERIC AS avg_resolution_hours
    FROM tickets t
    WHERE t.created_at BETWEEN p_start_date AND p_end_date
      AND (p_team_id IS NULL OR t.team_id = p_team_id)
      AND t.deleted_at IS NULL
    GROUP BY t.priority
    ORDER BY
        CASE t.priority
            WHEN 'urgent' THEN 1
            WHEN 'high' THEN 2
            WHEN 'medium' THEN 3
            WHEN 'low' THEN 4
        END;
END;
$$ LANGUAGE plpgsql STABLE;
```

**Uso em Laravel:**

```php
// Dashboard: Relatório mensal
$slaReport = DB::select('SELECT * FROM generate_sla_report(?, ?, ?)', [
    now()->startOfMonth(),
    now()->endOfMonth(),
    auth()->user()->team_id, // ou NULL para todos
]);

return view('reports.sla', ['data' => $slaReport]);
```

---

## Check Constraints (Data Validation)

### Validações em nível de DB

```sql
-- TICKETS: Validar status enum
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_status
    CHECK (status IN ('open', 'in_progress', 'on_hold', 'resolved', 'closed'));

-- TICKETS: Validar priority enum
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_priority
    CHECK (priority IN ('low', 'medium', 'high', 'urgent'));

-- TICKETS: Datas lógicas (resolved_at >= created_at)
ALTER TABLE tickets ADD CONSTRAINT chk_tickets_resolved_date
    CHECK (resolved_at IS NULL OR resolved_at >= created_at);

ALTER TABLE tickets ADD CONSTRAINT chk_tickets_closed_date
    CHECK (closed_at IS NULL OR closed_at >= resolved_at);

-- ARTICLES: Contadores não negativos
ALTER TABLE articles ADD CONSTRAINT chk_articles_views
    CHECK (views >= 0);

ALTER TABLE articles ADD CONSTRAINT chk_articles_helpful
    CHECK (helpful_count >= 0 AND not_helpful_count >= 0);

-- ARTICLES: Slug format (lowercase, hyphens only)
ALTER TABLE articles ADD CONSTRAINT chk_articles_slug_format
    CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$');

-- USERS: Email format
ALTER TABLE users ADD CONSTRAINT chk_users_email_format
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- TEAM_USER: Role enum
ALTER TABLE team_user ADD CONSTRAINT chk_team_user_role
    CHECK (role IN ('member', 'lead', 'supervisor'));
```

**Benefício:** Validação em DB + Laravel = dupla proteção!

---

## Indexes Avançados

### Partial Indexes (Performance otimizada)

```sql
-- Index apenas em tickets ATIVOS (não fechados)
CREATE INDEX idx_tickets_active_status ON tickets(status, priority, created_at)
    WHERE deleted_at IS NULL AND status NOT IN ('closed');

-- Index apenas em tickets OVERDUE (Dashboard critical query)
CREATE INDEX idx_tickets_overdue ON tickets(resolution_deadline, team_id)
    WHERE deleted_at IS NULL
      AND status IN ('open', 'in_progress')
      AND resolved_at IS NULL
      AND resolution_deadline < NOW();

-- Index apenas em artigos PUBLICADOS (queries públicas)
CREATE INDEX idx_articles_published_popular ON articles(views DESC, helpful_count DESC)
    WHERE is_published = true AND deleted_at IS NULL;

-- Index apenas em artigos FEATURED (homepage)
CREATE INDEX idx_articles_featured ON articles(featured, published_at DESC)
    WHERE is_published = true AND featured = true AND deleted_at IS NULL;
```

### Composite Indexes (Queries multi-campo)

```sql
-- Dashboard: Filtrar por team + status + priority
CREATE INDEX idx_tickets_team_status_priority ON tickets(team_id, status, priority, created_at DESC)
    WHERE deleted_at IS NULL;

-- Agent workload: assigned + status
CREATE INDEX idx_tickets_assigned_active ON tickets(assigned_to, status, priority)
    WHERE deleted_at IS NULL AND status IN ('open', 'in_progress');

-- SLA breach detection
CREATE INDEX idx_tickets_sla_breach ON tickets(resolution_deadline, status, team_id)
    WHERE deleted_at IS NULL AND status IN ('open', 'in_progress');

-- Comments count por ticket (evitar N+1)
CREATE INDEX idx_comments_ticket_active ON comments(ticket_id, created_at DESC)
    WHERE deleted_at IS NULL;

-- KB search: category + published
CREATE INDEX idx_articles_category_published ON articles(category_id, published_at DESC)
    WHERE is_published = true AND deleted_at IS NULL;
```

### Expression Indexes (Queries em colunas calculadas)

```sql
-- Buscar tickets por idade (NOW() - created_at)
CREATE INDEX idx_tickets_age ON tickets((EXTRACT(EPOCH FROM (NOW() - created_at))/3600))
    WHERE deleted_at IS NULL AND status IN ('open', 'in_progress');

-- Buscar artigos por helpfulness percentage
CREATE INDEX idx_articles_helpfulness ON articles((
    CASE
        WHEN (helpful_count + not_helpful_count) > 0
        THEN helpful_count::NUMERIC / (helpful_count + not_helpful_count)
        ELSE 0
    END
)) WHERE is_published = true AND deleted_at IS NULL;
```

---

## Considerações de Performance

### Indexes Estratégicos

-   **Foreign keys:** sempre indexadas
-   **Status/Priority:** queries de filtro comuns
-   **Timestamps:** ordenação cronológica
-   **JSONB fields:** GIN index para custom_fields
-   **Full-text:** GIN index para search
-   **Partial indexes:** WHERE clauses para queries específicas
-   **Composite indexes:** Múltiplas colunas em queries JOIN/WHERE

### Soft Deletes

-   Tickets, Comments, Articles: mantém histórico
-   Indexes com `WHERE deleted_at IS NULL` para performance
-   Views já filtram `deleted_at IS NULL` automaticamente

### Views vs Materialized Views

**Views (usadas no OrionOne):**

-   Query executada em tempo real
-   Sempre dados atuais
-   Sem overhead de refresh

**Materialized Views (futuro, se necessário):**

-   Dados pré-computados (cache)
-   Precisa `REFRESH MATERIALIZED VIEW`
-   Usar se queries demorarem >2s

### Partitioning (Futuro)

Se o volume crescer (>1M tickets):

-   Particionar `tickets` por data (`created_at`) - mensal ou anual
-   Particionar `activity_log` por mês
-   Particionar `comments` por `ticket_id` range

---

## Migrations Strategy

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
10. database_views (Views)
11. database_triggers (Triggers + Functions)
12. database_constraints (Check constraints)
13. database_indexes_advanced (Partial, Composite, Expression)
```

### Criar Migrations

```bash
# Views
php artisan make:migration create_database_views

# Triggers & Functions
php artisan make:migration create_database_triggers

# Constraints
php artisan make:migration add_check_constraints_to_tables

# Indexes avançados
php artisan make:migration add_advanced_indexes_to_tables

# Stored Procedures
php artisan make:migration create_stored_procedures
```

---

## Conclusão

Este schema foi desenhado para nível **Enterprise-Grade**:

✅ **Performance:**

-   Views pré-computadas (Dashboard, SLA, Agent performance)
-   Indexes estratégicos (Partial, Composite, Expression, GIN)
-   Triggers para automação (zero overhead PHP)

✅ **Escalabilidade:**

-   Estrutura normalizada (3NF)
-   Partitioning ready
-   Stored Procedures para lógica complexa

✅ **Auditoria:**

-   Soft deletes
-   Activity log automático (triggers)
-   Status change tracking

✅ **Flexibilidade:**

-   JSONB para custom_fields
-   Views customizáveis
-   Extensível com novas triggers

✅ **Data Integrity:**

-   Check constraints (validation em DB)
-   Foreign keys com CASCADE
-   Triggers de validação (ex: agent assignment)

✅ **Best Practices:**

-   Convenções Laravel
-   Spatie packages integration
-   PostgreSQL 16 features (JSONB, GIN, Full-text)
-   DRY via Stored Procedures

O schema suporta todos os requisitos funcionais do OrionOne enquanto mantém performance, manutenibilidade e **preparação para escala enterprise**.
