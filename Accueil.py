import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ice Acquisition", page_icon="🤖")

def navigate_to(page_name):
    st.query_params(page=page_name)

# Définir les fonctions pour chaque page
def Ice_Alternative():
    st.markdown(
        "[Lien vers Ice Alternative](https://mediafiles.botpress.cloud/5e78a2ca-9945-4a7c-bac7-04d847dd6bfc/webchat/bot.html)"
    )
    if st.button("Retour à la page principale"):
        st.experimental_rerun()

def Ice_Acquisition():
    st.markdown(
        "[Lien vers Ice Acquisition](https://chat.moustacheai.com/chat/d1ec6bad-df38-4019-b198-63def35f1d6e?&customerUUID=0359ed72-93c3-4ead-aa51-76d3005f4b22)"
    )
    if st.button("Retour à la page principale"):
        st.experimental_rerun()




def main_page():
    st.title("Ice CréIAtion")
    st.write("Choisissez votre IAlternative.")
    st.title("")

    if st.button("Ice Alternative"):
        Ice_Alternative()

    if st.button("Ice Acquisition"):
        Ice_Acquisition()


if "page" not in st.session_state:
    st.session_state.page = "main"
# Créer les boutons et rediriger en fonction du bouton cliqué
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "page1":
    Ice_Alternative()
elif st.session_state.page == "page2":
    Ice_Acquisition()

