#!/bin/bash
# Feature Scaffolding Script
# Usage: ./scripts/feature.sh FeatureName

FEATURE=$1

if [ -z "$FEATURE" ]; then
    echo "❌ Usage: ./scripts/feature.sh FeatureName"
    echo "   Example: ./scripts/feature.sh Ticket"
    exit 1
fi

# Lowercase para nomes de ficheiros
feature_lower=$(echo $FEATURE | tr '[:upper:]' '[:lower:]')
feature_plural="${feature_lower}s"

echo "🚀 Creating feature scaffold for: $FEATURE"
echo ""

# Migration
echo "📝 Creating migration..."
docker-compose exec orionone-app php artisan make:migration create_${feature_plural}_table

# Model + Factory + Seeder
echo "📝 Creating Model, Factory, and Seeder..."
docker-compose exec orionone-app php artisan make:model $FEATURE -fs

# Controller
echo "📝 Creating Controller..."
docker-compose exec orionone-app php artisan make:controller ${FEATURE}Controller --resource

# Form Requests
echo "📝 Creating Form Requests..."
docker-compose exec orionone-app php artisan make:request Store${FEATURE}Request
docker-compose exec orionone-app php artisan make:request Update${FEATURE}Request

# Tests
echo "📝 Creating Tests..."
docker-compose exec orionone-app php artisan make:test ${FEATURE}Test
docker-compose exec orionone-app php artisan make:test ${FEATURE}ServiceTest --unit

# Policy
echo "📝 Creating Policy..."
docker-compose exec orionone-app php artisan make:policy ${FEATURE}Policy --model=$FEATURE

# Observer (opcional)
echo "📝 Creating Observer..."
docker-compose exec orionone-app php artisan make:observer ${FEATURE}Observer --model=$FEATURE

echo ""
echo "✅ Feature scaffold criado: $FEATURE"
echo ""
echo "📋 Próximos passos:"
echo "   1. ✏️  Escrever migration em database/migrations/*_create_${feature_plural}_table.php"
echo "   2. 🧪 Escrever testes em tests/Feature/${FEATURE}Test.php"
echo "   3. 🏗️  Implementar lógica até testes passarem (TDD: RED → GREEN → REFACTOR)"
echo "   4. 🎨 Criar componentes Vue em resources/js/Components/${FEATURE}/"
echo "   5. 📄 Criar páginas Inertia em resources/js/Pages/${FEATURE}/"
echo "   6. ✅ Rodar: docker-compose exec orionone-app php artisan test"
echo "   7. 🧹 Rodar: docker-compose exec orionone-app ./vendor/bin/pint"
echo "   8. 🔍 Rodar: docker-compose exec orionone-app ./vendor/bin/phpstan analyse"
echo "   9. 💾 Commit: git commit -m \"feat(${feature_lower}): implementar $FEATURE\""
echo ""
