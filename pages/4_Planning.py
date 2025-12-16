import streamlit as st
import pandas as pd
import plotly.express as px  # Streamlit installe plotly par défaut, c'est top pour les graphes
from src.database import get_data

st.set_page_config(page_title="Planning & Stats", page_icon="📊")
st.title("📊 Tableau de Bord et Planning")

# --- KPI (Indicateurs Clés) ---
st.subheader("Vue d'ensemble")
col1, col2, col3 = st.columns(3)

# On utilise des requêtes COUNT simples pour les "Big Numbers"
nb_etudiants = get_data("SELECT COUNT(*) as c FROM etudiant").iloc[0]['c']
nb_activites = get_data("SELECT COUNT(*) as c FROM activite").iloc[0]['c']
nb_inscriptions = get_data("SELECT COUNT(*) as c FROM inscription").iloc[0]['c']

col1.metric("Étudiants Inscrits", nb_etudiants)
col2.metric("Activités Disponibles", nb_activites)
col3.metric("Total Inscriptions", nb_inscriptions)

st.divider()

# --- REQUÊTE COMPLEXE 1 : Taux de remplissage des activités ---
st.subheader("🔥 Popularité des Activités")

# Cette requête est cruciale pour le projet :
# Elle compte le nombre d'inscrits par activité (GROUP BY)
# Elle inclut même les activités sans inscrits (LEFT JOIN)
query_stats = """
SELECT 
    a.nom_activite,
    a.type_activite,
    a.capacite_max,
    COUNT(i.id_inscription) as nb_inscrits,
    ROUND((COUNT(i.id_inscription) * 100.0 / a.capacite_max), 1) as taux_remplissage
FROM activite a
LEFT JOIN inscription i ON a.id_activite = i.id_activite
GROUP BY a.id_activite
ORDER BY nb_inscrits DESC
"""
df_stats = get_data(query_stats)
st.dataframe(df_stats, use_container_width=True)

# Petit graphique bonus (optionnel mais ça fait pro)
if not df_stats.empty:
    fig = px.bar(
        df_stats, 
        x='nom_activite', 
        y='nb_inscrits', 
        color='type_activite',
        title="Nombre d'inscrits par activité"
    )
    st.plotly_chart(fig)

st.divider()

# --- REQUÊTE COMPLEXE 2 : Planning détaillé ---
st.subheader("📅 Planning des Étudiants")

# Filtre par activité
liste_activites = get_data("SELECT nom_activite FROM activite")
choix_activite = st.selectbox("Filtrer par activité", ["Toutes"] + liste_activites['nom_activite'].tolist())

if choix_activite == "Toutes":
    query_planning = """
    SELECT 
        a.nom_activite,
        a.date_debut,
        a.date_fin,
        e.nom || ' ' || e.prenom as etudiant,
        e.email
    FROM inscription i
    JOIN activite a ON i.id_activite = a.id_activite
    JOIN etudiant e ON i.id_etudiant = e.id_etudiant
    ORDER BY a.date_debut
    """
    df_planning = get_data(query_planning)
else:
    # Requête paramétrée avec filtre
    query_planning = """
    SELECT 
        a.nom_activite,
        a.date_debut,
        a.date_fin,
        e.nom || ' ' || e.prenom as etudiant,
        e.email
    FROM inscription i
    JOIN activite a ON i.id_activite = a.id_activite
    JOIN etudiant e ON i.id_etudiant = e.id_etudiant
    WHERE a.nom_activite = ?
    ORDER BY a.date_debut
    """
    df_planning = get_data(query_planning, (choix_activite,))

st.dataframe(df_planning, use_container_width=True)