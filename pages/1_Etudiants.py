import streamlit as st
import pandas as pd
from src.database import run_query, get_data

st.set_page_config(page_title="Étudiants", page_icon="🎓")

st.title("🎓 Gestion des Étudiants")

# --- SECTION 1 : AJOUTER UN ÉTUDIANT ---
st.subheader("Ajouter un nouvel étudiant")

with st.form("form_add_etudiant"):
    col1, col2 = st.columns(2)
    nom = col1.text_input("Nom")
    prenom = col2.text_input("Prénom")
    email = st.text_input("Email (doit être unique)")
    filiere = st.selectbox("Filière", ["IID", "G.Info", "G.Indus", "Reseaux", "AP"])
    
    submitted = st.form_submit_button("Enregistrer")
    
    if submitted:
        if nom and prenom and email:
            try:
                # Requête SQL paramétrée pour éviter les injections SQL
                query = "INSERT INTO etudiant (nom, prenom, email, filiere) VALUES (?, ?, ?, ?)"
                run_query(query, (nom, prenom, email, filiere))
                st.success(f"Étudiant {nom} {prenom} ajouté avec succès !")
            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
        else:
            st.warning("Veuillez remplir tous les champs obligatoires.")

st.markdown("---")

# --- SECTION 2 : LISTE DES ÉTUDIANTS ---
st.subheader("Liste des Étudiants")

# Requête SQL simple de lecture
df_etudiants = get_data("SELECT * FROM etudiant ORDER BY id_etudiant DESC")

# Affichage avec Streamlit
st.dataframe(df_etudiants, use_container_width=True)

st.markdown("---")

# --- SECTION 3 : SUPPRESSION RAPIDE ---
st.subheader("Supprimer un étudiant")
with st.expander("Zone de danger"):
    id_to_delete = st.number_input("ID de l'étudiant à supprimer", min_value=1, step=1)
    if st.button("🗑️ Supprimer cet étudiant"):
        try:
            # Vérifier si l'étudiant existe avant de supprimer (Optionnel mais propre)
            run_query("DELETE FROM etudiant WHERE id_etudiant = ?", (id_to_delete,))
            st.success(f"Étudiant ID {id_to_delete} supprimé.")
            st.rerun() # Rafraîchir la page pour mettre à jour le tableau
        except Exception as e:
            st.error(f"Impossible de supprimer : {e}")