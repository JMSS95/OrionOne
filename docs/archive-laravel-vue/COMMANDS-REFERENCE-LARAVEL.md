# Commands Reference - OrionOne

**Complete command reference for development, deployment, and maintenance.**

---

## Git Commands

### Repository Basics

```bash
# Check repository status
git status

# View commit history
git log --oneline --graph --all -10

# View differences
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff HEAD~1            # Compare with previous commit
```

### Branching

```bash
# Create new branch
git checkout -b feature/feature-name

# Switch between branches
git checkout main
git checkout feature/feature-name

# List all branches
git branch -a

# Delete branch (local)
git branch -d feature/feature-name

# Delete branch (remote)
git push origin --delete feature/feature-name
```

### Committing

```bash
# Stage files
git add .                              # All files
git add file1.php file2.js            # Specific files
git add docs/                         # Directory

# Commit
git commit -m "feat: add user authentication"
git commit -m "fix: resolve login bug"
git commit -m "docs: update README"

# Amend last commit
git commit --amend -m "Updated message"

# Unstage files
git restore --staged file.php
```

### Pushing & Pulling

```bash
# Push to remote
git push origin main
git push origin feature/feature-name

# Force push (use with caution)
git push origin main --force-with-lease

# Pull from remote
git pull origin main
git pull --rebase origin main          # Rebase instead of merge

# Fetch without merging
git fetch origin
```

### Merging & Rebasing

```bash
# Merge branch into current
git merge feature/feature-name
git merge origin/main

# Merge keeping our versions on conflicts
git merge origin/main --strategy-option ours

# Rebase
git rebase main
git rebase --continue                  # After resolving conflicts
git rebase --abort                     # Cancel rebase

# Interactive rebase (squash commits)
git rebase -i HEAD~3
```

### Conflict Resolution

```bash
# List files with conflicts
git diff --name-only --diff-filter=U

# Resolve using ours/theirs
git checkout --ours file.php           # Keep your version
git checkout --theirs file.php         # Keep their version

# Mark as resolved
git add file.php
git commit
```

### Stashing

```bash
# Save work temporarily
git stash
git stash save "Work in progress"

# List stashes
git stash list

# Apply stash
git stash apply                        # Keep stash
git stash pop                          # Apply and remove stash
git stash pop stash@{1}               # Specific stash

# Delete stash
git stash drop
git stash clear                        # Remove all stashes
```

### Tagging

```bash
# Create tag
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"

# Push tags
git push origin v1.0.0
git push origin --tags                 # All tags

# List tags
git tag -l

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### Undoing Changes

```bash
# Discard local changes
git restore file.php                   # Single file
git restore .                          # All files

# Reset to previous commit
git reset --soft HEAD~1                # Keep changes staged
git reset --mixed HEAD~1               # Keep changes unstaged (default)
git reset --hard HEAD~1                # Discard all changes (dangerous!)

# Revert commit (creates new commit)
git revert HEAD
git revert abc123
```

---

## GitHub Commands

### Pull Requests

```bash
# Create PR branch
git checkout -b feature/new-feature
git push origin feature/new-feature
# Then create PR on GitHub UI

# Update PR
git add .
git commit -m "Address PR feedback"
git push origin feature/new-feature

# Sync with main
git checkout main
git pull origin main
git checkout feature/new-feature
git merge main
git push origin feature/new-feature
```

### GitHub CLI (gh)

```bash
# Install: https://cli.github.com/

# Login
gh auth login

# Create PR
gh pr create --title "Feature: Add authentication" --body "Description"

# List PRs
gh pr list

# View PR
gh pr view 5

# Merge PR
gh pr merge 5 --squash
gh pr merge 5 --merge
gh pr merge 5 --rebase

# Clone repository
gh repo clone JMSS95/OrionOne

# Create issue
gh issue create --title "Bug: Login fails" --body "Description"
```

---

## Docker Commands

### Container Management

```bash
# Start all containers
docker-compose up -d

# Stop all containers
docker-compose down

# Restart containers
docker-compose restart

# Restart specific service
docker-compose restart orionone-app
docker-compose restart orionone-frontend

# View running containers
docker-compose ps

# View all containers (including stopped)
docker ps -a
```

### Logs

```bash
# View logs
docker-compose logs                    # All services
docker-compose logs orionone-app       # Specific service
docker-compose logs --tail=50          # Last 50 lines
docker-compose logs -f                 # Follow logs (real-time)

# Filter logs by time
docker-compose logs --since 5m         # Last 5 minutes
docker-compose logs --since "2025-11-08T10:00:00"
```

### Executing Commands

```bash
# Execute command in container
docker-compose exec orionone-app bash
docker-compose exec orionone-app php artisan migrate
docker-compose exec orionone-frontend npm run dev

# Execute as different user
docker-compose exec -u sail orionone-app bash

# Execute without TTY (for CI/CD)
docker-compose exec -T orionone-app php artisan test
```

### Building & Cleaning

```bash
# Build images
docker-compose build
docker-compose build --no-cache        # Force rebuild

# Remove stopped containers
docker-compose rm

# Remove all (containers, networks, volumes)
docker-compose down -v

# Prune system
docker system prune                    # Remove unused data
docker system prune -a                 # Remove all unused images
docker volume prune                    # Remove unused volumes
```

### Docker Images

```bash
# List images
docker images

# Remove image
docker rmi image_name:tag

# Pull image
docker pull php:8.2-fpm
```

### Networks

```bash
# List networks
docker network ls

# Inspect network
docker network inspect orionone_default

# Create network
docker network create my-network
```

---

## Laravel Artisan Commands

### Application

```bash
# Via Docker
docker-compose exec orionone-app php artisan [command]

# Direct (if PHP installed locally)
php artisan [command]
```

### Database

```bash
# Run migrations
php artisan migrate

# Rollback last migration
php artisan migrate:rollback

# Rollback all migrations
php artisan migrate:reset

# Fresh migrations (drop all tables)
php artisan migrate:fresh

# Fresh migrations with seeders
php artisan migrate:fresh --seed

# Run seeders
php artisan db:seed
php artisan db:seed --class=UserSeeder

# Create migration
php artisan make:migration create_tickets_table
php artisan make:migration add_avatar_to_users_table
```

### Models & Factories

```bash
# Create model
php artisan make:model Ticket

# Model with migration
php artisan make:model Ticket -m

# Model with migration, factory, seeder
php artisan make:model Ticket -mfs

# Create factory
php artisan make:factory TicketFactory

# Create seeder
php artisan make:seeder TicketSeeder
```

### Controllers

```bash
# Create controller
php artisan make:controller TicketController

# Resource controller (CRUD methods)
php artisan make:controller TicketController --resource

# API resource controller
php artisan make:controller Api/TicketController --api

# Invokable controller (single action)
php artisan make:controller ProcessTicketController --invokable
```

### Requests & Validation

```bash
# Create form request
php artisan make:request StoreTicketRequest
php artisan make:request UpdateTicketRequest
```

### Policies

```bash
# Create policy
php artisan make:policy TicketPolicy

# Policy for model
php artisan make:policy TicketPolicy --model=Ticket
```

### Jobs & Queues

```bash
# Create job
php artisan make:job ProcessTicket

# Run queue worker
php artisan queue:work
php artisan queue:work --once          # Process one job
php artisan queue:work --stop-when-empty

# List failed jobs
php artisan queue:failed

# Retry failed job
php artisan queue:retry all
php artisan queue:retry 5              # Specific job ID

# Clear failed jobs
php artisan queue:flush
```

### Cache

```bash
# Clear all caches
php artisan optimize:clear

# Individual caches
php artisan cache:clear                # Application cache
php artisan config:clear               # Configuration cache
php artisan route:clear                # Route cache
php artisan view:clear                 # Compiled views

# Cache configuration
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### Testing

```bash
# Run all tests
php artisan test

# Run specific test file
php artisan test tests/Feature/TicketTest.php

# Run specific test method
php artisan test --filter=test_user_can_create_ticket

# Run with coverage
php artisan test --coverage

# Run with coverage minimum
php artisan test --coverage --min=80

# Parallel testing
php artisan test --parallel
```

### IDE Helper

```bash
# Generate helper files
php artisan ide-helper:generate        # _ide_helper.php
php artisan ide-helper:models          # Model docblocks
php artisan ide-helper:meta            # .phpstorm.meta.php

# Write docblocks to models
php artisan ide-helper:models --write
```

### Laravel Data (Spatie)

```bash
# Create Data class
php artisan make:data TicketData
```

### Laravel Actions (Lorisleiva)

```bash
# Create Action class
php artisan make:action CreateTicketAction
php artisan make:action Users/UpdateProfileAction
```

### Maintenance

```bash
# Put application in maintenance mode
php artisan down
php artisan down --secret="token"      # Allow access with secret

# Bring application up
php artisan up

# Generate application key
php artisan key:generate

# Clear expired password reset tokens
php artisan auth:clear-resets
```

### Telescope (Debugging)

```bash
# Publish Telescope assets
php artisan telescope:install

# Clear Telescope data
php artisan telescope:clear

# Prune old entries
php artisan telescope:prune
```

### Custom Commands

```bash
# Create custom command
php artisan make:command SendTicketReminders
```

---

## Composer Commands

### Basic Operations

```bash
# Install dependencies
composer install

# Install dependencies (production)
composer install --no-dev --optimize-autoloader

# Update dependencies
composer update

# Update specific package
composer update spatie/laravel-data

# Require new package
composer require spatie/laravel-data
composer require --dev phpstan/phpstan

# Remove package
composer remove package/name

# Show installed packages
composer show
composer show -i                       # Installed only
```

### Autoloading

```bash
# Dump autoload
composer dump-autoload

# Optimized autoload (production)
composer dump-autoload --optimize
composer dump-autoload -o
```

### Validation

```bash
# Validate composer.json
composer validate

# Check for security vulnerabilities
composer audit
```

### Scripts

```bash
# Run custom scripts (from composer.json)
composer run-script test
composer run-script format
```

---

## NPM Commands

### Installation

```bash
# Install dependencies
npm install

# Install dependencies (CI)
npm ci                                 # Clean install

# Install specific package
npm install vue
npm install --save-dev @vitejs/plugin-vue

# Install global package
npm install -g pnpm
```

### Development

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Package Management

```bash
# Update packages
npm update

# Check outdated packages
npm outdated

# Remove package
npm uninstall package-name
npm uninstall --save-dev package-name

# List installed packages
npm list
npm list --depth=0                     # Top-level only
```

### Scripts

```bash
# Run custom scripts (from package.json)
npm run format
npm run lint
npm run test
```

### Troubleshooting

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Fix permissions (Linux/Mac)
sudo chown -R $USER:$GROUP ~/.npm
sudo chown -R $USER:$GROUP node_modules
```

---

## PowerShell Commands (Windows)

### Navigation

```powershell
# Change directory
cd C:\laragon\www\orionone
Set-Location C:\laragon\www\orionone

# Go back
cd ..

# Go to home directory
cd ~

# List files
ls
Get-ChildItem
ls -Force                              # Include hidden files
```

### File Operations

```powershell
# Create directory
mkdir docs\new-folder
New-Item -ItemType Directory -Path "docs\new-folder"

# Create file
New-Item -ItemType File -Path "test.txt"
echo "content" > test.txt

# Copy files
Copy-Item file.txt backup.txt
Copy-Item -Recurse folder\ backup-folder\

# Move files
Move-Item file.txt new-location\

# Delete files
Remove-Item file.txt
Remove-Item -Recurse folder\
Remove-Item -Force file.txt            # Force delete
```

### Process Management

```powershell
# Find process
Get-Process | Where-Object {$_.ProcessName -like "*php*"}

# Kill process by PID
Stop-Process -Id 1234
Stop-Process -Name "php"

# Kill process by port
$process = Get-NetTCPConnection -LocalPort 8888 -ErrorAction SilentlyContinue
if ($process) { Stop-Process -Id $process.OwningProcess -Force }
```

### Network

```powershell
# Check port usage
netstat -ano | findstr :8888
Get-NetTCPConnection -LocalPort 8888

# Test connection
Test-NetConnection localhost -Port 8888

# Get IP address
ipconfig
Get-NetIPAddress
```

### Environment Variables

```powershell
# View environment variables
$env:PATH
Get-ChildItem Env:

# Set environment variable (session)
$env:APP_ENV = "local"

# Set environment variable (permanent)
[System.Environment]::SetEnvironmentVariable("APP_ENV", "local", "User")
```

### Execution Policy

```powershell
# Check execution policy
Get-ExecutionPolicy

# Set execution policy (allow scripts)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Set-ExecutionPolicy Bypass -Scope Process
```

---

## Bash Commands (Linux/Mac)

### Navigation

```bash
# Change directory
cd /var/www/orionone

# Go back
cd ..

# Go to home
cd ~

# List files
ls
ls -la                                 # List all with details
ls -lh                                 # Human-readable sizes
```

### File Operations

```bash
# Create directory
mkdir -p docs/new-folder

# Create file
touch test.txt
echo "content" > test.txt

# Copy files
cp file.txt backup.txt
cp -r folder/ backup-folder/

# Move files
mv file.txt new-location/

# Delete files
rm file.txt
rm -rf folder/                         # Recursive force delete
```

### File Viewing

```bash
# View file content
cat file.txt
less file.txt                          # Paginated view
head -n 20 file.txt                    # First 20 lines
tail -n 20 file.txt                    # Last 20 lines
tail -f storage/logs/laravel.log       # Follow log file
```

### Permissions

```bash
# Change permissions
chmod 755 script.sh
chmod +x script.sh                     # Make executable
chmod -R 775 storage/                  # Recursive

# Change owner
chown user:group file.txt
chown -R www-data:www-data storage/

# Current user permissions
sudo chown -R $USER:$USER .
```

### Process Management

```bash
# Find process
ps aux | grep php
pgrep -f "php artisan"

# Kill process
kill 1234                              # By PID
killall php                            # By name
pkill -f "php artisan queue"           # By pattern

# Check port usage
lsof -i :8888
netstat -tuln | grep 8888
```

### Network

```bash
# Test connection
curl http://localhost:8888
wget http://localhost:8888

# Check IP address
ifconfig
ip addr show
```

### Search

```bash
# Find files
find . -name "*.php"
find . -type f -name "User.php"

# Search in files
grep -r "function" app/
grep -r "class User" app/ --include="*.php"
```

### Compression

```bash
# Create archive
tar -czf backup.tar.gz folder/
zip -r backup.zip folder/

# Extract archive
tar -xzf backup.tar.gz
unzip backup.zip
```

---

## Database Commands

### PostgreSQL (psql)

```bash
# Connect to database
psql -U postgres -d orionone

# Inside psql
\l                                     # List databases
\c orionone                           # Connect to database
\dt                                   # List tables
\d users                              # Describe table
\q                                    # Quit

# Execute SQL file
psql -U postgres -d orionone -f dump.sql

# Backup database
pg_dump -U postgres orionone > backup.sql

# Restore database
psql -U postgres orionone < backup.sql
```

### Via Docker

```bash
# Connect to PostgreSQL in Docker
docker-compose exec orionone-postgres psql -U postgres -d orionone

# Backup
docker-compose exec orionone-postgres pg_dump -U postgres orionone > backup.sql

# Restore
docker-compose exec -T orionone-postgres psql -U postgres orionone < backup.sql

# Execute SQL
docker-compose exec orionone-postgres psql -U postgres -d orionone -c "SELECT * FROM users;"
```

---

## Testing Commands

### PHPUnit

```bash
# Run all tests
./vendor/bin/phpunit

# Run specific test file
./vendor/bin/phpunit tests/Feature/TicketTest.php

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage

# Run with filter
./vendor/bin/phpunit --filter=testUserCanCreateTicket
```

### PHPStan (Static Analysis)

```bash
# Analyze code
./vendor/bin/phpstan analyse

# Specific level (0-9)
./vendor/bin/phpstan analyse --level=5

# With configuration file
./vendor/bin/phpstan analyse -c phpstan.neon
```

### Laravel Pint (Code Formatting)

```bash
# Format code
./vendor/bin/pint

# Dry run (preview changes)
./vendor/bin/pint --test

# Specific paths
./vendor/bin/pint app/Models
```

---

## Production Deployment

### Preparation

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
composer install --no-dev --optimize-autoloader
npm ci
npm run build

# 3. Run migrations
php artisan migrate --force

# 4. Clear and cache
php artisan optimize:clear
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 5. Restart queue workers
php artisan queue:restart

# 6. Set permissions
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache
```

### Zero-Downtime Deployment

```bash
# 1. Put in maintenance mode
php artisan down --secret="your-secret-token"

# 2. Deploy updates (steps above)

# 3. Bring application up
php artisan up
```

---

## Troubleshooting

### Common Issues

```bash
# Storage permission errors
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache

# Class not found
composer dump-autoload

# Config cached
php artisan config:clear
php artisan cache:clear

# Route not working
php artisan route:clear
php artisan route:cache

# Node modules issues
rm -rf node_modules package-lock.json
npm install

# Docker issues
docker-compose down -v
docker-compose up -d --build

# Database connection errors
php artisan config:clear
# Check .env file
# Restart database container
docker-compose restart orionone-postgres
```

### Logs

```bash
# Laravel logs
tail -f storage/logs/laravel.log

# Docker logs
docker-compose logs -f orionone-app

# Nginx logs (if using)
tail -f /var/log/nginx/error.log
```

---

## Useful Aliases

Add to `.bashrc` or `.zshrc`:

```bash
# Laravel
alias art="php artisan"
alias mfs="php artisan migrate:fresh --seed"
alias pint="./vendor/bin/pint"
alias stan="./vendor/bin/phpstan analyse"

# Docker
alias dcu="docker-compose up -d"
alias dcd="docker-compose down"
alias dcr="docker-compose restart"
alias dcl="docker-compose logs -f"
alias dce="docker-compose exec"

# Git
alias gs="git status"
alias ga="git add ."
alias gc="git commit -m"
alias gp="git push origin"
alias gl="git log --oneline --graph --all -10"

# NPM
alias nrd="npm run dev"
alias nrb="npm run build"
```

---

**Last Updated:** 08 November 2025
**Version:** 1.0
**Project:** OrionOne ITSM
