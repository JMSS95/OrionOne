# Database Schema - OrionOne

## Diagrama ER

```
┌─────────┐       ┌──────────┐       ┌─────────┐
│  users  │──────<│ tickets  │>──────│  teams  │
└────┬────┘       └────┬─────┘       └─────────┘
     │                 │
     │            ┌────▼─────┐
     │            │ comments │
     │            └──────────┘
     │
     │            ┌──────────┐       ┌────────────┐
     └───────────<│ articles │>──────│ categories │
                  └──────────┘       └────────────┘
```

## Tabelas Principais

### users

| Campo    | Tipo         | Descrição          |
| -------- | ------------ | ------------------ |
| id       | BIGSERIAL    | Primary key        |
| name     | VARCHAR(255) | Nome do utilizador |
| email    | VARCHAR(255) | Email (único)      |
| password | VARCHAR(255) | Password hash      |

### tickets

| Campo         | Tipo         | Descrição                           |
| ------------- | ------------ | ----------------------------------- |
| id            | BIGSERIAL    | Primary key                         |
| ticket_number | VARCHAR(20)  | Número único (TKT-000001)           |
| title         | VARCHAR(255) | Título do ticket                    |
| description   | TEXT         | Descrição detalhada                 |
| status        | VARCHAR(50)  | open, in_progress, resolved, closed |
| priority      | VARCHAR(50)  | low, medium, high, urgent           |
| requester_id  | BIGINT FK    | Quem criou (users.id)               |
| assigned_to   | BIGINT FK    | Agent atribuído (users.id)          |
| team_id       | BIGINT FK    | Equipa responsável (teams.id)       |

### comments

| Campo       | Tipo      | Descrição               |
| ----------- | --------- | ----------------------- |
| id          | BIGSERIAL | Primary key             |
| ticket_id   | BIGINT FK | Ticket relacionado      |
| user_id     | BIGINT FK | Autor do comentário     |
| content     | TEXT      | Conteúdo                |
| is_internal | BOOLEAN   | Visível só para agents? |

## Indexes

```sql
-- Performance indexes
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_requester ON tickets(requester_id);
CREATE INDEX idx_tickets_assigned ON tickets(assigned_to);
CREATE INDEX idx_comments_ticket ON comments(ticket_id);
```
