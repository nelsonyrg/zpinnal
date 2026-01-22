# ================================================
# Script para iniciar el ambiente de desarrollo (Windows)
# ================================================

$ErrorActionPreference = "Stop"

Write-Host "🚀 Iniciando ambiente de desarrollo..." -ForegroundColor Cyan

# Verificar que Docker está corriendo
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Error: Docker no está corriendo. Por favor inicia Docker Desktop." -ForegroundColor Red
    exit 1
}

# Copiar .env si no existe
if (-not (Test-Path ".env")) {
    Write-Host "📄 Creando archivo .env desde .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

# Construir imágenes si es necesario
Write-Host "🔨 Construyendo imágenes..." -ForegroundColor Yellow
docker-compose build

# Iniciar servicios
Write-Host "🐳 Iniciando contenedores..." -ForegroundColor Yellow
docker-compose up -d

# Esperar a que los servicios estén listos
Write-Host "⏳ Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar estado
Write-Host ""
Write-Host "✅ Ambiente de desarrollo iniciado!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   - Frontend:  http://localhost:5173"
Write-Host "   - Backend:   http://localhost:8000"
Write-Host "   - API Docs:  http://localhost:8000/docs"
Write-Host "   - pgAdmin:   http://localhost:5050 (perfil: tools)"
Write-Host ""
Write-Host "📋 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   - Ver logs:           docker-compose logs -f"
Write-Host "   - Detener:            docker-compose down"
Write-Host "   - Reiniciar backend:  docker-compose restart backend"
Write-Host "   - Shell backend:      docker-compose exec backend bash"
Write-Host "   - Shell frontend:     docker-compose exec frontend sh"
