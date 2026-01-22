# Frontend Vue.js + Capacitor - Dockerfile de Desarrollo
FROM node:20-slim

# Variables de entorno
ENV NODE_ENV=development \
    PNPM_HOME="/pnpm" \
    PATH="$PNPM_HOME:$PATH"

# Habilitar corepack para pnpm
RUN corepack enable

# Instalar dependencias del sistema necesarias para Capacitor
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    openjdk-17-jdk-headless \
    android-sdk \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno para Android SDK
ENV ANDROID_HOME=/usr/lib/android-sdk \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

WORKDIR /app

# Copiar archivos de dependencias primero
COPY package.json pnpm-lock.yaml* ./

# Instalar dependencias
RUN pnpm install --frozen-lockfile || pnpm install

# El código se monta como volumen en desarrollo
# COPY . . (solo para producción)

# Puerto del servidor de desarrollo
EXPOSE 5173

# Comando por defecto (desarrollo con hot-reload)
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
