# Modelo de Negócio - OrionOne

## Executive Summary

OrionOne é uma plataforma ITSM (IT Service Management) moderna, desenvolvida como alternativa acessível a soluções enterprise como ServiceNow, Zendesk e Jira Service Desk. O modelo de negócio foca em **SMEs (Small & Medium Enterprises)** e **startups** que necessitam de gestão profissional de suporte técnico sem o custo elevado das soluções enterprise.

**Proposta de Valor:** Plataforma ITSM completa, intuitiva e acessível, com todas as funcionalidades core a um preço justo, sem complexidade desnecessária.

---

## Value Proposition Canvas

### Customer Profile

#### Customer Jobs (O que os clientes precisam fazer)

-   Gerir tickets de suporte de forma organizada
-   Manter SLAs e métricas de qualidade
-   Colaborar em equipa na resolução de problemas
-   Reduzir volume de tickets repetitivos (knowledge base)
-   Monitorizar performance de equipas de suporte
-   Escalar processos de suporte sem contratar mais pessoas

#### Customer Pains (Problemas atuais)

-   **Soluções enterprise demasiado caras** (€50-150/user/mês)
-   **Curva de aprendizagem alta** (ServiceNow demora meses a dominar)
-   **Ferramentas genéricas inadequadas** (email, Excel, Trello não são feitos para ITSM)
-   **Falta de visibilidade** (gestores não sabem o estado do suporte)
-   **SLA violations frequentes** (sem alertas automáticos)
-   **Conhecimento disperso** (soluções em emails perdidos)

#### Customer Gains (Benefícios desejados)

-   Redução de custos (vs. Zendesk/ServiceNow)
-   Onboarding rápido (<1 dia para estar produtivo)
-   Interface intuitiva (como usar Gmail)
-   SLA tracking automático com alertas
-   Base de conhecimento que reduz tickets em 30%
-   Métricas e dashboards para decisões data-driven

### Value Map

#### Products & Services

-   **Ticket Management System** (CRUD, states, priorities, assignments)
-   **Team Collaboration** (comentários, notificações, @mentions)
-   **Knowledge Base** (artigos, categorias, pesquisa full-text)
-   **SLA Management** (tracking, alertas, compliance reports)
-   **Analytics & Reports** (dashboards, exportação, trends)
-   **Notifications** (email, in-app, webhooks)

#### Pain Relievers

-   **Pricing transparente** (3 tiers fixos, sem surpresas)
-   **Setup em 15 minutos** (vs. semanas do ServiceNow)
-   **Interface moderna** (Vue 3, Tailwind, mobile-first)
-   **Self-hosted option** (controlo total de dados)
-   **Open-source core** (community-driven, sem vendor lock-in)

#### Gain Creators

-   **ROI claro:** redução de 40% em custos de suporte (vs. Zendesk)
-   **Produtividade:** agents resolvem +25% tickets com KB
-   **Satisfação:** NPS >50 com interface intuitiva
-   **Escalabilidade:** suporta crescimento de 10 a 500 users sem re-platforming

---

## Business Model Canvas

### 1. Customer Segments

#### Segmento Primário: SMEs Tech-Savvy

-   **Tamanho:** 10-100 colaboradores
-   **Indústrias:** Tech startups, agências digitais, SaaS companies
-   **Características:**
    -   Equipa interna de IT/suporte (2-10 agents)
    -   Orçamento limitado (<€5k/ano para ITSM)
    -   Valorizem ferramentas modernas e developer-friendly
    -   Growth stage (escalabilidade é crítica)

**Exemplos de Clientes Ideais:**

-   Startup SaaS com 30 colaboradores e suporte Tier 1/2
-   Agência web com 50 colaboradores (suporte a clientes)
-   Scale-up fintech com 100 employees (IT Service Desk interno)

#### Segmento Secundário: Freelancers & Micro-empresas

-   **Tamanho:** 1-10 colaboradores
-   **Necessidade:** Gestão profissional de pedidos de clientes
-   **Preço:** Free tier ou Starter plan

#### Segmento Terciário: Instituições Educacionais

-   **Target:** Universidades, politécnicos, escolas técnicas
-   **Use case:** Service desk para alunos/docentes
-   **Vantagem:** Licença educacional com desconto (50%)

### 2. Value Propositions

**Slogan:** _"Enterprise ITSM, Startup Price"_

#### Para SMEs:

-   **Acessível:** 70% mais barato que Zendesk/ServiceNow
-   **Rápido:** Setup em <1 hora, onboarding em <1 dia
-   **Completo:** Todas as features críticas incluídas (não upsells)
-   **Escalável:** Cresce com a empresa (10 → 500 users)
-   **Moderno:** Stack tecnológico atual (Laravel 11, Vue 3)

#### Para Freelancers:

-   **Free tier generoso:** Até 5 users, unlimited tickets
-   **Profissional:** Interface polida para impressionar clientes
-   **Simples:** Sem complexidade desnecessária

#### Diferenciadores vs. Competição:

| Feature                | OrionOne    | Zendesk     | Freshdesk | ServiceNow  |
| ---------------------- | ----------- | ----------- | --------- | ----------- |
| **Preço (10 agents)**  | €150/mês    | €890/mês    | €490/mês  | €2500/mês   |
| **Setup Time**         | <1 hora     | 1 semana    | 2 dias    | 1-3 meses   |
| **Self-Hosted Option** | Sim         | Não         | Não       | Não         |
| **Open-Source Core**   | Sim         | Não         | Não       | Não         |
| **Modern Stack**       | Sim         | Parcial     | Parcial   | Não         |
| **Knowledge Base**     | Incluída    | Extra       | Sim       | Sim         |
| **SLA Management**     | Incluída    | Sim         | Pro       | Sim         |
| **Customization**      | ✅ Full     | ⚠️ Limitada | ⚠️        | ✅ Complexa |

### 3. Channels 📢

#### Aquisição de Clientes:

-   **Content Marketing** (SEO-optimized blog posts)
    -   "Best Zendesk alternatives for startups 2026"
    -   "How to reduce support costs by 50%"
    -   "Self-hosted ITSM solutions comparison"
-   **Product Hunt launch** (goal: Product of the Day)
-   **GitHub presence** (open-source core para community building)
-   **LinkedIn ads** (target: IT Managers, CTOs de SMEs)
-   **Partnerships** (web agencies, IT consultancies)

#### Conversão:

-   **Free trial:** 14 dias, no credit card required
-   **Interactive demo:** Sandbox com dados de exemplo
-   **Case studies:** ROI calculators, success stories
-   **Chatbot no site** (resposta instantânea a dúvidas)

#### Retenção:

-   **Onboarding email sequence** (dias 1, 3, 7, 14)
-   **In-app tutorials** (interactive walkthroughs)
-   **Customer success team** (Enterprise plans)
-   **Community forum** (peer-to-peer support)

### 4. Customer Relationships 🤝

#### Self-Service (Free & Starter)

-   Knowledge base completa
-   Video tutorials
-   Community forum
-   Email support (48h SLA)

#### Assisted Service (Professional)

-   Email + Chat support (24h SLA)
-   Onboarding call (30 min)
-   Quarterly business reviews

#### Dedicated Service (Enterprise)

-   Dedicated customer success manager
-   Priority support (4h SLA)
-   Custom onboarding & training
-   Slack/Teams integration para suporte

### 5. Revenue Streams 💰

#### Modelo de Pricing: SaaS Subscription (mensal/anual)

##### Free Tier - "Starter" 🆓

**Preço:** €0/mês
**Limites:**

-   Até 3 agents
-   Até 100 tickets ativos
-   1 GB storage
-   Email support (community)

**Target:** Freelancers, micro-empresas, testes

##### Professional - "Growth" 💼

**Preço:** €15/agent/mês (€12/mês se anual)
**Inclui:**

-   Unlimited agents
-   Unlimited tickets
-   10 GB storage por agent
-   Knowledge Base ilimitada
-   SLA management
-   Email + Chat support (24h SLA)
-   Custom branding (logo, cores)
-   API access

**Target:** SMEs com 5-50 agents

##### Enterprise - "Scale" 🏢

**Preço:** €25/agent/mês (€20/mês se anual)
**Inclui tudo de Professional +**

-   100 GB storage por agent
-   Priority support (4h SLA)
-   Dedicated customer success manager
-   Custom integrations (Slack, Teams, Jira)
-   SSO (SAML, OAuth)
-   Advanced analytics & reports
-   SLA: 99.9% uptime
-   White-label option

**Target:** Empresas 50+ agents, regulated industries

#### Add-ons (Revenue Boost)

-   **Extra Storage:** €5/mês por 50 GB
-   **Custom Development:** €100/hora para features específicas
-   **Training Sessions:** €500/dia para onboarding de grandes equipas
-   **Self-Hosted License:** €3,000/ano (perpetual license opcional)

#### Exemplos de Revenue:

| Cliente Tipo | Plan         | Agents | MRR    | ARR     |
| ------------ | ------------ | ------ | ------ | ------- |
| Startup A    | Professional | 5      | €75    | €900    |
| Scale-up B   | Professional | 25     | €375   | €4,500  |
| Enterprise C | Enterprise   | 100    | €2,500 | €30,000 |

**Objetivo Ano 1:** 100 clientes pagantes, €15k MRR, €180k ARR

### 6. Key Resources 🔑

#### Tecnológicos:

-   **Stack:** Laravel 11, PostgreSQL, Redis, Vue 3, Tailwind CSS
-   **Infra:** AWS/DigitalOcean (Kubernetes para escala)
-   **Monitoring:** Sentry, Laravel Pulse, Grafana
-   **CI/CD:** GitHub Actions, automated testing

#### Humanos (Roadmap):

-   **Ano 1 (MVP):** 1 Full-Stack Developer (founder)
-   **Ano 2 (Growth):**
    -   +1 Backend Developer
    -   +1 Frontend Developer
    -   +1 Customer Success Manager
-   **Ano 3 (Scale):**
    -   +1 DevOps Engineer
    -   +2 Sales reps
    -   +1 Marketing Manager

#### Financeiros:

-   **Bootstrap inicial:** €10k (desenvolvimento MVP)
-   **Funding Seed (opcional):** €100k para acelerar crescimento

#### Intelectuais:

-   **Open-source core** (community contributions)
-   **Brand & design system**
-   **Knowledge base content**
-   **Customer data & insights**

### 7. Key Activities 🛠️

#### Desenvolvimento de Produto (60% tempo)

-   Feature development (seguir roadmap)
-   Bug fixing & maintenance
-   Performance optimization
-   Security updates

#### Customer Acquisition (20% tempo)

-   Content marketing (blog posts, SEO)
-   Social media (LinkedIn, Twitter/X)
-   Product demos & webinars
-   Partnerships outreach

#### Customer Success (15% tempo)

-   Onboarding de novos clientes
-   Support tickets
-   Feature requests & feedback
-   Quarterly business reviews (Enterprise)

#### Operações (5% tempo)

-   Infrastructure management
-   Billing & invoicing
-   Legal & compliance

### 8. Key Partnerships 🤝

#### Tecnológicos:

-   **AWS/DigitalOcean:** Hosting & infra (potencial partnership discount)
-   **Stripe/Paddle:** Payment processing
-   **SendGrid/Postmark:** Email delivery

#### Distribuição:

-   **Web Agencies:** Resellers (20% commission)
-   **IT Consultancies:** Implementation partners
-   **Software Marketplaces:** Capterra, G2, GetApp (listagem gratuita)

#### Integrações:

-   **Slack/Microsoft Teams:** Chat integrations
-   **Jira/GitHub:** Developer workflow integrations
-   **Zapier/Make:** Automation platform

### 9. Cost Structure 💸

#### Custos Fixos (Mensais):

-   **Hosting & Infra:** €500/mês (início), escala com clientes
-   **Email service (SendGrid):** €100/mês
-   **Monitoring tools (Sentry):** €50/mês
-   **Domain & SSL:** €10/mês
-   **SaaS tools (Notion, Figma, etc):** €50/mês

**Total Fixo:** €710/mês (~€8,5k/ano)

#### Custos Variáveis:

-   **Customer acquisition (CAC):** €200 por cliente (ads, content)
-   **Customer support:** €5/cliente/mês (escala com volume)

#### Custos de Desenvolvimento:

-   **Ano 1 (solo founder):** Sweat equity (~€0 salary)
-   **Ano 2 (team):** €150k/ano (2 devs + 1 CSM)

#### Break-Even Analysis:

**Custos Mensais:** €710 fixo + variáveis
**ARPU (Average Revenue Per User):** €15/agent
**Break-Even:** ~50 agents pagantes (€750 MRR)

---

## Análise SWOT

### Strengths (Pontos Fortes) 💪

#### Técnicos:

-   **Stack moderno:** Laravel 11 + Vue 3 (atrativo para developers)
-   **Performance:** PostgreSQL + Redis (escalável)
-   **Open-source core:** Community-driven development
-   **Self-hosted option:** Diferenciador vs. competição

#### Negócio:

-   **Pricing competitivo:** 70% mais barato que líderes
-   **Time-to-market rápido:** MVP em 2.5 meses
-   **Bootstrap-friendly:** Custos operacionais baixos
-   **Nicho claro:** SMEs tech-savvy underserved

#### Produto:

-   **UI/UX moderna:** Não parece "enterprise software" antigo
-   **Mobile-first:** Funciona bem em tablets/phones
-   **Feature-complete:** Não faltam features críticas vs. competição

### Weaknesses (Pontos Fracos) 🚨

#### Produto:

-   **Brand awareness zero:** Nova marca no mercado saturado
-   **Feature parity incompleta:** Faltam integrações vs. Zendesk (100+ apps)
-   **Sem track record:** Nenhum case study inicial
-   **Escalabilidade não provada:** Não testado com 10k+ tickets/dia

#### Recursos:

-   **Team pequeno:** 1 developer inicialmente (bottleneck)
-   **Budget limitado:** Marketing constrangido sem funding
-   **Sem customer success team:** Onboarding pode sofrer

#### Mercado:

-   **Competição forte:** Zendesk, Freshdesk têm 10+ anos de vantagem
-   **Market education:** SMEs podem não saber que precisam de ITSM

### Opportunities (Oportunidades) 🚀

#### Mercado:

-   **Crescimento de SaaS:** +20% YoY, mais empresas precisam de suporte
-   **Remote work:** Equipas distribuídas precisam de ferramentas cloud
-   **Shift para self-hosted:** Empresas querem controlo de dados (GDPR)
-   **Insatisfação com incumbents:** Zendesk reviews mencionam preço alto

#### Tecnológicas:

-   **AI/ML:** Chatbots, auto-tagging, sentiment analysis (roadmap)
-   **No-code workflows:** Automações sem código (diferenciador)
-   **Mobile apps:** iOS/Android nativo (competitors fracos aqui)

#### Parcerias:

-   **Agencies:** 50k+ web agencies globalmente (resellers)
-   **Consultancies:** Implementam ITSM para clientes (channel sales)

#### Geográfico:

-   **Portugal & Brazil:** Mercado lusófono com menos competição
-   **Eastern Europe:** SMEs em crescimento, preço sensível

### Threats (Ameaças) ⚠️

#### Competição:

-   **Incumbents baixam preços:** Zendesk lança tier mais barato
-   **Big Tech entra:** Microsoft/Google lançam ITSM integrado
-   **Open-source free:** Alternatives como osTicket melhoram UI

#### Tecnológicas:

-   **Security breach:** Dados de clientes comprometidos (death sentence)
-   **Downtime prolongado:** SLA violations afetam reputação
-   **Vendor dependencies:** AWS outage afeta todos clientes

#### Mercado:

-   **Recessão económica:** SMEs cortam custos, incluindo SaaS
-   **Regulação:** GDPR-like regulations aumentam compliance costs
-   **Churn alto:** Se onboarding falha, clientes cancelam rápido

#### Operacionais:

-   **Burnout do founder:** Solo developer não é sustentável long-term
-   **Feature debt:** Pressão para lançar rápido sacrifica qualidade

---

## Go-to-Market Strategy

### Fase 1: MVP Launch (Jan-Mar 2026)

**Objetivo:** 10 early adopters pagantes

**Táticas:**

1. **Product Hunt launch:** Preparar página killer, vídeo demo, early bird discount
2. **Beta program:** 50 beta testers grátis por 3 meses (feedback intenso)
3. **Personal network:** Contactar 100 pessoas de network (LinkedIn, ex-colegas)
4. **Content marketing:** 10 blog posts (SEO long-tail keywords)
5. **Show HN (Hacker News):** Post no "Show HN" com link para GitHub

**Budget:** €0 (bootstrap, organic only)

**Success Metrics:**

-   500 website visits
-   50 trial signups
-   10 conversões (€150 MRR)

### Fase 2: Product-Market Fit (Apr-Jun 2026)

**Objetivo:** 50 clientes pagantes, €750 MRR

**Táticas:**

1. **Case studies:** Publicar 3 case studies de early adopters
2. **SEO content:** 30 blog posts (target: 1000 organic visits/mês)
3. **LinkedIn ads:** €500/mês (target: IT Managers)
4. **Partnerships:** Contactar 20 web agencies para reseller program
5. **Referral program:** €50 credit para cada referral convertido

**Budget:** €1,500 (ads + ferramentas)

**Success Metrics:**

-   2,000 website visits/mês
-   200 trial signups
-   25% trial → paid conversion
-   NPS > 40

### Fase 3: Growth (Jul-Dez 2026)

**Objetivo:** 200 clientes, €3k MRR

**Táticas:**

1. **Paid ads scale:** €2k/mês (LinkedIn + Google Search)
2. **Content marketing scale:** 50 posts, target 5k organic visits/mês
3. **Webinars:** Monthly webinar "How to scale IT support"
4. **Influencer partnerships:** Sponsor tech YouTubers/podcasters
5. **Integrations:** Lançar 10 integrações (Slack, Jira, GitHub, etc)

**Budget:** €30k (€5k/mês ads + €5k hiring)

**Success Metrics:**

-   10,000 website visits/mês
-   500 trial signups
-   40% trial → paid
-   Churn < 5%/mês
-   CAC < €300, LTV > €1,200 (ratio 4:1)

---

## Financial Projections (3 Anos)

### Ano 1 (2026): MVP & PMF

| Métrica       | Q1            | Q2     | Q3     | Q4     |
| ------------- | ------------- | ------ | ------ | ------ |
| **Clientes**  | 10            | 30     | 80     | 150    |
| **MRR**       | €150          | €600   | €1,500 | €3,000 |
| **ARR**       | €1,8k         | €7,2k  | €18k   | €36k   |
| **Custos**    | €2k           | €3k    | €5k    | €8k    |
| **Burn Rate** | -€2k          | -€2,4k | -€3,5k | -€5k   |
| **Runway**    | ∞ (bootstrap) |        |        |        |

**Resultado:** -€13k prejuízo (investimento inicial recuperado em Ano 2)

### Ano 2 (2027): Growth & Hiring

| Métrica      | Q1      | Q2    | Q3    | Q4    |
| ------------ | ------- | ----- | ----- | ----- |
| **Clientes** | 200     | 300   | 450   | 600   |
| **MRR**      | €4,5k   | €8k   | €13k  | €20k  |
| **ARR**      | €54k    | €96k  | €156k | €240k |
| **Custos**   | €15k    | €18k  | €22k  | €25k  |
| **Profit**   | -€10,5k | -€10k | -€9k  | -€5k  |

**Resultado:** -€34,5k prejuízo (investimento em team)

### Ano 3 (2028): Profitability & Scale

| Métrica      | Q1    | Q2    | Q3    | Q4    |
| ------------ | ----- | ----- | ----- | ----- |
| **Clientes** | 800   | 1,000 | 1,300 | 1,600 |
| **MRR**      | €30k  | €40k  | €55k  | €75k  |
| **ARR**      | €360k | €480k | €660k | €900k |
| **Custos**   | €30k  | €35k  | €40k  | €45k  |
| **Profit**   | €0    | €5k   | €15k  | €30k  |

**Resultado:** +€50k lucro (breakeven em Q2, rentável a partir de Q3)

### Unit Economics (Target Ano 2)

-   **ARPU (Average Revenue Per User):** €20/mês
-   **CAC (Customer Acquisition Cost):** €300
-   **LTV (Lifetime Value):** €1,200 (5 anos retention)
-   **LTV:CAC Ratio:** 4:1 (excelente)
-   **Payback Period:** 15 meses
-   **Gross Margin:** 85% (SaaS típico)

---

## Exit Strategy (Opcional)

### Opção 1: Bootstrap Sustentável (Lifestyle Business)

-   **Objetivo:** €100k/ano lucro para founder (anos 3-5)
-   **Growth:** Moderado (20% YoY)
-   **Team:** Pequeno (5-10 pessoas)
-   **Vantagem:** Controlo total, sem pressão de investors

### Opção 2: Acquisition (Ano 4-5)

**Potenciais Acquirers:**

-   Atlassian (Jira Service Management)
-   Zendesk
-   Freshworks
-   ServiceNow
-   Private equity (consolidação de SaaS)

**Valuation Target:** 5-8x ARR (€4-7M se €1M ARR)

### Opção 3: Venture-Backed Scale (Ano 2)

**Se captar Seed:**

-   €500k-1M para acelerar growth
-   Target: €10M ARR em 5 anos
-   Exit via IPO ou Series B+ acquisition (€50-100M+)

---

## Competitive Analysis

### Matriz Competitiva

| Competitor            | Market Share | Pricing         | Strengths                               | Weaknesses                      |
| --------------------- | ------------ | --------------- | --------------------------------------- | ------------------------------- |
| **Zendesk**           | 40%          | €€€€            | Brand, integrações, enterprise features | Caro, complexo, UI datada       |
| **Freshdesk**         | 25%          | €€€             | Onboarding fácil, pricing justo         | Menos features enterprise       |
| **ServiceNow**        | 20%          | €€€€€           | Enterprise-grade, ITIL certified        | Extremamente caro e complexo    |
| **Jira Service Mgmt** | 10%          | €€€             | Integração com Jira, developers love    | UI confusa para non-tech        |
| **osTicket**          | 5%           | € (open-source) | Grátis, self-hosted                     | UI horrível, features limitadas |
| **OrionOne**          | <1% (new)    | €€              | Moderno, acessível, self-hosted         | Sem brand, features incompletas |

### Posicionamento

```
                    Alto Preço
                        │
            ServiceNow  │  Zendesk
                        │
    Complexo ──────────┼────────── Simples
                        │
            osTicket    │  OrionOne
                        │  Freshdesk
                    Baixo Preço
```

**Sweet Spot de OrionOne:** Simples + Baixo Preço (underserved market)

---

## Risk Mitigation Plan

### Risco: Churn Alto (>10%/mês)

**Impacto:** Fatal (growth negativo)
**Mitigação:**

-   Onboarding obrigatório (call de 15 min)
-   In-app tutorials interativos
-   Emails de engagement (dias 1, 3, 7, 14, 30)
-   Exit surveys para entender razões
-   Feature requests prioritizados de churning customers

### Risco: Security Breach

**Impacto:** Catastrófico (perda de confiança, clientes, legal issues)
**Mitigação:**

-   Security audit trimestral (via Bugcrowd)
-   Penetration testing anual
-   ISO 27001 compliance (Ano 2)
-   Cyber insurance (€5k/ano)
-   Incident response plan documentado

### Risco: Competição Agressiva (Zendesk baixa preços)

**Impacto:** Alto (pressão em pricing)
**Mitigação:**

-   Diferenciação: self-hosted, open-source, UX moderna
-   Niche down: focar em developers/tech companies
-   Customer lock-in via data & customizações
-   Community building (não replicável)

### Risco: Founder Burnout

**Impacto:** Crítico (projeto pára)
**Mitigação:**

-   Work-life balance rigoroso (max 50h/semana)
-   Contratar parte da equipa em Ano 2
-   Automações para reduzir toil
-   Co-founder recruitment (se necessário)

---

## Success Metrics & KPIs

### Product Metrics

| KPI                          | Target Ano 1 | Target Ano 2 | Como Medir         |
| ---------------------------- | ------------ | ------------ | ------------------ |
| **Monthly Active Users**     | 500          | 3,000        | Laravel Analytics  |
| **Tickets Created/Mês**      | 5,000        | 50,000       | Database query     |
| **Avg. Resolution Time**     | <24h         | <12h         | Custom metric      |
| **NPS (Net Promoter Score)** | >30          | >50          | In-app surveys     |
| **Feature Adoption**         | 60%          | 80%          | Mixpanel/Amplitude |

### Business Metrics

| KPI               | Target Ano 1     | Target Ano 2 | Como Medir                 |
| ----------------- | ---------------- | ------------ | -------------------------- |
| **MRR Growth**    | +50%/mês (early) | +10%/mês     | Stripe dashboard           |
| **Churn Rate**    | <10%/mês         | <5%/mês      | Cohort analysis            |
| **CAC**           | <€300            | <€250        | Ad spend / conversões      |
| **LTV**           | >€900            | >€1,200      | ARPU × avg. lifespan       |
| **LTV:CAC Ratio** | >3:1             | >4:1         | LTV / CAC                  |
| **Gross Margin**  | >80%             | >85%         | (Revenue - COGS) / Revenue |

### Marketing Metrics

| KPI                 | Target Ano 1 | Target Ano 2 | Como Medir        |
| ------------------- | ------------ | ------------ | ----------------- |
| **Website Traffic** | 5k/mês       | 25k/mês      | Google Analytics  |
| **Trial Signups**   | 200/mês      | 1,000/mês    | CRM               |
| **Trial → Paid**    | 20%          | 40%          | Conversion funnel |
| **Organic Traffic** | 50%          | 70%          | GA (source)       |

---

## Roadmap de Produto (Pós-MVP)

### Q2 2026: Integrações & Automação

-   [ ] Slack integration (notificações)
-   [ ] Microsoft Teams integration
-   [ ] Zapier integration (1000+ apps)
-   [ ] Workflow automation (if/then rules)
-   [ ] API webhooks

### Q3 2026: Mobile & AI

-   [ ] Progressive Web App (iOS/Android)
-   [ ] AI-powered auto-tagging de tickets
-   [ ] Chatbot para KB search
-   [ ] Sentiment analysis em comentários

### Q4 2026: Enterprise Features

-   [ ] SSO (SAML, OAuth)
-   [ ] Multi-tenancy (SaaS multi-tenant)
-   [ ] Advanced permissions (custom roles)
-   [ ] Audit logs completos
-   [ ] Data residency options (EU, US)

### 2027: Scale & Expansion

-   [ ] Marketplace de plugins (community)
-   [ ] White-label customization completa
-   [ ] ITIL compliance certification
-   [ ] Mobile apps nativas (React Native)

---

## Conclusão

OrionOne tem potencial de se posicionar como **líder no segmento SME de ITSM**, oferecendo uma alternativa moderna, acessível e completa às soluções enterprise caras e complexas.

**Fatores Críticos de Sucesso:**

1. ✅ **Product-Market Fit:** Validar com 50 early adopters até Q2 2026
2. ✅ **Unit Economics Saudável:** LTV:CAC > 3:1, Churn < 5%
3. ✅ **Diferenciação Clara:** Self-hosted + Open-source + UX moderna
4. ✅ **Execução Rápida:** MVP em 2.5 meses, features core completas

**Next Steps Imediatos:**

1. Completar MVP (Jan 2026)
2. Beta program com 50 testers (Fev 2026)
3. Product Hunt launch (Mar 2026)
4. Primeiros 10 clientes pagantes (Q1 2026)

---

**Versão:** 1.0
**Data:** 07 Novembro 2025
**Autor:** JMSS95
**Próxima Revisão:** Março 2026 (pós-launch)
