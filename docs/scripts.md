# Scripts de Desenvolvimento

## Testes e Qualidade

### PHPStan (Análise Estática)

```bash
# Análise completa
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# Com mais memória
docker-compose exec orionone-app ./vendor/bin/phpstan analyse --memory-limit=512M
```

### Laravel Pint (Code Style)

```bash
# Verificar estilo
docker-compose exec orionone-app ./vendor/bin/pint --test

# Corrigir automaticamente
docker-compose exec orionone-app ./vendor/bin/pint
```

### PHPUnit (Testes)

```bash
# Todos os testes
docker-compose exec orionone-app php artisan test

# Com coverage
docker-compose exec orionone-app php artisan test --coverage

# Teste específico
docker-compose exec orionone-app php artisan test --filter TicketTest
```

## Comandos Úteis

### Artisan

```bash
# Migrations
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-app php artisan migrate:fresh --seed

# Cache
docker-compose exec orionone-app php artisan config:clear
docker-compose exec orionone-app php artisan route:clear
docker-compose exec orionone-app php artisan view:clear

# Tinker (REPL)
docker-compose exec orionone-app php artisan tinker
```

### Composer

```bash
# Instalar dependências
docker-compose exec orionone-app composer install

# Atualizar
docker-compose exec orionone-app composer update

# Adicionar package
docker-compose exec orionone-app composer require package/name
```

### NPM

```bash
# Instalar dependências (Linux-compatible)
docker-compose run --rm orionone-frontend npm install

# Build para produção
docker-compose run --rm orionone-frontend npm run build
```

## Workflow Diário

### Antes de Commit

```bash
# 1. Code style
docker-compose exec orionone-app ./vendor/bin/pint

# 2. Análise estática
docker-compose exec orionone-app ./vendor/bin/phpstan analyse

# 3. Testes
docker-compose exec orionone-app php artisan test
```

### Iniciar Desenvolvimento

```bash
# Subir containers
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```
