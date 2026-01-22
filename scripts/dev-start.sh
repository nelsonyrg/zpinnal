#!/bin/bash
# ================================================
# Script para iniciar el ambiente de desarrollo
# ================================================

set -e

echo "🚀 Iniciando ambiente de desarrollo..."

# Verificar que Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

# Copiar .env si no existe
if [ ! -f .env ]; then
    echo "📄 Creando archivo .env desde .env.example..."
    cp .env.example .env
fi

# Construir imágenes si es necesario
echo "🔨 Construyendo imágenes..."
docker-compose build

# Iniciar servicios
echo "🐳 Iniciando contenedores..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 5

# Verificar estado
echo ""
echo "✅ Ambiente de desarrollo iniciado!"
echo ""
echo "📍 URLs disponibles:"
echo "   - Frontend:  http://localhost:5173"
echo "   - Backend:   http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/docs"
echo "   - pgAdmin:   http://localhost:5050 (perfil: tools)"
echo ""
echo "📋 Comandos útiles:"
echo "   - Ver logs:           docker-compose logs -f"
echo "   - Detener:            docker-compose down"
echo "   - Reiniciar backend:  docker-compose restart backend"
echo "   - Shell backend:      docker-compose exec backend bash"
echo "   - Shell frontend:     docker-compose exec frontend sh"
