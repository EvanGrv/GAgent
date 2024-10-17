#!/bin/bash

# Obtenir le répertoire du script Bash actuel
SCRIPT_DIR=$(dirname "$0")

# Obtenir le chemin vers la racine du projet (remonter de deux niveaux dans l'arborescence)
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/../../..")

# Afficher une boîte de dialogue avec Zenity pour démarrer l'application Streamlit
zenity --question --text="Voulez-vous démarrer l'application Streamlit ?" --title="Lancer Streamlit"

# Vérifier si l'utilisateur a appuyé sur "Oui"
if [ $? == 0 ]; then
    # Lancer Streamlit avec le chemin vers app.py qui est à la racine du projet
    streamlit run "$PROJECT_ROOT/Accueil_🧊.py"
else
    echo "Démarrage annulé."
fi
