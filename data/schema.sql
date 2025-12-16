-- data/schema.sql

-- Enable Foreign Keys enforcement for SQLite
PRAGMA foreign_keys = ON;

-- 1. Table Responsables
CREATE TABLE IF NOT EXISTS responsable (
    id_responsable INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- 2. Table Activites
CREATE TABLE IF NOT EXISTS activite (
    id_activite INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_activite TEXT NOT NULL,
    type_activite TEXT CHECK(type_activite IN ('Club', 'Atelier', 'Evenement')) NOT NULL,
    description TEXT,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    capacite_max INTEGER CHECK(capacite_max > 0),
    id_responsable INTEGER,
    FOREIGN KEY (id_responsable) REFERENCES responsable(id_responsable) ON DELETE SET NULL,
    CHECK (date_fin >= date_debut)
);

-- 3. Table Etudiants
CREATE TABLE IF NOT EXISTS etudiant (
    id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    filiere TEXT NOT NULL
);

-- 4. Table Inscriptions
CREATE TABLE IF NOT EXISTS inscription (
    id_inscription INTEGER PRIMARY KEY AUTOINCREMENT,
    id_etudiant INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_etudiant) REFERENCES etudiant(id_etudiant) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite) ON DELETE CASCADE,
    UNIQUE(id_etudiant, id_activite) -- Prevents double booking
);