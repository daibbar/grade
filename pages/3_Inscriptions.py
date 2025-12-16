import streamlit as st
import pandas as pd
from src.database import run_query, get_data

st.set_page_config(page_title="Inscriptions", page_icon="📝")
st.title("📝 Gestion des Inscriptions")

# --- 1. RÉCUPÉRATION DES DONNÉES POUR LES LISTES DÉROULANTES ---
# On a besoin des ID et des Noms pour que l'utilisateur choisisse facilement

# Liste des étudiants
df_etudiants = get_data("SELECT id_etudiant, nom, prenom, filiere FROM etudiant")
etudiant_dict = {
    row['id_etudiant']: f"{row['nom']} {row['prenom']} ({row['filiere']})" 
    for _, row in df_etudiants.iterrows()
} if not df_etudiants.empty else {}

# Liste des activités
df_activites = get_data("SELECT id_activite, nom_activite, type_activite, capacite_max FROM activite")
activite_dict = {
    row['id_activite']: f"{row['nom_activite']} ({row['type_activite']}) - Max: {row['capacite_max']}" 
    for _, row in df_activites.iterrows()
} if not df_activites.empty else {}


# --- 2. FORMULAIRE D'INSCRIPTION ---
st.subheader("Nouvelle Inscription")

if not etudiant_dict or not activite_dict:
    st.warning("Il faut d'abord créer des étudiants et des activités pour faire une inscription.")
else:
    with st.form("form_inscription"):
        col1, col2 = st.columns(2)
        
        # Sélecteurs
        id_etudiant_sel = col1.selectbox("Choisir un Étudiant", options=etudiant_dict.keys(), format_func=lambda x: etudiant_dict[x])
        id_activite_sel = col2.selectbox("Choisir une Activité", options=activite_dict.keys(), format_func=lambda x: activite_dict[x])
        
        submitted = st.form_submit_button("Inscrire l'étudiant")
        
        if submitted:
            # --- LOGIQUE MÉTIER (SQL) ---
            
            # A. Vérifier la capacité (Requête COUNT)
            res = get_data("SELECT COUNT(*) as total FROM inscription WHERE id_activite = ?", (id_activite_sel,))
            nb_inscrits = res.iloc[0]['total']
            
            # Récupérer la capacité max de l'activité choisie
            cap_max = df_activites[df_activites['id_activite'] == id_activite_sel]['capacite_max'].values[0]
            
            if nb_inscrits >= cap_max:
                st.error(f"❌ Impossible : L'activité est complète ({nb_inscrits}/{cap_max}) !")
            else:
                # B. Tenter l'inscription
                try:
                    run_query(
                        "INSERT INTO inscription (id_etudiant, id_activite) VALUES (?, ?)",
                        (id_etudiant_sel, id_activite_sel)
                    )
                    st.success("✅ Inscription validée !")
                except Exception as e:
                    # Ici, on attrape l'erreur UNIQUE (déjà inscrit)
                    if "UNIQUE constraint failed" in str(e):
                        st.warning("⚠️ Cet étudiant est DÉJÀ inscrit à cette activité.")
                    else:
                        st.error(f"Erreur technique : {e}")

st.divider()

# --- 3. LISTE DES INSCRIPTIONS (JOIN COMPLEXE) ---
st.subheader("📋 Liste globale des inscriptions")

# Cette requête montre la puissance de SQL : On joint 3 tables !
sql_list = """
SELECT 
    i.id_inscription,
    e.nom || ' ' || e.prenom AS etudiant,
    e.filiere,
    a.nom_activite,
    a.type_activite,
    i.date_inscription
FROM inscription i
JOIN etudiant e ON i.id_etudiant = e.id_etudiant
JOIN activite a ON i.id_activite = a.id_activite
ORDER BY i.date_inscription DESC
"""

st.dataframe(get_data(sql_list), use_container_width=True)

# Bouton de désinscription (DELETE)
with st.expander("🗑️ Annuler une inscription"):
    id_to_del = st.number_input("ID Inscription à supprimer", min_value=1, step=1)
    if st.button("Supprimer l'inscription"):
        run_query("DELETE FROM inscription WHERE id_inscription = ?", (id_to_del,))
        st.success("Inscription supprimée.")
        st.rerun()