PRAGMA foreign_keys = ON;

-- ==========================================
-- TABLE: entities
-- ==========================================
CREATE TABLE IF NOT EXISTS entities (
    entity_id      TEXT PRIMARY KEY,
    name           TEXT,
    entity_type    TEXT,
    created_at     TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at     TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLE: component_types
-- ==========================================
CREATE TABLE IF NOT EXISTS component_types (
    component_type_id  TEXT PRIMARY KEY,
    name               TEXT UNIQUE NOT NULL,
    schema_json        TEXT,
    created_at         TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLE: components
-- ==========================================
CREATE TABLE IF NOT EXISTS components (
    component_id        TEXT PRIMARY KEY,
    entity_id           TEXT NOT NULL,
    component_type_id   TEXT NOT NULL,
    data_json           TEXT NOT NULL,
    created_at          TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at          TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(entity_id)
        REFERENCES entities(entity_id)
        ON DELETE CASCADE,

    FOREIGN KEY(component_type_id)
        REFERENCES component_types(component_type_id)
        ON DELETE CASCADE
);

-- Helpful index for ECS queries
CREATE INDEX IF NOT EXISTS idx_components_entity
    ON components(entity_id);

CREATE INDEX IF NOT EXISTS idx_components_type
    ON components(component_type_id);
