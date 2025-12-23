
-- data/schema.sql

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS responsable (
    id_responsable INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS clubs (
    id_club INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    category TEXT CHECK(category IN ('entertaiment', 'sport', 'technologique', 'entrepreneuriat social')) NOT NULL,
    date_creation DATETIME NOT NULL,
    club_description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id_event INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_event TEXT NOT NULL,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    CHECK (date_fin >= date_debut)
);

CREATE TABLE IF NOT EXISTS fillieres (
    id_filliere INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT CHECK (nom IN ('IID', 'GI', 'IRIC', 'GE', 'GPEE', 'MGSI')) NOT NULL
);

CREATE TABLE IF NOT EXISTS ressources (
    id_ressource INTEGER PRIMARY KEY AUTOINCREMENT,
    type_ressource TEXT CHECK (type_ressource IN ('salle', 'Amphitheatre', 'buvet', 'Bibliotheque', 'terrain', 'labo')) NOT NULL, 
    nom TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id_activite INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_activite TEXT NOT NULL,
    activite_description TEXT,
    type_activite TEXT CHECK(type_activite IN ('Voyage', 'Atelier', 'Conference', 'Competition')) NOT NULL,
    capacite_max INTEGER CHECK(capacite_max > 0),
    date_debut TIMESTAMP NOT NULL,
    date_fin TIMESTAMP NOT NULL,
    id_club INTEGER,
    id_event INTEGER,
    FOREIGN KEY (id_club) REFERENCES clubs(id_club) ON DELETE CASCADE,
    FOREIGN KEY (id_event) REFERENCES events(id_event) ON DELETE CASCADE,
    CONSTRAINT check_only_one CHECK (
        (id_club IS NULL AND id_event IS NOT NULL) OR (id_club IS NOT NULL AND  id_event IS NULL)
    ),
    CHECK (date_fin >= date_debut)
);

CREATE TABLE IF NOT EXISTS etudiants (
    id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    cne TEXT UNIQUE NOT NULL, 
    email TEXT UNIQUE NOT NULL,
    id_filliere INTEGER,
    FOREIGN KEY (id_filliere) REFERENCES fillieres(id_filliere)
);

CREATE TABLE IF NOT EXISTS clubs_membres (
    id_adhesion INTEGER PRIMARY KEY AUTOINCREMENT,
    date_adhesion DATE DEFAULT CURRENT_DATE,
    id_club INTEGER NOT NULL,
    id_etudiant INTEGER NOT NULL,
    FOREIGN KEY (id_club) REFERENCES clubs(id_club) ON DELETE CASCADE,
    FOREIGN KEY (id_etudiant) REFERENCES etudiants(id_etudiant) ON DELETE CASCADE,
    UNIQUE(id_club, id_etudiant)    
);


CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    id_ressource INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    FOREIGN KEY (id_ressource) REFERENCES ressources(id_ressource) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activities(id_activite) ON DELETE CASCADE
    --  si tu veux que chaque acitvite ne peut pas reserver une resource
    -- qu'une seule fois durant tout la duree de l'activite ajouter UNIQUE(id_ressource, id_activite)
    CHECK (date_fin >= date_debut)

);

CREATE TABLE IF NOT EXISTS events_organizers (
    id_event INTEGER NOT NULL,
    id_club INTEGER NOT NULL,
    FOREIGN KEY (id_event) REFERENCES events(id_event) ON DELETE CASCADE,
    FOREIGN KEY (id_club) REFERENCES clubs(id_club) ON DELETE CASCADE,
    UNIQUE(id_event, id_club)
);

CREATE TABLE IF NOT EXISTS events_participants (
    id_event INTEGER NOT NULL,
    id_etudiant INTEGER NOT NULL, 
    FOREIGN KEY (id_etudiant) REFERENCES etudiants(id_etudiant) ON DELETE CASCADE,
    FOREIGN KEY (id_event) REFERENCES events(id_event) ON DELETE CASCADE,
    UNIQUE(id_etudiant, id_event)
);

CREATE TABLE IF NOT EXISTS inscriptions (
    id_inscription INTEGER PRIMARY KEY AUTOINCREMENT,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_etudiant INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    FOREIGN KEY (id_etudiant) REFERENCES etudiants(id_etudiant) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activities(id_activite) ON DELETE CASCADE,
    UNIQUE(id_etudiant, id_activite) -- Prevents double booking
);

CREATE TABLE IF NOT EXISTS guests (
    id_guest INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_name TEXT NOT NULL,
    guest_phone TEXT NOT NULL,
    guest_email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS guest_activity_role (
    guest_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_guest INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    role_description TEXT NOT NULL,
    role_start_date TIMESTAMP NOT NULL,
    role_end_date TIMESTAMP NOT NULL,
    FOREIGN KEY (id_guest) REFERENCES guests(id_guest) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activities(id_activite) ON DELETE CASCADE,
    CHECK (role_end_date >= role_start_date)
);

INSERT INTO fillieres (nom) VALUES ('IID');
INSERT INTO fillieres (nom) VALUES ('GI');
INSERT INTO fillieres (nom) VALUES ('MGSI');
INSERT INTO fillieres (nom) VALUES ('IRIC');
INSERT INTO fillieres (nom) VALUES ('GI');
INSERT INTO fillieres (nom) VALUES ('GPEE');