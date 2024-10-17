import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent

module_dir = base_dir / "API_connection"
module_upload = "upload_file"

if module_dir not in sys.path:
    sys.path.append(str(module_dir))
imported_upload = __import__(module_upload)


def get_save_directory():
    base_path = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(base_path, "uploaded_files")
    os.makedirs(save_directory, exist_ok=True)
    return save_directory


# Fonction pour obtenir le chemin du fichier de sauvegarde
def get_save_path():
    save_directory = get_save_directory()
    return os.path.join(save_directory, "file_list.csv")


# Fonction pour charger les fichiers depuis le disque
def load_files():
    save_path = get_save_path()
    if os.path.exists(save_path):
        return pd.read_csv(save_path).to_dict("records")
    else:
        return []


# Fonction pour sauvegarder les fichiers sur le disque
def save_files(file_list):
    save_path = get_save_path()
    df = pd.DataFrame(file_list)
    df.to_csv(save_path, index=False)


def add_file(uploaded_file, file_list, username, expiration_days):
    save_directory = get_save_directory()
    file_path = os.path.join(save_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    file_info = {
        "Nom du fichier": uploaded_file.name,
        "Type de fichier": uploaded_file.type,
        "Taille du fichier (KB)": uploaded_file.size / 1024,
        "Date d'ajout": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Date d'expiration": (
            datetime.now() + timedelta(days=expiration_days)
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "Nom Administrateur": username,
        "Action": "Added",
    }
    file_list.append(file_info)
    return file_list


# Fonction pour supprimer un fichier
def delete_file(index, file_list, username):
    file_list[index]["Action"] = "Deleted"
    file_list[index]["Deleted By"] = username
    file_list[index]["Date Deleted"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return file_list


def file_upload_page():
    if "file_list" not in st.session_state:
        st.session_state["file_list"] = load_files()

    # Interface Streamlit
    st.title("Interface de stockage")

    # Nom de l'utilisateur
    username = st.text_input("Nom de l'administrateur:")

    # Ajout de fichiers
    uploaded_file = st.file_uploader(
        "Fichier à ajouter", type=["csv", "xlsx", "txt", "pdf", "jpg", "png"]
    )
    expiration_days = st.number_input(
        "Entrer le nombre de jour avant expiration", min_value=1, step=1, value=30
    )
    if uploaded_file is not None and username:
        st.session_state["file_list"] = add_file(
            uploaded_file, st.session_state["file_list"], username, expiration_days
        )
        save_files(st.session_state["file_list"])
        st.success(
            f"Le fichier '{uploaded_file.name}' à bien été ajouté par {username}!"
        )

    # Affichage du tableau des fichiers
    if st.session_state["file_list"]:
        df = pd.DataFrame(st.session_state["file_list"])
        st.dataframe(df)

        # Option pour supprimer un fichier
        delete_index = st.number_input(
            "Entrer le numéro du fichier à supprimer",
            min_value=0,
            max_value=len(st.session_state["file_list"]) - 1,
            step=1,
        )
        if st.button("Delete file") and username:
            st.session_state["file_list"] = delete_file(
                delete_index, st.session_state["file_list"], username
            )
            save_files(st.session_state["file_list"])
            st.success(
                f"Le fichier à l'index {delete_index} à été supprimé par {username}!"
            )
    else:
        st.write("Aucun fichier encore ajouté.")

    if st.sidebar.button("Retourner au menu principal"):
        st.session_state["page"] = "main"
