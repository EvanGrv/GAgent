import openai
import sys
from pathlib import Path
from llama_index.core import load_index_from_storage, StorageContext, Settings, Document, VectorStoreIndex, SimpleDirectoryReader
import gradio as gr
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import SentenceSplitter
from llama_index.experimental.query_engine import PandasQueryEngine
from datasets import load_dataset
import pandas as pd
from tqdm import tqdm
import json
from dotenv import load_dotenv
import os

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / 'data'
module_dir = base_dir.parent / "API_connection"
module_config = "config"

if module_dir not in sys.path:
    sys.path.append(str(module_dir))
print(module_config)
imported_api = __import__(module_config)
if imported_api:
    openai.api_key = imported_api.api_key

print(imported_api.api_key)

print(base_dir)
print(data_dir)
print(module_dir)