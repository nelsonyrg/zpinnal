# Configuración del Repositorio Git

Instrucciones para inicializar y subir este proyecto a un repositorio Git remoto.

## Inicialización del repositorio local

```bash
# Navegar al directorio del proyecto
cd C:\WORK\laboratorio\zpinnal

# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit: Vue.js/Capacitor + FastAPI dockerized development environment"

# Renombrar rama a main
git branch -M main
```

## Crear repositorio en GitHub

### Opción A: Desde la web

1. Ir a https://github.com/new
2. Nombre del repositorio: `zpinnal`
3. Dejar vacío (sin README, .gitignore ni licencia)
4. Click en "Create repository"

### Opción B: Usando GitHub CLI

```bash
gh repo create zpinnal --public --source=. --remote=origin --push
```

## Conectar y subir al repositorio remoto

```bash
# Agregar el remoto (reemplazar USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/USUARIO/zpinnal.git

# Subir al repositorio remoto
git push -u origin main
```

## Repositorio actual

- **URL:** https://github.com/nelsonyrg/zpinnal
- **Rama principal:** main
- **Commit inicial:** d6f10ec

## Comandos Git útiles

```bash
# Ver estado del repositorio
git status

# Ver historial de commits
git log --oneline

# Ver remotos configurados
git remote -v

# Descargar cambios del remoto
git pull origin main

# Subir cambios al remoto
git push origin main

# Crear nueva rama
git checkout -b nombre-rama

# Cambiar de rama
git checkout nombre-rama

# Fusionar rama a main
git checkout main
git merge nombre-rama
```

## Flujo de trabajo recomendado

1. **Crear rama para nueva funcionalidad:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Hacer cambios y commits:**
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   ```

3. **Subir rama al remoto:**
   ```bash
   git push -u origin feature/nueva-funcionalidad
   ```

4. **Crear Pull Request en GitHub**

5. **Fusionar a main después de revisión**

## Configuración de Git (opcional)

```bash
# Configurar nombre de usuario
git config --global user.name "Tu Nombre"

# Configurar email
git config --global user.email "tu@email.com"

# Configurar editor por defecto
git config --global core.editor "code --wait"

# Ver configuración actual
git config --list
```
