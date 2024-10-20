import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="GAgent", page_icon="🤖")

def navigate_to(page_name):
    st.query_params(page=page_name)

# Définir les fonctions pour chaque page





def main_page():
    st.title("GAgent")
    st.write("Bienvenue sur GAgent votre IAssistant")
    st.write("<- Choisissez votre asistant dans le menu")




if "page" not in st.session_state:
    st.session_state.page = "main"
# Créer les boutons et rediriger en fonction du bouton cliqué
if st.session_state.page == "main":
    main_page()


