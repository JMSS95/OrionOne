# Tech Deep Dive - DevOps (Docker/Nginx/Deploy)

> **Guia Completo**: Como funciona a infraestrutura do OrionOne - Docker, Docker Compose, Nginx, Deployment

---

## 1. DOCKER (Containerização)

### O que é?

**Docker** empacota a aplicação + dependências num "container" isolado. Pensa nele como uma "máquina virtual leve".

### Problema que Resolve:

#### Sem Docker (Dependency Hell)

```
Dev Machine:
- PHP 8.3
- PostgreSQL 16
- Redis 7
- Node 20

Production Server:
- PHP 8.1 ← Diferente!
- PostgreSQL 14 ← Diferente!
- Redis 6 ← Diferente!
- Node 18 ← Diferente!

Resultado: "Works on my machine!"
```

#### Com Docker (Consistency)

```
Dockerfile define:
- PHP 8.3
- PostgreSQL 16
- Redis 7
- Node 20

→ Funciona igual em:
 - Dev machine
 - Staging server
 - Production server
```

---

## 2. DOCKER COMPOSE (Orquestração)

### O que é?

**Docker Compose** define e corre múltiplos containers juntos.

### Docker Compose no OrionOne:

```yaml
# docker-compose.yml
version: "3.8"

services:
 # Laravel App
 app:
 build:
 context: .
 dockerfile: Dockerfile
 image: orionone-app
 container_name: orionone-app
 restart: unless-stopped
 working_dir: /var/www
 volumes:
 - ./:/var/www
 networks:
 - orionone-network
 depends_on:
 - postgres
 - redis
 environment:
 - APP_ENV=local
 - APP_DEBUG=true
 - DB_CONNECTION=pgsql
 - DB_HOST=postgres
 - DB_PORT=5432
 - DB_DATABASE=orionone
 - DB_USERNAME=orionone
 - DB_PASSWORD=secret
 - REDIS_HOST=redis
 - REDIS_PORT=6379

 # Nginx Web Server
 nginx:
 image: nginx:alpine
 container_name: orionone-nginx
 restart: unless-stopped
 ports:
 - "80:80"
 - "443:443"
 volumes:
 - ./:/var/www
 - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
 networks:
 - orionone-network
 depends_on:
 - app

 # PostgreSQL Database
 postgres:
 image: postgres:16-alpine
 container_name: orionone-postgres
 restart: unless-stopped
 environment:
 - POSTGRES_DB=orionone
 - POSTGRES_USER=orionone
 - POSTGRES_PASSWORD=secret
 ports:
 - "5432:5432"
 volumes:
 - postgres-data:/var/lib/postgresql/data
 networks:
 - orionone-network

 # Redis Cache/Queue
 redis:
 image: redis:7-alpine
 container_name: orionone-redis
 restart: unless-stopped
 ports:
 - "6379:6379"
 volumes:
 - redis-data:/data
 networks:
 - orionone-network

 # Queue Worker
 queue:
 build:
 context: .
 dockerfile: Dockerfile
 container_name: orionone-queue
 restart: unless-stopped
 working_dir: /var/www
 command: php artisan queue:work redis --sleep=3 --tries=3
 volumes:
 - ./:/var/www
 networks:
 - orionone-network
 depends_on:
 - app
 - redis

 # Scheduler (Cron Jobs)
 scheduler:
 build:
 context: .
 dockerfile: Dockerfile
 container_name: orionone-scheduler
 restart: unless-stopped
 working_dir: /var/www
 command: sh -c "while true; do php artisan schedule:run --verbose --no-interaction; sleep 60; done"
 volumes:
 - ./:/var/www
 networks:
 - orionone-network
 depends_on:
 - app

networks:
 orionone-network:
 driver: bridge

volumes:
 postgres-data:
 driver: local
 redis-data:
 driver: local
```

### Como Usar:

```bash
# Iniciar todos os containers
docker-compose up -d

# Ver status
docker-compose ps

# Logs
docker-compose logs -f app

# Entrar no container
docker-compose exec app bash

# Parar tudo
docker-compose down

# Rebuild (após mudanças no Dockerfile)
docker-compose up -d --build
```

---

## 3. DOCKERFILE (Imagem Laravel)

### O que é?

**Dockerfile** é a "receita" para construir a imagem Docker.

### Dockerfile do OrionOne:

```dockerfile
# Dockerfile
FROM php:8.3-fpm-alpine

# Metadata
LABEL maintainer="OrionOne Team"

# Argumentos de build
ARG USER_ID=1000
ARG GROUP_ID=1000

# Variáveis de ambiente
ENV TZ=Europe/Lisbon
ENV PHP_MEMORY_LIMIT=512M
ENV PHP_UPLOAD_MAX_FILESIZE=20M
ENV PHP_POST_MAX_SIZE=25M

# Instalar dependências do sistema
RUN apk add --no-cache \
 bash \
 curl \
 libpng-dev \
 libjpeg-turbo-dev \
 libwebp-dev \
 freetype-dev \
 postgresql-dev \
 zip \
 unzip \
 git \
 supervisor \
 npm

# Instalar extensões PHP
RUN docker-php-ext-configure gd \
 --with-freetype \
 --with-jpeg \
 --with-webp \
 && docker-php-ext-install -j$(nproc) \
 pdo \
 pdo_pgsql \
 pgsql \
 gd \
 bcmath \
 opcache \
 pcntl \
 exif

# Instalar Redis extension
RUN apk add --no-cache $PHPIZE_DEPS \
 && pecl install redis \
 && docker-php-ext-enable redis

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Configurar PHP
COPY docker/php/php.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker/php/opcache.ini /usr/local/etc/php/conf.d/opcache.ini

# Criar user não-root
RUN addgroup -g $GROUP_ID appgroup \
 && adduser -D -u $USER_ID -G appgroup appuser

# Workspace
WORKDIR /var/www

# Copiar código
COPY --chown=appuser:appgroup . /var/www

# Instalar dependências PHP
RUN composer install --no-dev --optimize-autoloader

# Instalar dependências Node.js
RUN npm ci && npm run build

# Permissões
RUN chown -R appuser:appgroup /var/www \
 && chmod -R 755 /var/www/storage \
 && chmod -R 755 /var/www/bootstrap/cache

# Mudar para user não-root
USER appuser

# Expor porta PHP-FPM
EXPOSE 9000

# Comando padrão
CMD ["php-fpm"]
```

### Build Multi-Stage (Otimizado):

```dockerfile
# Build stage (compila assets)
FROM node:20-alpine AS node-builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# App stage
FROM php:8.3-fpm-alpine

# ... (mesmas instruções acima)

# Copiar assets compilados do builder
COPY --from=node-builder /app/public/build /var/www/public/build
```

**Vantagens:**
✅ Imagem final **menor** (sem node_modules)
✅ Build mais rápido (cache de layers)

---

## 4. NGINX (Web Server)

### O que é?

**Nginx** é o web server que recebe requests HTTP e passa para o PHP-FPM.

### Fluxo de Request:

```
1. Browser → http://orionone.com/tickets
 ↓
2. Nginx (porta 80) recebe request
 ↓
3. Nginx verifica se é ficheiro estático (.css, .js, .png)
 ├─ SIM → Nginx serve diretamente (rápido!)
 └─ NÃO → Nginx passa para PHP-FPM (porta 9000)
 ↓
4. PHP-FPM executa Laravel
 ↓
5. Laravel retorna HTML
 ↓
6. Nginx envia HTML ao browser
```

### Nginx Config no OrionOne:

```nginx
# docker/nginx/default.conf
server {
 listen 80;
 server_name orionone.com www.orionone.com;
 root /var/www/public;

 # Logs
 access_log /var/log/nginx/access.log;
 error_log /var/log/nginx/error.log;

 # Index
 index index.php;

 # Character set
 charset utf-8;

 # Gzip compression
 gzip on;
 gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
 gzip_min_length 1000;

 # Security headers
 add_header X-Frame-Options "SAMEORIGIN" always;
 add_header X-Content-Type-Options "nosniff" always;
 add_header X-XSS-Protection "1; mode=block" always;
 add_header Referrer-Policy "no-referrer-when-downgrade" always;
 add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

 # Main location
 location / {
 try_files $uri $uri/ /index.php?$query_string;
 }

 # PHP-FPM
 location ~ \.php$ {
 fastcgi_pass app:9000; # Nome do container Docker
 fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
 include fastcgi_params;
 fastcgi_hide_header X-Powered-By;
 }

 # Static files (cache)
 location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
 expires 1y;
 add_header Cache-Control "public, immutable";
 access_log off;
 }

 # Block hidden files
 location ~ /\. {
 deny all;
 access_log off;
 log_not_found off;
 }

 # Block access to sensitive files
 location ~ /(?:composer\.json|composer\.lock|package\.json|package-lock\.json|\.env|\.git) {
 deny all;
 access_log off;
 log_not_found off;
 }

 # Max upload size
 client_max_body_size 20M;
}
```

### HTTPS (SSL/TLS):

```nginx
server {
 listen 443 ssl http2;
 server_name orionone.com www.orionone.com;

 # SSL certificates (Let's Encrypt)
 ssl_certificate /etc/letsencrypt/live/orionone.com/fullchain.pem;
 ssl_certificate_key /etc/letsencrypt/live/orionone.com/privkey.pem;

 # SSL config
 ssl_protocols TLSv1.2 TLSv1.3;
 ssl_ciphers HIGH:!aNULL:!MD5;
 ssl_prefer_server_ciphers on;

 # HSTS (força HTTPS por 1 ano)
 add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

 # ... (resto igual)
}

# Redirect HTTP → HTTPS
server {
 listen 80;
 server_name orionone.com www.orionone.com;
 return 301 https://$server_name$request_uri;
}
```

---

## 5. DEPLOYMENT (Produção)

### 1. **Setup Inicial**

#### No Servidor (DigitalOcean/AWS/Hetzner):

```bash
# 1. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Instalar Docker Compose
sudo apt install docker-compose-plugin

# 3. Clone repositório
git clone https://github.com/your-org/orionone.git
cd orionone

# 4. Configurar .env
cp .env.example .env.production
nano .env.production
```

```env
# .env.production
APP_ENV=production
APP_DEBUG=false
APP_URL=https://orionone.com

DB_CONNECTION=pgsql
DB_HOST=postgres
DB_DATABASE=orionone
DB_USERNAME=orionone
DB_PASSWORD=STRONG_PASSWORD_HERE

REDIS_HOST=redis

MAIL_MAILER=smtp
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
```

```bash
# 5. Build & Run
docker-compose -f docker-compose.prod.yml up -d --build

# 6. Migrations
docker-compose exec app php artisan migrate --force

# 7. Optimize
docker-compose exec app php artisan config:cache
docker-compose exec app php artisan route:cache
docker-compose exec app php artisan view:cache
```

---

### 2. **CI/CD (GitHub Actions)**

#### Workflow Automático:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
 push:
 branches: [main]

jobs:
 deploy:
 runs-on: ubuntu-latest

 steps:
 - name: Checkout code
 uses: actions/checkout@v4

 - name: Setup PHP
 uses: shivammathur/setup-php@v2
 with:
 php-version: 8.3
 extensions: pdo, pgsql, redis, gd

 - name: Install Composer dependencies
 run: composer install --no-dev --optimize-autoloader

 - name: Run tests
 run: php artisan test

 - name: Build assets
 run: |
 npm ci
 npm run build

 - name: Deploy to server
 uses: appleboy/ssh-action@v1.0.0
 with:
 host: ${{ secrets.SERVER_HOST }}
 username: ${{ secrets.SERVER_USERNAME }}
 key: ${{ secrets.SSH_PRIVATE_KEY }}
 script: |
 cd /var/www/orionone
 git pull origin main
 docker-compose exec -T app composer install --no-dev
 docker-compose exec -T app php artisan migrate --force
 docker-compose exec -T app php artisan config:cache
 docker-compose exec -T app php artisan route:cache
 docker-compose exec -T app php artisan view:cache
 docker-compose restart app

 - name: Notify success
 if: success()
 run: echo "Deploy successful!"
```

**Fluxo:**

```
1. Push para branch main
 ↓
2. GitHub Actions roda testes
 ↓
3. Se testes passam → Deploy automático
 ↓
4. SSH para servidor
 ↓
5. Git pull
 ↓
6. Rebuild containers
 ↓
7. Run migrations
 ↓
8. Cache optimize
 ↓
9. Restart app
```

---

### 3. **Zero-Downtime Deployment**

#### Blue-Green Deployment:

```yaml
# docker-compose.blue-green.yml
services:
 app-blue:
 build: .
 environment:
 - COLOR=blue

 app-green:
 build: .
 environment:
 - COLOR=green

 nginx:
 image: nginx:alpine
 volumes:
 - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
 ports:
 - "80:80"
 depends_on:
 - app-blue
 - app-green
```

```nginx
# docker/nginx/nginx.conf
upstream backend {
 server app-blue:9000 max_fails=3 fail_timeout=30s;
 server app-green:9000 max_fails=3 fail_timeout=30s backup;
}
```

**Processo:**

1. **Blue** (produção atual) está a correr
2. Deploy novo código para **Green**
3. Testa **Green**
4. Switch Nginx de **Blue** → **Green**
5. Se erro: Rollback para **Blue**

---

### 4. **Monitoring (Observabilidade)**

#### Laravel Telescope (Development):

```bash
# Já configurado no OrionOne
php artisan telescope:install
php artisan migrate

# Aceder em: /telescope
```

#### Laravel Horizon (Queue Monitoring):

```bash
composer require laravel/horizon
php artisan horizon:install
php artisan migrate

# Worker
php artisan horizon

# Dashboard: /horizon
```

#### Logs (Production):

```bash
# Ver logs em tempo real
docker-compose logs -f app

# Logs estruturados (JSON)
# config/logging.php
'stack' => [
 'driver' => 'stack',
 'channels' => ['daily', 'slack'],
 'ignore_exceptions' => false,
],

'daily' => [
 'driver' => 'daily',
 'path' => storage_path('logs/laravel.log'),
 'level' => env('LOG_LEVEL', 'debug'),
 'days' => 14,
],

'slack' => [
 'driver' => 'slack',
 'url' => env('LOG_SLACK_WEBHOOK_URL'),
 'username' => 'OrionOne Logger',
 'emoji' => ':boom:',
 'level' => 'critical',
],
```

---

### 5. **Backup Automático**

#### Script de Backup:

```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker-compose exec -T postgres pg_dump -U orionone orionone > "$BACKUP_DIR/database.sql"

# Backup storage (uploads)
tar -czf "$BACKUP_DIR/storage.tar.gz" storage/app/public

# Backup .env
cp .env "$BACKUP_DIR/.env"

echo "Backup completed: $BACKUP_DIR"

# Upload para S3 (AWS)
aws s3 sync $BACKUP_DIR s3://orionone-backups/$DATE/

# Limpar backups antigos (> 30 dias)
find /backups -type d -mtime +30 -exec rm -rf {} +
```

#### Cron Job:

```bash
# crontab -e
0 2 * * * /var/www/orionone/scripts/backup.sh >> /var/log/backup.log 2>&1
# Backup diário às 2h da manhã
```

---

### 6. **Health Checks**

#### Endpoint de Health:

```php
// routes/web.php
Route::get('/health', function () {
 try {
 // Check DB
 DB::connection()->getPdo();

 // Check Redis
 Cache::store('redis')->get('health_check');

 // Check Storage
 Storage::disk('public')->exists('test');

 return response()->json([
 'status' => 'healthy',
 'timestamp' => now(),
 ]);
 } catch (\Exception $e) {
 return response()->json([
 'status' => 'unhealthy',
 'error' => $e->getMessage(),
 ], 503);
 }
});
```

#### Docker Healthcheck:

```dockerfile
# Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
 CMD curl -f http://localhost/health || exit 1
```

#### Uptime Monitoring (External):

- **UptimeRobot**: https://uptimerobot.com (free)
- **Pingdom**: https://pingdom.com
- **StatusCake**: https://statuscake.com

---

## 7. SEGURANÇA

### 1. **Firewall (UFW)**

```bash
# Permitir apenas SSH, HTTP, HTTPS
sudo ufw allow 22/tcp # SSH
sudo ufw allow 80/tcp # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable
```

### 2. **Fail2Ban (Proteção contra Brute Force)**

```bash
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
```

### 3. **Secrets Management**

```bash
# Nunca commitar .env!
# .gitignore
.env
.env.production
```

```yaml
# GitHub Actions Secrets
# Settings → Secrets → Actions
SERVER_HOST: 123.45.67.89
SERVER_USERNAME: deploy
SSH_PRIVATE_KEY: -----BEGIN RSA PRIVATE KEY-----...
```

---

## 8. PERFORMANCE TUNING

### 1. **PHP-FPM Tuning**

```ini
; docker/php/php-fpm.conf
pm = dynamic
pm.max_children = 50
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.max_requests = 500
```

### 2. **OPcache**

```ini
; docker/php/opcache.ini
opcache.enable=1
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0 ; Production
opcache.revalidate_freq=0
```

### 3. **Nginx Tuning**

```nginx
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
client_max_body_size 20M;
```

---

## RESUMO: Stack DevOps

| Tecnologia | Propósito | Comandos |
| ------------------ | --------------- | ---------------------------- |
| **Docker** | Containerização | `docker build`, `docker run` |
| **Docker Compose** | Multi-container | `docker-compose up -d` |
| **Nginx** | Web server | Porta 80/443 |
| **PHP-FPM** | PHP processor | Porta 9000 |
| **Supervisor** | Process manager | Queue workers |
| **GitHub Actions** | CI/CD | Auto deploy |
| **Let's Encrypt** | SSL/TLS | Certificados grátis |

---

## CHECKLIST DE DEPLOY

- [ ] `.env.production` configurado
- [ ] Database backups automáticos
- [ ] SSL/TLS configurado (HTTPS)
- [ ] Firewall ativo (UFW)
- [ ] Monitoring ativo (logs)
- [ ] Health checks configurados
- [ ] CI/CD pipeline funcional
- [ ] Secrets no GitHub Actions
- [ ] OPcache ativado
- [ ] Redis cache funcional
- [ ] Queue workers a correr
- [ ] Scheduler (cron) ativo
- [ ] Error tracking (Sentry/Bugsnag)

---

## Conclusão dos Guias Técnicos

Completaste os **4 guias técnicos do OrionOne**:

1. **[TECH-DEEP-DIVE-BACKEND.md](./TECH-DEEP-DIVE-BACKEND.md)** - Laravel, PHP, Spatie
2. **[TECH-DEEP-DIVE-FRONTEND.md](./TECH-DEEP-DIVE-FRONTEND.md)** - Vue, Inertia, Tailwind
3. **[TECH-DEEP-DIVE-DATABASE.md](./TECH-DEEP-DIVE-DATABASE.md)** - PostgreSQL, Redis
4. **[TECH-DEEP-DIVE-DEVOPS.md](./TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx (este)

**Agora sabes:**

- Como funciona CADA tecnologia do projeto
- Porque foi escolhida
- Como usá-la no contexto do OrionOne
- Exemplos práticos de código

**Para a defesa do TCC**, podes explicar com confiança:

- Stack técnica completa
- Decisões arquiteturais
- Trade-offs e alternativas
- Integração entre camadas
