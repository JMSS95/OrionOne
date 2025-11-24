# GitHub Codespaces - Guia de Setup OrionOne ITSM

## Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Como Criar um Codespace](#como-criar-um-codespace)
4. [Primeira Utilização](#primeira-utilização)
5. [Arquitetura dos Containers](#arquitetura-dos-containers)
6. [Portas e Serviços](#portas-e-serviços)
7. [Comandos Úteis](#comandos-úteis)
8. [Desenvolvimento](#desenvolvimento)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Visão Geral

O OrionOne ITSM está totalmente configurado para funcionar com **GitHub Codespaces**, permitindo desenvolvimento full-stack diretamente no browser sem necessidade de instalação local.

### O que está incluído:

-   ✅ **Backend NestJS** (porta 3001)
-   ✅ **Frontend Next.js** (porta 3000)
-   ✅ **PostgreSQL 18** (porta 5432)
-   ✅ **Redis 7** (porta 6379)
-   ✅ **Meilisearch v1.25** (porta 7700)
-   ✅ **Mailpit** (SMTP: 1025, Web UI: 8025)
-   ✅ **Nginx** como reverse proxy (porta 80)

### Vantagens:

-   Setup automático em ~5 minutos
-   Desenvolvimento no browser ou VS Code local
-   Sincronização automática com o repositório
-   Todos os serviços Docker pré-configurados
-   Extensões VS Code pré-instaladas
-   Dependências instaladas automaticamente

---

## Pré-requisitos

-   **Conta GitHub** com acesso ao repositório OrionOne
-   **GitHub Codespaces** ativado (incluído em contas gratuitas com 60h/mês)
-   **Browser moderno** (Chrome, Edge, Firefox, Safari)

> **Nota:** Não é necessário ter Docker, Node.js, ou qualquer ferramenta instalada localmente!

---

## Como Criar um Codespace

### Método 1: Via GitHub Web

1. **Acede ao repositório:** `https://github.com/JMSS95/OrionOne`

2. **Clica no botão verde "Code":**

    ```
    [< > Code ▼]
    ```

3. **Seleciona a tab "Codespaces"**

4. **Clica em "Create codespace on feat/migrate-nextjs-nestjs"** (ou outra branch)

5. **Aguarda ~5 minutos** enquanto o Codespace é criado

### Método 2: Via GitHub CLI

```bash
gh codespace create --repo JMSS95/OrionOne --branch feat/migrate-nextjs-nestjs
```

### Método 3: Via VS Code Desktop

1. Instala a extensão **GitHub Codespaces** no VS Code
2. `Ctrl+Shift+P` → "Codespaces: Create New Codespace"
3. Seleciona `JMSS95/OrionOne`
4. Escolhe a branch

---

## Primeira Utilização

### O que acontece automaticamente:

1. **Container criado** com Node.js 20, Git, Docker, GitHub CLI
2. **Docker Compose inicia** todos os serviços (PostgreSQL, Redis, etc.)
3. **Script `post-create.sh` executa:**
    - Cria ficheiro `.env` (se não existir)
    - Aguarda PostgreSQL e Redis estarem prontos
    - Instala dependências (`npm install`) no Backend e Frontend
    - Executa migrações Prisma (`prisma migrate deploy`)
    - Executa seed da base de dados
    - Cria diretórios necessários (`uploads/`, `logs/`)
4. **Extensões VS Code instaladas** automaticamente
5. **Codespace pronto!** ✅

### Verificar que tudo está a funcionar:

1. **Abrir Terminal Integrado** (` Ctrl+`` ou  `Cmd+``)

2. **Verificar status dos serviços:**

    ```bash
    docker ps
    ```

    Deves ver 7 containers ativos:

    - `orionone-backend`
    - `orionone-frontend`
    - `orionone-postgres`
    - `orionone-redis`
    - `orionone-meilisearch`
    - `orionone-mailpit`
    - `orionone-nginx`

3. **Verificar logs:**

    ```bash
    docker-compose logs -f backend
    ```

4. **Aceder à aplicação:**
    - Clica na notificação de porta ou
    - Vai ao painel "PORTS" (parte inferior do VS Code)
    - Clica no ícone ao lado da porta 80

---

## Arquitetura dos Containers

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Codespace                         │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Frontend  │  │  Backend   │  │   Nginx    │            │
│  │  Next.js   │  │  NestJS    │  │   :80      │            │
│  │   :3000    │  │   :3001    │  │            │            │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘            │
│        │               │               │                    │
│        └───────────────┴───────────────┘                    │
│                        │                                    │
│  ┌────────────┬────────┴────────┬────────────┬──────────┐  │
│  │            │                 │            │          │  │
│  │ PostgreSQL │     Redis       │ Meilisearch│ Mailpit  │  │
│  │   :5432    │     :6379       │   :7700    │  :8025   │  │
│  └────────────┴─────────────────┴────────────┴──────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Detalhes dos Serviços:

| Serviço         | Imagem                     | Porta      | Descrição                      |
| --------------- | -------------------------- | ---------- | ------------------------------ |
| **backend**     | Custom (NestJS)            | 3001       | API REST, Prisma ORM, JWT Auth |
| **frontend**    | Custom (Next.js)           | 3000       | React 19, Tailwind, shadcn/ui  |
| **postgres**    | postgres:18-alpine         | 5432       | Base de dados principal        |
| **redis**       | redis:7-alpine             | 6379       | Cache e sessões                |
| **meilisearch** | getmeili/meilisearch:v1.25 | 7700       | Search engine                  |
| **mailpit**     | axllent/mailpit            | 1025, 8025 | Email testing                  |
| **nginx**       | nginx:alpine               | 80         | Reverse proxy                  |

---

## Portas e Serviços

O Codespace faz **port forwarding automático** das seguintes portas:

| Porta    | Serviço          | Visibilidade | URL Típica                    |
| -------- | ---------------- | ------------ | ----------------------------- |
| **80**   | Nginx (Main)     | Public       | `https://xxx.github.dev`      |
| **3000** | Next.js Frontend | Public       | `https://xxx-3000.github.dev` |
| **3001** | NestJS Backend   | Private      | `https://xxx-3001.github.dev` |
| **5432** | PostgreSQL       | Private      | Apenas interno                |
| **6379** | Redis            | Private      | Apenas interno                |
| **7700** | Meilisearch      | Private      | `https://xxx-7700.github.dev` |
| **8025** | Mailpit Web UI   | Public       | `https://xxx-8025.github.dev` |

### Como aceder aos serviços:

1. **Via painel "PORTS"** (parte inferior do VS Code):

    - Clica no ícone 🌐 para abrir no browser
    - Clica no ícone 🔒 para alterar visibilidade (Public/Private)

2. **Via notificações:**

    - O Codespace mostra notificações quando portas são abertas
    - Clica em "Open in Browser"

3. **Via comandos:**

    ```bash
    # Listar portas forwarded
    gh codespace ports

    # Abrir porta específica no browser
    gh codespace ports open 3000
    ```

---

## 🛠️ Comandos Úteis

### Docker

```bash
# Ver status de todos os containers
docker ps

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar um serviço
docker-compose restart backend

# Parar todos os serviços
docker-compose down

# Iniciar todos os serviços
docker-compose up -d

# Rebuild de um serviço específico
docker-compose up -d --build backend

# Limpar tudo (cuidado: apaga volumes!)
docker-compose down -v
```

### Base de Dados (PostgreSQL)

```bash
# Aceder ao psql
psql postgresql://orionone:secret@postgres:5432/orionone

# Executar query diretamente
psql postgresql://orionone:secret@postgres:5432/orionone -c "SELECT * FROM users;"

# Ver migrações
cd nest-backend
npx prisma migrate status

# Criar nova migração
npx prisma migrate dev --name nome_da_migracao

# Executar seed
npx prisma db seed

# Gerar Prisma Client
npx prisma generate

# Abrir Prisma Studio
npx prisma studio
```

### Redis

```bash
# Aceder ao redis-cli
redis-cli -h redis

# Verificar keys
redis-cli -h redis KEYS '*'

# Ver valor de uma key
redis-cli -h redis GET "key_name"

# Limpar cache
redis-cli -h redis FLUSHALL
```

### Meilisearch

```bash
# Verificar health
curl http://meilisearch:7700/health

# Listar índices
curl -H "Authorization: Bearer masterKeyForDevelopment123" \
     http://meilisearch:7700/indexes

# Ver stats
curl -H "Authorization: Bearer masterKeyForDevelopment123" \
     http://meilisearch:7700/stats
```

### Git

```bash
# Ver status
git status

# Criar nova branch
git checkout -b feature/nome-feature

# Commit
git add .
git commit -m "feat: descrição"

# Push
git push origin feature/nome-feature

# Pull
git pull origin feat/migrate-nextjs-nestjs

# Ver branches remotas
git branch -r
```

### NPM / Node

```bash
# Backend
cd nest-backend
npm install              # Instalar deps
npm run dev              # Modo desenvolvimento
npm run build            # Build
npm run test             # Testes
npm run test:watch       # Testes em watch mode
npm run lint             # ESLint

# Frontend
cd next-frontend
npm install
npm run dev
npm run build
npm run test
npm run lint
```

---

## Desenvolvimento

### Iniciar desenvolvimento:

1. **Abrir 2 terminais** no VS Code (`Ctrl+Shift+`` )

2. **Terminal 1 - Backend:**

    ```bash
    cd nest-backend
    npm run dev
    ```

    Verás: `Application is running on: http://localhost:3001`

3. **Terminal 2 - Frontend:**

    ```bash
    cd next-frontend
    npm run dev
    ```

    Verás: `Ready on http://localhost:3000`

4. **Aceder à aplicação:**
    - Via Nginx (recomendado): porta 80
    - Frontend direto: porta 3000
    - Backend API: porta 3001
    - Mailpit: porta 8025

### Workflow recomendado:

1. **Criar nova branch** para cada feature:

    ```bash
    git checkout -b feature/us1-1-user-registration
    ```

2. **Desenvolvimento TDD:**

    - Escrever teste primeiro (`*.spec.ts`)
    - Implementar código
    - Verificar que passa: `npm run test`

3. **Commit frequente:**

    ```bash
    git add .
    git commit -m "feat(auth): implement user registration"
    ```

4. **Push e criar PR:**
    ```bash
    git push origin feature/us1-1-user-registration
    # Criar PR no GitHub
    ```

### Hot Reload:

-   ✅ **Backend:** NestJS recarrega automaticamente ao guardar ficheiros
-   ✅ **Frontend:** Next.js Fast Refresh atualiza instantaneamente
-   ✅ **Prisma:** Após alterar `schema.prisma`, executa:
    ```bash
    npx prisma generate
    npx prisma migrate dev
    ```

### Debug:

#### Backend (NestJS):

1. Adiciona breakpoint no código (clica na margem esquerda da linha)
2. `F5` ou "Run and Debug" → "Debug NestJS"
3. Configura `.vscode/launch.json` (já incluído no Codespace)

#### Frontend (Next.js):

1. Adiciona breakpoint
2. Abre DevTools no browser (`F12`)
3. Ou usa "Debug: Open Link" no VS Code

---

## Troubleshooting

### Container não inicia:

```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar se porta está ocupada
docker ps -a

# Rebuild forçado
docker-compose up -d --build --force-recreate
```

### PostgreSQL não está acessível:

```bash
# Verificar se está a correr
docker ps | grep postgres

# Ver logs
docker-compose logs postgres

# Reiniciar
docker-compose restart postgres

# Testar conexão
pg_isready -h postgres -U orionone
```

### Migrações Prisma falham:

```bash
# Reset completo (cuidado: apaga dados!)
cd nest-backend
npx prisma migrate reset

# Ou aplicar manualmente
npx prisma migrate deploy
npx prisma generate
```

### "Cannot find module":

```bash
# Reinstalar dependências
cd nest-backend  # ou next-frontend
rm -rf node_modules package-lock.json
npm install
```

### Codespace lento:

-   Fecha tabs/painéis não utilizados
-   Para serviços não necessários:
    ```bash
    docker-compose stop meilisearch mailpit
    ```
-   Aumenta máquina do Codespace (Settings → Change machine type)

### Port forwarding não funciona:

1. Vai ao painel "PORTS"
2. Clica com botão direito na porta
3. Seleciona "Port Visibility" → "Public"

---

## Best Practices

### 1. **Commits Convencionais**

Usa prefixos semânticos:

```
feat: nova funcionalidade
fix: correção de bug
docs: alteração de documentação
style: formatação, sem alteração de lógica
refactor: refatoração de código
test: adicionar/corrigir testes
chore: tarefas de manutenção
```

Exemplo:

```bash
git commit -m "feat(incidents): add priority field to incident model"
```

### 2. **Branches**

```
main                    # Produção
feat/migrate-nextjs-nestjs  # Desenvolvimento principal
feature/us1-1-register      # Features específicas
fix/login-redirect          # Correções
```

### 3. **Testes**

Sempre escreve testes antes de fazer PR:

```bash
# Backend
cd nest-backend
npm run test
npm run test:e2e

# Frontend
cd next-frontend
npm run test
```

### 4. **Linting**

Antes de commit:

```bash
npm run lint
npm run lint:fix  # Corrige automaticamente
```

### 5. **Segurança**

-   ⛔ **Nunca** commita ficheiros `.env`
-   ✅ Usa `.env.example` como template
-   ✅ Secrets no GitHub Secrets (produção)

### 6. **Performance**

-   Para serviços não usados: `docker-compose stop meilisearch`
-   Fecha Codespace quando não estás a usar (economiza quotas)
-   Usa `.gitignore` para `node_modules/`, `.next/`, `dist/`

### 7. **Documentação**

Atualiza docs ao adicionar features:

-   `README.md` - Overview
-   `docs/guides/Sprint-X-guide.md` - Implementação
-   Código: Comentários JSDoc/TSDoc

---

## Variáveis de Ambiente

O ficheiro `.env` é criado automaticamente a partir de `.env.example`. Valores padrão para Codespace:

```env
# Database
DATABASE_URL=postgresql://orionone:secret@postgres:5432/orionone

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Meilisearch
MEILISEARCH_HOST=http://meilisearch:7700
MEILISEARCH_KEY=masterKeyForDevelopment123

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_EXPIRES_IN=7d

# Email (Mailpit)
EMAIL_HOST=mailpit
EMAIL_PORT=1025
EMAIL_USER=
EMAIL_PASS=
EMAIL_FROM=noreply@orionone.local

# App
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://backend:3001
```

---

## Recursos Adicionais

### Documentação do Projeto:

-   **README.md** - Visão geral
-   **SETUP.md** - Setup local (alternativa ao Codespace)
-   **CONTRIBUTING.md** - Como contribuir
-   **DEPLOYMENT.md** - Deploy em produção
-   **docs/guides/** - Guias de implementação Sprint 1-6

### Documentação Externa:

-   [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
-   [Dev Containers Spec](https://containers.dev/)
-   [NestJS Docs](https://docs.nestjs.com/)
-   [Next.js Docs](https://nextjs.org/docs)
-   [Prisma Docs](https://www.prisma.io/docs)

---

## Suporte

### Problemas com o Codespace:

1. **Verifica logs:** `docker-compose logs -f`
2. **Consulta documentação:** `docs/`
3. **Issues:** Cria issue no GitHub
4. **Discussão:** GitHub Discussions

### Contacto:

-   **GitHub:** [@JMSS95](https://github.com/JMSS95)
-   **Repository:** [OrionOne](https://github.com/JMSS95/OrionOne)

---

## Quotas GitHub Codespaces

### Plano Free:

-   **120 horas/mês** (máquina 2-core)
-   **60 horas/mês** (máquina 4-core)
-   **15 GB storage**

### Dicas para poupar quotas:

1. **Para o Codespace** quando não estás a usar:

    - Vai a `https://github.com/codespaces`
    - Stop ou Delete

2. **Timeout automático:**

    - Settings → Set idle timeout (default: 30 min)

3. **Usa máquina mais pequena:**

    - 2-core é suficiente para desenvolvimento

4. **Trabalha offline:**
    - Clone repo localmente para leitura
    - Usa Codespace só para código ativo

---

## Checklist Primeira Utilização

-   [ ] Codespace criado com sucesso
-   [ ] Todos os 7 containers a correr (`docker ps`)
-   [ ] Backend acessível na porta 3001
-   [ ] Frontend acessível na porta 3000
-   [ ] PostgreSQL conectado (verificar com `psql`)
-   [ ] Redis conectado (verificar com `redis-cli`)
-   [ ] Migrações Prisma aplicadas
-   [ ] Seed da BD executado
-   [ ] Mailpit UI acessível (porta 8025)
-   [ ] Extensões VS Code instaladas
-   [ ] Git configurado (`git config user.name`)

---

**Última atualização:** 24 de Novembro de 2025
**Versão:** 1.0.0
**Autor:** GitHub Copilot para OrionOne ITSM
