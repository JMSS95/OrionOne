# Quick Start - Setup em PC Novo

## Checklist Rápida

### Antes de Começar

-   [ ] Instalar **Git** (2.40+)
-   [ ] Instalar **Docker Desktop** (4.25+)
-   [ ] Instalar **Node.js** (20.x LTS)
-   [ ] Instalar **Composer** (2.6+)
-   [ ] Instalar **VS Code** (opcional mas recomendado)

---

## Setup em 5 Minutos

### 1. Clonar Repositório

```bash
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne
```

### 2. Configurar Ambiente

```bash
cp .env.example .env
```

### 3. Iniciar Docker

```bash
docker-compose up -d
```

### 4. Instalar Dependências

```bash
# Backend
docker-compose exec orionone-app composer install

# Frontend
docker-compose exec orionone-frontend npm install --legacy-peer-deps
```

### 5. Configurar Laravel

```bash
# Gerar chave
docker-compose exec orionone-app php artisan key:generate

# Criar DB de testes
docker-compose exec orionone-db psql -U laravel -d postgres -c "CREATE DATABASE orionone_test;"

# Migrations + Seeds
docker-compose exec orionone-app php artisan migrate:fresh --seed
```

### 6. Iniciar Frontend

```bash
docker-compose exec orionone-frontend npm run dev
```

### 7. Testar

```bash
# Executar testes
docker-compose exec orionone-app php artisan test

# Aceder à aplicação
# http://localhost:8888
```

---

## Tudo OK?

**Containers a correr:** `docker-compose ps`
**Testes passam:** `php artisan test` (dentro do container)
**Login funciona:** admin@orionone.test / password

---

## Próximos Passos

1. Ler **[SETUP.md](../SETUP.md)** completo
2. Seguir **[implementation-checklist.md](./implementation-checklist.md)** para desenvolvimento
3. Consultar **[COMMANDS-REFERENCE.md](./COMMANDS-REFERENCE.md)** para comandos úteis

---

## Problemas?

### Container não inicia

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Erro "could not find driver"

Estás a correr `php artisan` localmente? **Usa sempre:**

```bash
docker-compose exec orionone-app php artisan ...
```

### Frontend não compila

```bash
docker-compose exec orionone-frontend rm -rf node_modules
docker-compose exec orionone-frontend npm install --legacy-peer-deps
```

---

**Ver mais:** [SETUP.md](../SETUP.md) para troubleshooting completo
