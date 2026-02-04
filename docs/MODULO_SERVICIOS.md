# Módulo de Servicios

## Descripción

Módulo CRUD completo para la entidad **Servicio** con relación muchos a muchos (N:N) con la entidad **Categoría**.

## Modelo de datos

### Entidad Servicio

| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | SERIAL | Primary Key, autoincremental |
| nombre | VARCHAR(300) | Requerido, único |
| descripcion | TEXT | Sin límite de caracteres |
| activo | BOOLEAN | Default: true |
| created_at | TIMESTAMP | Generado automáticamente |
| updated_at | TIMESTAMP | Actualizado automáticamente |

### Relación N:N con Categorías

```
servicios (N) ←→ servicio_categorias ←→ (N) categorias
```

- Un servicio puede tener múltiples categorías asignadas
- Una categoría puede estar asignada a múltiples servicios
- La relación se gestiona a través de la tabla intermedia `servicio_categorias`

### Tabla intermedia: servicio_categorias

| Campo | Tipo | Restricción |
|-------|------|-------------|
| servicio_id | INTEGER | FK → servicios.id, ON DELETE CASCADE |
| categoria_id | INTEGER | FK → categorias.id, ON DELETE CASCADE |

Primary Key compuesta: (servicio_id, categoria_id)

## Archivos del Backend

### Modelo SQLAlchemy

**Archivo:** `backend/app/models/servicio.py`

- Clase `Servicio` con campos id, nombre, descripcion, activo, timestamps
- Tabla intermedia `servicio_categorias` definida con `sqlalchemy.Table`
- Relación `categorias` usando `relationship()` con `secondary=servicio_categorias`
- Estrategia de carga: `lazy="selectin"` para carga eficiente

### Schemas Pydantic

**Archivo:** `backend/app/schemas/servicio.py`

| Schema | Uso |
|--------|-----|
| `ServicioBase` | Campos base compartidos |
| `ServicioCreate` | Creación: incluye `categoria_ids: List[int]` |
| `ServicioUpdate` | Actualización: todos los campos opcionales, incluye `categoria_ids` |
| `ServicioResponse` | Respuesta: incluye `categorias: List[CategoriaSimple]` |
| `ServicioSimple` | Versión simplificada (id, nombre, activo) |

### Servicio CRUD

**Archivo:** `backend/app/services/servicio.py`

| Método | Descripción |
|--------|-------------|
| `get_all()` | Listar con filtros: solo_activos, categoria_id |
| `get_by_id()` | Obtener por ID con categorías cargadas |
| `get_by_nombre()` | Buscar por nombre (validación unicidad) |
| `create()` | Crear servicio y asignar categorías por IDs |
| `update()` | Actualizar campos y reasignar categorías |
| `delete()` | Eliminar servicio (cascade elimina relaciones) |
| `toggle_activo()` | Cambiar estado activo/inactivo |
| `count()` | Contar servicios con filtro opcional |

### Endpoints API

**Archivo:** `backend/app/api/v1/endpoints/servicios.py`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/servicios` | Listar con filtros (solo_activos, categoria_id) |
| GET | `/api/v1/servicios/count` | Conteo total |
| GET | `/api/v1/servicios/{id}` | Obtener por ID |
| POST | `/api/v1/servicios` | Crear con categorías asignadas |
| PUT | `/api/v1/servicios/{id}` | Actualizar con reasignación de categorías |
| PATCH | `/api/v1/servicios/{id}/toggle-activo` | Toggle activo/inactivo |
| DELETE | `/api/v1/servicios/{id}` | Eliminar servicio |

### Validaciones del API

- **Nombre único:** No permite duplicados al crear o actualizar
- **Categorías existentes:** Verifica que cada categoria_id exista en la base de datos
- **404:** Retorna error si el servicio no existe

### Registro del router

**Archivo modificado:** `backend/app/api/v1/__init__.py`

```python
from app.api.v1.endpoints import health, users, categorias, servicios

router.include_router(servicios.router, prefix="/servicios", tags=["servicios"])
```

## Archivos del Frontend

### Tipos TypeScript

**Archivo:** `frontend/src/types/servicio.ts`

- `Servicio`: Interfaz completa con categorías como `CategoriaSimple[]`
- `ServicioCreate`: Incluye `categoria_ids: number[]` para asignación
- `ServicioUpdate`: Todos los campos opcionales
- `ServicioSimple`: Versión reducida
- `ServicioFilters`: Filtros para listado (solo_activos, categoria_id)

### Servicio API

**Archivo:** `frontend/src/services/servicioApi.ts`

Cliente HTTP con Axios para todos los endpoints:
- `listar()` con filtros como query params
- `contar()`, `obtener()`, `crear()`, `actualizar()`
- `toggleActivo()`, `eliminar()`

### Store Pinia

**Archivo:** `frontend/src/stores/servicioStore.ts`

| Estado | Tipo |
|--------|------|
| `servicios` | Lista de servicios cargados |
| `servicioActual` | Servicio seleccionado para edición |
| `loading` | Indicador de carga |
| `error` | Mensaje de error |
| `totalServicios` | Conteo total |

| Getter | Descripción |
|--------|-------------|
| `serviciosActivos` | Filtro computado de servicios activos |

| Acción | Descripción |
|--------|-------------|
| `cargarServicios()` | Listar con filtros |
| `cargarConteo()` | Obtener total |
| `obtenerServicio()` | Cargar uno por ID |
| `crearServicio()` | Crear y agregar a la lista |
| `actualizarServicio()` | Actualizar y refrescar en la lista |
| `toggleActivo()` | Cambiar estado |
| `eliminarServicio()` | Eliminar y remover de la lista |

### Componentes Vue

#### ServicioForm.vue

**Archivo:** `frontend/src/components/servicios/ServicioForm.vue`

- Formulario para crear y editar servicios
- Campo nombre con contador de caracteres (máx. 300)
- Campo descripción como textarea sin límite
- **Selector múltiple de categorías** con chips interactivos
  - Muestra todas las categorías activas
  - Click para seleccionar/deseleccionar
  - Badge con conteo de seleccionadas
  - Indicador visual (check) en chips seleccionados
- Toggle de activo con checkbox
- Validación de campos requeridos
- Manejo de errores del API

#### ServicioLista.vue

**Archivo:** `frontend/src/components/servicios/ServicioLista.vue`

- Tabla con columnas: Nombre, Categorías, Estado, Acciones
- Preview de descripción (primeros 80 caracteres)
- Categorías mostradas como tags con estilo pill
- **Filtros:**
  - Por estado (Todos / Solo activos / Solo inactivos)
  - Por categoría (dropdown con todas las categorías)
- Toggle de estado activo/inactivo clickeable
- Botones de editar y eliminar por fila
- Modal de confirmación para eliminación
- Estado de lista vacía con botón de crear

#### ServiciosView.vue

**Archivo:** `frontend/src/views/ServiciosView.vue`

- Vista principal que alterna entre lista y formulario
- Navegación: lista → crear / lista → editar → lista
- Botón "Volver a la lista" en modo formulario

### Ruta y Navegación

**Archivo modificado:** `frontend/src/router/index.ts`

```typescript
{
  path: '/servicios',
  name: 'servicios',
  component: () => import('../views/ServiciosView.vue')
}
```

**Archivo modificado:** `frontend/src/App.vue`

Enlace agregado en la barra de navegación: `Categorías | Servicios | Acerca de`

## Base de datos

### Script de inicialización

**Archivo modificado:** `scripts/init-db.sql`

Se agregaron:
- Tabla `servicios` con índices y trigger de updated_at
- Tabla `servicio_categorias` con índices
- 3 servicios de ejemplo con categorías asignadas

### Datos de ejemplo

| Servicio | Categorías asignadas |
|----------|---------------------|
| Reparación de pantalla | Electrónica, Smartphones |
| Mantenimiento de laptop | Electrónica, Laptops |
| Asesoría de imagen | Ropa |

### Creación manual en BD existente

Si la base de datos ya existe y no tiene las tablas, ejecutar:

```powershell
docker-compose exec -T db psql -U postgres -d zpinnaldb <<'SQL'
CREATE TABLE IF NOT EXISTS servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(300) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_servicios_nombre ON servicios(nombre);
CREATE INDEX IF NOT EXISTS idx_servicios_activo ON servicios(activo);

DROP TRIGGER IF EXISTS update_servicios_updated_at ON servicios;
CREATE TRIGGER update_servicios_updated_at
    BEFORE UPDATE ON servicios
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TABLE IF NOT EXISTS servicio_categorias (
    servicio_id INTEGER REFERENCES servicios(id) ON DELETE CASCADE,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (servicio_id, categoria_id)
);

CREATE INDEX IF NOT EXISTS idx_sc_servicio ON servicio_categorias(servicio_id);
CREATE INDEX IF NOT EXISTS idx_sc_categoria ON servicio_categorias(categoria_id);
SQL
```

### Resetear todo desde cero

```powershell
docker-compose down -v
docker-compose up -d
```

## Ejemplos de uso del API

### Crear servicio con categorías

```bash
curl -X POST http://localhost:8000/api/v1/servicios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Nuevo Servicio",
    "descripcion": "Descripción del servicio",
    "activo": true,
    "categoria_ids": [1, 3]
  }'
```

### Listar servicios filtrados por categoría

```bash
curl http://localhost:8000/api/v1/servicios?categoria_id=1&solo_activos=true
```

### Actualizar categorías de un servicio

```bash
curl -X PUT http://localhost:8000/api/v1/servicios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "categoria_ids": [2, 4, 5]
  }'
```

## Commit

- **Hash:** `5cd7a4f`
- **Rama:** `dev1`
- **Mensaje:** feat: add Servicios module with N:N relationship to Categorias
