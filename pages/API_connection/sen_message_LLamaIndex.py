import streamlit as st
import pymongo
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    get_response_synthesizer,
)

import logging
import streamlit.components.v1 as components
import sys
from pathlib import Path
import io
from contextlib import redirect_stdout


base_dir = Path(__file__).resolve().parent
data_dir = Path(__file__).parent
module_dir = base_dir / "API_connection"
module_sen_message = "sen_message"
data_file = data_dir / "data"

if not data_file.exists():
    print(f"Directory {data_file} does not exist. Creating it now.")
    data_dir.mkdir(parents=True, exist_ok=True)

if module_dir not in sys.path:
    sys.path.append(str(module_dir))

imported_message = __import__(module_sen_message)

mongodb_client = pymongo.MongoClient()


if mongodb_client:
    print("Connection is successfull")
else:
    print("Connection failed")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
documents = SimpleDirectoryReader(str(data_file)).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)


def generate_stream(prompt):
    print("ici 4")
    response = query_engine.query(prompt)
    print("ici ecriture")
    print("ici 5")
    print(response.print_response_stream())
    f = io.StringIO()
    with redirect_stdout(f):
        response.print_response_stream()

    # Récupérer la sortie capturée
    result = f.getvalue()

    # Afficher dans Streamlit

    # Retourner la réponse capturée si nécessaire
    return result
