# ================================================
# Makefile - Comandos de desarrollo
# ================================================

.PHONY: help start stop restart build logs shell-backend shell-frontend test lint clean

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.prod.yml

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ----------------
# Desarrollo
# ----------------

start: ## Iniciar ambiente de desarrollo
	@echo "🚀 Iniciando ambiente de desarrollo..."
	@if [ ! -f .env ]; then cp .env.example .env; fi
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Ambiente iniciado"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:8000/docs"

stop: ## Detener todos los contenedores
	@echo "🛑 Deteniendo contenedores..."
	$(DOCKER_COMPOSE) down

restart: ## Reiniciar todos los servicios
	@echo "🔄 Reiniciando servicios..."
	$(DOCKER_COMPOSE) restart

build: ## Reconstruir imágenes
	@echo "🔨 Construyendo imágenes..."
	$(DOCKER_COMPOSE) build --no-cache

logs: ## Ver logs de todos los servicios
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Ver logs del backend
	$(DOCKER_COMPOSE) logs -f backend

logs-frontend: ## Ver logs del frontend
	$(DOCKER_COMPOSE) logs -f frontend

shell-backend: ## Abrir shell en el backend
	$(DOCKER_COMPOSE) exec backend bash

shell-frontend: ## Abrir shell en el frontend
	$(DOCKER_COMPOSE) exec frontend sh

shell-db: ## Abrir shell de PostgreSQL
	$(DOCKER_COMPOSE) exec db psql -U postgres -d zpinnaldb

# ----------------
# Testing
# ----------------

test: ## Ejecutar todos los tests
	@echo "🧪 Ejecutando tests..."
	$(DOCKER_COMPOSE) exec backend pytest -v
	$(DOCKER_COMPOSE) exec frontend pnpm test:unit

test-backend: ## Ejecutar tests del backend
	$(DOCKER_COMPOSE) exec backend pytest -v

test-backend-cov: ## Tests del backend con coverage
	$(DOCKER_COMPOSE) exec backend pytest --cov=app --cov-report=html

test-frontend: ## Ejecutar tests del frontend
	$(DOCKER_COMPOSE) exec frontend pnpm test:unit

test-frontend-cov: ## Tests del frontend con coverage
	$(DOCKER_COMPOSE) exec frontend pnpm test:coverage

# ----------------
# Linting y formato
# ----------------

lint: ## Ejecutar linters
	@echo "🔍 Ejecutando linters..."
	$(DOCKER_COMPOSE) exec backend ruff check app/
	$(DOCKER_COMPOSE) exec frontend pnpm lint

format: ## Formatear código
	@echo "✨ Formateando código..."
	$(DOCKER_COMPOSE) exec backend black app/
	$(DOCKER_COMPOSE) exec backend isort app/
	$(DOCKER_COMPOSE) exec frontend pnpm format

# ----------------
# Base de datos
# ----------------

db-migrate: ## Crear migración de Alembic
	$(DOCKER_COMPOSE) exec backend alembic revision --autogenerate -m "$(msg)"

db-upgrade: ## Aplicar migraciones
	$(DOCKER_COMPOSE) exec backend alembic upgrade head

db-downgrade: ## Revertir última migración
	$(DOCKER_COMPOSE) exec backend alembic downgrade -1

db-reset: ## Resetear base de datos
	@echo "⚠️  Reseteando base de datos..."
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d db
	@sleep 3
	$(DOCKER_COMPOSE) up -d

# ----------------
# Capacitor (Mobile)
# ----------------

cap-sync: ## Sincronizar Capacitor
	$(DOCKER_COMPOSE) exec frontend pnpm cap:sync

cap-android: ## Abrir proyecto Android
	cd frontend && pnpm cap:open:android

cap-ios: ## Abrir proyecto iOS
	cd frontend && pnpm cap:open:ios

# ----------------
# Producción
# ----------------

prod-build: ## Construir para producción
	$(DOCKER_COMPOSE_PROD) build

prod-start: ## Iniciar en modo producción
	$(DOCKER_COMPOSE_PROD) up -d

prod-stop: ## Detener producción
	$(DOCKER_COMPOSE_PROD) down

# ----------------
# Limpieza
# ----------------

clean: ## Limpiar contenedores, volúmenes y caché
	@echo "🧹 Limpiando..."
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f

clean-all: ## Limpieza completa (incluyendo imágenes)
	@echo "🧹 Limpieza completa..."
	$(DOCKER_COMPOSE) down -v --remove-orphans --rmi all
	docker system prune -af
