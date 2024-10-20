import streamlit as st
import sys
from pathlib import Path
import subprocess

source_dir = Path(__file__).resolve().parent.parent.parent
base_dir = Path(__file__).resolve().parent.parent
image_path = base_dir / "files/logo.webp"

module_dir = base_dir / "API_connection"
module_config = "config"

if module_dir not in sys.path:
    sys.path.append(str(module_dir))

imported_config = __import__(module_config)

current_dir = Path(__file__).resolve().parent
bash_script_path = current_dir / 'bash' / 'start_streamlit.sh'


def initialize_buttons():
    """Initialise les boutons une seule fois dans session_state"""
    if "initialized" not in st.session_state:
        st.session_state.button_1_text = "Question 1"
        st.session_state.button_1_link = ""
        st.session_state.button_2_text = "Question 2"
        st.session_state.button_2_link = ""
        st.session_state.initialized = True

def get_button_state():
    """Retourne l'état actuel des boutons"""
    return {
        "button_1_text": st.session_state.button_1_text,
        "button_1_link": st.session_state.button_1_link,
        "button_2_text": st.session_state.button_2_text,
        "button_2_link": st.session_state.button_2_link,
    }

def update_buttons(button_1_text, button_1_link, button_2_text, button_2_link):
    """Mise à jour des boutons dans session_state"""
    st.session_state.button_1_text = button_1_text
    st.session_state.button_1_link = button_1_link
    st.session_state.button_2_text = button_2_text
    st.session_state.button_2_link = button_2_link


def update_config(new_assistant_id, new_thread_id):
    config_file_path = source_dir / ".env"
    with config_file_path.open("r") as f:
        lines = f.readlines()
    new_lines = []

    for line in lines:
        if line.startswith("ASSISTANT_ID"):
            new_lines.append(f"ASSISTANT_ID='{new_assistant_id}'\n")
        elif line.startswith("THREAD_ID"):
            new_lines.append(f"THREAD_ID='{new_thread_id}'\n")
        else:
            new_lines.append(line)
    with config_file_path.open("w") as f:
        f.writelines(new_lines)


def admin():
    buttons = get_button_state()

    st.title("Administration")

    # Sidebar input for header title
    new_header_title = st.text_input(
        "Titre de la page", st.session_state.header_title
    )  # Text input for header title
    if st.button("Changer le tire"):
        st.session_state.header_title = (
            new_header_title  # Update header title in session state
        )
        st.success("Le titre à été changé avec succès!")

    st.sidebar.text(" ")

    uploaded_file = st.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg", "gif"]
    )
    if uploaded_file is not None:
        # Save the uploaded file to a session state variable
        st.session_state["uploaded_image"] = uploaded_file

    # Display the uploaded image in the sidebar if it exists
    if "uploaded_image" in st.session_state:
        st.sidebar.image(st.session_state["uploaded_image"], use_column_width=True)
    else:
        st.sidebar.image(str(image_path), use_column_width=True)

    st.sidebar.text(" ")

    new_assistant_id = st.text_input("Assistant ID", imported_config.assistant_id)
    new_thread_id = st.text_input("Thread ID", imported_config.thread_id)

    if st.button("Mettre à jour les configurations"):
        update_config(new_assistant_id, new_thread_id)
        try:
            result = subprocess.run(['bash', bash_script_path], check=True, capture_output=True, text=True)
            print("Script exécuté avec succès")
            print("Sortie du script :")
            print(result.stdout)  # Affiche la sortie du script Bash
        except subprocess.CalledProcessError as e:
            print(f"Le script a échoué avec l'erreur : {e.returncode}")
            print(f"Erreur : {e.stderr}")
        st.success("Configurations mises à jour !")

    st.title("Modification des boutons")

    button_1_text = st.text_input("Texte du bouton 1", buttons["button_1_text"])
    button_1_link = st.text_input("Lien du bouton 1", buttons["button_1_link"])

    button_2_text = st.text_input("Texte du bouton 2", buttons["button_2_text"])
    button_2_link = st.text_input("Lien du bouton 2", buttons["button_2_link"])

    # Sauvegarde des modifications dans session_state
    if st.button("Sauvegarder"):
        update_buttons(button_1_text, button_1_link, button_2_text, button_2_link)
        st.success("Modifications enregistrées avec succès !")





    if st.sidebar.button("Retourner au menu principal"):
        st.session_state["page"] = "main"

