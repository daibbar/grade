import streamlit as st
import pandas as pd
from datetime import date
import datetime
from src.database import run_query, get_data

st.set_page_config(page_title="Gestion des Clubs", page_icon="♟️")
st.title("♟️ Gestion Spécifique des Clubs")

st.subheader("Créer un nouveau Club")

with st.form("form_add_club"):
    col1, col2 = st.columns(2);
    with col1:
        st.text_input("Nom du club")
    with col2:
        st.date_input(
        "Date de Creation",
        value=datetime.date.today(),
        min_value=datetime.date(2007,1,1),
        max_value=datetime.date.today(),
        format="DD/MM/YYYY"
    )
    col3 = st.selectbox("Category du Club", "entertaiment")
    col4 = st.text_area("Description du Club")
    st.form_submit_button("Enregistrer le Club")
st.divider()