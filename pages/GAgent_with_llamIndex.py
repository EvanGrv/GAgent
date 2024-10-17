import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    get_response_synthesizer,
)
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
import logging
import sys
import streamlit as st
from pathlib import Path
import openai

# Utiliser Path.cwd() pour obtenir le répertoire actuel dans l'environnement Streamlit

base_dir = Path(__file__).resolve().parent
module_dir = base_dir / "API_connection"
module_config = "config"
module_sen_message = "sen_message_LLamaIndex"

if module_dir not in sys.path:
    sys.path.append(str(module_dir))
    print(f"this is module dir {module_dir}")
    print(f"this is BASE dir {base_dir}")

imported_api = __import__(module_config)
if imported_api:
    openai.api_key = imported_api.api_key
    print(f"This is openAI Key : {openai.api_key}")

imported_message = __import__(module_sen_message)

st.set_page_config(page_title="Start", page_icon="🤖")
st.header("Start with LLamaIndex")

# Ajoutez la racine du projet à sys.path
PERSIST_DIR = base_dir / "storage"
DATA_DIR = base_dir / "data"
if PERSIST_DIR and DATA_DIR not in sys.path:
    sys.path.append(str(PERSIST_DIR))
    sys.path.append(str(DATA_DIR))
else:
    print("Persist dir and data dir not found")


print(f"Pass to data {DATA_DIR}")
print(f"Pass to persist dir {PERSIST_DIR}")
# Vérifier si le répertoire de persistence et de données existe
if not PERSIST_DIR.exists():
    if not DATA_DIR.exists():
        raise ValueError(f"Directory {DATA_DIR} does not exist.")

    # Charger les documents et créer l'index
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)

    # Sauvegarder l'index pour une utilisation ultérieure
    index.storage_context.persist(persist_dir=str(PERSIST_DIR))
else:
    # Charger l'index existant
    storage_context = StorageContext.from_defaults(persist_dir=str(PERSIST_DIR))
    index = load_index_from_storage(storage_context)

# Créer le moteur de requêtes
query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)


def start():
    # Initialiser l'historique de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown('<div class="content">', unsafe_allow_html=True)

    # Afficher les messages de chat de l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.sidebar.text(" ")
    st.sidebar.text(" ")
    st.sidebar.text(" ")
    st.sidebar.title("Administrateur")

    user_input = st.chat_input("Je suis à votre écoute. Posez votre question.")
    if user_input:
        # Afficher le message de l'utilisateur dans le chat
        with st.chat_message("user"):
            st.write(user_input)
        # Ajouter le message de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Générer et afficher la réponse de l'assistant
        response = imported_message.generate_stream(user_input)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("</div>", unsafe_allow_html=True)


def page_selector():
    if "page" not in st.session_state:
        st.session_state["page"] = "start"

    if st.session_state["page"] == "start":
        start()


if __name__ == "__main__":
    page_selector()