import streamlit as st
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent
image_path = Path(__file__).resolve().parent / "files" / "logo.webp"

module_dir = base_dir / "API_connection"
module_sen_message = "sen_message"
module_upload = "upload_file"
module_config = "config"

if module_dir not in sys.path:
    sys.path.append(str(module_dir))
imported_message = __import__(module_sen_message)
imported_upload = __import__(module_upload)
imported_config = __import__(module_config)

fonction_dir = base_dir / "GAgent_fonction"
if fonction_dir not in sys.path:
    sys.path.append(str(fonction_dir))
fonction_message = "message_protocol"
fonction_admin = "admin_page"
imported_message_protocol = __import__(fonction_message)
imported_admin = __import__(fonction_admin)


st.set_page_config(page_title="GAgent", page_icon="🤖", layout="wide")

# Inject custom CSS to style the page


css_page_module = __import__("css_page", fromlist=["inject_custom_css"])

if hasattr(css_page_module, "inject_custom_css"):
    inject_custom_css = getattr(css_page_module, "inject_custom_css")
    print("La fonction inject_custom_css a été importée avec succès!")

    inject_custom_css()
    print("La fonction inject_custom_css a été exécutée avec succès!")
else:
    print("La fonction inject_custom_css n'a pas été trouvée dans css_page.")


if "header_title" not in st.session_state:
    st.session_state.header_title = "GAgent "

if "header_image" not in st.session_state:
    st.session_state.sidebar_image = image_path

st.markdown('<div class="fixed-top">', unsafe_allow_html=True)

# Use HTML to style the title and make it fixed at the top of the page
st.markdown(
    f'<div class="fixed-top"><h1 style="color:#45b7e5; margin: 0; padding: 0;">{st.session_state.header_title}</h1></div>',
    unsafe_allow_html=True,
)  # Use dynamic header title

# Add some space at the top to account for the fixed title
st.markdown('<div class="top-padding"></div>', unsafe_allow_html=True)

def import_function(module_name, function_name):
    try:
        module = __import__(module_name, fromlist=[function_name])
        return getattr(module, function_name)
    except (ImportError, AttributeError) as e:
        st.error(f"Erreur lors de l'importation de {function_name} depuis {module_name}: {e}")
        return None

def file_upload_page():
    file_upload = import_function("upload_page", "file_upload_page")
    if file_upload:
        file_upload()
    else:
        print("La fonction upload page ne fonctionne pas.")


def pdf_page():
    pdf_page_module = import_function("pdf_page","pdf_page")
    if pdf_page:
        pdf_page_module()
    else:
        print("La fonction pdf page ne fonctionne pas")


def admin():
    admin_page = import_function("admin_page","admin")
    if admin_page:
        admin_page()
    else:
        print("La fonction admin_page ne fonctionne pas")

# Importer dynamiquement les fonctions initialize_buttons et get_button_state
initialize_buttons = import_function("admin_page", "initialize_buttons")
get_button_state = import_function("admin_page", "get_button_state")

# Initialiser les boutons une seule fois si la fonction a été correctement importée
if initialize_buttons:
    initialize_buttons()



def main():
    buttons = get_button_state()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown('<div class="content">', unsafe_allow_html=True)
    logo_path = image_path

    if "uploaded_image" in st.session_state:
        st.sidebar.image(st.session_state["uploaded_image"], use_column_width=True)
    else:
        st.sidebar.image(str(logo_path), use_column_width=True)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.sidebar.title("Question")
    col1, col2 = st.columns(2)
    if st.sidebar.button(buttons["button_1_text"]):
        imported_message_protocol.open_link_in_new_tab(buttons['button_1_link'])

    if st.sidebar.button(buttons["button_2_text"]):
        imported_message_protocol.open_link_in_new_tab(buttons['button_2_link'])


    st.sidebar.text(" ")
    st.sidebar.text(" ")
    st.sidebar.text(" ")
    st.sidebar.title("Administrateur")

    if st.sidebar.button("Interface de stockage (Base de connaissance)"):
        st.session_state["page"] = "upload"

    if st.sidebar.button("Administration (Gestion de l'interface)"):
        st.session_state["page"] = "admin"

    user_input = st.chat_input("Je suis à votre écoute. Posez votre question.")
    if user_input:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate and display assistant response
        response = imported_message_protocol.generate_response_stream(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("</div>", unsafe_allow_html=True)

def page_selector():
    if "page" not in st.session_state:
        st.session_state["page"] = "main"

    if st.session_state["page"] == "main":
        main()
    elif st.session_state["page"] == "upload":
        file_upload_page()

    elif st.session_state["page"] == "pdf":
        pdf_page()
    elif st.session_state["page"] == "admin":
        admin()


if __name__ == "__main__":
    page_selector()
