# ================================================
# Script para ejecutar tests (Windows)
# ================================================

param(
    [string]$Service = "all",
    [switch]$Coverage
)

$ErrorActionPreference = "Stop"

Write-Host "🧪 Ejecutando tests..." -ForegroundColor Cyan

switch ($Service) {
    "backend" {
        Write-Host "Running backend tests..." -ForegroundColor Yellow
        if ($Coverage) {
            docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term
        } else {
            docker-compose exec backend pytest -v
        }
    }
    "frontend" {
        Write-Host "Running frontend tests..." -ForegroundColor Yellow
        if ($Coverage) {
            docker-compose exec frontend pnpm test:coverage
        } else {
            docker-compose exec frontend pnpm test:unit
        }
    }
    "all" {
        Write-Host "Running all tests..." -ForegroundColor Yellow
        Write-Host "`n--- Backend Tests ---" -ForegroundColor Cyan
        docker-compose exec backend pytest -v
        Write-Host "`n--- Frontend Tests ---" -ForegroundColor Cyan
        docker-compose exec frontend pnpm test:unit
    }
    default {
        Write-Host "Uso: .\run-tests.ps1 [-Service backend|frontend|all] [-Coverage]" -ForegroundColor Yellow
    }
}

Write-Host "`n✅ Tests completados!" -ForegroundColor Green
