# Planeamento de Desenvolvimento - OrionOne

## Visão Geral

Este documento estabelece o roadmap, metas, sprints e cronograma de desenvolvimento do projeto OrionOne, cobrindo o período de **Novembro 2025 a Janeiro 2026** (2.5 meses para MVP).

**Objetivo Principal:** Entregar um MVP funcional de plataforma ITSM com funcionalidades core de gestão de tickets, equipas e knowledge base, demonstrável ao júri do projeto final.

---

## Cronograma Geral

| Fase                              | Período                   | Duração   | Objetivo                                         |
| --------------------------------- | ------------------------- | --------- | ------------------------------------------------ |
| **Setup & Fundações**             | 01-10 Nov 2025            | 10 dias   | Ambiente, arquitetura, documentação              |
| **Sprint 1: Auth & Users**        | 11-17 Nov 2025            | 1 semana  | Sistema de autenticação e gestão de utilizadores |
| **Sprint 2: Tickets Core**        | 18 Nov - 01 Dez 2025      | 2 semanas | CRUD de tickets, states, assignment              |
| **Sprint 3: Colaboração**         | 02-15 Dez 2025            | 2 semanas | Comentários, notificações, equipas               |
| **Sprint 4: Knowledge Base**      | 16-29 Dez 2025            | 2 semanas | Artigos, categorias, search                      |
| **Sprint 5: Dashboard & Reports** | 30 Dez 2025 - 12 Jan 2026 | 2 semanas | Analytics, métricas, SLA tracking                |
| **Sprint 6: Polish & Deploy**     | 13-26 Jan 2026            | 2 semanas | Refinamento, testes, deployment                  |

**Data de Entrega:** 27 Janeiro 2026

---

## Fase 0: Setup & Fundações [COMPLETE]

**Status:** Concluída (01-10 Nov 2025)

### Objetivos Alcançados

-   [x] Docker Compose setup (5 containers)
-   [x] Laravel 11 + Vue 3 + Inertia.js configurado
-   [x] PostgreSQL 16 + Redis integrados
-   [x] Ferramentas de desenvolvimento (PHPStan, Pint, PHPUnit)
-   [x] Documentação inicial (architecture, requirements, development-guide)
-   [x] Scripts de automação (feature.ps1, feature.sh)
-   [x] Laravel Telescope para debugging
-   [x] Spatie Permission + Activity Log instalados

### Entregáveis

-   [x] `docker-compose.yml` funcional
-   [x] Dockerfile otimizado
-   [x] Documentação em `docs/`
-   [x] CI/CD pipeline (GitHub Actions) - PENDENTE
-   [x] README com badges e instruções

---

## Sprint 1: Auth & Users

**Período:** 11-17 Novembro 2025 (1 semana)
**Status:** EM PROGRESSO

### Objetivos

Implementar sistema completo de autenticação, autorização e gestão de utilizadores com roles e permissions.

### User Stories

#### US1.1: Autenticação Básica

**Como** visitante
**Quero** registar-me e fazer login
**Para** aceder à plataforma

**Critérios de Aceitação:**

-   [ ] Página de registo com validação (name, email, password)
-   [ ] Página de login
-   [ ] Verificação de email obrigatória
-   [ ] Recuperação de password via email
-   [ ] Logout seguro
-   [ ] Redirecionamento após login baseado em role

#### US1.2: Sistema de Roles

**Como** administrador
**Quero** atribuir roles aos utilizadores
**Para** controlar níveis de acesso

**Critérios de Aceitação:**

-   [ ] 3 roles: Admin, Agent, User
-   [ ] Seeder com roles e permissions predefinidos
-   [ ] Interface para atribuir roles (Admin panel)
-   [ ] Middleware para proteção de rotas por role

#### US1.3: Gestão de Perfil

**Como** utilizador autenticado
**Quero** editar o meu perfil
**Para** manter informações atualizadas

**Critérios de Aceitação:**

-   [ ] Editar nome, email, avatar
-   [ ] Alterar password (com confirmação da atual)
-   [ ] Upload de avatar (validação: max 2MB, jpg/png)
-   [ ] Validação de email único

### Tarefas Técnicas

**Backend:**

-   [ ] Migration `users` (já existe, revisar campos)
-   [ ] UserFactory com dados realistas
-   [ ] UserSeeder (10 admins, 20 agents, 50 users)
-   [ ] UserController (profile, update, avatar upload)
-   [ ] UserPolicy (view, update own profile)
-   [ ] Tests: UserTest, UserPolicyTest (90%+ coverage)

**Frontend:**

-   [ ] Login.vue (Inertia page)
-   [ ] Register.vue
-   [ ] ForgotPassword.vue
-   [ ] Profile.vue
-   [ ] Components: AvatarUpload.vue, PasswordInput.vue

**Integração:**

-   [ ] Email notifications (VerifyEmail, ResetPassword)
-   [ ] Spatie Permission setup
-   [ ] Activity log para login/logout

### Definition of Done

-   [ ] Todos os testes passam (>90% coverage)
-   [ ] PHPStan level 5 sem erros
-   [ ] Laravel Pint formatação OK
-   [ ] Frontend responsivo (mobile-first)
-   [ ] Documentação atualizada
-   [ ] Demo funcional para stakeholder

---

## Sprint 2: Tickets Core

**Período:** 18 Nov - 01 Dezembro 2025 (2 semanas)
**Status:** PLANEADA

### Objetivos

Implementar CRUD completo de tickets com estados, prioridades, atribuição e SLA tracking.

### User Stories

#### US2.1: Criar Ticket

**Como** utilizador autenticado
**Quero** criar um ticket de suporte
**Para** reportar um problema ou solicitar ajuda

**Critérios de Aceitação:**

-   [ ] Formulário: título, descrição, prioridade
-   [ ] Validação: título obrigatório (max 255), descrição (min 10 chars)
-   [ ] Auto-geração de ticket_number (TKT-000001)
-   [ ] Upload de anexos (opcional, max 10MB, 5 ficheiros)
-   [ ] Auto-assignment a equipa baseado em categoria (se configurado)
-   [ ] Email enviado ao agent/equipa
-   [ ] Redirect para página do ticket criado

#### US2.2: Listar Tickets

**Como** utilizador
**Quero** ver lista dos meus tickets
**Para** acompanhar o estado dos pedidos

**Critérios de Aceitação:**

-   [ ] Lista paginada (20 por página)
-   [ ] Filtros: status, prioridade, equipa, data
-   [ ] Search por ticket_number ou título
-   [ ] Ordenação: criação, atualização, prioridade
-   [ ] Badge visual para status e prioridade
-   [ ] Counter de tickets por status (dashboard widget)

#### US2.3: Ver Detalhes de Ticket

**Como** utilizador
**Quero** ver todos os detalhes de um ticket
**Para** entender o histórico e estado atual

**Critérios de Aceitação:**

-   [ ] Info completa: número, título, descrição, status, prioridade
-   [ ] Requester info (nome, avatar)
-   [ ] Assigned agent/team (se aplicável)
-   [ ] Timeline de mudanças de estado
-   [ ] SLA deadlines (1ª resposta, resolução)
-   [ ] Anexos downloadable
-   [ ] Activity log (via Spatie)

#### US2.4: Atualizar Ticket (Agent)

**Como** agent
**Quero** atualizar o estado do ticket
**Para** refletir progresso da resolução

**Critérios de Aceitação:**

-   [ ] Alterar status: Open → In Progress → Resolved → Closed
-   [ ] Alterar prioridade
-   [ ] Reatribuir a outro agent/equipa
-   [ ] Adicionar tags/labels
-   [ ] Marcar como escalated
-   [ ] Validação: apenas agents podem mudar status
-   [ ] Email ao requester em mudanças críticas

#### US2.5: Auto-Assignment

**Como** sistema
**Quero** atribuir tickets automaticamente
**Para** distribuir carga de trabalho

**Critérios de Aceitação:**

-   [ ] Lógica: round-robin por equipa
-   [ ] Respeitar disponibilidade do agent (is_active)
-   [ ] Fallback: atribuir apenas à equipa se sem agents disponíveis
-   [ ] Configurável por categoria (Hardware → Team Hardware)
-   [ ] Notificação ao agent atribuído

### Tarefas Técnicas

**Migrations:**

-   [ ] `create_tickets_table`
-   [ ] `create_ticket_attachments_table`

**Models & Relations:**

-   [ ] Ticket model (fillable, casts, relationships, scopes)
-   [ ] TicketAttachment model
-   [ ] TicketFactory (realistic data: 100 tickets)
-   [ ] TicketSeeder

**Backend:**

-   [ ] TicketController (index, create, store, show, edit, update, destroy)
-   [ ] StoreTicketRequest, UpdateTicketRequest
-   [ ] TicketService (createTicket, assignTicket, resolveTicket)
-   [ ] AssignmentService (auto-assignment logic)
-   [ ] SLAService (calculate deadlines)
-   [ ] TicketPolicy (view, create, update, delete)
-   [ ] TicketObserver (auto-generate ticket_number, log changes)

**Frontend:**

-   [ ] Tickets/Index.vue (lista + filtros)
-   [ ] Tickets/Create.vue
-   [ ] Tickets/Show.vue
-   [ ] Tickets/Edit.vue (Agent only)
-   [ ] Components: TicketCard, StatusBadge, PriorityBadge, FileUpload

**Tests:**

-   [ ] TicketTest (CRUD, validations, authorization)
-   [ ] TicketServiceTest (business logic)
-   [ ] TicketPolicyTest
-   [ ] AssignmentServiceTest

### Definition of Done

-   [ ] CRUD completo funcional
-   [ ] Auto-assignment testado com 3 cenários
-   [ ] SLA deadlines calculados corretamente
-   [ ] Tests >90% coverage
-   [ ] Frontend responsivo e acessível
-   [ ] Performance: lista de 1000 tickets < 200ms

---

## Sprint 3: Colaboração (Comments + Teams + Notifications) 💬

**Período:** 02-15 Dezembro 2025 (2 semanas)
**Status:** PLANEADA

### Objetivos

Implementar sistema de comentários (públicos/internos), gestão de equipas e notificações em tempo real.

### User Stories

#### US3.1: Comentários em Tickets

**Como** utilizador
**Quero** adicionar comentários a tickets
**Para** comunicar com o suporte

**Critérios de Aceitação:**

-   [ ] Form de comentário na página do ticket
-   [ ] Comentários públicos (visíveis ao requester)
-   [ ] Comentários internos (só agents/admin) - checkbox "Internal note"
-   [ ] Rich text editor (Markdown support)
-   [ ] Editar comentário (15min window, apenas autor)
-   [ ] Soft delete de comentários
-   [ ] Timestamp de criação/edição
-   [ ] Notificação ao requester em novos comentários públicos

#### US3.2: Gestão de Equipas

**Como** administrador
**Quero** criar e gerir equipas
**Para** organizar agents por especialização

**Critérios de Aceitação:**

-   [ ] CRUD de equipas (nome, descrição, email, slug)
-   [ ] Atribuir agents a equipas (many-to-many)
-   [ ] Definir team lead (role especial)
-   [ ] Listar tickets da equipa
-   [ ] Estatísticas por equipa (tickets abertos, resolvidos, tempo médio)

#### US3.3: Notificações

**Como** utilizador
**Quero** receber notificações de atividade
**Para** estar informado sobre os meus tickets

**Critérios de Aceitação:**

-   [ ] Email notifications:
    -   Ticket criado (ao agent/equipa)
    -   Ticket atribuído (ao agent)
    -   Novo comentário (ao requester)
    -   Status changed (ao requester)
    -   SLA violation warning
-   [ ] In-app notifications (Bell icon no navbar)
-   [ ] Marcação de notificações como lidas
-   [ ] Preferências de notificações (user settings)

### Tarefas Técnicas

**Migrations:**

-   [ ] `create_teams_table`
-   [ ] `create_team_user_table` (pivot)
-   [ ] `create_comments_table`
-   [ ] `create_notifications_table` (Laravel default)

**Models:**

-   [ ] Team, TeamFactory, TeamSeeder
-   [ ] Comment, CommentFactory, CommentSeeder
-   [ ] Notifications (usar Laravel Notifications)

**Backend:**

-   [ ] TeamController, CommentController
-   [ ] TeamService, CommentService
-   [ ] Notifications: TicketCreated, TicketAssigned, CommentAdded, SLAViolation
-   [ ] Policies: TeamPolicy, CommentPolicy
-   [ ] Observer: CommentObserver (trigger notifications)

**Frontend:**

-   [ ] Teams/Index.vue, Teams/Create.vue, Teams/Show.vue
-   [ ] Comments/CommentList.vue, Comments/CommentForm.vue
-   [ ] Notifications/NotificationDropdown.vue
-   [ ] MarkdownEditor.vue component

**Tests:**

-   [ ] CommentTest, TeamTest
-   [ ] NotificationTest (assert email sent)
-   [ ] > 90% coverage

### Definition of Done

-   [ ] Comentários públicos/internos funcionais
-   [ ] Equipas com members e lead
-   [ ] Email notifications enviados corretamente
-   [ ] In-app notifications com badge de contagem
-   [ ] Tests passam
-   [ ] Performance: carregar 50 comentários < 100ms

---

## Sprint 4: Knowledge Base 📚

**Período:** 16-29 Dezembro 2025 (2 semanas)
**Status:** PLANEADA

### Objetivos

Implementar base de conhecimento pública com artigos, categorias hierárquicas e pesquisa full-text.

### User Stories

#### US4.1: Ver Knowledge Base

**Como** visitante
**Quero** aceder à base de conhecimento
**Para** resolver problemas sem criar ticket

**Critérios de Aceitação:**

-   [ ] Homepage da KB com categorias
-   [ ] Listagem de artigos por categoria
-   [ ] Artigos em destaque (featured)
-   [ ] Pesquisa full-text (título + conteúdo)
-   [ ] Ordenação por relevância, popularidade, data
-   [ ] Feedback "Foi útil?" (Yes/No buttons)
-   [ ] Contador de visualizações

#### US4.2: Criar Artigos (Agent)

**Como** agent
**Quero** criar artigos na KB
**Para** partilhar soluções comuns

**Critérios de Aceitação:**

-   [ ] Form: título, conteúdo (Markdown), categoria, excerpt
-   [ ] Rascunhos (is_published = false)
-   [ ] Preview antes de publicar
-   [ ] SEO: slug auto-gerado, meta description
-   [ ] Upload de imagens inline
-   [ ] Versionamento (opcional para MVP)

#### US4.3: Gestão de Categorias

**Como** administrador
**Quero** criar categorias hierárquicas
**Para** organizar a KB

**Critérios de Aceitação:**

-   [ ] CRUD de categorias
-   [ ] Hierarquia: categorias pai e filhas
-   [ ] Ícones customizáveis (Heroicons)
-   [ ] Ordenação manual (drag-and-drop opcional)
-   [ ] Visibilidade (show/hide)

### Tarefas Técnicas

**Migrations:**

-   [ ] `create_categories_table`
-   [ ] `create_articles_table`

**Models:**

-   [ ] Category (self-referencing relationship), CategoryFactory, CategorySeeder
-   [ ] Article, ArticleFactory, ArticleSeeder (30 artigos)

**Backend:**

-   [ ] ArticleController, CategoryController
-   [ ] ArticleService (publish, unpublish, trackView, recordFeedback)
-   [ ] Search service (PostgreSQL full-text search)
-   [ ] ArticlePolicy (create, publish, edit)
-   [ ] ArticleObserver (auto-slug, update published_at)

**Frontend:**

-   [ ] KB/Index.vue (homepage com categorias)
-   [ ] KB/CategoryShow.vue (artigos da categoria)
-   [ ] KB/ArticleShow.vue (visualização de artigo)
-   [ ] KB/ArticleCreate.vue, KB/ArticleEdit.vue (Agent only)
-   [ ] Search/SearchResults.vue
-   [ ] MarkdownRenderer.vue

**Tests:**

-   [ ] ArticleTest, CategoryTest
-   [ ] SearchTest (test full-text search)
-   [ ] > 90% coverage

### Definition of Done

-   [ ] KB pública acessível sem login
-   [ ] Pesquisa full-text funcional (PostgreSQL)
-   [ ] Feedback "Was this helpful?" com persistência
-   [ ] Artigos renderizam Markdown corretamente
-   [ ] SEO-friendly URLs (slugs)
-   [ ] Performance: pesquisa em 1000 artigos < 150ms

---

## Sprint 5: Dashboard & Reports

**Duração:** 30 Dez - 05 Janeiro (1 semana)
**Status:** PLANEADA

### Objetivos

Implementar dashboards para Admin e Agent com métricas, gráficos e SLA tracking.

### User Stories

#### US5.1: Dashboard de Agent

**Como** agent
**Quero** ver os meus tickets e KPIs
**Para** gerir workload

**Critérios de Aceitação:**

-   [ ] Widgets:
    -   Tickets atribuídos (Open, In Progress)
    -   Tickets perto de violar SLA (urgentes)
    -   Tickets resolvidos hoje/esta semana
    -   Tempo médio de resolução
-   [ ] Gráfico: tickets por status (pie chart)
-   [ ] Lista de últimos tickets atualizados
-   [ ] Acesso rápido a ações (criar ticket, ver KB)

#### US5.2: Dashboard de Admin

**Como** administrador
**Quero** ver métricas globais
**Para** monitorizar performance do sistema

**Critérios de Aceitação:**

-   [ ] Widgets:
    -   Total de tickets (hoje, semana, mês)
    -   Taxa de resolução
    -   SLA compliance rate
    -   Tickets por equipa
    -   Agents mais ativos
-   [ ] Gráficos:
    -   Tickets criados vs resolvidos (line chart, 30 dias)
    -   Tickets por prioridade (bar chart)
    -   Performance de SLA (gauge)
-   [ ] Tabela: equipas com mais tickets abertos

#### US5.3: Relatórios

**Como** administrador
**Quero** gerar relatórios customizados
**Para** análise de dados

**Critérios de Aceitação:**

-   [ ] Filtros: período, equipa, agent, status, prioridade
-   [ ] Exportação: PDF, CSV
-   [ ] Métricas calculadas:
    -   First Response Time (média)
    -   Resolution Time (média)
    -   Reopened tickets rate
    -   Customer satisfaction (baseado em feedback)
-   [ ] Agendamento de relatórios (email semanal) - OPCIONAL

### Tarefas Técnicas

**Backend:**

-   [ ] DashboardController (agentStats, adminStats)
-   [ ] ReportingService (generateReport, calculateMetrics)
-   [ ] SLAService (compliance calculations)
-   [ ] Export service (PDF com DOMPDF, CSV nativo)
-   [ ] Queries otimizadas (caching de 5min para dashboards)

**Frontend:**

-   [ ] Dashboard/AgentDashboard.vue
-   [ ] Dashboard/AdminDashboard.vue
-   [ ] Reports/ReportBuilder.vue
-   [ ] Charts: usar Chart.js ou ApexCharts
-   [ ] Components: StatCard, LineChart, PieChart, BarChart

**Tests:**

-   [ ] DashboardTest
-   [ ] ReportingServiceTest
-   [ ] Performance test: dashboard load < 300ms

### Definition of Done

-   [ ] Dashboards carregam em <300ms
-   [ ] Gráficos responsivos (mobile-friendly)
-   [ ] Exportação de relatórios funcional
-   [ ] Caching implementado para queries pesadas
-   [ ] Tests >85% coverage (frontend charts complexo)

---

## Sprint 6: Polish & Deploy

**Duração:** 06-12 Janeiro (1 semana)
**Status:** PLANEADA

### Objetivos

Refinamento final, otimização de performance, testes E2E, deployment e preparação para apresentação.

### Tarefas

**Refinamento:**

-   [ ] UI/UX polish (feedback de utilizador teste)
-   [ ] Loading states e skeletons
-   [ ] Error handling user-friendly
-   [ ] Toast notifications (success, error, info)
-   [ ] Tooltips e help text
-   [ ] Accessibility audit (WCAG AA)
-   [ ] Mobile responsiveness full check

**Performance:**

-   [ ] Laravel query optimization (N+1 queries)
-   [ ] Redis caching estratégico
-   [ ] Lazy loading de imagens
-   [ ] Minify CSS/JS (Vite build)
-   [ ] Database indexes review
-   [ ] Load testing (100 utilizadores concorrentes)

**Testes:**

-   [ ] E2E tests com Playwright/Cypress (critical paths)
-   [ ] Smoke tests automatizados
-   [ ] Security audit (OWASP Top 10)
-   [ ] Penetration testing básico

**Deployment:**

-   [ ] Setup CI/CD (GitHub Actions)
-   [ ] Deploy para staging (Railway, Fly.io ou VPS)
-   [ ] Configuração de domínio
-   [ ] SSL certificates
-   [ ] Monitoring (Laravel Pulse ou Sentry)
-   [ ] Backup strategy

**Documentação:**

-   [ ] User manual (PDF ou KB articles)
-   [ ] API documentation (L5-Swagger)
-   [ ] Deployment guide
-   [ ] Video demo (5-10 min)
-   [ ] Slides para apresentação

### Definition of Done

-   [ ] Aplicação deployada e acessível online
-   [ ] Zero critical bugs
-   [ ] Performance: todas as páginas < 500ms
-   [ ] Lighthouse score > 90 (Performance, Accessibility)
-   [ ] Documentação completa
-   [ ] Apresentação preparada

---

## Métricas de Sucesso

### KPIs Técnicos

| Métrica                | Target  | Como Medir                        |
| ---------------------- | ------- | --------------------------------- |
| **Test Coverage**      | >90%    | PHPUnit `--coverage`              |
| **PHPStan Level**      | Level 5 | `phpstan analyse`                 |
| **Page Load Time**     | <500ms  | Laravel Debugbar, Chrome DevTools |
| **Lighthouse Score**   | >90     | Chrome Lighthouse                 |
| **Zero Critical Bugs** | 0       | Bug tracker, QA testing           |
| **Code Style**         | 100%    | Laravel Pint (zero violations)    |

### KPIs de Projeto

| Métrica                                 | Target          | Status                   |
| --------------------------------------- | --------------- | ------------------------ |
| **Requisitos Funcionais Implementados** | 100% (15/15)    | [IN PROGRESS] 13% (2/15) |
| **Sprints no Prazo**                    | 100% (6/6)      | [ON TRACK] 16% (1/6)     |
| **Features Completas**                  | 6 features core | [IN PROGRESS] 1/6        |
| **Documentação Atualizada**             | 100%            | [GOOD] 90%               |
| **Deploy Successful**                   | 1 produção      | [PENDING] 0/1            |

---

## Riscos e Mitigações

### Riscos Técnicos

| Risco                  | Probabilidade | Impacto | Mitigação                                                        |
| ---------------------- | ------------- | ------- | ---------------------------------------------------------------- |
| **Atraso em Sprint**   | Média         | Alto    | Buffer de 2 dias entre sprints, features opcionais identificadas |
| **Bugs em Produção**   | Média         | Médio   | TDD rigoroso, staging environment, smoke tests                   |
| **Performance Issues** | Baixa         | Médio   | Caching estratégico, load testing antes deploy                   |
| **Falta de Testes**    | Baixa         | Alto    | TDD obrigatório, coverage gates no CI/CD                         |

### Riscos de Prazo

| Risco                 | Probabilidade | Impacto | Mitigação                                                      |
| --------------------- | ------------- | ------- | -------------------------------------------------------------- |
| **Época de Exames**   | Alta          | Alto    | Sprint 4 em Dezembro (férias), workload reduzido               |
| **Scope Creep**       | Média         | Alto    | Requisitos congelados após Sprint 2, backlog de "nice-to-have" |
| **Falta de Feedback** | Baixa         | Médio   | Demo semanal a stakeholder (orientador/colega)                 |

---

## Features Opcionais (Nice-to-Have)

Se houver tempo extra após MVP, considerar:

-   [ ] Chat em tempo real (websockets com Pusher/Laravel Echo)
-   [ ] Mobile app (React Native ou Progressive Web App)
-   [ ] Integrações (Slack, Microsoft Teams)
-   [ ] Multi-tenancy (SaaS model)
-   [ ] Custom workflows (ticket automation rules)
-   [ ] Time tracking por ticket
-   [ ] Customer portal (white-label)

---

## Cerimónias Agile (Solo Developer)

Mesmo como developer solo, manter disciplina Agile:

### Daily Standup (5 min)

-   **Quando:** Todos os dias, 9h
-   **O quê:** Rever todo list, priorizar tarefas do dia
-   **Ferramenta:** GitHub Projects ou Notion

### Sprint Review (30 min)

-   **Quando:** Última sexta-feira do sprint
-   **O quê:** Demo de features completadas, atualizar roadmap
-   **Stakeholder:** Orientador ou colega para feedback

### Sprint Retrospective (15 min)

-   **Quando:** Última sexta-feira do sprint
-   **O quê:** O que funcionou, o que melhorar, lições aprendidas
-   **Output:** Action items para próximo sprint

### Sprint Planning (1h)

-   **Quando:** Segunda-feira do novo sprint
-   **O quê:** Breakdown de user stories, estimativas, commitments
-   **Output:** Sprint backlog atualizado

---

## Ferramentas de Planeamento

### GitHub Projects

-   [x] Board Kanban (To Do, In Progress, Done, Blocked)
-   [ ] Milestones para cada Sprint
-   [ ] Labels: bug, feature, docs, enhancement, priority:high

### Notion (Opcional)

-   [ ] Sprint planning docs
-   [ ] Retrospective notes
-   [ ] Research & spikes

### Time Tracking

-   [ ] Toggl ou Clockify (opcional, para análise de tempo)
-   [ ] Objetivo: 20-25h/semana de desenvolvimento

---

## Checklist Final (Pré-Entrega)

### Funcionalidades Core

-   [ ] Autenticação e autorização
-   [ ] CRUD de tickets
-   [ ] Sistema de comentários
-   [ ] Gestão de equipas
-   [ ] Knowledge Base
-   [ ] Dashboard com métricas

### Qualidade de Código

-   [ ] Tests >90% coverage
-   [ ] PHPStan Level 5 clean
-   [ ] Laravel Pint formatação OK
-   [ ] Zero critical bugs
-   [ ] Security audit passed

### Deployment

-   [ ] Aplicação em produção
-   [ ] SSL configurado
-   [ ] Monitoring ativo
-   [ ] Backups automáticos

### Documentação

-   [ ] README atualizado
-   [ ] API docs (Swagger)
-   [ ] User manual
-   [ ] Deployment guide
-   [ ] Architecture diagrams atualizados

### Apresentação

-   [ ] Slides preparados (20-30 slides)
-   [ ] Demo video (5-10 min)
-   [ ] Script de apresentação
-   [ ] Q&A preparation

---

## Próximos Passos Imediatos

### Esta Semana (11-17 Nov)

1. Completar Sprint 1: Auth & Users
2. Setup de seeds com dados realistas
3. Tests de autenticação (>90% coverage)
4. Frontend: Login, Register, Profile pages

### Próxima Semana (18-24 Nov)

1. Iniciar Sprint 2: Tickets Core
2. Migrations de tickets e attachments
3. Backend: CRUD de tickets
4. Frontend: Listagem e criação de tickets

---

**Última Atualização:** 07 Novembro 2025
**Revisão:** v1.0
**Próxima Revisão:** 17 Novembro 2025 (fim Sprint 1)
