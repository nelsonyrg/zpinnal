# ================================================
# dev.ps1 - Comandos de desarrollo para Windows
# Equivalente al Makefile para PowerShell
# Uso: .\scripts\dev.ps1 <comando>
# ================================================

param(
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(Position=1)]
    [string]$Arg1 = ""
)

$ErrorActionPreference = "Stop"

# Variables
$DOCKER_COMPOSE = "docker-compose"
$DOCKER_COMPOSE_PROD = "docker-compose -f docker-compose.prod.yml"

# ================================================
# Funciones de ayuda
# ================================================

function Show-Help {
    Write-Host ""
    Write-Host "  Zpinnal - Comandos de Desarrollo" -ForegroundColor Cyan
    Write-Host "  =================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Uso: .\scripts\dev.ps1 <comando>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  DESARROLLO" -ForegroundColor Green
    Write-Host "    start             Iniciar ambiente de desarrollo"
    Write-Host "    stop              Detener todos los contenedores"
    Write-Host "    restart           Reiniciar todos los servicios"
    Write-Host "    build             Reconstruir imagenes"
    Write-Host "    logs              Ver logs de todos los servicios"
    Write-Host "    logs-backend      Ver logs del backend"
    Write-Host "    logs-frontend     Ver logs del frontend"
    Write-Host "    shell-backend     Abrir shell en el backend"
    Write-Host "    shell-frontend    Abrir shell en el frontend"
    Write-Host "    shell-db          Abrir shell de PostgreSQL"
    Write-Host ""
    Write-Host "  TESTING" -ForegroundColor Green
    Write-Host "    test              Ejecutar todos los tests"
    Write-Host "    test-backend      Ejecutar tests del backend"
    Write-Host "    test-backend-cov  Tests del backend con coverage"
    Write-Host "    test-frontend     Ejecutar tests del frontend"
    Write-Host "    test-frontend-cov Tests del frontend con coverage"
    Write-Host ""
    Write-Host "  LINTING Y FORMATO" -ForegroundColor Green
    Write-Host "    lint              Ejecutar linters"
    Write-Host "    format            Formatear codigo"
    Write-Host ""
    Write-Host "  BASE DE DATOS" -ForegroundColor Green
    Write-Host "    db-migrate <msg>  Crear migracion de Alembic"
    Write-Host "    db-upgrade        Aplicar migraciones"
    Write-Host "    db-downgrade      Revertir ultima migracion"
    Write-Host "    db-reset          Resetear base de datos"
    Write-Host ""
    Write-Host "  CAPACITOR (MOBILE)" -ForegroundColor Green
    Write-Host "    cap-sync          Sincronizar Capacitor"
    Write-Host "    cap-android       Abrir proyecto Android"
    Write-Host "    cap-ios           Abrir proyecto iOS"
    Write-Host ""
    Write-Host "  PRODUCCION" -ForegroundColor Green
    Write-Host "    prod-build        Construir para produccion"
    Write-Host "    prod-start        Iniciar en modo produccion"
    Write-Host "    prod-stop         Detener produccion"
    Write-Host ""
    Write-Host "  LIMPIEZA" -ForegroundColor Green
    Write-Host "    clean             Limpiar contenedores y volumenes"
    Write-Host "    clean-all         Limpieza completa (incluye imagenes)"
    Write-Host ""
}

# ================================================
# Desarrollo
# ================================================

function Start-Dev {
    Write-Host "🚀 Iniciando ambiente de desarrollo..." -ForegroundColor Cyan

    if (-not (Test-Path ".env")) {
        Write-Host "📄 Creando archivo .env desde .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
    }

    Invoke-Expression "$DOCKER_COMPOSE up -d"

    Write-Host ""
    Write-Host "✅ Ambiente iniciado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 URLs disponibles:" -ForegroundColor Cyan
    Write-Host "   Frontend:  http://localhost:5173"
    Write-Host "   Backend:   http://localhost:8000"
    Write-Host "   API Docs:  http://localhost:8000/docs"
}

function Stop-Dev {
    Write-Host "🛑 Deteniendo contenedores..." -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE down"
    Write-Host "✅ Contenedores detenidos" -ForegroundColor Green
}

function Restart-Dev {
    Write-Host "🔄 Reiniciando servicios..." -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE restart"
    Write-Host "✅ Servicios reiniciados" -ForegroundColor Green
}

function Build-Dev {
    Write-Host "🔨 Construyendo imagenes..." -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE build --no-cache"
    Write-Host "✅ Imagenes construidas" -ForegroundColor Green
}

function Show-Logs {
    Invoke-Expression "$DOCKER_COMPOSE logs -f"
}

function Show-LogsBackend {
    Invoke-Expression "$DOCKER_COMPOSE logs -f backend"
}

function Show-LogsFrontend {
    Invoke-Expression "$DOCKER_COMPOSE logs -f frontend"
}

function Open-ShellBackend {
    Invoke-Expression "$DOCKER_COMPOSE exec backend bash"
}

function Open-ShellFrontend {
    Invoke-Expression "$DOCKER_COMPOSE exec frontend sh"
}

function Open-ShellDb {
    Invoke-Expression "$DOCKER_COMPOSE exec db psql -U postgres -d zpinnaldb"
}

# ================================================
# Testing
# ================================================

function Run-Tests {
    Write-Host "🧪 Ejecutando todos los tests..." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "--- Backend Tests ---" -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec backend pytest -v"
    Write-Host ""
    Write-Host "--- Frontend Tests ---" -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec frontend pnpm test:unit"
    Write-Host ""
    Write-Host "✅ Tests completados" -ForegroundColor Green
}

function Run-TestsBackend {
    Write-Host "🧪 Ejecutando tests del backend..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec backend pytest -v"
}

function Run-TestsBackendCov {
    Write-Host "🧪 Ejecutando tests del backend con coverage..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec backend pytest --cov=app --cov-report=html --cov-report=term"
}

function Run-TestsFrontend {
    Write-Host "🧪 Ejecutando tests del frontend..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec frontend pnpm test:unit"
}

function Run-TestsFrontendCov {
    Write-Host "🧪 Ejecutando tests del frontend con coverage..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec frontend pnpm test:coverage"
}

# ================================================
# Linting y Formato
# ================================================

function Run-Lint {
    Write-Host "🔍 Ejecutando linters..." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "--- Backend Lint ---" -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec backend ruff check app/"
    Write-Host ""
    Write-Host "--- Frontend Lint ---" -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec frontend pnpm lint"
}

function Run-Format {
    Write-Host "✨ Formateando codigo..." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "--- Backend Format ---" -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec backend black app/"
    Invoke-Expression "$DOCKER_COMPOSE exec backend isort app/"
    Write-Host ""
    Write-Host "--- Frontend Format ---" -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec frontend pnpm format"
}

# ================================================
# Base de datos
# ================================================

function New-DbMigration {
    param([string]$Message)

    if ([string]::IsNullOrEmpty($Message)) {
        Write-Host "❌ Error: Debes proporcionar un mensaje para la migracion" -ForegroundColor Red
        Write-Host "   Uso: .\scripts\dev.ps1 db-migrate 'descripcion del cambio'" -ForegroundColor Yellow
        return
    }

    Write-Host "📝 Creando migracion: $Message" -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec backend alembic revision --autogenerate -m '$Message'"
}

function Update-Db {
    Write-Host "⬆️  Aplicando migraciones..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec backend alembic upgrade head"
    Write-Host "✅ Migraciones aplicadas" -ForegroundColor Green
}

function Revert-Db {
    Write-Host "⬇️  Revirtiendo ultima migracion..." -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE exec backend alembic downgrade -1"
    Write-Host "✅ Migracion revertida" -ForegroundColor Green
}

function Reset-Db {
    Write-Host "⚠️  Reseteando base de datos..." -ForegroundColor Red
    Invoke-Expression "$DOCKER_COMPOSE down -v"
    Invoke-Expression "$DOCKER_COMPOSE up -d db"
    Start-Sleep -Seconds 3
    Invoke-Expression "$DOCKER_COMPOSE up -d"
    Write-Host "✅ Base de datos reseteada" -ForegroundColor Green
}

# ================================================
# Capacitor (Mobile)
# ================================================

function Sync-Capacitor {
    Write-Host "📱 Sincronizando Capacitor..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE exec frontend pnpm cap:sync"
}

function Open-Android {
    Write-Host "📱 Abriendo proyecto Android..." -ForegroundColor Cyan
    Push-Location frontend
    pnpm cap:open:android
    Pop-Location
}

function Open-iOS {
    Write-Host "📱 Abriendo proyecto iOS..." -ForegroundColor Cyan
    Push-Location frontend
    pnpm cap:open:ios
    Pop-Location
}

# ================================================
# Produccion
# ================================================

function Build-Prod {
    Write-Host "🏭 Construyendo para produccion..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE_PROD build"
    Write-Host "✅ Build de produccion completado" -ForegroundColor Green
}

function Start-Prod {
    Write-Host "🏭 Iniciando en modo produccion..." -ForegroundColor Cyan
    Invoke-Expression "$DOCKER_COMPOSE_PROD up -d"
    Write-Host "✅ Produccion iniciada" -ForegroundColor Green
}

function Stop-Prod {
    Write-Host "🏭 Deteniendo produccion..." -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE_PROD down"
    Write-Host "✅ Produccion detenida" -ForegroundColor Green
}

# ================================================
# Limpieza
# ================================================

function Clear-Dev {
    Write-Host "🧹 Limpiando contenedores y volumenes..." -ForegroundColor Yellow
    Invoke-Expression "$DOCKER_COMPOSE down -v --remove-orphans"
    docker system prune -f
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

function Clear-All {
    Write-Host "🧹 Limpieza completa (incluye imagenes)..." -ForegroundColor Red
    Invoke-Expression "$DOCKER_COMPOSE down -v --remove-orphans --rmi all"
    docker system prune -af
    Write-Host "✅ Limpieza completa terminada" -ForegroundColor Green
}

# ================================================
# Ejecutar comando
# ================================================

switch ($Command.ToLower()) {
    # Ayuda
    "help"              { Show-Help }
    "-h"                { Show-Help }
    "--help"            { Show-Help }

    # Desarrollo
    "start"             { Start-Dev }
    "stop"              { Stop-Dev }
    "restart"           { Restart-Dev }
    "build"             { Build-Dev }
    "logs"              { Show-Logs }
    "logs-backend"      { Show-LogsBackend }
    "logs-frontend"     { Show-LogsFrontend }
    "shell-backend"     { Open-ShellBackend }
    "shell-frontend"    { Open-ShellFrontend }
    "shell-db"          { Open-ShellDb }

    # Testing
    "test"              { Run-Tests }
    "test-backend"      { Run-TestsBackend }
    "test-backend-cov"  { Run-TestsBackendCov }
    "test-frontend"     { Run-TestsFrontend }
    "test-frontend-cov" { Run-TestsFrontendCov }

    # Linting y formato
    "lint"              { Run-Lint }
    "format"            { Run-Format }

    # Base de datos
    "db-migrate"        { New-DbMigration -Message $Arg1 }
    "db-upgrade"        { Update-Db }
    "db-downgrade"      { Revert-Db }
    "db-reset"          { Reset-Db }

    # Capacitor
    "cap-sync"          { Sync-Capacitor }
    "cap-android"       { Open-Android }
    "cap-ios"           { Open-iOS }

    # Produccion
    "prod-build"        { Build-Prod }
    "prod-start"        { Start-Prod }
    "prod-stop"         { Stop-Prod }

    # Limpieza
    "clean"             { Clear-Dev }
    "clean-all"         { Clear-All }

    default {
        Write-Host "❌ Comando desconocido: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
