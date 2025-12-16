import streamlit as st
import pandas as pd
from src.database import run_query, get_data

st.set_page_config(page_title="Activités & Responsables", page_icon="⚽")

st.title("⚽ Gestion des Activités")

# Onglets pour séparer les deux concepts (UX plus propre)
tab1, tab2 = st.tabs(["👥 Responsables", "📅 Activités"])

# ==============================================================================
# ONGLET 1 : GESTION DES RESPONSABLES
# ==============================================================================
with tab1:
    st.header("Ajouter un Responsable")
    
    with st.form("form_resp"):
        col1, col2 = st.columns(2)
        nom = col1.text_input("Nom")
        prenom = col2.text_input("Prénom")
        email = st.text_input("Email")
        
        if st.form_submit_button("Ajouter Responsable"):
            try:
                run_query(
                    "INSERT INTO responsable (nom, prenom, email) VALUES (?, ?, ?)",
                    (nom, prenom, email)
                )
                st.success(f"Responsable {nom} {prenom} ajouté !")
            except Exception as e:
                st.error(f"Erreur : {e}")

    st.divider()
    st.subheader("Liste des Responsables")
    st.dataframe(get_data("SELECT * FROM responsable"), use_container_width=True)


# ==============================================================================
# ONGLET 2 : GESTION DES ACTIVITÉS (Le cœur du SQL)
# ==============================================================================
with tab2:
    st.header("Créer une nouvelle activité")

    # 1. Récupérer la liste des responsables pour le menu déroulant (Foreign Key)
    df_resp = get_data("SELECT id_responsable, nom, prenom FROM responsable")
    
    # Créer un dictionnaire {ID: "Nom Prénom"} pour l'affichage
    if not df_resp.empty:
        options_resp = {
            row['id_responsable']: f"{row['nom']} {row['prenom']}" 
            for _, row in df_resp.iterrows()
        }
    else:
        st.warning("⚠️ Aucun responsable trouvé. Veuillez en ajouter un dans l'onglet précédent d'abord.")
        options_resp = {}

    # 2. Formulaire de création
    with st.form("form_activite"):
        nom_act = st.text_input("Nom de l'activité")
        type_act = st.selectbox("Type", ["Club", "Atelier", "Evenement"])
        desc = st.text_area("Description")
        
        c1, c2 = st.columns(2)
        d_debut = c1.date_input("Date début")
        d_fin = c2.date_input("Date fin")
        
        cap_max = st.number_input("Capacité Max", min_value=1, value=20)
        
        # Sélection du responsable via son ID
        id_resp_selected = st.selectbox(
            "Responsable", 
            options=options_resp.keys(), 
            format_func=lambda x: options_resp[x]
        ) if options_resp else None

        if st.form_submit_button("Créer l'activité"):
            if d_fin < d_debut:
                st.error("La date de fin ne peut pas être avant la date de début !")
            elif not id_resp_selected:
                st.error("Il faut sélectionner un responsable.")
            else:
                try:
                    query = """
                        INSERT INTO activite 
                        (nom_activite, type_activite, description, date_debut, date_fin, capacite_max, id_responsable)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    run_query(query, (nom_act, type_act, desc, d_debut, d_fin, cap_max, id_resp_selected))
                    st.success("Activité créée avec succès !")
                except Exception as e:
                    st.error(f"Erreur SQL : {e}")

    st.divider()
    
    # 3. Affichage avec JOIN (Exigence du cahier des charges)
    st.subheader("Planning des Activités (avec Responsables)")
    
    sql_display = """
    SELECT 
        a.id_activite,
        a.nom_activite,
        a.type_activite,
        a.date_debut,
        a.date_fin,
        a.capacite_max,
        r.nom || ' ' || r.prenom AS responsable_nom
    FROM activite a
    LEFT JOIN responsable r ON a.id_responsable = r.id_responsable
    ORDER BY a.date_debut
    """
    st.dataframe(get_data(sql_display), use_container_width=True)