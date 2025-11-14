# Deployment Guide - OrionOne ITSM

**Last Updated:** November 13, 2025

Production deployment guide for Next.js 15 + Nest.js 11 + PostgreSQL 18 stack.

---

## Pre-Deployment Checklist

- [ ] All tests passing (backend + frontend)
- [ ] Code coverage >80%
- [ ] Environment variables configured
- [ ] Database backup created
- [ ] SSL certificates ready
- [ ] Domain DNS configured

---

## Server Requirements

### Minimum Hardware

**Small Business (10-50 users):**

- 2 CPU cores, 4GB RAM, 40GB SSD

**Medium Business (50-200 users):**

- 4 CPU cores, 8GB RAM, 80GB SSD

**Large Business (200-500 users):**

- 8 CPU cores, 16GB RAM, 160GB SSD

### Software

- Ubuntu 22.04 LTS
- Node.js 20.x LTS
- PostgreSQL 18.0
- Redis 8.2
- Nginx 1.24+
- PM2 (process manager)
- Certbot (SSL certificates)

---

## Installation

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20

# Install PM2
npm install -g pm2

# Install Nginx
sudo apt install nginx -y

# Install Certbot
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Clone Repository

```bash
cd /var/www
sudo git clone https://github.com/JMSS95/OrionOne.git orionone
cd orionone
sudo chown -R $USER:$USER /var/www/orionone
```

### 3. Setup Backend

```bash
cd nest-backend
npm ci --omit=dev
cp .env.example .env
nano .env # Configure production variables
npm run build
npm run prisma:migrate:deploy
```

### 4. Setup Frontend

```bash
cd next-frontend
npm ci
cp .env.example .env.production
nano .env.production # Configure production variables
npm run build
```

---

## Environment Variables

### Backend (.env)

```bash
NODE_ENV=production
PORT=3000
DATABASE_URL=postgresql://orionone:password@localhost:5432/orionone
JWT_SECRET=your-secure-jwt-secret-min-32-chars
JWT_REFRESH_SECRET=your-secure-refresh-secret
REDIS_URL=redis://localhost:6379
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_KEY=your-master-key
AWS_S3_BUCKET=orionone-uploads
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@orionone.com
SMTP_PASSWORD=your-smtp-password
SENTRY_DSN=https://your-sentry-dsn
```

### Frontend (.env.production)

```bash
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn
```

---

## PM2 Process Management

Create `ecosystem.config.js` in project root with backend and frontend configurations.

**Configuration:**

- Backend: 2 instances (cluster mode), 500MB memory limit, port 3000
- Frontend: 2 instances (cluster mode), 1GB memory limit, port 3001

**Start applications:**

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

**Example config:** See `deployment/ecosystem.config.example.js`

---

## Nginx Configuration

### Setup Reverse Proxy

1. **Backend (API)**: Create `/etc/nginx/sites-available/orionone-api`

 - Upstream: `localhost:3000`
 - Server name: `api.yourdomain.com`
 - Proxy headers: X-Real-IP, X-Forwarded-For, X-Forwarded-Proto

2. **Frontend (SPA)**: Create `/etc/nginx/sites-available/orionone-frontend`

 - Upstream: `localhost:3001`
 - Server name: `yourdomain.com www.yourdomain.com`
 - Cache static assets: `/_next/static` (60 minutes)

3. **Enable sites:**

```bash
sudo ln -s /etc/nginx/sites-available/orionone-api /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/orionone-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Example configs:** See `deployment/nginx/` directory

---

## SSL/TLS (Let's Encrypt)

```bash
# Obtain certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal (runs twice daily)
sudo systemctl enable certbot.timer
```

---

## Database Optimization

**PostgreSQL tuning** (edit `/etc/postgresql/18/main/postgresql.conf`):

- `shared_buffers = 256MB` (25% of RAM)
- `effective_cache_size = 1GB` (50% of RAM)
- `work_mem = 16MB`
- `maintenance_work_mem = 128MB`
- `max_connections = 100`

**Apply changes:**

```bash
sudo systemctl restart postgresql
```

---

## Backup Strategy

### Automated Daily Backups

Create `/usr/local/bin/backup-orionone.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/orionone"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
docker exec orionone_postgres pg_dump -U orionone -d orionone -F c > $BACKUP_DIR/db_$DATE.dump
gzip $BACKUP_DIR/db_$DATE.dump

# Keep last 7 days
find $BACKUP_DIR -name "*.dump.gz" -mtime +7 -delete
```

Make executable and schedule:

```bash
sudo chmod +x /usr/local/bin/backup-orionone.sh
sudo crontab -e
```

Add cron job (daily at 2 AM):

```cron
0 2 * * * /usr/local/bin/backup-orionone.sh
```

### Restore Database

```bash
gunzip -c /var/backups/orionone/db_20251113.dump.gz | \
 docker exec -i orionone_postgres pg_restore -U orionone -d orionone -c
```

---

## Monitoring

### PM2 Monitoring

```bash
pm2 monit # Real-time monitoring
pm2 logs # View logs
pm2 status # Check status
```

### Health Checks

```bash
# Backend API
curl https://api.yourdomain.com/health

# Frontend
curl https://yourdomain.com
```

---

## Security Checklist

- [ ] Environment files secured (chmod 600)
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured (UFW: allow 80, 443, 22)
- [ ] Strong database passwords
- [ ] Redis password protected
- [ ] SSH key-based authentication only
- [ ] Fail2ban configured
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] Regular security updates

---

## Updates & Maintenance

### Update Application

```bash
cd /var/www/orionone

# Stop applications
pm2 stop all

# Backup database
/usr/local/bin/backup-orionone.sh

# Pull latest code
git pull origin main

# Backend
cd nest-backend
npm ci
npm run build
npm run prisma:migrate:deploy

# Frontend
cd ../next-frontend
npm ci
npm run build

# Restart
pm2 restart all
```

### System Updates

```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart nginx
pm2 restart all
```

---

## Troubleshooting

### 502 Bad Gateway

```bash
pm2 status # Check if apps are running
pm2 logs orionone-backend # Check backend logs
sudo tail -f /var/log/nginx/error.log
```

### Database Connection Fails

```bash
docker ps | grep postgres
docker logs orionone_postgres
cat nest-backend/.env | grep DATABASE_URL
```

### High Memory Usage

```bash
pm2 monit # Check memory usage
pm2 restart all # Restart applications
```

---

## Support

- **Documentation:** [`docs/`](docs/)
- **Tech Stack:** [`TECH-STACK.md`](TECH-STACK.md)
- **Commands:** [`docs/COMMANDS-REFERENCE.md`](docs/COMMANDS-REFERENCE.md)
- **Issues:** [GitHub Issues](https://github.com/JMSS95/OrionOne/issues)

---

**OrionOne ITSM Platform** • Production Deployment Guide
