#!/bin/bash
set -e

echo "OrionOne ITSM - Post Start"
echo "===================================="

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Verificar status dos serviços
log_info "Verificando status dos serviços..."

# PostgreSQL
if pg_isready -h postgres -U orionone &> /dev/null; then
    log_success "PostgreSQL: Online"
else
    echo "❌ PostgreSQL: Offline"
fi

# Redis
if redis-cli -h redis ping &> /dev/null; then
    log_success "Redis: Online"
else
    echo "❌ Redis: Offline"
fi

# Meilisearch
if curl -s http://meilisearch:7700/health &> /dev/null; then
    log_success "Meilisearch: Online"
else
    echo "⚠️  Meilisearch: Offline"
fi

echo ""
log_info "Codespace pronto para desenvolvimento!"
echo "===================================="
