# Mobile App - Vue.js/Capacitor + FastAPI

Ambiente de desarrollo completo dockerizado para aplicación móvil.

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Frontend | Vue.js 3 + TypeScript + Vite |
| Mobile | Capacitor 6 (iOS/Android) |
| Backend | FastAPI + Python 3.11 |
| Base de datos | PostgreSQL 16 |
| Cache | Redis 7 |
| Contenedores | Docker + Docker Compose |

## Requisitos Previos

- **Docker Desktop** (Windows/Mac) o Docker Engine (Linux)
- **Git**
- **Node.js 20+** (solo para desarrollo móvil nativo)
- **Android Studio** (para builds Android)
- **Xcode** (para builds iOS, solo macOS)

## Inicio Rápido

### 1. Clonar y configurar

```bash
# Clonar repositorio
git clone <repo-url>
cd zpinnal

# Copiar configuración de entorno
cp .env.example .env
```

### 2. Iniciar ambiente de desarrollo

**Windows (PowerShell):**
```powershell
.\scripts\dev-start.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh
```

**O usando Docker Compose directamente:**
```bash
docker-compose up -d
```

### 3. Acceder a los servicios

| Servicio | URL |
|----------|-----|
| Frontend (Vue.js) | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

### 4. Herramientas opcionales

```bash
# Iniciar pgAdmin y MailHog
docker-compose --profile tools up -d

# pgAdmin: http://localhost:5050
# MailHog: http://localhost:8025
```

## Estructura del Proyecto

```
zpinnal/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── core/           # Configuración central
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   └── main.py         # Punto de entrada
│   ├── tests/              # Tests del backend
│   ├── requirements.txt    # Dependencias producción
│   └── requirements-dev.txt # Dependencias desarrollo
│
├── frontend/               # Frontend Vue.js + Capacitor
│   ├── src/
│   │   ├── assets/        # Estilos y recursos
│   │   ├── components/    # Componentes Vue
│   │   ├── views/         # Vistas/páginas
│   │   ├── router/        # Configuración de rutas
│   │   ├── stores/        # Estado (Pinia)
│   │   ├── services/      # Servicios API
│   │   └── main.ts        # Punto de entrada
│   ├── android/           # Proyecto Android (generado)
│   ├── ios/               # Proyecto iOS (generado)
│   └── capacitor.config.ts
│
├── .docker/               # Dockerfiles
│   ├── backend/
│   └── frontend/
│
├── scripts/               # Scripts de utilidad
├── docker-compose.yml     # Desarrollo
├── docker-compose.prod.yml # Producción
└── Makefile              # Comandos de desarrollo
```

## Comandos de Desarrollo

### Windows (PowerShell) - Recomendado

El proyecto incluye un script PowerShell con todos los comandos necesarios:

```powershell
# Ver ayuda con todos los comandos disponibles
.\scripts\dev.ps1 help
```

#### Comandos disponibles:

| Categoría | Comando | Descripción |
|-----------|---------|-------------|
| **Desarrollo** | `.\scripts\dev.ps1 start` | Iniciar ambiente de desarrollo |
| | `.\scripts\dev.ps1 stop` | Detener todos los contenedores |
| | `.\scripts\dev.ps1 restart` | Reiniciar todos los servicios |
| | `.\scripts\dev.ps1 build` | Reconstruir imágenes |
| | `.\scripts\dev.ps1 logs` | Ver logs de todos los servicios |
| | `.\scripts\dev.ps1 logs-backend` | Ver logs del backend |
| | `.\scripts\dev.ps1 logs-frontend` | Ver logs del frontend |
| | `.\scripts\dev.ps1 shell-backend` | Abrir shell en el backend |
| | `.\scripts\dev.ps1 shell-frontend` | Abrir shell en el frontend |
| | `.\scripts\dev.ps1 shell-db` | Abrir shell de PostgreSQL |
| **Testing** | `.\scripts\dev.ps1 test` | Ejecutar todos los tests |
| | `.\scripts\dev.ps1 test-backend` | Tests del backend |
| | `.\scripts\dev.ps1 test-backend-cov` | Tests backend con coverage |
| | `.\scripts\dev.ps1 test-frontend` | Tests del frontend |
| | `.\scripts\dev.ps1 test-frontend-cov` | Tests frontend con coverage |
| **Linting** | `.\scripts\dev.ps1 lint` | Ejecutar linters |
| | `.\scripts\dev.ps1 format` | Formatear código |
| **Base de datos** | `.\scripts\dev.ps1 db-migrate "mensaje"` | Crear migración Alembic |
| | `.\scripts\dev.ps1 db-upgrade` | Aplicar migraciones |
| | `.\scripts\dev.ps1 db-downgrade` | Revertir última migración |
| | `.\scripts\dev.ps1 db-reset` | Resetear base de datos |
| **Capacitor** | `.\scripts\dev.ps1 cap-sync` | Sincronizar Capacitor |
| | `.\scripts\dev.ps1 cap-android` | Abrir proyecto Android |
| | `.\scripts\dev.ps1 cap-ios` | Abrir proyecto iOS |
| **Producción** | `.\scripts\dev.ps1 prod-build` | Construir para producción |
| | `.\scripts\dev.ps1 prod-start` | Iniciar en modo producción |
| | `.\scripts\dev.ps1 prod-stop` | Detener producción |
| **Limpieza** | `.\scripts\dev.ps1 clean` | Limpiar contenedores y volúmenes |
| | `.\scripts\dev.ps1 clean-all` | Limpieza completa (incluye imágenes) |

### Linux/Mac (Make)

```bash
make help           # Ver todos los comandos disponibles
make start          # Iniciar ambiente
make stop           # Detener ambiente
make logs           # Ver logs
make test           # Ejecutar tests
make lint           # Ejecutar linters
make shell-backend  # Shell en backend
make shell-frontend # Shell en frontend
```

### Usando Docker Compose directamente

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
docker-compose logs -f backend  # Solo backend

# Reiniciar un servicio
docker-compose restart backend

# Ejecutar comando en contenedor
docker-compose exec backend pytest
docker-compose exec frontend pnpm test

# Detener y limpiar
docker-compose down
docker-compose down -v  # Incluye volúmenes
```

## Desarrollo Frontend

### Hot Reload

El código del frontend se sincroniza automáticamente. Los cambios se reflejan instantáneamente en http://localhost:5173.

### Instalar nuevas dependencias

```bash
docker-compose exec frontend pnpm add <paquete>
docker-compose exec frontend pnpm add -D <paquete-dev>
```

### Ejecutar tests

```bash
docker-compose exec frontend pnpm test:unit
docker-compose exec frontend pnpm test:coverage
```

## Desarrollo Backend

### Hot Reload

Uvicorn está configurado con `--reload`. Los cambios en el código Python se aplican automáticamente.

### Instalar nuevas dependencias

```bash
# Agregar a requirements.txt, luego:
docker-compose exec backend pip install -r requirements.txt
# O reconstruir:
docker-compose build backend
```

### Ejecutar tests

```bash
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=app --cov-report=html
```

### Migraciones de base de datos

```bash
# Crear migración
docker-compose exec backend alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
docker-compose exec backend alembic upgrade head
```

## Desarrollo Móvil (Capacitor)

### Configuración inicial

```bash
# Instalar dependencias localmente (fuera de Docker)
cd frontend
npm install

# Inicializar Capacitor (primera vez)
npx cap init "Mobile App" com.example.mobileapp

# Agregar plataformas
npx cap add android
npx cap add ios
```

### Build para móvil

```bash
# Build del frontend
docker-compose exec frontend pnpm build

# Sincronizar con proyectos nativos
npx cap sync

# Abrir en Android Studio
npx cap open android

# Abrir en Xcode (solo macOS)
npx cap open ios
```

### Live Reload en dispositivo

1. Obtener IP de tu máquina
2. Editar `capacitor.config.ts`:
```typescript
server: {
  url: 'http://TU_IP:5173',
  cleartext: true
}
```
3. Ejecutar `npx cap sync` y correr la app

## Testing

### Backend (pytest)

```bash
# Todos los tests
docker-compose exec backend pytest

# Con coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Test específico
docker-compose exec backend pytest tests/test_api.py -v
```

### Frontend (Vitest)

```bash
# Todos los tests
docker-compose exec frontend pnpm test:unit

# Con coverage
docker-compose exec frontend pnpm test:coverage

# Modo watch
docker-compose exec frontend pnpm test
```

## Producción

### Build de imágenes

```bash
docker-compose -f docker-compose.prod.yml build
```

### Despliegue

```bash
# Configurar variables de entorno de producción
export DATABASE_URL=postgresql://...
export SECRET_KEY=$(openssl rand -hex 32)

# Iniciar
docker-compose -f docker-compose.prod.yml up -d
```

## Solución de Problemas

### Los contenedores no inician

```bash
# Ver logs detallados
docker-compose logs

# Reconstruir desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problemas de permisos (Linux)

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar
```

### Puerto en uso

```bash
# Verificar qué usa el puerto
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Cambiar puertos en docker-compose.yml
```

### Base de datos corrupta

```bash
# Resetear volúmenes
docker-compose down -v
docker-compose up -d
```

## Variables de Entorno

Ver `.env.example` para todas las variables disponibles.

| Variable | Descripción | Default |
|----------|-------------|---------|
| DEBUG | Modo debug | true |
| DATABASE_URL | Conexión PostgreSQL | postgresql+asyncpg://... |
| REDIS_URL | Conexión Redis | redis://redis:6379/0 |
| SECRET_KEY | Clave secreta JWT | dev-secret-key... |
| VITE_API_URL | URL de la API | /api/v1 |
