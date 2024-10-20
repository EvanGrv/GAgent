from dotenv import load_dotenv
from pathlib import Path
from historique_conversation import note_engine
from llama_index.core.tools import QueryEngineTool,ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from prompts import data_engine, paragraphe
from llama_index.core import Settings
import openai
import sys


load_dotenv()
base_dir = Path(__file__).resolve().parent
data_dir = base_dir / 'data'
module_dir = base_dir.parent / "API_connection"
module_config = "config"
print(module_config)
if module_dir not in sys.path:
    sys.path.append(str(module_dir))
imported_api = __import__(module_config)
if imported_api:
    openai.api_key = imported_api.api_key

print(imported_api.api_key)


tools = [
    note_engine,
    QueryEngineTool(
        query_engine= data_engine,
        metadata=ToolMetadata(
            name="data_data",
            description=" Toutes les informations à propos du manuel opératoire",
        ),
    ),
]
llm = OpenAI(model="gpt-4o")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context =paragraphe)

while(prompt := input("Enter a promp (q to quit): ")) != "q":
    result = agent.query(prompt)
    result2 = data_engine.retrieve(prompt)
    result3 = data_engine.query(prompt)
    print(tools)
    print(result)
    print("Retriever ---------------------------:", result2)
    print("Query Engine -----------------------------:", result3.pr)



