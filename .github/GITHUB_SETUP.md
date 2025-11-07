# Configuração do GitHub - OrionOne

## ✅ Já Configurado

-   [x] Repositório público
-   [x] LICENSE (MIT)
-   [x] Colaborador adicionado (pendente aceitação)
-   [x] Badges no README

---

## 📋 Configurações Pendentes

### 1. About Section (Lado direito do repositório)

**Localização:** Página principal do repo → ⚙️ (ícone engrenagem ao lado de "About")

**Description:**

```
Modern ITSM Platform for IT Support Management - CET Academic Project 2024/2025
```

**Topics (adicionar estas tags):**

```
laravel
vue3
inertia
itsm
ticketing-system
postgresql
docker
tailwindcss
academic-project
servicedesk
```

---

### 2. Repository Settings → Features

**Localização:** Settings → General → Features

**Ativar:**

-   ✅ Issues (para tracking de bugs e features)
-   ✅ Preserve this repository (arquivamento)

**Desativar:**

-   ❌ Projects (não necessário - tens docs/requirements.md)
-   ❌ Wiki (tens pasta docs/ completa)
-   ❌ Sponsorships
-   ❌ Discussions (opcional - só se quiseres Q&A público)

---

### 3. Repository Settings → Pull Requests

**Localização:** Settings → General → Pull Requests

**Configurar:**

-   ✅ Allow squash merging (mantém histórico limpo)
-   ❌ Allow merge commits
-   ❌ Allow rebase merging
-   ✅ Automatically delete head branches (limpa branches após merge)
-   ✅ Always suggest updating pull request branches

---

### 4. Security & Analysis

**Localização:** Settings → Security and analysis

**Ativar:**

-   ✅ Dependency graph (mostra dependências)
-   ✅ Dependabot alerts (avisos de segurança)
-   ✅ Dependabot security updates (updates automáticos - CUIDADO: pode criar muitos PRs)

**Secret scanning:**

-   ✅ Push protection (evita commits com secrets)

---

### 5. Branch Protection (Opcional mas Profissional)

**Localização:** Settings → Branches → Add rule

**Branch name pattern:** `main`

**Regras recomendadas para projeto académico:**

-   ✅ Require a pull request before merging
    -   ❌ Require approvals: 0 (és só tu)
-   ❌ Require status checks (não tens CI/CD ainda)
-   ✅ Require conversation resolution before merging
-   ✅ Do not allow bypassing the above settings

**Benefício:** Obriga-te a trabalhar em branches (git flow profissional)

---

## 🎨 Social Preview (Opcional)

**Localização:** Settings → Social preview → Upload an image

**Quando fazer:** Após criares o dashboard principal

**Tamanho recomendado:** 1280x640px

**Ferramenta grátis:** https://www.canva.com/

---

## 🔄 Workflow Recomendado com Branch Protection

Se ativares branch protection:

```bash
# 1. Criar branch para feature
git checkout -b feature/RF02-tickets

# 2. Trabalhar normalmente
git add .
git commit -m "feat: implement ticket CRUD"

# 3. Push da branch
git push origin feature/RF02-tickets

# 4. No GitHub: Create Pull Request
# 5. Review (tu mesmo) e merge
# 6. Branch apagada automaticamente
```

---

## 📊 GitHub Insights (Mostrar ao Instrutor)

**Localização:** Tab "Insights" no repo

**Útil para mostrar:**

-   Pulse (atividade semanal)
-   Contributors (teus commits)
-   Traffic (quem visitou)
-   Network (gráfico de branches)

---

## 🎯 Próximos Passos (Semana 2-3)

### GitHub Actions (CI/CD)

Criar `.github/workflows/laravel.yml`:

```yaml
name: Laravel Tests

on: [push, pull_request]

jobs:
    test:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3
            - name: Run PHPUnit
              run: docker-compose exec -T orionone-app php artisan test
```

### Issue Templates

Criar `.github/ISSUE_TEMPLATE/bug_report.md` e `feature_request.md`

---

## ✅ Checklist Final

-   [ ] About section preenchida
-   [ ] Topics adicionados (10 tags)
-   [ ] Features configuradas (Issues ON, Wiki OFF)
-   [ ] Pull Requests settings (squash merge)
-   [ ] Dependabot ativado
-   [ ] Branch protection (opcional)
-   [ ] Social preview (quando tiveres dashboard)

---

**Nota:** O colaborador só aparece com permissões após aceitar o convite por email!
