import openai
import sys
from pathlib import Path
from llama_index.core import  load_index_from_storage, StorageContext

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / 'data'
index_dir = data_dir / 'storage'
module_dir = base_dir.parent / "API_connection"
module_config = "config"
print(module_config)
if module_dir not in sys.path:
    sys.path.append(str(module_dir))
imported_api = __import__(module_config)
if imported_api:
    openai.api_key = imported_api.api_key

print(imported_api.api_key)

storage_context = StorageContext.from_defaults(persist_dir=str(index_dir))
index = load_index_from_storage(storage_context)

qe = index.as_query_engine()
question = qe.query("Que contient le Manuel Opératoire ?")
print(question)

chat = index.as_chat_engine(verbose=True)
question2 = chat.chat("Que contient le Manuel Opératoire")
print(question2)