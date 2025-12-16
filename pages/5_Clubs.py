import streamlit as st
import pandas as pd
from datetime import date
from src.database import run_query, get_data

st.set_page_config(page_title="Gestion des Clubs", page_icon="♟️")
st.title("♟️ Gestion Spécifique des Clubs")

st.info("Cette page permet de gérer uniquement les **Clubs** (Activités récurrentes).")

# --- 1. AJOUTER UN CLUB ---
st.subheader("Créer un nouveau Club")

# Récupération des responsables pour la liste déroulante
df_resp = get_data("SELECT id_responsable, nom, prenom FROM responsable")
options_resp = {row['id_responsable']: f"{row['nom']} {row['prenom']}" for _, row in df_resp.iterrows()} if not df_resp.empty else {}

with st.form("form_add_club"):
    nom_club = st.text_input("Nom du Club (ex: Club Robotique)")
    description = st.text_area("Description / Objectifs")
    
    col1, col2 = st.columns(2)
    # Pour un club, on suppose souvent que ça dure toute l'année, on peut pré-remplir
    date_debut = col1.date_input("Date de lancement", value=date.today())
    date_fin = col2.date_input("Date de fin de saison", value=date(date.today().year + 1, 6, 30))
    
    capacite = st.number_input("Capacité maximale de membres", min_value=5, value=50)
    
    id_resp = st.selectbox("Responsable du Club", options=options_resp.keys(), format_func=lambda x: options_resp[x]) if options_resp else None
    
    submit = st.form_submit_button("Créer le Club")
    
    if submit:
        if not id_resp:
            st.error("Un responsable est obligatoire.")
        elif date_fin < date_debut:
            st.error("La date de fin est incohérente.")
        else:
            try:
                # 🧠 ASTUCE : On force le type_activite à 'Club' directement dans la requête
                query = """
                    INSERT INTO activite 
                    (nom_activite, type_activite, description, date_debut, date_fin, capacite_max, id_responsable)
                    VALUES (?, 'Club', ?, ?, ?, ?, ?)
                """
                run_query(query, (nom_club, description, date_debut, date_fin, capacite, id_resp))
                st.success(f"Le club '{nom_club}' a été créé avec succès !")
            except Exception as e:
                st.error(f"Erreur : {e}")

st.divider()

# --- 2. LISTE DES CLUBS EXISTANTS ---
st.subheader("Liste des Clubs actifs")

# On filtre uniquement sur WHERE type_activite = 'Club'
query_clubs = """
SELECT 
    a.id_activite,
    a.nom_activite,
    a.description,
    r.nom || ' ' || r.prenom as responsable,
    a.capacite_max,
    (SELECT COUNT(*) FROM inscription i WHERE i.id_activite = a.id_activite) as membres_actuels
FROM activite a
LEFT JOIN responsable r ON a.id_responsable = r.id_responsable
WHERE a.type_activite = 'Club'
ORDER BY a.nom_activite
"""

df_clubs = get_data(query_clubs)
st.dataframe(df_clubs, use_container_width=True)

# --- 3. Suppression spécifique ---
with st.expander("🗑️ Dissoudre un Club"):
    list_clubs_to_del = get_data("SELECT id_activite, nom_activite FROM activite WHERE type_activite='Club'")
    dict_del = {row['id_activite']: row['nom_activite'] for _, row in list_clubs_to_del.iterrows()} if not list_clubs_to_del.empty else {}
    
    if dict_del:
        id_del = st.selectbox("Choisir le club à supprimer", options=dict_del.keys(), format_func=lambda x: dict_del[x])
        if st.button("Confirmer la suppression"):
            run_query("DELETE FROM activite WHERE id_activite = ?", (id_del,))
            st.success("Club supprimé.")
            st.rerun()
    else:
        st.write("Aucun club à supprimer.")