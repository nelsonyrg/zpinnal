# Fix: Error tabla "categorias" no existe

## Problema

Al acceder al módulo de Categorías en el frontend (`http://localhost:5173/categorias`), el backend mostraba el siguiente error en los logs:

```
sqlalchemy.exc.ProgrammingError:
(sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError)
<class 'asyncpg.exceptions.UndefinedTableError'>:
relation "categorias" does not exist

[SQL: SELECT categorias.id, categorias.nombre, categorias.descripcion,
categorias.icono, categorias.activo, categorias.categoria_padre_id,
categorias.created_at, categorias.updated_at
FROM categorias ORDER BY categorias.nombre
LIMIT $1::INTEGER OFFSET $2::INTEGER]
```

## Causa

El script `scripts/init-db.sql` solo se ejecuta cuando el contenedor de PostgreSQL se crea **por primera vez**. Como la base de datos `zpinnaldb` ya existía antes de agregar la definición de la tabla `categorias` al script, la tabla nunca fue creada.

## Solución aplicada

Se ejecutó el SQL directamente en el contenedor de PostgreSQL en ejecución:

```powershell
docker-compose exec -T db psql -U postgres -d zpinnaldb <<'SQL'
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    icono VARCHAR(700),
    activo BOOLEAN DEFAULT true NOT NULL,
    categoria_padre_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_categorias_nombre ON categorias(nombre);
CREATE INDEX IF NOT EXISTS idx_categorias_padre ON categorias(categoria_padre_id);
CREATE INDEX IF NOT EXISTS idx_categorias_activo ON categorias(activo);

DROP TRIGGER IF EXISTS update_categorias_updated_at ON categorias;
CREATE TRIGGER update_categorias_updated_at
    BEFORE UPDATE ON categorias
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

INSERT INTO categorias (nombre, descripcion, activo) VALUES
    ('Electrónica', 'Productos electrónicos y tecnología', true),
    ('Ropa', 'Vestimenta y accesorios', true),
    ('Hogar', 'Artículos para el hogar', true);

INSERT INTO categorias (nombre, descripcion, activo, categoria_padre_id)
SELECT 'Smartphones', 'Teléfonos inteligentes', true, id FROM categorias WHERE nombre = 'Electrónica';

INSERT INTO categorias (nombre, descripcion, activo, categoria_padre_id)
SELECT 'Laptops', 'Computadoras portátiles', true, id FROM categorias WHERE nombre = 'Electrónica';
SQL
```

## Datos insertados

| ID | Nombre | Categoría Padre | Activo |
|----|--------|-----------------|--------|
| 1 | Electrónica | — | true |
| 2 | Ropa | — | true |
| 3 | Hogar | — | true |
| 4 | Smartphones | Electrónica (1) | true |
| 5 | Laptops | Electrónica (1) | true |

## Prevención futura

Para instalaciones nuevas desde cero, el `init-db.sql` ya incluye la creación de la tabla. Si se necesita recrear la base de datos:

```powershell
docker-compose down -v
docker-compose up -d
```

Esto elimina los volúmenes y fuerza la ejecución del script de inicialización.
