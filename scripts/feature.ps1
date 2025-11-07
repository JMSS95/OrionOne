# Feature Scaffolding Script (PowerShell)
# Usage: .\scripts\feature.ps1 FeatureName

param(
    [Parameter(Mandatory=$true)]
    [string]$Feature
)

$featureLower = $Feature.ToLower()
$featurePlural = "${featureLower}s"

Write-Host "🚀 Creating feature scaffold for: $Feature" -ForegroundColor Green
Write-Host ""

# Migration
Write-Host "📝 Creating migration..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:migration create_${featurePlural}_table

# Model + Factory + Seeder
Write-Host "📝 Creating Model, Factory, and Seeder..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:model $Feature -fs

# Controller
Write-Host "📝 Creating Controller..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:controller ${Feature}Controller --resource

# Form Requests
Write-Host "📝 Creating Form Requests..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:request Store${Feature}Request
docker-compose exec orionone-app php artisan make:request Update${Feature}Request

# Tests
Write-Host "📝 Creating Tests..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:test ${Feature}Test
docker-compose exec orionone-app php artisan make:test ${Feature}ServiceTest --unit

# Policy
Write-Host "📝 Creating Policy..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:policy ${Feature}Policy --model=$Feature

# Observer
Write-Host "📝 Creating Observer..." -ForegroundColor Yellow
docker-compose exec orionone-app php artisan make:observer ${Feature}Observer --model=$Feature

Write-Host ""
Write-Host "✅ Feature scaffold criado: $Feature" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. ✏️  Escrever migration em database/migrations/*_create_${featurePlural}_table.php"
Write-Host "   2. 🧪 Escrever testes em tests/Feature/${Feature}Test.php"
Write-Host "   3. 🏗️  Implementar lógica até testes passarem (TDD: RED → GREEN → REFACTOR)"
Write-Host "   4. 🎨 Criar componentes Vue em resources/js/Components/${Feature}/"
Write-Host "   5. 📄 Criar páginas Inertia em resources/js/Pages/${Feature}/"
Write-Host "   6. ✅ Rodar: docker-compose exec orionone-app php artisan test"
Write-Host "   7. 🧹 Rodar: docker-compose exec orionone-app ./vendor/bin/pint"
Write-Host "   8. 🔍 Rodar: docker-compose exec orionone-app ./vendor/bin/phpstan analyse"
Write-Host "   9. 💾 Commit: git commit -m `"feat(${featureLower}): implementar $Feature`""
Write-Host ""
