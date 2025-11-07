# Requisitos do Sistema OrionOne

## Visão Geral

Este documento especifica os requisitos funcionais (RF) e não funcionais (RNF) do sistema OrionOne - uma plataforma ITSM moderna para gestão de tickets de suporte técnico.

**Objetivo:** Desenvolver um sistema web de gestão de tickets que permita a criação, atribuição, acompanhamento e resolução de pedidos de suporte, com suporte a múltiplos utilizadores, equipas e níveis de acesso.

---

## Requisitos Funcionais

### RF01 - Autenticação e Autorização

**Descrição:** O sistema deve suportar autenticação segura com diferentes níveis de acesso.

**Critérios de Aceitação:**

-   Login com email e password
-   Recuperação de password via email
-   Verificação de email obrigatória
-   Logout seguro
-   Sistema de roles: Admin, Agent, User
-   Permissões granulares via Spatie Permission

**Prioridade:** Alta
**Complexidade:** Média

---

### RF02 - Gestão de Tickets

**Descrição:** O sistema deve permitir CRUD completo de tickets de suporte.

**Critérios de Aceitação:**

-   Criar ticket com título, descrição, prioridade
-   Visualizar lista de tickets (filtros: status, prioridade, equipa)
-   Visualizar detalhes de ticket individual
-   Editar ticket (título, descrição, prioridade, status)
-   Atribuir ticket a agent ou equipa
-   Alterar status: Open → In Progress → Resolved → Closed
-   Fechar/reabrir ticket
-   Soft delete (manter histórico)
-   Geração automática de ticket_number (TKT-000001)

**Regras de Negócio:**

-   User pode criar tickets
-   User pode ver apenas os seus tickets
-   Agent pode ver tickets da sua equipa
-   Admin pode ver todos os tickets
-   Apenas Agent/Admin podem alterar status

**Prioridade:** Alta
**Complexidade:** Alta

---

### RF03 - Sistema de Comentários

**Descrição:** Utilizadores devem poder adicionar comentários públicos e internos aos tickets.

**Critérios de Aceitação:**

-   Adicionar comentário a ticket
-   Comentários públicos (visíveis ao requester)
-   Comentários internos (apenas Agent/Admin)
-   Editar comentário (apenas autor, dentro de 15min)
-   Soft delete de comentários
-   Timestamp de criação/edição
-   Notificação ao requester em novos comentários públicos

**Prioridade:** Alta
**Complexidade:** Média

---

### RF04 - Gestão de Equipas

**Descrição:** Organização de agents em equipas especializadas.

**Critérios de Aceitação:**

-   Criar/editar/eliminar equipas
-   Atribuir agents a equipas (many-to-many)
-   Definir team lead
-   Categorias de equipas (Hardware, Software, Network, etc)
-   Email da equipa
-   Estatísticas por equipa

**Prioridade:** Média
**Complexidade:** Média

---

### RF05 - Atribuição de Tickets

**Descrição:** Sistema de atribuição automática e manual de tickets.

**Critérios de Aceitação:**

-   Atribuição manual (Admin/Team Lead escolhe agent)
-   Atribuição automática baseada em:
    -   Keywords no título/descrição
    -   Carga de trabalho do agent (round-robin)
    -   Especialização da equipa
-   Reatribuição de tickets
-   Histórico de atribuições

**Prioridade:** Média
**Complexidade:** Alta

---

### RF06 - SLA Tracking

**Descrição:** Gestão de Service Level Agreements com deadlines e alertas.

**Critérios de Aceitação:**

-   Cálculo automático de deadlines baseado em prioridade:
    -   **Urgent:** 2h primeira resposta, 8h resolução
    -   **High:** 4h primeira resposta, 24h resolução
    -   **Medium:** 8h primeira resposta, 48h resolução
    -   **Low:** 24h primeira resposta, 5 dias resolução
-   Excluir fins de semana do cálculo
-   Alertas de violação de SLA
-   Dashboard com métricas de SLA
-   Campo `is_escalated` para tickets com SLA violado

**Prioridade:** Média
**Complexidade:** Alta

---

### RF07 - Knowledge Base

**Descrição:** Base de conhecimento para self-service e redução de tickets.

**Critérios de Aceitação:**

-   Criar/editar/eliminar artigos
-   Sistema de categorias hierárquico
-   Editor de conteúdo (Markdown/WYSIWYG)
-   Sistema de publicação (draft/published)
-   Pesquisa full-text (PostgreSQL)
-   Contador de visualizações
-   Feedback "Foi útil?" (Sim/Não)
-   Artigos destacados (featured)
-   SEO-friendly URLs (slugs)

**Prioridade:** Média
**Complexidade:** Média

---

### RF08 - Dashboard e Métricas

**Descrição:** Visão geral de estatísticas e KPIs do sistema.

**Critérios de Aceitação:**

-   Tickets por status (gráfico)
-   Tickets por prioridade
-   Tickets por equipa
-   Performance de SLA (% compliance)
-   Tempo médio de resolução
-   Tickets abertos vs fechados (timeline)
-   Top agents (mais tickets resolvidos)
-   Filtros por período (hoje, semana, mês, ano)

**Prioridade:** Média
**Complexidade:** Média

---

### RF09 - Notificações

**Descrição:** Sistema de notificações por email e in-app.

**Critérios de Aceitação:**

-   Email ao criar ticket (para requester)
-   Email ao atribuir ticket (para agent)
-   Email em novo comentário público (para requester)
-   Email em SLA breach warning
-   Email ao resolver ticket (para requester)
-   Notificações in-app (database notifications)
-   Configuração de preferências de notificação

**Prioridade:** Baixa
**Complexidade:** Média

---

### RF10 - Activity Log (Auditoria)

**Descrição:** Registo automático de todas as ações críticas no sistema.

**Critérios de Aceitação:**

-   Log de criação/edição/eliminação de tickets
-   Log de atribuições
-   Log de mudanças de status
-   Log de comentários
-   Armazenar: quem, o quê, quando, antes/depois
-   Interface de visualização de histórico
-   Integração com Spatie Activity Log

**Prioridade:** Baixa
**Complexidade:** Baixa

---

### RF11 - Gestão de Utilizadores (Admin)

**Descrição:** Administração de utilizadores do sistema.

**Critérios de Aceitação:**

-   Listar utilizadores
-   Criar/editar utilizador
-   Ativar/desativar conta
-   Atribuir roles e permissões
-   Adicionar utilizador a equipas
-   Reset password (Admin)

**Prioridade:** Baixa
**Complexidade:** Baixa

---

### RF12 - Pesquisa Global

**Descrição:** Busca rápida em tickets e knowledge base.

**Critérios de Aceitação:**

-   Pesquisa por ticket_number
-   Pesquisa por título/descrição
-   Pesquisa em artigos da KB
-   Resultados ordenados por relevância
-   Highlighting de termos pesquisados

**Prioridade:** Baixa
**Complexidade:** Média

---

## Requisitos Não Funcionais

### RNF01 - Performance

**Descrição:** O sistema deve responder rapidamente às ações dos utilizadores.

**Critérios de Aceitação:**

-   Tempo de resposta < 2 segundos em 95% dos requests
-   Tempo de carregamento inicial < 3 segundos
-   Suporte a 100+ utilizadores simultâneos
-   Queries otimizadas (indexes, eager loading)
-   Cache de queries frequentes (Redis, 5-15min TTL)
-   Lazy loading de listas longas

**Métricas:**

-   Response time médio: < 500ms
-   Database queries por request: < 15
-   Memory usage: < 512MB por processo PHP

---

### RNF02 - Segurança

**Descrição:** Proteção contra vulnerabilidades comuns e dados sensíveis.

**Critérios de Aceitação:**

-   Passwords armazenadas com hash bcrypt
-   CSRF protection em todos os formulários
-   SQL injection prevention (Eloquent ORM)
-   XSS protection (automatic escaping)
-   Rate limiting por IP (60 requests/min)
-   HTTPS obrigatório em produção
-   Validação de inputs (server-side)
-   Autorização granular (Policies)
-   Session security (httpOnly cookies)

**Compliance:**

-   Seguir OWASP Top 10
-   PSR-12 coding standards

---

### RNF03 - Usabilidade

**Descrição:** Interface intuitiva e responsiva.

**Critérios de Aceitação:**

-   Design responsivo (mobile, tablet, desktop)
-   Compatibilidade com browsers modernos (Chrome, Firefox, Safari, Edge)
-   Acessibilidade WCAG 2.1 AA
-   Feedback visual em ações (loading, success, error)
-   Mensagens de erro claras
-   Navegação intuitiva (max 3 cliques para qualquer ação)
-   Atalhos de teclado para ações comuns

**UX Guidelines:**

-   Consistência visual (Tailwind CSS)
-   Ícones claros (Heroicons)
-   Tooltips explicativos

---

### RNF04 - Escalabilidade

**Descrição:** Sistema preparado para crescimento de utilizadores e dados.

**Critérios de Aceitação:**

-   Arquitetura horizontal scaling ready
-   Sessões em Redis (partilhadas entre servidores)
-   Queue jobs assíncronos (emails, reports)
-   Database connection pooling
-   Soft deletes (preservar histórico)
-   Partitioning strategy (futuro: particionar tickets por ano)

**Capacidade:**

-   Suportar 10,000+ tickets sem degradação
-   Suportar 1,000+ utilizadores

---

### RNF05 - Manutenibilidade

**Descrição:** Código limpo, testável e documentado.

**Critérios de Aceitação:**

-   Arquitetura MVC + Service Layer
-   Separation of concerns (Controllers thin)
-   Dependency Injection
-   Testes automatizados (Unit + Feature)
-   Coverage mínimo: 70%
-   Documentação técnica (architecture.md, schema.md)
-   Conventional Commits
-   Code review obrigatório

**Standards:**

-   PSR-12 (PHP)
-   ESLint (JavaScript)
-   Prettier (formatting)

---

### RNF06 - Disponibilidade

**Descrição:** Sistema disponível 24/7 com mínimo downtime.

**Critérios de Aceitação:**

-   Uptime target: 99% (7.2h downtime/mês aceitável)
-   Backups automáticos diários (PostgreSQL)
-   Healthchecks (database, redis, app)
-   Graceful degradation (se Redis falhar, usar database sessions)
-   Error logging (Telescope, Laravel Log)
-   Monitoring (Uptime Kuma / New Relic)

**Recovery:**

-   RTO (Recovery Time Objective): < 4h
-   RPO (Recovery Point Objective): < 24h

---

### RNF07 - Portabilidade

**Descrição:** Fácil deployment em diferentes ambientes.

**Critérios de Aceitação:**

-   Docker setup completo (4 containers)
-   Environment variables (.env)
-   Database migrations versionadas
-   Seeders para dados de teste
-   Documentação de deployment
-   CI/CD ready (GitHub Actions)

**Ambientes suportados:**

-   Local (Laragon, XAMPP, Docker)
-   Produção (VPS, Cloud)

---

### RNF08 - Compatibilidade

**Descrição:** Requisitos de tecnologia e dependências.

**Versões mínimas:**

-   **PHP:** 8.2+
-   **PostgreSQL:** 16+
-   **Redis:** 7+
-   **Node.js:** 20 LTS
-   **Composer:** 2.x
-   **NPM:** 10+

**Browsers suportados:**

-   Chrome 100+
-   Firefox 100+
-   Safari 15+
-   Edge 100+

---

## Matriz de Prioridades

| Requisito             | Prioridade | Complexidade | Sprint |
| --------------------- | ---------- | ------------ | ------ |
| RF01 - Autenticação   | Alta       | Média        | 1      |
| RF02 - Gestão Tickets | Alta       | Alta         | 1-2    |
| RF03 - Comentários    | Alta       | Média        | 2      |
| RF04 - Equipas        | Média      | Média        | 3      |
| RF05 - Atribuição     | Média      | Alta         | 3      |
| RF06 - SLA            | Média      | Alta         | 4      |
| RF07 - Knowledge Base | Média      | Média        | 5      |
| RF08 - Dashboard      | Média      | Média        | 6      |
| RF09 - Notificações   | Baixa      | Média        | 7      |
| RF10 - Activity Log   | Baixa      | Baixa        | 8      |
| RF11 - Gestão Users   | Baixa      | Baixa        | 8      |
| RF12 - Pesquisa       | Baixa      | Média        | 9      |

**Duração estimada MVP:** 10 semanas (2.5 meses)

---

## Casos de Uso Principais

### UC01 - Criar Ticket (User)

1. User faz login
2. Clica em "Novo Ticket"
3. Preenche título, descrição, prioridade
4. Submete formulário
5. Sistema valida dados
6. Sistema cria ticket com status "Open"
7. Sistema auto-atribui a equipa baseada em keywords
8. Sistema calcula SLA deadlines
9. Sistema envia email ao requester (confirmação)
10. Sistema envia notificação à equipa atribuída

### UC02 - Resolver Ticket (Agent)

1. Agent vê lista de tickets atribuídos
2. Seleciona ticket
3. Adiciona comentário interno (análise do problema)
4. Adiciona comentário público (resposta ao requester)
5. Altera status para "Resolved"
6. Sistema regista `resolved_at` timestamp
7. Sistema envia email ao requester
8. Sistema atualiza métricas de SLA

### UC03 - Pesquisar Solução (User)

1. User acede a Knowledge Base
2. Pesquisa por keyword ("reset password")
3. Sistema retorna artigos relevantes
4. User clica em artigo
5. Sistema incrementa contador de views
6. User lê solução
7. User marca como "útil" ou "não útil"
8. Sistema atualiza rating do artigo

---

## Glossário

-   **Agent:** Utilizador técnico que resolve tickets
-   **Requester:** Utilizador que criou o ticket
-   **SLA:** Service Level Agreement - acordo de tempo de resposta
-   **Escalation:** Ticket atribuído a nível superior (manager)
-   **Knowledge Base:** Base de conhecimento com artigos de self-service
-   **Soft Delete:** Eliminação lógica (flag deleted_at) sem remover dados

---

## Referências

-   [Laravel 11 Documentation](https://laravel.com/docs/11.x)
-   [PostgreSQL 16 Documentation](https://www.postgresql.org/docs/16/)
-   [OWASP Top 10](https://owasp.org/www-project-top-ten/)
-   [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
