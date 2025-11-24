#!/bin/bash
set -e

echo "🚀 OrionOne ITSM - Post Create Setup"
echo "===================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para mensagens
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 1. Verificar se .env existe
log_info "Verificando configuração de ambiente..."
if [ ! -f "/app/.env" ]; then
    log_warning ".env não encontrado, copiando de .env.example..."
    cp /app/.env.example /app/.env
    log_success "Ficheiro .env criado"
else
    log_success "Ficheiro .env já existe"
fi

# 2. Aguardar que PostgreSQL esteja pronto
log_info "Aguardando PostgreSQL estar pronto..."
timeout=60
counter=0
until pg_isready -h postgres -U orionone &> /dev/null || [ $counter -eq $timeout ]; do
    printf "."
    sleep 1
    ((counter++))
done
echo ""

if [ $counter -eq $timeout ]; then
    log_warning "PostgreSQL pode não estar pronto, continuando mesmo assim..."
else
    log_success "PostgreSQL pronto!"
fi

# 3. Aguardar que Redis esteja pronto
log_info "Aguardando Redis estar pronto..."
counter=0
until redis-cli -h redis ping &> /dev/null || [ $counter -eq $timeout ]; do
    printf "."
    sleep 1
    ((counter++))
done
echo ""

if [ $counter -eq $timeout ]; then
    log_warning "Redis pode não estar pronto, continuando mesmo assim..."
else
    log_success "Redis pronto!"
fi

# 4. Instalar dependências do Backend
log_info "Instalando dependências do Backend (NestJS)..."
cd /app
if [ -f "package.json" ]; then
    npm install
    log_success "Dependências do Backend instaladas"
else
    log_warning "package.json do Backend não encontrado"
fi

# 5. Executar migrações Prisma
log_info "Executando migrações do Prisma..."
if [ -f "prisma/schema.prisma" ]; then
    npx prisma generate
    npx prisma migrate deploy
    log_success "Migrações aplicadas"

    # Seed da base de dados
    if [ -f "prisma/seed.ts" ]; then
        log_info "Executando seed da base de dados..."
        npx prisma db seed
        log_success "Seed executado"
    fi
else
    log_warning "Schema Prisma não encontrado"
fi

# 6. Verificar conexão entre serviços
log_info "Verificando conectividade com serviços..."
if curl -s http://frontend:3000 &> /dev/null; then
    log_success "Frontend container acessível"
else
    log_warning "Frontend pode estar a iniciar ainda..."
fi

# 7. Verificar Meilisearch
log_info "Verificando Meilisearch..."
if curl -s http://meilisearch:7700/health &> /dev/null; then
    log_success "Meilisearch está operacional"
else
    log_warning "Meilisearch pode não estar acessível"
fi

# 8. Criar diretório de uploads
log_info "Criando diretórios necessários..."
mkdir -p /app/uploads
mkdir -p /app/logs
log_success "Diretórios criados"

# 9. Configurar Git
log_info "Configurando Git..."
git config --global --add safe.directory /app
log_success "Git configurado"

echo ""
echo "===================================="
log_success "Setup completo!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Verifique o ficheiro .env (em /app/.env) se necessário"
echo "   2. Execute 'npm run dev' para iniciar o backend em modo dev"
echo "   3. Os containers frontend/nginx iniciam automaticamente via docker-compose"
echo "   4. Aceda às portas forwarded no painel PORTS do VS Code"
echo ""
echo "🔗 Serviços disponíveis:"
echo "   - Nginx Proxy: porta 80 (recomendado)"
echo "   - Frontend:    porta 3000"
echo "   - Backend API: porta 3001"
echo "   - Mailpit:     porta 8025"
echo "   - Meilisearch: porta 7700"
echo ""
echo "📚 Documentação: .devcontainer/CODESPACE-SETUP-GUIDE.md"
echo "===================================="
