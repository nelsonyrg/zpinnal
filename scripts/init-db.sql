-- ================================================
-- Script de inicialización de base de datos
-- Se ejecuta automáticamente al crear el contenedor
-- ================================================

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tabla de ejemplo: usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para users
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- Tabla de Categorías
-- ================================================
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

-- Índices para categorias
CREATE INDEX IF NOT EXISTS idx_categorias_nombre ON categorias(nombre);
CREATE INDEX IF NOT EXISTS idx_categorias_padre ON categorias(categoria_padre_id);
CREATE INDEX IF NOT EXISTS idx_categorias_activo ON categorias(activo);

-- Trigger para categorias
DROP TRIGGER IF EXISTS update_categorias_updated_at ON categorias;
CREATE TRIGGER update_categorias_updated_at
    BEFORE UPDATE ON categorias
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Categorías de ejemplo
INSERT INTO categorias (nombre, descripcion, activo) VALUES
    ('Electrónica', 'Productos electrónicos y tecnología', true),
    ('Ropa', 'Vestimenta y accesorios', true),
    ('Hogar', 'Artículos para el hogar', true)
ON CONFLICT DO NOTHING;

-- Subcategorías de ejemplo
INSERT INTO categorias (nombre, descripcion, activo, categoria_padre_id)
SELECT 'Smartphones', 'Teléfonos inteligentes', true, id FROM categorias WHERE nombre = 'Electrónica'
ON CONFLICT DO NOTHING;

INSERT INTO categorias (nombre, descripcion, activo, categoria_padre_id)
SELECT 'Laptops', 'Computadoras portátiles', true, id FROM categorias WHERE nombre = 'Electrónica'
ON CONFLICT DO NOTHING;

-- ================================================
-- Tabla de Servicios
-- ================================================
CREATE TABLE IF NOT EXISTS servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(300) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para servicios
CREATE INDEX IF NOT EXISTS idx_servicios_nombre ON servicios(nombre);
CREATE INDEX IF NOT EXISTS idx_servicios_activo ON servicios(activo);

-- Trigger para servicios
DROP TRIGGER IF EXISTS update_servicios_updated_at ON servicios;
CREATE TRIGGER update_servicios_updated_at
    BEFORE UPDATE ON servicios
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- Tabla intermedia N:N Servicio <-> Categoria
-- ================================================
CREATE TABLE IF NOT EXISTS servicio_categorias (
    servicio_id INTEGER REFERENCES servicios(id) ON DELETE CASCADE,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (servicio_id, categoria_id)
);

CREATE INDEX IF NOT EXISTS idx_sc_servicio ON servicio_categorias(servicio_id);
CREATE INDEX IF NOT EXISTS idx_sc_categoria ON servicio_categorias(categoria_id);

-- Servicios de ejemplo
INSERT INTO servicios (nombre, descripcion, activo) VALUES
    ('Reparación de pantalla', 'Servicio de reparación de pantallas para smartphones y tablets', true),
    ('Mantenimiento de laptop', 'Limpieza, actualización de software y hardware', true),
    ('Asesoría de imagen', 'Consultoría personalizada de estilo y vestimenta', true)
ON CONFLICT DO NOTHING;

-- Asignar categorías a servicios
INSERT INTO servicio_categorias (servicio_id, categoria_id)
SELECT s.id, c.id FROM servicios s, categorias c
WHERE s.nombre = 'Reparación de pantalla' AND c.nombre IN ('Electrónica', 'Smartphones')
ON CONFLICT DO NOTHING;

INSERT INTO servicio_categorias (servicio_id, categoria_id)
SELECT s.id, c.id FROM servicios s, categorias c
WHERE s.nombre = 'Mantenimiento de laptop' AND c.nombre IN ('Electrónica', 'Laptops')
ON CONFLICT DO NOTHING;

INSERT INTO servicio_categorias (servicio_id, categoria_id)
SELECT s.id, c.id FROM servicios s, categorias c
WHERE s.nombre = 'Asesoría de imagen' AND c.nombre = 'Ropa'
ON CONFLICT DO NOTHING;

-- Usuario de prueba (password: testpassword123)
-- Hash generado con bcrypt
INSERT INTO users (email, username, hashed_password, is_active, is_superuser)
VALUES (
    'admin@example.com',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.i0vx0tJvXPmC3G',
    true,
    true
) ON CONFLICT (email) DO NOTHING;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos inicializada correctamente';
END $$;
