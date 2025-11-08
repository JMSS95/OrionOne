# OrionOne - Documentation Index

**Last Updated:** November 8, 2025  
**Version:** 1.0.0  
**Project Status:** Phase 1 - Setup Complete

---

## Quick Start

New to the project? Start here:

1. **[Setup Guide](../SETUP.md)** - Initial installation and configuration
2. **[Docker Guide](DOCKER-GUIDE.md)** - Container management basics
3. **[Development Guide](development-guide.md)** - Coding standards and workflows

---

## Documentation Structure

### Project Overview

| Document | Purpose | Audience | Status |
|----------|---------|----------|--------|
| [Requirements](requirements.md) | Functional and non-functional requirements | All team | Complete |
| [Architecture](architecture.md) | System design and technology choices | Developers | Complete |
| [Business Model](business-model.md) | Market analysis, pricing, go-to-market strategy | Stakeholders | Complete |
| [Tech Stack](tech-stack.md) | Technologies used and justifications | Developers | Complete |

### Development Resources

| Document | Purpose | Audience | Status |
|----------|---------|----------|--------|
| [Development Planning](development-planning.md) | Sprint roadmap, timeline, milestones | Team | Complete |
| [Implementation Checklist](implementation-checklist.md) | Step-by-step TDD implementation guide | Developers | Complete |
| [Development Guide](development-guide.md) | Coding standards, workflows, best practices | Developers | Complete |
| [Database Schema](database-schema.md) | Entity relationships and migrations | Developers | Complete |

### Setup & Operations

| Document | Purpose | Audience | Status |
|----------|---------|----------|--------|
| [Setup Changelog](SETUP-CHANGELOG.md) | Phase 1 setup changes log | Developers | Complete |
| [Docker Guide](DOCKER-GUIDE.md) | Docker basics for beginners | All team | Complete |
| [Components Guide](COMPONENTS-GUIDE.md) | UI components usage examples | Frontend | Complete |
| [Components Summary](COMPONENTS-SUMMARY.md) | Quick component reference | Frontend | Complete |

---

## Essential Commands Reference

### Git Workflow

```bash
# Check status
git status

# Create feature branch
git checkout -b feat/feature-name

# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat: add user authentication"

# Push to remote
git push origin feat/feature-name

# Create Pull Request on GitHub
# Navigate to: https://github.com/JMSS95/OrionOne/pulls

# Sync with main branch
git checkout main
git pull origin main
git checkout feat/feature-name
git merge main
```

**Conventional Commit Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting (no logic change)
- `refactor:` Code restructuring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### GitHub Operations

```bash
# Clone repository
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# Check remote
git remote -v

# Fetch latest changes
git fetch origin

# View branches
git branch -a

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name
```

**Protected Branch Rules:**
- `main` branch requires Pull Request
- Cannot force push to `main`
- All PRs must pass CI checks

### Docker Management

```bash
# Start all containers
docker-compose up -d

# Stop all containers
docker-compose down

# View running containers
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# Execute command in container
docker-compose exec [service-name] [command]

# Rebuild containers
docker-compose up -d --build

# Remove all containers and volumes (CAUTION: Deletes data!)
docker-compose down -v
```

**Service Names:**
- `orionone-app` - PHP application
- `orionone-frontend` - Vite dev server
- `orionone-nginx` - Web server (port 8888)
- `orionone-postgres` - Database (port 5432)
- `orionone-redis` - Cache (port 6379)

### Laravel Artisan Commands

```bash
# Run migrations
docker-compose exec orionone-app php artisan migrate

# Fresh migrations with seeders
docker-compose exec orionone-app php artisan migrate:fresh --seed

# Create new migration
docker-compose exec orionone-app php artisan make:migration create_table_name

# Create model with migration and factory
docker-compose exec orionone-app php artisan make:model ModelName -mf

# Create controller
docker-compose exec orionone-app php artisan make:controller ControllerName

# Run tests
docker-compose exec orionone-app php artisan test

# Run specific test file
docker-compose exec orionone-app php artisan test --filter=TestName

# Clear all caches
docker-compose exec orionone-app php artisan optimize:clear

# Generate IDE helpers
docker-compose exec orionone-app php artisan ide-helper:generate
docker-compose exec orionone-app php artisan ide-helper:models --write
```

### PowerShell (Windows) Commands

```powershell
# Navigate to project
cd C:\laragon\www\orionone

# List directory contents
ls
Get-ChildItem

# View file contents
Get-Content file.txt
cat file.txt

# Find files
Get-ChildItem -Recurse -Filter "*.php"

# Search in files
Select-String -Path "*.php" -Pattern "searchterm"

# Check port usage
netstat -ano | findstr :8888

# Kill process by port
# Get PID from netstat, then:
taskkill /PID <process_id> /F

# Environment variables
$env:VARIABLE_NAME

# Run PowerShell script
.\scripts\feature.ps1 "FeatureName"
```

### Bash (Linux/Mac) Commands

```bash
# Navigate to project
cd ~/projects/orionone

# List directory contents
ls -la

# View file contents
cat file.txt

# Find files
find . -name "*.php"

# Search in files
grep -r "searchterm" --include="*.php"

# Check port usage
lsof -i :8888

# Kill process by port
kill -9 $(lsof -t -i:8888)

# Environment variables
export VARIABLE_NAME=value

# Run bash script
./scripts/feature.sh "FeatureName"
```

### NPM Commands

```bash
# Install dependencies
npm install

# Run development server (in Docker via docker-compose)
npm run dev

# Build for production
npm run build

# Run linter
npm run lint

# Fix linting issues
npm run lint:fix
```

### Composer Commands

```bash
# Install dependencies
docker-compose exec orionone-app composer install

# Update dependencies
docker-compose exec orionone-app composer update

# Require new package
docker-compose exec orionone-app composer require vendor/package

# Remove package
docker-compose exec orionone-app composer remove vendor/package

# Dump autoload
docker-compose exec orionone-app composer dump-autoload
```

---

## Development Workflow

### Creating a New Feature

1. **Create feature branch**
   ```bash
   git checkout -b feat/feature-name
   ```

2. **Write tests first (TDD)**
   ```bash
   php artisan make:test FeatureTest
   # Write failing tests
   php artisan test --filter=FeatureTest
   ```

3. **Implement feature**
   - Follow coding standards in [development-guide.md](development-guide.md)
   - Use Laravel Actions pattern
   - Use Spatie Data for DTOs

4. **Run tests**
   ```bash
   php artisan test
   ```

5. **Run code quality checks**
   ```bash
   ./vendor/bin/phpstan analyse
   ./vendor/bin/pint
   ```

6. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add feature description"
   ```

7. **Push and create PR**
   ```bash
   git push origin feat/feature-name
   # Create PR on GitHub
   ```

### Fixing a Bug

1. **Create bugfix branch**
   ```bash
   git checkout -b fix/bug-description
   ```

2. **Write regression test**
   ```bash
   # Create test that reproduces the bug
   php artisan test --filter=BugTest
   # Should fail
   ```

3. **Fix the bug**
   - Make minimal changes
   - Keep fix focused

4. **Verify fix**
   ```bash
   php artisan test --filter=BugTest
   # Should pass
   php artisan test
   # All tests should pass
   ```

5. **Commit and PR**
   ```bash
   git add .
   git commit -m "fix: resolve bug description"
   git push origin fix/bug-description
   ```

---

## Code Quality Standards

### Required Checks Before Commit

```bash
# 1. Run tests
php artisan test

# 2. Run PHPStan
./vendor/bin/phpstan analyse

# 3. Run Pint formatter
./vendor/bin/pint

# 4. Check test coverage (aim for >90%)
php artisan test --coverage --min=90
```

### Pre-commit Checklist

- [ ] All tests passing
- [ ] No PHPStan errors (Level 5)
- [ ] Code formatted with Pint
- [ ] Test coverage >90%
- [ ] No console.log in frontend code
- [ ] Migrations run successfully
- [ ] Docker containers running
- [ ] No sensitive data in commits

---

## Environment Variables

### Required `.env` Variables

```bash
# Application
APP_NAME=OrionOne
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8888

# Database
DB_CONNECTION=pgsql
DB_HOST=orionone-postgres
DB_PORT=5432
DB_DATABASE=orionone
DB_USERNAME=orionone
DB_PASSWORD=secret

# Redis
REDIS_HOST=orionone-redis
REDIS_PORT=6379

# Mail (Development)
MAIL_MAILER=log
MAIL_FROM_ADDRESS=noreply@orionone.test

# Vite
VITE_APP_NAME="${APP_NAME}"
```

---

## Troubleshooting

### Common Issues

**Issue:** Port 8888 already in use
```powershell
# Windows
netstat -ano | findstr :8888
taskkill /PID <process_id> /F

# Linux/Mac
lsof -i :8888
kill -9 $(lsof -t -i:8888)
```

**Issue:** Docker containers won't start
```bash
docker-compose down
docker-compose up -d --build
```

**Issue:** Database connection failed
```bash
# Check PostgreSQL is running
docker-compose ps
docker-compose logs orionone-postgres

# Verify .env credentials match docker-compose.yml
```

**Issue:** Vite not compiling
```bash
# Restart Vite
docker-compose restart orionone-frontend

# Clear Vite cache
docker-compose exec orionone-frontend rm -rf node_modules/.vite
```

**Issue:** Tests failing
```bash
# Clear test database
php artisan migrate:fresh --env=testing

# Rebuild autoload
composer dump-autoload
```

---

## Additional Resources

### External Documentation

- [Laravel 11 Docs](https://laravel.com/docs/11.x)
- [Vue 3 Docs](https://vuejs.org/)
- [Inertia.js Docs](https://inertiajs.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/)
- [Docker Docs](https://docs.docker.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

### Package Documentation

- [Spatie Laravel Data](https://spatie.be/docs/laravel-data)
- [Laravel Actions](https://laravelactions.com/)
- [Spatie Query Builder](https://spatie.be/docs/laravel-query-builder)
- [Spatie Permission](https://spatie.be/docs/laravel-permission)
- [Spatie Activity Log](https://spatie.be/docs/laravel-activitylog)

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

---

## Support

For questions or issues:
1. Check this documentation
2. Search existing GitHub issues
3. Create new issue with detailed description

---

**Maintained by:** JMSS95  
**Last Review:** November 8, 2025
