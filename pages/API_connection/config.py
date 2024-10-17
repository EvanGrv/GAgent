from pathlib import Path
import sys
import importlib.util

# Obtenir le chemin racine du projet (3 niveaux au-dessus du fichier config.py)
racine_projet = Path(__file__).resolve().parent.parent.parent

# Ajouter la racine du projet à sys.path pour que les imports fonctionnent dynamiquement
sys.path.append(str(racine_projet))

# Chemin vers le fichier settings.py
settings_path = racine_projet / "settings.py"

# Charger dynamiquement le module settings.py
spec = importlib.util.spec_from_file_location("settings", settings_path)
settings = importlib.util.module_from_spec(spec)
spec.loader.exec_module(settings)

# Maintenant, nous avons accès à settings.SETTINGS
assistant_id = settings.SETTINGS.ASSISTANT_ID
thread_id = settings.SETTINGS.THREAD_ID
api_key = settings.SETTINGS.API_KEY
mongo_uri = settings.SETTINGS.MONGO_URI

# Afficher la clé API pour vérification
print(f"[config.py] API_KEY: {api_key}")
print(f"[config.py] ASSISTANT_ID: {assistant_id}")
print(f"[config.py] THREAD_ID: {thread_id}")
print(f"[config.py] MONGO_URI: {mongo_uri}")
