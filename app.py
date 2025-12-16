import streamlit as st
import os
from src.database import init_db, DB_PATH

# 1. Page Configuration (Title, Icon)
st.set_page_config(
    page_title="Gestion Parascolaire",
    page_icon="🏫",
    layout="wide"
)

# 2. Main Header
st.title("🏫 Système de Gestion des Activités Parascolaires")
st.markdown("---")

# 3. Project Description
st.markdown("""
### Bienvenue
Cette application permet de gérer les activités parascolaires d'un établissement.
Utilisez le menu latéral pour naviguer entre les différentes sections :

* **Étudiants** : Gestion des inscriptions administratives.
* **Activités** : Création et planning des clubs/ateliers.
* **Inscriptions** : Associer un étudiant à une activité.
* **Planning** : Vue d'ensemble et statistiques.
""")

st.info("💡 Ce projet utilise **SQLite** et **Streamlit** sans ORM, avec des requêtes SQL pures.")

# 4. Database Management Section (Admin Zone)
st.markdown("---")
st.subheader("⚙️ Administration Technique")

col1, col2 = st.columns([1, 3])

with col1:
    # Button to initialize the DB
    if st.button("🔄 Réinitialiser la Base de Données"):
        init_db()
        st.success("Base de données (ré)initialisée avec succès !")

with col2:
    # Check if DB exists to show status
    if os.path.exists(DB_PATH):
        st.success(f"✅ La base de données est connectée : `{DB_PATH}`")
    else:
        st.error("❌ Base de données introuvable. Cliquez sur le bouton pour l'initialiser.")