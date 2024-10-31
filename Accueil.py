import streamlit as st


st.set_page_config(page_title="GAgent", page_icon="🤖")


def navigate_to(page_name):
    st.query_params(page=page_name)


# Définir les fonctions pour chaque page


def main_page():
    st.title("GAgent")
    st.write("Bienvenue sur GAgent votre IAssistant")
    st.write("<- Choisissez votre asistant dans le menu")
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Afficher le contenu en Markdown
    st.markdown(readme_content, unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "main"
# Créer les boutons et rediriger en fonction du bouton cliqué
if st.session_state.page == "main":
    main_page()
