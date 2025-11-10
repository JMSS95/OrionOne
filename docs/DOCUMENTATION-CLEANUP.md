# Documentação a Consolidar/Remover - OrionOne

**Data:** 10 Novembro 2025
**Análise:** Redundâncias e documentos desatualizados

---

## 🔴 Documentos REDUNDANTES (Remover)

### 1. **development-planning.md** ❌ REMOVER

**Razão:** Completamente substituído por documentos mais recentes

**Conteúdo substituído por:**

-   ✅ `MVP-PRIORITIES.md` - Roadmap atualizado Sprint 2-6
-   ✅ `implementation-checklist.md` - Checklist TDD detalhado
-   ✅ `MVP-READINESS-CHECKLIST.md` - Estado atual 95%

**Problemas:**

-   Datas antigas (Nov 2025 - Jan 2026)
-   Informação desatualizada sobre Fase 0
-   Não reflete Stack Analysis 2025 (PHP 8.4, Pest, etc)

**Ação:** ❌ **DELETE** `docs/development-planning.md`

---

### 2. **SETUP-CHANGELOG.md** ❌ REMOVER

**Razão:** Histórico já integrado em outros documentos

**Conteúdo substituído por:**

-   ✅ `tech-stack.md` - Stack atual com status
-   ✅ `STACK-ANALYSIS-2025.md` - Análise completa 8.7/10
-   ✅ `MVP-READINESS-CHECKLIST.md` - Setup atual

**Problemas:**

-   Setup inicial já não é relevante (Novembro 2025)
-   Não menciona melhorias recentes (PHP 8.4, Pest, Scribe)
-   Comandos antigos (muitos já executados)

**Ação:** ❌ **DELETE** `docs/SETUP-CHANGELOG.md`

---

### 3. **QUICK-START.md** ⚠️ MANTER MAS ATUALIZAR

**Razão:** Útil para novos developers mas precisa atualização

**Problemas:**

-   Não menciona Docker como obrigatório
-   Comandos locais (composer, php artisan) sem docker-compose
-   Não reflete PHP 8.4 upgrade

**Ação:** ✅ **UPDATE** com Docker-first approach

---

## ✅ Documentos ESSENCIAIS (Manter)

### Core Documentation

1. **README.md** ✅ - Índice de documentação (atualizar links)
2. **architecture.md** ✅ - Arquitetura do sistema
3. **tech-stack.md** ✅ - Stack tecnológica (ATUALIZADO)
4. **database-schema.md** ✅ - Schema DB
5. **development-guide.md** ✅ - Metodologia TDD
6. **implementation-checklist.md** ✅ - Roadmap detalhado

### Analysis & Planning

7. **STACK-ANALYSIS-2025.md** ✅ - Análise técnica 8.7/10
8. **ITSM-STACK-ANALYSIS.md** ✅ - Análise mercado ITSM 8.5/10
9. **MVP-PRIORITIES.md** ✅ - Prioridades MVP Sprint 2-6
10. **MVP-READINESS-CHECKLIST.md** ✅ - Estado atual 95%

### Reference Guides

11. **COMMANDS-REFERENCE.md** ✅ - Comandos úteis
12. **COMPONENTS-GUIDE.md** ✅ - Componentes UI
13. **DOCKER-GUIDE.md** ✅ - Docker para iniciantes
14. **business-model.md** ✅ - Modelo de negócio
15. **requirements.md** ✅ - Requisitos funcionais

---

## 🔄 Ações Necessárias

### 1. Remover Documentos Obsoletos

```bash
git rm docs/development-planning.md
git rm docs/SETUP-CHANGELOG.md
git commit -m "docs: remove obsolete documentation (replaced by MVP-PRIORITIES and Stack Analysis)"
```

### 2. Atualizar QUICK-START.md

**Mudanças:**

-   ✅ Docker-first approach (todos os comandos via docker-compose)
-   ✅ Mencionar PHP 8.4 requirement
-   ✅ Adicionar verificação Pest PHP
-   ✅ Link para MVP-READINESS-CHECKLIST.md

### 3. Atualizar README.md

**Remover referências:**

-   ❌ development-planning.md
-   ❌ SETUP-CHANGELOG.md

**Adicionar referências:**

-   ✅ STACK-ANALYSIS-2025.md
-   ✅ ITSM-STACK-ANALYSIS.md
-   ✅ MVP-PRIORITIES.md
-   ✅ MVP-READINESS-CHECKLIST.md

---

## 📊 Estrutura Final Recomendada

```
docs/
├── README.md                          # Índice geral (ATUALIZAR)
│
├── 🚀 Getting Started
│   ├── QUICK-START.md                 # Setup rápido (ATUALIZAR)
│   ├── DOCKER-GUIDE.md                # Docker basics
│   └── COMMANDS-REFERENCE.md          # Comandos úteis
│
├── 🏗️ Architecture & Design
│   ├── architecture.md                # MVC + Services
│   ├── tech-stack.md                  # Stack atual
│   └── database-schema.md             # Schema DB
│
├── 💻 Development
│   ├── development-guide.md           # TDD methodology
│   ├── implementation-checklist.md    # Sprint 1-6 roadmap
│   ├── COMPONENTS-GUIDE.md            # UI components
│   └── MVP-READINESS-CHECKLIST.md     # Current status 95%
│
├── 📊 Analysis & Planning
│   ├── STACK-ANALYSIS-2025.md         # Tech score 8.7/10
│   ├── ITSM-STACK-ANALYSIS.md         # Market analysis 8.5/10
│   └── MVP-PRIORITIES.md              # Sprint 2-6 priorities
│
└── 📋 Business & Requirements
    ├── business-model.md              # Business model
    └── requirements.md                # Functional requirements
```

---

## 🎯 Resumo

### Documentos Obsoletos (2)

-   ❌ development-planning.md (substituído por MVP-PRIORITIES)
-   ❌ SETUP-CHANGELOG.md (histórico não relevante)

### Documentos a Atualizar (2)

-   ⚠️ QUICK-START.md (Docker-first approach)
-   ⚠️ README.md (atualizar índice)

### Documentos Essenciais (15)

-   ✅ Todos os outros mantêm-se

### Benefícios

1. ✅ Menos confusão (remove docs desatualizados)
2. ✅ Informação centralizada (MVP-PRIORITIES tem tudo)
3. ✅ Docker-first em toda documentação
4. ✅ Referências atualizadas (PHP 8.4, Pest, Scribe)

---

**Próxima Ação:**

1. Remover development-planning.md e SETUP-CHANGELOG.md
2. Atualizar QUICK-START.md com Docker commands
3. Atualizar README.md com novos links

**Última Atualização:** 10 Novembro 2025, 05:45
