# Deployment Guide - OrionOne

## Produção

### Build Assets

```bash
# Compilar assets para produção
npm run build

# Verificar que assets foram gerados
ls public/build/
```

### Optimize Laravel

```bash
# Cache de configuração
php artisan config:cache

# Cache de rotas
php artisan route:cache

# Cache de views
php artisan view:cache

# Optimize autoloader
composer install --optimize-autoloader --no-dev
```

### Migrations em Produção

```bash
# IMPORTANTE: Sempre fazer backup antes de migrations!
# pg_dump -U postgres -d orionone -F c -f backup_$(date +%Y%m%d).dump

# Executar migrations
php artisan migrate --force

# Verificar status
php artisan migrate:status
```

## Ambiente Recomendado

### Servidor

-   **OS**: Ubuntu 22.04 LTS ou superior
-   **PHP**: 8.3+ com PHP-FPM
-   **Web Server**: Nginx 1.24+
-   **Database**: PostgreSQL 16
-   **Cache**: Redis 7.x
-   **Process Manager**: Supervisor (para queues)

### Requisitos Mínimos Hardware

**Pequena Empresa (10-50 users):**

-   2 CPU cores
-   4GB RAM
-   20GB SSD

**Média Empresa (50-200 users):**

-   4 CPU cores
-   8GB RAM
-   50GB SSD

**Grande Empresa (200-500 users):**

-   8 CPU cores
-   16GB RAM
-   100GB SSD

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name orionone.example.com;
    root /var/www/orionone/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

## Supervisor Configuration (Queue Worker)

```ini
[program:orionone-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/orionone/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=www-data
numprocs=2
redirect_stderr=true
stdout_logfile=/var/www/orionone/storage/logs/worker.log
stopwaitsecs=3600
```

Restart supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start orionone-worker:*
```

## Cron Jobs (Scheduler)

Adicionar ao crontab:

```bash
* * * * * cd /var/www/orionone && php artisan schedule:run >> /dev/null 2>&1
```

## SSL/HTTPS (Certbot)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d orionone.example.com

# Auto-renewal já está configurado
sudo certbot renew --dry-run
```

## Backup Strategy

### Database Backup (Diário)

```bash
#!/bin/bash
# /usr/local/bin/backup-orionone-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/orionone"
DB_NAME="orionone"

mkdir -p $BACKUP_DIR

pg_dump -U postgres -d $DB_NAME -F c -f $BACKUP_DIR/db_$DATE.dump

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "db_*.dump" -mtime +7 -delete
```

Adicionar ao crontab:

```
0 2 * * * /usr/local/bin/backup-orionone-db.sh
```

### Files Backup (Semanal)

```bash
#!/bin/bash
# /usr/local/bin/backup-orionone-files.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/orionone"
APP_DIR="/var/www/orionone"

tar -czf $BACKUP_DIR/files_$DATE.tar.gz \
    $APP_DIR/storage/app/public \
    $APP_DIR/.env

# Manter apenas últimas 4 semanas
find $BACKUP_DIR -name "files_*.tar.gz" -mtime +28 -delete
```

## Monitoring

### Laravel Telescope (Development/Staging)

Acessível em: `https://orionone.example.com/telescope`

**IMPORTANTE**: Desativar em produção ou proteger com autenticação forte.

### Laravel Pulse (Production Monitoring)

Acessível em: `https://orionone.example.com/pulse`

Monitora:

-   Request throughput
-   Slow queries
-   Exceptions
-   Queue jobs
-   Cache hits/misses

### Log Monitoring

```bash
# Ver logs em tempo real
tail -f /var/www/orionone/storage/logs/laravel.log

# Ver erros
grep "ERROR" /var/www/orionone/storage/logs/laravel.log
```

## Security Checklist

-   [ ] `.env` com permissões 600
-   [ ] `APP_DEBUG=false` em produção
-   [ ] `APP_ENV=production`
-   [ ] Firewall configurado (UFW)
-   [ ] SSL/HTTPS ativo
-   [ ] Telescope desativado ou protegido
-   [ ] Database backups automatizados
-   [ ] Redis protegido com password
-   [ ] Fail2ban configurado
-   [ ] SSH com key-based auth
-   [ ] Rate limiting configurado
-   [ ] CORS configurado corretamente

## Troubleshooting

### 500 Internal Server Error

```bash
# Verificar logs
tail -f storage/logs/laravel.log

# Limpar cache
php artisan config:clear
php artisan cache:clear
php artisan view:clear

# Verificar permissões
sudo chown -R www-data:www-data storage bootstrap/cache
sudo chmod -R 775 storage bootstrap/cache
```

### Queue não processa jobs

```bash
# Verificar supervisor
sudo supervisorctl status orionone-worker:*

# Restart workers
sudo supervisorctl restart orionone-worker:*

# Ver logs do worker
tail -f storage/logs/worker.log
```

### Conexão database falha

```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Testar conexão
psql -U laravel -d orionone -h localhost

# Verificar .env
cat .env | grep DB_
```

## Performance Tuning

### OPcache (PHP)

Editar `/etc/php/8.3/fpm/conf.d/10-opcache.ini`:

```ini
opcache.enable=1
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=10000
opcache.validate_timestamps=0
opcache.revalidate_freq=0
```

### PostgreSQL

Editar `/etc/postgresql/16/main/postgresql.conf`:

```conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
maintenance_work_mem = 128MB
max_connections = 100
```

### Redis

Editar `/etc/redis/redis.conf`:

```conf
maxmemory 512mb
maxmemory-policy allkeys-lru
```

## Updates & Maintenance

### Atualizar aplicação

```bash
cd /var/www/orionone

# Backup
sudo -u www-data php artisan down
pg_dump -U postgres -d orionone -F c -f backup_pre_update.dump

# Pull changes
git pull origin main

# Update dependencies
composer install --no-dev --optimize-autoloader
npm install
npm run build

# Run migrations
php artisan migrate --force

# Clear cache
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Restart services
sudo supervisorctl restart orionone-worker:*
sudo systemctl reload php8.3-fpm

# Up
sudo -u www-data php artisan up
```

---

**Deployment Guide** • OrionOne ITSM Platform • 2025
