# Commands Reference - OrionOne ITSM

**Complete command reference for development, deployment, and maintenance.**

**Stack:** Next.js 15 + Nest.js 11 + PostgreSQL 18 + Redis 8.2 + Meilisearch 1.25
**Last Updated:** 13 November 2025

---

## Table of Contents

1. [Git Commands](#git-commands)
2. [GitHub Commands](#github-commands)
3. [Docker Commands](#docker-commands)
4. [Nest.js Backend Commands](#nestjs-backend-commands)
5. [Next.js Frontend Commands](#nextjs-frontend-commands)
6. [Prisma ORM Commands](#prisma-orm-commands)
7. [npm Commands](#npm-commands)
8. [Database Commands (PostgreSQL)](#database-commands-postgresql)
9. [Testing Commands](#testing-commands)
10. [Deployment Commands](#deployment-commands)
11. [Troubleshooting](#troubleshooting)

---

## Git Commands

### Repository Basics

```bash
# Check repository status
git status

# View commit history
git log --oneline --graph --all -10
git log --oneline --author="Your Name" -10

# View differences
git diff # Unstaged changes
git diff --staged # Staged changes
git diff HEAD~1 # Compare with previous commit
git diff main..feature/branch # Compare branches
```

### Branching

```bash
# Create new branch from current
git checkout -b feature/ticket-system
git checkout -b fix/login-bug

# Switch between branches
git checkout main
git checkout feat/migrate-nextjs-nestjs

# List all branches
git branch -a # All branches (local + remote)
git branch -r # Remote branches only

# Delete branch (local)
git branch -d feature/old-feature
git branch -D feature/old-feature # Force delete

# Delete branch (remote)
git push origin --delete feature/old-feature

# Rename branch
git branch -m old-name new-name
```

### Committing (Conventional Commits)

```bash
# Stage files
git add . # All files
git add src/ # Directory
git add nest-backend/src/auth/ # Specific path
git add next-frontend/app/ # Frontend changes

# Commit with conventional commit format
git commit -m "feat(auth): add JWT authentication"
git commit -m "fix(tickets): resolve status update bug"
git commit -m "docs(readme): update installation steps"
git commit -m "chore(deps): update to Next.js 15.5.6"
git commit -m "refactor(api): improve error handling"
git commit -m "test(auth): add login integration tests"
git commit -m "perf(db): add indexes to tickets table"
git commit -m "style(ui): format with Prettier"

# Multi-line commit
git commit -m "feat(tickets): implement ticket creation" \
-m "- Add CreateTicketDto validation" \
-m "- Add Prisma ticket model" \
-m "- Add API endpoint POST /api/tickets"

# Amend last commit
git commit --amend -m "Updated message"
git commit --amend --no-edit # Keep message

# Unstage files
git restore --staged file.ts
git restore --staged .
```

### Pushing & Pulling

```bash
# Push to remote
git push origin main
git push origin feat/migrate-nextjs-nestjs

# Push new branch
git push -u origin feature/new-feature

# Force push (use with caution)
git push origin main --force-with-lease # Safer than --force

# Pull from remote
git pull origin main
git pull --rebase origin main # Rebase instead of merge

# Fetch without merging
git fetch origin
git fetch --all
```

### Merging & Rebasing

```bash
# Merge branch into current
git merge feature/ticket-system
git merge origin/main

# Merge keeping our versions on conflicts
git merge origin/main --strategy-option ours

# Rebase current branch onto main
git rebase main
git rebase --continue # After resolving conflicts
git rebase --abort # Cancel rebase

# Interactive rebase (squash commits)
git rebase -i HEAD~3
git rebase -i main # Rebase all commits since main
```

### Conflict Resolution

```bash
# List files with conflicts
git diff --name-only --diff-filter=U
git status | grep "both modified"

# Resolve using ours/theirs
git checkout --ours file.ts # Keep your version
git checkout --theirs file.ts # Keep their version

# Mark as resolved
git add file.ts
git commit

# Abort merge/rebase
git merge --abort
git rebase --abort
```

### Stashing

```bash
# Save work temporarily
git stash
git stash save "WIP: ticket creation feature"
git stash push -m "WIP: authentication" src/auth/

# List stashes
git stash list

# Apply stash
git stash apply # Keep stash
git stash pop # Apply and remove stash
git stash pop stash@{1} # Specific stash

# Show stash content
git stash show
git stash show -p stash@{0} # Show diff

# Delete stash
git stash drop stash@{0}
git stash clear # Remove all stashes
```

### Tagging

```bash
# Create tag (semantic versioning)
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0 - MVP Release"
git tag -a v0.1.0 -m "Sprint 1 Complete"

# Push tags
git push origin v1.0.0
git push origin --tags # All tags

# List tags
git tag -l
git tag -l "v1.*" # Filter tags

# Delete tag
git tag -d v1.0.0 # Local
git push origin --delete v1.0.0 # Remote

# Checkout tag
git checkout v1.0.0
```

### Undoing Changes

```bash
# Discard local changes
git restore file.ts # Single file
git restore . # All files
git restore src/ # Directory

# Reset to previous commit
git reset --soft HEAD~1 # Keep changes staged
git reset --mixed HEAD~1 # Keep changes unstaged (default)
git reset --hard HEAD~1 # Discard all changes (dangerous!)

# Reset to specific commit
git reset --hard abc123

# Revert commit (creates new commit)
git revert HEAD
git revert abc123
git revert HEAD~3..HEAD # Revert multiple commits
```

### Git Worktree (Work on multiple branches)

```bash
# Create worktree for hotfix
git worktree add ../orionone-hotfix hotfix/critical-bug

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../orionone-hotfix
```

---

## GitHub Commands

### Pull Requests

```bash
# Create PR branch
git checkout -b feature/user-dashboard
git push -u origin feature/user-dashboard
# Then create PR on GitHub UI

# Update PR after feedback
git add .
git commit -m "refactor: address PR review comments"
git push origin feature/user-dashboard

# Sync with main (rebase)
git checkout main
git pull origin main
git checkout feature/user-dashboard
git rebase main # Rebase onto latest main
git push origin feature/user-dashboard --force-with-lease

# Sync with main (merge)
git checkout feature/user-dashboard
git merge main
git push origin feature/user-dashboard
```

### GitHub CLI (gh)

```bash
# Install: https://cli.github.com/
# Windows: winget install GitHub.cli
# Mac: brew install gh

# Login
gh auth login

# Repository operations
gh repo clone JMSS95/OrionOne
gh repo view
gh repo view --web # Open in browser

# Pull Requests
gh pr create --title "feat: Add ticket dashboard" \
 --body "Implements ticket listing and filtering"
gh pr create --draft # Create draft PR

# List PRs
gh pr list
gh pr list --state open
gh pr list --author @me

# View PR
gh pr view 5
gh pr view 5 --web # Open in browser
gh pr diff 5 # Show diff

# Checkout PR locally
gh pr checkout 5

# Review PR
gh pr review 5 --approve
gh pr review 5 --request-changes --body "Comments"
gh pr review 5 --comment --body "Looks good!"

# Merge PR
gh pr merge 5 --squash
gh pr merge 5 --merge
gh pr merge 5 --rebase
gh pr merge 5 --delete-branch # Delete after merge

# Issues
gh issue create --title "Bug: Login fails on mobile" \
 --body "Description" --label bug
gh issue list
gh issue view 10
gh issue close 10
gh issue reopen 10

# Actions (CI/CD)
gh workflow list
gh workflow view
gh run list
gh run view
gh run watch # Watch live run
```

---

## Docker Commands

### Container Management

```bash
# Start all containers
docker-compose up -d

# Start with rebuild
docker-compose up -d --build

# Stop all containers
docker-compose down

# Stop and remove volumes ( deletes data)
docker-compose down -v

# Restart containers
docker-compose restart

# Restart specific service
docker-compose restart orionone-backend
docker-compose restart orionone-frontend
docker-compose restart orionone-db

# View running containers
docker-compose ps
docker ps # All Docker containers

# View all containers (including stopped)
docker ps -a
```

### Logs

```bash
# View logs
docker-compose logs # All services
docker-compose logs orionone-backend # Backend logs
docker-compose logs orionone-frontend # Frontend logs
docker-compose logs orionone-db # PostgreSQL logs
docker-compose logs orionone-redis # Redis logs
docker-compose logs orionone-meilisearch # Meilisearch logs

# Last N lines
docker-compose logs --tail=50 orionone-backend
docker-compose logs --tail=100 orionone-frontend

# Follow logs (real-time)
docker-compose logs -f
docker-compose logs -f orionone-backend

# Filter logs by time
docker-compose logs --since 5m # Last 5 minutes
docker-compose logs --since "2025-11-13T10:00:00"
docker-compose logs --since 1h orionone-backend
```

### Executing Commands in Containers

```bash
# Backend (Nest.js)
docker-compose exec orionone-backend bash
docker-compose exec orionone-backend npm run start:dev
docker-compose exec orionone-backend npx prisma studio

# Frontend (Next.js)
docker-compose exec orionone-frontend bash
docker-compose exec orionone-frontend npm run build
docker-compose exec orionone-frontend npm run lint

# Database (PostgreSQL)
docker-compose exec orionone-db psql -U postgres -d orionone
docker-compose exec orionone-db pg_dump -U postgres orionone > backup.sql

# Redis
docker-compose exec orionone-redis redis-cli
docker-compose exec orionone-redis redis-cli PING

# Meilisearch
docker-compose exec orionone-meilisearch curl http://localhost:7700/health

# Execute without TTY (for scripts/CI)
docker-compose exec -T orionone-backend npm test
```

### Building & Cleaning

```bash
# Build images
docker-compose build
docker-compose build --no-cache # Force rebuild without cache
docker-compose build orionone-backend # Build specific service

# Pull latest images
docker-compose pull

# Remove stopped containers
docker-compose rm
docker-compose rm -f # Force remove

# Remove all (containers, networks, volumes)
docker-compose down -v

# Prune Docker system
docker system prune # Remove unused data
docker system prune -a # Remove all unused images
docker system prune -a --volumes # Include volumes
docker volume prune # Remove unused volumes
docker image prune # Remove dangling images

# Show disk usage
docker system df
```

### Docker Images

```bash
# List images
docker images
docker image ls

# Remove image
docker rmi orionone-orionone-backend
docker rmi postgres:18-alpine

# Pull specific image
docker pull postgres:18-alpine
docker pull redis:8.2-alpine
docker pull getmeili/meilisearch:v1.25

# Inspect image
docker image inspect postgres:18-alpine

# Tag image
docker tag orionone-backend:latest orionone-backend:v1.0.0
```

### Networks

```bash
# List networks
docker network ls

# Inspect network
docker network inspect orionone_orionone_network

# Create network
docker network create orionone-custom-network

# Remove network
docker network rm orionone-custom-network

# Connect container to network
docker network connect orionone_orionone_network container_name
```

### Health Checks

```bash
# Check service health
docker-compose ps
docker inspect --format='{{.State.Health.Status}}' orionone_backend
docker inspect --format='{{.State.Health.Status}}' orionone_frontend
docker inspect --format='{{.State.Health.Status}}' orionone_postgres

# View health check logs
docker inspect orionone_backend | grep -A 10 Health
```

---

## Nest.js Backend Commands

### Development

```bash
# Via Docker (recommended)
docker-compose up -d orionone-backend
docker-compose logs -f orionone-backend

# Via npm (if running locally)
cd nest-backend

# Development mode (watch mode)
npm run start:dev

# Debug mode
npm run start:debug

# Production mode
npm run start:prod
```

### Building

```bash
# Build for production
npm run build

# Check build output
ls -la dist/

# Production build in Docker
docker-compose build orionone-backend
```

### Generate Resources

```bash
# Generate module
npx nest generate module tickets
npx nest g mo tickets # Short form

# Generate controller
npx nest generate controller tickets
npx nest g co tickets --no-spec # Without test file

# Generate service
npx nest generate service tickets
npx nest g s tickets

# Generate complete resource (REST API)
npx nest generate resource tickets
# Prompts: REST API, CRUD entry points, Yes

# Generate resource with all files
npx nest g resource users --no-spec

# Generate guard
npx nest g guard auth/jwt
npx nest g guard auth/roles

# Generate interceptor
npx nest g interceptor common/transform

# Generate pipe
npx nest g pipe common/validation

# Generate filter
npx nest g filter common/http-exception

# Generate middleware
npx nest g middleware common/logger

# Generate decorator
npx nest g decorator common/user
```

### Code Quality

```bash
# Linting
npm run lint
npm run lint -- --fix # Auto-fix issues

# Formatting
npm run format # Format with Prettier
npm run format -- --check # Check without writing

# Type checking
npx tsc --noEmit
```

### Module Structure

```bash
# Typical module generation workflow
npx nest g module tickets
npx nest g controller tickets --no-spec
npx nest g service tickets --no-spec
npx nest g class tickets/dto/create-ticket.dto --no-spec
npx nest g class tickets/dto/update-ticket.dto --no-spec
npx nest g class tickets/entities/ticket.entity --no-spec
```

---

## Next.js Frontend Commands

### Development

```bash
# Via Docker (recommended)
docker-compose up -d orionone-frontend
docker-compose logs -f orionone-frontend

# Via npm (if running locally)
cd next-frontend

# Development mode (with hot reload)
npm run dev

# Development on specific port
npm run dev -- -p 3001

# Development with turbo (faster)
npm run dev -- --turbo
```

### Building & Production

```bash
# Build for production
npm run build

# Check build output
ls -la .next/

# Start production server
npm start

# Production on specific port
npm start -- -p 3000

# Analyze bundle size
npm run build -- --analyze # If @next/bundle-analyzer is configured
```

### Code Quality

```bash
# Linting
npm run lint
npm run lint -- --fix # Auto-fix issues
npm run lint -- --max-warnings 0 # Fail on warnings

# Type checking
npx tsc --noEmit
```

### Component Generation (Manual)

```bash
# Create component structure
mkdir -p app/components/tickets
touch app/components/tickets/TicketList.tsx
touch app/components/tickets/TicketCard.tsx
touch app/components/tickets/TicketForm.tsx

# Create page
mkdir -p app/tickets
touch app/tickets/page.tsx
touch app/tickets/layout.tsx
touch app/tickets/loading.tsx
touch app/tickets/error.tsx

# Create API route
mkdir -p app/api/tickets
touch app/api/tickets/route.ts

# Create dynamic route
mkdir -p app/tickets/[id]
touch app/tickets/[id]/page.tsx
```

### Next.js Specific Commands

```bash
# Clear Next.js cache
rm -rf .next

# Info about Next.js installation
npx next info

# Telemetry status
npx next telemetry status
npx next telemetry disable
npx next telemetry enable
```

---

## Prisma ORM Commands

### Schema Management

```bash
# Generate Prisma Client
npx prisma generate
docker-compose exec orionone-backend npx prisma generate

# Format schema file
npx prisma format

# Validate schema
npx prisma validate

# Pull schema from database
npx prisma db pull

# Push schema to database (dev only)
npx prisma db push
```

### Migrations

```bash
# Create migration
npx prisma migrate dev --name init
npx prisma migrate dev --name add_tickets_table
npx prisma migrate dev --name add_avatar_to_users

# Apply migrations (production)
npx prisma migrate deploy
docker-compose exec orionone-backend npx prisma migrate deploy

# Reset database ( deletes all data)
npx prisma migrate reset
npx prisma migrate reset --skip-seed # Without seeding

# View migration status
npx prisma migrate status

# Create migration from schema changes
npx prisma migrate dev

# Resolve migration issues
npx prisma migrate resolve --applied 20251113_init
npx prisma migrate resolve --rolled-back 20251113_init
```

### Seeding

```bash
# Run seed
npm run prisma:seed
npx ts-node prisma/seed.ts
docker-compose exec orionone-backend npx ts-node prisma/seed.ts

# Custom seed scripts
npx ts-node prisma/seed-users.ts
npx ts-node prisma/seed-tickets.ts
```

### Prisma Studio (Database GUI)

```bash
# Open Prisma Studio
npx prisma studio
npm run prisma:studio

# Via Docker
docker-compose exec orionone-backend npx prisma studio
# Access at: http://localhost:5555

# On specific port
npx prisma studio --port 5556
```

### Database Operations

```bash
# Execute raw SQL
npx prisma db execute --file ./script.sql

# Seed database
npx prisma db seed

# Database statistics
npx prisma db stat
```

---

## npm Commands

### Installation

```bash
# Install all dependencies
npm install
npm ci # Clean install (use in CI/CD)

# Install specific package
npm install axios
npm install @tanstack/react-query
npm install zod

# Install dev dependency
npm install --save-dev @types/node
npm install -D typescript eslint prettier

# Install specific version
npm install next@15.5.6
npm install react@19.2.0

# Install from GitHub
npm install user/repo#branch
```

### Updates

```bash
# Check for updates
npm outdated

# Update all packages
npm update

# Update specific package
npm update axios
npm update next

# Update to latest (ignoring semver)
npm install axios@latest
npm install next@latest

# Interactive update
npx npm-check-updates
npx npm-check-updates -u # Update package.json
npm install # Install updates
```

### Scripts

```bash
# List available scripts
npm run

# Run custom script
npm run custom-script

# Run with arguments
npm run dev -- --port 3001
npm run build -- --profile
```

### Package Management

```bash
# Remove package
npm uninstall axios
npm remove @tanstack/react-query

# List installed packages
npm list
npm list --depth=0 # Top-level only
npm list axios # Specific package

# Show package info
npm view axios
npm view next versions # All versions
npm view @nestjs/common
```

### Security

```bash
# Audit dependencies
npm audit
npm audit --production # Production only

# Fix vulnerabilities
npm audit fix
npm audit fix --force # Force major updates

# Check for specific vulnerability
npm audit --json | grep CVE-2025
```

### Cache

```bash
# Clear npm cache
npm cache clean --force
npm cache verify

# Show cache location
npm config get cache
```

### Publishing (if needed)

```bash
# Login to npm registry
npm login

# Publish package
npm publish

# Update version
npm version patch # 1.0.0 → 1.0.1
npm version minor # 1.0.0 → 1.1.0
npm version major # 1.0.0 → 2.0.0
```

---

## Database Commands (PostgreSQL)

### Connection

```bash
# Connect to database via Docker
docker-compose exec orionone-db psql -U postgres -d orionone

# Connect as specific user
docker-compose exec orionone-db psql -U postgres

# Connect and execute command
docker-compose exec orionone-db psql -U postgres -d orionone -c "SELECT version();"
```

### Database Operations

```bash
# List databases
docker-compose exec orionone-db psql -U postgres -c "\l"

# List tables
docker-compose exec orionone-db psql -U postgres -d orionone -c "\dt"

# Describe table
docker-compose exec orionone-db psql -U postgres -d orionone -c "\d users"
docker-compose exec orionone-db psql -U postgres -d orionone -c "\d+ tickets"

# List indexes
docker-compose exec orionone-db psql -U postgres -d orionone -c "\di"

# Show table size
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT
 tablename,
 pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### Queries

```bash
# Execute query
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT * FROM users LIMIT 5;
"

# Count records
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT COUNT(*) FROM tickets;
"

# Query with formatting
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT id, email, role FROM users;
" --html > users.html

# Export to CSV
docker-compose exec orionone-db psql -U postgres -d orionone -c "
COPY (SELECT * FROM tickets) TO STDOUT WITH CSV HEADER;
" > tickets.csv
```

### Backup & Restore

```bash
# Backup database
docker-compose exec orionone-db pg_dump -U postgres orionone > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with compression
docker-compose exec orionone-db pg_dump -U postgres orionone | gzip > backup.sql.gz

# Backup specific tables
docker-compose exec orionone-db pg_dump -U postgres -t users -t tickets orionone > backup_tables.sql

# Restore database
docker-compose exec -T orionone-db psql -U postgres orionone < backup.sql

# Restore with drop
docker-compose exec orionone-db psql -U postgres -c "DROP DATABASE orionone;"
docker-compose exec orionone-db psql -U postgres -c "CREATE DATABASE orionone;"
docker-compose exec -T orionone-db psql -U postgres orionone < backup.sql
```

### Maintenance

```bash
# Vacuum database
docker-compose exec orionone-db psql -U postgres -d orionone -c "VACUUM ANALYZE;"

# Reindex database
docker-compose exec orionone-db psql -U postgres -d orionone -c "REINDEX DATABASE orionone;"

# Show database statistics
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
ORDER BY n_tup_ins DESC;
"

# Show index usage
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT
 schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
"
```

### User Management

```bash
# Create user
docker-compose exec orionone-db psql -U postgres -c "
CREATE USER app_user WITH PASSWORD 'secure_password';
"

# Grant privileges
docker-compose exec orionone-db psql -U postgres -c "
GRANT ALL PRIVILEGES ON DATABASE orionone TO app_user;
"

# List users
docker-compose exec orionone-db psql -U postgres -c "\du"
```

---

## Testing Commands

### Backend (Nest.js + Jest)

```bash
# Run all tests
npm test
docker-compose exec orionone-backend npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:cov
npm run test:cov -- --coverage-reporters=html # HTML report

# Specific test file
npm test -- auth.service.spec.ts
npm test -- tickets.controller.spec.ts

# Specific test suite
npm test -- --testNamePattern="TicketService"
npm test -- -t "should create ticket"

# E2E tests
npm run test:e2e
npm run test:e2e -- --verbose

# Debug tests
npm run test:debug

# Clear Jest cache
npx jest --clearCache
```

### Frontend (Next.js + Jest)

```bash
# Run tests (if configured)
npm test
docker-compose exec orionone-frontend npm test

# Run with coverage
npm run test:coverage

# Update snapshots
npm test -- -u
npm test -- --updateSnapshot
```

### Test Coverage Reports

```bash
# Backend coverage
npm run test:cov
open coverage/lcov-report/index.html # Mac/Linux
start coverage/lcov-report/index.html # Windows

# Check coverage thresholds
npm run test:cov -- --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

---

## Deployment Commands

### Production Build

```bash
# Backend
cd nest-backend
npm run build
npm run start:prod

# Frontend
cd next-frontend
npm run build
npm start
```

### Docker Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production stack
docker-compose -f docker-compose.prod.yml up -d

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL="postgresql://user:pass@localhost:5432/orionone"
JWT_SECRET="your-secret-key"
NODE_ENV="production"

# Frontend (.env.local)
NEXT_PUBLIC_API_URL="https://api.orionone.com"
```

### Health Checks

```bash
# Backend health
curl http://localhost:3001/api/health

# Frontend health
curl http://localhost:3000

# Database health
docker-compose exec orionone-db pg_isready -U postgres

# Redis health
docker-compose exec orionone-redis redis-cli PING

# Meilisearch health
curl http://localhost:7700/health
```

### Database Migrations (Production)

```bash
# Apply migrations
docker-compose exec orionone-backend npx prisma migrate deploy

# Verify migration status
docker-compose exec orionone-backend npx prisma migrate status

# Rollback (manual)
# 1. Restore database backup
# 2. Remove failed migration from _prisma_migrations table
```

---

## Troubleshooting

### Backend Issues

```bash
# Container won't start
docker-compose logs orionone-backend
docker-compose restart orionone-backend
docker-compose up -d --force-recreate orionone-backend

# Database connection issues
docker-compose exec orionone-backend npx prisma db pull
docker-compose exec orionone-db psql -U postgres -d orionone -c "SELECT 1;"

# Port already in use
# Windows:
netstat -ano | findstr :3001
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :3001
kill -9 <PID>

# Clear Prisma cache
rm -rf node_modules/.prisma
npx prisma generate

# Rebuild node_modules
rm -rf node_modules package-lock.json
npm install
```

### Frontend Issues

```bash
# Next.js cache issues
rm -rf .next
npm run dev

# Module not found errors
rm -rf node_modules package-lock.json
npm install

# Port already in use
# Check process on port 3000
netstat -ano | findstr :3000 # Windows
lsof -i :3000 # Linux/Mac

# Type errors
npx tsc --noEmit
npm run lint
```

### Docker Issues

```bash
# Containers won't start
docker-compose down
docker-compose up -d --force-recreate

# Network issues
docker network prune
docker-compose down
docker-compose up -d

# Volume issues
docker volume ls
docker volume prune
docker-compose down -v # Deletes data

# Image issues
docker image prune -a
docker-compose build --no-cache

# Disk space issues
docker system df
docker system prune -a --volumes
```

### Database Issues

```bash
# Connection refused
docker-compose ps orionone-db
docker-compose logs orionone-db
docker-compose restart orionone-db

# Migration issues
docker-compose exec orionone-backend npx prisma migrate status
docker-compose exec orionone-backend npx prisma migrate resolve --applied <migration_name>

# Seed issues
docker-compose exec orionone-backend npx ts-node prisma/seed.ts

# Lock issues
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT * FROM pg_locks WHERE NOT granted;
"

# Kill long-running queries
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active' AND query_start < NOW() - INTERVAL '5 minutes';
"
```

### Performance Issues

```bash
# Check container resources
docker stats

# Check database connections
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT count(*) FROM pg_stat_activity;
"

# Check slow queries
docker-compose exec orionone-db psql -U postgres -d orionone -c "
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
"

# Analyze query performance
docker-compose exec orionone-db psql -U postgres -d orionone -c "
EXPLAIN ANALYZE SELECT * FROM tickets WHERE status = 'OPEN';
"
```

### Node.js Issues

```bash
# Memory leaks
NODE_OPTIONS="--max-old-space-size=4096" npm run start:dev

# Module resolution issues
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# TypeScript issues
npx tsc --noEmit --skipLibCheck
```

---

## Quick Reference

### Daily Development Workflow

```bash
# 1. Start development environment
docker-compose up -d

# 2. Watch logs
docker-compose logs -f orionone-backend orionone-frontend

# 3. Make changes...

# 4. Check status
git status
npm test

# 5. Commit
git add .
git commit -m "feat: add feature"
git push origin feature/branch

# 6. Stop environment
docker-compose down
```

### Production Deployment Checklist

```bash
# 1. Run tests
npm run test:cov # Backend
npm test # Frontend

# 2. Build
npm run build # Both projects

# 3. Database migrations
npx prisma migrate deploy

# 4. Environment variables
cp .env.example .env
# Edit .env with production values

# 5. Docker build
docker-compose -f docker-compose.prod.yml build

# 6. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 7. Health checks
curl http://localhost:3001/api/health
curl http://localhost:3000

# 8. Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

**Last Updated:** 13 November 2025
**Maintained by:** OrionOne Development Team
**Stack Version:** Next.js 15.5.6 + Nest.js 11.1.8 + PostgreSQL 18.0
